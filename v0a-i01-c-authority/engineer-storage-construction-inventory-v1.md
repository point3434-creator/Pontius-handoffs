# Engineering storage construction inventory v1

Status: static engineering inspection; not a cold review, execution receipt,
correctness verdict, patch authorization, or claim that the work cap now passes.

Pinned source
- W/tools/generate_test_inventory.py and T/engineer-generator-v20.py both:
  e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679
- W = D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1
- T = D:\Pontius-handoffs\v0a-i01-c-authority
- Retained v19 generator:
  3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1
- All source line numbers below refer to the pinned v20 file.

Scope and method
- Read source plus stdlib ast.parse/ast.walk of source bytes, using Python 3.11.
  No generator, test, case, helper, or control imported or executed.
- Enumerated all direct _ExecutionState calls, all _fork_values calls, all
  state-receiver update calls, and assignments to authority/bindings/_names.
  Inspected source around each distinct construction/adoption/semantic boundary.
- Six direct state constructors, one object.__new__ in copy, 72 fork callers,
  14 state-capable update sites, and one additional pre-entry dict update.
- No W edits, tests, APIs, caps, Git configuration, commits, or payload actions.
  This create-only T note is the sole write for this resumed inspection.
- Root supplied failure context; this note does not independently verify runs
  or infer measured savings. All proposed changes require separate review.

Design assessment
STRAINED for workload fit: construction and full-fallback joins repeatedly build
immutable AVL versions one entry at a time, including helper-disabled passes.
The adapter preserves important semantic distinctions, but misses bounded
sharing/building seams below. These are storage alternatives, not permission to
skip authority transfer, omit cell writes, increase caps, or widen support.

Constructor contract: 14564-14584
- An ExecutionState parent determines authority.enabled and its authority budget,
  even if the enabled/budget arguments disagree. Authority and bindings fork;
  the parent's name meter is reused. A plain Mapping parent supplies none of
  these stores or proof.
- Local cells allocate first, in the existing local_names iteration order, only
  when the inherited/new authority is enabled.
- For each values.items() entry, same-name same-object parent values outside
  local_names inherit the exact name entry, including proof OR pending debt.
  This path does no transfer and no cell write.
- Every other entry goes through __setitem__: transfer, projection insertion,
  and all existing bound-cell writes if enabled. Same-object local parameter
  values still require these writes to the fresh activation's cells.
- There are no production generator-valued local_names arguments here; resolver
  lexical local_names is the existing frozenset. Do not silently broaden an
  optimization to arbitrary iterables with different iteration behavior.

Every direct construction and allocation
1. 14967, SourceOrderedResolver.__init__:
   values is the newly prepared plain dict self.values; parent=entry_values;
   local_names=lexical_scope.local_names; enabled=bool(helper_registry).
   It is NOT the parent object. Dict preparation at 14811-14965 inserts aliases,
   evaluated module entries and local summaries, overlays parent at 14905, then
   resets locals/parameters/nonlocals/globals. Existing key positions survive.
   With a state parent, unchanged nonlocals inherit; new/changed names and ALL
   locals transfer/write. Without state parent all entries transfer. It may be
   disabled, or enabled, according to the constructor rule above.
   Whole-parent sharing is unsafe: aliases can precede a different parent order;
   local reset and fresh parameter cell writes cannot be omitted.

2. 14974, _fork_values non-state branch:
   supplied values is plain Mapping, no parent/local_names, mode is resolver
   helper-registry truthiness. Fresh stores; every entry must take transfer.
   Ref-bearing values are not proof that their object store accompanied them;
   enabled transfer's missing-store refusal at 14046-14054 must remain.
   State inputs instead use copy at 14973, not this constructor.

3. 18476, _registered_helper_environment:
   empty values, parent=caller values, default enabled=True. Normally reached
   only through helper-enabled _apply_helper_call_effects. State parents keep
   their mode, stores and bindings, but NO caller names are initially projected.
   There are no constructor local allocations or name writes.
   18477-18486 then semantically assigns aliases, selected seeds and evaluated
   defining-module assignments. 18488 is a semantic filtered overlay.
   Sharing the caller's names would leak unrelated caller locals into the
   defining-module namespace. Turning those later setters into inherited raw
   constructor entries would omit transfers and writes to inherited bindings.

