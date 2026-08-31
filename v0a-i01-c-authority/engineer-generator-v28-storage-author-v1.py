import ast
import copy
import difflib
import hashlib
import json
import subprocess
import symtable
from pathlib import Path

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
W = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
GIT = r"C:\Program Files\Git\cmd\git.exe"
PRE = "1f908957ee43d5841f8da09e306bd52dc5efeca9609a5d522e76df22b4dcd951"
PROTO = "0c4e9ae2bef9b5489cc00f11adb5dd3400be6f6d5ea90537fb5951bba8ba1a71"
PLAN = "e32d45c914cf9422429f493b3dfec475e23d05d58f957dca896ec95b75bb2d93"
CLARIFY = "7a4e338e5ed990df6cfa2d850638833362036558f649ae626ea0e0472239fce5"
BASE = "29c02f6fbd5eb0b7ddc9e816ef28f570b9839358"

def sha(b): return hashlib.sha256(b).hexdigest()
def pinned(name, wanted):
    b = (T/name).read_bytes()
    assert sha(b) == wanted, (name, sha(b), wanted)
    return b
def dump(value): return ast.dump(value, include_attributes=False)
def jb(value): return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")
def span(source, node): return ast.get_source_segment(source, node)
def top(tree, name):
    return next(n for n in tree.body if getattr(n, "name", None) == name)
def method(tree, cls, name):
    return next(n for n in top(tree, cls).body if getattr(n, "name", None) == name)
def assignment_name(node):
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        return node.targets[0].id
    return None
def assignment(tree, name):
    return next(n for n in tree.body if assignment_name(n) == name)
def exact_def(source, tree, name):
    n = top(tree, name)
    return source.splitlines(keepends=True)[n.lineno-1:n.end_lineno]

old_bytes = pinned("engineer-generator-v26-storage.py", PRE)
old = old_bytes.decode("utf-8")
assert b"\r" not in old_bytes
prototype = pinned("engineer-name-radix-prototype-v1.py", PROTO).decode("utf-8")
pinned("engineer-v26-cost-remedy-plan-v1.md", PLAN)
pinned("engineer-v26-cost-remedy-clarification-v2.md", CLARIFY)
binding_bytes = pinned("engineer-generator-v26-storage-binding-map-v1.json", "e024329a9dcae92c22b3185f62543bbcd1ec535cbfdf5aba01e930fd67f22d10")
accounting_bytes = pinned("engineer-name-radix-accounting-v1.json", "79f64e5e7bbb429bedd108654b69c8ab5893973ee742517b543129f762f68f2b")
old_static = json.loads(pinned("engineer-generator-v26-storage-static-v1.json", "d30ab3307f7dc11ce978ac045beaca676868000b3d795ab88b31d3a8cf1e2e71"))
mapping = json.loads(binding_bytes)["global_binding_map"]
original_accounting = json.loads(accounting_bytes)
assert len(old_static["w_after"]) == 1761
w_before = {name: sha((W/name).read_bytes()) for name in old_static["w_after"]}
assert w_before == old_static["w_after"], "W changed since retained v26 proof"
assert w_before["tools/generate_test_inventory.py"] == "e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679"

