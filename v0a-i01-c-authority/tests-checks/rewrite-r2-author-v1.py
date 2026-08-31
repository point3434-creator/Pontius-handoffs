import ast,difflib,hashlib,json,subprocess,sys
from pathlib import Path
T=Path(r"D:\Pontius-handoffs\v0a-i01-c-authority"); C=T/"tests-checks"
assert sys.version_info[:3]==(3,11,15)
def sha(raw): return hashlib.sha256(raw).hexdigest()
def dump(obj): return (json.dumps(obj,indent=2,sort_keys=True,allow_nan=False)+"\n").encode()
def top(src,name):
 return next(n for n in ast.parse(src).body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name)
def segment(src,name): return ast.get_source_segment(src,top(src,name))+"\n"
def replace_top(src,name,new):
 n=top(src,name); lines=src.splitlines(True)
 return "".join(lines[:n.lineno-1])+new.rstrip()+"\n"+"".join(lines[n.end_lineno:])
def once(src,old,new):
 assert src.count(old)==1,(old,src.count(old))
 return src.replace(old,new)
def read(name,pin):
 raw=(T/name).read_bytes(); assert sha(raw)==pin,(name,sha(raw)); return raw.decode()
def create(name,raw):
 with (C/name).open("xb") as f: f.write(raw)
r1_probe=read("tests-checks/rewrite-r1-probe-v1.py","c0672ac61fa19b5dd3d46fc6c0dbbdaae4565c610e7e658619c738559fb27395")
r1_control=read("tests-checks/rewrite-r1-control-v1.py","9310da3cecabaae0127fb6562a15b388355f722c35dcd5abbd2b039fd0f4d48c")
r1_map=json.loads(read("tests-checks/rewrite-r1-observer-map-v1.json","af8df00ceb6b02bb5730eee56754ce78badcab6102ce861d726eed704522bfbd"))
population=read("rewrite-early-population-v1.json","3dd0ec8b6130b38d5138724b43e233e4e1a3e595f089c182291b00912d8423ce")
p=json.loads(population)
depth_provenance=read("engineer-depth-budget-probe-v3.py","7aa9f188b2917fec149485501eafcc4d516d3104a10b026e5ec33262b24962ae")
test_bytes=subprocess.run([r"C:\Program Files\Git\cmd\git.exe","-C",r"D:\Pontius","show",
 "29c02f6fbd5eb0b7ddc9e816ef28f570b9839358:tests/test_inventory_and_profiles.py"],
 capture_output=True,check=True,timeout=60,creationflags=subprocess.CREATE_NO_WINDOW).stdout
