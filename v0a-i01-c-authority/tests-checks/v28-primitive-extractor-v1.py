"""Static-only v28 extraction verifier; import never executes a candidate or test.
Root may import this stdlib verifier inside its approved snapshot bootstrap.
The --author entrypoint only parses, compiles without execution, and creates artifacts.
"""
from __future__ import annotations

import ast
import builtins
import hashlib
import json
from pathlib import Path
import symtable
import sys

SOURCE_SHA = "4db6502350e59fe363998351384a62d9e669598241a644810e9a7ffd6b4b4d0e"
SUPPORT_SHA = "0c4e9ae2bef9b5489cc00f11adb5dd3400be6f6d5ea90537fb5951bba8ba1a71"
BINDING_SHA = "d786b9a609a37bf88ea18d6d6585d2ffb6cafd6ced908d23c1e086291ed8650c"
PRODUCTION_ACCOUNTING_SHA = "077c1b4779709672a79368ea1081ecd9cb0499c651851a571a80f075e983c45b"
OLD_ACCOUNTING_SHA = "79f64e5e7bbb429bedd108654b69c8ab5893973ee742517b543129f762f68f2b"
DEFINITIONS = (
    "_NameEntry", "_name_check_name", "_NameHistory", "_name_history",
    "_NameRadixLeaf", "_NameRadixBranch", "_NameLeafEdit", "_NameBranchEdit",
    "_name_radix_hash", "_name_radix_slot", "_name_radix_child", "_name_radix_lookup",
    "_name_radix_pending_count", "_name_radix_leaf", "_name_radix_seal_leaf",
    "_name_radix_copy_leaf", "_name_radix_records", "_name_radix_group",
    "_name_radix_edit_records", "_name_radix_edit", "_name_radix_freeze",
    "_name_radix_bulk", "_name_radix_names", "_NameOrder", "_name_order",
    "_name_known_order", "_name_seal_order_table", "_name_realize_order",
    "_name_charge_cache_commit", "_name_commit_order", "_name_keys",
    "_name_ordered_items", "_NameVersion", "_NamePublication",
    "_name_prepare_publication", "_name_charge_publication_commit",
    "_name_commit_publication", "_NameCursor", "_name_common_history",
    "_name_pending_names", "_join_name_versions",
)
CONSTANTS = ("_NAME_RADIX_BITS", "_NAME_LEAF_SIZE", "_NAME_HASH_WIDTH",
             "_NAME_HASH_MASK", "_NAME_MISSING", "_NAME_DELETED")
PUBLIC = {"Entry": "_NameEntry", "MISSING": "_NAME_MISSING",
          "NameVersion": "_NameVersion", "NameCursor": "_NameCursor",
          "join": "_join_name_versions", "_NameMeter": "Meter"}
SUPPORT = ("MAXIMUM_WORK", "BudgetExceeded", "Meter")
IMPORT_TEXT = ("from __future__ import annotations", "from dataclasses import dataclass",
               "from types import MappingProxyType", "import sys")
MAXIMUM = 262144


