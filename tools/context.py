"""Plan selective reference loading by depth mode and problem ID.

Token figures are estimates (ceil(characters / 4)), not model-tokenizer counts or
measured savings. Python 3 standard library.

  python tools/context.py SDP-023 SDP-024 SDP-171        # compact route
  python tools/context.py --mode standard SDP-023        # route plus mode references
  python tools/context.py --mode deep --json             # full JSON structure
"""
import argparse, json, math, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'skills/solution-design-hardening'
PROBLEM_HEADING = re.compile(r'^# (SDP-\d{3}) - (.+)$', re.M)
INDEX_ROW = re.compile(r'^\| (SDP-\d{3}) \| .+ \| \[SDP-\d{3}\]\(problems/(SDP-\d{3})\.md\) \|$', re.M)
RELATED = re.compile(r'^- \*\*Related:\*\* (.+)$', re.M)
WARNING = 'Estimated tokens are characters/4, not model tokens or measured savings. Add related problems and applicable references as evidence warrants.'

# References each depth adds on top of the previous depth (paths relative to the skill root).
MODES = {
    'lightweight': ['SKILL.md'],
    'focused': ['references/PROBLEM-INDEX.md'],
    'standard': ['references/DETECTION-GUIDANCE.md', 'references/PATTERN-GUIDANCE.md'],
    'deep': ['references/ARCHITECTURAL-INTELLIGENCE.md', 'references/SECURITY-ASSESSMENT.md',
             'references/SECURITY-CAPABILITIES.md', 'references/technology/DISCOVERY.md',
             'references/technology/CAPABILITY-MAPPING.md', 'references/technology/VERSION-VERIFICATION.md',
             'references/INTEGRATION-VERIFICATION.md', 'references/OPERATIONS.md'],
    'comprehensive': ['references/SOLUTION-DESIGN-PROBLEMS.md', 'references/ASSESSMENT-OUTPUT.md',
                      'references/SECURITY-STANDARDS.md', 'assets/coverage-register.md'],
}
DEPTHS = list(MODES)


def estimate_tokens(text):
    return math.ceil(len(text) / 4)


def _entry(path, root, **extra):
    text = path.read_text(encoding='utf-8')
    return dict(path=path.relative_to(root).as_posix(), utf8_bytes=len(text.encode('utf-8')),
                estimated_tokens=estimate_tokens(text), **extra)


def index(root=ROOT):
    """Map each problem ID to (domain index, problem file) from the domain index tables."""
    found = {}
    for domain in sorted((root / 'references').glob('problems-*.md')):
        for m in INDEX_ROW.finditer(domain.read_text(encoding='utf-8')):
            if m[1] in found or m[1] != m[2]:
                raise ValueError(f'duplicate or mismatched problem ID {m[1]}')
            found[m[1]] = (domain, root / 'references/problems' / f'{m[1]}.md')
    return found


def related_ids(problem_file):
    m = RELATED.search(problem_file.read_text(encoding='utf-8'))
    return [x.strip() for x in m[1].split(',')] if m else []


def mode_references(mode, root=ROOT):
    if mode not in MODES:
        raise ValueError(f'unknown mode {mode}')
    paths = [p for d in DEPTHS[:DEPTHS.index(mode) + 1] for p in MODES[d]]
    return [_entry(root / p, root) for p in paths]


def select(ids, root=ROOT, mode=None):
    routes = index(root)
    if not ids or not set(ids) <= routes.keys():
        raise ValueError('explicit known IDs required')
    requested = sorted(set(ids))
    domains = sorted({routes[i][0] for i in requested})
    playbooks = [_entry(d, root, requested_ids=[i for i in requested if routes[i][0] == d]) for d in domains]
    problems = [_entry(routes[i][1], root, id=i, related=related_ids(routes[i][1])) for i in requested]
    related = sorted({r for p in problems for r in p['related']} - set(requested))
    references = mode_references(mode, root) if mode else []
    all_domains = {d for d, _ in routes.values()}
    estimated = dict(references=sum(r['estimated_tokens'] for r in references),
                     domain_indexes=sum(p['estimated_tokens'] for p in playbooks),
                     problems=sum(p['estimated_tokens'] for p in problems))
    estimated['total'] = sum(estimated.values())
    return dict(requested_ids=requested, mode=mode, references=references, playbooks=playbooks,
                problems=problems, related_ids_not_loaded=related,
                selected_playbook_bytes=sum(p['utf8_bytes'] for p in playbooks + problems),
                all_playbook_bytes=sum(d.stat().st_size for d in all_domains) +
                sum(f.stat().st_size for _, f in routes.values()),
                core_skill_bytes=(root / 'SKILL.md').stat().st_size,
                estimated_tokens=estimated, warning=WARNING)


def compact(result):
    lines = [f"ref {r['path']} ~{r['estimated_tokens']}" for r in result.get('references', [])]
    lines += [f"index {p['path']} ~{p['estimated_tokens']} [{' '.join(p['requested_ids'])}]" for p in result.get('playbooks', [])]
    lines += [f"problem {p['path']} ~{p['estimated_tokens']}" + (f" related {' '.join(p['related'])}" if p['related'] else '')
              for p in result.get('problems', [])]
    total = result['estimated_tokens']['total']
    lines.append(f"total ~{total} estimated tokens (chars/4, not measured)")
    if result.get('related_ids_not_loaded'):
        lines.append('check related: ' + ' '.join(result['related_ids_not_loaded']))
    return '\n'.join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('ids', nargs='*')
    p.add_argument('--mode', choices=DEPTHS)
    p.add_argument('--json', action='store_true', help='Print the full JSON structure')
    a = p.parse_args()
    if a.ids:
        result = select(a.ids, mode=a.mode)
    elif a.mode:
        refs = mode_references(a.mode)
        result = dict(mode=a.mode, references=refs, estimated_tokens=dict(total=sum(r['estimated_tokens'] for r in refs)), warning=WARNING)
    else:
        p.error('give problem IDs, --mode, or both')
    print(json.dumps(result, indent=2) if a.json else compact(result))


if __name__ == '__main__':
    main()