4. 21831, _merge_states empty-input branch:
   empty Mapping, no parent/local_names, mode=bool(resolver helper registry).
   Fresh empty stores/projection. Nothing to transfer, copy, or write.
   One input 21833 copies/fresh-converts through _fork_values; multiple inputs
   21834 do the same for the first state before authority/binding joins.

5. 25388, _review_body provenance_entries:
   values=entry_values or {}, parent=entry_values, no local_names;
   enabled=bool(helper_registry). For a nonempty ExecutionState, values IS parent.
   Every entry is inherited; zero name transfers and zero bound-cell writes.
   Empty state parent also has zero entries even though "or {}" chooses a dict.
   Plain/None entry creates fresh stores and semantically transfers every input.
   Later receiver provenance changes at 25400 are separate semantic setters.
   This exact-parent/no-locals boundary can share the parent's immutable
   names/order/proof/debt while still forking authority and bindings.

6. 25895, recursive local-helper review entry:
   input is a plain dict comprehension of source_flow.values_by_call[id(call)],
   excluding the local node's lexical local_names; parent is that source state.
   No local_names argument is passed, so no local cell allocation here.
   The source snapshot is a state produced by the resolver snapshot/join path;
   all retained entries preserve exact parent value identity and parent order.
   They therefore inherit without transfer/cell writes. Bindings/cells for
   omitted names STILL fork; omission is a name projection, not cell deletion.
   A persistent filtered projection can reuse entries/root subtrees or remove
   excluded names raw, preserving filtered order and correct change history.
   Plain arbitrary Mapping parent must retain the generic constructor behavior.

7. 14734, _ExecutionState.copy allocation:
   exact full projection copy; 14735 shares the immutable version, 14736/14737
   fork authority and bindings. Preserves mode/proof/debt; no transfer, fresh
   lexical allocation, or bound-cell write. This sharing is already present.
   The 72 fork callers below all funnel through this or item 2.

Every execution-state update site
The classifications below apply when the receiver is ExecutionState. BoolOp
19629 and IfExp 19665 can also run during pre-entry module-expression evaluation
with the plain dict prepared at 14811. There, builtin dict clear/update installs
only values and must not be changed into authority/bindings adoption.
- 17267 refreshed_bindings and 17281 refreshed_frame in generator resume:
  iterable pairs; ordinary semantic overlays in list order. Parameter/frame
  values may be refreshed to the first matching mutable-identity projection.
  Existing local map is a fork; its mode/bindings are unchanged. Transfer and
  each bound-cell write remain owed even for identical values.
- 18123 simple local-helper deferred return:
  generator of argument bindings, with first matching mutable alias lookup.
  Semantic overlay on a fork; same obligations as generator resume.
- 18488 registered-helper environment:
  generator of caller pairs excluding caller lexical locals, only when source
  module matches. Semantic overlay, not authority/bindings adoption. It can
  overwrite aliases/seeds and inherited captured bindings.
- 18561 projected helper-call probe:
  supplied environment IS ExecutionState. Nonempty raw overlay/adoption after
  the resolver constructor initialized its lexical locals as unbound.
  Adopt supplied authority AND bindings. Preserve destination-only names and
  destination positions, overwrite/add supplied names in supplied order. No
  transfer/cell writes. Current nonempty _project installs pending name debt.
  Do not substitute unconditional replacement or semantic update.
- Replacement pairs, clear immediately followed by state update:
  16382/16383 resolve;
  19628/19629 BoolOp completed states;
  19664/19665 IfExp completed branches;
  23126/23127 selected If branch;
  23139/23140 merged If branches;
  23177/23178 For successors;
  23226/23227 While successors;
  23276/23277 Try successors;
  23319/23320 Match alternatives.
  Supplied state comes from a fork, statement state, or _merge_states.
  With a state receiver, all adopt complete stores/bindings and names via the
  implemented empty-destination version fork. No name transfer or cell writes.
  clear resets only names; it does not perform Python del on captured bindings.

The additional 14905 update is a builtin dict receiver BEFORE conversion.
It is a raw values-only overlay preserving dict insertion positions; it neither
adopts stores nor transfers. Store inheritance happens later at 14967.

No production state update uses keywords. The adapter's keyword branch remains
semantic. No current state update supplies an arbitrary Mapping except via the
iterable generators above; the public adapter method still distinguishes it.

Other adoption/projection boundaries
- 15010 captured-cell hydration in _call_environment: fork exact caller state,
  replace binding tuples at 15006, then raw name projection from cells. Pending
  debt, no re-transfer and no cell rewrite.
