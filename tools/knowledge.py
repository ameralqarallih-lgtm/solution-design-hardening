"""Knowledge-preservation baseline for the skill tree. Python 3 standard library.

Extracts normalized statements from every Markdown file in the skill so a
restructure can prove that guidance was moved, not dropped.

  python tools/knowledge.py baseline   # write evals/fixtures/knowledge-baseline.json
  python tools/knowledge.py check      # list baseline statements missing from the tree
"""
import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/solution-design-hardening'
BASELINE = ROOT / 'evals/fixtures/knowledge-baseline.json'
EDITS = ROOT / 'evals/fixtures/knowledge-edits.json'
LINK = re.compile(r'!?\[([^\]]*)\]\([^)]*\)')
SENTENCE = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9`\[*"(])')
MIN_CHARS = 4


def normalize(text):
    text = LINK.sub(r'\1', text)
    text = text.replace('**', '').replace('`', '').replace('—', '-').replace('–', '-')
    text = re.sub(r'^\s*(?:#+|[-*+]|\d+\.)\s+', '', text)
    text = re.sub(r'\s+', ' ', text).strip().lower()
    return text.strip(' .;:')


def lines(text):
    """Yield content lines; drop frontmatter except the description value."""
    if text.startswith('---\n'):
        _, header, text = text.split('---', 2)
        for line in header.splitlines():
            if line.startswith('description:'):
                yield line.split(':', 1)[1]
    for line in text.splitlines():
        if line.lstrip().startswith('|'):
            cells = [c for c in line.strip().strip('|').split('|')]
            if all(re.fullmatch(r'\s*:?-{3,}:?\s*', c) for c in cells):
                continue
            yield from cells
        else:
            yield line


def statements(text):
    out = []
    for line in lines(text):
        for part in SENTENCE.split(line.strip()):
            s = normalize(part)
            if len(s) >= MIN_CHARS:
                out.append(s)
    return out


def corpus(root=SKILL):
    """Normalized full text of the tree; statements are checked as substrings."""
    chunks = []
    for md in sorted(root.rglob('*.md')):
        chunks.extend(normalize(line) for line in lines(md.read_text(encoding='utf-8')))
    return ' \n '.join(chunks)


def extract(root=SKILL):
    found = {}
    for md in sorted(root.rglob('*.md')):
        source = md.relative_to(root).as_posix()
        for s in statements(md.read_text(encoding='utf-8')):
            found.setdefault(s, source)
    return found


def missing(baseline, edits, root=SKILL):
    """Return baseline statements absent from the tree and not covered by a reviewed edit."""
    text = corpus(root)
    edited = {e['statement']: e for e in edits}
    gaps = []
    for source, items in baseline.items():
        for s in items:
            if s in text:
                continue
            edit = edited.get(s)
            if edit and normalize(edit['replacement']) in text:
                continue
            gaps.append((source, s))
    return gaps


def grouped(found):
    out = {}
    for s, source in found.items():
        out.setdefault(source, []).append(s)
    return dict(sorted(out.items()))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('command', choices=('baseline', 'check'))
    a = p.parse_args()
    if a.command == 'baseline':
        data = grouped(extract())
        BASELINE.write_text(json.dumps(data, indent=0, ensure_ascii=False) + '\n', encoding='utf-8')
        print(f'Wrote {sum(map(len, data.values()))} statements from {len(data)} files to {BASELINE.relative_to(ROOT)}')
        return
    baseline = json.loads(BASELINE.read_text(encoding='utf-8'))
    edits = json.loads(EDITS.read_text(encoding='utf-8')) if EDITS.exists() else []
    gaps = missing(baseline, edits)
    for source, s in gaps:
        print(f'{source}: {s}')
    print(f'{len(gaps)} missing statements', file=sys.stderr)
    sys.exit(1 if gaps else 0)


if __name__ == '__main__':
    main()
