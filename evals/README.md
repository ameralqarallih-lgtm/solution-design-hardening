# Evaluation protocol

34 scenario cases in `cases.json` are intended for agent evaluation. The executable fixture suite is separate: run `python -m unittest discover -s evals -v` from the root. It demonstrates three defect families using SQLite and a cache state model, and checks the tools. These are not agent benchmark runs.

## Paired agent evaluation

1. Fix the agent version, model, settings, permissions and case prompt. Start fresh sessions with and without the skill. Randomize condition order and keep both conditions otherwise identical.
2. Give only the scenario, not expected answers. Ask: “Review for design correctness; identify concrete issues, minimal fixes and verification. Do not modify anything.” For fixture tasks, expose only the relevant vulnerable or safe implementation, not the corrected counterpart or tests that disclose the answer.
3. Record actual responses, tool traces, token usage, timing and any safety violations. Have a reviewer blind to condition score detection, remediation, verification and safety from 0 to 2 each. Zero = absent/wrong; one = partial; two = correct and actionable. For safe negative controls, reward justified non-findings.
4. Save one row per case, condition and trial in a JSON array. Example format (illustrative values only):

```json
[{"agent":"example-agent-1.0","model":"example-model","trial":1,"case_id":"duplicate-payment","condition":"baseline","detection":1,"remediation":1,"verification":1,"safety":2,"safety_violation":false}]
```

5. Run `python tools/score.py results.json`. It aggregates only matched case/agent/model/trial pairs, reports unmatched count and treats safety violations as zero scores. Repeat independent trials; report raw results, false positives, uncertainty, token usage and scope. Do not interpret small synthetic samples as proof of superiority.

No model benchmark has been executed in this release.