old_tree = ast.parse(old)
proto_tree = ast.parse(prototype)
old_freeze = span(old, top(old_tree, "_name_radix_freeze"))
old_init = span(old, method(old_tree, "_SourceOrderedResolver", "__init__"))
old_update = "        self.values.update(entry_values or {})"
assert old_init.count(old_update) == 1
assert old.count(old_freeze) == 1
new_freeze = "def _name_radix_freeze(meter, node):\n    \"\"\"Freeze owned paths only; unchanged immutable siblings remain shared.\"\"\"\n    meter.charge(\"radix_freeze_node_visits\")\n    if node is None or isinstance(node, (_NameRadixLeaf, _NameRadixBranch)):\n        return node\n    if isinstance(node, _NameLeafEdit):\n        return _name_radix_seal_leaf(meter, node.data)\n    meter.charge(\"radix_freeze_base_reads\")\n    base = node.base\n    meter.charge(\"radix_child_list_allocation\")\n    if base is None:\n        children, bitmap, pending_count = [], 0, 0\n        for slot in range(16):\n            meter.charge(\"radix_freeze_slot_visits\")\n            meter.charge(\"radix_editor_dictionary_attempts\")\n            child = node.changes.get(slot, _NAME_MISSING)\n            if child is _NAME_MISSING:\n                child = _name_radix_child(meter, node.base, slot)\n            else:\n                child = _name_radix_freeze(meter, child)\n            if child is not None:\n                bitmap |= 1 << slot\n                pending_count += _name_radix_pending_count(meter, child)\n                meter.charge(\"radix_child_list_reference_copies\")\n                children.append(child)\n    else:\n        # All edits stay private. Each old child comes from the immutable base;\n        # only packed-list ranks follow the evolving working bitmap.\n        meter.charge(\"radix_freeze_base_metadata_reads\", 3)\n        base_bitmap, base_children, pending_count = base.bitmap, base.children, base.pending_count\n        bitmap = base_bitmap\n        meter.charge(\"radix_freeze_base_child_size_reads\")\n        meter.charge(\"radix_freeze_base_child_reference_copies\", len(base_children))\n        children = list(base_children)\n        meter.charge(\"radix_freeze_change_view_and_iterator_allocations\", 2)\n        for slot, replacement in node.changes.items():\n            meter.charge(\"radix_freeze_changed_slot_visits\")\n            bit = 1 << slot\n            meter.charge(\"radix_freeze_base_slot_tests\")\n            if base_bitmap & bit:\n                meter.charge(\"radix_child_index_operations\")\n                old_index = (base_bitmap & (bit - 1)).bit_count()\n                meter.charge(\"radix_child_reference_visits\")\n                old_child = base_children[old_index]\n            else:\n                old_child = None\n            child = _name_radix_freeze(meter, replacement)\n            old_pending = _name_radix_pending_count(meter, old_child)\n            new_pending = _name_radix_pending_count(meter, child)\n            meter.charge(\"radix_freeze_pending_delta_operations\", 2)\n            pending_count += new_pending - old_pending\n            meter.charge(\"radix_freeze_working_bitmap_reads\")\n            present = bool(bitmap & bit)\n            meter.charge(\"radix_freeze_working_rank_operations\")\n            index = (bitmap & (bit - 1)).bit_count()\n            if child is None:\n                if present:\n                    meter.charge(\"radix_freeze_child_delete_operations\")\n                    meter.charge(\"radix_freeze_working_child_size_reads\")\n                    meter.charge(\"radix_freeze_child_shift_reference_copies\", len(children) - index - 1)\n                    del children[index]\n                    meter.charge(\"radix_freeze_working_bitmap_writes\")\n                    bitmap &= ~bit\n            elif present:\n                meter.charge(\"radix_freeze_child_replace_operations\")\n                meter.charge(\"radix_child_list_reference_copies\")\n                children[index] = child\n            else:\n                meter.charge(\"radix_freeze_child_insert_operations\")\n                meter.charge(\"radix_freeze_working_child_size_reads\")\n                meter.charge(\"radix_freeze_child_shift_reference_copies\", len(children) - index)\n                meter.charge(\"radix_child_list_reference_copies\")\n                children.insert(index, child)\n                meter.charge(\"radix_freeze_working_bitmap_writes\")\n                bitmap |= bit\n    if not children:\n        return None\n    meter.charge(\"radix_child_tuple_allocation\")\n    meter.charge(\"radix_child_tuple_reference_copies\", len(children))\n    frozen = tuple(children)\n    meter.charge(\"radix_branch_allocation\")\n    meter.charge(\"radix_branch_field_reference_copies\", 3)\n    return _NameRadixBranch(bitmap, frozen, pending_count)"
new_splice = "        # Earlier setup is unchanged. Borrow only across the proved zero-write\n        # lexical window; the final ExecutionState constructor still forks.\n        self.budget.consume()  # Exact prepared mapping type check.\n        borrow_entry = type(self.values) is dict\n        if borrow_entry:\n            self.budget.consume()  # Prepared dictionary length read.\n            borrow_entry = not self.values\n        if borrow_entry:\n            self.budget.consume()  # Exact entry wrapper type check.\n            borrow_entry = type(entry_values) is _ExecutionState\n        if borrow_entry:\n            self.budget.consume()  # Exact lexical-scope type check.\n            borrow_entry = type(self.lexical_scope) is _LexicalBindingScope\n        if borrow_entry:\n            self.budget.consume()  # Registry type and ordinary-dict test.\n            registry_type = type(self.helper_registry)\n            if registry_type is not dict:\n                self.budget.consume()  # The one other nonreentrant registry type.\n                borrow_entry = registry_type is _ReviewRegistry\n        if borrow_entry:\n            self.budget.consume(4)  # Binding-set tuple and its three references.\n            binding_sets = (\n                self.lexical_scope.local_names,\n                self.lexical_scope.nonlocal_names,\n                self.lexical_scope.global_names,\n            )\n            for binding_names in binding_sets:\n                self.budget.consume(2)  # Set visit and exact type check.\n                if type(binding_names) is not frozenset:\n                    borrow_entry = False\n                    break\n                self.budget.consume()  # Empty-set check.\n                if binding_names:\n                    borrow_entry = False\n                    break\n        if borrow_entry:\n            # Preserve the original source truthiness exactly once. Falsey entry\n            # names keep the old detached construction, with the same parent.\n            if entry_values:\n                self.budget.consume()  # Borrow the exact name-input reference.\n                self.values = entry_values\n            else:\n                self.values.update({})\n        else:\n            self.values.update(entry_values or {})"
new_init = old_init.replace(old_update, new_splice)
candidate = old.replace(old_freeze, new_freeze).replace(old_init, new_init)
candidate_bytes = candidate.encode("utf-8")
candidate_sha = sha(candidate_bytes)
tree = ast.parse(candidate)
# No source/prototype import or execution. Parsing plus compile-to-code is syntax only.
compile(tree, "engineer-generator-v28-storage.py", "exec", dont_inherit=True)
assert candidate.count(new_freeze) == 1
assert candidate.count(new_init) == 1
inverse = candidate.replace(new_freeze, old_freeze).replace(new_init, old_init)
assert inverse.encode("utf-8") == old_bytes

