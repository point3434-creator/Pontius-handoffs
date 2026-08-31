Static census attribution for the supplied provenance-v4 census01, compared with r009/provenance-v3 census311-03. This is an independent, non-cold source-and-artifact comparison, not a candidate acceptance review or runtime verdict.

The bounded comparison found no lost or added capability row and no newly unblocked item. All 141 expanded capability rows are exactly equal, and the specification and analyzed-site digests are unchanged. The blocker increase is a conservative proof-cost increase: 349 added row instances minus one replaced refusal gives the reported net increase of 348. A blocker whose reason says identity “was mutated” records analyzer invalidation; it does not establish runtime mutation.

The authority for every position below is the census01 source snapshot, before the root's later census-literal refresh. Root owns the separate final-census stability linkage. No claim in this report silently substitutes later source bytes.

| Bound input | SHA-256 |
| --- | --- |
| D:/Pontius-handoffs/v0a-i01-ab/slice-c-provenance-v3-census-311-03.json | 42013dfbe68bf17a04dc48080f40191b3b89bde617bda59177c31a15edcef9a4 |
| D:/Pontius-handoffs/v0a-i01-ab/slice-c-provenance-v4-census-311-01.json | 279003a00735795c63a1e3f0e292499669ccd320abb2c7bef5f5f4dced0f3a82 |
| r009 tools/generate_test_inventory.py | 9031a42ded45bbd8af3afb3044c683be40ed45121c375b3de04e5bdf05b8c924 |
| census01 tools/generate_test_inventory.py | 29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692 |
| r009 tests/test_inventory_and_profiles.py | a3b580a72851ca2d4dd359259c1897326a3c8048119fc6169a65a2fc50c8b102 |
| census01 tests/test_inventory_and_profiles.py | 7367404a7b8bd6a2c15049a5a9a88b9863efa2c7cd6bca5c0fdfef008553c8a8 |

The old snapshot is D:/pontius-snapshots/abc-provenance-v3-focused02-f4be93d4192b4c1fadfe5b53aafc515c/harness. The census01 snapshot is D:/pontius-snapshots/abc-provenance-v4-census01-1a1bba2793f5489e9c98a94027a13f8b/harness. The generator, secure-filesystem sibling, inventory, profiles, and eight source files used for position attribution were freshly hashed in both snapshots against the respective census pins. The comparison JSON records all 24 verified hashes.

[The complete mechanical comparison](D:/Pontius-handoffs/v0a-i01-ab/abc-provenance-v4-final-census-attribution-comparison.json) has SHA-256 b41a3efb73a74e19a987d780b07cf208a6864e5e435436ee934e381ab6dc6f10. It preserves duplicate blocker instances and lists every raw removal, relocation, semantic removal, semantic addition, and newly blocked item.

| Invariant or change | r009 | census01 | Result |
| --- | ---: | ---: | --- |
| Parsed stable IDs | 2860 | 2873 | 13 added methods |
| Test files | 405 | 405 | unchanged |
| Expanded capability rows | 141 | 141 | complete rows exactly equal |
| Deny-all rows | 2801 | 2814 | exactly the 13 new stable IDs added; none removed |
| Blocker instances | 895 | 1243 | +348 |
| Unique blocker tuples | 693 | 1019 | +326 |
| Repeated instances beyond unique tuples | 202 | 224 | +22; not 22 distinct sites |
| Blocked items | 344 | 447 | 103 added; none removed |
| String decoys | 599 | 601 | +2 in task2_synthetic only |

The unchanged specification digest is d303a26e373f0b173a4283dcede5735fdae6b849fdb0cb0ffcddec9017e8012a. The unchanged analyzed-site digest is 3170f99166d98d3879109a0d02ea68a096bf096ae79e1d0ab871d6ba764f6020. Counts remain 45 direct subprocess sites, 5 helper subprocess sites, 27 cross-file helper edges, and 30 CuPy call nodes. These are artifact comparisons, not executions of those sites.

