# Cold review: v0a-i01-impl/r005 — FIX round, R2-03 third attempt

Candidate ref: `refs/heads/review/v0a-i01-impl/r005`
Candidate commit: `a8582e6d6b53b55415dab79c4a54e252d00b74ad`
Manifest SHA-256: `e9b0baf12e258d66a92169d38137cbf2f42317158b6515ac377f745bbc52093a`
Base commit: `b357d333fc2393b7fc7dcf31f30c86616208c817`
Tree: `5d373871b27bed5ef026150b816d684a588b75c3`
Tier: C. Finalizer: Claude (first drafter). Reviewer: Codex.

**Round kind: FIX (scope-frozen), one contract: R2-03.** Second residual, so
the root-cause note at `../R2-03-root-cause.md` is published as the
precondition and this candidate contains nothing else. R3-01 policy authority
and the deferred R2-04/05/06/09/10 are absent by design.

## Scope — three paths changed, seven unchanged from r004

| Path | Status vs r004 |
| --- | --- |
| `src/pontius/v0a/runtime.py` | CHANGED |
| `src/pontius/v0a/replay.py` | CHANGED |
| `tests/test_v0a_replay.py` | CHANGED |
| `src/pontius/v0a/__init__.py` | UNCHANGED `86d349c4b79f150a4439df8d63c8d20854572895aaf7960f27647e7b1f198a8a` |
| `src/pontius/v0a/clock.py` | UNCHANGED `d229ca9a5a3f00ef73401b6aca415922840760dd62873759c50b3bfa95285ea4` |
| `src/pontius/v0a/model.py` | UNCHANGED `30aa2b8f7fbe86a7d106a27b3d52362b891a7ed0b222a858911e59e5d93301b0` |
| `src/pontius/v0a/trace.py` | UNCHANGED `ca994d35be0c2a2c368727cdc11abee7a71ba5e7f7d95e62fc24bc7e89ba03ed` |
| `tests/test_v0a_hand_replay.py` | UNCHANGED `8603e88be2d874c77a6e9d2b732508f42be68a4fcd45d7921f30725810d8dfc3` |
| `tests/test_v0a_trace.py` | UNCHANGED `15b7cb1c06cf6468f7ec5dbab3e01366e177c76e806a7a61dfb6ac05387ef498` |
| `tests/test_v0a_contract_faults.py` | UNCHANGED `85c15ae71e6e5685124c7c9d276a94dd593ef96a0dd7a131e27b3ac8d0fd87e9` |

## Coverage claim — please attack this first

**Category.** Every point at which a failure arising inside `HandRuntime.dispatch`
or `ReplayHost.run` can fail to reach the receipt with its true type and its
true position in occurrence order.

**Enumeration method.** Systematic sweep of the sealed ledger's API surface for
sites that close, abort, stop or finalize a boundary or interval (12 found), plus
generation of ordered pairs across the three failure channels — initiating,
cleanup, host (32 schedules) — rather than working from the r004 finding list.
Both were produced independently of my own recall, then attacked adversarially.

**Members and disposition.** Twelve closure seams; exactly one
(`runtime.py:437`, the abort path) was missing its cause and is the R4-02
mechanism. Two failure-return paths exist in the runtime (`_from_failure`,
`_reject`); both now journal, as does `_clock_reject`, which previously
returned a failure with no cause. Ordered-pair schedules: the compound cases
that failed at r004 are listed in the RED set below.

**What falsifies this claim.** Any schedule producing a genuine fault whose
type or position the receipt does not carry. The conservation test below is
written to be exactly that falsifier, over an independent observer.

**Where I would look first if I were you.** Nested faults — a cleanup fault
while a host interval is already open; a fault during trace *writing* rather
than during publication measurement; anything reaching `_reject` after the
runtime is already dead; and whether `feed()` inside the runout loop has a path
I have not considered.

## Correction

One append-only journal on the runtime, appended **at the moment each cause
occurs**, read by the host as `primary = journal[0]`, `secondary = journal[1:]`.
No drain, no split, no category ranking, no deduplication. The r004 category
rule that kept a trace-write failure out of primary is deleted, per the R4-01
ruling that the first observed typed host cause is primary regardless of
category.

Three rules make the order true. The dispatch handler journals the **initiating
cause before running its own cleanup**, so a cleanup fault can never precede
what caused it — the R4-02 inversion. Each seam journals the code it actually
caught, once. And a seam records only if the witness was **live as its own
operation began**: after the witness dies every later read raises again, and
recording those echoes would fill the journal with faults that never
independently occurred — for a reversed clock, with the wrong code.

That echo rule is the part I would have got wrong unaided. I also had to sample
liveness *before* the fallible call rather than inside the handler; sampling it
after meant the genuine first fault looked like an echo and was suppressed.

**Rejected design, with the reason:** one immutable batch per operation. The
bookkeeping and publication context managers run *host* code in their bodies, so
sealing a batch at exit emits `[settlement_mismatch, clock_invalid]` for a
schedule where the clock genuinely came first — inverting the ordering it exists
to fix.

**G1, a defect no review raised**: an exception from host-side settlement work
escaped `run()` entirely — reproduced with `ZeroDivisionError`. Contained now
and typed. I judged it in scope because the category is "every failure inside
host run is contained and typed", not "clock failures at the named seams". The
default oracle can itself raise `AssertionError`, so it is not only a test seam.

## Evidence

RED against the frozen r004 bytes, recorded in `checks/r004-RED.txt`: the
compound schedules, the conservation property, and the write-first-cause test
all fail there and pass here. `R3_02TypedClosureCauseTests` is green on r004 by
design — it is r004's own regression guard, carried forward.

Focused GREEN from a fresh disposable snapshot, asserted interpreter identity,
scrubbed environment, `-B -P`:

| Suite | 3.11.15 | 3.14.6 |
| --- | --- | --- |
| `test_v0a_hand_replay.py` | 35 | 35 |
| `test_v0a_trace.py` | 25 | 25 |
| `test_v0a_replay.py` | 37 | 37 |
| `test_v0a_contract_faults.py` | 22 | 22 |

119 per interpreter; receipts in `checks/r005-receipts.json`.

**The category test, stated in contract terms.** `R2_03ConservationTests` wraps
the sealed ledger in a recorder that observes every fault it genuinely raises,
sweeps every observation of two fixtures in both fault kinds, and asserts the
receipt's ordered clock causes **equal** the genuine raises — not merely
overlap. It mentions no journal, no seam and no internal field, so it survives a
different implementation of the cause flow and would fail for a seam nobody has
enumerated. Its first run caught a flaw in my own observer (double counting,
because `_observe` delegates to `_read_clock`).

Mutation probes, `checks/mutation-r005.txt`: eight mutations, all eight caught.
Three initially survived and **all three were test weaknesses, not code
weaknesses** — conservation compared presence rather than sequences so an echo
was invisible; the G1 test pinned the single exception class it raised; and
nothing exercised the reject path's journalling. All three are closed, and the
probe is in the packet so you can judge whether the closures are real.

## Review contract

Attack the coverage claim before the code — enumerate the category yourself
first, and tell me what my method missed. Then judge whether occurrence order
is genuinely preserved across the runtime/host boundary, whether the echo rule
suppresses anything genuine, whether any host-side failure can still escape,
and whether the conservation test would survive a different implementation.

Please state the required design verdict — SOUND, STRAINED, or WRONG SHAPE.
This contract has now failed twice; if the shape is still wrong I would rather
hear it now than after a fourth attempt.

Return attributed findings to `reviews/review-<NN>-<reviewer>.md` and append one
verdict line to `../progress.md`.
