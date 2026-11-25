"""Adaptive context routing must stay complete. No size or token limits are enforced:
completeness and correctness take precedence over context size."""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from context import ROOT, index, mode_references, select

ALL_IDS = [f'SDP-{i:03}' for i in range(1, 236)]


class ContextRouting(unittest.TestCase):
    def test_every_problem_is_routable(self):
        r = select(ALL_IDS)
        self.assertEqual([p['id'] for p in r['problems']], ALL_IDS)
        self.assertEqual(len(r['playbooks']), 24)

    def test_related_ids_are_surfaced_not_dropped(self):
        r = select(['SDP-023'])
        self.assertIn('SDP-063', r['problems'][0]['related'])
        self.assertIn('SDP-063', r['related_ids_not_loaded'])

    def test_selection_loads_requested_problems_only_not_whole_catalog(self):
        r = select(['SDP-023', 'SDP-024', 'SDP-171'], mode='focused')
        self.assertEqual([p['id'] for p in r['problems']], ['SDP-023', 'SDP-024', 'SDP-171'])
        self.assertLess(r['selected_playbook_bytes'], r['all_playbook_bytes'])

    def test_deeper_modes_add_references_and_never_remove_them(self):
        modes = ('lightweight', 'focused', 'standard', 'deep', 'comprehensive')
        paths = [[r['path'] for r in mode_references(m)] for m in modes]
        for smaller, larger in zip(paths, paths[1:]):
            self.assertTrue(set(smaller) < set(larger))
        self.assertIn('references/SOLUTION-DESIGN-PROBLEMS.md', paths[-1])

    def test_core_routes_every_depth_reference(self):
        core = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        for path in ('references/PROBLEM-INDEX.md', 'references/CONTEXT-STRATEGY.md',
                     'references/DETECTION-GUIDANCE.md', 'references/PATTERN-GUIDANCE.md',
                     'references/ARCHITECTURAL-INTELLIGENCE.md', 'references/SECURITY-ASSESSMENT.md',
                     'references/technology/DISCOVERY.md', 'references/INTEGRATION-VERIFICATION.md',
                     'references/SOLUTION-DESIGN-PROBLEMS.md', 'references/ASSESSMENT-OUTPUT.md',
                     'assets/coverage-register.md'):
            self.assertIn(f']({path})', core, path)
        for mode in ('Lightweight', 'Focused', 'Standard', 'Deep', 'Comprehensive'):
            self.assertRegex(core, re.compile(rf'^\| {mode} \|', re.M))

    def test_guidance_never_limits_reading(self):
        core = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        strategy = (ROOT / 'references/CONTEXT-STRATEGY.md').read_text(encoding='utf-8')
        self.assertIn('when in doubt use the deeper mode', core)
        self.assertIn('There is no size or token limit on what an agent reads', strategy)
        self.assertNotRegex(core + strategy, r'1-3 (problem|Level 3) files|lowest depth|Target tokens')


if __name__ == '__main__':
    unittest.main()