Only tests/test_inventory_and_profiles.py differs in the 405-file source corpus. Removing census01 lines 21137–21577, inclusive, restores the old complete source text exactly. The insertion is 441 lines and 13 test methods. Consequently every old position in that file at line 21137 or later maps to old line +441. This is a byte-pinned source-text equality check, not an assumption based only on a diff hunk.

Only one of the 13 new methods contributes a new corpus blocker: test_callable_authority_annotations_refuse_without_inventing_execution at line 21443, a mixed-protected-receiver refusal on the lookup-and-call through namespace['ReviewTests']. The remaining 348 added blocker instances concern pre-existing item IDs. Of the 103 newly blocked items, one is this new method and 102 are pre-existing items.

All apparent removals were checked as a multiset keyed by (item_id, relative_path, line, reason). There are 32 raw removed instances. Thirty-one are unchanged refusals relocated by +441 in tests/test_inventory_and_profiles.py. The table is exhaustive; a repeated line is a repeated row instance. Class and method names below complete the prefix tests/test_inventory_and_profiles.py::.

| Item | Reason | Old lines | Census01 lines | Instances |
| --- | --- | --- | --- | ---: |
| DesignReviewTests::test_helper_effective_inputs_cover_registered_defaults_and_class_receivers | mixed protected receiver | 21337, 21339 | 21778, 21780 | 2 |
| DesignReviewTests::test_descriptor_defaults_preserve_real_python_argument_binding | mixed protected receiver | 21416 | 21857 | 1 |
| DesignReviewTests::test_receiver_descriptor_not_parameter_spelling_controls_binding | mixed protected receiver | 21469, 21478 | 21910, 21919 | 2 |
| DesignReviewTests::test_unknown_receiver_context_blocks_and_lexical_capture_is_preserved | mixed protected receiver | 21526, 21529 | 21967, 21970 | 2 |
| DesignReviewTests::test_invalid_static_helper_arguments_remain_blocked | mixed protected receiver | 21568 | 22009 | 1 |
| DesignReviewTests::test_helper_registry_and_argument_binding_fail_closed | mixed protected receiver | 21679, 21775 | 22120, 22216 | 2 |
| AtomicAndGitBoundaryTests::test_lock_set_precedes_all_destination_and_lifetime_observation | namespace escape | 24489, 24541 | 24930, 24982 | 2 |
| AtomicAndGitBoundaryTests::test_lock_set_precedes_all_destination_and_lifetime_observation | namespace identity | 24514, 24532, 24541, 24541, 24669, 24670, 24673, 24707, 24712, 24760, 24765, 24821 | 24955, 24973, 24982, 24982, 25110, 25111, 25114, 25148, 25153, 25201, 25206, 25262 | 12 |
| AtomicAndGitBoundaryTests::test_pair_marks_one_commit_and_never_rolls_back_after_cleanup_failure | namespace store | 25394, 25395 | 25835, 25836 | 2 |
| CheckedInInventoryTests::test_baseline_counts_digests_and_materialized_partition_are_exact | mixed protected receiver | 30383 | 30824 | 1 |
| CheckedInInventoryTests::test_historical_payload_subgroups_have_independently_locked_ids | mixed protected receiver | 30701 | 31142 | 1 |
| CheckedInInventoryTests::test_exact_declared_unconditional_skips_match_outer_literal_and_digest | mixed protected receiver | 30771 | 31212 | 1 |
| CheckedInProfileTests::test_exact_interpreter_slots_profiles_and_budgets_are_declared | mixed protected receiver | 30921 | 31362 | 1 |
| CheckedInProfileTests::test_twelve_historical_cases_bind_exact_commits_trees_and_v7_overlays | mixed protected receiver | 30978 | 31419 | 1 |