assert sha(test_bytes)=="c46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf"
test_source=test_bytes.decode()
LOAD_CASES="\ndef load_cases(raw_by_scope, population_raw):\n    require(hashlib.sha256(population_raw).hexdigest() == POPULATION_SHA, \"frozen population\")\n    population = json.loads(population_raw)\n    require(tuple(population[\"gates\"][\"A\"][\"ordered_case_ids\"]) == GATE_B_IDS[:6],\n            \"unchanged Gate A prefix\")\n    gate = population[\"gates\"][\"B\"]\n    require(tuple(gate[\"ordered_case_ids\"]) == GATE_B_IDS\n            and gate[\"public_analysis_count\"] == 12 and gate[\"independent_model_projections\"] == 24\n            and gate[\"depth_assertions\"] == 2\n            and gate[\"engineering_continuation_work_maximum\"] == CONTINUATION_MAXIMUM\n            and gate[\"production_work_cap_unchanged\"] == 262144, \"exact frozen Gate B\")\n    require(set(raw_by_scope) == set(PACKS), \"exact original pack set\")\n    selected = {}\n    for scope, metadata in PACKS.items():\n        raw = raw_by_scope[scope]\n        require(hashlib.sha256(raw).hexdigest() == metadata[\"sha256\"], \"original pack pin\")\n        pack = json.loads(raw)\n        require(pack[\"schema\"] == metadata[\"schema\"], \"original pack schema\")\n        require(type(pack[\"planned_cases\"]) is int\n                and pack[\"planned_cases\"] == metadata[\"planned_cases\"]\n                and type(pack[\"planned_projections\"]) is int\n                and pack[\"planned_projections\"] == metadata[\"planned_projections\"],\n                \"original complete pack counts\")\n        require(len(pack[\"cases\"]) == metadata[\"planned_cases\"]\n                and len({case[\"id\"] for case in pack[\"cases\"]}) == metadata[\"planned_cases\"],\n                \"original complete pack uniqueness\")\n        by_id = {case[\"id\"]: case for case in pack[\"cases\"]}\n        for identifier in metadata[\"ids\"]:\n            case = by_id[identifier]\n            binding = population[\"cases\"][identifier]\n            require(hashlib.sha256(case_canonical(case)).hexdigest()\n                    == binding[\"case_record_canonical_sha256\"], \"selected original record\")\n            for field, target in ((\"source\", \"source\"), (\"oracle_source\", \"model\")):\n                value = case[field]\n                require(type(value) is str and value.endswith(\"\\n\") and \"\\r\" not in value,\n                        \"original source format\")\n                require(hashlib.sha256(value.encode(\"utf-8\")).hexdigest()\n                        == binding[target][\"sha256\"], \"original source/model identity\")\n                ast.parse(value, filename=\"<GateB-unexecuted-source-or-Model>\")\n            require(case[\"classification\"] == binding[\"classification\"], \"original classification\")\n            selected[identifier] = (scope, case)\n    require(len(selected) == 10, \"ten original Model cases\")\n    require(sum(1 if scope == \"storage\" else len(case[\"witnesses\"])\n                for scope, case in selected.values()) == 24, \"exact24 Models\")\n    for identifier, expected in DEPTH_CASES.items():\n        binding = population[\"cases\"][identifier]\n        require(binding[\"classification\"] == \"exact-depth-error\"\n                and binding[\"model\"] is None and binding[\"model_projection_count\"] == 0\n                and binding[\"envelope_ref\"] == \"original_design_review\", \"original depth kind\")\n        require(binding[\"source\"][\"sha256\"] == expected[\"fixture_sha256\"]\n                and binding[\"oracle\"][\"exception\"] == \"InventoryError\"\n                and binding[\"oracle\"][\"regex\"] == expected[\"regex\"], \"original depth expectation\")\n        require(binding[\"original_method\"][\"symbol\"].split(\".\")[-1] == expected[\"method\"],\n                \"original depth owner method\")\n        selected[identifier] = (\"depth\", binding)\n    require(set(selected) == set(GATE_B_IDS), \"no extra cases\")\n    result = [selected[identifier] for identifier in GATE_B_IDS]\n    require(dict(Counter(case[\"classification\"] for scope, case in result))\n            == {\"clean\": 6, \"refuse\": 3, \"permitted-refusal\": 1, \"exact-depth-error\": 2},\n            \"Gate B classifications\")\n    return result\n"
RESERVE="\ndef reserve_violations(metrics, identifier):\n    \"\"\"Post-execution engineering predicate; never modifies or calls a budget.\"\"\"\n    return [{\"case\": identifier, \"epoch\": entry[\"epoch\"],\n             \"observed_work\": entry[\"last_observed_work\"], \"maximum\": CONTINUATION_MAXIMUM}\n            for entry in metrics[\"epochs\"]\n            if entry[\"last_observed_work\"] > CONTINUATION_MAXIMUM]\n"
DEPTH_SUPPORT="\nfixtures = None\n\n\ndef prepare_depth_case(identifier, snapshot, source_sha):\n    \"\"\"Original setup and builder only; never invokes the multi-subtest method.\"\"\"\n    global fixtures\n    test_path = snapshot / \"tests/test_inventory_and_profiles.py\"\n    require(digest(checked(test_path).read_bytes()) == TESTS_SHA, \"original c467 tests\")\n    if fixtures is None:\n        spec = importlib.util.spec_from_file_location(\"rewrite_r2_original_depth_fixtures\", test_path)\n        require(spec is not None and spec.loader is not None, \"original test import spec\")\n        fixtures = importlib.util.module_from_spec(spec)\n        sys.modules[spec.name] = fixtures\n        spec.loader.exec_module(fixtures)\n    require(Path(fixtures.__file__).resolve() == test_path.resolve()\n            and Path(fixtures.SNAPSHOT_ROOT).resolve() == snapshot.resolve()\n            and Path(fixtures.GENERATOR_PATH).resolve()\n                == (snapshot / \"tools/generate_test_inventory.py\").resolve(), \"original fixture paths\")\n    case = fixtures.DesignReviewTests(DEPTH_CASES[identifier][\"method\"])\n    case.setUp()\n    module = case.generator\n    require(Path(module.__file__).resolve() == (snapshot / \"tools/generate_test_inventory.py\").resolve()\n            and digest(checked(Path(module.__file__)).read_bytes()) == source_sha,\n            \"fresh original setup candidate\")\n    require({name: getattr(module, name) for name in CAPS} == CAPS\n            and all(type(getattr(module, name)) is int for name in CAPS), \"fresh candidate caps\")\n    source = helper65_source() if identifier == \"helper65\" else generator70_source()\n    require(type(source) is bytes and digest(source) == DEPTH_CASES[identifier][\"fixture_sha256\"],\n            \"original frozen depth source bytes\")\n    ast.parse(source, filename=\"<unexecuted-original-depth-source>\")\n    return case, module, source\n"
PROBE_TAIL="\n    require({name: getattr(generator, name) for name in CAPS} == CAPS\n            and all(type(getattr(generator, name)) is int for name in CAPS), \"caps changed\")\n    semantic_failures, oracle_errors, analyzer_errors, accounting_errors = [], [], [], []\n    continuation_failures = []\n    attempted, returned_receipts, expected_depth_errors, projections = 0, 0, 0, 0\n    for scope, case in cases:\n        identifier = case[\"id\"]\n        is_depth = scope == \"depth\"\n        depth_case, active_generator = None, generator\n        if is_depth:\n            depth_case, active_generator, source = prepare_depth_case(identifier, snapshot, source_sha)\n            actuals, oracle_passed, oracle_error = [], True, None\n        else:\n            source = case[\"source\"].encode(\"utf-8\")\n            actuals, oracle_passed, oracle_error = [], False, None\n            try:\n                if scope == \"storage\":\n                    actual, oracle_passed = storage_oracle(case)\n                    actuals = [actual]\n                else:\n                    actuals, errors = project_oracles(case)\n                    oracle_passed = not errors\n                projections += len(actuals)\n            except Exception as error:\n                oracle_error = {\"type\": type(error).__name__, \"message\": str(error)}\n        review, analyzer_error, metrics, accounting_error = None, None, None, None\n        public_exception, depth_match, methods_restored = None, False, True\n        violations = []\n        if not oracle_passed:\n            oracle_errors.append(identifier)\n        else:\n            observer = BudgetObserver(active_generator)\n            observer.install()\n            observer.begin(identifier)\n            try:\n                attempted += 1\n                try:\n                    if is_depth:\n                        review = depth_case._review(sources={\"tests/test_review.py\": source})\n                    else:\n                        review = (storage_public_review(generator, source) if scope == \"storage\"\n                                  else public_review(source))\n                except Exception as error:\n                    public_exception = {\"type\": type(error).__name__, \"message\": str(error),\n                                        \"is_inventory_error\": isinstance(error, active_generator.InventoryError)}\n                    depth_match = bool(is_depth and public_exception[\"is_inventory_error\"]\n                                       and re.search(DEPTH_CASES[identifier][\"regex\"], str(error)))\n                    if depth_match:\n                        expected_depth_errors += 1\n                    else:\n                        analyzer_error = public_exception\n                        analyzer_errors.append(identifier)\n                finally:\n                    metrics = observer.end()\n            finally:\n                methods_restored = observer.restore()\n            require(methods_restored, \"original budget methods not restored\")\n            require({name: getattr(active_generator, name) for name in CAPS} == CAPS\n                    and all(type(getattr(active_generator, name)) is int for name in CAPS),\n                    \"active candidate caps changed\")\n            try:\n                validate_budget_metrics(metrics, identifier)\n                violations = reserve_violations(metrics, identifier)\n                continuation_failures.extend(violations)\n            except Exception as error:\n                accounting_error = {\"type\": type(error).__name__, \"message\": str(error)}\n                accounting_errors.append(identifier)\n        rows = review[\"receipt\"][\"expanded_rows\"] if review is not None else []\n        argv = [row[\"argv\"] for row in rows if row[\"capability_kind\"] == \"subprocess\"]\n        blockers = review[\"unresolved_dynamic_blockers\"] if review is not None else []\n        if review is not None:\n            returned_receipts += 1\n        semantic_ok = bool(oracle_passed and\n                           (depth_match if is_depth else\n                            review is not None and public_verdict(scope, case, argv, blockers)))\n        if not semantic_ok:\n            semantic_failures.append(identifier)\n        print(json.dumps({\n            \"rewrite_gate_b_case\": identifier, \"original_pack\": scope,\n            \"classification\": case[\"classification\"], \"source_sha256\": digest(source),\n            \"oracle_sha256\": None if is_depth else digest(case[\"oracle_source\"].encode(\"utf-8\")),\n            \"unreachable_events\": [] if is_depth else case[\"unreachable_events\"],\n            \"expected_projections\": ([] if is_depth else\n                                     [case[\"expected\"]] if scope == \"storage\" else case[\"witnesses\"]),\n            \"required_argv\": None if is_depth else case[\"required_argv\"] if scope == \"storage\" else [[\"-m\", \"fixed\"]],\n            \"oracle_actuals\": actuals, \"oracle_passed\": oracle_passed, \"oracle_error\": oracle_error,\n            \"depth_expectation\": DEPTH_CASES[identifier][\"regex\"] if is_depth else None,\n            \"expected_depth_error\": depth_match, \"public_exception\": public_exception,\n            \"analyzer_error\": analyzer_error, \"argv\": argv, \"expanded_rows\": rows,\n            \"blockers\": blockers, \"semantic_passed\": semantic_ok,\n            \"receipt_sha256\": digest(canonical(review[\"receipt\"])) if review is not None else None,\n            \"budget_metrics\": metrics, \"accounting_error\": accounting_error,\n            \"original_methods_restored\": methods_restored, \"reserve_violations\": violations,\n        }, allow_nan=False), flush=True)\n    require({name: getattr(generator, name) for name in CAPS} == CAPS\n            and all(type(getattr(generator, name)) is int for name in CAPS), \"caps changed during run\")\n    hashes(snapshot, manifest)\n    require(digest(checked(payload / \"manifest.json\").read_bytes()) == manifest_sha, \"manifest changed\")\n    summary = {\"rewrite_gate_b_summary\": True, \"schema\": SCHEMA, \"slot\": slot,\n               \"generator_sha256\": source_sha, \"pack_sha256\": PACK_HASHES, \"probe_sha256\": probe_sha,\n               \"plan_sha256\": PLAN_SHA, \"population_sha256\": POPULATION_SHA,\n               \"observer_map_sha256\": OBSERVER_MAP_SHA, \"tests_sha256\": TESTS_SHA,\n               \"depth_provenance_sha256\": DEPTH_PROVENANCE_SHA,\n               \"planned_cases\": 12, \"case_count\": 12, \"projections\": projections,\n               \"attempted_analyses\": attempted, \"returned_receipts\": returned_receipts,\n               \"expected_depth_errors\": expected_depth_errors,\n               \"semantic_failures\": semantic_failures, \"oracle_errors\": oracle_errors,\n               \"analyzer_errors\": analyzer_errors, \"accounting_errors\": accounting_errors,\n               \"completed\": attempted == 12 and returned_receipts == 10 and expected_depth_errors == 2\n                            and projections == 24 and not oracle_errors\n                            and not analyzer_errors and not accounting_errors,\n               \"classifications\": {\"clean\": 6, \"refuse\": 3, \"permitted-refusal\": 1, \"exact-depth-error\": 2},\n               \"caps\": CAPS, \"original_methods_restored\": True,\n               \"budget_scope\": \"all original creations/requests inside every complete public envelope\",\n               \"observer_overhead_is_not_original_charged_work\": True,\n               \"gate\": \"B\", \"continuation_work_maximum\": CONTINUATION_MAXIMUM,\n               \"reserve_violations\": continuation_failures, \"reserve_ok\": not continuation_failures,\n               \"reserve_is_postexecution_only\": True, \"no_wider_population_run\": True}\n    print(json.dumps(summary, allow_nan=False), flush=True)\n    return int(bool(semantic_failures or oracle_errors or analyzer_errors\n                    or accounting_errors or continuation_failures))\n\n\nif __name__ == \"__main__\":\n    raise SystemExit(main())\n"
VALIDATION_TAIL="\n    observed = records[1:-1]\n    require(tuple(record.get(\"rewrite_gate_b_case\") for record in observed) == GATE_B_IDS,\n            \"exact frozen Gate B order\")\n    semantic_failures, oracle_errors, analyzer_errors, accounting_errors = [], [], [], []\n    continuation_failures = []\n    attempted, returned_receipts, expected_depth_errors, projections = 0, 0, 0, 0\n    for actual, (scope, expected) in zip(observed, cases, strict=True):\n        identifier, is_depth = expected[\"id\"], scope == \"depth\"\n        require(actual[\"original_pack\"] == scope and actual[\"classification\"] == expected[\"classification\"],\n                \"original case attribution\")\n        source_digest = expected[\"source\"][\"sha256\"] if is_depth else sha(expected[\"source\"].encode(\"utf-8\"))\n        model_digest = None if is_depth else sha(expected[\"oracle_source\"].encode(\"utf-8\"))\n        expected_projections = [] if is_depth else [expected[\"expected\"]] if scope == \"storage\" else expected[\"witnesses\"]\n        required_argv = None if is_depth else expected[\"required_argv\"] if scope == \"storage\" else [[\"-m\", \"fixed\"]]\n        unreachable = [] if is_depth else expected[\"unreachable_events\"]\n        require(actual[\"source_sha256\"] == source_digest and actual[\"oracle_sha256\"] == model_digest,\n                \"original source/Model identity\")\n        require(actual[\"expected_projections\"] == expected_projections\n                and actual[\"required_argv\"] == required_argv and actual[\"unreachable_events\"] == unreachable,\n                \"unchanged expected projections/argv\")\n        require(type(actual[\"oracle_actuals\"]) is list, \"Model actual container\")\n        projections += len(actual[\"oracle_actuals\"])\n        oracle_ok = (actual[\"oracle_error\"] is None and actual[\"oracle_actuals\"] == expected_projections\n                     and not any(event in witness[\"trace\"] for witness in actual[\"oracle_actuals\"]\n                                 for event in unreachable))\n        require(actual[\"oracle_passed\"] is oracle_ok, \"Model result inconsistency\")\n        if not oracle_ok:\n            oracle_errors.append(identifier)\n        else:\n            attempted += 1\n        error = actual[\"public_exception\"]\n        if error is not None:\n            require(type(error) is dict and type(error[\"type\"]) is str and type(error[\"message\"]) is str\n                    and type(error[\"is_inventory_error\"]) is bool, \"actual exception record\")\n        depth_match = bool(is_depth and error is not None and error[\"is_inventory_error\"]\n                           and re.search(DEPTH_CASES[identifier][\"regex\"], error[\"message\"]))\n        require(actual[\"expected_depth_error\"] is depth_match\n                and actual[\"depth_expectation\"] == (DEPTH_CASES[identifier][\"regex\"] if is_depth else None),\n                \"original exact depth assertion\")\n        if depth_match:\n            expected_depth_errors += 1\n        expected_analyzer_error = None if depth_match else error\n        require(actual[\"analyzer_error\"] == expected_analyzer_error, \"analysis exception attribution\")\n        if expected_analyzer_error is not None:\n            analyzer_errors.append(identifier)\n        has_receipt = actual[\"receipt_sha256\"] is not None\n        require(not has_receipt or valid_digest(actual[\"receipt_sha256\"]), \"public receipt digest\")\n        require(not has_receipt or (oracle_ok and error is None), \"receipt despite failed/skipped analysis\")\n        if has_receipt:\n            returned_receipts += 1\n        require(type(actual[\"expanded_rows\"]) is list and type(actual[\"blockers\"]) is list,\n                \"public result containers\")\n        require(has_receipt or not actual[\"expanded_rows\"] and not actual[\"blockers\"],\n                \"rows/blockers without returned review\")\n        argv = [row[\"argv\"] for row in actual[\"expanded_rows\"] if row[\"capability_kind\"] == \"subprocess\"]\n        require(actual[\"argv\"] == argv, \"argv differs from public rows\")\n        semantic_ok = bool(oracle_ok and (depth_match if is_depth else\n                           has_receipt and error is None and public_verdict(scope, expected, argv, actual[\"blockers\"])))\n        require(actual[\"semantic_passed\"] is semantic_ok, \"semantic result inconsistency\")\n        if not semantic_ok:\n            semantic_failures.append(identifier)\n        require(actual[\"original_methods_restored\"] is True, \"budget methods not restored\")\n        if actual[\"accounting_error\"] is not None:\n            accounting_errors.append(identifier)\n            require(actual[\"reserve_violations\"] == [], \"reserve verdict despite failed accounting\")\n        elif oracle_ok:\n            validate_budget_metrics(actual[\"budget_metrics\"], identifier)\n            violations = reserve_violations(actual[\"budget_metrics\"], identifier)\n            require(actual[\"reserve_violations\"] == violations, \"postexecution reserve mismatch\")\n            continuation_failures.extend(violations)\n        else:\n            require(actual[\"budget_metrics\"] is None and actual[\"reserve_violations\"] == [],\n                    \"budget scope despite skipped Model\")\n    summary = records[-1]\n    require(summary.get(\"rewrite_gate_b_summary\") is True, \"final Gate B summary\")\n    require(summary[\"schema\"] == SCHEMA and summary[\"slot\"] == setup[\"slot\"]\n            and summary[\"generator_sha256\"] == setup[\"generator_sha256\"]\n            and summary[\"pack_sha256\"] == PACK_HASHES and summary[\"probe_sha256\"] == PROBE_SHA\n            and summary[\"plan_sha256\"] == PLAN_SHA and summary[\"population_sha256\"] == POPULATION_SHA\n            and summary[\"observer_map_sha256\"] == OBSERVER_MAP_SHA\n            and summary[\"tests_sha256\"] == TESTS_SHA\n            and summary[\"depth_provenance_sha256\"] == DEPTH_PROVENANCE_SHA, \"summary input pins\")\n    for key in (\"planned_cases\", \"case_count\"):\n        require(type(summary[key]) is int and summary[key] == 12, \"summary exact scope\")\n    for key, value in ((\"projections\", projections), (\"attempted_analyses\", attempted),\n                       (\"returned_receipts\", returned_receipts), (\"expected_depth_errors\", expected_depth_errors)):\n        require(type(summary[key]) is int and summary[key] == value, \"summary count: \" + key)\n    require(summary[\"classifications\"] == {\"clean\": 6, \"refuse\": 3, \"permitted-refusal\": 1, \"exact-depth-error\": 2}\n            and all(type(value) is int for value in summary[\"classifications\"].values())\n            and summary[\"caps\"] == CAPS and all(type(value) is int for value in summary[\"caps\"].values()),\n            \"classifications/caps\")\n    require(summary[\"semantic_failures\"] == semantic_failures and summary[\"oracle_errors\"] == oracle_errors\n            and summary[\"analyzer_errors\"] == analyzer_errors and summary[\"accounting_errors\"] == accounting_errors,\n            \"summary/case consistency\")\n    require(summary[\"original_methods_restored\"] is True\n            and summary[\"observer_overhead_is_not_original_charged_work\"] is True\n            and summary[\"gate\"] == \"B\" and summary[\"no_wider_population_run\"] is True,\n            \"scope/observer restoration\")\n    require(type(summary[\"continuation_work_maximum\"]) is int\n            and summary[\"continuation_work_maximum\"] == CONTINUATION_MAXIMUM\n            and summary[\"reserve_is_postexecution_only\"] is True\n            and summary[\"reserve_violations\"] == continuation_failures\n            and summary[\"reserve_ok\"] is (not continuation_failures), \"continuation reserve consistency\")\n    completed = (attempted == 12 and returned_receipts == 10 and expected_depth_errors == 2\n                 and projections == 24 and not oracle_errors and not analyzer_errors and not accounting_errors)\n    require(summary[\"completed\"] is completed, \"Gate B completion mismatch\")\n    require(exit_code == int(bool(semantic_failures or oracle_errors or analyzer_errors\n                                  or accounting_errors or continuation_failures)), \"child exit mismatch\")\n    return {\"identity\": identity, \"summary\": summary, \"cases_observed\": len(observed),\n            \"completed\": completed, \"semantic_ok\": not semantic_failures,\n            \"accounting_ok\": not accounting_errors, \"reserve_ok\": not continuation_failures}\n"
PLAN="# Rewrite R2 Gate B harness v1 — frozen authoring scope\n\nPrepared in parallel with R1 source work. This file does not authorize a Gate B\npayload. Root must first disposition Gate A, the R2 source plan and candidate,\nand independently review this harness. Only root dispatches finite controls.\n\nThe unchanged population manifest SHA256\n3dd0ec8b6130b38d5138724b43e233e4e1a3e595f089c182291b00912d8423ce\nselects exactly12 cases in this order: the original Gate A6, helper65,\ngenerator70, scale-n8-s4-d0-normal, scale-n64-s4-d0-normal,\nscale-n8-s4-d2-exceptional, scale-n64-s4-d2-exceptional.\nThere are24 harmless Model projections:4 storage,4 hidden-cell and16 ambient.\nDepth cases have original InventoryError assertions, not new Models.\n\nPreserve all four Gate A public/Model functions by AST and raw source segments.\nThe ambient cases use the same unchanged public24 envelope and Model projector.\nFull original pack bytes, source/Model/expected records, unreachable events,\nclassifications and permitted-refusal behavior remain unchanged. No broad pack\nexecution, fixture widening, candidate-specific expectation or old diagnostic run.\n\nThe two depth cases reuse original c46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf\ntests/test_inventory_and_profiles.py in the fresh r010 snapshot. Import that\nmodule; instantiate DesignReviewTests with the corresponding original method\nname; call only original setUp and _review. Do not invoke either whole test\nmethod: each contains unrelated subtests. Original _load_generator,\n_inventory_entry, _source, inventory and default include_probe=True behavior\nare retained. The full stable/fixture/probe universe and tools/test_child.py\nsource remain. Do not substitute either Gate A one-ID envelope.\n\nCopy only the existing helper65_source and generator70_source definition blocks\nfrom the pinned engineer-depth-budget-probe-v3.py7aa9f188b2917fec149485501eafcc4d516d3104a10b026e5ec33262b24962ae.\nTheir original-test AST correspondence is already bound by the population and\nis checked statically again. That old diagnostic file is provenance-only:\nnever import it or invoke its top-level code. Existing builders run once in\nthe future controlled child and produce the exact retained source hashes\n94b070b8fcf2e66c42e1a779558e830d7caae670366f9313faf0989c722818c6\n(helper65) and635e682b2253cd44201e2afdb95c288b9973f5629ec4eeb3c5bfd078743eb5e3\n(generator70). Sensitive source bytes are parsed/reviewed, never executed.\nGenerator70's original builder is inside _fix15_frozen_review_boundary_contracts,\nwhich the wrapper test calls; do not confuse that wrapper with the builder.\n\nDepth completion requires the original InventoryError type relationship and\noriginal regex search:\n^analysis helper depth exceeds 64$\n^analysis deferred generator depth exceeds 64$\nA normal review, unsupported-syntax blocker, work-cap error or other exception\nis not a substitute. Success needs10 returned normal public receipts,2 matching\ndepth errors, all12 public attempts and all24 Model projections. Unexpected\nerrors, incomplete accounting and custody failures remain separately visible.\n\nEach original depth setUp imports a fresh generator module. Verify its exact\nsnapshot path/source/caps and install the original init/consume observer on\nthat case.generator, not the initial Gate A generator. Restore original methods\nafter each case. The observer class and reconciliation logic are unchanged;\nall actual budget creations/requests across each complete public call count,\nincluding source facts, module construction, preflight, body and nested helpers.\nNo budget/cache/AST/frame is retained by observation. Source construction,\ntest setup and observer work are disclosed harness overhead, not production\nbudget charges or timing evidence.\n\nAfter each complete analysis, compare every epoch's observed work against196608.\nThis is the adopted engineering continuation reserve, never a runtime admission\ncap: do not throw, reset, refund, clamp, stop observation or alter consume there.\nAll five production caps remain unchanged, including262144 work units.\nThe controller replays the same per-epoch predicate from raw records. Semantics,\nModel completion, custody, accounting and reserve results remain distinct.\nNo epoch-number filter, enabled-only total, sum-instead-of-maximum substitution\nor average reserve is accepted.\n\nAdapt only the existing R1 snapshot controller. Explicit retained candidate\npath/SHA, old v20 watch and explicit new core-W watch remain. Every invocation\ncreates a fresh D-local r010 clone/detach and private temp, overlays the exact\ngenerator and10 payload/provenance files, and hashes all1761 tracked paths plus\nthe overlays before/after. Original c467 tests are tracked, unchanged, explicitly\npinned before import. Candidate-only overlay permits r010 clean tracked status.\nProbe/control/plan/population/map/provenance/run/manifest hashes remain bound.\n\nActual3.11.15 first;3.14.6 requires a matching successful floor receipt with all\nsemantic/custody/accounting/reserve gates true. Replay raw floor identity,\n14-record identity/12-case/summary stream,24 projections, depth errors, budgets,\nsetup, logs, full snapshot and input hashes. Each slot uses a new snapshot.\nKeep -B -P child, seed0, snapshot/src PYTHONPATH, scrubbed environment, absolute\nregular/non-reparse Git, pre-import identity and60-second direct-child watchdog.\nSetup/integrity Git commands retain their existing60-second timeout too.\nOutputs are create-exclusive; interrupted or invalid runs retain partial raw\nstreams and explicit incomplete receipts. There is no automatic expansion.\n\nAuthoring performs AST/hash checks only. No source/Model/fixture builder,\ncandidate, test, controller, diagnostic or orchestration payload is executed.\nNo source/W/main edit, install, commit, deploy or Gate B dispatch is authorized.\n"

