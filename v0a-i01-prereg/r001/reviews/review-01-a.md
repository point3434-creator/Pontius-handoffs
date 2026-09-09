Issuer: `/root/cold_review_a`

Verdict: **NOT CLEAN** — two Important contract findings.

Candidate: `073f0c5b8e6ad4f8d6e10dd9118b722186968ddf`  
Verified manifest: `4b01560395285a30fb65530fb776598d076c4a7bc687eed89d32e650c18dbdc0`.

1. **Important / medium severity, high confidence — Delivered actions lack a representable clock-failure record.**  
   Location: ADR-0485 lines **275–280**, related **214–215, 250–252, 323–327**.  
   A mailbox can acknowledge acceptance, after which the shared witness reverses or returns an invalid value during outer `finish_action()`. The unchanged ledger raises before returning its completion snapshot. Delivery is known, but no valid `emission_observed_ns`, elapsed interval, or final ledger outputs exist. The required decision timing object has no unavailable/null variant. Writing a complete decision invents timing; emitting only the action-bearing failure row fails the brief’s per-controlled-action decision-record requirement and loses its full context binding.  
   **Minimal remediation:** freeze an explicit unavailable-timing variant for known delivered actions, including which measurements remain valid and the typed clock failure. Require a real mailbox-acceptance → clock-failure control; forbid fabricated emission observations.

2. **Important / medium severity, medium confidence — The frozen semantic projection retains changing run identity.**  
   Location: ADR-0485 lines **295–304**, related **242–250, 373–374, 404**.  
   The specified projection includes decision rows with only `timing` removed. Every such row contains `run_id`, while correctness/rehearsal reruns use distinct unique identities. Therefore identical scheduled events, decisions, and settlement yield different projected bytes across valid reruns. The text does not settle whether replay compares this projection or an additional, unspecified selection of “semantic choices.” That leaves the preregistered deterministic comparison ambiguous.  
   **Minimal remediation:** specify the canonical projection’s exact container and field list, excluding run-specific identity from across-run comparison while validating those bindings independently. Require two distinct run identities with identical choices to compare equal.

The bootstrap exception is an explicit **pending controller decision**, not a defect: the candidate acknowledges its prospective change to ADR-0482 and keeps operational closure, budgets, population, and invocation authority unavailable.

Read-only inspection confirmed the parent, brief blob, baseline blob, two-file scope, and LF blob bytes. Public clock/spine APIs otherwise support the outer-ledger design. No tests, owners, writes, or other-reviewer communications occurred.
