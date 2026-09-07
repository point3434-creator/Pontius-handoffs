# Final bounded-read qualification

Implementation, source review and required final acceptance are complete.
Specific ADR-0512 decision commit/push authorization remains pending.

Final candidate: `ab318584db351fdb2d19b3669b12e2975e18f6df`.
Manifest SHA-256: `facede42f50a7c62b36665c9641712b0b3f6091a2fe6f47b495768ec6ff89287`.

Both Python 3.11.15 and 3.14.6 passed 124 tests, with zero skips, in fresh
D-local snapshots of the exact final candidate, after review closure. Each
slot also passed runtime/source probes, inventory generation check, boundary
checker and status freshness. All command arguments, scrubbed environments,
full outputs, exits and elapsed times are retained in qualified311/qualified314.

Two fresh Tier C reviews of r003 found only Markdown width; both reviewers
then verified the complete final mechanical delta and returned CLEAN/SOUND.
Original NOT CLEAN substantive reports and final mechanical closures are
preserved under handoff/reviews. Mechanical closure is not a new cold pass.

The local final CI-block rehearsal passed all eight tests with the native
C-local floor interpreter and a D-local exact-final snapshot. It is not hosted
GitHub CI. Two incomplete launcher attempts remain retained; their missing
PATHEXT environment defect did not require any production or CI code change.

Earlier broad runs used a production-equivalent candidate. They are retained
as development evidence; the final broad runs close the exact-candidate gate
without relying on equivalence as a substitute for required execution.

Workspace task files equal all 15 frozen blobs. V2 differs from v1 only in
the self-origin and bounded read expression. Sealed source and fixture bytes,
both consumed comparison pins, and all 14 diagnostic pins are unchanged.

Full structured qualification: qualification.json.
Measurement conclusions: measurement-summary.json and the frozen performance report.
Authoring helper copies are retained in handoff/helpers and excluded from the decision.
