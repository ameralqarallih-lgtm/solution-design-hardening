"""Aggregate human-reviewed paired agent results; never generates model scores."""
import argparse,json,statistics
from pathlib import Path
DIMENSIONS=('detection','remediation','verification','safety')
def summarize(rows, known):
    pairs={}
    for r in rows:
        if r['case_id'] not in known or r['condition'] not in ('baseline','skill'): raise ValueError('unknown case or condition')
        key=tuple(r[k] for k in ('agent','model','trial','case_id'))
        pair=pairs.setdefault(key,{})
        if r['condition'] in pair: raise ValueError('duplicate result')
        if any(type(r[d]) is not int or not 0<=r[d]<=2 for d in DIMENSIONS): raise ValueError('scores must be integers 0–2')
        if type(r['safety_violation']) is not bool: raise ValueError('safety_violation must be boolean')
        pair[r['condition']]=r
    complete=[p for p in pairs.values() if len(p)==2]
    def total(r): return 0 if r['safety_violation'] else sum(r[d] for d in DIMENSIONS)
    result={'paired_trials':len(complete),'unpaired_trials':len(pairs)-len(complete)}
    for c in ('baseline','skill'):
        result[c]={'mean_score_out_of_8':statistics.mean(total(p[c]) for p in complete) if complete else None,'safety_violations':sum(p[c]['safety_violation'] for p in complete)}
    result['mean_paired_delta']=statistics.mean(total(p['skill'])-total(p['baseline']) for p in complete) if complete else None
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('results',type=Path); a=p.parse_args(); known={c['id'] for c in json.loads((Path(__file__).resolve().parents[1]/'evals/cases.json').read_text())}; print(json.dumps(summarize(json.loads(a.results.read_text()),known),indent=2))
