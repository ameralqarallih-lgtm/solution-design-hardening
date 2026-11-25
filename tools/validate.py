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
assert ids==[f'SDP-{i:03}' for i in range(1,236)], 'Catalog IDs missing or reordered'
playbook_ids=[]
for p in sorted((skill/'references').glob('problems-*.md')):
    sections=re.split(r'^## (SDP-\d{3}) — .+$',p.read_text(),flags=re.M)
    for i in range(1,len(sections),2):
        playbook_ids.append(sections[i])
        for field in ('**Failure:**','**Detection:**','**Remediation and safeguards:**','**Verification:**'):
            assert field in sections[i+1], (p,sections[i],field)
assert sorted(playbook_ids)==sorted(ids), 'Missing or duplicate playbook entries'
for md in root.rglob('*.md'):
    for link in re.findall(r'\]\(([^)]+)\)',md.read_text()):
        if not link.startswith(('http:','https:','#')):
            assert (md.parent/link.split('#')[0]).exists(), (md,link)
cases=json.loads((root/'evals/cases.json').read_text())
assert len({c['id'] for c in cases})==len(cases)
for c in cases:
    assert c['scenario'] and c['expected'] and set(c['problem_ids'])<=set(ids)
capability_dir=skill/'references/technology/capabilities'
assert len(list(capability_dir.glob('*.md')))==17
for profile in capability_dir.glob('*.md'):
    for heading in ('## Discover and verify','## Implementation decisions','## Counterexamples and limits','## Verification'):
        assert heading in profile.read_text(), (profile,heading)
assert len(cases)==66
from scan import RULES
assert len(RULES)==27 and len({r[0] for r in RULES})==27
assert {r[1] for r in RULES}<=set(ids)
assert (skill/'references/INTEGRATION-VERIFICATION.md').is_file()
assert len(list((skill/'references/technologies').glob('*.md')))==13
mapped=re.findall(r'^\| (SDP-\d{3}) \|', (skill/'references/SECURITY-STANDARDS.md').read_text(),re.M)
assert len(mapped)==len(set(mapped)) and set(mapped)<=set(ids) and set(ids[160:])<=set(mapped)
assert len(list((skill/'references').glob('problems-*.md')))==24
assert (skill/'assets/threat-model.md').is_file()
assert (skill/'assets/architecture-model.md').is_file()
assert (skill/'references/ARCHITECTURAL-INTELLIGENCE.md').is_file()
from correlate import analyze
assert not analyze(json.loads((root/'examples/architecture-model.json').read_text()),set(ids))['unassigned_findings']
print(f'PASS: skill metadata, internal links, {len(ids)} sequential problem IDs and complete playbook coverage, {len(cases)} evaluation cases. No agent evaluations executed.')

gold=json.loads((root/'evals/gold-findings.json').read_text())
assert len(gold)==16 and sum(not v for v in gold.values())==5 and set(gold)<={c['id'] for c in cases}
assert all(isinstance(v,list) and len(set(v))==len(v) and all(isinstance(x,str) and x for x in v) for v in gold.values())
activation=json.loads((root/'evals/activation-cases.json').read_text())
assert len(activation)==8 and len({c['id'] for c in activation})==8 and sum(c['relevant'] for c in activation)==4
assert all(c['prompt'] and type(c['relevant']) is bool for c in activation)
from context import select
assert len(select(ids)['playbooks'])==24
print('PASS: 16 labeled detection cases, 8 activation probes and complete reference routing.')
