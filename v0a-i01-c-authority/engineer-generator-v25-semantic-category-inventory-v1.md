# V25 semantic candidate handoff

Engineering implementation/self-inspection only; not a cold review, execution
authorization, passing-test report or release judgment.

## Pins and scope

Candidate is a create-only T artifact derived from exact v23
53a17d52196bd83a540ebf4892d3687f3efbe9633d1539fa834ea0a27f0db499.
No storage v24/v26/v28/v29 source is an input.

Root explicitly authorized T-only source authoring after reviewing:
- Plan v1: 39807c39a14e6f2009ffa69f5f09604c8354c1043a09be6c63e5982412621c2d.
- Normative v2: e2ed7f88a6c081be3ec54556e47a327ce1ea2d336e55200e788857cfec099bb8.
- V3: 1d661231a472fc689af06ea993234f27ab88a65da950d83f1811c1f941d94723.
- Origin clarification v2: 458e182d3bfc8e715e1f9f2be0762fe1237088570a98c81f1958b1f766b22e70.
- Projection companion: 96bbf47d1251b5249e7796c6f3f9482f6a2a6e2b257c26207f0b5e7e6c9ae21e.
- Inheritance clarification: 6f1aeb1b68593ac5f3c863d4137b5008700eb5cf5b5f88a72d8252a043cc7582.

Root separately authorized only operation-budget keyword additions in
_ExecutionState._write_cells and __delitem__. These two methods are NOT byte/AST
unchanged. Removing those keywords restores their exact v23 AST; their storage,
transfer, strong/weak write and deletion algorithms are unchanged.

The executing-plans, code-work and verification/review skills were applied.
Root's explicit no-payload/no-commit scope governs this handoff: no test,
Model, analyzer, candidate import, production execution or commit was performed.

## Evidence used

Root's v23 semantic verification report is
33a2257f5ec5ac31ec3f4b59342dc46e86bcab6451df1656ca7fd1931aa1d1a7.
It records the same C03 and Q05 residuals across both slots; 34/36 satisfy their
fixed labels. R8's separate root verification is
181248855d1947c775d21728ed3ae5c2bb62b7deb15604154f88b95290e89bac
(R8 section only, not the unrelated storage lane).

L8 verification is 0ff78f0573d8cae835509d987b61a7ec12574912f0b63e3d3121d918325def5b:
root reports identical complete records, all four clean controls passing and
L01/L03/L05/L07 wrong-clean on both slots. The author rehashed these retained
report files, but did not independently rerun their snapshot or payload checks.

The static proof pins all seven original44+L8 case packs (52 cases). Expectations,
harmless traces and sensitive source fixtures were not edited. There is no v25
behavioral result yet; root must inspect the issued bytes before any payload.

## Changes and boundaries

| Category | Implementation and limit |
| --- | --- |
| C03 reached factory | Cached helper effect shape gains a construction bit for FunctionDef/AsyncFunctionDef/Lambda/ClassDef in its existing metered walk. Ordinary no-work skips require no construction or retained class/deferred input. Deferred creation, invalid binding, depth and prepass gates remain. No nested body runs merely on construction. |
| R01/R03 target binding | Only ast.Name with Store context is allocated as a class comprehension local. Existing eager header and enclosing-current-cell body boundary remains. |
| R05/R07 alternatives/epoch | Flatten all direct/merged generator alternatives; same-identity state merge OR-retains class marker. Empty class generator is dormant only when its outer iterator epoch is unchanged. |
| Q05/L01-L08 class transport | Enabled normal class completion reserves an existing-store class owner, even with empty members, before binding. Named/wildcard may-roots and owner tag live on AuthorityRecord. Direct, container and captured aliases carry the same ref. No value/MRO/callable/lexical proof is granted. |
| Origin and scalar shape loss | Explicit implicit_class or helper class provenance without live tagged ownership stays unresolved. Obligation stores get typed helper-namespace refusal; scalar/non-obligation stores do not. _assign's legacy mapping projection retains an explicit alternative edge to the prior class owner, preserving current-record ownership or unresolved origin. |
| Inheritance | Read-only class_member_base edges retain base refs, not copied member snapshots. Only requested-name selection follows them. Current records dominate old values; unresolved bases export a typed obligation at reached selection. Existing proved scalar/sequence/mapping own results are not poisoned by inherited alternatives; otherwise same-name may-roots are conservative. No shadow heap/MRO precision. |
| Native shape loss | Current exact shape is checked at collection results, subscripts, element stores and native retention. Retention-only mutations invalidate current record.value and retain element roots. Extend checks the donor's current shape. Old helper identity elsewhere in the container cannot restore stale contents. |
| Native completed effect | Call-local NativeCollectionEffect distinguishes actual exact updates from mere get/pop/clear/copy admission. Admission tokens have shape_exact=False. The normal call site handles tokens before returned FlowValues; later poison preserves current exact data only for the same completed owner effect. |
| Immediate versus contained | Alternative and element carriers are distinct. Iterator consumers inspect possible immediate iterators, not generators merely contained in a list/tuple. Native copies/materialization keep element roots; extraction/next/target binding exports alternatives. Ordinary callable captures and unread class tables/base edges are not iterators. |
| Refusal propagation | Every new active consumption/store refusal uses the existing helper-namespace channel. Missing-owner/base issues remain helper_deferred_refusal obligations through selection/transfer until reached. Helper completion already forwards this channel; no new failure is left only in an inner effect probe. |