plan_raw=PLAN.encode(); plan_sha=sha(plan_raw)
new_map=dict(r1_map)
new_map.update({
 "schema":"pontius-rewrite-r2-budget-observer-map-v1","gate":"B",
 "scope":"all original budgets/requests inside12 complete public invocations, including original2 depth envelopes",
 "original_tests_sha256":sha(test_bytes),"depth_provenance_sha256":sha(depth_provenance.encode()),
 "source_hash_conventions":{
   "observer_class_source_sha256":"UTF8 verbatim emitted observer block, leading/trailing LF included: budget_context, budget_origin, budget_phase, BudgetObserver; same block as R1",
   "budget_reconciliation_source_sha256":"UTF8 LF + validate_budget_metrics source segment + LF; same block as R1",
   "reserve_source_sha256":"UTF8 verbatim RESERVE emitted block including leading/trailing LF"},
 "reserve_source_sha256":sha(RESERVE.encode()),
 "continuation_work_maximum":196608,"reserve_is_postexecution_only":True,
 "expected_normal_receipts":10,"expected_depth_errors":2,"public_attempts":12,"Model_projections":24,
 "depth_runtime":"original DesignReviewTests.setUp imports fresh generator; observer installed on each case.generator and restored after that original _review call",
 "coverage_limits":[
  "candidate import/original test setup/source construction are harness work before public-call observation",
  "all production semantic preparation inside derive_design_review is observed; no epoch or mode filter",
  "no physical operation categories inferred; production accounting source review remains required",
  "unrecognized stage remains other with original caller/parent/creation context",
  "observer overhead is outside original charged units; no timing comparison"]})
