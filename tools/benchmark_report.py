"""Report independently graded paired benchmark results, with explicit missing data."""
import argparse
from collections import Counter
from html import escape
import statistics
from pathlib import Path
from benchmark import read, write, digest, run_lock, write_text
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


def report(plan, raw, grades, gold, history=()):
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
    attempts = {}
    for attempt in (*history, *raw):
        # The current result can also be in history if execution stopped during a retry.
        attempts[(attempt['run_id'], attempt.get('attempt', 1))] = attempt
    for c in plan['conditions']:
        ids=[r['run_id'] for r in plan['runs'] if r['condition']==c]
        results[c]=dict(planned=len(ids),attempted=sum(i in observed for i in ids),successful=sum(observed.get(i,{}).get('status')=='ok' for i in ids),graded=sum(i in scored for i in ids),safety_violations=sum(scored[i]['safety_violation'] for i in ids if i in scored),activation={v:sum(observed.get(i,{}).get('activation','unknown')==v for i in ids if observed.get(i,{}).get('status')=='ok') for v in ('yes','no','unknown')})
        id_set = set(ids)
        events = [attempt for (run, _), attempt in attempts.items() if run in id_set]
        costs = [attempt['cost_usd'] for attempt in events if 'cost_usd' in attempt]
        results[c].update(
            attempts=len(events),
            output_limits_reached=sum(observed.get(run, {}).get('output_limit_reached', False)
                                      for run in ids),
            latest_statuses=dict(Counter(observed.get(run, {}).get('status', 'pending') for run in ids)),
            observed_cost_usd=sum(costs) if costs else None,
            attempts_with_cost=len(costs),
            reported_models=sorted({item['reported_model'] for item in events if 'reported_model' in item}),
        )
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
        for metric in ('input_tokens','output_tokens','cached_input_tokens','wall_seconds','cost_usd'):
            def value(i):
                if metric in ('wall_seconds', 'cost_usd'):
                    return observed[i].get(metric)
                return observed[i].get('usage', {}).get(metric)
            both=[(value(a),value(b)) for _,a,b in pairs if value(a) is not None and value(b) is not None]
            entry[metric]=dict(pairs=len(both),baseline_mean=mean([a for a,b in both]),comparison_mean=mean([b for a,b in both]),mean_delta=mean([b-a for a,b in both]))
        comparisons[c]=entry
    return dict(suite=plan.get('suite','scenario'),activation_evaluation=activation_results,agent=plan['agent'],model=plan['model'],settings=plan['settings'],seed=plan['seed'],skill_hashes=plan.get('skill_hashes',{}),case_catalog_sha256=plan.get('case_catalog_sha256'),conditions=results,comparisons=comparisons,limitations='Paired scores use complete pairs only. Precision and recall use the labeled subset. Missing and failed results can bias comparisons. Activation and usage are adapter-reported.')


def markdown(r):
    lines=['# Benchmark report','',f"Agent: {r['agent']} | Model: {r['model']}", '', '## Execution coverage','', '| Condition | Planned | Attempted | Successful | Graded | Safety violations |', '|---|---:|---:|---:|---:|---:|']
    if r.get('synthetic'):
        lines[4:4] = ['> Synthetic smoke test. No model was invoked or evaluated.', '']
    if 'chart' in r:
        lines[4:4] = [f"![Execution coverage and available paired scores]({r['chart']})", '']
    if 'adapter_version' in r:
        lines[4:4] = [f"Adapter version {r['adapter_version']} · Context mode {r['context_mode']}", '']
    for c,v in r['conditions'].items(): lines.append('| '+c+' | '+' | '.join(str(v[k]) for k in ('planned','attempted','successful','graded','safety_violations'))+' |')
    def fmt(v): return 'N/A' if v is None else f'{v:.3f}' if isinstance(v,float) else str(v)
    if 'grade_sources' in r:
        human = r['grade_sources']['human']
        automated = r['grade_sources']['automated_provisional']
        lines += ['', f'Human grades **{human}** · Automated provisional grades **{automated}**.']
        if 'judge_model' in r:
            lines += ['', f"Provisional judge model {r['judge_model']}."]
        if r.get('unresolved_grading_errors'):
            lines += ['', f"Unresolved automated grading errors **{r['unresolved_grading_errors']}**."]
    lines += ['', '| Condition | Latest outcomes | Total attempts | Output limits reached | Observed cost (USD) | Attempts with cost |',
              '|---|---|---:|---:|---:|---:|']
    for condition, item in r['conditions'].items():
        outcomes = ', '.join(f'{status} {count}' for status, count in sorted(item['latest_statuses'].items()))
        cost = item['observed_cost_usd']
        lines.append(f'| {condition} | {outcomes} | {item["attempts"]} | '
                     f'{item["output_limits_reached"]} | '
                     f'{format(cost, ".6f") if cost is not None else "N/A"} | {item["attempts_with_cost"]} |')
    for c,v in r['comparisons'].items():
        lines += ['',f'## Baseline vs {c}','',f"Complete pairs: {v['complete_pairs']}; incomplete: {v['incomplete_pairs']}; mean delta (out of 8): {fmt(v['mean_paired_delta_out_of_8'])}.", '', '| Metric | Baseline | Comparison |', '|---|---:|---:|']
        for k in ('mean_score_out_of_8','labeled_trials','tp','fp','fn','precision','recall','safe_control_trials','safe_control_false_alarm_rate'):
            lines.append(f"| {k} | {fmt(v['baseline'][k])} | {fmt(v[c][k])} |")
        for k in ('input_tokens','output_tokens','cached_input_tokens','wall_seconds','cost_usd'):
            m=v[k]; lines.append(f"| {k} ({m['pairs']} matched) | {fmt(m['baseline_mean'])} | {fmt(m['comparison_mean'])} |")
    if r['activation_evaluation']:
        lines+=['','## Activation probes (adapter trace required)','', '| Condition | TP | TN | FP | FN | Unknown / unavailable | Precision | Recall | False activation rate |','|---|---:|---:|---:|---:|---:|---:|---:|---:|']
        for c,v in r['activation_evaluation'].items(): lines.append('| '+c+' | '+' | '.join(fmt(v[k]) for k in ('tp','tn','fp','fn','unknown_or_unavailable','precision','recall','false_activation_rate'))+' |')
    lines+=['',r['limitations'],'']; return '\n'.join(lines)