The sole semantic removal is fixture:tests/test_fresh_action_width_transfer_confirmation.py::FreshActionWidthTransferConfirmationTests at line 145, formerly “helper descriptor member identity is unresolved.” Census01 reports “helper namespace identity was mutated” at that same item, path, and line. The source file is unchanged (SHA-256 6b48a6d872466a98a2616619776f35933fc6998db2c10c2c30387ded6f7f9d71).

The fixture defines confirmed_owner at line 109; its body refers to cls, including cls.receipt_prefix_counts at line 110. That callback is supplied as arm_owner at line 128 in the external call beginning at line 123. Census01 adds an escape refusal at 123, a deferred-consumption refusal at tuple(...) line 135, and the namespace-identity refusal on cls._write_direct_terminal at 145. In the generator, _helper_member_value checks invalid_helper_owners at lines 17935–17937 before its descriptor-stability check at 17944–17945. Thus the removed descriptor diagnostic is superseded by earlier proof invalidation, not by authorization of the call or an unblocked fixture.

| Added blocker reason | Instances | Unique tuples | Attribution |
| --- | ---: | ---: | --- |
| helper namespace escape is dynamically unresolved | 215 | 205 | Newly retained callable/owner authority reaches an unresolved call boundary |
| helper namespace identity was mutated | 126 | 115 | Downstream owner/member proof invalidation |
| helper namespace effects are dynamically unresolved | 5 | 4 | Constructor/helper effect projection cannot discharge the proof |
| helper callable identity was mutated | 1 | 1 | Downstream callable proof invalidation |
| deferred generator consumption is dynamically unresolved | 1 | 1 | The transfer-confirmation fixture's later tuple consumption |
| mixed protected receiver is dynamically unresolved | 1 | 1 | New annotation-test corpus call at line 21443 |
| Total added | 349 | 327 | Minus one replaced descriptor instance gives +348 |

This supports a bounded cost partition: 220 escape/effect refusal instances plus one new synthetic mixed-receiver instance are primary reported proof boundaries; 127 identity refusal instances are propagated proof invalidations; one deferred-consumption instance is the fixture's additional downstream refusal. All 127 new identity instances have an added escape row for the same item and source path at an earlier or equal line. That co-occurrence is mechanically established. It is not a dynamic causal trace across every branch. The invalidation mechanism is directly visible in _apply_helper_call_effects at lines 17780–17783 and 17819–17820, _invalidate_helper_identities at 17427–17441, _helper_member_value at 17935–17937, and callable refusal selection at 15790–15793.

Distinct source mechanisms explain the new proof boundaries without requiring a runtime-mutation claim:

- Captured class authority passed to an external function: the transfer-confirmation fixture at lines 109–128 passes confirmed_owner, which retains cls. Subsequent uses of cls inherit the analyzer's invalidated proof.
- Captured receiver authority in injected callbacks: tests/test_legal_river_quotient_cuda_compensated_work_preflight.py lines 731–746 defines callbacks that use self.assertEqual and passes them to runner.execute_owner_to_path. The escape at 741 is followed by namespace-identity refusals on later assertions at 748–760 and a callable-identity refusal on _synthetic_events() at 765. These later assertion positions are propagation costs, not additional source assignments.
- Mock callback forwarding: tests/test_evidence_manifest_generation.py lines 1014–1035 captures real_create and passes swap_then_create through mock.patch.object(..., side_effect=...). The new refusal at 1031 is an unresolved forwarding boundary. The callback body was read, not invoked.
- Callback effects without a retained test receiver: tests/test_native_simplex_audit_runner.py lines 283–305 supplies fake_linprog, which accesses captured materialized state and appends to calls. The refusal is at invoke_highs_backend(..., linprog_function=fake_linprog), line 302. The new fallback _unproved_callable_effects at generator lines 17293–17344 explains how unresolved callable effects can survive even when direct retained-owner discovery is empty. This does not imply that fake_linprog mutates a helper namespace at runtime.
- Registered observation callbacks: tests/test_v0a_replay.py lines 1648–1659 defines observe using ReplayHost._events.__code__, HandRuntime.dispatch.__code__, and captured clock state, then supplies it to sys.setprofile. The refusal is at the registration call, not proof that registration itself ran a sensitive body.
- Implicit constructor/helper effects: all five new namespace-effect rows occur at _ConfigurationTree(...) calls in tests/test_test_orchestration_configuration.py:3061, 3086, 3162, and 3260 (two instances). The constructor at 580–599 prepares inventory and calls _refresh_inventory_metadata. Generator lines 17372–17425 project implicit-method effects and report unresolved effects. This source attribution identifies the projection boundary; the artifact alone does not expose which internal proof condition failed for each invocation.