# Whole-module comparison after replacing only the two authorized AST nodes.
inverse_tree = copy.deepcopy(tree)
for i, n in enumerate(inverse_tree.body):
    if getattr(n, "name", None) == "_name_radix_freeze":
        inverse_tree.body[i] = copy.deepcopy(top(old_tree, "_name_radix_freeze"))
sor = top(inverse_tree, "_SourceOrderedResolver")
for i, n in enumerate(sor.body):
    if getattr(n, "name", None) == "__init__":
        sor.body[i] = copy.deepcopy(method(old_tree, "_SourceOrderedResolver", "__init__"))
assert dump(inverse_tree) == dump(old_tree)

# Original new-branch loop and publication suffix remain exactly the same AST.
old_freeze_ast = top(old_tree, "_name_radix_freeze")
new_freeze_ast = top(tree, "_name_radix_freeze")
old_slot_loop = next(n for n in old_freeze_ast.body if isinstance(n, ast.For))
new_branch_if = next(n for n in new_freeze_ast.body
                     if isinstance(n, ast.If) and isinstance(n.test, ast.Compare)
                     and isinstance(n.test.left, ast.Name) and n.test.left.id == "base")
assert dump(old_slot_loop) == dump(next(n for n in new_branch_if.body if isinstance(n, ast.For)))
old_suffix = old_freeze_ast.body[old_freeze_ast.body.index(old_slot_loop)+1:]
new_suffix = new_freeze_ast.body[new_freeze_ast.body.index(new_branch_if)+1:]
assert [dump(n) for n in old_suffix] == [dump(n) for n in new_suffix]
assert not any(isinstance(n, ast.Attribute) and isinstance(n.ctx, (ast.Store, ast.Del))
               for n in ast.walk(new_freeze_ast)), "freeze mutates a published attribute"

# Verify B changes exactly the original update site; every following statement,
# including the final ExecutionState call, is unchanged.
old_init_ast = method(old_tree, "_SourceOrderedResolver", "__init__")
new_init_ast = method(tree, "_SourceOrderedResolver", "__init__")
def is_old_update(n):
    return isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) and (
        isinstance(n.value.func, ast.Attribute) and n.value.func.attr == "update"
        and isinstance(n.value.func.value, ast.Attribute)
        and n.value.func.value.attr == "values")
