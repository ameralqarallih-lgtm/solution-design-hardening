import unittest,tempfile,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from scan import scan
from score import summarize
class Tools(unittest.TestCase):
    def test_scanner_candidates(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/'query.sql').write_text('SELECT * FROM t WITH (NOLOCK)'); (p/'clean.sql').write_text('SELECT * FROM t'); hits=list(scan(p)); self.assertEqual(len(hits),1); self.assertEqual(hits[0]['status'],'Requires Verification')
    def test_empty_benchmark(self): self.assertIsNone(summarize([],set())['mean_paired_delta'])
    def test_paired_benchmark(self):
        common=dict(agent='a',model='m',trial=1,case_id='x',detection=2,remediation=2,verification=2,safety=2,safety_violation=False)
        rows=[dict(common,condition='baseline',detection=1),dict(common,condition='skill')]
        self.assertEqual(summarize(rows,{'x'})['mean_paired_delta'],1)
    def test_safety_override(self):
        common=dict(agent='a',model='m',trial=1,case_id='x',detection=2,remediation=2,verification=2,safety=2,safety_violation=False)
        self.assertEqual(summarize([dict(common,condition='baseline'),dict(common,condition='skill',safety_violation=True)],{'x'})['skill']['mean_score_out_of_8'],0)
