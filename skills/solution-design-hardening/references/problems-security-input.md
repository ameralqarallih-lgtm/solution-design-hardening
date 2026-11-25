# Injection and untrusted content - problem playbook

Use [security assessment guidance](SECURITY-ASSESSMENT.md) and [standards mappings](SECURITY-STANDARDS.md). These are defensive investigation leads; confirm trust boundaries, reachability and effective controls. Use only authorized isolated tests with synthetic data.

Read only the problem files you need. Every problem below uses this decision rule:

- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

| ID | Problem | Guidance |
|---|---|---|
| SDP-179 | SQL injection | [SDP-179](problems/SDP-179.md) |
| SDP-180 | NoSQL query injection | [SDP-180](problems/SDP-180.md) |
| SDP-181 | Command injection | [SDP-181](problems/SDP-181.md) |
| SDP-182 | Cross-site scripting | [SDP-182](problems/SDP-182.md) |
| SDP-183 | Server-side request forgery | [SDP-183](problems/SDP-183.md) |
| SDP-184 | Cross-site request forgery | [SDP-184](problems/SDP-184.md) |
| SDP-185 | Unsafe XML processing | [SDP-185](problems/SDP-185.md) |
| SDP-186 | Unsafe deserialization | [SDP-186](problems/SDP-186.md) |
| SDP-187 | Path traversal and archive extraction | [SDP-187](problems/SDP-187.md) |
| SDP-188 | Template injection | [SDP-188](problems/SDP-188.md) |
| SDP-189 | Unsafe redirect | [SDP-189](problems/SDP-189.md) |
| SDP-190 | HTTP parser disagreement | [SDP-190](problems/SDP-190.md) |
| SDP-191 | Unsafe file upload | [SDP-191](problems/SDP-191.md) |
| SDP-192 | Unsafe upstream API consumption | [SDP-192](problems/SDP-192.md) |