- 18959-18964 activation preparation: fork environment, raw-pop helper locals,
  raw-install argument bindings. Pop/reinsert order is visible. Caller cells
  must not be deleted/written before fresh local cells allocate at 14967.
- 19020 helper-completion authority-only adoption: preserve caller bindings and
  caller names, adopt completed child authority, then restore caller observed
  and results maps at 19023/19024. 19025-19029 raw-refresh existing bound caller
  names from adopted cells. Subsequent rebound-name writes 19038 are semantic.
- 23570 class body forks names/store; 23573 resets only bindings to an empty
  AuthorityMap for class-local namespace semantics. 23596 adopts authority
  only; class-local name projection/bindings must not replace the outer ones.
  These two authority-only callers are descendants of the same input mode.
- 21835-21841 join imports supplied authority and unions binding cell tuples in
  first-seen order, irrespective of name compatibility. AuthorityState.join
  does not change enabled. Overlap/missing-cell full fallback must remain.
- 21896 directly installs joined immutable names; 21899-21901 still performs
  all participating bound-cell writes. Identical name roots do not discharge
  strong/weak cell writes.
- 16385 terminal resolve clear has no replacement and no semantic deletions.
  The remaining direct _names assignments occur inside the adapter itself.

Safe bulk-building seams and limits
A. Exact-parent no-local constructor (25388) can fork names directly. Do not
   generalize from equal values to equal order, or skip local-cell setup.

B. Ordered filtered-parent constructor (25895) can preserve exact entries
   structurally. No transfer or cell delete may be added for omitted names.
   A root with changed membership needs correct order and change-history data;
   treating it as an unchanged root would corrupt later joins.

C. Generic constructor (14576-14584) can prepare final ordered entries then
   build one balanced immutable tree, while performing original semantic
   operations in original input order. Proof:
   _transfer_authority 14034-14083 reads/writes only authority, not the name map;
   _transferred_name_entry 14637-14652 only calls that transfer and certifies its
   result; _write_cells 14675-14679 reads/writes only existing authority cells.
   Inherited comparison consults parent, not partially constructed self.
   Keep local identity allocation first, and keep transfer+cell-write sequencing.
   Do not simply declare all initial values raw or certified.

D. Full-fallback join 21876-21888 is another bulk-building boundary:
   preserve exact set().union(*state.keys()) order and each name's flow merge,
   transfer, and all sequential cell writes. Only assemble the result name
   index once. _merge_flow_values 13431-13489 reads its supplied immutable
   values; it does not consult result projection. Overlapping cells still need
   original order. A bulk tree build is not permission to use optimized joins
   on disabled/plain/missing-cell/overlapping-cell inputs.

E. Nonempty state overlay 14711-14718 may bulk-build a final projection with
   destination order and pending certificates, after adopting stores. It may
   not share supplied proof-carrying entries indiscriminately: current raw
   installation semantics distinguishes pending debt even for identical values.
   Existing empty-destination adoption already shares safely.
   A narrowly proved caller-equivalent replacement would require proof that
   destination-only names are absent, final key order matches, and certificate
   treatment is permitted. This inspection grants no such shortcut at 18561.

Every bulk operation must meter actual input visits, entry/reference copies,
temporary structures, comparisons/sorting, tree/order/history allocation and
cache work. Eliminate intermediate work rather than exempting work performed.
Balanced bulk construction would be a new internal implementation, not a helper
already available in this v20 adapter. Cost improvement remains unmeasured.

Disabled representation option and mode crossings
- _transfer_authority returns its input immediately when disabled, 14043/14044.
  Constructor allocates no local cells; setters/deleters skip bound-cell writes.
  Disabled joins always take full fallback, yet current names still incur AVL
  storage and ordered materialization costs.
- A dict-backed disabled projection is semantically plausible: retain exact
  order, independent fork snapshots, raw-vs-semantic interfaces, and the
  original full fallback merge. It is not established sufficient for corpus
  fitness, particularly helper-enabled public24 workloads.
- Four explicit helper-disabled resolver roots omit helper_registry:
  23756 helper-return summary; 24982 process-definition program resolver;
  26282 definition-time protocol resolver; 26722 receiver-attribute preflight.
  The latter has a plain receiver-entry dict and lexical local names.
- 23853 review-flow resolver passes its registry and entry_values; 25564 supplies
  provenance_entries created at 25388 under the same registry. Empty registry
  can therefore also create disabled review states.
