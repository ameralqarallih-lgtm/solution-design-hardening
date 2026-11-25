"""Run one read-only Codex activation probe for the benchmark adapter protocol."""

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from benchmark_adapters import MAX_RESPONSE, cli_result, cli_run, event_records


SKILL_PATH = ".agents/skills/solution-design-hardening/skill.md"
TITLE = re.compile(r"(?m)^# Solution Design Hardening\s*$")


def mentions_skill(value):
    return SKILL_PATH in re.sub(r"[/\\]+", "/", value).lower()


def activation(events, stderr):
    blocked = any(mentions_skill(line) and "blocked by policy" in line.lower()
                  for line in stderr.splitlines())
    for event in events:
        item = event.get("item", {})
        if event.get("type") != "item.completed" or item.get("type") != "command_execution":
            continue
        if not mentions_skill(item.get("command", "")):
            continue
        if item.get("exit_code") == 0 and TITLE.search(item.get("aggregated_output", "")):
            return "yes", "Completed command trace returned the installed skill body."
        blocked = True
    if blocked:
        return "unknown", "Host trace recorded an attempted installed skill read that did not succeed."
    if any(event.get("type") == "turn.completed" for event in events):
        return "no", "Completed trace contained no observed read of the installed skill body."
    return "unknown", "Host trace did not contain a completed turn."


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True)
    parser.add_argument("--trace-dir", type=Path)
    args = parser.parse_args()
    cwd = Path.cwd()
    executable = shutil.which("codex")
    if not executable:
        parser.error("Install Codex CLI and put it on PATH.")
    subprocess.run(["git", "init", "--quiet", cwd], check=True, capture_output=True)
    snapshot = cwd / "skill"
    if snapshot.is_dir():
        shutil.copytree(snapshot, cwd / Path(SKILL_PATH).parent)
    command = [
        executable, "-a", "never", "exec", "--sandbox", "read-only", "--json", "--ephemeral",
        "--ignore-user-config", "--ignore-rules", "--disable", "apps", "--disable", "browser_use",
        "--disable", "computer_use", "--disable", "plugins", "-c", 'web_search="disabled"',
        "-c", "project_doc_max_bytes=0", "-c", 'model_reasoning_effort="low"',
        "--model", args.model, "-",
    ]
    prompt = (cwd / "prompt.txt").read_text(encoding="utf-8")
    code, raw, stderr = cli_run(command, cwd, 150, prompt)
    if args.trace_dir:
        folder = ROOT / args.trace_dir
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f"{cwd.name}.jsonl").write_bytes(raw)
        (folder / f"{cwd.name}.stderr.txt").write_bytes(stderr)
    if code or len(raw) > MAX_RESPONSE:
        raise SystemExit(code or 1)
    result = cli_result("codex", raw)
    state, evidence = activation(event_records(raw), stderr.decode("utf-8", errors="replace"))
    if args.trace_dir:
        evidence += f" Trace: {cwd.name}.jsonl."
    print(json.dumps({"response": result["response"], "usage": result["usage"],
                      "activation": state, "activation_evidence": evidence}))


if __name__ == "__main__":
    main()
