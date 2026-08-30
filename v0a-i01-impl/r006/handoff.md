# Cold review: v0a-i01-impl/r006 — FIX round, R2-03 fourth attempt

Candidate ref: `refs/heads/review/v0a-i01-impl/r006`
Candidate commit: `c74b80628a89938ca585ef3240b5c267a7174d0f`
Manifest SHA-256: `2078d59a4a112bf29a2bd9faca9a2ca070bbd1028a940f2eeb617c9e1c31555f`
Base commit: `b357d333fc2393b7fc7dcf31f30c86616208c817`
Tree: `a22414541973b76ddd1efa1ca8fc41f51b7a4065`
Tier: C. Finalizer: Claude. Reviewer: Codex.

**Round kind: FIX (scope-frozen), one contract: R2-03, fourth attempt.** The
third residual is recorded, and the root-cause history at
`../R2-03-root-cause.md` carries an appended r005 supplement explaining the
host-body/origin gap. Controller directed continuation with a standing
condition: if this leaves R2-03 open, the contract changes hands rather than
receiving a fifth attempt from me.

## Scope — three paths changed, seven unchanged from r005

| Path | Status vs r005 |
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

## Coverage claim — attack this first

**Category**, taken from the r005 disposition rather than drawn by me, because
mine has been too narrow three times: every operation with a *body* and a
*cleanup*, across the cross-product of returned-mismatch versus raised-error,
ledger-origin versus direct-witness-origin, and entry / body / exit /
finalization position — such that the receipt carries each genuine cause with
its true type and true position.

**Enumeration method.** Not recall. Every measured interval with a body is now
reachable only through one owner, and an AST test enumerates any use of the
unowned private form. The previous three attempts each fixed the site the
finding named; this one makes the site unable to differ.

**Members and disposition.** Two owned operations exist (`owned_bookkeeping`,
`owned_publication`); the raw `_bookkeeping` and `_publication_interval` are
private and unused outside the runtime. All four matrix positions are covered
by tests; the returned-mismatch/exit-fault cell was already correct at r005 and
is retained as the opposing control.

**What falsifies this claim.** Any operation with a body and cleanup that does
not journal its body cause before cleanup runs; any genuine fault whose type or
position the receipt does not carry; any host-side exception that escapes.

**Where I would look first if I were you.** Whether `owned_publication`'s body
can fail in a way the trace-write path already handles differently; whether a
cause can be journalled twice when a body raises `OperationFailed` from a
nested owned operation; whether the AST test can be satisfied while still
reaching a raw interval through an alias; and the `_optional` wrapper around
publication, which predates this round.

## Correction

**One owner, not another site.** `owned_bookkeeping` and `owned_publication`
wrap the measured interval and catch the body's exception *inside* it, so the
body's cause is journalled before the interval's own exit can produce one. The
unowned intervals are private, so an operation cannot get the order wrong by
forgetting — it would have to reach past the public surface, and the AST test
fails if it does.

That closes **R5-01** (the body error no longer arrives after its cleanup
fault) and **R5-02** (a body-origin clock fault is classified and journalled by
the owner rather than assumed to have been recorded by a seam). `classify()`
gives clock errors their true type and everything else the operation's declared
`body_failure`, so exception type never again stands in for proof of retention.

`OperationFailed` signals that a cause is already journalled, so the host adds
nothing and nothing escapes `run()`.

## Evidence

RED against frozen r005 (`checks/r005-RED.txt`): both reviewer mechanisms and
the structural test fail there and pass here. The returned-mismatch control was
already green at r005 and is reported as such rather than claimed as a fix.

Focused GREEN from a fresh disposable snapshot, asserted interpreter identity,
scrubbed environment, `-B -P`:

| Suite | 3.11.15 | 3.14.6 |
| --- | --- | --- |
| `test_v0a_hand_replay.py` | 35 | 35 |
| `test_v0a_trace.py` | 25 | 25 |
| `test_v0a_replay.py` | 41 | 41 |
| `test_v0a_contract_faults.py` | 22 | 22 |

123 per interpreter; receipts in `checks/r006-receipts.json`.

Mutation probes (`checks/mutation-r006.txt`): ten mutations, all ten caught —
including *bypassing the owner for a raw interval*, which the structural test
catches. The conservation observer and the full-sweep tests from r005 are
retained unchanged and still pass.

## Review contract

Attack the coverage claim before the code; enumerate the category yourself and
tell me what the owner does not cover. Then judge whether body-before-cleanup
ordering now holds at every operation, whether any genuine cause can still be
lost or duplicated, and whether the owner can be bypassed.

State the required design verdict. This contract has failed three times; a
STRAINED or WRONG SHAPE verdict now is more useful to me than a CLEAN one that
does not hold.

Return attributed findings to `reviews/review-<NN>-<reviewer>.md` and append one
verdict line to `../progress.md`.
