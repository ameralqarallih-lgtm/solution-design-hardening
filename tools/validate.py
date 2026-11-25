"""Offline structural validation, not agent evaluation. Python 3 standard library."""
from pathlib import Path
import re,json

from context import PROBLEM_HEADING, index, select

root=Path(__file__).resolve().parents[1]
skill=root/'skills/solution-design-hardening'
s=(skill/'SKILL.md').read_text(encoding='utf-8')
assert s.startswith('---\n')
header=s.split('---',2)[1]
assert re.search(r'^name: solution-design-hardening$',header,re.M)
assert 0<len(re.search(r'^description: (.+)$',header,re.M)[1])<=1024
if len(s.splitlines())>=500:
    # Agent Skills best-practice guidance, not a requirement: never trim knowledge to satisfy it.
    print(f'NOTE: SKILL.md has {len(s.splitlines())} lines; guidance suggests moving detail into references. Not a failure.')
ids=re.findall(r'^\| (SDP-\d{3}) \|', (skill/'references/SOLUTION-DESIGN-PROBLEMS.md').read_text(encoding='utf-8'),re.M)
assert ids==[f'SDP-{i:03}' for i in range(1,236)], 'Catalog IDs missing or reordered'
problem_dir=skill/'references/problems'
problem_files=sorted(problem_dir.glob('SDP-*.md'))
assert [f.stem for f in problem_files]==ids, 'Missing or extra problem files'
for f in problem_files:
    text=f.read_text(encoding='utf-8')
    m=PROBLEM_HEADING.match(text)
    assert m and m[1]==f.stem, (f,'heading')
    for field in ('**Failure:**','**Detection:**','**Remediation and safeguards:**','**Verification:**'):
        assert field in text, (f,field)
    for rel in re.findall(r'SDP-\d{3}',text.split('**Related:**',1)[1]) if '**Related:**' in text else []:
        assert rel in ids and rel!=f.stem, (f,rel)
routes=index(skill)
assert sorted(routes)==ids, 'Domain indexes must list every problem exactly once'
for domain in sorted((skill/'references').glob('problems-*.md')):
    text=domain.read_text(encoding='utf-8')
    assert text.count('- **Decision:**')==1, (domain,'one shared decision rule')
problem_index=(skill/'references/PROBLEM-INDEX.md').read_text(encoding='utf-8')
for domain in sorted((skill/'references').glob('problems-*.md')):
    assert f']({domain.name})' in problem_index, (domain.name,'missing from PROBLEM-INDEX')
def covered(text):
    out=set()
    for a,b in re.findall(r'SDP-(\d{3})[-–](\d{3})',text):
        out|={f'SDP-{i:03}' for i in range(int(a),int(b)+1)}
    return out
assert covered(problem_index)>=set(ids), 'PROBLEM-INDEX ranges must cover every ID'
detection=(skill/'references/DETECTION-GUIDANCE.md').read_text(encoding='utf-8')
detection_scopes=[l.split('|')[1] for l in detection.splitlines() if l.startswith('| SDP-')]
detection_ids=set()
for scope in detection_scopes:
    for a,b in re.findall(r'(\d{3})[-–](\d{3})',scope):
        detection_ids|={f'SDP-{i:03}' for i in range(int(a),int(b)+1)}
assert detection_ids>=set(ids), 'DETECTION-GUIDANCE ranges must cover every ID'
for heading in ('## Select the operating mode','## Select the depth and load only what it needs','## Safety and evidence boundaries','## Workflow','## Mandatory engineering safeguards','## Correctness gates'):
    assert heading in s, ('SKILL.md heading',heading)
for md in root.rglob('*.md'):
    if set(md.relative_to(root).parts) & {'.git', '.venv', 'benchmark-runs'}:
        continue
    for link in re.findall(r'\]\(([^)]+)\)',md.read_text(encoding='utf-8')):
        if not link.startswith(('http:','https:','#')):
            assert (md.parent/link.split('#')[0]).exists(), (md,link)
cases=json.loads((root/'evals/cases.json').read_text(encoding='utf-8'))
assert len({c['id'] for c in cases})==len(cases)
for c in cases:
    assert c['scenario'] and c['expected'] and set(c['problem_ids'])<=set(ids)
capability_dir=skill/'references/technology/capabilities'
assert len(list(capability_dir.glob('*.md')))==17
for profile in capability_dir.glob('*.md'):
    for heading in ('## Discover and verify','## Implementation decisions','## Counterexamples and limits','## Verification'):
        assert heading in profile.read_text(encoding='utf-8'), (profile,heading)
assert len(cases)==66
from scan import RULES
assert len(RULES)==27 and len({r[0] for r in RULES})==27
assert {r[1] for r in RULES}<=set(ids)
assert (skill/'references/INTEGRATION-VERIFICATION.md').is_file()
assert len(list((skill/'references/technologies').glob('*.md')))==13
mapped=re.findall(r'^\| (SDP-\d{3}) \|', (skill/'references/SECURITY-STANDARDS.md').read_text(encoding='utf-8'),re.M)
assert len(mapped)==len(set(mapped)) and set(mapped)<=set(ids) and set(ids[160:])<=set(mapped)
assert len(list((skill/'references').glob('problems-*.md')))==24
assert (skill/'assets/threat-model.md').is_file()
assert (skill/'assets/architecture-model.md').is_file()
assert (skill/'references/ARCHITECTURAL-INTELLIGENCE.md').is_file()
from correlate import analyze
assert not analyze(json.loads((root/'examples/architecture-model.json').read_text(encoding='utf-8')),set(ids))['unassigned_findings']
print(f'PASS: skill metadata, internal links, {len(ids)} sequential problem IDs, per-problem files and domain indexes, {len(cases)} evaluation cases. No agent evaluations executed.')

gold=json.loads((root/'evals/gold-findings.json').read_text(encoding='utf-8'))
assert len(gold)==16 and sum(not v for v in gold.values())==5 and set(gold)<={c['id'] for c in cases}
assert all(isinstance(v,list) and len(set(v))==len(v) and all(isinstance(x,str) and x for x in v) for v in gold.values())
activation=json.loads((root/'evals/activation-cases.json').read_text(encoding='utf-8'))
assert len(activation)==8 and len({c['id'] for c in activation})==8 and sum(c['relevant'] for c in activation)==4
assert all(c['prompt'] and type(c['relevant']) is bool for c in activation)
assert len(select(ids)['playbooks'])==24 and len(select(ids)['problems'])==235
print('PASS: 16 labeled detection cases, 8 activation probes and complete reference routing.')
