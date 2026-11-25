"""Read-only architecture candidates from bounded local files; not a call graph or runtime topology."""
import argparse
import hashlib
import json
import os
import re
import stat
import xml.etree.ElementTree as ET
from pathlib import Path
from scan import COMPILED, SKIP, EXT

MAX_BYTES = 1024 * 1024
PROJECTS = {'package.json', 'pyproject.toml', 'pom.xml', 'build.gradle', 'build.gradle.kts', 'go.mod', 'Cargo.toml', 'composer.json', 'Gemfile', 'mix.exs', 'pubspec.yaml', 'Package.swift'}
PROJECT_SUFFIXES = {'.csproj', '.fsproj', '.vbproj'}
SIGNALS = [
    ('transaction-start', r'\b(?:BeginTransaction(?:Async)?|begin_transaction|beginTransaction|atomic|transaction)\s*\(|\bBEGIN\s+TRANSACTION\b'),
    ('commit', r'\b(?:commit|CommitAsync|Commit|SaveChanges(?:Async)?)\s*\(|\bCOMMIT\s*;'),
    ('rollback', r'\b(?:rollback|Rollback(?:Async)?)\s*\('),
    ('message-publish', r'\b(?:publish|PublishAsync|Publish|basic_publish|send_message)\s*\('),
    ('message-ack', r'\b(?:basic_ack|ack|BasicAck(?:Async)?|acknowledge)\s*\('),
    ('external-call', r'\b(?:requests\.(?:get|post|put|delete|patch)|fetch|SendAsync|httpx\.(?:get|post)|charge)\s*\('),
    ('cache-operation', r'\b(?:cache|redis)\.(?:get|set|delete|invalidate|remove|GetAsync|SetAsync|RemoveAsync)\s*\('),
    ('authorization', r'\b(?:Authorize(?:Async)?|AllowAnonymous|authorize|check_permission|has_permission)\b'),
    ('input-boundary', r'\b(?:app|router)\.(?:get|post|put|patch|delete|route)\s*\(|\[Http(?:Get|Post|Put|Patch|Delete)\b'),
    ('background-entry', r'\b(?:BackgroundService|ExecuteAsync|Celery|CronJob|BackgroundTasks)\b'),
    ('tenant-context', r'\b(?:tenant_id|tenantId|TenantId)\b'),
    ('constraint', r'\b(?:UNIQUE|CHECK|FOREIGN\s+KEY)\s*\(|\bHasIndex\s*\('),
]
PATTERNS = [(kind, re.compile(pattern)) for kind, pattern in SIGNALS]
SECRET = re.compile(r'(^|[._-])(secrets?|credentials?|private[-_]key|env)([._-]|$)', re.I)


def stable(prefix, *parts):
    return prefix + '-' + hashlib.sha256('\0'.join(str(x) for x in parts).encode()).hexdigest()[:16]