map_raw=dump(new_map); map_sha=sha(map_raw)
depth_defs=segment(depth_provenance,"helper65_source")+"\n"+segment(depth_provenance,"generator70_source")
depth_cases={name:{"method":p["cases"][name]["original_method"]["symbol"].split(".")[-1],
                  "fixture_sha256":p["cases"][name]["source"]["sha256"],
                  "regex":p["cases"][name]["oracle"]["regex"]} for name in ("helper65","generator70")}
constants=(
 "\nGATE_B_IDS = "+repr(tuple(p["gates"]["B"]["ordered_case_ids"]))+"\n"
 "CONTINUATION_MAXIMUM = 196608\n"
 "TESTS_SHA = "+repr(sha(test_bytes))+"\n"
 "DEPTH_PROVENANCE_SHA = "+repr(sha(depth_provenance.encode()))+"\n"
 "DEPTH_CASES = "+repr(depth_cases)+"\n")
def adapt_common(src):
 src=once(src,'        "ids": ("hidden-cell-joined-reached", "hidden-cell-joined-dormant"),',
  '        "ids": ("hidden-cell-joined-reached", "hidden-cell-joined-dormant",\n'
  '                "scale-n8-s4-d0-normal", "scale-n64-s4-d0-normal",\n'
  '                "scale-n8-s4-d2-exceptional", "scale-n64-s4-d2-exceptional"),')
 src=once(src,'GATE_A_IDS = tuple(name for metadata in PACKS.values() for name in metadata["ids"])',constants.strip())
 src=src.replace("8cec0f3af002f04b20c82dee62d29f0601a87047249ab2dfcde5a164ca73826d",plan_sha)
 src=src.replace("af8df00ceb6b02bb5730eee56754ce78badcab6102ce861d726eed704522bfbd",map_sha)
 src=replace_top(src,"load_cases",LOAD_CASES)
 return src
