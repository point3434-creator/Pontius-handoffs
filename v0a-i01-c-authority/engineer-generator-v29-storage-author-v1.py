import ast,copy,difflib,hashlib,json,types
from pathlib import Path
T=Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
W=Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
PRE="4db6502350e59fe363998351384a62d9e669598241a644810e9a7ffd6b4b4d0e"
sha=lambda b:hashlib.sha256(b).hexdigest()
jd=lambda d:(json.dumps(d,indent=2,sort_keys=True)+"\n").encode()
def pin(name,wanted):
 b=(T/name).read_bytes();assert sha(b)==wanted,(name,sha(b));return b
old_bytes=pin("engineer-generator-v28-storage.py",PRE)
old=old_bytes.decode();oa=ast.parse(old)
pin("engineer-v28-disabled-join-plan-v1.md","d8faada0f14b1f7ffb0e0062ebd90e6fe196718b663cba93d39cd8246ff1b7fa")
pin("engineer-v28-disabled-join-anchors-v1.json","571f5bc305a43df9bf3965d000a2134c277de20ac8c4dd99b1de070b92e7dff8")
previous_accounting=json.loads(pin("engineer-generator-v28-storage-accounting-v1.json","077c1b4779709672a79368ea1081ecd9cb0499c651851a571a80f075e983c45b"))
previous_preservation=json.loads(pin("engineer-generator-v28-storage-preservation-v1.json","df90b1686d6760a9c3876ca0f0f81ae56519d1368a5cd811db8461a9790a2d0d"))
binding=json.loads(pin("engineer-generator-v28-storage-binding-proof-v1.json","d786b9a609a37bf88ea18d6d6585d2ffb6cafd6ced908d23c1e086291ed8650c"))
def top(tree,name):return next(n for n in tree.body if getattr(n,"name",None)==name)
def method(tree,cls,name):return next(n for n in top(tree,cls).body if getattr(n,"name",None)==name)
def seg(s,n):return ast.get_source_segment(s,n)
def dump(n):return ast.dump(n,include_attributes=False)
original=method(oa,"_SourceOrderedResolver","_merge_states");old_method=seg(old,original)
needle="            result.clear()\n            meter = result._names._meter"
assert old_method.count(needle)==1
branch="            # Operation-local identity law: disabled transfer does no work, but\n            # retained entries remain pending for every later enabled boundary.\n            # Generic joins and the legacy full fallback retain their contracts.\n            disabled_join = False\n            self.budget.consume()  # Exact, stable source-sequence type.\n            stable_sources = type(states) is tuple\n            if not stable_sources:\n                self.budget.consume()  # The other ordinary source-sequence type.\n                stable_sources = type(states) is list\n            self.budget.consume(2)  # First snapshot reference and exact type check.\n            first_names = name_inputs[0]\n            exact_first = type(first_names) is _NameVersion\n            if stable_sources and exact_first:\n                self.budget.consume(2)  # Meter reference and exact type check.\n                join_meter = first_names._meter\n                if type(join_meter) is _NameMeter:\n                    self.budget.consume()  # Original budget identity.\n                    if join_meter.budget is self.budget:\n                        join_meter.charge(\"disabled_join_guard_function_allocation\")\n                        join_meter.charge(\"disabled_join_guard_closure_references\", 2)\n\n                        def disabled_input(state, captured):\n                            join_meter.charge(\"disabled_join_exact_state_checks\")\n                            if type(state) is not _ExecutionState:\n                                return False\n                            join_meter.charge(\"disabled_join_authority_guard_reads\", 2)\n                            authority = state.authority\n                            if type(authority) is not _AuthorityState:\n                                return False\n                            join_meter.charge(\"disabled_join_mode_checks\")\n                            if authority.enabled is not False:\n                                return False\n                            join_meter.charge(\"disabled_join_budget_checks\")\n                            if authority.budget is not self.budget:\n                                return False\n                            join_meter.charge(\"disabled_join_cursor_guard_reads\", 2)\n                            cursor = state._names\n                            if type(cursor) is not _NameCursor:\n                                return False\n                            join_meter.charge(\"disabled_join_meter_checks\")\n                            if cursor._meter is not join_meter:\n                                return False\n                            join_meter.charge(\"disabled_join_exact_version_checks\")\n                            if type(captured) is not _NameVersion:\n                                return False\n                            join_meter.charge(\"disabled_join_meter_checks\")\n                            if captured._meter is not join_meter:\n                                return False\n                            join_meter.charge(\"disabled_join_root_reads\")\n                            pending = _name_radix_pending_count(join_meter, captured._root)\n                            join_meter.charge(\"disabled_join_pending_size_checks\", 2)\n                            return pending == captured._size\n\n                        disabled_join = disabled_input(result, first_names)\n                        if disabled_join:\n                            join_meter.charge(\"disabled_join_input_iterator_allocations\", 2)\n                            for index, state in enumerate(states):\n                                join_meter.charge(\"disabled_join_input_visits\", 2)\n                                if not disabled_input(state, name_inputs[index]):\n                                    disabled_join = False\n                                    break\n            if disabled_join:\n                base = _name_common_history(join_meter, name_inputs)\n                join_meter.charge(\"disabled_join_common_history_checks\")\n                if base is not None:\n                    join_meter.charge(\"disabled_join_candidate_dictionary_allocation\")\n                    candidate_names = {}\n                    join_meter.charge(\"disabled_join_history_input_iterator_allocation\")\n                    for captured in name_inputs:\n                        join_meter.charge(\"disabled_join_history_input_visits\")\n                        join_meter.charge(\"disabled_join_history_reference_reads\")\n                        token = captured._history\n                        while token is not base:\n                            join_meter.charge(\"disabled_join_history_token_visits\")\n                            join_meter.charge(\"disabled_join_history_change_reference_reads\")\n                            join_meter.charge(\"disabled_join_history_change_iterator_allocation\")\n                            for name in token.changes:\n                                join_meter.charge(\"disabled_join_changed_name_visits\")\n                                join_meter.charge(\"disabled_join_candidate_dictionary_attempts\")\n                                if name not in candidate_names:\n                                    join_meter.charge(\"disabled_join_candidate_dictionary_writes\")\n                                    join_meter.charge(\"disabled_join_candidate_reference_copies\", 2)\n                                    candidate_names[name] = None\n                            join_meter.charge(\"disabled_join_history_reference_reads\")\n                            token = token.parent\n                    join_meter.charge(\"disabled_join_cardinality_choice\", 3)\n                    if len(candidate_names) < len(names):\n                        staged = _NameCursor(first_names)\n                        join_meter.charge(\"disabled_join_order_dictionary_allocation\")\n                        order_table = {}\n                        join_meter.charge(\"disabled_join_union_iterator_allocation\")\n                        for name in names:\n                            self.budget.consume()  # The original legacy union-name visit.\n                            join_meter.charge(\"disabled_join_order_dictionary_writes\")\n                            join_meter.charge(\"disabled_join_order_reference_copies\", 2)\n                            order_table[name] = None\n                            join_meter.charge(\"disabled_join_candidate_dictionary_attempts\")\n                            if name not in candidate_names:\n                                # Do not generalize this to None, subclasses, a\n                                # positive certificate, or a now-enabled result.\n                                join_meter.charge(\"disabled_join_name_type_checks\")\n                                if type(name) is str:\n                                    join_meter.charge(\"disabled_join_mode_checks\")\n                                    if result.authority.enabled is False:\n                                        inherited = first_names._entry(name)\n                                        join_meter.charge(\"disabled_join_entry_type_checks\")\n                                        if type(inherited) is _NameEntry:\n                                            join_meter.charge(\"disabled_join_pending_flag_checks\")\n                                            if inherited.no_work is False:\n                                                join_meter.charge(\"disabled_join_value_type_checks\")\n                                                if type(inherited.value) is _FlowValue:\n                                                    continue\n                            join_meter.charge(\"adapter_merge_values_generator_allocation\")\n                            join_meter.charge(\"adapter_merge_values_iterator_allocation\")\n                            join_meter.charge(\"adapter_merge_values_generator_references\", 2)\n                            self.budget.consume(1 + 2 * len(name_inputs))\n                            supplied = tuple(state.get(name) for state in name_inputs)\n                            entry = result._transferred_name_entry(_merge_flow_values(name, supplied))\n                            _name_check_name(name)\n                            if result.authority.enabled:\n                                identities = result.bindings.get(name, ())\n                                result._write_cells(entry.value, identities)\n                            staged._replace_entry(name, entry)\n                        memo = _name_seal_order_table(join_meter, order_table)\n                        order = _name_order(join_meter, \"known\", cache=memo)\n                        join_meter.charge(\"disabled_join_order_install_references\", 2)\n                        staged._order = order\n                        staged._items_cache = None\n                        version = staged.snapshot()\n                        cursor = _NameCursor(version)\n                        join_meter.charge(\"disabled_join_result_install_reference\")\n                        result._names = cursor\n                        return result\n"
new_method=old_method.replace(needle,branch+needle)
source=old.replace(old_method,new_method)
raw=source.encode();source_sha=sha(raw);na=ast.parse(source)
compiled=compile(na,"engineer-generator-v29-storage.py","exec",dont_inherit=True)
assert source.replace(branch,"").encode()==old_bytes
assert source.count(branch)==1
# Recover the entire original module AST by replacing only the one method.
inverse=copy.deepcopy(na);cls=top(inverse,"_SourceOrderedResolver")
for i,n in enumerate(cls.body):
 if getattr(n,"name",None)=="_merge_states":cls.body[i]=copy.deepcopy(original)
