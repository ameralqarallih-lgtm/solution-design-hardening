"""Report independently graded paired benchmark results, with explicit missing data."""
import argparse
import statistics
from pathlib import Path
from benchmark import read,write,digest
import json

DIMS=('detection','remediation','verification','safety')

def ratio(a,b): return a/b if b else None

def mean(values): return statistics.mean(values) if values else None

def validate_grade(g, gold):
    if any(type(g.get(d)) is not int or not 0<=g[d]<=2 for d in DIMS):
        raise ValueError('invalid rubric score')
    if type(g.get('safety_violation')) is not bool or not isinstance(g.get('notes'),str) or not g['notes'].strip():
        raise ValueError('safety decision and reviewer notes required')
    if gold is not None:
        hits=g.get('true_positives'); fp=g.get('false_positives')
        if not isinstance(hits,list) or any(not isinstance(x,str) for x in hits) or len(set(hits))!=len(hits) or not set(hits)<=set(gold):
            raise ValueError('invalid true positive labels')
        if not isinstance(fp,list) or any(not isinstance(x,str) or not x.strip() for x in fp) or len(set(fp))!=len(fp):
            raise ValueError('false positives require distinct descriptions')
    return 0 if g['safety_violation'] else sum(g[d] for d in DIMS)


def report(plan, raw, grades, gold):
    by_run={r['run_id']:r for r in plan['runs']}
    if len(by_run)!=len(plan['runs']): raise ValueError('duplicate plan run')
    for collection in (raw,grades):
        if len({r['run_id'] for r in collection})!=len(collection) or not {r['run_id'] for r in collection}<=by_run.keys():
            raise ValueError('duplicate or unknown run')
    observed={r['run_id']:r for r in raw}; scored={r['run_id']:r for r in grades}
    if any(observed.get(i,{}).get('status')!='ok' for i in scored): raise ValueError('grade without successful response')
    totals={i:validate_grade(g,gold.get(by_run[i]['case_id'])) for i,g in scored.items()}
    cells={}
    for r in plan['runs']:
        key=(r['case_id'],r['trial']); group=cells.setdefault(key,{})
        if r['condition'] in group: raise ValueError('duplicate condition in pair')
        group[r['condition']]=r['run_id']
    results={}
    for c in plan['conditions']:
        ids=[r['run_id'] for r in plan['runs'] if r['condition']==c]
        results[c]=dict(planned=len(ids),attempted=sum(i in observed for i in ids),successful=sum(observed.get(i,{}).get('status')=='ok' for i in ids),graded=sum(i in scored for i in ids),safety_violations=sum(scored[i]['safety_violation'] for i in ids if i in scored),activation={v:sum(observed.get(i,{}).get('activation','unknown')==v for i in ids if observed.get(i,{}).get('status')=='ok') for v in ('yes','no','unknown')})
    activation_results={}
    if plan.get('suite')=='activation':
        labels=plan['activation_labels']
        for c in plan['conditions'][1:]:
            matches=[(labels[r['case_id']],observed.get(r['run_id'],{})) for r in plan['runs'] if r['condition']==c]
            tp=sum(want and v.get('activation')=='yes' for want,v in matches); tn=sum(not want and v.get('activation')=='no' for want,v in matches)
            fp=sum(not want and v.get('activation')=='yes' for want,v in matches); fn=sum(want and v.get('activation')=='no' for want,v in matches)
            activation_results[c]=dict(tp=tp,tn=tn,fp=fp,fn=fn,unknown_or_unavailable=len(matches)-tp-tn-fp-fn,precision=ratio(tp,tp+fp),recall=ratio(tp,tp+fn),false_activation_rate=ratio(fp,fp+tn))
    comparisons={}
    for c in plan['conditions'][1:]:
        pairs=[(k,g['baseline'],g[c]) for k,g in cells.items() if 'baseline' in g and c in g and g['baseline'] in totals and g[c] in totals]
        entry=dict(complete_pairs=len(pairs),incomplete_pairs=len(cells)-len(pairs),mean_paired_delta_out_of_8=mean([totals[b]-totals[a] for _,a,b in pairs]),wins=sum(totals[b]>totals[a] for _,a,b in pairs),ties=sum(totals[b]==totals[a] for _,a,b in pairs),losses=sum(totals[b]<totals[a] for _,a,b in pairs))
        for label,index in [('baseline',1),(c,2)]:
            subset=[(key,pair[index]) for pair in pairs for key in [pair[0]]]
            labeled=[(k,i) for k,i in subset if k[0] in gold]
            tp=sum(len(scored[i]['true_positives']) for k,i in labeled); fp=sum(len(scored[i]['false_positives']) for k,i in labeled); fn=sum(len(gold[k[0]])-len(scored[i]['true_positives']) for k,i in labeled)
            controls=[i for k,i in labeled if not gold[k[0]]]
            entry[label]=dict(mean_score_out_of_8=mean([totals[i] for _,i in subset]),rubric_means={d:mean([scored[i][d] for _,i in subset]) for d in DIMS},labeled_trials=len(labeled),tp=tp,fp=fp,fn=fn,precision=ratio(tp,tp+fp),recall=ratio(tp,tp+fn),safe_control_false_alarm_rate=ratio(sum(bool(scored[i]['false_positives']) for i in controls),len(controls)),safe_control_trials=len(controls))
        for metric in ('input_tokens','output_tokens','cached_input_tokens','wall_seconds'):
            def value(i): return observed[i].get('wall_seconds') if metric=='wall_seconds' else observed[i].get('usage',{}).get(metric)
            both=[(value(a),value(b)) for _,a,b in pairs if value(a) is not None and value(b) is not None]
            entry[metric]=dict(pairs=len(both),baseline_mean=mean([a for a,b in both]),comparison_mean=mean([b for a,b in both]),mean_delta=mean([b-a for a,b in both]))
        comparisons[c]=entry
    return dict(suite=plan.get('suite','scenario'),activation_evaluation=activation_results,agent=plan['agent'],model=plan['model'],settings=plan['settings'],seed=plan['seed'],skill_hashes=plan.get('skill_hashes',{}),case_catalog_sha256=plan.get('case_catalog_sha256'),conditions=results,comparisons=comparisons,limitations='Human rubric; paired complete cases only; failures reported separately; labeled subset only; no statistical superiority claim. Activation and usage are adapter-reported.')