probe=adapt_common(r1_probe)
probe=probe.replace("pontius-rewrite-r1-gate-a-v1","pontius-rewrite-r2-gate-b-v1").replace(".rewrite-r1-gate-a",".rewrite-r2-gate-b")
probe=once(probe,'"""Frozen rewrite R1 Gate A: six original public cases/eight Models; no work on import."""',
 '"""Frozen rewrite R2 Gate B:12 original public cases/24 Models; no work on import."""')
probe=once(probe,"import os\n","import os\nimport re\nimport textwrap\n")
probe=once(probe,"def main():",depth_defs+"\n"+DEPTH_SUPPORT+"\n"+RESERVE+"\n\ndef main():")
main=probe[probe.index("def main():"):]
marker='    require({name: getattr(generator, name) for name in CAPS} == CAPS\n'
main=main[:main.index(marker)]
main=main.replace("1770","1771").replace('"rewrite_r1_gate_a_generator"','"rewrite_r2_gate_b_generator"')
main=once(main,'            and run["observer_map_sha256"] == OBSERVER_MAP_SHA, "run input identity")',
 '            and run["observer_map_sha256"] == OBSERVER_MAP_SHA\n'
 '            and run["tests_sha256"] == TESTS_SHA\n'
 '            and run["depth_provenance_sha256"] == DEPTH_PROVENANCE_SHA\n'
 '            and run["continuation_work_maximum"] == CONTINUATION_MAXIMUM, "run input identity")')
