"""Prepare reproducible, paired, opt-in coding-agent evaluations (Python stdlib)."""
import argparse
from contextlib import contextmanager
import hashlib
import json
import math
import os
import random
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPT = ('Review the following synthetic scenario for architectural and security correctness. '
          'Identify concrete defects or justified non-findings, the minimal sufficient fixes, '
          'and verification or missing evidence. Do not modify source code or contact live services.\n\n')
MAX_OUTPUT = 1_000_000


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write_text(path, content):
    path = Path(path)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as temp:
        pending = Path(temp.name)
    try:
        pending.write_text(content, encoding='utf-8')
        pending.replace(path)
    finally:
        pending.unlink(missing_ok=True)


def write(path, obj):
    write_text(path, json.dumps(obj, indent=2, ensure_ascii=False) + '\n')


@contextmanager
def run_lock(out):
    """An OS-held lock is released even if the runner is interrupted."""
    with (out / '.benchmark.lock').open('a+b') as lock:
        lock.seek(0)
        try:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise ValueError('Another benchmark process is using this experiment.') from None
        yield


def digest(data):
    return hashlib.sha256(data).hexdigest()


def skill_digest(path):
    if not (path/'SKILL.md').is_file():
        raise ValueError('skill directory must contain SKILL.md')
    parts = []
    for p in sorted(path.rglob('*')):
        if p.is_symlink():
            raise ValueError('symlink in skill directory')
        if p.is_file():
            parts.append([p.relative_to(path).as_posix(), digest(p.read_bytes())])
    return digest(json.dumps(parts).encode())


def make_plan(cases, ids, trials, seed, conditions, agent, model, settings):
    if trials < 1 or len(set(ids)) != len(ids) or not ids:
        raise ValueError('positive trials and unique nonempty case selection required')
    if not all(isinstance(x,str) and x.strip() for x in (agent, model, settings)):
        raise ValueError('record agent, model and settings')
    if len(set(conditions)) != len(conditions) or conditions[:2] != ['baseline','skill']:
        raise ValueError('baseline and skill conditions required')
    by_id = {c['id']: c for c in cases}
    if not set(ids) <= by_id.keys():
        raise ValueError('unknown case')
    rng = random.Random(seed)
    rows = []
    for cid in ids:
        prompt = by_id[cid]['prompt'] if 'prompt' in by_id[cid] else PROMPT + by_id[cid]['scenario']
        for trial in range(1, trials+1):
            order = list(conditions)
            rng.shuffle(order)
            for condition in order:
                rows.append(dict(run_id=f'run-{rng.getrandbits(128):032x}', case_id=cid,
                                 trial=trial, condition=condition, prompt=prompt,
                                 prompt_sha256=digest(prompt.encode())))
    if len({r['run_id'] for r in rows}) != len(rows):
        raise ValueError('run ID collision')
    return dict(schema=1, seed=seed, agent=agent, model=model, settings=settings,
                conditions=conditions, case_ids=ids, trials=trials, runs=rows)


def prepare(out, cases, ids, trials, seed, agent, model, settings, competitor=None, suite='scenario',
            automation=None):
    plan = make_plan(cases, ids, trials, seed, ['baseline','skill']+(['competitor'] if competitor else []), agent, model, settings)
    skill = ROOT/'skills/solution-design-hardening'
    sources = {'skill':skill}
    if competitor:
        sources['competitor'] = Path(competitor).resolve()
    plan['skill_hashes'] = {k:skill_digest(v) for k,v in sources.items()}
    plan['case_catalog_sha256'] = digest(json.dumps(cases,sort_keys=True).encode())
    gold = read(ROOT/'evals/gold-findings.json') if suite=='scenario' else {}
    plan['suite']=suite
    plan['activation_labels']={c['id']:c['relevant'] for c in cases} if suite=='activation' else {}
    plan['gold_sha256'] = digest(json.dumps(gold,sort_keys=True).encode())
    if automation is not None:
        rubric = {case['id']: case['expected'] for case in cases if case['id'] in ids}
        plan['automation'] = automation
        plan['rubric_sha256'] = digest(json.dumps(rubric, sort_keys=True).encode())
    out.mkdir(parents=True, exist_ok=False)
    for k,v in sources.items():
        shutil.copytree(v, out/'skill-snapshots'/k)
    write(out/'gold.private.json',gold)
    if automation is not None:
        write(out/'rubric.private.json', rubric)
    write(out/'plan.private.json', plan)
    return plan


def invoke(command, workspace, timeout):
    """Trusted, caller-selected adapter. No shell; this is NOT an OS sandbox."""
    start = time.monotonic()
    with tempfile.TemporaryFile() as stdout:
        try:
            p = subprocess.run(command, cwd=workspace, stdin=subprocess.DEVNULL,
                               stdout=stdout, stderr=subprocess.DEVNULL, timeout=timeout, check=False)
        except (subprocess.TimeoutExpired, OSError) as e:
            return dict(status='timeout' if isinstance(e,subprocess.TimeoutExpired) else 'adapter_error', wall_seconds=time.monotonic()-start)
        elapsed = time.monotonic()-start
        if p.returncode != 0:
            return dict(status='adapter_error', exit_code=p.returncode, wall_seconds=elapsed)
        stdout.seek(0)
        raw = stdout.read(MAX_OUTPUT+1)
        try:
            if len(raw)>MAX_OUTPUT:
                raise ValueError('response too large')
            data=json.loads(raw)
            if not isinstance(data,dict) or not isinstance(data.get('response'),str) or not data['response'].strip():
                raise ValueError('missing response')
            usage=data.get('usage',{})
            if not isinstance(usage,dict) or any(k not in ('input_tokens','output_tokens','cached_input_tokens') or type(v) is not int or v<0 for k,v in usage.items()):
                raise ValueError('invalid usage')
            if 'cached_input_tokens' in usage and ('input_tokens' not in usage or usage['cached_input_tokens']>usage['input_tokens']):
                raise ValueError('invalid cached tokens')
            activation=data.get('activation','unknown')
            if activation not in ('yes','no','unknown'):
                raise ValueError('invalid activation')
            # Only a trace can substantiate activation. Adapter claims are not independently verified.
            evidence=data.get('activation_evidence','')
            if not isinstance(evidence,str) or len(evidence)>4000 or (activation!='unknown' and not evidence.strip()):
                raise ValueError('invalid activation evidence')
            return dict(status='ok',response=data['response'],usage=usage,activation=activation,
                        activation_evidence=evidence,wall_seconds=elapsed)
        except (ValueError,UnicodeError,TypeError):
            return dict(status='invalid_output',wall_seconds=elapsed)


