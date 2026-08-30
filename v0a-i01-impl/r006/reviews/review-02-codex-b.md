# Cold review 02 — Codex B — r006

Reviewer: Codex independent cold reviewer B, 2026-08-30.
Ref: refs/heads/review/v0a-i01-impl/r006
Commit: c74b80628a89938ca585ef3240b5c267a7174d0f
Manifest: 2078d59a4a112bf29a2bd9faca9a2ca070bbd1028a940f2eeb617c9e1c31555f
Scope: Tier C FIX R2-03 only, versus r005
(a8582e6d6b53b55415dab79c4a54e252d00b74ad).

**Verdict: NOT CLEAN. Specification compliance: FAIL. Contract shape: SOUND.
Engineering design: STRAINED. Confidence: high. R2-03 remains open.**

## Important findings

1. **B1: the new owner invents a clock cause from a failed-witness refusal.**
   At runtime.py:414-416, classification uses exception type without establishing
   whether the cause was already retained. In real ReplayHost.run, fail the shared
   witness at settlement interval entry, then let the public settlement_oracle
   sample that same witness. One reversed source fault yields
   `[clock_reversed, clock_invalid]`; one invalid/source-error fault yields
   `[clock_invalid, clock_invalid]`. There is exactly one source fault and no
   source retry. The second entry is an echo, not a genuine later cause. This
   violates R2-03 exact typed-cause conservation. Preserve cause origin/retention
   across entry and body while retaining separate genuine same-code failures;
   enum deduplication is not a valid correction.

2. **B2: exception formatting can escape without a host receipt.**
   Runtime.py:416 evaluates `str(error)` before raising OperationFailed. A public
   settlement_oracle raising a ValueError subclass whose `__str__` raises
   RuntimeError causes ReplayHost.run to escape after journalling
   settlement_mismatch, returning no ReplayOutcome or completion receipt. The
   publication owner repeats this pattern at runtime.py:429. The executable case
   is the real settlement path. Failure-signal construction must preserve
   containment without relying on fallible callback formatting.

Both findings reproduce on actual CPython 3.11.15 and 3.14.6 without substituting
runtime, witness, ledger, or mailbox implementations. B2 has lower expected
frequency, but both violate required failure outcomes in the declared scope.

## Evidence and coverage judgment

The independently derived inventory predates opening handoff.md. Full ten-row
blob manifest, candidate tree/HEAD, snapshot imports, and legitimate checkout
CRLF translation were verified. The four existing focused suites pass 123 tests
per interpreter; 19 independent diagnostics per interpreter include both findings
and no probe errors. Ordinary raised/returned body failures followed by cleanup,
fresh body-clock faults, and publication-body/exit ordering pass their controls.

The coverage claim is too strong: new presence assertions miss extra causes,
and the earlier ledger-only observer does not observe direct body witness echoes.
The AST check is a narrow guard, not proof of all ownership paths. Same-runtime
nested timing is unsupported by the sealed ledger and is **not counted as a
finding or a new requirement** here. Its limits are retained in the notes.

Required behavior is exact cause conservation and reliable receipt containment.
A token, richer failure object, constant marker message, or stronger tests are
advisory techniques, not additional mandated design. No deferred trace, policy,
value, broad/GPU, experiment, integration, or commit claim is made.

Detailed observations, commands, environment identities, and receipt hashes:
`checks/cold-b-verification-notes.md` (SHA-256
9230f73e09ad2d6da0ef4040fad803468b6396a665c2ed928af523615ff05eb6).
Recommendation: keep this candidate rejected for R2-03 and apply the controller's
stated change-of-hands condition.
