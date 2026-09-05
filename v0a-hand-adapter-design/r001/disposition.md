# Controller disposition: design r001

Candidate 21474e3d5b105c1709205df1eb5543417abb5a0a; manifest
ce327c6982338c148d26d4d73cad978ad05b49596520449337d2cc9cb9be0bc9.

Not adoptable. Reviewer A issued CLEAN, Spec/Quality PASS, C/I/M 0/0/0, SOUND.
Reviewer B issued FAIL, Spec/Quality FAIL, C/I/M 1/0/0, SOUND. A's pass does not
override B's unresolved source-identity finding. Both original reports remain
unchanged and attached to this candidate, not transferred to a correction.

- Review A SHA-256: 4c381331948775b86916f99324db27fc0286d87a499fc7e410841573ff208790.
- Review B SHA-256: 19e85c4e99a2928de87d9b01f7d4bafaa6a90b6cd9ee9614d2496ab225e141ab.

B/C1 is accepted. A separate synthetic bare-repository control reproduced the
mechanism: HEAD kept original commit 37b66aeeaaeea085d47c955db33233680ede71a0;
ordinary commit-path blob reading returned replacement bytes, while
--no-replace-objects returned the original bytes. The repository is
../../metadata-replace-control.git; no project source or payload executed.
The retained receipt is ../../metadata-replace-control.json, SHA-256
653e3b949816ebed2b2381c55b62b919b9ed30e731a32944f6efa5c3ee93ac51.
Installed Git documentation corroborates the same switch semantics. The actual
review repository has no replacement refs, so r001's own identity is unaffected.

Authorize no new source surface. Use the one already budgeted correction round
to make every prospective source identity/object read explicitly raw, add the
real-CLI replacement refusal control, and name related filtered/archive-view
limits. Keep schemas, host/reader/output contracts, six pins, size budgets and
parked lanes unchanged. This is substantive source-binding clarification, not
an ADR-0492 mechanical correction; r002 needs two fresh independent cold reviews.

Both design verdicts are SOUND. No redesign trigger or source implementation
exists. The third-candidate stop rule remains; a further required correction
after r002 returns to the controller. No publication, adoption, hand run or
existing-file edit is authorized by this disposition.