New opaque-method handling forwards __iter__, retains one-step extracted roots
and refuses reached sensitive __next__/send/throw alternatives. Existing direct
generator/local-generator paths, unstarted-close exemptions and invalid binding
paths stay in place. There is no new opaque close/throw completion precision.

Class body final namespace determines initial own roots; post-install writes
are may-only. Existing descriptor, reflective, global-write and exception guards
remain. No new precise removal, metaclass support, TryStar or correlation recovery
is claimed. The explicit unresolved-origin store refusal is the approved
exception to the earlier blanket dormant-store sentence; enabled normal reserved
class storage remains dormant unless an existing guard independently refuses.

The class.__dict__/vars(class) subscript-write concern was examined and rejected:
a real class exposes a read-only mappingproxy, so such a write does not mutate the
class. No mutable-class-dictionary write machinery was added. Extracted member
values retain their own may-roots; lookup alone adds no execution blocker.

## Metering and preserved laws

The two internal merge helpers now require the operation's existing budget.
Every one of 35 direct source calls supplies it; static inspection rejects any
indirect/unowned merge reference. Recursive calls propagate it. No new epoch,
budget source or cap is introduced.

The exact first _merge_flow_values AST fast path remains unchanged: repeated
identical FlowValue objects return that same object before any new walk or charge.
This includes generators and opaque carriers. This proves only that helper law,
not ownership safety of a surrounding storage optimization.

All new graph/union work uses operation budgets: visited edges/ref tuples,
duplicate checks, member/root copies and allocations. AuthorityRecord no-op
comparison uses identity, avoiding generated equality over new member tuples.
Different-but-equal records can cause extra metered merges/COW; this cost risk
must be measured under existing caps. Existing whole-analyzer equality is not
claimed audited or fully metered. Carrier payload equality is identity-based.

Role-aware visited value and authority sets are operation-local. Current live
records dominate historical embedded projections. Missing provenance is never
treated as an empty generator or an empty member table, and no cached proof
crosses state publication/mutation.

## Static verification and custody

The retained static proof records:
- CPython 3.11.15 under -I -S -B -P; source/AST text processing only.
- Base/plan/case-pack hashes checked; original 44 and distinct L8 unchanged.
- Exact v23 name-storage region and all 27 storage nodes.
- Exact _AnalysisBudget and MAXIMUM constants.
- Only approved existing top-level nodes changed; four new carrier/union nodes.
- All other top-level statements exact AST except adding typing.Literal.
- Exact allowed ExecutionState keyword-only delta and all merge callers.
- Constructor/consumer/refusal cause inventories and candidate line anchors.
- The 17 W watch paths before/after, including generator v20
  e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679.
- Exact diffs from v23 and retained r010 source
  29c02f6fbd5eb0b7ddc9e816ef28f570b9839358.

These checks establish source syntax, scope and custody; they do not establish
semantic correctness, runtime fit or regression freedom. Root-owned reviewed
floor-first isolated controls remain necessary for all 52 fixed expectations
and the other retained scopes. No W/main/test source bytes were changed here.


## Exact candidate sites

| Node | Candidate lines | AST SHA-256 |
| --- | --- | --- |
| _merge_flow_values | 13583-13641 | 3e26197b08481f807a7774a160b676e24590dd4e3286d9f1bc2ef284a28a1eb2 |
| _merge_legacy_flow_values | 13644-13950 | cd5bca922e4b1cf3be08b30bb228239796609c06c29e18c232c3db60d67b2ae2 |
| _AuthorityRecord | 14023-14031 | f7651039d0d071ed94a45e74e87ca05016125ccdbf155e4ea08c0dbb48405fbe |
| _AuthorityMap | 14034-14092 | 17f55eabb55125d1c8f9080c659d12fe8ed942c3c3b40624367f0d33821298bf |
| _AuthorityState | 14150-14220 | a9b941f66ce13520fad1cdcde5018ebbe3c57552b9d3a977598d6a63fdac050a |
| _transfer_authority | 14223-14314 | fa99bc70c141cadd0678ffe371f9ba9a2fdabd1d413fbd77d3b18792486ad893 |
| _ExecutionState | 14913-15108 | 6c9e8c96d42e08c2bf2848a7f88bc9f0285e31e313bff58ad9bbb040b08fedea |
| _captured_call_environment | 15212-15238 | bcb6dfc6a39d4773479ce41500654830fe0d872823d889d94c90afbf49b221ab |
| _SourceOrderedResolver | 15286-25238 | 87baec34e2abc1f5466a63c75b74577d725a2df201eccdb5593ae320cdc7b48a |
| _source_ordered_helper_return | 25299-25339 | 9cf7fe901dd0547e27c97e6cf46a8e7396052785064e959e1038a5ea05dbb55a |
| _DeferredResultCarrier | 9041-9045 | f534e6efb6eaefaba5c9e2a9f0645f491d2d1a051345d3db36eedf079ad10bce |
| _NativeCollectionEffect | 9049-9052 | 3e2b168110707d2fabc04c42e631708f74d532ccf2c416f7ed3f40ffb05a6960 |
| _ordered_flow_roots | 9055-9070 | 0a2c00d7df0450f758a69c10829b64c5547c375f04e97d86f61edc08efad470d |
| _join_member_obligations | 9073-9094 | f50bff9233758d1a312e60224629d118057f3f9a160197d4d9d84e765434747a |

