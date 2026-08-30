# Trace acceptance correction plan and coverage draft

2026-08-30, Codex non-cold implementation. Tier C FIX for R2-05/R2-06.
Base: policy r002, 2f4287f68a83fac4225a05a91daffdb3f2977a43.
Scope: src/pontius/v0a/trace.py, src/pontius/v0a/replay.py,
tests/test_v0a_trace.py, tests/test_v0a_replay.py only. No freeze until root reviews
and layers this correction after the separate value candidate. Claude owns C.

Strict parser checks canonical finite JSON; exact row/event/nested schemas;
identity, index/count/timing/delivery consistency and both digests. Parsing is
structural, never successful replay. Preserve ordered records. The public accepting
checker lives in replay.py, takes raw bytes and explicit expected source/configuration/
policy bindings, and walks its own betting/card state plus bound fixture script/deal.
It never runs HandRuntime, ReplayHost or the runtime selector. Pure policy admission
and sealed kernels remain shared authorities. Independently derived selection and
settlement must match all recorded fields; successful trace verification cannot prove
host publication/finalization without its receipt. Failed prefixes never earn success.

Discovery: enumerate every row variant and nested field from ADR-0485; JSON failure
routes; record ordering and paired decision/failure identities; clock variants; policy,
visible-state, schedule and settlement boundaries. New canonical negative controls
start from real host traces and independently rebind both digests so identity checks
do not mask another rule. Preserve structural-only synthetic fixtures as such.
RED matrix: wrong types/keys/ranges/enums/nonfinite/canonical form, invalid source and
policy bindings, illegal and legal-but-wrong actions, state/card/selection identities,
missing/reordered decisions, false counts and completion, malformed timing, settlement
and showdown tampering. Positive A/B, distinct run IDs, lawful emission reserve,
failed prefixes, odd chips and fold controls. Prove checker does not rerun the host.

Limits: no new writer, incremental publication or accounting interval; no trace-only
proof of measured work completeness, hidden real-time checkpoint positions, source seal
or host completion. A final duration above 14 seconds alone is not a work-cutoff fault.
Interrupted prefixes lack proof of checkpoints not recorded. Existing failed producer
traces may omit the triggering failed event; preserve honest structural failures.
No new module/test filename, sealed change, broad/GPU/owner/rehearsal/authority claim.

Oracle risk: current chip-depth oracle appends each contribution layer while the kernel
merges adjacent layers with identical eligibility. Prove any mismatch before correcting
only the independent oracle behavior needed for this trace acceptance contract.

Expected 900-1400 changed lines including tests; reassess actual size and scope.
Tests first on frozen predecessor in fresh disposable D-local snapshots; actual 3.11.15
first then 3.14.6, -B -P, exact cwd/src PYTHONPATH, scrubbed environment and absolute Git.
Retain immutable logs/exit/overlay/interpreter receipts under trace-checks. The final
coverage record will distinguish exercised, excluded and unresolved cases. Falsifier:
a malformed or semantically wrong supplied trace obtains successful verification, or
a supported valid trace is refused by an invented contract. No ledgers or cold reviews.
