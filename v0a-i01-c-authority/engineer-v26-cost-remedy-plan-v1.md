# v26 measured cost diagnosis and bounded remedy proposal

Author: codex/authority_cost_audit, engineering author/inspector.
This is a source-and-receipt analysis, not a cold review or release verdict.
No source change, additional probe, or payload is authorized by this note.

## Evidence and fixed boundary

- Candidate: engineer-generator-v26-storage.py, SHA256
  1f908957ee43d5841f8da09e306bd52dc5efeca9609a5d522e76df22b4dcd951.
- Root complete verification: coordinator-v26-depth-budget-verification-v1.json,
  SHA256 2e729e903ed0f0c869e88aa595d62bc0da5a2f3a47d29962f901a4865a87bf30.
  Root rehashed5298 snapshot paths and reconciled all three raw five-record streams.
- Original tests SHA256 c46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf.
- Complete helper1050 receipt: tests-checks/depth-budget-v26-cost01-helper1050-311-receipt.json,
  SHA256 39c226dd9a619edc22da425d846a4e07319eb24bb42064f5e323392fb352015f.
- Complete helper65 receipt: tests-checks/depth-budget-v26-cost01-helper65-311-receipt.json,
  SHA256 9544ba20d5eb289a10032166a764e302a02d2eb1f20229e7953d1c04e4562cbe.
- Complete generator70 receipt: tests-checks/depth-budget-v26-cost01-generator70-311-receipt.json,
  SHA256 14351189ec337a045a8e812174bad3f018901804d4f52c72b1929bbdc950f366.

I independently rehashed these three receipts and their six raw stdout/stderr
logs, read final failing-epoch summaries and corresponding source. I did not
repeat root's5298-path audit. All three diagnostics completed intact on actual
3.11.15; each analyzed candidate stopped at262145 under unchanged262144 cap.

component_units/phase_units are aliases of one disjoint partition. Publication
preparation deltas are inclusive cross-cuts; do not add them to components.
The totals below use final completion after unwind, including failed preparation.
These are charged-work measurements, not CPU/runtime or projected-speed ratios.

## Two mechanisms, three concrete paths

| Case | Observed path and costs |
| --- | --- |
| helper1050, epoch1 | Disabled definition-time pass while installing helper_628; no active helper/deferred execution. Publication preparation199347 (76.0%); radix_freeze144283 (55.0% of total). One3-name bulk constructor only; no full/version joins.631 changed commits,1265 preparation/fork attempts; dirty tails have one entry. Final failed preparation costs84. |
| helper65, epoch7 | Enabled helper execution, constructing the helper_50 resolver with active helper count51.54 bulk constructor attempts/53 complete; growing source/parent pairs5..55 agree in cardinality.51 dirty publications have base0/tails5..55. Preparation52435; lookup60644; bulk-constructor preparation32929; radix_bulk17901; ordering37480. |
| generator70, epoch6 | Disabled unittest receiver prepass creating GeneratorExp line42, before generator consumption.36 full merges each take(73,73) input cardinalities and output73. Zero version joins. Preparation9806; lookup80486; full-join bulk preparation40248; radix_bulk27454 across its initial constructor and merges; ordering19537. |

The first case is repeated small immutable publication. The other two repeatedly
reconstruct environments: helper entry preparation and disabled full joins.
Equal cardinalities do not establish identical keys, entries, order or authority.
The data does not justify another storage representation or a universal shortcut.

## A. Bounded radix freeze correction

Source14337-14365 rebuilds each edited branch by visiting all16 slots, redoing
base bitmap/index/reference lookups and pending-count reads for unchanged children,
then copying child references into a list and again into a tuple. helper1050 has
15844 freeze-slot visits and14559 pending-count reads; this is actual performed
work, not an observer artifact.

Proposed experiment within the existing representation: for an existing immutable
base branch, stage one packed-child copy, process only changed slots, and derive
pending_count from base.pending_count plus changed-child deltas. Freeze changed
descendants only. Preserve ascending slot order, bitmap, deletions and insertions.
New branches may keep the existing full construction path.