def execute(out, command, timeout=180):
    if not command or not math.isfinite(timeout) or timeout <= 0:
        raise ValueError('adapter command and positive timeout required')
    plan=read(out/'plan.private.json')
    if plan.get('automation'):
        raise ValueError('This experiment uses a built-in adapter. Resume it with evaluate --resume.')
    for condition,expected in plan['skill_hashes'].items():
        if skill_digest(out/'skill-snapshots'/condition)!=expected:
            raise ValueError('skill snapshot changed')
    results=out/'raw.private'
    results.mkdir(exist_ok=True)
    pending = [row for row in plan['runs'] if not (results / (row['run_id'] + '.json')).exists()]
    if not pending:
        return
    executable = shutil.which(command[0])
    if not executable:
        raise ValueError('Adapter executable was not found. Put it on PATH or use an absolute path.')
    command = [str(Path(executable).resolve()), *command[1:]]
    if len(command) > 1 and command[1].endswith('.py') and not command[1].startswith('-'):
        script = Path(command[1]).resolve()
        if not script.is_file():
            raise ValueError('Adapter script was not found. Use the path to a real adapter or run evaluate.')
        command[1] = str(script)
    for row in pending:
        target=results/(row['run_id']+'.json')
        if target.exists():
            continue # failures retained; do not selectively rerun in the same trial
        if digest(row['prompt'].encode())!=row['prompt_sha256']:
            raise ValueError('prompt changed')
        with tempfile.TemporaryDirectory(prefix='sdh-run-') as temp:
            w=Path(temp)
            (w/'prompt.txt').write_text(row['prompt'],encoding='utf-8')
            if row['condition']!='baseline':
                shutil.copytree(out/'skill-snapshots'/row['condition'],w/'skill')
            result=invoke(command,w,timeout)
        write(target,dict(run_id=row['run_id'],**result))


def review_packet(out):
    plan=read(out/'plan.private.json')
    # Randomized condition order is retained; no condition or usage metadata in packet.
    rows=[]
    for r in plan['runs']:
        p=out/'raw.private'/(r['run_id']+'.json')
        if p.exists():
            raw=read(p)
            if raw['status']=='ok':
                rows.append(dict(run_id=r['run_id'],case_id=r['case_id'],prompt=r['prompt'],response=raw['response']))
    return rows


def main():
    from benchmark_adapters import AdapterError
    from benchmark_automation import add_commands, compare, doctor, evaluate

    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='action',required=True)
    p=sub.add_parser('prepare'); p.add_argument('out',type=Path); p.add_argument('--agent',required=True); p.add_argument('--model',required=True); p.add_argument('--settings',required=True); p.add_argument('--cases',nargs='+'); p.add_argument('--trials',type=int,default=1); p.add_argument('--seed',type=int,default=42); p.add_argument('--competitor',type=Path); p.add_argument('--suite',choices=('scenario','activation'),default='scenario')
    p=sub.add_parser('run'); p.add_argument('out',type=Path); p.add_argument('--timeout',type=float,default=180); p.add_argument('--allow-external-execution',action='store_true'); p.add_argument('--adapter',nargs=argparse.REMAINDER,required=True)
    p=sub.add_parser('review'); p.add_argument('out',type=Path)
    add_commands(sub)
    a=parser.parse_args()
    try:
        if a.action == 'doctor':
            return doctor(a)
        if a.action == 'evaluate':
            return evaluate(a)
        if a.action == 'compare':
            return compare(a)
        if a.action=='prepare':
            cases=read(ROOT/'evals'/('cases.json' if a.suite=='scenario' else 'activation-cases.json'))
            plan=prepare(a.out,cases,a.cases or [c['id'] for c in cases],a.trials,a.seed,a.agent,a.model,a.settings,a.competitor,a.suite)
            print(f'Prepared {len(plan["runs"])} runs; no agent invoked.')
        elif a.action=='run':
            if not a.allow_external_execution:
                parser.error('explicit --allow-external-execution required; adapter may incur costs and has local process permissions')
            with run_lock(a.out):
                execute(a.out,a.adapter,a.timeout)
            print('Adapter attempts recorded; inspect status and grade independently.')
        else:
            with run_lock(a.out):
                write(a.out/'review.json',review_packet(a.out))
            print('Review packet created; responses may reveal condition.')
    except (AdapterError, ValueError, OSError) as error:
        parser.exit(2, f'Benchmark error: {error}\n')
    except KeyboardInterrupt:
        parser.exit(130, 'Benchmark interrupted. Completed attempts are available for resume.\n')

if __name__=='__main__':
    raise SystemExit(main())