update_index = [i for i,n in enumerate(old_init_ast.body) if is_old_update(n)][-1]
assert span(old, old_init_ast.body[update_index]) == old_update.strip()
post_old = old_init_ast.body[update_index+1:]
post_new = new_init_ast.body[-len(post_old):]
assert [dump(n) for n in post_old] == [dump(n) for n in post_new]
assert [dump(n) for n in old_init_ast.body[:update_index]] == [dump(n) for n in new_init_ast.body[:update_index]]
changed_block = new_init_ast.body[update_index:len(new_init_ast.body)-len(post_old)]
assert len(changed_block) > 1
window = post_new[:-1]
loop_names = []
for n in window:
    assert isinstance(n, ast.For), ast.dump(n)
    assert isinstance(n.iter, ast.Attribute)
    loop_names.append(n.iter.attr)
assert loop_names == ["local_names", "nonlocal_names", "global_names"]
assert isinstance(post_new[-1], ast.Assign)
assert isinstance(post_new[-1].value, ast.Call)
assert isinstance(post_new[-1].value.func, ast.Name)
assert post_new[-1].value.func.id == "_ExecutionState"

# Binding-aware canonicalization: names may change only if the complete lexical
# audit proves the mapped spelling is global, never a shadowing local/free name.
def nonglobal_bindings(source, names):
    result = []
    def walk(table, path):
        if table.get_type() != "module":
            for symbol in table.get_symbols():
                if symbol.get_name() in names and not symbol.is_global():
                    result.append({"scope": path, "name": symbol.get_name(),
                                   "local": symbol.is_local(), "free": symbol.is_free(),
                                   "parameter": symbol.is_parameter()})
        for child in table.get_children():
            walk(child, path + "." + child.get_name())
    walk(symtable.symtable(source, "<static>", "exec"), "module")
    return result
prototype_shadow = nonglobal_bindings(prototype, set(mapping))
candidate_shadow = nonglobal_bindings(candidate, set(mapping.values()))
assert prototype_shadow == [] and candidate_shadow == []
class GlobalNames(ast.NodeTransformer):
    def __init__(self, name_map): self.name_map = name_map
    def visit_Name(self, node):
        node.id = self.name_map.get(node.id, node.id)
        return node
