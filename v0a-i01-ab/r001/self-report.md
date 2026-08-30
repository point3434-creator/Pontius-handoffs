# r001 implementation report — R2-03 bounded redesign

Implementer: Codex. This is a self-report, not an independent review.
Candidate identity is in candidate.json; predecessor is v0a-i01-impl/r006.
Scope: four files, clock/runtime/replay and test_v0a_replay. No sealed file changed.

RED/GREEN receipts are in checks/; freeze-verification.json binds the final frozen
blobs to both final executed snapshots. All 127 focused tests pass on actual
CPython3.11.15 and3.14.6. No broad suites/GPU/rehearsal/owner execution occurred.

The witness retains a canonical source occurrence and separately owns later refusal
exceptions. The runtime drains the occurrence once before any later cause, while
independent equal-code errors remain separate. Both measured operations use one
explicit context manager; original body errors are retained before cleanup and are
replaced with a constant trusted signal, without string/metadata/traceback hooks.
The optional generator wrapper was removed from publication. Dispatch/finish_action
carry the actual clock occurrence through _HandFailure to the same retention path.

Initial implementation design was inspected read-only by ab_failure_design and the
scope plan by ab_scope_inventory; neither is a cold pass. Plan-amendment-01 preserves
Claude as ceremonial finalizer and the exact review/gate/authorization sequence.
The witness compatibility refinement and intermediate harness/encoding corrections
are disclosed in coverage.md, not silently discarded.

No full A/B clean claim is made here. Other correction contracts retain their board
standing. No source integration or ceremonial commit is authorized by this report.