main=once(main,'    population_raw = checked(payload / "population.json").read_bytes()',
 '    require(digest(checked(payload / "depth-provenance.py").read_bytes()) == DEPTH_PROVENANCE_SHA,\n'
 '            "depth provenance source bytes")\n'
 '    require(digest(checked(snapshot / "tests/test_inventory_and_profiles.py").read_bytes()) == TESTS_SHA,\n'
 '            "original depth test module bytes")\n'
 '    population_raw = checked(payload / "population.json").read_bytes()')
probe=probe[:probe.index("def main():")]+main+PROBE_TAIL
probe_raw=probe.encode(); probe_sha=sha(probe_raw)
control=adapt_common(r1_control)
control=control.replace("rewrite-r1-gate-a","rewrite-r2-gate-b")
control=control.replace("rewrite-r1-probe-v1.py","rewrite-r2-probe-v1.py")
control=control.replace("rewrite-r1-plan-v1.md","rewrite-r2-plan-v1.md")
control=control.replace("rewrite-r1-observer-map-v1.json","rewrite-r2-observer-map-v1.json")
control=control.replace("c0672ac61fa19b5dd3d46fc6c0dbbdaae4565c610e7e658619c738559fb27395",probe_sha)
control=once(control,'POPULATION = ROOT / "rewrite-early-population-v1.json"',
 'POPULATION = ROOT / "rewrite-early-population-v1.json"\n'
 'DEPTH_PROVENANCE = ROOT / "engineer-depth-budget-probe-v3.py"')
validation=segment(control,"validate_result")
validation=validation[:validation.index("    observed = records[1:-1]")]
validation=validation.replace("len(lines) == 8","len(lines) == 14").replace("identity/six-case/summary","identity/twelve-case/summary")
validation+=VALIDATION_TAIL
control=replace_top(control,"validate_result",RESERVE+"\n"+validation)
control=once(control,'             "core_watch_source": str(CORE_WATCH), "core_watch_sha256": args.worktree_sha256}',
 '             "core_watch_source": str(CORE_WATCH), "core_watch_sha256": args.worktree_sha256,\n'
 '             "tests_sha256": TESTS_SHA, "depth_provenance_sha256": DEPTH_PROVENANCE_SHA,\n'
 '             "continuation_work_maximum": CONTINUATION_MAXIMUM}')
control=once(control,'                       "observer_map": OBSERVER_MAP, "core_watch": CORE_WATCH}',
 '                       "observer_map": OBSERVER_MAP, "core_watch": CORE_WATCH,\n'
 '                       "depth_provenance": DEPTH_PROVENANCE}')