The new callable representation retains defaults, free bindings, receiver and return/container obligations. The traversal at generator lines 17257–17297 follows these values and explicitly describes itself as retaining authority without executing the callback. This is the mechanism relevant to the broader refusal coverage. Static effect projection is analyzer work over syntax, not execution of the inspected Python bodies.

Native list storage was checked separately because storing a callback must not itself be treated as invoking it. tests/test_native_simplex_audit_reanalysis.py is byte-identical in both snapshots (SHA-256 d95fba06549273fcb43fabf4a25370f6bdd7ab752592bfccc46f77ef6df17f25). Its complete 200-instance blocker multiset is exactly equal across the two censuses. There are no blockers at list initialization line 347 or cases.append(...) lines 354, 361, 370, and 377. The later explicit callback invocation is mutate(campaign) at line 382; this report does not claim that later invocation is generally authorized merely because storage is inert.

The generator's _retain_native_list_call at lines 17721–17748 applies only to proved mutable native lists with collection identity and supported append/extend/insert argument shapes. It retains authority through _retain_native_collection_authority, then the caller returns at 17766–17768 before the generic unresolved-call escape path. Retention updates helper_obligations on collection aliases at 17715–17719 and does not invalidate owners or emit a blocker. The legacy collection path still handles shape and exception behavior. These static checks and the unchanged 200-row census support the absence of a new store-alone refusal in the named real-file example; they are not a universal heap-model verification.

The two additional string decoys are in the new annotation test: the subprocess source-template string beginning at tests/test_inventory_and_profiles.py:21398 and the literal 'subprocess.run(' in assertNotIn at line 21436. The generator's decoy tokens at lines 26010–26015 and task2 source classification at 26105–26106 account for their partition. task2_synthetic increases from 542 to 544; design_production=17, historical_production=6, and prior_stabilization_synthetic=34 remain fixed. The decoy digest changes from 2136e9e38c556de45235202b2b38f729f35b7ef5ff3678932575c4c1e35689db to 69c33850d37e91651ca1e8b836d2c3262ab4e6487634d16e8873e6df2c8c0424. That digest also includes line positions, so it must not be described as hashing only two new strings.

Evidence was produced with read-only PowerShell JSON/multiset processing, literal file reads, file hashing, and git diff --no-index over the two named source files. The exact +441 source restoration was independently checked with source-text equality. No census helper, generator, test, inspected callback, sensitive body, GPU path, experiment owner, or publication path was executed. Only the authorized new Markdown and comparison JSON were created, with LF endings and create-new semantics; no source, snapshot, ledger, capability, or publication artifact was changed.

The result is limited to the supplied census01 artifacts and source pins. Unchanged capability rows, preserved denial rows, no newly unblocked items, exact retention of the old test source outside the insertion, and the superseded descriptor refusal provide no observed capability-loss or guard-weakening finding for this corpus. They do not prove universal analyzer soundness, exhaustively classify benign versus harmful callbacks, establish runtime behavior, measure execution cost, replace focused tests, or authorize a candidate. Root's subsequent census-literal refresh and final-census stability evidence remain separate.
