# Engineering finding: alternative activation cells collapse at a join

This is an engineering check of an unfrozen replacement, not a cold-review
verdict or a new round disposition. No accepted A/B bytes were changed.

Inspected generator SHA-256:
33f944158ca20df62724d83d44a680440c455653100ba28d67b69954849cd8a5.
That is the immutable iteration05 overlay of frozen base
29c02f6fbd5eb0b7ddc9e816ef28f570b9839358, not the base generator itself.
Diagnostic: coordinator-join-probe-v1.py, SHA-256
1d91f234169e17833c7a40c35674564a6b6daa687d658cb06d93dbecd7341995.

The generated public diagnostic crosses capture mode (live cell or default),
activation order (unsafe first, safe first, both safe, both unsafe), and both
runtime choices at the same unknown branch. Eight analyzed programs have sixteen
independently executed harmless projections. Inspected subprocess source is never
executed. Both-safe controls permit explicit conservative refusal; the six programs
with a feasible mutation require a blocker.

Actual CPython 3.11.15 ran first, then 3.14.6, in separate disposable D-local
snapshots under the existing identity/import/environment policy. In each run,
seven programs meet their expectations and cell/unsafe-first fails. The true
choice executes body/write and then raises TypeError because the launch method
was replaced by None; the false choice executes body/sink and returns fixed.
Despite that feasible mutation, the public analyzer emits the original literal
[-m, fixed] subprocess capability and no blocker. Reversing the order refuses.
The raw source, both traces, returned rows and blockers are retained in the logs.

Mechanism: same-definition callables from separate factory activations preserve
different captured cell identities. The value join retains their authority
references and their common function definition, but call-environment creation
assigns each same-named captured value in turn. The last assignment hides another
feasible activation. This is a loss of alternatives at a transfer boundary.

The correction must preserve all admitted cell alternatives on read and later
capture, or explicitly refuse their ambiguous consumption. A write through an
ambiguous binding must not strongly overwrite every possible target: runtime
writes one cell, leaving the others unchanged. The analogous rule applies to
destructive updates through alternative collection identities. A single proved
target may retain its existing strong-update behavior. These are category-level
requirements, not a requested general Python heap interpreter.

The test author is extending the generated family to both statement and
conditional-expression selection. Original issued tests, classifications,
receipts and the 15-case scope correction remain immutable. GREEN must be run
against the eventual replacement; these RED receipts do not establish it.

Receipts: coordinator-checks/join-iteration05-311-receipt.json and
coordinator-checks/join-iteration05-314-receipt.json. Their corresponding .txt
files bind the raw outcomes. The runner's outer exit zero means receipt collection
succeeded; each receipt records payload exit one and the exact failed case.
