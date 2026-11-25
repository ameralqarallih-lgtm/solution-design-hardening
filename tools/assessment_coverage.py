"""Report catalog coverage from an assessment or coverage register. Optional; Python 3 standard library.

  python tools/assessment_coverage.py SOLUTION-DESIGN-ASSESSMENT.md [--catalog path] [--batch 20] [--json]

Reads table rows whose first cell is a catalog ID and whose second cell is a status.
It reports assessed, missing and invalid entries and the next batch. It does not
judge whether the recorded evidence is sufficient.
"""
import argparse, json, re
from pathlib import Path

CATALOG = Path(__file__).resolve().parents[1] / 'skills/solution-design-hardening/references/SOLUTION-DESIGN-PROBLEMS.md'
STATUSES = ('Fully Addressed', 'Partially Addressed', 'Not Addressed', 'Incorrectly Addressed',
            'Not Applicable', 'Requires Verification')
ROW = re.compile(r'^\|\s*([A-Z][A-Z0-9]*-\d{3})\s*\|\s*([^|]*?)\s*\|', re.M)


def catalog_ids(path=CATALOG):
    return re.findall(r'^\| (SDP-\d{3}) \|', Path(path).read_text(encoding='utf-8'), re.M)


def coverage(text, ids, batch=20):
    recorded, invalid, duplicates = {}, [], []
    for pid, status in ROW.findall(text):
        if not status:
            continue  # template row not yet assessed; reported as missing
        if pid in recorded:
            duplicates.append(pid)
        elif status not in STATUSES:
            invalid.append(dict(id=pid, status=status))
        else:
            recorded[pid] = status
    missing = [i for i in ids if i not in recorded]
    counts = {s: sum(1 for i in ids if recorded.get(i) == s) for s in STATUSES}
    return dict(catalog=len(ids), assessed=len(ids) - len(missing), missing=missing,
                invalid_status=invalid, duplicates=sorted(set(duplicates)), status_counts=counts,
                project_ids=sorted(set(recorded) - set(ids)), next_batch=missing[:batch],
                complete=not missing and not invalid and not duplicates)


def compact(r):
    lines = [f"assessed {r['assessed']}/{r['catalog']}" + (' complete' if r['complete'] else '')]
    lines += [f"{s}: {n}" for s, n in r['status_counts'].items() if n]
    if r['invalid_status']:
        lines.append('invalid status: ' + ' '.join(f"{x['id']}={x['status']}" for x in r['invalid_status']))
    if r['duplicates']:
        lines.append('duplicates: ' + ' '.join(r['duplicates']))
    if r['next_batch']:
        lines.append('next batch: ' + ' '.join(r['next_batch']))
    return '\n'.join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('report', type=Path)
    p.add_argument('--catalog', type=Path, default=CATALOG)
    p.add_argument('--batch', type=int, default=20)
    p.add_argument('--json', action='store_true')
    a = p.parse_args()
    if a.batch < 1:
        p.error('--batch must be positive')
    r = coverage(a.report.read_text(encoding='utf-8'), catalog_ids(a.catalog), a.batch)
    print(json.dumps(r, indent=2) if a.json else compact(r))
    raise SystemExit(0 if r['complete'] else 1)


if __name__ == '__main__':
    main()
