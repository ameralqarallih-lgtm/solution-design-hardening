"""Offline structural validation, not agent evaluation. Python 3 standard library."""
from pathlib import Path
import re,json
root=Path(__file__).resolve().parents[1]
skill=root/'skills/solution-design-hardening'
s=(skill/'SKILL.md').read_text()
assert s.startswith('---\n')
header=s.split('---',2)[1]
assert re.search(r'^name: solution-design-hardening$',header,re.M)
assert 0<len(re.search(r'^description: (.+)$',header,re.M)[1])<=1024
assert len(s.splitlines())<500
ids=re.findall(r'^\| (SDP-\d{3}) \|', (skill/'references/SOLUTION-DESIGN-PROBLEMS.md').read_text(),re.M)
assert ids==[f'SDP-{i:03}' for i in range(1,125)], 'Catalog IDs missing or reordered'
for md in skill.rglob('*.md'):
    for link in re.findall(r'\]\(([^)]+)\)',md.read_text()):
        if not link.startswith(('http:','https:','#')):
            assert (md.parent/link.split('#')[0]).exists(), (md,link)
cases=json.loads((root/'evals/cases.json').read_text())
assert len({c['id'] for c in cases})==len(cases)
for c in cases:
    assert c['scenario'] and c['expected'] and set(c['problem_ids'])<=set(ids)
print(f'PASS: skill metadata, internal links, {len(ids)} sequential problem IDs, {len(cases)} evaluation cases. No agent evaluations executed.')
