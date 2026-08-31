# v17 prerepair: preserve observations with bounded layered storage

Date: 2026-08-31. Engineering note before source modification, not a cold review,
release, acceptance claim or authorization to commit. Exact predecessor generator:
3b9046fc9928bc17378ab57ab4d920bd57ae99994233bd503528670b362f8ab4.
Scope remains the separate C authority transfer replacement in stage0-design.md.

The measured gen03 RED is tests-checks/red-budget-gen03-v4-311-receipt.json,
SHA-256 622cf3853869e0dadad1fab79f24113fd8950a680fde996f5594a0775f0acc9e.
Its unchanged budget raises at 262145 against the existing 262144 work-unit cap.
The diagnosed item is EvidenceManifestTests.test_each_schema_rejects_its_applicable_
malformed_scalar_path_count_and_digest_fields in tests/test_evidence_manifests.py,
definition line 218. Observed-table copies alone consume 184860 units (70.52%).
The large initial cases tuple retains sibling observations through one outer
expression; nested call/exception snapshots fork that table before more writes.
The final throwing lookup is not the dominant accumulated cost.

Adopt a specialized observed-only map with a short tuple of dictionary layers.
A fork shares all layers and marks each branch's current last layer as published.
A subsequent write either appends a new exclusively owned delta layer or, at
eight layers, compacts all entries oldest-to-newest into a fresh owned dictionary.
Reads search newest-to-oldest. Old snapshots keep their old tuple and dictionaries;
no published dictionary is mutated. Clear replaces only the clearing branch's
layers. The newest entry wins, including when several branches replace one key.

Eight is a representation compaction threshold, never an admission limit or
refusal condition. It bounds lookup depth without increasing any analysis cap.
All actual dictionary/layer allocation, tuple copying, fork, clear, lookup-layer
attempts, writes, compaction traversal and visited entries remain budgeted. Do
not suppress a budget exception. A failed compaction cannot publish a partial
replacement. The value type is the existing immutable _FlowValue.

API discovery searched every observed reference in the exact predecessor:
initialization13928; fork13941/18397; clear13966/18472; get17733/17736/18166/
18246/18482/18483/18494; setitem18508. No iteration, deletion, membership,
length, generic mapping mutation or direct backing-table access is required.
Keep get's caller-supplied default behavior. Retain v16's evaluation-depth clear,
all historical call snapshots, results, live object/cell stores and binding maps.
No cell merge optimization, lazy capture, free-name cache or other microfix is
part of this edit. Production diff is one added specialized class and the single
observed initializer replacement; every existing function remains otherwise exact.

Why not subtree pruning now: receiver consumers read a grandchild such as
node.func.value after argument evaluation. Discarding a completed child or
retaining only immediate operands could remove an observation still needed by
its parent. Proving all parent/grandchild lifetime roots is a wider semantic
change. Layered storage preserves the complete logical map and changes only its
copy cost; dormant/retained authority and optional precision do not change.

Risks and falsifiers: a forked branch changing any prior snapshot, a lookup
returning an older value after an override/compaction, clear affecting a sibling,
or an unmetered actual copy falsifies the representation invariant. The existing
historical-callee and retained-receiver public cases must stay unchanged. Root
will first run ordinary isolated --write with the release interpreter, then the
required focused checks on 3.11.15 before 3.14.6. No payload runs are assigned to
this engineer. Ordinary generation, canonical census, fresh cold reviews and
broad gates remain pending; no GREEN is asserted here.
