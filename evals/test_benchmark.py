import json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from benchmark import make_plan,prepare,execute,review_packet,invoke,read,ROOT
from benchmark_report import report,markdown
from context import select
from codex_native_adapter import activation, parser as native_parser

CASES=read(ROOT/'evals/cases.json')
GOLD=read(ROOT/'evals/gold-findings.json')

def plan(ids=('outbox-crash',),conditions=('baseline','skill')):
    return make_plan(CASES,list(ids),1,99,list(conditions),'test-agent','test-model','synthetic')

def records(p):
    raw=[]; grades=[]
    for r in p['runs']:
        skill=r['condition']=='skill'; cid=r['case_id']; gold=GOLD.get(cid,[])
        raw.append(dict(run_id=r['run_id'],status='ok',usage={'input_tokens':20 if skill else 10},activation='unknown',wall_seconds=1.0))
        grades.append(dict(run_id=r['run_id'],detection=2 if skill else 1,remediation=2,verification=2,safety=2,safety_violation=False,notes='synthetic test grade',true_positives=gold if skill else [],false_positives=[] if skill else ['unsupported defect']))
    return raw,grades

class BenchmarkTests(unittest.TestCase):
    def test_seed_and_identical_prompts(self):
        p=plan(); self.assertEqual(p,plan()); self.assertEqual(len({r['prompt'] for r in p['runs']}),1); self.assertNotIn('expected',p['runs'][0]); self.assertNotIn(CASES[2]['expected'],p['runs'][0]['prompt'])
    def test_bad_case(self):
        with self.assertRaises(ValueError): plan(('not-real',))
    def test_competitor_pairs(self):
        p=plan(conditions=('baseline','skill','competitor')); raw,g=records(p); r=report(p,raw,g,GOLD); self.assertEqual(r['comparisons']['competitor']['complete_pairs'],1)
    def test_precision_recall_and_controls(self):
        p=plan(('outbox-crash','local-transaction')); raw,g=records(p); v=report(p,raw,g,GOLD)['comparisons']['skill']; self.assertEqual(v['skill']['precision'],1); self.assertEqual(v['skill']['recall'],1); self.assertEqual(v['baseline']['recall'],0); self.assertEqual(v['baseline']['safe_control_false_alarm_rate'],1); self.assertEqual(v['mean_paired_delta_out_of_8'],1)
    def test_missing_data(self):
        p=plan(); raw,g=records(p); r=report(p,raw[:1],g[:1],GOLD); v=r['comparisons']['skill']; self.assertEqual(v['incomplete_pairs'],1); self.assertIsNone(v['mean_paired_delta_out_of_8']); self.assertIsNone(v['skill']['precision']); self.assertIn('N/A',markdown(r))
    def test_unknown_usage(self):
        p=plan(); raw,g=records(p); raw[0]['usage']={}; v=report(p,raw,g,GOLD)['comparisons']['skill']; self.assertEqual(v['input_tokens']['pairs'],0); self.assertIsNone(v['input_tokens']['mean_delta'])
    def test_safety_override(self):
        p=plan(); raw,g=records(p); index=next(i for i,r in enumerate(p['runs']) if r['condition']=='skill'); g[index]['safety_violation']=True; v=report(p,raw,g,GOLD)['comparisons']['skill']; self.assertEqual(v['skill']['mean_score_out_of_8'],0)
    def test_invalid_grades(self):
        p=plan(); raw,g=records(p); g[0]['true_positives']=['invented'];
        with self.assertRaises(ValueError): report(p,raw,g,GOLD)
    def test_duplicate_grades(self):
        p=plan(); raw,g=records(p)
        with self.assertRaises(ValueError): report(p,raw,g+g[:1],GOLD)
    def test_failed_attempt_cannot_be_graded(self):
        p=plan(); raw,g=records(p); raw[0]['status']='timeout'
        with self.assertRaises(ValueError): report(p,raw,g,GOLD)
    def test_adapter_workspace_and_blinding(self):
        with tempfile.TemporaryDirectory() as d:
            base=Path(d); out=base/'run'; adapter=base/'adapter.py'; adapter.write_text('import json\nfrom pathlib import Path\nassert set(p.name for p in Path(".").iterdir()) <= {"prompt.txt","skill"}\nprint(json.dumps({"response":"synthetic response","usage":{"input_tokens":3}}))')
            p=prepare(out,CASES,['outbox-crash'],1,42,'a','m','s'); execute(out,[sys.executable,str(adapter)]); packet=review_packet(out); self.assertEqual(len(packet),2); self.assertTrue(all(set(r)=={'run_id','case_id','prompt','response'} for r in packet)); self.assertTrue(all(read(f)['status']=='ok' for f in (out/'raw.private').glob('*.json'))); execute(out,[sys.executable,'nonexistent.py']); self.assertEqual(len(review_packet(out)),2)
    def test_snapshot_tamper(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'run'; prepare(out,CASES,['outbox-crash'],1,42,'a','m','s'); (out/'skill-snapshots/skill/SKILL.md').write_text('changed')
            with self.assertRaises(ValueError): execute(out,[sys.executable,'nonexistent.py'])
    def test_adapter_errors(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(invoke([sys.executable,'-c','print("bad JSON")'],Path(d),2)['status'],'invalid_output'); self.assertEqual(invoke([sys.executable,'-c','import time; time.sleep(2)'],Path(d),0.1)['status'],'timeout'); self.assertEqual(invoke([sys.executable,'-c','raise SystemExit(4)'],Path(d),2)['status'],'adapter_error')
    def test_context_routing(self):
        r=select(['SDP-023','SDP-024','SDP-171']); self.assertEqual(len(r['playbooks']),2); self.assertEqual([p['id'] for p in r['problems']],['SDP-023','SDP-024','SDP-171']); self.assertLess(r['selected_playbook_bytes'],r['all_playbook_bytes']); self.assertIn('not model tokens',r['warning']); self.assertIn('SDP-063',r['related_ids_not_loaded'])
    def test_activation_probe_metrics(self):
        cases=read(ROOT/'evals/activation-cases.json'); p=make_plan(cases,[c['id'] for c in cases],1,99,['baseline','skill'],'a','m','s'); p.update(suite='activation',activation_labels={c['id']:c['relevant'] for c in cases}); raw=[dict(run_id=r['run_id'],status='ok',activation=('yes' if p['activation_labels'][r['case_id']] else 'no') if r['condition']=='skill' else 'unknown') for r in p['runs']]; raw[next(i for i,r in enumerate(p['runs']) if r['condition']=='skill' and p['activation_labels'][r['case_id']])]['activation']='unknown'; result=report(p,raw,[],{})['activation_evaluation']['skill']; self.assertEqual(result['tp'],3); self.assertEqual(result['tn'],4); self.assertEqual(result['unknown_or_unavailable'],1); self.assertEqual(result['false_activation_rate'],0)
    def test_invalid_context_id(self):
        with self.assertRaises(ValueError): select(['SDP-999'])

    def test_native_activation_requires_host_evidence(self):
        turn = {"type": "turn.completed"}
        text = {"type": "item.completed", "item": {"type": "agent_message",
                                                   "text": "I used solution-design-hardening."}}
        command = r"Get-Content .agents\skills\solution-design-hardening\SKILL.md"
        denied = f"ERROR: {command} rejected: blocked by policy"
        read = {"type": "item.completed", "item": {"type": "command_execution", "command": command,
                                                   "exit_code": 0,
                                                   "aggregated_output": "# Solution Design Hardening\n"}}
        self.assertEqual(activation([text, turn], "")[0], "no")
        self.assertEqual(activation([text, turn], denied)[0], "unknown")
        self.assertEqual(activation([read, turn], "")[0], "yes")

    def test_native_adapter_timeout_is_configurable_and_validated(self):
        self.assertEqual(native_parser().parse_args(['--model', 'm']).timeout, 180)
        self.assertEqual(native_parser().parse_args(['--model', 'm', '--timeout', '240']).timeout, 240)
        import contextlib, io
        for bad in ('0', '-5', 'nan', 'inf'):
            with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
                native_parser().parse_args(['--model', 'm', '--timeout', bad])

if __name__=='__main__': unittest.main()
