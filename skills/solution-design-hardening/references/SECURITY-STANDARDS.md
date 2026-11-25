# Security standards and traceability

Versioned reference baseline, reviewed 2026-11-25. These are independently authored **candidate relevance mappings**, not official OWASP or CWE crosswalks, certification, or proof of compliance. Validate each applicable CWE and requirement against the original version before using it in a formal report. A blank mapping is intentional where no sufficiently specific candidate is assigned. No standards content is bundled wholesale.

## Reference versions and scope

- [OWASP Top 10:2025](https://top10.owasp.org/2025/): web risk awareness categories (A01–A10).
- [OWASP API Security Top 10:2023](https://api-security.owasp.org/editions/2023/en/0x11-t10/): API risk awareness categories (API1–API10).
- [OWASP ASVS 5.0.0](https://asvs.owasp.org/downloads/): technical requirements; select applicable requirement IDs and verification level at assessment time, using the original specification. Do not infer an ASVS pass from a catalog match.
- [CWE](https://cwe.mitre.org/data/index.html): weakness taxonomy. IDs below are candidate weakness labels; individual applicability and abstraction levels have not been exhaustively independently verified.
- [OWASP LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) and [Agentic Applications 2026](https://genai.owasp.org/top-10-for-agentic-applications-2026/): use for AI trust boundaries, tool authority, supply chain, data and memory, output handling, execution budget and inter-agent communication. Consult exact risk IDs at assessment time rather than reuse a previous edition's numbering.
- [NIST SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final): secure development lifecycle, organizational preparation, software protection, production and vulnerability response. Version 1.2 draft is not treated as final here.
- [SLSA 1.2](https://slsa.dev/spec/v1.2/): artifact provenance and supply chain assurance. Determine the applicable track and level from actual evidence; signatures and SBOMs alone do not establish a level.
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks): choose the exact product/version benchmark and deployment profile; not a universal pass/fail checklist.
- [MITRE ATT&CK](https://attack.mitre.org/): use adversarial behavior as a threat-model input when applicable, not a software weakness or compliance catalog.
- [STRIDE](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-getting-started): threat discovery by identity, integrity, accountability, confidentiality, availability and privilege boundaries.

## Applying standards without overstating coverage

Start with applicable assets, actors and trust boundaries. Use the catalog to find weaknesses, select relevant versioned standard requirements, and record requirement ID, source, applicable scope, evidence, result and residual gap. A risk category may cover many different controls. Review all applicable ASVS requirements independently when ASVS is requested; do not equate the 235-problem baseline with full ASVS, CIS, ATT&CK or SLSA coverage. For AI, use the actual deployed system and relevant 2026 risk definitions. Record standards version changes separately from stable SDP IDs. If sources or versions cannot be verified, record a verification task.

## Candidate problem crosswalk

| Problem | OWASP web / API risk categories | Candidate CWE |
|---|---|---|
| SDP-007 | A08:2025 | — |
| SDP-018 | A08:2025 | — |
| SDP-051 | A06:2025, API4:2023 | — |
| SDP-073 | A06:2025, API4:2023 | — |
| SDP-078 | A07:2025 | CWE-294 |
| SDP-099 | A01:2025, API1:2023 | CWE-862 |
| SDP-112 | A08:2025 | CWE-345 |
| SDP-120 | A01:2025, API1:2023 | — |
| SDP-131 | A01:2025 | CWE-367 |
| SDP-132 | A01:2025 | — |
| SDP-133 | A07:2025 | — |
| SDP-134 | A01:2025 | CWE-441 |
| SDP-135 | A09:2025 | CWE-532 |
| SDP-136 | A06:2025, API4:2023 | CWE-770 |
| SDP-150 | A01:2025 | — |
| SDP-156 | A04:2025 | — |
| SDP-157 | A09:2025 | CWE-778 |
| SDP-161 | A07:2025, API2:2023 | CWE-287 |
| SDP-162 | A07:2025, API2:2023 | CWE-384 |
| SDP-163 | A07:2025, API2:2023 | CWE-614 |
| SDP-164 | A07:2025, API2:2023 | CWE-307 |
| SDP-165 | A07:2025, API2:2023 | CWE-347 |
| SDP-166 | A07:2025, API2:2023 | CWE-613 |
| SDP-167 | A07:2025, API2:2023 | CWE-352 |
| SDP-168 | A07:2025, API2:2023 | CWE-204 |
| SDP-169 | A07:2025, API2:2023 | CWE-640 |
| SDP-170 | A07:2025, API2:2023 | CWE-287 |
| SDP-171 | A01:2025, API1:2023 | CWE-639 |
| SDP-172 | A01:2025, API5:2023 | CWE-862 |
| SDP-173 | A01:2025, API3:2023 | CWE-915 |
| SDP-174 | A01:2025, API3:2023 | CWE-200 |
| SDP-175 | A01:2025, A10:2025 | CWE-636 |
| SDP-176 | A01:2025, API5:2023 | CWE-269 |
| SDP-177 | A06:2025, API6:2023 | CWE-799 |
| SDP-178 | A01:2025, API8:2023 | CWE-942 |
| SDP-179 | A05:2025 | CWE-89 |
| SDP-180 | A05:2025 | CWE-943 |
| SDP-181 | A05:2025 | CWE-78 |
| SDP-182 | A05:2025 | CWE-79 |
| SDP-183 | A01:2025, API7:2023 | CWE-918 |
| SDP-184 | A01:2025 | CWE-352 |
| SDP-185 | A05:2025 | CWE-611 |
| SDP-186 | A08:2025 | CWE-502 |
| SDP-187 | A01:2025 | CWE-22 |
| SDP-188 | A05:2025 | CWE-1336 |
| SDP-189 | A01:2025 | CWE-601 |
| SDP-190 | A02:2025 | CWE-444 |
| SDP-191 | A06:2025 | CWE-434 |
| SDP-192 | A06:2025, API10:2023 | CWE-20 |
| SDP-193 | A02:2025 | CWE-798 |
| SDP-194 | A02:2025 | CWE-312 |
| SDP-195 | A04:2025 | CWE-312 |
| SDP-196 | A04:2025 | CWE-319 |
| SDP-197 | A04:2025 | CWE-295 |
| SDP-198 | A04:2025 | CWE-916 |
| SDP-199 | A04:2025 | CWE-327 |
| SDP-200 | A04:2025 | CWE-323 |
| SDP-201 | A04:2025 | CWE-330 |
| SDP-202 | A04:2025 | CWE-320 |
| SDP-203 | A04:2025 | CWE-359 |
| SDP-204 | A01:2025 | CWE-306 |
| SDP-205 | A02:2025 | CWE-284 |
| SDP-206 | A01:2025 | CWE-862 |
| SDP-207 | A08:2025 | CWE-345 |
| SDP-208 | A02:2025 | CWE-250 |
| SDP-209 | A02:2025, API8:2023 | CWE-668 |
| SDP-210 | A02:2025, API8:2023 | CWE-1188 |
| SDP-211 | A02:2025 | CWE-269 |
| SDP-212 | A02:2025, API9:2023 | CWE-1059 |
| SDP-213 | A03:2025 | CWE-1104 |
| SDP-214 | A03:2025 | CWE-427 |
| SDP-215 | A08:2025 | CWE-494 |
| SDP-216 | A03:2025 | CWE-250 |
| SDP-217 | A03:2025 | CWE-522 |
| SDP-218 | A03:2025 | CWE-345 |
| SDP-219 | A03:2025 | CWE-1104 |
| SDP-220 | A09:2025 | CWE-778 |
| SDP-221 | A09:2025 | CWE-732 |
| SDP-222 | A09:2025 | CWE-778 |
| SDP-223 | A10:2025 | CWE-209 |
| SDP-224 | A02:2025 | CWE-16 |
| SDP-225 | A07:2025 | CWE-613 |
| SDP-226 | A06:2025 | CWE-74 |
| SDP-227 | A01:2025 | CWE-250 |
| SDP-228 | A01:2025 | CWE-862 |
| SDP-229 | A01:2025 | CWE-200 |
| SDP-230 | A08:2025 | CWE-345 |
| SDP-231 | A05:2025 | CWE-94 |
| SDP-232 | A06:2025, API4:2023 | CWE-770 |
| SDP-233 | A08:2025 | CWE-345 |
| SDP-234 | A01:2025 | CWE-200 |
| SDP-235 | A01:2025 | CWE-345 |
