# AI and agentic application security - problem playbook

Use [security assessment guidance](SECURITY-ASSESSMENT.md) and [standards mappings](SECURITY-STANDARDS.md). These are defensive investigation leads; confirm trust boundaries, reachability and effective controls. Use only authorized isolated tests with synthetic data.

Read only the problem files you need. Every problem below uses this decision rule:

- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

| ID | Problem | Guidance |
|---|---|---|
| SDP-226 | Prompt injection trust-boundary failure | [SDP-226](problems/SDP-226.md) |
| SDP-227 | Excessive agent authority | [SDP-227](problems/SDP-227.md) |
| SDP-228 | RAG authorization bypass | [SDP-228](problems/SDP-228.md) |
| SDP-229 | Agent memory isolation failure | [SDP-229](problems/SDP-229.md) |
| SDP-230 | Knowledge and model input poisoning | [SDP-230](problems/SDP-230.md) |
| SDP-231 | Unsafe model output execution | [SDP-231](problems/SDP-231.md) |
| SDP-232 | Unbounded agent execution and cost | [SDP-232](problems/SDP-232.md) |
| SDP-233 | Untrusted tool or MCP integration | [SDP-233](problems/SDP-233.md) |
| SDP-234 | AI sensitive output disclosure | [SDP-234](problems/SDP-234.md) |
| SDP-235 | Agent-to-agent trust failure | [SDP-235](problems/SDP-235.md) |