def markdown(r):
    lines=['# Benchmark report','',f"Agent: {r['agent']} | Model: {r['model']}", '', '## Execution coverage','', '| Condition | Planned | Attempted | Successful | Graded | Safety violations |', '|---|---:|---:|---:|---:|---:|']
    for c,v in r['conditions'].items(): lines.append('| '+c+' | '+' | '.join(str(v[k]) for k in ('planned','attempted','successful','graded','safety_violations'))+' |')
    def fmt(v): return 'N/A' if v is None else f'{v:.3f}' if isinstance(v,float) else str(v)
    for c,v in r['comparisons'].items():
        lines += ['',f'## Baseline vs {c}','',f"Complete pairs: {v['complete_pairs']}; incomplete: {v['incomplete_pairs']}; mean delta (out of 8): {fmt(v['mean_paired_delta_out_of_8'])}.", '', '| Metric | Baseline | Comparison |', '|---|---:|---:|']
        for k in ('mean_score_out_of_8','labeled_trials','tp','fp','fn','precision','recall','safe_control_trials','safe_control_false_alarm_rate'):
            lines.append(f"| {k} | {fmt(v['baseline'][k])} | {fmt(v[c][k])} |")
        for k in ('input_tokens','output_tokens','cached_input_tokens','wall_seconds'):
            m=v[k]; lines.append(f"| {k} ({m['pairs']} matched) | {fmt(m['baseline_mean'])} | {fmt(m['comparison_mean'])} |")
    if r['activation_evaluation']:
        lines+=['','## Activation probes (adapter trace required)','', '| Condition | TP | TN | FP | FN | Unknown / unavailable | Precision | Recall | False activation rate |','|---|---:|---:|---:|---:|---:|---:|---:|---:|']
        for c,v in r['activation_evaluation'].items(): lines.append('| '+c+' | '+' | '.join(fmt(v[k]) for k in ('tp','tn','fp','fn','unknown_or_unavailable','precision','recall','false_activation_rate'))+' |')
    lines+=['',r['limitations'],'']; return '\n'.join(lines)


def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('out',type=Path); p.add_argument('grades',type=Path); a=p.parse_args()
    plan=read(a.out/'plan.private.json'); folder=a.out/'raw.private'; raw=[read(f) for f in sorted(folder.glob('*.json'))]
    gold=read(a.out/'gold.private.json')
    if digest(json.dumps(gold,sort_keys=True).encode())!=plan['gold_sha256']: raise ValueError('gold labels changed')
    r=report(plan,raw,read(a.grades),gold); write(a.out/'report.json',r); (a.out/'report.md').write_text(markdown(r),encoding='utf-8')
    print('Report generated; inspect missing pairs and limitations.')

if __name__=='__main__': main()