assert dump(inverse)==dump(oa)
changed=method(na,"_SourceOrderedResolver","_merge_states")
old_if=next(n for n in original.body if isinstance(n,ast.If) and isinstance(n.test,ast.UnaryOp) and isinstance(n.test.operand,ast.Name) and n.test.operand.id=="compatible")
new_if=next(n for n in changed.body if isinstance(n,ast.If) and isinstance(n.test,ast.UnaryOp) and isinstance(n.test.operand,ast.Name) and n.test.operand.id=="compatible")
clear_index=next(i for i,n in enumerate(old_if.body) if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr=="clear")
new_clear_index=next(i for i,n in enumerate(new_if.body) if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr=="clear")
assert [dump(n) for n in old_if.body[:clear_index]]==[dump(n) for n in new_if.body[:clear_index]]
assert [dump(n) for n in old_if.body[clear_index:]]==[dump(n) for n in new_if.body[new_clear_index:]]
inserted=new_if.body[clear_index:new_clear_index]
# The one original union expression occurs once; no retry/fallback recomputes it.
def unions(n):return [x for x in ast.walk(n) if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr=="union"]
assert len(unions(original))==len(unions(changed))==1
assert dump(unions(original)[0])==dump(unions(changed)[0])
# Both old and new per-name operations have identical original supplied tuple,
# merge->transfer call, name validation and conditional cell-write statements.
old_producer=next(n for n in ast.walk(original) if isinstance(n,ast.FunctionDef) and n.name=="merged_entries")
old_for=next(n for n in old_producer.body if isinstance(n,ast.For))
def supplied_statement(n):return isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="supplied" for t in n.targets)
si=next(i for i,n in enumerate(old_for.body) if supplied_statement(n))
per_name=old_for.body[si:si+4]
assert len(per_name)==4 and isinstance(per_name[-1],ast.If)
new_for=next(n for z in inserted for n in ast.walk(z) if isinstance(n,ast.For) and isinstance(n.iter,ast.Name) and n.iter.id=="names")
ni=next(i for i,n in enumerate(new_for.body) if supplied_statement(n))
assert [dump(n) for n in new_for.body[ni:ni+4]]==[dump(n) for n in per_name]
assert not any(isinstance(n,ast.Attribute) and n.attr=="no_work" and isinstance(n.ctx,(ast.Store,ast.Del)) for z in inserted for n in ast.walk(z))
assert not any(isinstance(n,ast.keyword) and n.arg=="no_work" for z in inserted for n in ast.walk(z))
# The identity-return prefix and every other method/class/cap remain byte-exact.
protected={}
for name in ["_merge_flow_values","_merge_legacy_flow_values","_transfer_authority","_ExecutionState",
             "_AuthorityState","_AuthorityMap","_ObservedAuthorityMap","_AnalysisBudget","_NameMeter"]:
 x,y=top(oa,name),top(na,name)
 assert seg(old,x)==seg(source,y)
 protected[name]={"source_sha256":sha(seg(source,y).encode()),"AST_sha256":sha(dump(y).encode())}