def canonical(node, name_map):
    result = GlobalNames(name_map).visit(copy.deepcopy(node))
    if isinstance(result, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        result.name = name_map.get(result.name, result.name)
    return result
primitive_defs = [n for n in proto_tree.body
                  if isinstance(n, (ast.FunctionDef, ast.ClassDef))
                  and getattr(n, "name", None) in mapping and n.name != "Meter"]
primitive_constants = [n for n in proto_tree.body if assignment_name(n) in mapping]
assert len(primitive_defs) == 41 and len(primitive_constants) == 6
primitive_rows = []
for n in primitive_defs + primitive_constants:
    name = getattr(n, "name", None) or assignment_name(n)
    actual = top(tree, mapping[name]) if hasattr(n, "name") else assignment(tree, mapping[name])
    expected = canonical(n, mapping)
    equal = dump(expected) == dump(actual)
    assert equal == (name != "_radix_freeze"), name
    primitive_rows.append({"prototype_name": name, "candidate_name": mapping[name],
        "kind": type(n).__name__, "equal_to_binding_aware_reference": equal,
        "prototype_AST_sha256": sha(dump(n).encode()),
        "candidate_AST_sha256": sha(dump(actual).encode()),
        "candidate_line": actual.lineno})
# No member spelling, slots, reflective strings or class body changed from v26.
primitive_classes = [n for n in primitive_defs if isinstance(n, ast.ClassDef)]
member_layout = []
for n in primitive_classes:
    a = top(old_tree, mapping[n.name]); b = top(tree, mapping[n.name])
    assert dump(a) == dump(b)
    original_members = [(x.attr, type(x.ctx).__name__) for x in ast.walk(n) if isinstance(x, ast.Attribute)]
    actual_members = [(x.attr, type(x.ctx).__name__) for x in ast.walk(b) if isinstance(x, ast.Attribute)]
    original_strings = [x.value for x in ast.walk(n) if isinstance(x, ast.Constant) and isinstance(x.value,str)]
    actual_strings = [x.value for x in ast.walk(b) if isinstance(x, ast.Constant) and isinstance(x.value,str)]
    assert original_members == actual_members and original_strings == actual_strings
    member_layout.append({"prototype_class": n.name, "candidate_class": mapping[n.name],
        "class_AST_unchanged_from_v26": True, "members_and_literal_strings_equal_prototype": True,
        "validated_v26_slot_inventory": old_static["slot_reference"][n.name]})
backmap = {v:k for k,v in mapping.items()}
freeze_reference = top(proto_tree, "_radix_freeze")
freeze_back = canonical(new_freeze_ast, backmap)
primitive_diff = "".join(difflib.unified_diff(
    (ast.unparse(freeze_reference)+"\n").splitlines(True),
    (ast.unparse(freeze_back)+"\n").splitlines(True),
    fromfile="prototype/_radix_freeze (AST presentation)",
    tofile="v28/_radix_freeze (binding-aware inverse AST presentation)"))

# Preserve every old cap and all outer semantics; no C/semantic-v25 patch.
caps = {assignment_name(n): span(old,n) for n in old_tree.body
        if assignment_name(n) and assignment_name(n).startswith("MAXIMUM_ANALYSIS_")}
assert len(caps) == 5, caps
for name in caps:
    assert dump(assignment(old_tree,name)) == dump(assignment(tree,name))
protected = {}
for name in ["_AnalysisBudget", "_NameMeter", "_transfer_authority", "_ExecutionState",
             "_AuthorityMap", "_AuthorityState", "_ObservedAuthorityMap"]:
    a=top(old_tree,name); b=top(tree,name)
    assert dump(a)==dump(b)
    assert span(old,a)==span(candidate,b)
    protected[name]={"AST_sha256":sha(dump(b).encode()),"source_sha256":sha(span(candidate,b).encode())}
for cls,name in [("_SourceOrderedResolver","_merge_states"),("_ExecutionState","_write_cells")]:
    a=method(old_tree,cls,name);b=method(tree,cls,name)
    assert dump(a)==dump(b) and span(old,a)==span(candidate,b)
    protected[cls+"."+name]={"AST_sha256":sha(dump(b).encode()),"source_sha256":sha(span(candidate,b).encode())}

def charge_inventory(root):
    out={}
    class Visitor(ast.NodeVisitor):
        def __init__(self): self.scope=[]
        def visit_ClassDef(self,n):
            self.scope.append(n.name); self.generic_visit(n); self.scope.pop()
        def visit_FunctionDef(self,n):
            self.scope.append(n.name); self.generic_visit(n); self.scope.pop()
        visit_AsyncFunctionDef=visit_FunctionDef
        def visit_Call(self,n):
            if isinstance(n.func, ast.Attribute) and n.func.attr=="charge":
                assert n.args and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str), ast.dump(n)
                out.setdefault(n.args[0].value,[]).append({"function":".".join(self.scope),
                    "line":n.lineno,"units":ast.unparse(n.args[1]) if len(n.args)>1 else "1"})
            self.generic_visit(n)
    Visitor().visit(root)
    return out
