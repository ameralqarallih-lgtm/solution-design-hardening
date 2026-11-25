# Authentication and identity — problem playbook

Use [security assessment guidance](SECURITY-ASSESSMENT.md) and [standards mappings](SECURITY-STANDARDS.md). These are defensive investigation leads; confirm trust boundaries, reachability and effective controls. Use only authorized isolated tests with synthetic data.

## SDP-161 — Authentication bypass

- **Failure:** An unauthenticated caller reaches protected operations.
- **Detection:** Trace routes, middleware order, alternative transports and public-route exemptions.
- **Remediation and safeguards:** Require validated identity at every protected entry point; explicitly inventory public routes.
- **Verification:** Exercise anonymous, invalid and valid identities on every route class; public health route remains accessible.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-162 — Session fixation

- **Failure:** A pre-authentication session remains usable as the authenticated session.
- **Detection:** Inspect login and privilege-change session rotation and old session invalidation.
- **Remediation and safeguards:** Rotate session identifiers on authentication and privilege changes; invalidate previous identifiers server-side.
- **Verification:** Log in with an existing anonymous session; verify old identifier cannot access protected state.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-163 — Session theft and unsafe cookies

- **Failure:** Session credentials are exposed or reused outside intended context.
- **Detection:** Inspect cookie flags, transport, session persistence, logout and browser access.
- **Remediation and safeguards:** Use Secure, HttpOnly and context-appropriate SameSite cookies; limit lifetime, revoke sessions and prevent credential leakage.
- **Verification:** Check cookie attributes and logout with synthetic sessions; ensure necessary cross-site login still works.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-164 — Credential stuffing and brute force

- **Failure:** Repeated authentication attempts compromise accounts or deny service to victims.
- **Detection:** Inspect login throttling across replicas, MFA and account lockout abuse paths.
- **Remediation and safeguards:** Use risk-based per-account and per-source controls, MFA and recovery; avoid permanent attacker-triggered lockouts.
- **Verification:** Use synthetic accounts and bounded attempts across replicas; verify limits and legitimate recovery.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-165 — Token validation failure

- **Failure:** Untrusted or wrong-context tokens authenticate callers.
- **Detection:** Inspect verifier configuration, issuer, audience, expiry, token type and key trust; distinguish decoding from validation.
- **Remediation and safeguards:** Use maintained protocol library; validate signature, allowed algorithms, issuer, audience, expiry and intended token type; reject untrusted keys.
- **Verification:** Reject synthetic expired, wrong issuer/audience and incorrectly signed tokens; accept a valid intended token.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-166 — Token revocation gap

- **Failure:** A revoked session or credential remains valid beyond policy.
- **Detection:** Trace logout, disable-account and key compromise propagation across services.
- **Remediation and safeguards:** Define revocation latency, short lifetimes and appropriate introspection or revocation state; avoid assuming self-contained tokens revoke instantly.
- **Verification:** Disable a synthetic identity and measure denial across services within policy; test provider outage behavior.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-167 — OAuth and OIDC binding failure

- **Failure:** A callback, authorization code or identity assertion is accepted for the wrong client or session.
- **Detection:** Inspect exact redirect registration, state, nonce, PKCE and issuer/client binding; check library defaults.
- **Remediation and safeguards:** Use authorization code flow with PKCE where applicable, exact redirect allowlist, session-bound state and OIDC nonce validation; use standard library.
- **Verification:** Verify mismatched state, nonce, redirect and code verifier are rejected in test identity provider; normal login works.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-168 — Account enumeration

- **Failure:** Authentication or recovery reveals whether an account exists.
- **Detection:** Compare status, response body and observable timing for existing and nonexistent identities.
- **Remediation and safeguards:** Use consistent outward responses, bounded attempts and asynchronous recovery where appropriate; avoid leaking account status.
- **Verification:** Compare synthetic accounts with repeated bounded samples; verify legitimate recovery is unaffected.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-169 — Unsafe account recovery

- **Failure:** Recovery credentials allow unauthorized resets or repeat use.
- **Detection:** Trace reset token generation, storage, expiry, redemption atomicity and session revocation.
- **Remediation and safeguards:** Use high-entropy purpose-bound single-use tokens stored safely, atomic redemption, short expiry and post-reset session policy.
- **Verification:** Redeem synthetic token concurrently, then after expiry; only one authorized reset succeeds.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

## SDP-170 — Workload identity impersonation

- **Failure:** A service accepts a spoofed workload identity or credentials from the wrong environment.
- **Detection:** Inspect service token issuer/audience, certificate identities and environment bindings.
- **Remediation and safeguards:** Use authenticated workload identities, short-lived credentials and explicit audience/environment trust; authorize each operation.
- **Verification:** Reject wrong workload and environment credentials in isolated test; accept intended identity.
- **Decision:** Record scope, existing protection, expected denial and permitted behavior; if runtime or policy is unknown, mark Requires Verification.

