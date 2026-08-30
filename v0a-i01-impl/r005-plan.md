# r005 plan — R2-03 third attempt, cause-flow refactor

Author: Claude, 2026-08-30. Contract: R2-03 only (second residual; the
root-cause note at `R2-03-root-cause.md` is the precondition and is published).
Design verdict adopted: STRAINED, bounded cause-flow refactor as the
coordinator recommended — not a host rewrite.

## Provenance and my own verification

The implementation contract below came from a category-first enumeration rather
than from the review's finding list, which is the specific habit both
root-cause notes identify. It swept the sealed ledger's API surface for closure
seams (12 found, exactly one missing its cause: `runtime.py:437`) and
enumerated the compound fault space as ordered pairs across the three channels
(32 schedules, 12 failing today), then attacked its own claims adversarially.

Two things I verified independently before adopting it:

- **The echo trap is real.** `clock.py` raises `ClockInvalidError` on *every*
  read after the witness has failed. Adding the missing abort catch naively
  would therefore append one code per echo rather than one per fault. The
  contract's rule R-C — append only if the witness was alive when the faulting
  operation began — exists for exactly this, and it is a trap I would have
  walked into unaided.
- **A new defect, G1, in no review**: a settlement-oracle exception escapes
  `ReplayHost.run` entirely. Reproduced: `ZeroDivisionError` propagates out of
  `run()`. It is in scope, because the category is "every failure inside host
  run is contained and typed", not "clock failures at the five named seams".
  Added to the RED set as **G1**: an escaping host-side exception must become a
  contained typed outcome. The default oracle can itself raise `AssertionError`
  on non-conservation, so this is not purely a test-seam concern.

Everything below is the enumeration's contract, adopted as written apart from
the G1 addition.

---

# R2-03 (r005) — Implementation Contract: Host Failure Closure

## 1. Cause-flow shape: single append-only cause journal, appended at occurrence

One ordered, append-only journal of `FailureCode` owned by `HandRuntime`, exposed as an immutable tuple (`closure_failures` stays the accessor) plus a `record(code)` entry point the host also calls. Every producer appends **at the moment the cause occurs**. The host reads it once: `primary = journal[0] if journal else None`, `secondary = journal[1:]`. No drain, no split, no ranking, no de-duplication.

Three rules make the order true:

