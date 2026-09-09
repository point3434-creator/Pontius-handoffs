Issuer: /root/cold_review_b
Candidate: 073f0c5b8e6ad4f8d6e10dd9118b722186968ddf
Manifest: 4b01560395285a30fb65530fb776598d076c4a7bc687eed89d32e650c18dbdc0

Verdict: **NOT CLEAN — one Important finding (P2, high confidence).**

Candidate `073f0c5b8e6ad4f8d6e10dd9118b722186968ddf`, parent `ca0b2e41bbf5d9fc1649de20379299331de6591a`, and manifest `4b01560395285a30fb65530fb776598d076c4a7bc687eed89d32e650c18dbdc0` independently verified. Brief and legacy-baseline blob identities also match.

**P2 — The frozen trace cannot honestly represent a delivered action whose closing clock observation fails.**

Location: [ADR-0485, lines 275–280](/D:/Pontius/docs/decisions/ADR-0485-preregister-the-blueprint-only-v0a-hand-contract.md:275), together with lines 214–222, 250–252, and 323–334.

Concrete counterexample:

1. A valid controlled response starts.
2. The mailbox accepts its action and returns an unambiguous receipt.
3. The immediately required outer `finish_action()` encounters an invalid or reversed clock sample.

The sealed `ActionClockLedger.finish_action()` observes the clock before constructing or archiving its snapshot (`action_clock.py:546`); `_read_clock`/`_observe` raises for this schedule (`181–190`). Therefore no valid closing snapshot or `emission_observed_ns` exists.

The brief nevertheless requires a schema-v1 decision record for every controlled action. This candidate requires integer emission/elapsed nanoseconds and numeric ledger outputs, without a unavailable-timing variant. Substituting a previous sample would violate lines 186–188 and misrepresent the delivery observation. Recording only the proposed failure row preserves the action, but omits its required decision context and timing status. The terminal still counts that known delivered action.

The related pre-delivery failure case also lacks a place to preserve an interrupted response’s timing: failure rows contain no timing fields, and terminal totals contain only preparation and post-terminal work.

**Smallest fix:** Freeze an explicit failure-side action-record variant now. Preserve the action identity/context, known receipt, and available valid observations; mark closing timing unavailable with a typed reason and nullable unavailable fields. Define interrupted-response accounting and decision-count rules, forbid successful terminals for these cases, and require a real mailbox-acceptance → clock-failure acceptance control. Never manufacture an emission timestamp.

No other material finding survived this pass. Privacy separation, blueprint outcome distinctions, delivery ambiguity, claims limits, and deferred operating-budget authority are otherwise coherent at the proposed-spec level.

The ADR-0482 sequencing exception still requires explicit controller adoption; I did not assume it granted.

No files changed, tests ran, owners were invoked, or other reviewers were consulted. Git identity checks and `git diff --check` passed; no runtime behavior is claimed verified.
