# Finalizer ruling 02: I-01 corrected on new source

Date: 2026-09-09. Finalizer: Codex. This is a disposition, not a cold review.
Correction packet: v0a-eval-panel-timing/r002.
Candidate: a40e29ca432fa6024a29033efebdaa5b8a31f968.
Manifest: fc9b71e953da8bec6e4919376aed3687efc4ac02da0b77cab2473152246d7df2.
Ref: refs/heads/review/v0a-eval-panel-timing/r002.

I-01 is RESOLVED on this new candidate. Timing correction: CLEAN / SOUND.
Two independent cold source reviews returned CLEAN / SOUND without required
corrections. Focused verification passed 40 cases with zero skips. The subsequent
broad gate accounted for 593 cases: 583 passed and
10 optional SciPy skips, exit 0, source_verified true. All execution
used CPython 3.14.6. Native integration and strict warning gates passed.

measure() executes once without allocation tracing, records body clock endpoints
before postchecks/reporting, and refuses an active external tracer while leaving
its ownership unchanged. Timing mode and unavailable traced-memory metadata are
explicit at every measurement and are required by the full-pool estimator.
Native Job memory remains separate. No historical duration is divided by a
synthetic diagnostic ratio or relabeled as an untraced measurement.

The full source, reviews, original receipts, limitations and scope are recorded
in ../../v0a-eval-panel-timing/r002/disposition.md.
Disposition SHA-256:
0391d12a2190e9f1aee7cc23ea45c9190fb2270eee12fe4a9da23e97a3f97081

Ruling 01 remains valid for d8d291cc and 9fce4bf, which still contain I-01.
Those bytes and historical reports have not changed. This ruling closes the
finding only on the named descendant. It does not waive unrelated recorded
Minors or establish the measured resource decision required before steps 4-7.

The source is locally frozen and eligible for the controller's exact-candidate
adoption decision. No ceremonial adoption, public push or retained capacity /
preflight run occurred. The measured prerequisite remains a separate gate.
