# Independent correction inventory, before deferred coverage

Reviewer: fresh Codex metadata-correction reviewer, r002.
Candidate: `12df7106b2fca3b25ed4f57115ba9a31e70b6815`.
Manifest: `c09f4bcc313e987764597f49ef703e8794e76e7be725dc52a642850803a5bb1c`.

Recorded before opening r002 coverage.md or the prior r001 review report.

The incorporation invariant is exact equality to combined source
`c7de23de276c50463d831f3983fede82a5400ce8` on the original 12 paths, with
only ADR-0491 and generated STATUS added to that scope. Governance output
must have raw LF bytes without BOM or trailing whitespace. The renderer,
historical sources, earlier acceptance identities and authority boundaries
must remain unchanged.

Independent discovery used r001/r002 raw git comparisons, the 14-path base
delta, candidate identity, ADR-0490, complete ADR-0491 and the unchanged
status renderer's output path. The complete r001/r002 changed-path set is
STATUS.md alone. Its displayed raw diff changes all 88 lines; the comparison
ignoring end-of-line whitespace is empty. This identifies CRLF-to-LF output
serialization as the candidate correction category, pending exact byte
counts and equality after replacing CRLF with LF.

Related sites to verify: STATUS.md raw blob and packet copy; ADR-0491 raw blob;
all 12 incorporated blobs; the manifest's raw row bytes and sorting; parent,
tree and immutable ref; unchanged status_generation.py and its test module;
the previous review's binding correction; the existing source-review and
acceptance pins. There is no source-code correction or new authority surface
in the discovered delta. Generated STATUS has long historical ledger rows,
so line width there is renderer behavior, not a correction-specific change.

Verification map: exact identities and scope -> raw git objects and independent
SHA-256 row construction; serialization -> raw bytes and whole-content equality;
incorporation/authority -> unchanged ADR and bound records; generated freshness
-> separately required post-CLEAN isolated checks on 3.11.15 then 3.14.6.
No full source implementation rereview or broad source test rerun is intended.