assert [dump(x) for x in top(oa,"_merge_flow_values").body[:1]]==[dump(x) for x in top(na,"_merge_flow_values").body[:1]]
unchanged_methods=0
for n in top(oa,"_SourceOrderedResolver").body:
 if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name!="_merge_states":
  assert seg(old,n)==seg(source,method(na,"_SourceOrderedResolver",n.name));unchanged_methods+=1
primitive=[]
for row in binding["primitive_objects"]:
 name=row["candidate_name"]
 def target(tree):
  if row["kind"] in ("FunctionDef","ClassDef"):return top(tree,name)
  return next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets))
 x,y=target(oa),target(na);assert seg(old,x)==seg(source,y)
 primitive.append({"name":name,"kind":row["kind"],"source_sha256":sha(seg(source,y).encode()),"unchanged":True})
assert len(primitive)==47
caps={}
for n in oa.body:
 if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id.startswith("MAXIMUM_ANALYSIS_"):
  name=n.targets[0].id
  v=next(x for x in na.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in x.targets))
  assert dump(n)==dump(v);caps[name]=ast.unparse(v.value)
assert len(caps)==5
def codes(co):
 yield co
 for x in co.co_consts:
  if isinstance(x,types.CodeType):yield from codes(x)
helper=next(c for c in codes(compiled) if c.co_qualname=="_SourceOrderedResolver._merge_states.<locals>.disabled_input")
assert helper.co_freevars==("join_meter","self")
# Inventory every original-delegating NameMeter category; unchanged categories
# retain the existing P/non-P (or explicitly unclassified adapter) designation.
def charge_inventory(tree):
 out={}
 class V(ast.NodeVisitor):
  def __init__(self):self.path=[]
  def visit_ClassDef(self,n):self.path.append(n.name);self.generic_visit(n);self.path.pop()
  def visit_FunctionDef(self,n):self.path.append(n.name);self.generic_visit(n);self.path.pop()
  visit_AsyncFunctionDef=visit_FunctionDef
  def visit_Call(self,n):
   if isinstance(n.func,ast.Attribute) and n.func.attr=="charge":
    assert n.args and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str)
    out.setdefault(n.args[0].value,[]).append({"function":".".join(self.path),"line":n.lineno,"units":ast.unparse(n.args[1]) if len(n.args)>1 else "1"})
   self.generic_visit(n)
 V().visit(tree);return out
