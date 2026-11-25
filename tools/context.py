"""Plan selective reference loading; UTF-8 bytes are not model tokens."""
import argparse,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'skills/solution-design-hardening'

def select(ids, root=ROOT):
    index={}
    for path in sorted((root/'references').glob('problems-*.md')):
        for m in re.finditer(r'^## (SDP-\d{3}) — .+$',path.read_text(encoding='utf-8'),re.M):
            if m[1] in index: raise ValueError('duplicate problem ID')
            index[m[1]]=path
    if not ids or not set(ids)<=index.keys(): raise ValueError('explicit known IDs required')
    paths=sorted({index[i] for i in ids})
    files=[dict(path=p.relative_to(root).as_posix(),utf8_bytes=p.stat().st_size,requested_ids=sorted({i for i in ids if index[i]==p})) for p in paths]
    return dict(requested_ids=sorted(set(ids)),playbooks=files,selected_playbook_bytes=sum(f['utf8_bytes'] for f in files),all_playbook_bytes=sum(p.stat().st_size for p in set(index.values())),core_skill_bytes=(root/'SKILL.md').stat().st_size,warning='Routing aid only; add related problems and applicable capability, security and architecture references. Bytes are not tokens or measured savings.')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('ids',nargs='+'); a=p.parse_args(); print(json.dumps(select(a.ids),indent=2))
