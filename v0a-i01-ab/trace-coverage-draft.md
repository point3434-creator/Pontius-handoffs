# Trace correction implementation and coverage draft

Non-cold Codex worker handoff, 2026-08-30. Unfrozen and uncommitted.
Branch codex/v0a-i01-trace in D:\Pontius-worktrees\codex-v0a-i01-trace.
Base policy r002: 2f4287f68a83fac4225a05a91daffdb3f2977a43.
Parent must review and layer the value and policy successor changes before a
separate freeze/cold review. Do not copy entire replay.py files over later host
publication changes: apply the attached draft patch or merge its disjoint hunks.

## Scope and result

Only trace.py, replay.py, test_v0a_trace.py and test_v0a_replay.py changed.
No sealed module, new module/test filename, writer/publication behavior, accounting
interval, ledger, cold report, fixture constant, source seal or authority was changed.

R2-06: canonical raw JSON is checked before value admission; duplicate keys,
nonfinite/overflow values, noncanonical JSON and over-deep malformed input receive
TraceInvalidError. Every row/event variant and nested action/timing/preparation/
settlement/pot schema has exact key/type/range checks. Counts, policy/hand identities,
response time partitions and flags, monotonic response order, accepted failure pairs,
terminal consistency, prefix digest and semantic digest are checked. Comparable exact
integer strengths retain the model's unbounded ordering domain; mixed integer/tuple
rank domains are refused. ParsedTrace retains ordered records. parse_trace documents
that structural validation is not successful legal replay.

R2-05: verify_successful_trace requires raw bytes and explicit expected fixture,
immutable blueprint, source commit, source manifest, mode and clock kind. It admits
value-only expectations before behavior, owns the betting/card walk, uses the unchanged
sealed action_for directly, and compares the actual recorded event/decision ordering,
script, full deal, state/card digests, selected action/reason and all settlement fields.
It never calls ReplayHost.run, HandRuntime.dispatch or either runtime selector. The
only runtime reuse is the pure source admission helper. Acceptance returns a frozen
VerifiedTrace summary, never a passed host receipt. Failed prefixes are inspectable
but cannot earn success, including the current producer shape whose failed triggering
event is omitted while its accepted decision/failure pair remains.

New oracle dependency (not a recurrence of closed R2-07): a real public-API sequence
produces contributions (0,1,2,15,15,5), with seats3/4 live and tied. Folded-only depth
thresholds must form one 38-chip award. The predecessor independently split layers,
which would round payouts to20/18 instead of19/19. red-v2 and final predecessor RED
retain the legal sequence and manual ((38,(3,4)), (0,0,0,19,19,0)) expectation. The
narrow correction merges adjacent identical eligibility before division; it never
calls production pot assembly. Parent explicitly accepted this discovered dependency.

## Fresh evidence

All payloads ran only in fresh disposable D-local shared-clone snapshots. Each run
asserted CPython executable/full version, -B, -P, cwd/src PYTHONPATH and scrubbed
environment before payload import. Overlay hashes were unchanged after execution.
Absolute Git was used. Logs and JSON receipts are create-only under trace-checks.
No broad suite, rehearsal, GPU, production identity or timing-evidence claim.

- red-final-311-receipt.json: frozen predecessor plus final test files only.
  Trace regressions:9 methods,129 failed subtest assertions and3 genuine untyped
  boundary errors (malformed hand identity, nested pot seat, deep decoded value).
  Replay regressions:8 methods,43 assertion failures for absent accepting checker
  and the independently demonstrated folded-depth oracle mismatch.
- green-final-311-receipt.json: actual CPython3.11.15,148 tests pass.
- green-final-314-receipt.json: actual CPython3.14.6,148 tests pass.
  Both:39 hand replay +34 trace +53 replay +22 contract faults.
- git diff --check: passes. Exactly the four approved paths are modified.

Earlier receipts are retained honestly. red-v3 contained a test import typo, corrected
before red-v4; draft-v3/v4 exposed invalid custom opponent scripts, corrected to legal
public-API schedules. draft-strength-red proves the draft's accidental nonnegative
rank constraint, removed before final GREEN. None is presented as final verification.

## Coverage and limits

Exercised: all nested variant key categories; malformed primitive/container/card/rank/
seat values; NaN/Infinity/overflow/noncanonical number spellings; duplicate keys and
prefix/semantic digests; source/configuration/policy/mode/clock bindings; illegal and
legal-but-wrong controlled actions; table hit/default selection; before/after/visible
state identities; actor/street/event/action ordering; payout/final-stack/pot eligibility;
showdown ranks/live mask; full A/B acceptance; nonpassive table hit; fold terminal;
actual14.5-second delayed mailbox using lawful emission reserve; accepted late and
accepted interrupted failed prefixes; exact response and interrupted counts; no caller
subtype hooks; profile observer proves no producer/selector rerun during acceptance.

Structural synthetic fixtures remain structural-only, with corrected internally valid
seconds, comparable ranks and digests. They are never successful legal replay controls.
Rebound negative controls calculate both digests independently so prefix mismatch does
not mask the tested rule. A separate deep-input refusal intentionally tests the decoder
boundary before later binding checks.

Trace-only acceptance proves declared pre-publication timing consistency, not complete
actual measured work or hidden checkpoint placement. It cannot establish source sealing,
external invocation authority, native file publication/finalization, or host completion
without that separate receipt. A final elapsed value over14 seconds does not by itself
prove work cutoff; true cutoff flags require a compatible observed prefix. The exact
ns-to-float partition check searches the actual integer conversion intervals instead
of applying an invented epsilon, including beyond float's exact integer range.

No cold review was performed or read by this worker. Root review and final combined
successor verification remain required before freezing this correction.

## Exact draft file hashes

- `src/pontius/v0a/trace.py`: `ecd519401b8f40cb05778d3d514deb334bd6688024971cae9ad35184d812ddc6`
- `src/pontius/v0a/replay.py`: `f201605780fbe20332d819637cc1413e16ba4114a743b8d42e4af5f5fb8a3fa5`
- `tests/test_v0a_trace.py`: `5ea023f069db3f869c637522dfd30387b09519de1956edd4d7c9d9af0266f94c`
- `tests/test_v0a_replay.py`: `5e3bda27b8291fc3be93fc24bd04d1685ca966980cee2228dff9d23e6109b12a`

Patch SHA256: `88c0a49c5dc336e00e2ca65804217b373dc6e26391f2a3fad70a5f939e01b902`.

```text
src/pontius/v0a/replay.py | 238 +++++++++++++++++++++++++++++++++++-
 src/pontius/v0a/trace.py  | 304 +++++++++++++++++++++++++++++++++++++---------
 tests/test_v0a_replay.py  | 231 +++++++++++++++++++++++++++++++++++
 tests/test_v0a_trace.py   | 269 ++++++++++++++++++++++++++++++++++++++--
 4 files changed, 970 insertions(+), 72 deletions(-)
```