def req(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def dump(node):
    return ast.dump(node, include_attributes=False)


def top_name(node):
    if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
        return node.name
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        return node.targets[0].id
    return None


def source_piece(text, node):
    start = min([node.lineno] + [item.lineno for item in getattr(node, "decorator_list", ())])
    return "".join(text.splitlines(keepends=True)[start - 1:node.end_lineno]).rstrip("\n") + "\n"


def unique_top(tree, names):
    result = {}
    for node in tree.body:
        name = top_name(node)
        if name in names:
            req(name not in result, "duplicate selected top-level name: " + name)
            result[name] = node
    req(set(result) == set(names), "missing selected top-level names")
    return result


def derive(candidate_raw, support_raw, binding_raw, production_accounting_raw,
           old_accounting_raw):
    for raw, wanted, label in (
        (candidate_raw, SOURCE_SHA, "production candidate"),
        (support_raw, SUPPORT_SHA, "test-meter support reference"),
        (binding_raw, BINDING_SHA, "production binding proof"),
        (production_accounting_raw, PRODUCTION_ACCOUNTING_SHA, "production accounting"),
        (old_accounting_raw, OLD_ACCOUNTING_SHA, "prior accounting"),
    ):
        req(sha(raw) == wanted, label + " hash mismatch")
        req(b"\r" not in raw, label + " must use LF")
    source, reference = candidate_raw.decode("utf-8"), support_raw.decode("utf-8")
    source_tree, ref_tree = ast.parse(source), ast.parse(reference)
    selected = unique_top(source_tree, (*DEFINITIONS, *CONSTANTS))
    req(len(DEFINITIONS) == 41 and len(CONSTANTS) == 6, "primitive population")
    req(all(type(selected[name]).__name__ in {"ClassDef", "FunctionDef"} for name in DEFINITIONS),
        "primitive definition kind")
    req(all(type(selected[name]) is ast.Assign for name in CONSTANTS), "primitive constant kind")
    binding = json.loads(binding_raw)
    req(binding["candidate_sha256"] == SOURCE_SHA, "binding subject")
    req({row["candidate_name"] for row in binding["primitive_objects"]} == set(selected),
        "independent selection versus retained binding inventory")
    req(binding["candidate_shadowed_mapped_bindings"] == [], "retained binding audit differs")
    support = unique_top(ref_tree, SUPPORT)
    req(ast.literal_eval(support["MAXIMUM_WORK"].value) == MAXIMUM, "cap changed")
    imports = []
    for wanted in IMPORT_TEXT:
        target = ast.parse(wanted).body[0]
        matches = [node for node in ref_tree.body if dump(node) == dump(target)]
        req(len(matches) == 1, "support import mismatch: " + wanted)
        imports.append(source_piece(reference, matches[0]))
    pieces = ['"""Exact production v28 name primitive with separate original fault-injection meter.\n'
              'No analyzer, protected fixture or test body is present.\n'
              'Production SHA256: ' + SOURCE_SHA + '\n"""\n']
    pieces.extend(imports)
    pieces.extend(source_piece(reference, support[name]) for name in SUPPORT)
    ordered = sorted(selected.items(), key=lambda item: item[1].lineno)
    pieces.extend(source_piece(source, node) for _, node in ordered)
    pieces.extend(name + " = " + target + "\n" for name, target in PUBLIC.items())
    extracted_raw = ("\n".join(piece.rstrip("\n") for piece in pieces) + "\n").encode("utf-8")
    extracted_text = extracted_raw.decode("utf-8")
    extracted_tree = ast.parse(extracted_text)
    extracted = unique_top(extracted_tree, selected)
    primitive_proof = []
    for name, original in ordered:
        req(dump(original) == dump(extracted[name]), "production AST changed: " + name)
        primitive_proof.append({
            "name": name, "kind": type(original).__name__, "production_line": original.lineno,
            "extracted_line": extracted[name].lineno, "AST_sha256": sha(dump(original).encode()),
            "exact_AST_equal": True, "exact_source_segment_equal":
                source_piece(source, original) == source_piece(extracted_text, extracted[name]),
        })
        req(primitive_proof[-1]["exact_source_segment_equal"], "production source segment changed")
    extracted_support = unique_top(extracted_tree, SUPPORT)
    support_proof = []
    for name in SUPPORT:
        req(dump(support[name]) == dump(extracted_support[name]), "support AST changed")
        support_proof.append({"name": name, "exact_AST_equal": True,
                              "AST_sha256": sha(dump(support[name]).encode())})
    # Resolve global references without renaming any Name, Attribute, slot or local.
    table = symtable.symtable(extracted_text, "<v28-extraction>", "exec")
    available = {symbol.get_name() for symbol in table.get_symbols()
                 if symbol.is_assigned() or symbol.is_imported() or symbol.is_namespace()}
    global_refs = set()
    def collect(scope):
        for symbol in scope.get_symbols():
            if symbol.is_global() and symbol.is_referenced():
                global_refs.add(symbol.get_name())
        for child in scope.get_children():
            collect(child)
    collect(table)
    unresolved = sorted(global_refs - available - set(dir(builtins)))
    req(not unresolved, "unresolved extraction globals: " + repr(unresolved))
    forbidden = {"eval", "exec", "__import__", "compile", "open", "subprocess", "importlib"}
    req(not (global_refs & forbidden), "unexpected executable dependency")
    req("_ExecutionState" not in available and "_AnalysisBudget" not in available,
        "production adapter leaked into primitive extraction")
    # Static compilation only: never evaluate this code object.
    compile(extracted_text, "<v28-extracted-primitive>", "exec")
    charge_sites = {}
    for name, node in ordered:
        for call in ast.walk(node):
            if isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute) and call.func.attr == "charge":
                req(call.args and isinstance(call.args[0], ast.Constant)
                    and type(call.args[0].value) is str, "nonliteral primitive charge category")
                kind = call.args[0].value
                charge_sites.setdefault(kind, []).append({
                    "definition": name, "production_line": call.lineno,
                    "units_AST": dump(call.args[1]) if len(call.args) > 1 else "Constant(value=1)",
                })
    prod_accounting = json.loads(production_accounting_raw)
    old_accounting = json.loads(old_accounting_raw)
    req(prod_accounting["source_sha256"] == SOURCE_SHA, "production accounting subject")
    req(old_accounting["prototype_sha256"] == SUPPORT_SHA, "old accounting subject")
    new_kinds = set(prod_accounting["new_categories"])
    req(len(new_kinds) == 16 and new_kinds <= set(charge_sites), "new freeze accounting closure")
    req(set(charge_sites) == set(old_accounting["categories"]) | new_kinds,
        "primitive literal categories differ beyond declared sixteen")
    categories = {}
    for kind in sorted(charge_sites):
        item = prod_accounting["categories"][kind]
        req(item["metric"] in {"P", "non-P"} and type(item["operation"]) is str and item["operation"],
            "unclassified primitive category: " + kind)
        categories[kind] = {field: item[field] for field in ("metric", "operation")}
        if kind in old_accounting["categories"]:
            req(categories[kind] == old_accounting["categories"][kind],
                "prior category reclassified: " + kind)
    accounting = {key: value for key, value in old_accounting.items()
                  if key not in {"categories", "prototype_sha256", "prototype_path"}}
    accounting.update({
        "categories": categories, "prototype_sha256": sha(extracted_raw),
        "prototype_path": "v28-primitive-extracted-v1.py",
        "production_source_sha256": SOURCE_SHA,
        "production_accounting_sha256": PRODUCTION_ACCOUNTING_SHA,
        "support_reference_sha256": SUPPORT_SHA,
        "extraction_policy": "Identity production namespace; public aliases; exact original Meter support only.",
    })
    accounting_raw = encoded(accounting)
    proof = {
        "schema": "pontius-v28-primitive-extraction-proof-v1",
        "candidate_sha256": SOURCE_SHA, "support_reference_sha256": SUPPORT_SHA,
        "binding_sha256": BINDING_SHA, "production_accounting_sha256": PRODUCTION_ACCOUNTING_SHA,
        "old_accounting_sha256": OLD_ACCOUNTING_SHA, "extracted_sha256": sha(extracted_raw),
        "accounting_sha256": sha(accounting_raw),
        "definition_count": len(DEFINITIONS), "constant_count": len(CONSTANTS),
        "production_namespace_map": {name: name for name in selected},
        "public_alias_map": PUBLIC, "primitive_nodes": primitive_proof, "support_nodes": support_proof,
        "global_references": sorted(global_refs), "unresolved_globals": unresolved,
        "literal_charge_categories": len(charge_sites), "charge_sites": charge_sites,
        "new_categories": sorted(new_kinds), "old_category_mappings_unchanged": True,
        "all_primitive_ASTs_identical": True, "all_source_segments_identical": True,
        "attributes_slots_locals_untouched": True, "caps_unchanged": True,
        "static_compile_only": True, "candidate_imported_or_executed": False,
        "production_budget_adapter_extracted": False, "constructor_B_extracted": False,
    }
    return extracted_raw, accounting_raw, encoded(proof)


