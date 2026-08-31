# R2 input closure finding and bounded correction

Important: two case envelope references do not resolve.

This finding binds H aa75536cad0ae54b76b02f9351cd7bc789d7f443, manifest
96d1b71a3a08b73d2cf1bb09d3ac06473253b6291addf2fbefc541e3bbe3b41f,
population tests-checks/rewrite-r2-identity-population-v1.json SHA256
30295f39daafcf265103cd78f3de50393c9111633ca3d5f8515e3f77c9a1197a.

Both hidden-cell-joined-reached and hidden-cell-joined-dormant retain the
original envelope_ref name_environment_public. The new envelopes map omits
that key. A controller resolving all case references from this manifest would
fail before executing those unchanged controls, or would have to invent a
fallback outside the frozen specification. Neither is acceptable.

Category: closure of every reference in the population's case registry, while
preserving the eight required original descriptors and their original execution
envelopes. Root enumerated every population case's envelope_ref against all map
keys; precisely these two are missing. Independent input review discovered the
same defect. The root static result 104771163002c01b9f2510272b882f9a7ca3016e71befce1c4ace12fdb7886cc
also verifies exact source/Model inverse deltas, unchanged witness data other
than the discriminator, all eight original descriptors, caps and test module.
No Model, sensitive fixture, analyzer or test payload executed.

Authorize the original input author to issue a population v2 only, adding the
exact original name_environment_public envelope descriptor alongside the new
identity_name_environment_public descriptor. Do not redirect hidden-cell cases,
edit old files, alter any case/source/Model/witness/expectation or change the
new identity envelope. Retain a minimal semantic diff, all-case reference
closure check, and successor handoff. New provenance may name this frozen
finding; any other change must be explained for review.

This is prospective engineering input repair, not a product bug-fix claim or
permission to execute. The new population must be frozen and rereviewed before
executable harness authoring. The held R1 candidate and old R2 harness remain
unchanged. Full implementation and final cold-review obligations remain open.