| Changed/new resolver method | Candidate line |
| --- | --- |
| __init__ | 15287 |
| _class_generator_requires_refusal | 15507 |
| _deferred_result_values | 15513 |
| _retained_deferred_values | 15601 |
| _immediate_deferred_values | 15606 |
| _carrier_result | 15611 |
| _element_result_values | 15624 |
| _has_class_member_obligations | 15685 |
| _class_member_owner_ids | 15695 |
| _class_member_obligations | 15795 |
| _with_class_member_authority | 15826 |
| _retain_class_member_write | 15862 |
| _current_exact_collection_value | 15895 |
| _invalidate_collection_result_shape | 15915 |
| _transfer | 15938 |
| _refresh_bound_projection | 15955 |
| _class_read_name | 15978 |
| _class_merge_local_projection | 16057 |
| _evaluate_class_comprehension | 16117 |
| _snapshot_call | 17846 |
| _resume_deferred_local_generator_value | 18287 |
| _poison_mutable_collection | 18716 |
| _record_deferred_generator_consumption | 18744 |
| _deferred_generator_state_is_sensitive | 18949 |
| _consume_generator_expression | 19083 |
| _reachable_helper_authorities | 19398 |
| _helper_effect_shape | 19630 |
| _has_callable_authority | 19868 |
| _native_effect_preserves | 19904 |
| _collection_authority_result | 19912 |
| _retain_native_collection_authority | 19990 |
| _retain_native_list_call | 20005 |
| _apply_helper_call_effects | 20099 |
| _evaluate | 20361 |
| _evaluate_comprehension | 20491 |
| _evaluate_value | 20790 |
| _assign | 22746 |
| _delete_target | 23111 |
| _merge_auxiliary_states | 23382 |
| _flow_statement_value | 23660 |
| _try_statement_states | 24276 |
| _flow_class_statement | 24463 |
| _finish_class_definition | 24621 |
| _statements | 24720 |

| Merge call owner | Candidate line | Existing operation budget |
| --- | --- | --- |
| _merge_flow_values | 13595 | budget |
| _merge_flow_values | 13596 | budget |
| _merge_flow_values | 13630 | budget |
| _merge_flow_values | 13635 | budget |
| _merge_legacy_flow_values | 13676 | budget |
| _merge_legacy_flow_values | 13720 | budget |
| _merge_legacy_flow_values | 13761 | budget |
| _merge_legacy_flow_values | 13765 | budget |
| _AuthorityState.join | 14198 | self.budget |
| _AuthorityState.join | 14218 | self.budget |
| _ExecutionState._write_cells | 15047 | self.authority.budget |
| _ExecutionState.__delitem__ | 15057 | self.authority.budget |
| _captured_call_environment | 15234 | budget |
| _SourceOrderedResolver._current_exact_collection_value | 15910 | self.budget |
| _SourceOrderedResolver._refresh_bound_projection | 15964 | self.budget |
| _SourceOrderedResolver._class_read_name | 16003 | self.budget |
| _SourceOrderedResolver._class_merge_local_projection | 16062 | self.budget |
| _SourceOrderedResolver._class_merge_local_projection | 16081 | self.budget |
| _SourceOrderedResolver._snapshot_call | 17859 | self.budget |
| _SourceOrderedResolver._snapshot_call | 17872 | self.budget |
| _SourceOrderedResolver._resume_deferred_local_generator_value | 18340 | self.budget |
| _SourceOrderedResolver._evaluate_comprehension | 20632 | self.budget |
| _SourceOrderedResolver._evaluate_comprehension | 20738 | self.budget |
| _SourceOrderedResolver._evaluate_value | 20823 | self.budget |
| _SourceOrderedResolver._evaluate_value | 21280 | self.budget |
| _SourceOrderedResolver._evaluate_value | 21318 | self.budget |
| _SourceOrderedResolver._evaluate_value | 22044 | self.budget |
| _SourceOrderedResolver._merge_auxiliary_states | 23402 | self.budget |
| _SourceOrderedResolver._merge_auxiliary_states | 23433 | self.budget |
| _SourceOrderedResolver._merge_auxiliary_states | 23468 | self.budget |
| _SourceOrderedResolver._flow_statement_value | 23903 | self.budget |
| _SourceOrderedResolver._try_statement_states | 24332 | self.budget |
| _SourceOrderedResolver._statements | 24877 | self.budget |
| _source_ordered_helper_return | 25333 | budget |
| _source_ordered_helper_return | 25339 | budget |
