# C helper-provenance Stage 0 decision

Root reviews and adopts the independent binding_engineer category inventory and
central-admission design, following the r008 cold review's public failures. The
category is helper identity at the callee evaluation point, not receiver spelling.
This is a bounded repair in generator + inventory tests; existing A/B and other C
files remain unchanged. New source waits for meaningful RED in a fresh floor clone.

Design:
1. Registry hits discover candidates; they never prove that a current name/member
   still identifies that definition. Missing proof for a sensitive candidate is an
   explicit blocker even with fixed literal argv. Apply the same admission rule
   to local-function expansion, not only class methods.
2. Carry exact class/instance/helper-callable provenance through the existing
   source-ordered flow. Parameters and lexical bindings override global/helper
   seeds. Divergent/unknown/unbound provenance does not collapse to raw spelling.
3. A helper callable proves both definition identity and binding mode. Keep the
   descriptor/default/positional-only fixes. Capture the callable before argument
   evaluation; later argument-side root rebinding must not reinterpret it.
4. Certify the original descriptor member as well as its qualifier. Do not build
   a general Python object heap. Recognized member/namespace mutation or escape
   may conservatively poison the involved helper identity; unsupported reflection,
   descriptors, metaclasses, replacement and alias patterns must explicitly refuse.
   An already extracted callable retains its own identity across later root-name
   rebinding. Any additional supported mutation precision needs a concrete test.
5. Preserve the proper comprehension and nested-scope semantics already modeled
   by source flow. Do not alter the exception visitor's enclosing-local semantics
   or add disconnected per-spelling blacklists. Meter added work under the existing
   analysis budget; no silent cap/zip truncation or approximate approval.

Discovery inventory: all parameter kinds; local/chained/unpacked/annotated/augmented
assignment, deletion and annotation-only locals; for/with/except/match targets;
walrus expressions; four comprehension forms, multiple/nested targets and deferred
consumption; nested functions/lambdas/classes/captures/global/nonlocal; imports and
new definitions; source-order joins/restoration/early exits; aliases and qualifier
chains; method replacement/deletion including class body; reflective namespace
mutation; unsupported dynamic lookup/construction/scope forms. Affectedness beyond
reviewed reproductions is source-inspection hypothesis until RED establishes it.

Meaningful tests use public derive_design_review and independent pure-Python return
projections; sensitive fixture subprocesses never run. Fixed argv exposes false
approval; differing helper argv catches wrong-definition selection. Negatives must
record explicit blockers. Opposing positives cover known ordinary/static/class
bindings, reversed self/cls names, original signature/default semantics, unbound
function calls, lexical captures, first comprehension iterable/outer scope, and
callee capture before argument effects. Unsupported cases must be labeled as
refusals instead of being silently removed from the contract.

Sequence: new category tests -> floor RED -> bounded source changes -> selected
existing flow/binding regressions and new GREEN on3.11 then3.14 -> release exact
owned hashes/report to root. Root performs combined ordinary regeneration, census
refresh, full affected snapshots, fresh immutable round and two cold reviews.
No broader wall on r008, no capability/baseline/optional/GPU/lifecycle authority,
and no source finalization approval is implied.
