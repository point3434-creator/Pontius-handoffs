# R1 Task5 v2 correction handoff

Engineering authoring checkpoint, not a cold verdict or runtime GREEN. Round scope is the bounded correction of the frozen Task5 v1 final-review findings. Root authorized this source change after the source-only cost/semantic reviews and approved the independently derived entry-name table. No candidate import, analyzer/Model/test payload, commit, or original-policy execution occurred in this lane.

## Exact retained identity

- Source: rewrite-r1-task5-source-v2.py, SHA256 c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f; 1166485 bytes. NEW W tools/generate_test_inventory.py matches and is held unchanged.
- Root freeze: H b1d15de062ac45c351f0254b358ee1e5fc35bdee; manifest beb50fab0fe159249de1397529b78a71e2b176b8e3643ea64ccb37dbf1a1c15a.
- Predecessor remains rewrite-r1-task5-source-v1.py, SHA256 810cbb934e20a13c9c4794e3574bcb6a248ddc8b4a84a56045f6370c1a066cea; H d224ea401898e462b327c43f129822dd52168782 / manifest afc26d19bf76e44694b4e88254946aa2607bf4ece45965098a67ff946e148401.
- Exact 11-pair operations: rewrite-r1-task5-edits-v2.json, SHA256 d1be8b35c664f7cda35cb50e3053d605999c8a6c030ef362796ff9212def496e.
- v1-to-v2 diff: rewrite-r1-task5-from-v1-v2.diff, SHA256 b87a1fd109f9d8d0f0fce6625d7a161b949af91d781093a1514adaf6673f5162.
- Full r010 diff: rewrite-r1-task5-from-r010-v2.diff, SHA256 00ef99dfa3722242a7165e18c642b1eb31b13c7d7e8698f7eb913f38e33361c1.
- Authoring checker: rewrite-r1-task5-static-check-v2.py, SHA256 9cb540f0622fe1eac05cba4c94cf03d1603a3c29451212d56af16089a8260403.
- Authoring proof: rewrite-r1-task5-static-v2.json, SHA256 dfd3a6b93a1bcde9afa818cef3c19aa35287d742d416fc661f2b872cd6c8de19.
- Root independent static report: coordinator-rewrite-r1-task5-static-v2.json, SHA256 652488045b3cfac3901c4583b93f29da86e9ce0414926aea89c647ef324d4dcc (identity/result reported by root, separate from the author's check).

Controlling plan remains 18f8124432880016d6dd0690ed4d3b582b8e202c5bdda21ae48a65efa0ae521d. Cost review is rewrite-r1-task5-cost-review-v1.md, SHA256 01b9eba1f059ac272e4c0a991b2f7bee41b76685b6b17b58140a9c62eca1ed59. Semantic review is rewrite-r1-task5-semantic-review-v1.md, SHA256 93f14ff8e628377ad121602033d78b861866b2e7283fbc8eb73f3a7c6457934a. Earlier source, reports and edits remain immutable.

## Category correction and operation ledger

| Reviewed category | Implemented v2 boundary | Actual charge |
|---|---|---|
| Module and selected-item export copies | All three module exports and all four item exports call _c_extend_review_rows using their existing operation context | 2N: N copied-element visits plus N installed destination references. No new list or budget owner is invented; empty copies charge zero. |
| Owned preflight refusal construction | All four prior preflight refusal paths and the new entry-guard refusal use _c_preflight_blocker | 11: dictionary allocation1 + eight key/value references + append operation1 + appended reference1. No fictitious four-element input traversal is charged for a literal dictionary. |
| Terminal adapter result transport | Both success and policy-refusal return paths in _c_emit_sink pay for their pair | 3: tuple allocation plus two references. The impossible children-error path creates no returned pair and gets no pair charge. Original _process_definition internals are unchanged. |
| Unsupported manufactured-entry protocols | _c_entry_namespace_supported examines only current explicit members of the selected unittest class before receiver manufacture | Per reached name: visit1 + prefix check1; suffix check1 only after matching prefix; reserved-set probe1 only if the dunder check did not already refuse. Early refusal does not charge unreached names/probes. |
| Invented subprocess return fact | Successful _c_sink retains its detached observation but returns _CAtom unknown with an explicit reason | Existing _c_atom pays for the new atom. _c_out receives that atom instead of allocating a default literal-None atom. No subprocess result-object model is added. |

The output helper centralizes all seven owned export copies. The refusal helper centralizes all five owned preflight dictionary/appends. The former four-name fixture scan is removed; its names are in the exact frozen generic entry set. The guards do not charge a second scan of names or hook bodies. No old policy parsing/normalization work was newly remetered. No new budget epoch, reset, refund, cap, table ownership or state-write algorithm changed.

The subprocess result remains harmless when discarded or stored without a fact-dependent operation. Assignment, returns, defaults and captures retain the same unknown value. Existing identity comparison with None remains unknown rather than inventing False/True; reached truth use refuses. Unsupported member, subscript or call use likewise follows the existing refusal boundaries. A known containing tuple/list can still have proved length/truth without claiming anything about its unknown element. The correction does not equate retention with execution.

## Frozen entry policy and provenance

The implementation embeds all111 sorted reserved_names from rewrite-r1-unittest-entry-reserved-names-v1.json, SHA256 55ed71468da3c480e4805672b2b254e1bff5d6d0cf99a2c36ed0fbcfec202ceb, plus an independent any-dunder predicate. Its source note SHA256 is cc424e9f043ce7a195d0b37491fe99c6d61788a45d80e1dd0ae8a77659b348f0. Root rederived and approved the table in coordinator-rewrite-r1-entry-table-verification-v1.json, SHA256 ea385d052fb8f6b163d099d9cce5eb1a7409bc1bbc0a2da7d72aec4b0582d7d7.

The table combines102 class-scope TestCase names from configured3.11.15/3.14.6 source and nine receiver/class lifecycle fields. Seven entries are dunders;104 are nondunders. The fixed frozenset is immutable module metadata; no per-analysis table construction, dynamic unittest import, runtime introspection or source-dependent helper-name heuristic occurs. The JSON retains each source/config hash and each included name's AST provenance. The author's final checker asserts exact equality with the111-name list.

The guard applies only to a selected manufactured unittest entry, after canonical namespace/function admission and before creating the receiver. An explicit same-named override is conservatively refused without executing its body. Inherited unmodified framework names do not appear as explicit user overrides. Ordinary user helpers/lexical locals are not banned. Dormant local class construction is unchanged. Existing independent constructor/header/decorator/signature/descriptor refusals remain; this guard does not claim general framework or protocol execution.

## Static verification and limits

Actual3.11.15 -I -S -B -P ran only the retained AST/hash checker and exited0. It checked exact application of the11 issued edit pairs; source/W equality; LF/noBOM; all16 other protected paths; exact original-byte restoration after removing the canonical core and restoring the already-approved matcher/name changes; exact normalized original AST; unchanged14 binder guards/six wrappers; exact111-name table; seven charged export calls; five charged preflight refusal calls; and one entry-guard call. Only three preexisting functions change from v1: _c_sink, _c_emit_sink and the new _process_review_rows. New definitions are the frozen constant and three small helpers.

The total against r010 is2191 additions +7 deletions =2198 changed lines;302 remain under the initial2500-line boundary. The core span is2150 lines. All v2 replacement text fits100 columns. The original binder and public receipt/native writer/caps remain exact under the documented normalization. The other16-path proof names only its explicit setup paths. Main docs/workflow.md changed concurrently outside this lane; it and CLAUDE.md were not edited here, and no stale raw workflow preservation claim is made.

The v1 terminal boundary remains: sole detached observation producer, explicit -c exclusion before observation, captured environment and empty unvisited visitor for pure terminal policy, no live old resolver/preclassifier/review-body fallback. Scope/state/call/trace machinery did not change in v2.

The internal site labels are NOT independent all-site reachability proof. In particular, v1's module-observation exclusion can label reached module sites 'proved_unreachable'; that reporting code is unchanged and its labels are not public. Root accepted narrowing this evidentiary claim in this round. The actual nonsynthetic _c_call source-site membership check remains in force; it is not a substitute for whole public behavioral verification.

The fixed GateA six analyses/eight Model projections and all expected labels are unchanged. Opaque self.choice truth may still refuse before the hidden pair's branch/join paths; such refusal must not be reported as precise joined-cell execution. The original GateB open-choice premise remains held; no special scalar assumption was added. Unsupported runtime syntax, later migration/private-API obligations and cost fitness remain as in the accepted R1 scope.

These are source corrections with static authoring evidence. Independent v2 engineering rereviews and root-owned floor-first GateA must still determine semantic/accounting closure and runtime results. No GREEN, broad no-regression, headroom or release-readiness claim is made. Hold source c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f unchanged through that review and any authorized floor/dev runs.