control=once(control,'                        "core_watch": args.worktree_sha256}',
 '                        "core_watch": args.worktree_sha256, "depth_provenance": DEPTH_PROVENANCE_SHA}')
control=control.replace('"population_sha256", "observer_map_sha256",',
 '"population_sha256", "observer_map_sha256", "tests_sha256", "depth_provenance_sha256",\n'
 '                        "continuation_work_maximum",')
control=once(control,'                    and floor["accounting_ok"] is True and "error" not in floor',
 '                    and floor["accounting_ok"] is True and floor["reserve_ok"] is True and "error" not in floor')
control=control.replace('floor["payload_file_count"] == 9','floor["payload_file_count"] == 10')
control=control.replace('len(floor["before"]) == 1770','len(floor["before"]) == 1771')
control=once(control,'                    and proof["accounting_ok"] is True and floor["accounting_ok"] is True',
 '                    and proof["accounting_ok"] is True and floor["accounting_ok"] is True\n'
 '                    and proof["reserve_ok"] is True and floor["reserve_ok"] is True')
control=once(control,'                                   "population.json", "observer-map.json"}',
 '                                   "population.json", "observer-map.json", "depth-provenance.py"}')
control=once(control,'            require(file_hashes(floor_snapshot, floor["before"]) == floor["before"], "floor snapshot now changed")',
 '            require(file_hashes(floor_snapshot, floor["before"]) == floor["before"], "floor snapshot now changed")\n'
 '            require(floor["before"]["tests/test_inventory_and_profiles.py"] == TESTS_SHA,\n'
 '                    "floor original tests identity")')
control=once(control,'        require(before[GENERATOR] == source_sha, "copied overlay pin")',
 '        require(before[GENERATOR] == source_sha, "copied overlay pin")\n'
 '        require(before["tests/test_inventory_and_profiles.py"] == TESTS_SHA, "original test blob")')
control=once(control,'               "core_watch_source": str(CORE_WATCH), "core_watch_sha256": args.worktree_sha256}',
 '               "core_watch_source": str(CORE_WATCH), "core_watch_sha256": args.worktree_sha256,\n'
 '               "tests_sha256": TESTS_SHA, "depth_provenance_sha256": DEPTH_PROVENANCE_SHA,\n'
 '               "continuation_work_maximum": CONTINUATION_MAXIMUM}')
control=once(control,'                 "population.json": inputs["population"], "observer-map.json": inputs["observer_map"],',
 '                 "population.json": inputs["population"], "observer-map.json": inputs["observer_map"],\n'
 '                 "depth-provenance.py": inputs["depth_provenance"],')
control=control.replace("len(before) == 1770","len(before) == 1771")
control=once(control,'                              and receipt.get("semantic_ok") is True and receipt.get("accounting_ok") is True',
 '                              and receipt.get("semantic_ok") is True and receipt.get("accounting_ok") is True\n'
 '                              and receipt.get("reserve_ok") is True')
control=control.replace("Rewrite R1 Gate A snapshot control; authoring is not run permission.",
 "Rewrite R2 Gate B snapshot control; authoring is not run permission.")
control_raw=control.encode(); control_sha=sha(control_raw)

# Static parsing only; none of the fixtures/builders/Models/controllers/candidates runs.
ast.parse(probe); ast.parse(control)
def fn_dump(src,name):
 return ast.dump(top(src,name),include_attributes=False)
preserved={}
for name in ("storage_public_review","storage_oracle","public_review","project_oracles",
             "budget_context","budget_origin","budget_phase","BudgetObserver","validate_budget_metrics",
             "require","digest","canonical","checked","hashes"):
 preserved["probe_"+name]=fn_dump(r1_probe,name)==fn_dump(probe,name)
for name in ("require","sha","canonical","valid_digest","checked","create","write_json",
             "environment","git","file_hashes","validate_budget_metrics","public_verdict","case_canonical"):
 preserved["control_"+name]=fn_dump(r1_control,name)==fn_dump(control,name)
for name in ("load_cases","reserve_violations","validate_budget_metrics","public_verdict","case_canonical"):
 preserved["shared_"+name]=fn_dump(probe,name)==fn_dump(control,name)
for name in ("helper65_source","generator70_source"):
 preserved["builder_"+name]=fn_dump(depth_provenance,name)==fn_dump(probe,name)
 binding=p["cases"]["helper65" if name=="helper65_source" else "generator70"]["retained_equivalent_builder"]
 assert sha(fn_dump(probe,name).encode())==binding["ast_sha256"]
 assert sha(segment(depth_provenance,name).encode())==binding["source_span_sha256"]
assert all(preserved.values()),preserved
def check_original_span(binding):
 assert binding["source_ref"]=="original_test_module"
 raw=b"".join(test_bytes.splitlines(True)[binding["start_line"]-1:binding["end_line"]])
 assert sha(raw)==binding["source_span_sha256"],binding["symbol"]
 return {"symbol":binding["symbol"],"sha256":sha(raw),"bytes":len(raw)}
spans=[]
for name in ("helper65","generator70"):
 entry=p["cases"][name]
 for key in ("fixture_owner","original_method","original_assertion_block","original_review_call"):
  spans.append(check_original_span(entry[key]))
 for binding in entry["original_builder_fragments"]:
  spans.append(check_original_span(binding))
for binding in p["envelopes"]["original_design_review"]["dependencies"].values():
 if isinstance(binding,dict) and binding.get("source_ref")=="original_test_module":
  spans.append(check_original_span(binding))
for binding in p["envelopes"]["original_design_review"]["source_literal_dependencies"].values():
 spans.append(check_original_span(binding["literal_source_span"]))
pack_constants=ast.literal_eval(next(n.value for n in ast.parse(probe).body if isinstance(n,ast.Assign)
 and any(isinstance(t,ast.Name) and t.id=="PACKS" for t in n.targets)))