old_charges=charge_inventory(old_tree)
new_charges=charge_inventory(tree)
new_categories=set(new_charges)-set(old_charges)
assert set(old_charges) <= set(new_charges)
new_operations={
 "radix_freeze_base_reads": ("non-P","Read the editor's immutable base once."),
 "radix_freeze_base_metadata_reads": ("non-P","Read cached base bitmap, packed children and pending total, three fields."),
 "radix_freeze_base_child_size_reads": ("non-P","Read the packed tuple size before staging its copy."),
 "radix_freeze_base_child_reference_copies": ("P","Copy every base packed-child reference once into the unpublished list."),
 "radix_freeze_change_view_and_iterator_allocations": ("non-P","Create the changes-dictionary items view and traversal iterator, two objects."),
 "radix_freeze_changed_slot_visits": ("P","Visit one actual changed-slot dictionary entry."),
 "radix_freeze_base_slot_tests": ("non-P","Test one changed slot against the original cached bitmap."),
 "radix_freeze_pending_delta_operations": ("non-P","Subtract old child pending count and add new count, two operations."),
 "radix_freeze_working_bitmap_reads": ("non-P","Test current slot presence in the evolving packed-list bitmap."),
 "radix_freeze_working_rank_operations": ("non-P","Compute current packed-list rank from the evolving bitmap."),
 "radix_freeze_child_delete_operations": ("non-P","One staged packed-list deletion operation."),
 "radix_freeze_child_replace_operations": ("non-P","One staged packed-list replacement operation."),
 "radix_freeze_child_insert_operations": ("non-P","One staged packed-list insertion operation."),
 "radix_freeze_child_shift_reference_copies": ("P","Charge each list reference shifted by insertion or deletion."),
 "radix_freeze_working_bitmap_writes": ("non-P","Update the evolving bitmap after insertion or deletion."),
 "radix_freeze_working_child_size_reads": ("non-P","Read staged list size to calculate actual shifted references."),
}
assert new_categories==set(new_operations), (new_categories,set(new_operations))
full_categories={}
for name,sites in new_charges.items():
    if name in original_accounting["categories"]:
        old_category=original_accounting["categories"][name]
        full_categories[name]={"metric":old_category["metric"],
                              "operation":old_category["operation"],
                              "origin":"unchanged prototype classification","source_sites":sites}
    elif name in new_operations:
        metric,operation=new_operations[name]
        full_categories[name]={"metric":metric,"operation":operation,
                              "origin":"v28 A existing-branch freeze","source_sites":sites}
    else:
        # Existing production-only NameMeter operations are retained, not added by v28.
        assert name in old_charges
        full_categories[name]={"metric":None,"operation":"Existing production adapter category; not classified by the isolated primitive P metric.",
                              "origin":"unchanged production adapter","source_sites":sites}
b_consumes=[]
for n in changed_block:
    for c in ast.walk(n):
        if isinstance(c,ast.Call) and isinstance(c.func,ast.Attribute) and c.func.attr=="consume":
            b_consumes.append({"line":c.lineno,"units":ast.unparse(c.args[0]) if c.args else "1",
                              "call":span(candidate,c)})
b_consumes.sort(key=lambda x:x["line"])
assert len(b_consumes)==10, b_consumes

# Original base source is read as bytes only; no checkout or mutation.
r010=subprocess.run([GIT,"-C",str(W),"show",BASE+":tools/generate_test_inventory.py"],
                    check=True,capture_output=True).stdout
assert sha(r010)=="29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692"
delta="".join(difflib.unified_diff(old.splitlines(True),candidate.splitlines(True),
    fromfile="engineer-generator-v26-storage.py",tofile="engineer-generator-v28-storage.py"))
full="".join(difflib.unified_diff(r010.decode().splitlines(True),candidate.splitlines(True),
    fromfile=BASE+"/tools/generate_test_inventory.py",tofile="engineer-generator-v28-storage.py"))
assert pinned("engineer-generator-v26-storage.py",PRE)==old_bytes
w_after={name:sha((W/name).read_bytes()) for name in w_before}
assert w_after==w_before
preservation={"schema":"pontius-v28-storage-preservation-v1","candidate_sha256":candidate_sha,
 "source_predecessor_sha256":PRE,"W_path":str(W),"tracked_keys":1761,
 "W_before":w_before,"W_after":w_after,"all_unchanged":True,
 "all_five_analysis_caps":caps,"protected_definitions":protected,
 "candidate_or_tests_imported_or_executed":False,"W_written":False}
binding_report={"schema":"pontius-v28-storage-binding-proof-v1",
 "candidate_sha256":candidate_sha,"prototype_sha256":PROTO,"predecessor_sha256":PRE,
 "global_binding_map":mapping,"policy":"Transform declarations and ast.Name global bindings only after a full lexical audit. Never transform Attribute.attr, slots, strings, parameters or keywords.",
 "prototype_shadowed_mapped_bindings":prototype_shadow,
 "candidate_shadowed_mapped_bindings":candidate_shadow,
 "primitive_objects":primitive_rows,"definitions":41,"constants":6,
 "unchanged_definitions":40,"intentional_changed_definition":"_radix_freeze",
 "class_member_and_slot_proofs":member_layout,
 "all_class_bodies_unchanged":True,
 "remaining_members_outside_the_freeze_function_unchanged":True}