- 18549 projected and 19000 live helper probes pass the caller's registry and
  descendant environment. Helper effect entry is guarded by registry at 18852.
- No enabled mutation exists outside AuthorityState construction/fork.
  Parent inheritance, copy, and ordinary descendants preserve the actual mode;
  enabled argument alone is not a valid representation discriminator.
- State update ADOPTS supplied mode; generic iterable update keeps destination
  mode. A two-representation adapter must handle mode-changing update explicitly
  even if existing production callers normally preserve lineage.
- Mixed _merge_states retains FIRST state mode; authority join does not promote
  it. Plain first Mapping uses resolver bool to choose a fresh enabled/disabled
  state, with all original transfers owed. Do not reinterpret mixed inputs.
- Helper/class authority-only assignments preserve mode in current callers but
  are seams where a future representation-mode invariant must be maintained.
  No silent raw conversion may mint an enabled no-work certificate from
  disabled values or erase missing-store obligations.
- _names private access is concentrated in adapter and _merge_states; a mode
  branch must cover constructor inheritance and 21842-21849 compatibility,
  not merely __getitem__/__setitem__.

Complete _fork_values caller appendix (72 sites)
Each call below is exact full-copy semantics for a state: no fresh local cells,
no transfers/writes, preserve actual mode. Otherwise it is fresh plain-Mapping
conversion at 14974 with resolver-chosen mode and every transfer owed. Arguments
are named to distinguish whole states from prepared local/default environments;
none of these calls itself requests an overlay or filtered projection.

14996 _call_environment(values)
15649 _extreme_key_projection(values)
16697 _snapshot_call(values)
16788 _environment_snapshot(values)
16889 _record_throw_state(values)
16902 _evaluate_with_successors(values)
17003 _deferred_local_generator_is_sensitive(values)
17248 _resume_deferred_local_generator(values)
17317 _resume_deferred_local_generator(successors.normal[0])
17766 _deferred_generator_node_is_sensitive(values)
17864 _deferred_generator_state_is_sensitive(values)
17972 _consume_generator_expression(values)
18122 _simple_local_helper_deferred_return(values)
18182,18187 _with_callable_authority(default_scope)
18302 _unproved_callable_effects(values)
18638 _record_callable_construction_obligations(values)
18959 _apply_helper_call_effects(environment)
19579 _evaluate_value(values)
19621 _evaluate_value(current)
21034 _evaluate_value(values)
21135 _evaluate_value(local_values)
21833,21834 _merge_states(states[0])
22167 _flow_statements(values)
22189 _flow_expression_statement(values)
22251 _flow_statement_value(values)
22275,22285 _flow_statement_value(current)
22313,22315,22348 _flow_statement_value(values)
22415 _flow_statement_value(exceptional.state)
22451,22470,22543,22560 _flow_statement_value(current)
22564 _flow_statement_value(incoming)
22633 _flow_statement_value(residual.state)
22668,22676 _flow_statement_value(handler_state)
22796 _try_body_states(values)
22831,22846,22854,22868 _try_statement_states(values)
22874 _try_statement_states(current)
22908 _try_statement_states(values)
22916 _try_statement_states(current)
22937 _try_statement_states(values)
22943 _try_statement_states(incoming)
22951 _try_statement_states(case_state)
22966 _try_statement_states(values)
22968 _try_statement_states(current)
22980 _exceptional_environment_state(values)
23125,23130,23133,23157,23171,23194,23197 _statements(values)
23200 _statements(body)
23252 _statements(values)
23257 _statements(body)
23262,23273 _statements(raised)
23282 _statements(values)
23286 _statements(residual)
23308 _statements(case_state)
23313 _statements(residual)
23570 _statements(values)

Residual proof obligations
- Exact source order and inherited-entry identity/proof/debt are semantic
  invariants; no private exact allocation ID equality is demanded.
- Missing live store references at legitimate helper/class/adoption boundaries
  remain relevant. Fabricated future private IDs are not a public source case.
- Preserve first-owner traversal tuples and same-key retained children; this
  note establishes no new public discrepancy from private registration order.
- A safe storage refinement still needs reviewed finite floor-first execution
  against frozen scopes. Existing public24/design53/matrix192/212/join8/weak3/
  lexical6/A19/B18 required plus one excluded and composition cases remain
  unchanged. This note does not author or execute any additional case.
