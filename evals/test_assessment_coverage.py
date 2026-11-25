import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from assessment_coverage import catalog_ids, coverage

IDS = ['SDP-001', 'SDP-002', 'SDP-003']


class Coverage(unittest.TestCase):
    def test_catalog_has_every_id(self):
        self.assertEqual(len(catalog_ids()), 235)

    def test_missing_invalid_and_next_batch(self):
        report = '\n'.join(['| ID | Status |', '|---|---|', '| SDP-001 | Not Applicable |',
                            '| SDP-002 | Looks fine |', '| SDP-003 | |', '| PRJ-001 | Not Addressed |'])
        r = coverage(report, IDS, batch=1)
        self.assertEqual(r['assessed'], 1)
        self.assertEqual(r['missing'], ['SDP-002', 'SDP-003'])
        self.assertEqual(r['invalid_status'], [{'id': 'SDP-002', 'status': 'Looks fine'}])
        self.assertEqual(r['next_batch'], ['SDP-002'])
        self.assertEqual(r['project_ids'], ['PRJ-001'])
        self.assertFalse(r['complete'])

    def test_duplicates_block_completion(self):
        rows = [f'| {i} | Fully Addressed |' for i in IDS] + ['| SDP-001 | Not Addressed |']
        r = coverage('\n'.join(rows), IDS)
        self.assertEqual(r['duplicates'], ['SDP-001'])
        self.assertFalse(r['complete'])
        self.assertTrue(coverage('\n'.join(rows[:3]), IDS)['complete'])

    def test_template_register_is_parseable(self):
        template = (Path(__file__).resolve().parents[1] /
                    'skills/solution-design-hardening/assets/coverage-register.md').read_text(encoding='utf-8')
        r = coverage(template, catalog_ids())
        self.assertEqual((r['assessed'], r['invalid_status']), (0, []))
        self.assertEqual(r['next_batch'][0], 'SDP-001')


if __name__ == '__main__':
    unittest.main()
