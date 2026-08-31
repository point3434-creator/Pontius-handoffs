# R3 private-interface recommendation v1

Engineering planning by codex/r010_cold_a. This records the completed bounded review; it is not R3 GO, a test-migration authorization, an implementation approval or a cold verdict. No further case population was inspected or created.

Verified input pair:
- H commit a6510e250484e21e53ab85fac6027a4c309cda08.
- rewrite-r1-task3-v1-manifest.sha256: 3599296998a7d85c5abf9a59ecfe917a9ca3997a7891abf45b13ac8d9fb68a96.
- rewrite-private-api-compatibility-inventory-v1.md: da599d0acad2ad29b7a60470fa2a41f772b248c2c703daff829b0be08affa22f.
- rewrite-design-v1.md: 701552c177840e4c5c0dd9c5985776256af5b31e7e997067dd662638a67c3ca8.

The three files above were independently read as Git blobs at that commit and compared to local raw bytes and expected hashes. Known test ranges were reread from original Git blob a62562fbba5969e33cc04786d91064afad30e580, SHA-256 c46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf. Line anchors below refer to that original test file.

Comparison boundary: held R1 source c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f; approved R2 plan d5491bc204b07ec0e1f861b7cfe03facab9b8c9907a38726f64d96c096fe0d4f and addendum 1a1a6bc7f8ef4c56a72735670ff0bb65e883f3aa559abec7b4fec01af6991998. This comparison identifies declared support gaps, not runtime failures.

Recommendation: prospectively authorize explicit migration of the stateful private test interfaces for R3, while permitting small canonical-backed, read-only observation adapters. Do not promise byte-identical private tests and removal of every old interface simultaneously.

| Known original root | Existing obligations to preserve | Replaceable representation |
| --- | --- | --- |
| test_round4_source_order_and_branch_bounds_red_contracts_are_independent, line 19419 | Exact callable classification; negative membership after overwrite/throw; original source-site attribution; typed exception successors; nonexecuted deferred writes; protocol descriptor evidence; call bounds | Resolver/preclassifier spellings, values/normal/raises interface shapes, _flow_qname encoding and sentinel strings |
| test_round4_analysis_budget_red_contracts_are_independent, line 20406 | All five caps, exact required error categories/messages, cardinality checks, complete discovery and shared budget ownership without reset/refund | A superseded second analysis pass and its precise charge placement only under separately justified fixture replacement |
| test_helper_registry_and_argument_binding_fail_closed, line 22061 | Ambiguous shorthand rejection, correct tools.test_child namespace, unchanged public binder behavior | Registry descriptor implementation and private spelling; definition-only key views can remain |

The stateful tests feed dict(resolver.values) back into execution and advance returned successors. A facade is safe only if execution remains entirely canonical and never reconstructs live state from reporting values. Preserving that mapping protocol would add a substantive compatibility contract contrary to R3's explicit scope/state direction. Migrating those invocations to canonical step/observation interfaces is clearer. Preserve the original source fixtures, harmless oracles and exact semantic assertions; replacing them with some public refusal would lose required evidence.

A small adapter may retain ID-keyed call observations, qualified-name strings, descriptor summaries and registry membership without adding another engine. Leaving an old preclassifier, bounds evaluator or resolver behind those names, or independently computing their answers, would retain a second semantic authority. Neither facade nor migration permits such a rescue path. Preserve the 119 behavioral method identities/count where practicable and attribute only approved interface/source-census changes.

The seeded fixture at lines 20569–20596 needs a specific disposition. It discovers 32 calls with the supplied budget and then requires the second operation to exceed 262144. If both real operations remain, preserve the fixture exactly. If R3 eliminates the second pass, retain the original bytes/evidence and prospectively replace its architecture-specific staging assertion with a justified canonical boundary check. Do not add redundant traversal or artificial charges to reproduce the old failure location. Complete discovery, shared ownership, honest actual work and unchanged caps remain binding.

Known requirements materially beyond held R1 plus approved R2 are:
- Empty tuple generators, next/default exhaustion and source-level StopIteration; false-filter/walrus nonexecution controls.
- Existing typed routing through finally, suppression and other abrupt exits.
- Implicit comparison-protocol evidence identifying both descriptors at the original call site.
- Loop/comprehension cardinality and multiplication checks beyond R2's bounded range creation subset, plus existing child-depth behavior.

These are existing contract-completion work, not reasons to broaden R2 now. The retired 34+28+31 primitive checks do not require resurrecting their storage APIs; original production behavioral tests are a different population. Preserve all binding classifications and expectations unless a later explicit disposition separately justifies replacement.

No test, Model, analyzer, sensitive fixture, candidate or harness payload was executed. No source/test/baseline/population was changed. This note records the recommendation for a later explicit decision and authorizes no R3 work.