accounting_report={"schema":"pontius-v28-production-name-accounting-v1",
 "source_sha256":candidate_sha,"source_path":str(T/"engineer-generator-v28-storage.py"),
 "prototype_accounting_sha256":sha(accounting_bytes),
 "categories":full_categories,
 "new_categories":sorted(new_categories),
 "new_B_direct_original_budget_consumes":b_consumes,
 "B_guard_accounting":"Sequential guards pay only when reached. Tuple allocation plus three retained set references costs4; each set visit/type check2, then emptiness1; source truthiness delegates the unchanged exact ExecutionState len meter; final existing forks retain all charges.",
 "limits":["Semantic storage units are explicit traversals/reference copies/dictionary attempts, not CPU opcodes or allocator-perfect implementation internals.",
           "Leaf dictionary internal hash/equality probes remain outside one logical dictionary-attempt unit; collision semantics and existing charges unchanged.",
           "Production-only preexisting categories are marked with metric null, not silently assigned the prototype P classification.",
           "No charges removed from unchanged operations, caps unchanged, actual runtime and whole-analyzer fitness unmeasured."],
 "publication":"All fresh child lists, tuples, frozen descendants and counts remain unpublished until original preparation/commit code succeeds. Changed slots use immutable old children and evolving current ranks."}
artifacts={
 "engineer-generator-v28-storage.py":candidate_bytes,
 "engineer-generator-v28-storage-from-v26.diff":delta.encode(),
 "engineer-generator-v28-storage-from-r010.diff":full.encode(),
 "engineer-generator-v28-storage-primitive-from-reference.diff":primitive_diff.encode(),
 "engineer-generator-v28-storage-preservation-v1.json":jb(preservation),
 "engineer-generator-v28-storage-binding-proof-v1.json":jb(binding_report),
 "engineer-generator-v28-storage-accounting-v1.json":jb(accounting_report),
}
artifact_pins={name:sha(data) for name,data in artifacts.items()}
report={"schema":"pontius-v28-storage-static-v1","source_sha256":candidate_sha,
 "source_bytes":len(candidate_bytes),"predecessor_sha256":PRE,"prototype_sha256":PROTO,
 "plan_sha256":PLAN,"clarification_sha256":CLARIFY,
 "measured_RED_verification_sha256":"2e729e903ed0f0c869e88aa595d62bc0da5a2f3a47d29962f901a4865a87bf30",
 "authorized_changes":["A: existing-base radix freeze staging; original new-base loop retained",
                       "B: guarded late exact entry borrow through zero-write lexical window"],
 "exact_inverse_recovers_v26":True,"whole_module_AST_equal_after_reversing_only_A_and_B":True,
 "new_branch_loop_AST_unchanged":True,"freeze_common_return_suffix_AST_unchanged":True,
 "freeze_contains_no_attribute_store_or_delete":True,
 "B_earlier_setup_AST_unchanged":True,"B_following_lexical_loops_and_final_fork_AST_unchanged":True,
 "B_following_lexical_loop_names":loop_names,
 "A_line":new_freeze_ast.lineno,"B_first_line":changed_block[0].lineno,
 "B_final_constructor_line":post_new[-1].lineno,
 "protected_definitions":protected,"analysis_caps_unchanged":len(caps),
 "new_name_categories":sorted(new_categories),"new_B_consume_sites":len(b_consumes),
 "binding_aware_primitive_equal_definitions":40,"binding_aware_primitive_equal_constants":6,
 "all1761_W_paths_unchanged":True,
 "source_parsed_and_syntax_compiled_only":True,"source_imported_or_executed":False,
 "payload_executed":False,"W_written":False,"C_implemented":False,"semantic_v25_combined":False,
 "helper1050_contract_nuance":"Original4949 accepts analysis.*(?:depth|budget); unchanged work exception says analysis work units exceed262144 (spacing preserved in source), and original20587 requires that wording. Do not infer that helper1050 must reach depth. No test, regex or error wording changed; root owns the contract reconciliation.",
 "limitations":["Static proof is not runtime validation. Existing design53 must run first after root inspection.",
                "Existing primitive order/collision/retention/atomicity requirements still need verification against changed freeze; prior558 checks bind the prior primitive only.",
                "Generator70 full disabled joins remain unchanged; C utility and whole generation success are unproven."],
 "artifacts":artifact_pins}