Charge every actual base/reference copy, changed-slot visit/rank operation,
insert/delete shift, pending read, allocation and final tuple copy. Never mutate
published children or publish partial work. Failure/retry ownership stays intact.
No fanout/leaf threshold change, accounting discount, new cache, or new backend.
This specifically targets measured unnecessary repeated traversal; it does not
promise enough remaining budget or better cost for every dense-change shape.

## B. Preserve a proved unchanged helper-entry projection

Source15239 first constructs a plain name dict;15333 updates it from entry_values;
15395 wraps it in _ExecutionState with that same parent. The prepared dict destroys
the exact-parent identity shortcut at14957 even when preparation changes no name.
The failing constructor probes come from _apply_helper_call_effects19428.

Propose a narrowly guarded constructor preparation path. Exact ExecutionState
entry plus exact empty seed mappings alone are insufficient: prove ALL name-
producing preparation inactive. This includes aliases, module assignments, local
functions, sensitive helper names, helper seeds, lexical locals/parameters,
nonlocals and global fallback writes. Preserve initialization of all other resolver
fields, registry/exception metadata, and existing parent-derived authority mode.
For that proved identity case, retain entry_values as the final name input and
reach the existing _ExecutionState parent fork. Skip only the now-absent raw name
dict copy/update/rebuild; never update or return the caller's mutable wrapper.

Any setup write/evaluation, uncertain/custom Mapping, local masking or entry-mode
uncertainty takes the exact old preparation path. Charge guard work and all actual
remaining forks. This avoids generic transfer omission and does not infer capture
proof from equal projected values. The source/parent counts identify the target
but do not alone prove every observed constructor qualifies.

The preceding _registered_helper_environment18886-18920 also deliberately orders
aliases/seeds/module evaluation and filtered current names. Do not replace that
routine with a caller fork merely because names look equal: its transfer/cell
writes and module-versus-caller locality are real obligations. That is a separate
proof if later needed, not included in this first constructor shortcut.

## C. Disabled joins: identity proof first, contextual proof only explicitly

_source _merge_states22254-22347 forces disabled state through full reconstruction.
Try the narrowest admissible condition first: exact ExecutionState inputs, all
authority.enabled False, same budget/meter, and identical immutable name roots.
Such root identity proves exact entries/keys/pending metadata; counts do not.
Even then preserve the exact legacy set-union order with an order recipe, not
first-parent order. Retain pending flags and normal snapshot/fork ownership.

No recorded counter establishes shared-root frequency. This fast path may have
zero useful hits. Utility must be reported, not presumed from36 equal-size joins.
If roots differ, keep the old path until a separately approved context-local proof
exists. _transfer_authority14042-14043 returns immediately when authority is
disabled, before its consume. That can justify omitting its no-op effect ONLY in
a currently proved all-disabled join. It cannot justify setting entry.no_work,
promoting a leaf certificate, or skipping future enabled transfer after adoption.

A broader changed-name join would need exact immutable common ancestry/change
enumeration, ordinary flow merge for every changed alternative, unchanged-entry
reuse only under that local disabled proof, pending debt preserved, and exact
legacy order. Plain Mapping, enabled/mixed-mode, foreign meter, or missing ancestry
must retain the old full path. All discovery/order/copies remain charged.
Before any such change, explicitly amend/reconcile the current blanket
every-transfer/no-work-entry rule for this operation-local no-op proof; do not
silently introduce an exception or reuse the pure join callback contract unchanged.

## Decision, sequence and stop rules

Prefer these localized seams over another storage backend. First accept/reject
their proofs and scope independently. A changes only freeze mechanics; B changes
only proved-empty resolver name preparation; C needs its explicit transfer-law
reconciliation and evidence of utility. Do not combine semantic v25 work into them.
No source implementation is requested or performed by this note.

Any implementation should be retained separately, inspected before execution,
then checked against the unchanged three RED cases and original design53.
A also preserves the existing independent storage order/collision/retention/
failure-atomicity requirements; primitive success never substitutes for actual
analyzer fitness. Keep all five caps and source expectations unchanged.

Stop if an identity shortcut cannot prove exact order/ownership/debt, if measured
hits are absent, or if a proposed fix merely moves cost into uncharged preparation.
Do not consume the existing mutable successor, remove historical states, widen
no_work, or claim readiness until actual focused and ordinary generation evidence
supports it. The current v26 candidate remains unaccepted.