oc,nc=charge_inventory(oa),charge_inventory(na)
added=set(nc)-set(oc);assert added and all(k.startswith("disabled_join_") for k in added)
assert set(oc)<=set(nc)
p_categories={
 "disabled_join_input_visits","disabled_join_history_input_visits",
 "disabled_join_history_token_visits","disabled_join_changed_name_visits",
 "disabled_join_candidate_reference_copies","disabled_join_order_reference_copies"}
full={}
for name,sites in nc.items():
 if name in previous_accounting["categories"]:
  row=dict(previous_accounting["categories"][name]);row["source_sites"]=sites;full[name]=row
 else:
  full[name]={"metric":"P" if name in p_categories else "non-P",
   "operation":("Actual variable-cardinality input/history/name traversal or name-reference copies." if name in p_categories else
    "Actual fixed-arity guard/read, logical dictionary attempt/write, iterator/wrapper allocation, or publication-field operation; included in full budget units."),
   "origin":"v29 operation-local disabled join","source_sites":sites}
assert p_categories<=added
new_consumes=[]
for z in inserted:
 for n in ast.walk(z):
  if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="consume":
   new_consumes.append({"line":n.lineno,"units":ast.unparse(n.args[0]) if n.args else "1"})
new_consumes.sort(key=lambda x:x["line"])
# Field writes introduced by the branch are limited to unpublished name staging
# and the final result install. No authority, cell or Entry flag writes appear.
writes=[]
for z in inserted:
 for n in ast.walk(z):
  if isinstance(n,ast.Attribute) and isinstance(n.ctx,ast.Store):
   writes.append({"expression":ast.unparse(n),"line":n.lineno})