artifacts["engineer-generator-v28-storage-static-v1.json"]=jb(report)
note=f"""# v28 storage candidate: A+B only, unexecuted

Candidate engineer-generator-v28-storage.py SHA256 {candidate_sha}.
Exact predecessor v26 SHA256 {PRE}.
Scope binds remedy plan {PLAN} and clarification {CLARIFY}.
Measured RED binds coordinator-v26-depth-budget-verification-v1.json
2e729e903ed0f0c869e88aa595d62bc0da5a2f3a47d29962f901a4865a87bf30.

## A: immutable-base freeze

At candidate line{new_freeze_ast.lineno}, existing immutable branches stage one packed
child list from the base and visit actual changed slots. Original base children
supply each old pending count once; cached base total receives only old/new deltas.
The evolving bitmap supplies insertion/deletion ranks, keeping ascending slot order
despite arbitrary changed-slot insertion order. Every shifted/stored reference,
list/tuple allocation, changed-entry visit, pending read and rank/bitmap operation
is charged. The new-branch sixteen-slot loop and common immutable return suffix
remain unchanged. No published node, cursor, history or order cache is mutated.
Failure before the unchanged commit boundary leaves only unreachable staged work;
there is no partial cache publication or retry refund.

## B: late identity-preserving borrow

At candidate line{changed_block[0].lineno}, all preceding resolver setup remains exact.
The guarded case requires exact empty prepared dict, exact ExecutionState entry,
exact LexicalBindingScope, three exact empty frozensets and an exact dict or
ReviewRegistry registry. Registry subclasses/custom mappings stay on the original
expression. These guards are sequential and charged.

Eligible source truthiness is evaluated once. Only nonempty entries are borrowed
through the three now-proven inactive loops. At line{post_new[-1].lineno}, the original
ExecutionState call still forks parent authority/bindings and names; caller wrapper
ownership never transfers. Falsey entry names retain detached construction while
parent authority/bindings still follow the old constructor. No Entry proof/pending
flag, transfer, cell write or preparation effect is newly omitted.

## Static evidence and remaining work

The exact inverse recovers every predecessor byte. Reversing only A and B recovers
the whole original AST. Forty primitive definitions and six constants remain equal
to the reviewed primitive under global-binding-only namespacing. The sole primitive
delta is freeze; all primitive class members and slot strings remain unchanged.
AnalysisBudget, NameMeter, transfer, cell writes, all ExecutionState methods,
full/sparse merges and every other resolver method are unchanged. All five caps and
all1761 W tracked bytes are preserved.

The accounting inventory distinguishes newly charged A operations, unchanged
prototype classifications, existing adapter-only categories and B's direct original
budget guard charges. It measures semantic storage work, not CPU instructions or
hidden C dictionary equality probes. No savings/runtime prediction is asserted.

Helper1050 original4949 accepts analysis.*(?:depth|budget), but the existing work
exception says "analysis work units exceed 262144", also required at original20587.
That is a possible assertion/error-category conflict, not proof helper1050 must
reach depth. No test, regex, refusal wording or cap changed. Root handles that
contract separately. Generator70's exact depth64 obligation and full-merge work
remain; C is deliberately absent.

No W install, main edit, semantic-v25 merge, candidate import or payload execution
occurred. Root source review is next, then the original design53 first; unchanged
primitive requirements follow to verify altered freeze mechanics. Prior558 primitive
passes do not establish v28 or whole-analyzer fitness.

Artifacts: exact v26/r010 diffs; binding-aware primitive delta; preservation,
binding, accounting and static JSON under the engineer-generator-v28-storage prefix.
"""
artifacts["engineer-generator-v28-storage-handoff-v1.md"]=note.encode()
for name in artifacts:
    assert not (T/name).exists(), "create-only target exists: "+name
for name,data in artifacts.items():
    with (T/name).open("xb") as f:
        f.write(data)
    assert (T/name).read_bytes()==data
print(json.dumps({"source_sha256":candidate_sha,"source_bytes":len(candidate_bytes),
 "A_line":new_freeze_ast.lineno,"B_line":changed_block[0].lineno,
 "B_final_constructor_line":post_new[-1].lineno,
 "written":{name:sha(data) for name,data in artifacts.items()},
 "new_categories":len(new_categories),"W_unchanged_paths":1761},indent=2))
