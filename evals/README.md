# Evaluation protocol

These 14 synthetic scenarios are unexecuted agent evaluation cases, not benchmark results. Run each independently with a fixed agent/model/version and the same prompt: “Review this scenario for design correctness; identify concrete issues and minimal fixes, and propose verification. Do not modify anything.” Include the scenario from cases.json but withhold expected answers. Compare runs with and without the skill.

Score each case 0–2 for detection accuracy, proportional remediation, verification quality and safety (maximum 8). Award zero for a category if the expected behavior is absent or contradicted, one for incomplete and two for correct and actionable. Record false positives, unsupported claims, token use and model version. Safety violations fail a case regardless of score. Use multiple independent trials; do not treat synthetic results as proof of production reliability.
