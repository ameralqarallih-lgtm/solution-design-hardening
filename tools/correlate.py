"""Check an analyst-authored architecture model and summarize explicit risk relationships.
Does not validate evidence truth, discover causal relationships, or authorize remediation.
"""
import argparse
import json
import re
from pathlib import Path

ID = re.compile(r'^[A-Za-z][A-Za-z0-9_-]{0,63}$')
KINDS = ('components','evidence','flows','invariants','root_causes','findings','tasks')


def analyze(model, known):
    if not isinstance(model,dict) or model.get('schema_version') != 1:
        raise ValueError('expected architecture model schema_version 1')
    tables={}; all_ids=set()
    for kind in KINDS:
        rows=model.get(kind)
        if not isinstance(rows,list): raise ValueError(f'{kind} must be a list')
        table={}
        for row in rows:
            if not isinstance(row,dict): raise ValueError(f'{kind}: object required')
            i=row.get('id')
            if not isinstance(i,str) or not ID.fullmatch(i) or i in all_ids: raise ValueError(f'{kind}: invalid or duplicate ID')
            table[i]=row; all_ids.add(i)
        tables[kind]=table
    def links(row, field, target, required=False):
        v=row.get(field,[])
        if not isinstance(v,list) or any(not isinstance(x,str) or x not in target for x in v) or len(set(v))!=len(v) or (required and not v):
            raise ValueError(f'{row["id"]}: invalid {field}')
        return v
    def choice(row,field,options):
        if row.get(field) not in options: raise ValueError(f'{row["id"]}: invalid {field}')
    def nonempty(row,field):
        if not isinstance(row.get(field),str) or not row[field].strip(): raise ValueError(f'{row["id"]}: missing {field}')
    for r in tables['evidence'].values():
        nonempty(r,'locator'); choice(r,'kind',('source','config','test','runtime','documentation','requirement'))
    for kind in ('components','flows','invariants','root_causes','findings'):
        for r in tables[kind].values():
            choice(r,'status',('candidate','supported','unknown'))
            links(r,'evidence_ids',tables['evidence'],r['status']=='supported')
    for r in tables['components'].values(): nonempty(r,'name')
    for r in tables['flows'].values():
        for f in ('source','target'):
            if not isinstance(r.get(f),str) or r[f] not in tables['components']: raise ValueError(f'{r["id"]}: invalid {f}')
        choice(r,'trust_crossing',('yes','no','unknown')); choice(r,'transaction_relation',('same-local','separate','unknown','not-applicable'))
        nonempty(r,'effect'); nonempty(r,'failure_boundary')
    for r in tables['invariants'].values():
        nonempty(r,'requirement'); nonempty(r,'scope'); nonempty(r,'enforcement');
        if r.get('owner') is not None and (not isinstance(r['owner'],str) or r['owner'] not in tables['components']): raise ValueError(f'{r["id"]}: invalid owner')
        if r['status']=='supported' and r.get('owner') is None: raise ValueError(f'{r["id"]}: supported invariant needs owner')
        links(r,'flow_ids',tables['flows'])
    for r in tables['root_causes'].values(): nonempty(r,'mechanism')
    for r in tables['findings'].values():
        links(r,'problem_ids',known,True); links(r,'component_ids',tables['components'],True)
        links(r,'flow_ids',tables['flows']); links(r,'invariant_ids',tables['invariants']); links(r,'root_cause_ids',tables['root_causes'])
        choice(r,'severity',('Critical','High','Medium','Low','Unknown'))
    assigned=set(); dependencies={}
    for r in tables['tasks'].values():
        assigned.update(links(r,'finding_ids',tables['findings'],True))
        dependencies[r['id']]=set(links(r,'depends_on',tables['tasks']))
        nonempty(r,'acceptance'); choice(r,'kind',('remediation','verification'))
    # Stable topological waves; never invent dependencies from co-location.
    waves=[]; done=set(); remaining=set(dependencies)
    while remaining:
        ready=sorted(i for i in remaining if dependencies[i]<=done)
        if not ready: raise ValueError('task dependency cycle')
        waves.append(ready); done.update(ready); remaining.difference_update(ready)
    groups=[]
    for target,field in (('root_causes','root_cause_ids'),('invariants','invariant_ids')):
        for i,r in sorted(tables[target].items()):
            findings=[f for f in tables['findings'].values() if i in f.get(field,[])]
            if len(findings)<2: continue
            groups.append({'basis':target,'id':i,'finding_ids':sorted(f['id'] for f in findings),'problem_ids':sorted({p for f in findings for p in f['problem_ids']}),'status':'analyst-supported linkage; not independently verified' if r['status']=='supported' and all(f['status']=='supported' for f in findings) else 'candidate linkage; requires verification'})
    return {'schema_version':1,'counts':{k:len(v) for k,v in tables.items()},'groups':groups,'unassigned_findings':sorted(set(tables['findings'])-assigned),'task_waves':waves,'unknown_trust_flows':sorted(r['id'] for r in tables['flows'].values() if r['trust_crossing']=='unknown'),'unknown_transaction_flows':sorted(r['id'] for r in tables['flows'].values() if r['transaction_relation']=='unknown'),'limitations':['Structural checks only: does not authenticate evidence or verify causal claims.','Shared invariant does not imply shared root cause.','Task waves respect declared dependencies, not inferred priorities or approvals.']}


def catalog_ids():
    p=Path(__file__).resolve().parents[1]/'skills/solution-design-hardening/references/SOLUTION-DESIGN-PROBLEMS.md'
    return set(re.findall(r'^\| (SDP-\d{3}) \|',p.read_text(),re.M))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('model',type=Path); a=p.parse_args()
    try: print(json.dumps(analyze(json.loads(a.model.read_text(encoding='utf-8')),catalog_ids()),indent=2))
    except (OSError,ValueError,TypeError) as e: p.error(str(e))