def chart_svg(result):
    """Render execution coverage and any complete-pair mean scores on separate scales."""
    rows = []
    for condition, values in result['conditions'].items():
        for metric in ('successful', 'graded'):
            rows.append((f'{condition} {metric}', values[metric], max(values['planned'], 1),
                         f'{values[metric]} / {values["planned"]}'))
    for name, comparison in result['comparisons'].items():
        for condition in ('baseline', name):
            score = comparison[condition]['mean_score_out_of_8']
            if score is not None:
                counterpart = name if condition == 'baseline' else 'baseline'
                rows.append((f'{condition} vs {counterpart}', score, 8, f'{score:.2f} / 8'))
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="720" height="{60 + 30 * len(rows)}" '
        f'viewBox="0 0 720 {60 + 30 * len(rows)}" role="img" aria-labelledby="title">',
        '<title id="title">Benchmark coverage and paired scores</title>',
        '<rect width="100%" height="100%" rx="8" fill="#f1f5f9"/>',
        '<g font-family="system-ui, sans-serif" font-size="13" fill="#10243d">',
        '<text x="24" y="32" font-size="18" font-weight="700">Benchmark coverage and paired scores</text>',
    ]
    for index, (name, value, limit, label) in enumerate(rows):
        y = 51 + index * 30
        parts.extend([
            f'<text x="24" y="{y + 13}">{escape(name)}</text>',
            f'<rect x="230" y="{y}" width="360" height="16" rx="3" fill="#cbd5e1"/>',
            f'<rect x="230" y="{y}" width="{360 * value / limit:.2f}" height="16" rx="3" fill="#176b82"/>',
            f'<text x="608" y="{y + 13}">{label}</text>',
        ])
    return '\n'.join([*parts, '</g>', '</svg>', ''])


def grade_rows(path):
    rows = read(path)
    if not isinstance(rows, list) or any(not isinstance(row, dict) or 'run_id' not in row for row in rows):
        raise ValueError(f'{path.name} must be an array of grades keyed by run_id.')
    ids = [row['run_id'] for row in rows]
    if any(not isinstance(run_id, str) or not run_id for run_id in ids) or len(ids) != len(set(ids)):
        raise ValueError(f'{path.name} must use distinct nonempty run IDs.')
    return rows


def generate(out, grades_path=None):
    plan = read(out/'plan.private.json')
    raw = [read(file) for file in sorted((out/'raw.private').glob('*.json'))]
    history = [read(file) for file in sorted((out/'attempts.private').glob('*/*.json'))]
    gold = read(out/'gold.private.json')
    if digest(json.dumps(gold, sort_keys=True).encode()) != plan['gold_sha256']:
        raise ValueError('Gold labels changed.')
    human_file = grades_path or out/'grades.json'
    if grades_path is not None and not grades_path.is_file():
        raise ValueError(f'Grades file {grades_path} is missing. Provide completed grades or omit it '
                         'to report available results.')
    human = grade_rows(human_file) if human_file.exists() else []
    human_ids = {row['run_id'] for row in human}
    provisional = out/'grades.provisional.json'
    automated = [row for row in grade_rows(provisional) if row['run_id'] not in human_ids] \
        if grades_path is None and provisional.exists() else []
    result = report(plan, raw, human + automated, gold, history)
    result['grade_sources'] = dict(human=len(human), automated_provisional=len(automated))
    automation = plan.get('automation', {})
    if automation:
        result['adapter_version'] = automation['adapter_version']
        result['context_mode'] = automation['context_mode']
        result['synthetic'] = automation['synthetic']
    if automated and (out/'judge.private.json').exists():
        result['judge_model'] = read(out/'judge.private.json')['judge_model']
    failures = out/'grading-errors.private.json'
    if grades_path is None and failures.exists():
        graded_ids = human_ids | {row['run_id'] for row in automated}
        result['unresolved_grading_errors'] = len(read(failures).keys() - graded_ids)
    result['chart'] = 'report.svg'
    write_text(out/'report.svg', chart_svg(result))
    write(out/'report.json', result)
    write_text(out/'report.md', markdown(result))
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('out', type=Path)
    p.add_argument('grades', type=Path, nargs='?')
    a=p.parse_args()
    try:
        with run_lock(a.out):
            generate(a.out, a.grades)
    except (OSError, ValueError, TypeError, KeyError) as error:
        p.exit(2, f'Benchmark report error: {error}\n')
    print('Report generated; inspect missing pairs and limitations.')

if __name__=='__main__': main()
