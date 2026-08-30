# v0a-i01-impl slice B — implementer self-report

Implementer: Claude (drafter/finalizer this checkpoint). Date: 2026-08-30.
Base: master `b357d333fc2393b7fc7dcf31f30c86616208c817`.
Worktree: `D:/Pontius-worktrees/v0a-increment-1`, branch `v0a/increment-1`.
Status: focused GREEN, not frozen, not committed, no authority claimed.
Slice A remains frozen and under review as `v0a-i01-impl/r001`; slice B was
written in parallel and does not touch r001's frozen bytes on disk — but it
does modify `runtime.py`, so a slice-B round will present that file as
changed against r001.

## What slice B adds

| File | Lines | Responsibility |
| --- | --- | --- |
| `src/pontius/v0a/trace.py` | 812 | Canonical serialization, strict parsing, semantic projection, create-new writes |
| `src/pontius/v0a/replay.py` | 578 | Explicit-deal host, fixtures A/B, independent oracle, host completion receipt |
| `src/pontius/v0a/runtime.py` | +130 | Public-ledger accounting: interval classification, bookkeeping, publication, finalization |
| `tests/test_v0a_trace.py` | 475 | 25 trace contract tests |
| `tests/test_v0a_replay.py` | 330 | 20 replay/oracle/accounting tests |

Total across slices A and B: 4,621 lines. Slice A alone was 2,296; the
combined candidate is well past the ~3,000-line proactive-slicing threshold,
which is why slice B belongs in its own round with review scoped to the
paths whose digests differ from r001.

## Fixtures reproduce ADR-0287 exactly

Both controls are derived by the ADR-0485 seed rule — SHA-256 of the seed
label, first eight bytes big-endian, modulo 24, selecting that zero-based
lexicographic permutation of `cdhs` — applied as a whole-deal suit renaming
that preserves ranks, actions, and payouts:

| Control | Seed label | Permutation | Result |
| --- | --- | --- | --- |
| A | `pontius-v0a-hand-replay-v1/control-A` | `cdhs → hcsd` | 12-chip single pot, four controlled emissions, seat 3 K-high-straight win |
| B | `pontius-v0a-hand-replay-v1/control-B` | `cdhs → hdsc` | pots `(24, 10, 16, 30)`, payouts `(16, 10, 24, 30, 0, 0)`, two controlled emissions |

Fixture B's four side pots and their per-layer winners match ADR-0287's
independently constructed expectations exactly, through the real runtime and
the real betting kernel. The suit renaming is disclosed determinism, not
sampling: it preserves every hand ranking, which is why the historical
expectations still bind.

## The oracle is a real judge

`chip_depth_settlement` recomputes pots and payouts from contribution depth
alone and never calls production pot assembly, per the ADR-0287 gate reused
here as an engineering control. It is proven independent three ways: it
reproduces fixture B's expectations standalone from bare contributions; it
returns different payouts when the strength ordering changes; and a
deliberately wrong oracle injected into the host makes the hand fail closed
with `settlement_mismatch`, an empty terminal settlement, and `passed=false`.

## Terminal accounting

Following the r5 contract addition: the outer ledger stays open past betting
termination; every non-response interval closes through the sealed public API
and is classified exactly once by whether betting was already terminal at the
interval's entry; the terminal row's two totals close at the pre-publication
cut; and the terminal row's own construction, serialization, and write are
measured in one final interval reported only in the host completion receipt
as `terminal_publication_compute_seconds`. A test proves publication does not
move either counter, and that the trace contains no publication field.

## Evidence

**RED before source** for both modules (trace tests failed on absent
`pontius.v0a.trace`; replay tests failed on absent `pontius.v0a.replay`).

**Focused GREEN, disposable snapshot, dual interpreter** (fresh
`--no-hardlinks` clone, `core.autocrlf=false`, detached at the base commit,
overlay digests recorded, scrubbed environment, `-B -P`, interpreter identity
asserted before payload execution):

| Interpreter | hand_replay | trace | replay |
| --- | --- | --- | --- |
| CPython 3.14.6 | 36 pass | 25 pass | 20 pass |
| CPython 3.11.15 | 36 pass | 25 pass | 20 pass |

**Mutation probes.** Nine mutations against trace/replay/accounting after an
initial all-green run; eight caught. Two rounds of probing found three real
test defects, all fixed:

1. **Every strict-parsing test was passing for the wrong reason.** The
   mutation helper re-serialized rows, so any change to a non-terminal row
   broke the terminal's prefix digest and raised *before* the rule under test
   ran. Duplicate-key, unknown-key, and record-index rules were effectively
   untested. The helper now rebinds the prefix digest so each rule is
   isolated, the prefix digest keeps its own dedicated test, and a guard test
   asserts the helper itself produces an otherwise-valid trace.
2. **A path-escape test was masked by my own leaked state.** An earlier probe
   run had written `escape.jsonl` into the shared temp directory, so the
   existence check rejected the escape before the escape check ran. The test
   now confines the escape target to a directory it owns and asserts no file
   was created.
3. **The oracle's dead-money handling was never exercised** — no fixture has
   a seat that folds after contributing, so removing the folded filter
   changed nothing. Added a case where a folded seat holds the best strength
   and must collect nothing while its chips stay in the pot.

**Known non-catching mutations,** documented rather than chased:

- *Interval durations inflated by 1 ns.* No test pins exact accounting
  totals; pinning them would couple the suite to the sealed ledger's internal
  observation count and break on any refactor. Classification, non-fabrication,
  and separateness are all covered; absolute precision is not.
- *`O_EXCL` removed from the trace write.* The explicit existence check still
  rejects. The paired mutation (removing the existence check) *is* caught,
  because `O_EXCL` alone raises the wrong exception type — so both guards are
  individually load-bearing and neither is dead.

## Open items for the reviewer

1. **Settlement-oracle injection.** `ReplayHost` accepts a `settlement_oracle`
   parameter defaulting to the real `chip_depth_settlement`. It exists so the
   mismatch path can be exercised with a deliberately wrong judge — the
   production comparison logic runs unchanged; only the judge is substituted.
   If the reviewer reads this as weakening the independence guarantee, the
   alternative is to leave the mismatch branch untested, which I like less.
2. **Slice A's unreachable controlled-seat guard** (carried from the r001
   self-report) is still open and unchanged.

## Not done

Slice C: v0a origin classification and import policy in the boundary checker
with its own boundary tests, `STABILIZATION_TEST_FILES` admission with
inventory/profile regeneration and honest census refresh, and the CI gate.
The legacy dependency baseline remains untouched and unregenerated. No
rehearsal or production identity exists; run identities are
`pontius-v0a-hand-replay-v1-correctness-*` only, and the host refuses any
production identity outright.