def inspect(root, max_files=20000):
    root = Path(root).resolve()
    if not root.is_dir() or max_files < 1:
        raise ValueError('root must be a directory and max_files positive')
    files, skipped, warnings = {}, {'excluded': 0, 'oversize_or_unreadable': 0}, []
    truncated = False
    for base, dirs, names in os.walk(root, followlinks=False, onerror=lambda _: warnings.append('Directory unreadable')):
        dirs[:] = sorted(d for d in dirs if d not in SKIP and not d.startswith('.') and not (Path(base)/d).is_symlink() and not SECRET.search(d))
        for name in sorted(names):
            p = Path(base)/name
            if name.startswith('.') or SECRET.search(name) or p.is_symlink():
                skipped['excluded'] += 1; continue
            if name not in PROJECTS and p.suffix.lower() not in PROJECT_SUFFIXES | EXT:
                continue
            if len(files) >= max_files:
                truncated = True; break
            try:
                info = p.stat()
                if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_BYTES:
                    skipped['oversize_or_unreadable'] += 1; continue
                # Bounded read, including if a file grows after stat.
                with p.open('rb') as f:
                    raw = f.read(MAX_BYTES + 1)
                if len(raw) > MAX_BYTES: raise ValueError('oversize')
                # Keep only paths, parsed local references and matched signal metadata, not raw files.
                text = raw.decode('utf-8')
            except (OSError, UnicodeError, ValueError):
                skipped['oversize_or_unreadable'] += 1; continue
            rel = p.relative_to(root).as_posix()
            markers, risks, refs = [], [], []
            project = name in PROJECTS or p.suffix.lower() in PROJECT_SUFFIXES
            if project:
                try:
                    if p.suffix.lower() in PROJECT_SUFFIXES:
                        if re.search(r'<!\s*(?:DOCTYPE|ENTITY)', text, re.I): raise ValueError('DTD not accepted')
                        tree = ET.fromstring(text)
                        refs = [(e.get('Include',''), 'project-reference') for e in tree.iter() if e.tag.split('}')[-1]=='ProjectReference']
                    elif name == 'package.json':
                        data = json.loads(text)
                        if not isinstance(data, dict): raise ValueError('not object')
                        for key in ('dependencies','devDependencies','optionalDependencies','peerDependencies'):
                            values = data.get(key,{})
                            if isinstance(values,dict):
                                refs.extend((v.split(':',1)[1], 'declared-local-package') for v in values.values() if isinstance(v,str) and v.startswith(('file:','link:')))
                except (ET.ParseError, ValueError, TypeError):
                    warnings.append(f'Manifest parse incomplete: {rel}')
            if p.suffix.lower() in EXT:
                for n,line in enumerate(text.splitlines(),1):
                    for kind,pat in PATTERNS:
                        if pat.search(line): markers.append((kind,n))
                    for rule,pid,pat,hint,suffixes in COMPILED:
                        if (suffixes is None or p.suffix.lower() in suffixes) and pat.search(line): risks.append((rule,pid,n))
            files[rel] = (project, refs, markers, risks)
        if truncated: break
    manifests = {}
    for rel,(project,*_) in files.items():
        if project: manifests.setdefault(Path(rel).parent.as_posix(),[]).append(rel)
    components = [{'id':stable('CMP',d),'directory':d,'manifests':sorted(paths),'status':'Candidate','kind':'project-directory'} for d,paths in sorted(manifests.items())]
    if '.' not in manifests:
        components.append({'id':stable('CMP','.'),'directory':'.','manifests':[],'status':'Candidate','kind':'unassigned-root'})
    by_dir = {c['directory']:c['id'] for c in components}
    def owner(rel):
        return next(by_dir[d.as_posix()] for d in Path(rel).parents if d.as_posix() in by_dir)
    edges, markers, risks, unresolved = [], [], [], []
    for rel,(_,refs,signals,hits) in sorted(files.items()):
        src = owner(rel)
        for ref,kind in refs:
            # Only link to an already inventoried local manifest; never read target or emit raw reference.
            if not ref or re.search(r'[$*?\x00]|://',ref) or Path(ref).is_absolute() or re.match(r'^[A-Za-z]:',ref):
                unresolved.append({'manifest':rel,'kind':kind,'status':'Requires Verification'}); continue
            try:
                target = (root/rel).parent / ref.replace('\\','/')
                # lexical normalization: do not follow symlinks or read outside the root
                target = Path(os.path.abspath(target)).relative_to(root).as_posix()
            except (ValueError,OSError):
                unresolved.append({'manifest':rel,'kind':kind,'status':'Requires Verification'}); continue
            target_dir = Path(target).parent.as_posix() if target in files and files[target][0] else target
            valid = (kind == 'project-reference' and target in files and files[target][0] and Path(target).suffix.lower() in PROJECT_SUFFIXES) or (kind == 'declared-local-package' and (Path(target)/'package.json').as_posix() in files)
            if valid and target_dir in manifests:
                dst = by_dir[target_dir]
                edge = {'id':stable('DEP',src,dst,rel,kind),'source':src,'target':dst,'kind':kind,'evidence':{'path':rel},'status':'Declared; runtime unverified'}
                if edge not in edges: edges.append(edge)
            else: unresolved.append({'manifest':rel,'kind':kind,'status':'Requires Verification'})
        for kind,n in signals:
            markers.append({'id':stable('SIG',rel,n,kind),'component':src,'path':rel,'line':n,'kind':kind,'status':'Requires Verification'})
        for rule,pid,n in hits:
            risks.append({'id':stable('RSK',rel,n,rule),'component':src,'path':rel,'line':n,'rule_id':rule,'problem_id':pid,'status':'Requires Verification'})
    # Co-location is a triage hint only, not shared root cause or execution order.
    groups = {}
    for hit in risks:
        groups.setdefault((hit['component'],hit['path']),[]).append(hit)
    investigations = [{'component':c,'path':p,'candidate_ids':[h['id'] for h in hs],'problem_ids':sorted({h['problem_id'] for h in hs}),'basis':'same file only','status':'Requires Verification'} for (c,p),hs in sorted(groups.items()) if len({h['problem_id'] for h in hs})>1]
    return {'schema_version':1,'scope':'local static candidate inventory','components':components,'declared_dependencies':sorted(edges,key=lambda e:e['id']),'unresolved_references':unresolved,'boundary_signals':markers,'risk_candidates':risks,'investigation_groups':investigations,'coverage':{'inspected_files':len(files),'skipped':skipped,'truncated':truncated,'warnings':warnings},'limitations':['Directory grouping is provisional; multiple projects can share a directory.','Only .NET project and npm file/link references are extracted; other dependency types require manual tracing.','Signals can match comments, tests or unrelated code; line order is not execution order.','No runtime call graph, transaction scope, trust crossing, business invariant or root cause is inferred.','No source lines, raw reference values or configuration secrets are emitted; paths can still be sensitive.','Hidden/generated/secret-named files and symlinks are excluded; exclusions and unreadable files are not proof of absence.']}


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('root',type=Path); p.add_argument('--max-files',type=int,default=20000); a=p.parse_args()
    try: print(json.dumps(inspect(a.root,a.max_files),indent=2))
    except ValueError as e: p.error(str(e))