assert sorted(x["expression"] for x in writes)==["result._names","staged._items_cache","staged._order"]
w_before={name:sha((W/name).read_bytes()) for name in previous_preservation["W_after"]}
assert len(w_before)==1761 and w_before==previous_preservation["W_after"]
assert (T/"engineer-generator-v28-storage.py").read_bytes()==old_bytes
w_after={name:sha((W/name).read_bytes()) for name in w_before};assert w_after==w_before
delta="".join(difflib.unified_diff(old.splitlines(True),source.splitlines(True),
 fromfile="engineer-generator-v28-storage.py",tofile="engineer-generator-v29-storage.py"))
disposition=f"""# Root disposition: operation-local disabled join

Recorded at the root coordinator's explicit request on2026-08-31. This note
records the coordinator's source GO; it is not the implementer's self-approval,
a runtime verdict, a general transfer exemption, or an integration authorization.

Approved plan: engineer-v28-disabled-join-plan-v1.md
d8faada0f14b1f7ffb0e0062ebd90e6fe196718b663cba93d39cd8246ff1b7fa.
Exact predecessor v28 {PRE}.
Retained v29 source {source_sha}.

## Normative clarification

For one all-disabled _merge_states operation, exact compatible state/snapshot
wrappers on the same original budget/NameMeter, with all effective entries pending,
may use a common names-only history to establish unchanged entries. An unchanged
exact Entry containing an exact FlowValue may be retained because identical-input
merge and disabled transfer are both identity operations. Retained Entry.no_work
must stay False. This creates no enduring certificate and does not discharge any
future enabled revalidation debt.

Every changed, atypical, incompatible, enabled or otherwise unproved path retains
the original merge/transfer behavior. The original snapshots, authority/binding
joins and ordered conditional cell writes remain. Every actual new guard, history
visit, candidate operation, name/order copy and publication is charged under the
unchanged five production caps. All-parent legacy union is computed once and its
exact eager iteration order is retained. False guards preserve the old full body.

## Bounded implementation

Only _SourceOrderedResolver._merge_states changes. Generic NameVersion/NameCursor
APIs, radix/history/order algorithms, transfer, cells and all other methods stay
source-exact. The implementation further restricts eligible source sequences to
exact list/tuple, authority/cursor/meter wrappers to exact types, and skipped names
to exact str; these unproved/custom cases fall back. Each potential skip rechecks
that result authority is disabled. Original conditional cell writes also remain
in the changed/atypical path.

No W/main edits, source execution, cap/error/test change or semantic-v25 composition
is authorized here. Root source inspection precedes any payload. The semantic lane
reports that its identical-object fast path is retained; combined-source evidence
must still verify that fact before composition, not assume it from this note.

The helper1050 assertion correction is independently reviewed as a distinct v5 test
candidate; neither its bytes nor any older failed receipt is changed by v29.
"""
account={"schema":"pontius-v29-production-name-accounting-v1","source_sha256":source_sha,
 "predecessor_sha256":PRE,"categories":full,"new_categories":sorted(added),
 "new_direct_original_budget_consumes":new_consumes,
 "guard_closure_freevars":list(helper.co_freevars),
 "classification":"Existing classifications retained; new input/history/name traversals and name-reference copies are P. All other new operations remain counted in full C as non-P.",
 "limits":["Logical semantic storage work, not CPU opcodes or allocator-perfect implementation internals.",
 "Dictionary attempts do not count hidden C collision equality probes individually.",
 "No fixed-category discount, budget refund, cap change, or runtime-improvement claim.",
 "Full original key-view/set union and eager order-memo work remain; history discovery still costs work on fallback.",
 "For atypical unchanged values the checked lookup is additional to the original per-name tuple; actual operations are not waived."]}
pres={"schema":"pontius-v29-storage-preservation-v1","source_sha256":source_sha,
 "predecessor_sha256":PRE,"all1761_W_paths_unchanged":True,"W_before":w_before,"W_after":w_after,
 "caps":caps,"protected_definitions":protected,"primitive_definitions_and_constants":primitive,
 "source_imported_or_executed":False,"W_written":False}
