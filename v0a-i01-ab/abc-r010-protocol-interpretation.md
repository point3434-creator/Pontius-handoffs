# r010 protocol interpretation

ADR-0485's existing three-review circuit breaker is interpreted with the current
controller workflow's per-contract residual count, not packet serial numbers.
The initial C helper-identity review was r008. r009 was its first frozen FIX and
recorded a first residual; coordinator and cold-review reports on those same
bytes are one residual round, not separate attempts. r010 is the next frozen FIX.
Earlier packet numbers cover distinct accepted A/B contracts. Internal engineering
runs are retained verification records, not extra cold-review verdicts.

A second residual on this contract triggers the existing separate root-cause and
design reassessment requirement; this interpretation grants no waiver. The current
bounded proof/effect replacement follows a pre-edit scope/discovery assessment.
The four-path FIX allowlist remains generator, inventory contract tests and the
ordinary inventory/profile pair. Record the actual r009-to-r010 delta separately.
A/B's ten accepted blobs and remaining C files are preserved, and are carried in
the full 17-path main-based integration manifest only for preservation review.
Any governance wording cleanup stays outside that manifest.

Pinned current workflow and CLAUDE copies govern reviewers, with exact hashes.
Initial inputs exclude coverage contents and implementation narratives. Reviewers
record an independent source/invariant inventory first, then open hashed deferred
coverage. Reviewers are mutually blind and never implemented this repair.
Two fresh CLEAN verdicts precede the enumerated currentCI12+v0a5 CPU wall.

Claude remains checkpoint finalizer. Controller approval must identify the final
candidate after reviews and gates. No generic earlier permission transfers to new
bytes. No source seal, rehearsal, guarded profile, GPU or experimental authority
is granted by this engineering candidate or its focused checks.