- **R-A (initiate before cleanup).** `runtime.py:426` (`except _HandFailure`, the file's only such handler, against 30 raise sites) appends `failure.code` **before** calling `_release_boundary`. `_from_failure` never appends. `_reject` (`runtime.py:1038`) appends for the pre-boundary rejects, which have no cleanup.
- **R-B (cleanup appends its own real cause).** Each closure seam appends the typed code it actually caught, once.
- **R-C (echo rule).** A seam appends **only if `self._witness.failed` was False when the faulting operation began**. Once the witness is dead, `clock.py:47-48` raises `ClockInvalidError("a failed monotonic witness is never retried")` on any re-read — an echo of an already-recorded cause, and for a reversed clock a *fabricated* code. Without R-C the abort fix adds 150 spurious duplicates across the 414-schedule sweep and breaks B1/B2; with it the sweep diff is 0 outside the intended set.

Host side: `note`/`drain`/`split` (`replay.py:419-449`, 31 lines) are deleted; `note(outcome.failure.code)` at `:457` and `:474` disappear (the runtime already appended); `note(SETTLEMENT_MISMATCH)` at `:553` and `note(TRACE_WRITE_FAILED)` at `:598` become direct `record()` calls. The category filter at `replay.py:442` is deleted — ADR-0485:437,441-442 states a *temporal* rule; the docstring's categorical ban is an over-read, so removing it needs no fresh ruling. `replay.py:444` is dead code and goes with it.

**Why not "one immutable batch per operation."** A batch is correct only for a *leaf* operation. `bookkeeping` (`runtime.py:292-323`) and `publication_interval` (`:325-354`) are context managers whose bodies run host code that produces host causes: the entry fault is appended at `:312`/`:343`, then the body notes `settlement_mismatch` (`replay.py:553`) or `trace_write_failed` (`:598`). Sealing at exit emits `[settlement_mismatch, clock_invalid]` and breaks the passing `test_v0a_replay.py:562`. Making batches correct requires splitting both managers into six leaves plus a push/pop nesting stack — at which point every batch holds one element and the machinery is pure overhead with a new silent-ordering failure mode.

## 2. Closure seams that must route through the journal

| Seam | Site | Status today |
|---|---|---|
| boundary abort (`abort_transition_boundary`) | `runtime.py:437` | **MISSING** — `:438` catches with no binding, records nothing. R4-02. |
| bookkeeping entry | `runtime.py:310-312` | present; add R-C |
| bookkeeping exit | `runtime.py:318-321` | present; add R-C |
| publication entry | `runtime.py:340-343` | present; add R-C |
| publication exit | `runtime.py:349-352` | present; add R-C |
| finalize | `runtime.py:382-384` | present; add R-C |
| boundary close (transition) | `runtime.py:663-674` | return channel → journal via R-A |
| boundary close (showdown) | `runtime.py:624-630` | return channel → journal via R-A |
| `finish_action` (measured wall) | `runtime.py:784-810` | return channel → R-A; **also set `_clock_dead`** (today only `witness.failed` latches) |
| response snapshot | `runtime.py:759-761` | return channel → R-A |
| boundary open | `runtime.py:413-417` | Clock* via R-A; the bare-`RuntimeError`→`EVENT_ORDER` fabrication at `:416-417` is out of scope (§5) |
| ledger construction | `runtime.py:408-410` | return channel → R-A |

## 3. Compound test matrix

Construct all through `ReplayHost.run` with a faulting clock at read *k* of a counted clean run.

| ID | True order | Primary | Secondary | Construction | Today |
|---|---|---|---|---|---|
| A1 | event_order → clock_invalid | `event_order` | `clock_invalid` | `REJECT_SEAT` (script seat 3 = controlled); total 19, fault k=16 | **RED** |
| A2 | event_order → clock_reversed | `event_order` | `clock_reversed` | as A1, kind=reversed | **RED** |
| A3 | event_order → clock_invalid (OSError source) | `event_order` | `clock_invalid` | as A1, kind=source | **RED** |
| A4 | invalid_event → clock_invalid | `invalid_event` | `clock_invalid` | `REJECT_RAISE` (raise-to 1); total 21, k=18 (k=17 is the spine ledger's own abort) | **RED** |
| A5 | invalid_event → clock_invalid | `invalid_event` | `clock_invalid` | `TINY` stacks `(1,)*6`; total 9, k=6 | **RED** |
| D1 | trace_write_failed alone | `trace_write_failed` | — | occupied `trace.jsonl` | **RED** (R4-01) |
| D2 | trace_write_failed alone (OSError) | `trace_write_failed` | — | destination parent absent | **RED** |
| D3 | trace_write_failed → clock_invalid | `trace_write_failed` | `clock_invalid` | occupied destination, k=137 | **RED** (inverted today) |
| A6 | event_order → clock_invalid (host channel) | `event_order` | `clock_invalid` | `REJECT_SEAT`, k=17 or 19 | green (control) |
| A7 | invalid_event → clock_invalid | `invalid_event` | `clock_invalid` | `TINY`, k=7 | green (control) |
| B1 | clock_invalid only (dead-witness echo) | `clock_invalid` | — | `TINY`, k=5 | green; **naive fix breaks it** |
| B2 | clock_reversed only (echo fabricates) | `clock_reversed` | — | `TINY`, k=5, reversed | green; **naive fix breaks it** |
| C1–C4 | bookkeeping/publication/finalize × settlement_mismatch | per existing | per existing | `FIXTURE_A` + wrong oracle, k=134/135/136/138 | green (regression guard) |

RED set = A1–A5, D1–D3. B1/B2 and C1–C4 are the anti-regression guards that fail any naive or batch-shaped fix. Invert `test_v0a_replay.py:327` and rename it off "secondary failure".

Plus a direct unit test on the journal: append the same `FailureCode` twice, assert both survive in order (duplicates are unreachable through the boundary today — 1,833-schedule sweep found zero — but the journal must not de-duplicate).

## 4. Structural test for a seam nobody knows exists

**Conservation of genuine faults.** Wrap the sealed `ActionClockLedger` in a test-only recorder that logs every exception it raises together with `witness.failed` at method entry. Define *genuine* = raised while `witness.failed` was False. Sweep every single-fault schedule over each fixture (4 fixtures × every observation index × {invalid, reversed, source}) and assert, per run, that the multiset of typed clock codes in the journal equals the multiset of genuine ledger raises, in order. A new closure seam added later that forgets to append drops a genuine raise and fails conservation without anyone enumerating seams; an over-recording seam fails it from the other side.

Backstop, cheap and static: an AST test asserting every `except` clause in `runtime.py` naming `ClockInvalidError`/`ClockReversedError` either calls the journal appender or re-raises. This fails at authoring time, before the sweep runs.

## 5. Not covered, and transition risk

- **Bare ledger `RuntimeError`** has no code in the frozen vocabulary. Seams stay silent for it (`_record_closure_failure` docstring, `runtime.py:268-271`); a failing receipt can still carry `primary=None`. Record as an explicit gap, not a fix.
- **`runtime.py:416-417`** returns `EVENT_ORDER` for a ledger `RuntimeError` — a fabricated code asserting an ordering fault that did not occur. Unreachable via `ReplayHost` today; needs its own preregistration and a new typed code.
- **`ValueError`/`TypeError` at 624/663/784/759** are uncaught and provably unreachable through the public boundary; leave them uncaught rather than inventing a code.
- **Same-code duplicate pairs** are unreachable; pinned only by the unit test.
- **Risks.** (i) Moving the dispatch-failure append from host to runtime double-counts if any `note()` call site is left behind — the conservation test plus an exact-length assertion on green fixtures catches it. (ii) R-C is a behaviour change at five currently-passing seams; the 414-schedule diff must be **zero receipts changed** apart from the RED set. (iii) `finish_action` gaining `_clock_dead` changes `measurable` on a path that today latches only via `witness.failed`; assert `measurable`, never `accounting.complete` (which is False on healthy-clock rejections too, `runtime.py:359`, and would pass vacuously). (iv) Deleting `split()` removes the only place trace-write was special-cased; grep for other `TRACE_WRITE_FAILED` comparisons before landing.