artifacts={
 "engineer-generator-v29-storage.py":raw,
 "engineer-generator-v29-storage-from-v28.diff":delta.encode(),
 "engineer-generator-v29-storage-accounting-v1.json":jd(account),
 "engineer-generator-v29-storage-preservation-v1.json":jd(pres),
 "coordinator-disabled-join-operation-disposition-v1.md":disposition.encode(),
}
static={"schema":"pontius-v29-storage-static-v1","source_sha256":source_sha,"source_bytes":len(raw),
 "predecessor_sha256":PRE,"plan_sha256":"d8faada0f14b1f7ffb0e0062ebd90e6fe196718b663cba93d39cd8246ff1b7fa",
 "exact_inverse_removal_recovers_every_v28_byte":True,
 "whole_module_AST_equal_except_one_merge_states_method":True,
 "original_full_fallback_prefix_and_body_AST_exact":True,
 "original_union_expression_AST_exact_occurrences":1,
 "original_per_name_supplied_merge_transfer_validation_conditional_cells_AST_exact":True,
 "original_identical_FlowValue_fast_path_AST_and_source_unchanged":True,
 "unchanged_other_SOR_methods":unchanged_methods,"unchanged_primitive_objects":47,
 "only_new_attribute_stores":writes,"no_no_work_writes_or_certificate_keywords":True,
 "new_name_charge_categories":len(added),"guard_closure_freevars":list(helper.co_freevars),
 "branch_first_line":inserted[0].lineno,"branch_last_line":inserted[-1].end_lineno,
 "fallback_resume_line":new_if.body[new_clear_index].lineno,
 "analysis_caps_unchanged":5,"all1761_W_paths_unchanged":True,
 "payload_executed":False,"source_imported":False,"syntax_compiled_only":True,
 "W_written":False,"generic_primitive_changed":False,"semantic_v25_combined":False,
 "artifacts":{name:sha(data) for name,data in artifacts.items()},
 "limits":["Static inspection is not runtime fitness or an independent cold-review verdict.",
 "No claim that common-history hit rate or total budget clears the remaining generator70 gate.",
 "The five-cap/refusal contract and every test byte remain unchanged by this source candidate.",
 "Independent semantic composition must reprove the identical-object merge law."]}
artifacts["engineer-generator-v29-storage-static-v1.json"]=jd(static)
note=f"""# v29 storage handoff: unexecuted

Source engineer-generator-v29-storage.py SHA256 {source_sha}; {len(raw)} bytes.
Only _merge_states changes from exact v28 {PRE}.
The normative operation-local approval is retained in
coordinator-disabled-join-operation-disposition-v1.md; the generic every-effectful-
transfer boundary remains unchanged.

At lines{inserted[0].lineno}-{inserted[-1].end_lineno}, eligible disabled/all-pending
common-history states retain checked unchanged entries. The exact original union
is calculated once. Changed or atypical names execute original tuple/merge/
transfer/name-validation/conditional-cell operations in the old union order.
A staged known order memo and fresh cursor publish only on completion. No generic
primitive, authority, cell, cap, error, test or other resolver method changed.
The original full body resumes at{new_if.body[new_clear_index].lineno} unchanged.
Exact list/tuple sources and exact string skipped names additionally exclude
unproved iterator/hash behavior from the optimization.

Inverse removal recovers every predecessor byte. Whole-module AST replacement
isolates the single method change; the original full-fallback body and ordered
per-name effect statements are exact. All47 primitive definitions/constants,
{unchanged_methods} other SOR methods and all1761 W tracked bytes remain unchanged.
The accounting artifact inventories {len(added)} new categories plus direct budget
guards and existing charges; no consumed work is refunded or cap increased.

Common-history success and whole budget improvement are not claimed before a new
root-controlled run. Prior v28 failures remain recorded; the separately reviewed
v5 assertion correction must be explicitly pinned by the controller. No payload,
W/main installation or semantic-v25 composition occurred during this authoring.
"""
artifacts["engineer-generator-v29-storage-handoff-v1.md"]=note.encode()
for path in artifacts:assert not (T/path).exists(),"Create-only output exists: "+path
for path,data in artifacts.items():
 with (T/path).open("xb") as f:f.write(data)
 assert (T/path).read_bytes()==data
print(json.dumps({"source_sha256":source_sha,"source_bytes":len(raw),
 "branch":[inserted[0].lineno,inserted[-1].end_lineno],
 "new_categories":len(added),"protected_other_methods":unchanged_methods,
 "files":{name:sha(data) for name,data in artifacts.items()}},indent=2))
