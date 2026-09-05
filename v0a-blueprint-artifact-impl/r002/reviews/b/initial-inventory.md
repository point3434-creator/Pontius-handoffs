# Review B initial inventory, before deferred FIX coverage

Candidate 5e56e4454f7b8ccb360d3e36245abc33318349bb; manifest
6d5e14a64466f8aaa874d4bdf62ada439703eb74911a7b4dc4445c14b2af13b5.

Read the base CLAUDE/workflow, ADR-0490, three adopted design documents, both
controller extensions, frozen source diff and both frozen tests, and immutable
blueprint value consumer. No r002 deferred coverage or prior reviews read yet.

Initial invariant and related-path inventory:

1. Exact wire root/entry/key/action fields; duplicate decoded names at every
   object depth; UTF-8/BOM, trailing content, float/constants, excessive nesting.
   Probe parser hooks separately from record-constructor failures.
2. Exact source/entry/key/action records and exact tuple/string/int/bool/enum
   values before any foreign method/representation/equality/hash invocation.
   Include object.__new__ incomplete exact records, later entries and nested
   history scalars/arrays, source IDs and malicious int/string/tuple subclasses.
3. Six-seat widths, private canonicalization, ordered board/pending/history,
   no private/board overlap, history action/null/return relationships; unchanged
   validators remain authoritative rather than full reachability reconstruction.
4. Uniform integer domain on all scalar, vector, nullable/history/action paths;
   640 digits accepted independently of interpreter default; 641 refused before
   conversion. Accepted decode -> unchanged digest -> encode -> decode closes.
5. Unicode scalar strings in both directions; astral escape pairs preserve
   identity, Python surrogate pairs refused, no normalization or byte ceiling.
6. Literal full-key and canonical byte oracle, entry permutations, empty policy,
   raw-byte identity versus unchanged policy identity; temporary-file bytes.
7. Real HandRuntime hit raise 6 and exactly one delivery, miss passive call,
   illegal hit no delivery; ReplayHost full hand and independent reader with
   separate expected policy, payout and stacks. Preserve acceptance controls
   despite consolidating tests to the combined 300-line bound.
8. Actual public source gate positive and negatives: shadow flat module,
   sibling/deeper module, forbidden import, legacy ingress; exact driver origin
   and three internal edges only; unchanged v0a six-file/runtime bytes.
9. Registration-only deltas and unchanged generator/analyzer/driver test logic;
   generated historical IDs and zero grants; manual/source/test/fixture budgets.
10. Recompute frozen parent/tree/ref, whole-row sorted SHA-256 manifest, all
    overlay blobs and FIX scope. Probe exclusively through inspected snapshot
    runner, floor then exact 3.14, with frozen overlay and no broad run.

Evidence strategy: independently audit metadata, read actual raw receipts,
then add targeted missing-path probes against frozen r002. Finite probes are
not exhaustive coverage or operating authority.