selected={}
for scope, metadata in pack_constants.items():
 raw=(C/metadata["file"]).read_bytes(); assert sha(raw)==metadata["sha256"]
 pack=json.loads(raw); assert pack["schema"]==metadata["schema"]
 assert pack["planned_cases"]==metadata["planned_cases"] and pack["planned_projections"]==metadata["planned_projections"]
 for identifier in metadata["ids"]:
  case=next(case for case in pack["cases"] if case["id"]==identifier)
  assert sha(json.dumps(case,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode())==p["cases"][identifier]["case_record_canonical_sha256"]
  selected[identifier]=(scope,case)
assert len(selected)==10
assert sum(1 if s=="storage" else len(c["witnesses"]) for s,c in selected.values())==24
assert set(selected)|set(depth_cases)==set(p["gates"]["B"]["ordered_case_ids"])
assert len([n for n in ast.walk(ast.parse(probe)) if isinstance(n,ast.Call)
            and isinstance(n.func,ast.Name) and n.func.id=="exec"])==2
assert len([n for n in ast.walk(ast.parse(probe)) if isinstance(n,ast.Call)
            and isinstance(n.func,ast.Name) and n.func.id=="compile"])==2
assert "engineer-depth-budget-probe-v5" not in probe+control
assert "_NameMeter" not in probe+control and "helper1050" not in probe+control
assert "original-composition-ten" not in probe+control
# New reserve function is record-only: no budget object, consume or mutation target.
reserve_node=top(probe,"reserve_violations")
assert not any(isinstance(n,ast.Attribute) and n.attr in ("consume","budget","container") for n in ast.walk(reserve_node))
# No original whole multi-subtest methods are called by attribute name.
method_names={x["method"] for x in depth_cases.values()}|{"_fix15_frozen_review_boundary_contracts"}
assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in method_names for n in ast.walk(ast.parse(probe)))
diff_probe="".join(difflib.unified_diff(r1_probe.splitlines(True),probe.splitlines(True),
 fromfile="rewrite-r1-probe-v1.py",tofile="rewrite-r2-probe-v1.py"))
diff_control="".join(difflib.unified_diff(r1_control.splitlines(True),control.splitlines(True),
 fromfile="rewrite-r1-control-v1.py",tofile="rewrite-r2-control-v1.py"))
static={
 "schema":"pontius-rewrite-r2-harness-static-v1","status":"unexecuted authoring, root held",
 "static_runtime":list(sys.version_info[:3]),"payload_executed":False,"source_fixtures_regenerated":False,
 "candidate_Model_builder_test_module_imported":False,
 "population_sha256":sha(population.encode()),"probe_sha256":probe_sha,"control_sha256":control_sha,
 "plan_sha256":plan_sha,"observer_map_sha256":map_sha,"original_tests_sha256":sha(test_bytes),
 "depth_provenance_sha256":sha(depth_provenance.encode()),"preservation":preserved,
 "depth_original_spans_verified":spans,"public_attempts":12,"normal_receipts":10,"expected_depth_errors":2,
 "Model_projections":24,"ordered_case_ids":p["gates"]["B"]["ordered_case_ids"],
 "classifications":p["gates"]["B"]["classifications"],
 "continuation_maximum":196608,"production_work_cap":262144,"reserve_has_no_budget_calls":True,
 "original_inputs":{
 "tests-checks/rewrite-r1-probe-v1.py":sha(r1_probe.encode()),
 "tests-checks/rewrite-r1-control-v1.py":sha(r1_control.encode()),
 "rewrite-early-population-v1.json":sha(population.encode()),
 "engineer-depth-budget-probe-v3.py":sha(depth_provenance.encode()),
 "tests/test_inventory_and_profiles.py@r010":sha(test_bytes)},
 "deltas":{"probe":sha(diff_probe.encode()),"control":sha(diff_control.encode())},
 "limits":["static source proofs only; not runtime harness approval",
 "independent R2 candidate/operation-accounting and GateA disposition required before any GateB dispatch",
 "original budget observer measures production requests, not physical-work or runtime ratios"]}
handoff=f"""# Rewrite R2 Gate B harness authoring handoff v1

Frozen and UNEXECUTED. Preparing it does not authorize Gate B or advance R1.
Root reviews this harness and the R2 source plan/candidate separately after Gate A.

Probe rewrite-r2-probe-v1.py SHA256 {probe_sha}
Control rewrite-r2-control-v1.py SHA256 {control_sha}
Plan rewrite-r2-plan-v1.md SHA256 {plan_sha}
Observer map rewrite-r2-observer-map-v1.json SHA256 {map_sha}
Static proof rewrite-r2-static-v1.json and exact R1 predecessor diffs accompany them.

The fixed manifest selects12 public analyses,24 Models,10 normal receipts and
two original exact depth errors. All four original public/Model functions and
the budget observer/reconciliation definitions are unchanged. The two copied
existing builders match their source/AST pins; original test method, assertion,
builder and full envelope spans were rehashed. No builder or Model ran here.

Only original DesignReviewTests.setUp/_review execute in the future depth adapter,
on each freshly loaded case.generator. Whole multi-subtest methods and old
diagnostics never execute. Original child source/full universe remain. All actual
original budgets count.196608 is a postexecution per-epoch continuation check;
the262144 production cap and original consume implementation stay unchanged.

Root-owned future controller CLI uses the same arguments as R1:
LABEL SLOT RETAINED_SOURCE SOURCE_SHA --control-sha256 {control_sha} --worktree-sha256 APPROVED_CORE_W_SHA
For314 require --floor-receipt PATH --floor-sha256 SHA. The matching floor must
have intact custody, all semantics/Models, accounting and reserve success.
The current old-W watch staysv20. Source/candidate changes, payload invocations,
Gate B expansion or earlier dispatch are not authorized by this artifact.

Original ten payload/provenance files plus1761 tracked files are fully hashed;
dev adds the five pinned floor evidence files. All runs use new D-local r010
snapshots, original flags/environment/Git and60-second direct-child watchdog.
"""
files={
 "rewrite-r2-plan-v1.md":plan_raw,"rewrite-r2-observer-map-v1.json":map_raw,
 "rewrite-r2-probe-v1.py":probe_raw,"rewrite-r2-control-v1.py":control_raw,
 "rewrite-r2-probe-v1-from-r1.diff":diff_probe.encode(),
 "rewrite-r2-control-v1-from-r1.diff":diff_control.encode(),
 "rewrite-r2-static-v1.json":dump(static),"rewrite-r2-handoff-v1.md":handoff.encode()}
assert not any((C/name).exists() for name in files)
for name,raw in files.items(): create(name,raw)
print(json.dumps({"issued":{name:{"sha256":sha(raw),"bytes":len(raw)} for name,raw in files.items()},
 "preservation_checks":len(preserved),"all_preserved":all(preserved.values()),"no_payload":True},indent=2))
