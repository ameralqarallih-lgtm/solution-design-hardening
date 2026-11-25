"""Read-only manifest inventory; no execution, network, or capability inference."""
import argparse, json, os, re
from pathlib import Path

SKIP={'.git','node_modules','vendor','bin','obj','.venv','venv','dist','build','__pycache__','target'}
MANIFESTS={'package.json':'JavaScript','package-lock.json':'JavaScript lockfile','pnpm-lock.yaml':'JavaScript lockfile','yarn.lock':'JavaScript lockfile','pom.xml':'JVM','build.gradle':'JVM','build.gradle.kts':'JVM','gradle.lockfile':'JVM lockfile','pyproject.toml':'Python','requirements.txt':'Python','poetry.lock':'Python lockfile','uv.lock':'Python lockfile','go.mod':'Go','go.sum':'Go checksum file','Cargo.toml':'Rust','Cargo.lock':'Rust lockfile','composer.json':'PHP','composer.lock':'PHP lockfile','Gemfile':'Ruby','Gemfile.lock':'Ruby lockfile','mix.exs':'Elixir','mix.lock':'Elixir lockfile','pubspec.yaml':'Dart','pubspec.lock':'Dart lockfile','Package.swift':'Swift','packages.lock.json':'.NET lockfile','global.json':'.NET SDK','Dockerfile':'Container build','compose.yaml':'Container composition','compose.yml':'Container composition','docker-compose.yml':'Container composition','docker-compose.yaml':'Container composition','Chart.yaml':'Helm chart'}
# Only emit strictly constrained version tokens, never arbitrary manifest strings.
VERSION=re.compile(r'^[vV]?[0-9]+(?:\.[0-9]+){0,3}(?:[-+][A-Za-z0-9.]{1,24})?$')

def safe_version(value):
    return value if isinstance(value,str) and len(value)<=40 and VERSION.fullmatch(value) else None

def classify(name):
    if name in MANIFESTS: return MANIFESTS[name]
    if name.endswith(('.csproj','.fsproj','.vbproj')): return '.NET'
    if name.endswith('.tf'): return 'Terraform'
    if name.startswith('Dockerfile.'): return 'Container build'
    return None

def extract_version(p):
    # Selected metadata only; no parsing arbitrary dependency URLs, credentials or source lines.
    if p.name not in {'global.json','go.mod'} and p.suffix not in {'.csproj','.fsproj','.vbproj'}: return None
    try:
        if p.stat().st_size>1024*1024: return None
        raw=p.read_text(encoding='utf-8')
        if p.name=='global.json':
            sdk=json.loads(raw).get('sdk',{})
            return safe_version(sdk.get('version')) if isinstance(sdk,dict) else None
        if p.name=='go.mod':
            m=re.search(r'^go\s+(\S+)\s*$',raw,re.M)
            return safe_version(m[1]) if m else None
        # A target framework is not an installed runtime version; leave it unreported.
    except (OSError,UnicodeError,ValueError,AttributeError): pass
    return None

def discover(root):
    root=Path(root).resolve(); records=[]; errors=[]
    for base,dirs,files in os.walk(root,followlinks=False,onerror=lambda e:errors.append('A directory could not be read')):
        dirs[:]=sorted(d for d in dirs if d not in SKIP and not d.startswith('.') and not (Path(base)/d).is_symlink())
        for name in sorted(files):
            p=Path(base)/name; kind=classify(name)
            if not kind or p.is_symlink() or not p.is_file(): continue
            records.append({'path':p.relative_to(root).as_posix(),'technology_signal':kind,'declared_toolchain_version':extract_version(p),'resolved_version':None,'deployed_version':None,'capability_status':'Unknown'})
    return {'scope':'allowlisted manifest signals only; no deployed version or capability verification','signals':records,'warnings':errors,'limitations':['Does not parse dependency inventories or deployment configuration.','Unlisted or custom technologies require manual discovery.','Presence of a manifest does not prove active use.','Hidden directories, symlinks and common generated directories are skipped.']}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('root',type=Path); a=parser.parse_args()
    if not a.root.is_dir(): parser.error('root must be a directory')
    print(json.dumps(discover(a.root),indent=2))
