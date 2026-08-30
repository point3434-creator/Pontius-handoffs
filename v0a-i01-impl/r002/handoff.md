# Cold review: v0a-i01-impl/r002 (slice A fix round + slice B)

Candidate ref: `refs/heads/review/v0a-i01-impl/r002`
Candidate commit: `18c965d1f3445c253a6333c4d10899c1dcac0cc6`
Manifest SHA-256: `4cfd14ac7bfdb22e052bb9f625610657c01aafa07182acf58d19367a8816cb18`
Base commit: `b357d333fc2393b7fc7dcf31f30c86616208c817`
Tree: `35f00349a7538cffc02f8e81f71913251be200be`
Tier: C. Finalizer: Claude (first drafter this checkpoint). Reviewer: Codex.

The full commit and manifest bind identity; this path and the index only
locate them. The ref is local and has **not** been pushed. Read the
candidate's Git blobs, recompute the manifest under the whole-row byte sort,
and treat changed bytes or changed scope as requiring r003. R001 and r002 are
both immutable.

## Scope — review the delta, verify the rest

Ten paths differ from the base. Two are **byte-identical to r001** and were
reviewed there; their digests are stated so you can verify that claim rather
than take it on trust, and re-reviewing them is optional:

| Path | Status vs r001 |
| --- | --- |
| `src/pontius/v0a/__init__.py` | UNCHANGED `86d349c4b79f150a4439df8d63c8d20854572895aaf7960f27647e7b1f198a8a` |
| `tests/test_v0a_hand_replay.py` | UNCHANGED `f82b436eeec0e811d61e910c5ff3e01f3ccd6fe10325d86f03d748c65f9686d3` |
| `src/pontius/v0a/runtime.py` | CHANGED — F1–F7 fixes plus slice-B accounting |
| `src/pontius/v0a/model.py` | CHANGED — receipt use, exact schema string, V2 spine-reason enum |
| `src/pontius/v0a/clock.py` | CHANGED — source-fault normalization |
| `src/pontius/v0a/trace.py` | NEW — slice B |
| `src/pontius/v0a/replay.py` | NEW — slice B |
| `tests/test_v0a_trace.py` | NEW — slice B |
| `tests/test_v0a_replay.py` | NEW — slice B |
| `tests/test_v0a_contract_faults.py` | NEW — F1–F7 regressions |

Slice C (v0a origin classification and import policy, inventory admission,
CI gate) is still outstanding; its absence is scope, not a finding. The
legacy dependency baseline is untouched.

## What changed and why

**The r001 fix round.** All seven accepted findings were reproduced as
independent public-boundary regressions before any source change, and the RED
receipt against r001 behaviour is retained at `checks/r001-RED.txt` (8
failures, 10 errors across the seven findings). Corrections:

- **F1** — the outer boundary now opens as the first operation of every
  dispatch, before validation, visible-card construction, and V2 work. All
  four handlers share one boundary per dispatch, and a rejection closes it
  through `abort_transition_boundary` so no interval escapes accounting.
- **F2** — completion is explicit and irreversible. A showdown vector is
  accepted exactly once, policy is disabled before strengths are taken, a
  fold terminal also completes the hand, and every later event is refused.
- **F3** — the blueprint's canonical digest is bound once at hand start and
  every selection must match it, must carry the key recomputed for this exact
  state, and — when it claims a miss — must be exactly the passive default.
  Mismatches raise `source_binding_mismatch`. No second full-policy rehash is
  performed per decision, per the disposition's guidance.
- **F4** — the witness normalizes ordinary source faults to
  `ClockInvalidError` and stays permanently failed; ledger construction and
  boundary acquisition are inside the typed failure boundary; an established
  wall start is now carried into the interrupted record instead of being
  dropped.
- **F5** — once `deliver` is entered, no exception class can establish that
  publication never happened: any non-rejection exception yields
  `delivery_ambiguous` with `unknown`, never retried.
- **F6** — the acknowledgement is validated: an exact `DeliveryReceipt` bound
  to the emitted hand and action index, or the hand fails closed with honest
  uncertainty.
- **F7** — cutoff and deadline truths established by a valid snapshot are
  carried into interrupted records; `null` is used only where nothing was
  established, and `false` never is.

Review B's two non-blocking observations are also addressed: schema version
is compared as an exact `str`, and `spine_reason` is bound to the V2 enum
spelling rather than any ASCII text.

**Slice B** adds canonical trace serialization with strict parsing and a
run-independent semantic projection, and the explicit-deal replay host with
ADR-0287 fixtures A and B, an independent chip-depth settlement oracle that
never calls production pot assembly, terminal accounting through the
pre-publication cut, and a host completion receipt carrying
`terminal_publication_compute_seconds` outside the trace it describes.

## Evidence

Focused GREEN from a fresh disposable snapshot (`--no-hardlinks`,
`core.autocrlf=false`, detached at base, overlay digests recorded, scrubbed
environment, absolute `PONTIUS_GIT`, `-B -P`, interpreter identity asserted
before payload import), on both release interpreters:

| Suite | CPython 3.11.15 | CPython 3.14.6 |
| --- | --- | --- |
| `test_v0a_hand_replay.py` | 36 pass | 36 pass |
| `test_v0a_trace.py` | 25 pass | 25 pass |
| `test_v0a_replay.py` | 20 pass | 20 pass |
| `test_v0a_contract_faults.py` | 18 pass | 18 pass |

Receipts: `checks/r002-receipts.json`. Mutation probes: twelve mutations, one
per fix (and two per finding where a fix has two halves), all caught —
`checks/mutation-fixes.txt`. Earlier slice-B probing is summarised in
`../slice-b-self-report.md`.

## Review contract

Weigh in particular: whether the boundary-first restructure leaves any path
where adapter work escapes the wall or a boundary leaks unclosed; whether
completion is genuinely irreversible across fold and showdown terminals;
whether the blueprint binding can still be defeated by a delegating source;
whether any clock fault escapes `dispatch` or loses an established start;
whether delivery outcomes can still claim more than the acknowledgement
proves; whether interrupted timing can assert an unestablished flag; and, for
slice B, whether the semantic projection is genuinely run-independent,
whether the oracle is independent of production settlement, and whether
publication time can leak into the terminal row's totals.

Two open items the implementer flags rather than hides:

1. **`ReplayHost` accepts a `settlement_oracle` parameter** defaulting to the
   real oracle, so the mismatch path can be exercised with a deliberately
   wrong judge. The production comparison runs unchanged; only the judge is
   substituted. If you read this as weakening independence, say so — the
   alternative is leaving that branch untested.
2. **The controlled-seat guard** the r001 disposition ruled non-blocking is
   retained unchanged.

CLEAN requires that no material finding survive verification. Bind every
Critical/Important finding to this commit and manifest, cite exact frozen
locations, give a concrete failing scenario, and name the smallest correction
without implementing it. Run nothing from the primary checkout. Return
attributed findings to `reviews/review-<NN>-<reviewer>.md` and append one
verdict line to `../progress.md`.