def verify_extraction(candidate_raw, support_raw, binding_raw, production_accounting_raw,
                      old_accounting_raw, extracted_raw, accounting_raw, proof_raw):
    actual = derive(candidate_raw, support_raw, binding_raw, production_accounting_raw,
                    old_accounting_raw)
    for supplied, regenerated, label in zip(
        (extracted_raw, accounting_raw, proof_raw), actual,
        ("extraction", "accounting", "proof"), strict=True,
    ):
        req(supplied == regenerated, label + " differs from deterministic static derivation")
    return {"candidate_sha256": SOURCE_SHA, "extracted_sha256": sha(extracted_raw),
            "accounting_sha256": sha(accounting_raw), "proof_sha256": sha(proof_raw),
            "production_nodes_verified": 47, "static_only": True}


def main():
    req(sys.argv[1:] == ["--author"], "only explicit static --author mode exists")
    req(sys.version_info[:3] == (3, 11, 15) and sys.flags.isolated
        and sys.flags.no_site and sys.flags.safe_path and sys.dont_write_bytecode,
        "static author interpreter/flags")
    root = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
    out = root / "tests-checks"
    arguments = [(root / name).read_bytes() for name in (
        "engineer-generator-v28-storage.py", "engineer-name-radix-prototype-v1.py",
        "engineer-generator-v28-storage-binding-proof-v1.json",
        "engineer-generator-v28-storage-accounting-v1.json",
        "engineer-name-radix-accounting-v1.json",
    )]
    results = derive(*arguments)
    names = ("v28-primitive-extracted-v1.py", "v28-primitive-accounting-v1.json",
             "v28-primitive-extraction-proof-v1.json")
    req(not any((out / name).exists() for name in names), "issued artifact already exists")
    verification = verify_extraction(*arguments, *results)
    for name, raw in zip(names, results, strict=True):
        with (out / name).open("xb") as stream:
            stream.write(raw)
    print(json.dumps({"static_authoring_only": True, "payload_executed": False,
                      "verification": verification,
                      "artifacts": {name: {"sha256": sha(raw), "bytes": len(raw)}
                                    for name, raw in zip(names, results, strict=True)}}, indent=2))


if __name__ == "__main__":
    main()
