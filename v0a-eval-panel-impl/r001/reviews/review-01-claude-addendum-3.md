# Third addendum to cold review 01 — Claude — v0a-eval-panel-impl/r001

Issued 2026-09-09. New record; nothing earlier is rewritten. This addendum
**downgrades I-01 from Important to Minor** in light of a controller ruling
delivered after the second addendum, and records why.

Binding: candidate `e39d3b93695bfc601d051e8e71f334eef4d10d19`, manifest
`4f16c97f50734f06cc6bcd5286a87d355aaf4f8589f8796de1e33a8c5b47c405`.

## Controller ruling (2026-09-09), verbatim intent

"I decided to drop Python 3.11 and just use 3.14; I have no need for backwards
compatibility." The project's mandated interpreter is CPython 3.14.6 only. This
is not yet reflected in the repository (`README.md` still says 3.11 or newer;
the candidate brief says "3.11.15 before 3.14.6"), and it is not in the
packet's pinned `inputs/controller-rulings.md`, whose digest is fixed by the
handoff; the finalizer should carry it into the next round's rulings file.

## Effect on I-01

The measured failure (second addendum) is the naive-summation residual on
CPython 3.11. On 3.14, the built-in `sum()` returned exactly `0.0` in 2,000 of
2,000 orderings, and that is structural, not luck: every term is `0` or an
exact multiple of one value `2p`, partial sums stay below about 2 in magnitude,
so each addition's rounding error is captured exactly by Neumaier's two-sum and
the compensation term accumulates without rounding; the final `s + c` of a true
zero is exactly `0.0`. For this term structure the reference is **exact** on
CPython ≥ 3.12: an exact production tie gives `S_check = S_bet = 0.0` and `max`
selects CHECK, matching production; non-ties agree in sign because
`S_bet = 2·S_check` exactly. The concrete failing scenario therefore does not
occur under the ruled environment. I-01 is no longer an Important defect.

## What remains — Minor

1. **Unstated dependency.** The candidate's action-comparison predicate is
   correct only because CPython ≥ 3.12's compensated `sum()` is exact for this
   term structure. The candidate does not say so; a future interpreter change
   or a reference reimplemented with explicit accumulation would reintroduce
   the r001 defect silently. Smallest correction: state the interpreter floor
   as an environment requirement of the reference check, and keep the exact
   tie in the reference sample so the assumption is exercised.
2. **Stale environment requirement.** The brief's "Python 3.11.15 before
   3.14.6" and the design's matching sequence contradict the ruling. Any
   correction is a byte change and hence an r002; this alone requires one.

The tie-case comparison rule proposed earlier is no longer *required*; it
remains a cheap hardening and is advisory.

## Standing of the two reviews

Under the candidate as frozen (3.11 first), review-01's I-01 was correct and
review-02's CLEAN did not engage the tie case. Under the environment the
controller has now ruled, review-02's CLEAN is the closer verdict and
review-01's finding reduces to the Minor items above. Both statements are
true; the ruling arrived between them. The receipts in `checks/` stand as
evidence for both.

## Revised verdict from reviewer 01

**Defect verdict: NOT CLEAN — Minor only (C/I/M 0/0/2).** Design verdict
**SOUND**, unchanged. The Minor items are correctable in one round together
with the environment statement.
