"""Knowledge preservation: restructuring may move or deduplicate guidance, never drop it."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from knowledge import BASELINE, EDITS, missing, normalize, statements


class KnowledgePreservation(unittest.TestCase):
    def test_every_baseline_statement_is_still_present(self):
        baseline = json.loads(BASELINE.read_text(encoding='utf-8'))
        edits = json.loads(EDITS.read_text(encoding='utf-8'))
        self.assertGreater(sum(map(len, baseline.values())), 3000)
        gaps = missing(baseline, edits)
        self.assertEqual(gaps, [], f'{len(gaps)} statements lost; first: {gaps[:5]}')

    def test_reviewed_edits_are_complete(self):
        baseline = {s for items in json.loads(BASELINE.read_text(encoding='utf-8')).values() for s in items}
        for edit in json.loads(EDITS.read_text(encoding='utf-8')):
            self.assertIn(edit['statement'], baseline)
            self.assertTrue(edit['replacement'].strip() and edit['reason'].strip())

    def test_normalization_ignores_links_and_formatting_only(self):
        self.assertEqual(normalize('- **Read** [the catalog](a/B.md) first.'), 'read the catalog first')
        self.assertEqual(statements('| Scope | Check one. Then two |\n|---|---|'), ['scope', 'check one', 'then two'])

    def test_moved_text_counts_and_dropped_text_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'a.md').write_text('Keep the invariant. Verify the crash window.\n', encoding='utf-8')
            baseline = {'a.md': statements((root / 'a.md').read_text(encoding='utf-8'))}
            (root / 'a.md').write_text('Keep the invariant.\n', encoding='utf-8')
            (root / 'b.md').write_text('- **Verify** the crash window.\n', encoding='utf-8')
            self.assertEqual(missing(baseline, [], root), [])
            (root / 'b.md').unlink()
            self.assertEqual(missing(baseline, [], root), [('a.md', 'verify the crash window')])


if __name__ == '__main__':
    unittest.main()
