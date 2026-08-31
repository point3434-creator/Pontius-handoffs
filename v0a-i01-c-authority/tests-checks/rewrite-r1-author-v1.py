import ast
import difflib
import hashlib
import json
from pathlib import Path
import sys
T=Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
C=T/"tests-checks"
assert sys.version_info[:3] == (3,11,15)
def sha(raw): return hashlib.sha256(raw).hexdigest()
def dump(value): return (json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+"\n").encode()
def create(path,raw):
    with path.open("xb") as f: f.write(raw)
def top(src,name):
    return next(n for n in ast.parse(src).body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name)
def segment(src,name): return ast.get_source_segment(src,top(src,name))+"\n"
def replace_top(src,name,value):
    n=top(src,name); lines=src.splitlines(keepends=True)
    return "".join(lines[:n.lineno-1])+value.rstrip()+"\n"+"".join(lines[n.end_lineno:])
def once(src,old,new):
    assert src.count(old)==1,(old,src.count(old))
    return src.replace(old,new)
def file_pin(path,expected=None):
    raw=path.read_bytes()
    if expected: assert sha(raw)==expected,(path,sha(raw))
    return raw.decode("utf-8")
base_control=file_pin(C/"original-composition-ten-control-v1.py")
base_probe=file_pin(C/"original-composition-ten-probe-v1.py","e2564b1d1d61c0a92e449f80eb5118eb72141b3fabd9022cf2b2881d1c56927e")
name_probe=file_pin(C/"name-environment-probe-v1.py","94a91ff970aa0df12c4334d72a2476ca5d58a4b76aa3a412c5440e93411806b4")
population=file_pin(T/"rewrite-early-population-v1.json","3dd0ec8b6130b38d5138724b43e233e4e1a3e595f089c182291b00912d8423ce")
baseline=file_pin(T/"rewrite-r1-base-generator.py","29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692")
COMMON="\nPACKS = {\n    \"storage\": {\n        \"file\": \"storage-composition-cases-v1.json\",\n        \"sha256\": \"faa0026181653881737e15af0effe6e670fbad3ad20e684c1d019851dd0dd709\",\n        \"schema\": \"pontius-storage-composition-cases-v1\",\n        \"planned_cases\": 4, \"planned_projections\": 4,\n        \"ids\": (\"shared-list-consumed\", \"shared-list-dormant\",\n                \"class-adoption-unsafe\", \"class-adoption-safe\"),\n    },\n    \"name_environment\": {\n        \"file\": \"name-environment-cases-v1.json\",\n        \"sha256\": \"d07ccfd6d72daee378d1a67468290e7e30fd8f2a0e608bad9cc16fc4b51b2e9c\",\n        \"schema\": \"pontius-engineering-name-environment-family-v1\",\n        \"planned_cases\": 24, \"planned_projections\": 58,\n        \"ids\": (\"hidden-cell-joined-reached\", \"hidden-cell-joined-dormant\"),\n    },\n}\nPACK_HASHES = {scope: metadata[\"sha256\"] for scope, metadata in PACKS.items()}\nGATE_A_IDS = tuple(name for metadata in PACKS.values() for name in metadata[\"ids\"])\nPOPULATION_SHA = \"3dd0ec8b6130b38d5138724b43e233e4e1a3e595f089c182291b00912d8423ce\"\n\n\ndef case_canonical(value):\n    return json.dumps(value, ensure_ascii=False, sort_keys=True,\n                      separators=(\",\", \":\"), allow_nan=False).encode(\"utf-8\")\n\n\ndef load_cases(raw_by_scope, population_raw):\n    require(hashlib.sha256(population_raw).hexdigest() == POPULATION_SHA, \"frozen population\")\n    population = json.loads(population_raw)\n    require(tuple(population[\"gates\"][\"A\"][\"ordered_case_ids\"]) == GATE_A_IDS,\n            \"exact Gate A selection\")\n    require(population[\"gates\"][\"A\"][\"public_analysis_count\"] == 6\n            and population[\"gates\"][\"A\"][\"independent_model_projections\"] == 8,\n            \"frozen Gate A counts\")\n    require(set(raw_by_scope) == set(PACKS), \"exact original pack set\")\n    combined = []\n    for scope, metadata in PACKS.items():\n        raw = raw_by_scope[scope]\n        require(hashlib.sha256(raw).hexdigest() == metadata[\"sha256\"], \"original pack pin\")\n        pack = json.loads(raw)\n        require(pack[\"schema\"] == metadata[\"schema\"], \"original pack schema\")\n        require(type(pack[\"planned_cases\"]) is int\n                and pack[\"planned_cases\"] == metadata[\"planned_cases\"]\n                and type(pack[\"planned_projections\"]) is int\n                and pack[\"planned_projections\"] == metadata[\"planned_projections\"],\n                \"original complete pack counts\")\n        require(len(pack[\"cases\"]) == metadata[\"planned_cases\"]\n                and len({case[\"id\"] for case in pack[\"cases\"]}) == metadata[\"planned_cases\"],\n                \"original complete pack uniqueness\")\n        by_id = {case[\"id\"]: case for case in pack[\"cases\"]}\n        for identifier in metadata[\"ids\"]:\n            case = by_id[identifier]\n            binding = population[\"cases\"][identifier]\n            require(hashlib.sha256(case_canonical(case)).hexdigest()\n                    == binding[\"case_record_canonical_sha256\"], \"selected record binding\")\n            for field, target in ((\"source\", \"source\"), (\"oracle_source\", \"model\")):\n                value = case[field]\n                require(type(value) is str and value.endswith(\"\\n\") and \"\\r\" not in value,\n                        \"original source format\")\n                require(hashlib.sha256(value.encode(\"utf-8\")).hexdigest()\n                        == binding[target][\"sha256\"], \"original source/model binding\")\n                ast.parse(value, filename=\"<GateA-unexecuted-source-or-Model>\")\n            require(case[\"classification\"] == binding[\"classification\"], \"classification binding\")\n            combined.append((scope, case))\n    require(tuple(case[\"id\"] for scope, case in combined) == GATE_A_IDS, \"exact Gate A order\")\n    require(dict(Counter(case[\"classification\"] for scope, case in combined))\n            == {\"clean\": 2, \"refuse\": 3, \"permitted-refusal\": 1}, \"Gate A classifications\")\n    require(sum(1 if scope == \"storage\" else len(case[\"witnesses\"])\n                for scope, case in combined) == 8, \"Gate A exact eight Models\")\n    return combined\n\n\ndef public_verdict(scope, case, argv, blockers):\n    if case[\"classification\"] == \"refuse\":\n        return bool(blockers)\n    if scope == \"storage\":\n        return not blockers and argv == case[\"required_argv\"]\n    if case[\"classification\"] == \"permitted-refusal\":\n        return bool(blockers) or argv == [[\"-m\", \"fixed\"]]\n    return not blockers and argv == [[\"-m\", \"fixed\"]]\n"
OBSERVER="\ndef budget_context(frame):\n    \"\"\"Return scalars only; never retain frames, ASTs, stores or budget objects.\"\"\"\n    rows = []\n    while frame is not None:\n        row = {\"function\": frame.f_code.co_qualname, \"line\": frame.f_lineno,\n               \"file\": Path(frame.f_code.co_filename).name}\n        local = frame.f_locals\n        for name in (\"relative_path\", \"item_id\", \"stable_id\", \"name\"):\n            value = local.get(name)\n            if type(value) is str:\n                row[name] = value\n        rows.append(row)\n        frame = frame.f_back\n    return rows\n\n\ndef budget_origin(frame):\n    return (frame.f_code.co_qualname + \":\" + str(frame.f_lineno)\n            if frame is not None else \"<root>\")\n\n\ndef budget_phase(frame):\n    \"\"\"Nearest matching original entry wins; unrecognized paths remain explicit.\"\"\"\n    stages = (\n        (\"_definition_time_protocol_resolver\", \"definition_time_protocol\"),\n        (\"_unittest_receiver_attributes\", \"unittest_preflight\"),\n        (\"_source_ordered_helper_return\", \"source_ordered_helper_return\"),\n        (\"review_flow\", \"review_flow\"),\n    )\n    while frame is not None:\n        short = frame.f_code.co_name\n        for name, label in stages:\n            if short == name:\n                return label\n        frame = frame.f_back\n    return \"other\"\n\n\nclass BudgetObserver:\n    def __init__(self, module):\n        self.module = module\n        self.original_init = module._AnalysisBudget.__init__\n        self.original_consume = module._AnalysisBudget.consume\n        self.original_codes = (self.original_init.__code__, self.original_consume.__code__)\n        self.current = None\n        self.by_id = {}\n        self.unscoped_events = 0\n\n    def install(self):\n        observer = self\n        original_init, original_consume = self.original_init, self.original_consume\n\n        def observed_init(budget, *args, **keywords):\n            if observer.current is None:\n                observer.unscoped_events += 1\n                return original_init(budget, *args, **keywords)\n            context = budget_context(sys._getframe(1))\n            observer.current[\"initialization_attempts\"] += 1\n            try:\n                result = original_init(budget, *args, **keywords)\n            except BaseException as error:\n                observer.current[\"initialization_errors\"].append({\n                    \"type\": type(error).__name__, \"message\": str(error), \"creation_stack\": context})\n                raise\n            initial = object.__getattribute__(budget, \"work_units\")\n            require(type(initial) is int and initial >= 0, \"original budget initial integer\")\n            entry = {\"epoch\": len(observer.current[\"epochs\"]) + 1, \"initial_work\": initial,\n                     \"last_observed_work\": initial, \"requested_units\": 0, \"consume_calls\": 0,\n                     \"completed_consume_calls\": 0, \"exceptional_consume_calls\": 0,\n                     \"origins\": {}, \"phase_units\": {}, \"creation_stack\": context,\n                     \"consume_exceptions\": []}\n            observer.current[\"epochs\"].append(entry)\n            # An id reused after destruction is overwritten by this new epoch.\n            # An old live budget cannot share an id; no budget reference escapes.\n            observer.by_id[id(budget)] = entry\n            return result\n\n        def observed_consume(budget, units=1):\n            if observer.current is None:\n                observer.unscoped_events += 1\n                return original_consume(budget, units)\n            entry = observer.by_id.get(id(budget))\n            require(entry is not None, \"consume without observed original initialization\")\n            before = object.__getattribute__(budget, \"work_units\")\n            require(type(units) is int and units >= 0 and type(before) is int,\n                    \"original integer charge contract\")\n            require(before == entry[\"last_observed_work\"], \"unobserved original work mutation\")\n            frame = sys._getframe(1)\n            origin = budget_origin(frame)\n            parent = budget_origin(frame.f_back)\n            phase = budget_phase(frame)\n            row = entry[\"origins\"].setdefault(origin + \" <- \" + parent, {\"calls\": 0, \"units\": 0})\n            row[\"calls\"] += 1\n            row[\"units\"] += units\n            entry[\"phase_units\"][phase] = entry[\"phase_units\"].get(phase, 0) + units\n            entry[\"consume_calls\"] += 1\n            entry[\"requested_units\"] += units\n            try:\n                result = original_consume(budget, units)\n            except BaseException as error:\n                entry[\"exceptional_consume_calls\"] += 1\n                entry[\"consume_exceptions\"].append({\n                    \"type\": type(error).__name__, \"message\": str(error),\n                    \"before\": before, \"requested_units\": units,\n                    \"after\": object.__getattribute__(budget, \"work_units\"),\n                    \"stack\": budget_context(frame)})\n                raise\n            else:\n                entry[\"completed_consume_calls\"] += 1\n                return result\n            finally:\n                entry[\"last_observed_work\"] = object.__getattribute__(budget, \"work_units\")\n                # frame references are call-local, never stored in observer records.\n                del frame\n\n        self.observed_init = observed_init\n        self.observed_consume = observed_consume\n        self.module._AnalysisBudget.__init__ = observed_init\n        self.module._AnalysisBudget.consume = observed_consume\n\n    def begin(self, identifier):\n        require(self.current is None, \"overlapping case budgets\")\n        self.by_id = {}\n        self.current = {\"case\": identifier, \"epochs\": [], \"initialization_attempts\": 0,\n                        \"initialization_errors\": []}\n\n    def end(self):\n        result = self.current\n        require(result is not None, \"no active case budget scope\")\n        self.current = None\n        self.by_id = {}\n        result[\"epoch_count\"] = len(result[\"epochs\"])\n        result[\"requested_units_across_epochs\"] = sum(e[\"requested_units\"] for e in result[\"epochs\"])\n        result[\"maximum_epoch_observed_work\"] = max(\n            (e[\"last_observed_work\"] for e in result[\"epochs\"]), default=0)\n        result[\"unscoped_events\"] = self.unscoped_events\n        # This is the final observed consume value, not a retained end-of-life object read.\n        result[\"last_observed_work_is_final_consume_value\"] = True\n        return result\n\n    def restore(self):\n        require(self.current is None, \"restore during analysis\")\n        intact = (self.module._AnalysisBudget.__init__ is self.observed_init\n                  and self.module._AnalysisBudget.consume is self.observed_consume)\n        self.module._AnalysisBudget.__init__ = self.original_init\n        self.module._AnalysisBudget.consume = self.original_consume\n        return bool(intact and self.module._AnalysisBudget.__init__ is self.original_init\n                    and self.module._AnalysisBudget.consume is self.original_consume\n                    and self.original_init.__code__ is self.original_codes[0]\n                    and self.original_consume.__code__ is self.original_codes[1])\n"
BUDGET_VALIDATE="\ndef validate_budget_metrics(metrics, identifier):\n    require(type(metrics) is dict and metrics[\"case\"] == identifier, \"budget case identity\")\n    epochs = metrics[\"epochs\"]\n    require(type(epochs) is list and len(epochs) > 0, \"original budget scope empty\")\n    require(type(metrics[\"epoch_count\"]) is int and metrics[\"epoch_count\"] == len(epochs),\n            \"budget epoch count\")\n    require(type(metrics[\"initialization_attempts\"]) is int\n            and metrics[\"initialization_attempts\"] == len(epochs)\n            and metrics[\"initialization_errors\"] == [], \"budget initialization coverage\")\n    require(metrics[\"unscoped_events\"] == 0 and type(metrics[\"unscoped_events\"]) is int\n            and metrics[\"last_observed_work_is_final_consume_value\"] is True, \"budget scope gaps\")\n    for index, entry in enumerate(epochs, 1):\n        for field in (\"epoch\", \"initial_work\", \"last_observed_work\", \"requested_units\",\n                      \"consume_calls\", \"completed_consume_calls\", \"exceptional_consume_calls\"):\n            require(type(entry[field]) is int and entry[field] >= 0, \"budget integer: \" + field)\n        require(entry[\"epoch\"] == index, \"budget creation sequence\")\n        require(entry[\"initial_work\"] + entry[\"requested_units\"] == entry[\"last_observed_work\"],\n                \"original requested work reconciliation\")\n        require(entry[\"consume_calls\"] == entry[\"completed_consume_calls\"]\n                + entry[\"exceptional_consume_calls\"], \"consume completion reconciliation\")\n        require(len(entry[\"consume_exceptions\"]) == entry[\"exceptional_consume_calls\"],\n                \"consume exception count\")\n        require(type(entry[\"origins\"]) is dict and type(entry[\"phase_units\"]) is dict,\n                \"budget disjoint maps\")\n        require(all(type(k) is str and type(v) is dict\n                    and type(v[\"calls\"]) is int and v[\"calls\"] >= 0\n                    and type(v[\"units\"]) is int and v[\"units\"] >= 0\n                    for k, v in entry[\"origins\"].items()), \"origin metrics types\")\n        require(all(type(k) is str and type(v) is int and v >= 0\n                    for k, v in entry[\"phase_units\"].items()), \"phase metrics types\")\n        require(sum(v[\"units\"] for v in entry[\"origins\"].values()) == entry[\"requested_units\"]\n                and sum(v[\"calls\"] for v in entry[\"origins\"].values()) == entry[\"consume_calls\"]\n                and sum(entry[\"phase_units\"].values()) == entry[\"requested_units\"],\n                \"disjoint original work sums\")\n        require(type(entry[\"creation_stack\"]) is list and entry[\"creation_stack\"], \"creation context\")\n        for event in entry[\"consume_exceptions\"]:\n            require(all(type(event[k]) is int for k in (\"before\", \"requested_units\", \"after\")),\n                    \"exception charge integers\")\n            require(event[\"before\"] + event[\"requested_units\"] == event[\"after\"],\n                    \"exceptional original charge\")\n            require(event[\"type\"] == \"InventoryError\"\n                    and event[\"message\"] == \"analysis work units exceed 262144\"\n                    and event[\"after\"] > CAPS[\"MAXIMUM_ANALYSIS_WORK_UNITS\"],\n                    \"unchanged canonical work refusal\")\n    require(type(metrics[\"requested_units_across_epochs\"]) is int\n            and metrics[\"requested_units_across_epochs\"] == sum(e[\"requested_units\"] for e in epochs),\n            \"all-epoch request sum\")\n    require(type(metrics[\"maximum_epoch_observed_work\"]) is int\n            and metrics[\"maximum_epoch_observed_work\"] == max(e[\"last_observed_work\"] for e in epochs),\n            \"maximum epoch observed work\")\n    return True\n"
PROBE_TAIL="\n    require({name: getattr(generator, name) for name in CAPS} == CAPS\n            and all(type(getattr(generator, name)) is int for name in CAPS), \"caps changed\")\n    semantic_failures, oracle_errors, analyzer_errors, accounting_errors = [], [], [], []\n    analyzed, projections = 0, 0\n    observer = BudgetObserver(generator)\n    observer.install()\n    methods_restored = False\n    try:\n        for scope, case in cases:\n            actuals, oracle_passed, oracle_error = [], False, None\n            try:\n                if scope == \"storage\":\n                    actual, oracle_passed = storage_oracle(case)\n                    actuals = [actual]\n                else:\n                    actuals, errors = project_oracles(case)\n                    oracle_passed = not errors\n                projections += len(actuals)\n            except Exception as error:\n                oracle_error = {\"type\": type(error).__name__, \"message\": str(error)}\n            review, analyzer_error, metrics, accounting_error = None, None, None, None\n            if not oracle_passed:\n                oracle_errors.append(case[\"id\"])\n            else:\n                observer.begin(case[\"id\"])\n                try:\n                    review = (storage_public_review(generator, case[\"source\"].encode(\"utf-8\"))\n                              if scope == \"storage\" else public_review(case[\"source\"].encode(\"utf-8\")))\n                    analyzed += 1\n                except Exception as error:\n                    analyzer_error = {\"type\": type(error).__name__, \"message\": str(error)}\n                    analyzer_errors.append(case[\"id\"])\n                finally:\n                    metrics = observer.end()\n                try:\n                    validate_budget_metrics(metrics, case[\"id\"])\n                except Exception as error:\n                    accounting_error = {\"type\": type(error).__name__, \"message\": str(error)}\n                    accounting_errors.append(case[\"id\"])\n            rows = review[\"receipt\"][\"expanded_rows\"] if review is not None else []\n            argv = [row[\"argv\"] for row in rows if row[\"capability_kind\"] == \"subprocess\"]\n            blockers = review[\"unresolved_dynamic_blockers\"] if review is not None else []\n            semantic_ok = bool(oracle_passed and review is not None\n                               and public_verdict(scope, case, argv, blockers))\n            if not semantic_ok:\n                semantic_failures.append(case[\"id\"])\n            print(json.dumps({\n                \"rewrite_gate_a_case\": case[\"id\"], \"original_pack\": scope,\n                \"classification\": case[\"classification\"],\n                \"source_sha256\": digest(case[\"source\"].encode(\"utf-8\")),\n                \"oracle_sha256\": digest(case[\"oracle_source\"].encode(\"utf-8\")),\n                \"unreachable_events\": case[\"unreachable_events\"],\n                \"expected_projections\": ([case[\"expected\"]] if scope == \"storage\" else case[\"witnesses\"]),\n                \"required_argv\": case[\"required_argv\"] if scope == \"storage\" else [[\"-m\", \"fixed\"]],\n                \"oracle_actuals\": actuals, \"oracle_passed\": oracle_passed, \"oracle_error\": oracle_error,\n                \"analyzer_error\": analyzer_error, \"argv\": argv, \"expanded_rows\": rows,\n                \"blockers\": blockers, \"semantic_passed\": semantic_ok,\n                \"receipt_sha256\": digest(canonical(review[\"receipt\"])) if review is not None else None,\n                \"budget_metrics\": metrics, \"accounting_error\": accounting_error,\n            }, allow_nan=False), flush=True)\n    finally:\n        methods_restored = observer.restore()\n    require(methods_restored, \"original budget methods not restored\")\n    require({name: getattr(generator, name) for name in CAPS} == CAPS\n            and all(type(getattr(generator, name)) is int for name in CAPS), \"caps changed during run\")\n    hashes(snapshot, manifest)\n    require(digest(checked(payload / \"manifest.json\").read_bytes()) == manifest_sha, \"manifest changed\")\n    summary = {\"rewrite_gate_a_summary\": True, \"schema\": SCHEMA, \"slot\": slot,\n               \"generator_sha256\": source_sha, \"pack_sha256\": PACK_HASHES, \"probe_sha256\": probe_sha,\n               \"plan_sha256\": PLAN_SHA, \"population_sha256\": POPULATION_SHA,\n               \"observer_map_sha256\": OBSERVER_MAP_SHA, \"planned_cases\": 6, \"case_count\": 6,\n               \"projections\": projections, \"analyzed_cases\": analyzed,\n               \"semantic_failures\": semantic_failures, \"oracle_errors\": oracle_errors,\n               \"analyzer_errors\": analyzer_errors, \"accounting_errors\": accounting_errors,\n               \"completed\": analyzed == 6 and projections == 8 and not oracle_errors\n                            and not analyzer_errors and not accounting_errors,\n               \"classifications\": {\"clean\": 2, \"refuse\": 3, \"permitted-refusal\": 1}, \"caps\": CAPS,\n               \"original_methods_restored\": methods_restored,\n               \"budget_scope\": \"all original creations/requests inside every complete public envelope\",\n               \"observer_overhead_is_not_original_charged_work\": True,\n               \"gate\": \"A\", \"GateB_not_run\": True}\n    print(json.dumps(summary, allow_nan=False), flush=True)\n    return int(bool(semantic_failures or oracle_errors or analyzer_errors or accounting_errors))\n\n\nif __name__ == \"__main__\":\n    raise SystemExit(main())\n"
RESULT_VALIDATE="\ndef validate_result(stdout, exit_code, setup, cases):\n    require(type(exit_code) is int, \"child exit exact integer\")\n    require(b\"\\r\" not in stdout and stdout.endswith(b\"\\n\"), \"stdout complete LF\")\n    lines = stdout.splitlines()\n    require(len(lines) == 8 and all(line.startswith(b\"{\") for line in lines),\n            \"exact identity/six-case/summary stream\")\n    records = [json.loads(line) for line in lines]\n    require(all(type(record) is dict for record in records), \"JSON record types\")\n    require(set(records[0]) == {\"identity_before_imports\"}, \"first pre-import identity\")\n    identity = records[0][\"identity_before_imports\"]\n    exe, version = SLOTS[setup[\"slot\"]]\n    require(identity[\"implementation\"] == \"cpython\" and identity[\"version_info\"] == list(version)\n            and all(type(n) is int for n in identity[\"version_info\"])\n            and Path(identity[\"executable\"]).resolve() == exe.resolve(), \"actual child runtime\")\n    require(identity[\"cwd\"] == setup[\"snapshot\"] and identity[\"environment\"] == setup[\"environment\"]\n            and identity[\"manifest_sha256\"] == setup[\"manifest_sha256\"]\n            and type(identity[\"verified_files\"]) is int\n            and identity[\"verified_files\"] == len(setup[\"before\"])\n            and identity[\"generator_sha256\"] == setup[\"generator_sha256\"]\n            and identity[\"probe_sha256\"] == PROBE_SHA, \"identity context\")\n    require(setup[\"environment\"] == environment(checked(Path(setup[\"temp\"]), True),\n                                                checked(Path(setup[\"snapshot\"]), True)),\n            \"replayed scrubbed environment\")\n    expected_command = [str(exe), \"-B\", \"-P\", str(Path(setup[\"snapshot\"]) / PAYLOAD / \"probe.py\"),\n                        setup[\"slot\"], setup[\"manifest_sha256\"], sha(canonical(setup[\"environment\"]))]\n    require(setup[\"command\"] == expected_command and type(setup[\"timeout_seconds\"]) is int\n            and setup[\"timeout_seconds\"] == TIMEOUT, \"replayed command/watchdog\")\n    for flag in (\"dont_write_bytecode=1\", \"no_user_site=1\", \"optimize=0\", \"isolated=0\",\n                 \"ignore_environment=0\", \"no_site=0\", \"safe_path=True\"):\n        require(flag in identity[\"flags\"], \"child flag: \" + flag)\n    observed = records[1:-1]\n    require(tuple(record.get(\"rewrite_gate_a_case\") for record in observed) == GATE_A_IDS,\n            \"exact frozen Gate A case order\")\n    semantic_failures, oracle_errors, analyzer_errors, accounting_errors = [], [], [], []\n    analyzed, projections = 0, 0\n    for actual, (scope, expected) in zip(observed, cases, strict=True):\n        require(actual[\"original_pack\"] == scope, \"original pack attribution\")\n        require(actual[\"classification\"] == expected[\"classification\"]\n                and actual[\"unreachable_events\"] == expected[\"unreachable_events\"],\n                \"original expectations drift\")\n        for field, key in ((\"source\", \"source_sha256\"), (\"oracle_source\", \"oracle_sha256\")):\n            require(actual[key] == sha(expected[field].encode(\"utf-8\")), \"original source/model identity\")\n        expected_projections = [expected[\"expected\"]] if scope == \"storage\" else expected[\"witnesses\"]\n        required_argv = expected[\"required_argv\"] if scope == \"storage\" else [[\"-m\", \"fixed\"]]\n        require(actual[\"expected_projections\"] == expected_projections\n                and actual[\"required_argv\"] == required_argv, \"original expected projection/argv\")\n        require(type(actual[\"oracle_actuals\"]) is list, \"Model actual container\")\n        projections += len(actual[\"oracle_actuals\"])\n        oracle_ok = (actual[\"oracle_error\"] is None and actual[\"oracle_actuals\"] == expected_projections\n                     and not any(event in witness[\"trace\"] for witness in actual[\"oracle_actuals\"]\n                                 for event in expected[\"unreachable_events\"]))\n        require(actual[\"oracle_passed\"] is oracle_ok, \"oracle result inconsistency\")\n        if not oracle_ok:\n            oracle_errors.append(expected[\"id\"])\n        if actual[\"analyzer_error\"] is not None:\n            analyzer_errors.append(expected[\"id\"])\n        has_receipt = actual[\"receipt_sha256\"] is not None\n        require(not has_receipt or valid_digest(actual[\"receipt_sha256\"]), \"public receipt digest\")\n        require(not has_receipt or (oracle_ok and actual[\"analyzer_error\"] is None),\n                \"receipt despite skipped/failed analyzer\")\n        if has_receipt:\n            analyzed += 1\n        require(type(actual[\"expanded_rows\"]) is list and type(actual[\"blockers\"]) is list,\n                \"public result containers\")\n        argv = [row[\"argv\"] for row in actual[\"expanded_rows\"] if row[\"capability_kind\"] == \"subprocess\"]\n        require(actual[\"argv\"] == argv, \"argv differs from original public rows\")\n        semantic_ok = bool(oracle_ok and actual[\"analyzer_error\"] is None and has_receipt\n                           and public_verdict(scope, expected, argv, actual[\"blockers\"]))\n        require(actual[\"semantic_passed\"] is semantic_ok, \"semantic inconsistency\")\n        if not semantic_ok:\n            semantic_failures.append(expected[\"id\"])\n        if actual[\"accounting_error\"] is not None:\n            accounting_errors.append(expected[\"id\"])\n        elif oracle_ok:\n            validate_budget_metrics(actual[\"budget_metrics\"], expected[\"id\"])\n        else:\n            require(actual[\"budget_metrics\"] is None, \"budget scope despite skipped Model\")\n    summary = records[-1]\n    require(summary.get(\"rewrite_gate_a_summary\") is True, \"final Gate A summary\")\n    require(summary[\"schema\"] == SCHEMA and summary[\"slot\"] == setup[\"slot\"]\n            and summary[\"generator_sha256\"] == setup[\"generator_sha256\"]\n            and summary[\"pack_sha256\"] == PACK_HASHES and summary[\"probe_sha256\"] == PROBE_SHA\n            and summary[\"plan_sha256\"] == PLAN_SHA and summary[\"population_sha256\"] == POPULATION_SHA\n            and summary[\"observer_map_sha256\"] == OBSERVER_MAP_SHA, \"summary pins\")\n    for key in (\"planned_cases\", \"case_count\"):\n        require(type(summary[key]) is int and summary[key] == 6, \"summary exact scope\")\n    require(type(summary[\"projections\"]) is int and summary[\"projections\"] == projections,\n            \"Model projection count\")\n    require(type(summary[\"analyzed_cases\"]) is int and summary[\"analyzed_cases\"] == analyzed,\n            \"analyzed count disagrees with public receipts\")\n    require(summary[\"classifications\"] == {\"clean\": 2, \"refuse\": 3, \"permitted-refusal\": 1}\n            and all(type(value) is int for value in summary[\"classifications\"].values())\n            and summary[\"caps\"] == CAPS and all(type(value) is int for value in summary[\"caps\"].values()),\n            \"classifications/caps\")\n    require(summary[\"semantic_failures\"] == semantic_failures and summary[\"oracle_errors\"] == oracle_errors\n            and summary[\"analyzer_errors\"] == analyzer_errors and summary[\"accounting_errors\"] == accounting_errors,\n            \"summary/case consistency\")\n    require(summary[\"original_methods_restored\"] is True\n            and summary[\"observer_overhead_is_not_original_charged_work\"] is True\n            and summary[\"gate\"] == \"A\" and summary[\"GateB_not_run\"] is True, \"scope/observer restoration\")\n    completed = (analyzed == 6 and projections == 8 and not oracle_errors\n                 and not analyzer_errors and not accounting_errors)\n    require(summary[\"completed\"] is completed, \"completion mismatch\")\n    require(exit_code == int(bool(semantic_failures or oracle_errors or analyzer_errors or accounting_errors)),\n            \"child exit mismatch\")\n    return {\"identity\": identity, \"summary\": summary, \"cases_observed\": len(observed),\n            \"completed\": completed, \"semantic_ok\": not semantic_failures,\n            \"accounting_ok\": not accounting_errors}\n"
PLAN="# Rewrite R1 Gate A harness v1 — frozen authoring scope\n\nStatus: authored for independent coordinator review; no payload invocation is authorized by this file.\n\nRun exactly the six ordered Gate A cases and eight harmless Model projections in\nrewrite-early-population-v1.json (SHA256\n3dd0ec8b6130b38d5138724b43e233e4e1a3e595f089c182291b00912d8423ce):\nshared-list-consumed, shared-list-dormant, class-adoption-unsafe, class-adoption-safe,\nhidden-cell-joined-reached, hidden-cell-joined-dormant. The classification vector is\nrefuse, clean, refuse, clean, refuse, permitted-refusal. No Gate B case, revised\nexpectation, synthetic fixture, old depth diagnostic or automatic expansion is included.\n\nThe four storage cases retain their original storage-composition public envelope,\ninventory, stable ID and Model runner. The two name-environment cases retain their\noriginal public24 envelope, inventory, stable ID and multi-witness Model runner.\nOnly the storage public function's definition name is changed to avoid a collision;\nits arguments and body remain exact. Sensitive source strings are passed as bytes\nto derive_design_review; only the separate existing harmless Models execute.\nThe full original pack bytes are pinned; selection cannot change their sources,\nmodels, labels, traces, unreachable-event obligations or permitted-refusal rule.\n\nThe candidate is a root-supplied retained generator .py under the task directory,\nbound to an explicit SHA256. The same controller supports exact r010 RED and a\nfuture reviewed core GREEN, without source-dependent expectations or dispatch.\nThe source's _AnalysisBudget.consume segment and all five cap values remain pinned.\nThe new core worktree is watched at an explicit approved SHA256; the previous v20\nworktree is additionally watched at its existing fixed SHA256. Neither is executed.\n\nThe controller runs on actual CPython3.11.15 with -I -S -B -P, creates a fresh\nD-local r010 clone/detach and private temp per invocation, overlays only the exact\ngenerator plus nine pinned/configured harness files, and hashes all1761 tracked\nfiles plus that overlay manifest before/after. The child runs actual3.11.15 or\n3.14.6 with -B -P, hash seed0, snapshot/src PYTHONPATH, no user site, scrubbed\nenvironment and absolute regular/non-reparse Git. Identity is emitted before\ncandidate import. Git setup/integrity commands and the direct child have60-second\nwatchdogs. Output names are create-exclusive; snapshots are not reused.\n\nA 3.14 invocation requires a hash-pinned, intact, complete, successful matching\n3.11 receipt with exact source/probe/control/population/accounting/watch pins.\nThe controller replays and rehashes the floor's raw identity, six case outcomes,\neight projections, all budget records, summary, setup, logs and snapshot. RED on\n3.11 is retained but never unlocks3.14. Each launch remains coordinator-owned.\n\nThe observer delegates original __init__ and consume exactly once with unchanged\narguments, returns and exceptions. All budget creations/requests inside every\nselected complete public call are observed, including definition-time/preflight,\ndirect entry, helper-return and ordinary review paths. Every original request,\nincluding a throwing request, is counted; no charge is invented at another refusal.\nRecords retain only scalar labels/counters/strings, never budget/AST/store objects\nor frames. Object IDs are local lookup keys replaced on each actual construction;\nhistorical epoch records cannot cause ID-reuse misattribution.\n\nPer epoch, initial + all requested units must equal the last observed consume\nvalue, with call/exception and disjoint caller/phase totals reconciled. The latter\nis not an end-of-life read of a retained budget. No unit, copy, traversal, reset,\nrefund, operation category or cap is introduced into production by observation.\nOriginal budget method objects/code are restored, cap values preserved. Observer\nstack inspection and bookkeeping add runtime overhead outside charged work;\nthese results are not timing/physical-work comparisons. This observation does\nnot certify the new core's operation accounting or prove no hidden work; source\nreview of that accounting remains a separate prerequisite.\n\nGate A uses the unchanged production work cap262144 and the other four caps.\nIt records headroom without imposing Gate B's196608 continuation criterion.\nPassing these six cases permits only the separately reviewed next checkpoint;\nit does not authorize Gate B, broad suites, integration, release or deployment.\n"

consume=next(n for n in top(baseline,"_AnalysisBudget").body if isinstance(n,ast.FunctionDef) and n.name=="consume")
consume_segment=ast.get_source_segment(baseline,consume)
consume_sha=sha(consume_segment.encode())
plan_raw=PLAN.encode()
plan_sha=sha(plan_raw)
observer_map={
 "schema":"pontius-rewrite-r1-budget-observer-map-v1","gate":"A","population_sha256":sha(population.encode()),
 "scope":"all original budgets/requests inside six complete public derive_design_review invocations",
 "hooks":[
  {"target":"_AnalysisBudget.__init__","delegation":"original exactly once, original args/kwargs/return/exception",
   "observations":"successful creation scalar work, full scalar creation context, per-case monotonic epoch; failed attempts visible"},
  {"target":"_AnalysisBudget.consume","delegation":"original exactly once, same units/default, return and exception",
   "observations":"original requested units, before/after scalar work, nearest caller/parent, nearest semantic stage, throwing request context"}],
 "original_consume_source_segment_sha256":consume_sha,
 "original_caps":json.loads(population)["original_caps"],
 "observer_class_source_sha256":sha(OBSERVER.encode()),
 "budget_reconciliation_source_sha256":sha(BUDGET_VALIDATE.encode()),
 "disjoint_views":{"origins":"immediate caller and parent; sum units/calls",
                   "phase_units":"nearest definition_time_protocol/unittest_preflight/source_ordered_helper_return/review_flow, otherwise other"},
 "inclusive_views":["creation_stack","throwing consume stack"],
 "retention":"scalars/strings/counters only; no budget, AST, state, object, frame, exception or cache retained",
 "object_id_reuse":"each original successful initialization replaces id lookup with new epoch; historical scalar records retained",
 "last_observed_work":"initial value for zero-request epoch, otherwise after final observed consume; not a retained budget finalization read",
 "coverage_limits":["candidate import precedes observation; no test/public-analysis import side effect is authorized",
                    "no new-core physical operation categories inferred; separate production accounting inspection required",
                    "unrecognized pipeline stage remains other, with exact caller/parent/creation stack",
                    "observer overhead is runtime work outside original charged units, not a runtime benchmark"],
 "no_production_changes":["no raised caps","no omitted or refunded original charge","no cache or budget objects retained",
                          "no reset/split","no semantic fallbacks or fixture-keyed dispatch"],
 "execution_authorized":False}
observer_raw=dump(observer_map); observer_sha=sha(observer_raw)
new_constants = (
    '\nPLAN_SHA = '+repr(plan_sha)+'\nOBSERVER_MAP_SHA = '+repr(observer_sha)+'\n'
    'CONSUME_SEGMENT_SHA = '+repr(consume_sha)+'\n'
)
probe = base_probe
start=probe.index("PACKS = {"); end=probe.index("\nPLAN_SHA =",start)
probe=probe[:start]+COMMON[:COMMON.index("\n\ndef case_canonical")].strip()+"\n"+probe[end:]
probe=once(probe,'PLAN_SHA = "3b330b732d99bdf02bae7b270a57f1d9cc0352fe1db573f5148c751084ad3f1a"',new_constants.strip())
probe=probe.replace(".original-composition-ten",".rewrite-r1-gate-a").replace("pontius-original-composition-ten-v1","pontius-rewrite-r1-gate-a-v1")
probe=once(probe,'"""Original ten frozen composition witnesses; no payload work on import."""','"""Frozen rewrite R1 Gate A: six original public cases/eight Models; no work on import."""')
probe=replace_top(probe,"load_cases",COMMON[COMMON.index("def case_canonical"):].strip())
probe=replace_top(probe,"scalar_oracle","")
probe=once(probe,"def public_review(generator, source):","def storage_public_review(generator, source):")
prefix=probe[:probe.index("def main():")]
prefix+=segment(name_probe,"public_review")+"\n"+segment(name_probe,"project_oracles")+"\n"+OBSERVER+"\n"+BUDGET_VALIDATE+"\n"
main=probe[probe.index("def main():"):]
main=main[:main.index('    require({name: getattr(generator, name) for name in CAPS} == CAPS, "caps changed")')]
main=once(main,"def main():","def main():\n    global generator")
main=main.replace("1768","1770")
main=once(main,'and run["plan_sha256"] == PLAN_SHA, "run input identity")',
          'and run["plan_sha256"] == PLAN_SHA and run["population_sha256"] == POPULATION_SHA\n'
          '            and run["observer_map_sha256"] == OBSERVER_MAP_SHA, "run input identity")')
main=once(main,'    require(digest(checked(payload / "plan.md").read_bytes()) == PLAN_SHA, "plan bytes")',
          '    require(digest(checked(payload / "plan.md").read_bytes()) == PLAN_SHA, "plan bytes")\n'
          '    require(digest(checked(payload / "observer-map.json").read_bytes()) == OBSERVER_MAP_SHA,\n'
          '            "observer map bytes")\n'
          '    population_raw = checked(payload / "population.json").read_bytes()\n'
          '    require(digest(population_raw) == POPULATION_SHA, "frozen population bytes")')
main=once(main,'    sys.stdout.reconfigure(newline="\\n")',
          '    source_text = checked(source_path).read_bytes().decode("utf-8")\n'
          '    source_tree = ast.parse(source_text, filename=str(source_path))\n'
          '    budgets = [n for n in source_tree.body if type(n) is ast.ClassDef and n.name == "_AnalysisBudget"]\n'
          '    require(len(budgets) == 1, "single original budget class")\n'
          '    consumes = [n for n in budgets[0].body if type(n) is ast.FunctionDef and n.name == "consume"]\n'
          '    require(len(consumes) == 1 and digest(ast.get_source_segment(source_text, consumes[0]).encode())\n'
          '            == CONSUME_SEGMENT_SHA, "original consume source unchanged")\n'
          '    del source_tree, budgets, consumes\n'
          '    sys.stdout.reconfigure(newline="\\n")')
main=once(main,'                        for scope, metadata in PACKS.items()})',
          '                        for scope, metadata in PACKS.items()}, population_raw)')
main=main.replace('"original_composition_generator"','"rewrite_r1_gate_a_generator"')
probe=prefix+main+PROBE_TAIL
probe_raw=probe.encode(); probe_sha=sha(probe_raw)
control=base_control
start=control.index("PACKS = {"); end=control.index("\nPLAN =",start)
control=control[:start]+COMMON[:COMMON.index("\n\ndef case_canonical")].strip()+"\n"+control[end:]
control=control.replace("original-composition-ten","rewrite-r1-gate-a")
control=once(control,'PROBE = CHECKS / "rewrite-r1-gate-a-probe-v1.py"',
             'PROBE = CHECKS / "rewrite-r1-probe-v1.py"')
control=once(control,'PROBE_SHA = "e2564b1d1d61c0a92e449f80eb5118eb72141b3fabd9022cf2b2881d1c56927e"',
             "PROBE_SHA = "+repr(probe_sha))
control=once(control,'PLAN = CHECKS / "rewrite-r1-gate-a-plan-v1.md"',
             'PLAN = CHECKS / "rewrite-r1-plan-v1.md"')
control=once(control,'PLAN_SHA = "3b330b732d99bdf02bae7b270a57f1d9cc0352fe1db573f5148c751084ad3f1a"',
             "PLAN_SHA = "+repr(plan_sha)+"\nOBSERVER_MAP_SHA = "+repr(observer_sha)+
             '\nOBSERVER_MAP = CHECKS / "rewrite-r1-observer-map-v1.json"\n'+
             'POPULATION = ROOT / "rewrite-early-population-v1.json"\n'+
             'CORE_WATCH = Path(r"D:\\Pontius-worktrees\\codex-v0a-i01-c-core-v1\\tools\\generate_test_inventory.py")')
control=replace_top(control,"load_cases",COMMON[COMMON.index("def case_canonical"):].strip()+"\n\n"+BUDGET_VALIDATE)
control=replace_top(control,"validate_result",RESULT_VALIDATE)
control=once(control,'    parser.add_argument("--control-sha256", required=True)',
             '    parser.add_argument("--control-sha256", required=True)\n'
             '    parser.add_argument("--worktree-sha256", required=True)')
control=once(control,'    source_sha = args.overlay_sha256',
             '    source_sha = args.overlay_sha256\n'
             '    require(valid_digest(args.worktree_sha256), "explicit core worktree watch digest")')
control=once(control,'             "probe_sha256": PROBE_SHA, "pack_sha256": PACK_HASHES, "plan_sha256": PLAN_SHA}',
             '             "probe_sha256": PROBE_SHA, "pack_sha256": PACK_HASHES, "plan_sha256": PLAN_SHA,\n'
             '             "population_sha256": POPULATION_SHA, "observer_map_sha256": OBSERVER_MAP_SHA,\n'
             '             "core_watch_source": str(CORE_WATCH), "core_watch_sha256": args.worktree_sha256}')
control=once(control,'        require(overlay.parent == ROOT and overlay.name.startswith("engineer-generator-")\n'
             '                and overlay.suffix == ".py", "candidate must be an explicit retained T source")',
             '        require(overlay.parent == ROOT and overlay.suffix == ".py",\n'
             '                "candidate must be an explicit retained T source")')
control=once(control,'                       "plan": PLAN, "control": control}',
             '                       "plan": PLAN, "control": control, "population": POPULATION,\n'
             '                       "observer_map": OBSERVER_MAP, "core_watch": CORE_WATCH}')
control=once(control,'                        **PACK_HASHES, "plan": PLAN_SHA, "control": args.control_sha256}',
             '                        **PACK_HASHES, "plan": PLAN_SHA, "control": args.control_sha256,\n'
             '                        "population": POPULATION_SHA, "observer_map": OBSERVER_MAP_SHA,\n'
             '                        "core_watch": args.worktree_sha256}')
control=once(control,'        cases = load_cases({scope: inputs[scope] for scope in PACKS})',
             '        cases = load_cases({scope: inputs[scope] for scope in PACKS}, inputs["population"])')
control=control.replace('"watch_source", "watch_sha256",',
                        '"watch_source", "watch_sha256", "core_watch_source", "core_watch_sha256",\n'
                        '                        "population_sha256", "observer_map_sha256",')
control=once(control,'and floor["exit"] in (0, 1) and "error" not in floor and "cleanup_error" not in floor,',
             'and floor["exit"] == 0 and floor["success"] is True and floor["semantic_ok"] is True\n'
             '                    and floor["accounting_ok"] is True and "error" not in floor\n'
             '                    and "cleanup_error" not in floor,')
control=control.replace('floor["payload_file_count"] == 7','floor["payload_file_count"] == 9')
control=control.replace('len(floor["before"]) == 1768','len(floor["before"]) == 1770')
control=once(control,'                    and floor["success"] is bool(floor["exit"] == 0), "floor output completion")',
             '                    and proof["accounting_ok"] is True and floor["accounting_ok"] is True\n'
             '                    and floor["success"] is True, "floor output completion")')
control=once(control,'                                   "control.py", "plan.md", "retained-source.py", "run.json"}',
             '                                   "control.py", "plan.md", "retained-source.py", "run.json",\n'
             '                                   "population.json", "observer-map.json"}')
control=once(control,'                    {" M " + GENERATOR, *("?? " + PAYLOAD + "/" + name\n'
             '                      for name in (*floor_payload_names, "manifest.json"))}, "floor status now changed")',
             '                    ({(" M " + GENERATOR)} if source_sha != BASE_GENERATOR_SHA else set()) |\n'
             '                    {"?? " + PAYLOAD + "/" + name for name in (*floor_payload_names, "manifest.json")},\n'
             '                    "floor status now changed")')
control=control.replace('"semantic_RED_permitted": True','"successful_floor_required": True')
control=once(control,'        require(git(snapshot, temp, "status", "--porcelain=v1", "-z", "--untracked-files=all")\n'
             '                == b" M tools/generate_test_inventory.py\\0", "extra overlay paths")',
             '        expected_overlay = b"" if source_sha == BASE_GENERATOR_SHA else b" M tools/generate_test_inventory.py\\0"\n'
             '        require(git(snapshot, temp, "status", "--porcelain=v1", "-z", "--untracked-files=all")\n'
             '                == expected_overlay, "extra overlay paths")')
control=once(control,'               "watch_source": str(WATCH), "watch_sha256": WATCH_SHA}',
             '               "watch_source": str(WATCH), "watch_sha256": WATCH_SHA,\n'
             '               "population_sha256": POPULATION_SHA, "observer_map_sha256": OBSERVER_MAP_SHA,\n'
             '               "core_watch_source": str(CORE_WATCH), "core_watch_sha256": args.worktree_sha256}')
control=once(control,'                 "retained-source.py": inputs["overlay"], "run.json": canonical(run),',
             '                 "retained-source.py": inputs["overlay"], "run.json": canonical(run),\n'
             '                 "population.json": inputs["population"], "observer-map.json": inputs["observer_map"],')
control=control.replace("len(before) == 1768", "len(before) == 1770")
control=once(control,'                expected_dirty = {" M " + GENERATOR, *("?? " + PAYLOAD + "/" + name for name in (*files, "manifest.json"))}',
             '                expected_dirty = ({" M " + GENERATOR} if source_sha != BASE_GENERATOR_SHA else set()) | {\n'
             '                    "?? " + PAYLOAD + "/" + name for name in (*files, "manifest.json")}')
control=once(control,'                              and receipt.get("semantic_ok") is True',
             '                              and receipt.get("semantic_ok") is True and receipt.get("accounting_ok") is True')
control=control.replace("Original ten composition replay control; authoring is not run permission.",
                        "Rewrite R1 Gate A snapshot control; authoring is not run permission.")
control=control.replace("Arguments: LABEL SLOT RETAINED_SOURCE_ABSOLUTE SOURCE_SHA --control-sha256 SHA",
                        "Arguments: LABEL SLOT RETAINED_SOURCE_ABSOLUTE SOURCE_SHA --control-sha256 SHA --worktree-sha256 SHA")
control_raw=control.encode(); control_sha=sha(control_raw)

# Static-only verification. No import/compile/execute of harness, candidates or Models.
ast.parse(probe); ast.parse(control)
p=json.loads(population)
actual=[]
pack_constants=ast.literal_eval(next(n.value for n in ast.parse(probe).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="PACKS" for t in n.targets)))
for scope, metadata in pack_constants.items():
    raw=(C/metadata["file"]).read_bytes()
    assert sha(raw)==metadata["sha256"]
    pack=json.loads(raw)
    assert pack["schema"]==metadata["schema"]
    assert pack["planned_cases"]==metadata["planned_cases"] and pack["planned_projections"]==metadata["planned_projections"]
    by_id={case["id"]:case for case in pack["cases"]}
    for ident in metadata["ids"]:
        case=by_id[ident]; bind=p["cases"][ident]
        assert sha(json.dumps(case,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode())==bind["case_record_canonical_sha256"]
        actual.append(case)
assert [c["id"] for c in actual]==p["gates"]["A"]["ordered_case_ids"]
def normalized_fn(src,name,replacement=None):
    n=top(src,name)
    if replacement: n.name=replacement
    return ast.dump(n,include_attributes=False)
preserved={
 "storage_public_function_body_and_signature":normalized_fn(base_probe,"public_review","storage_public_review")==normalized_fn(probe,"storage_public_review"),
 "storage_Model_runner":normalized_fn(base_probe,"storage_oracle")==normalized_fn(probe,"storage_oracle"),
 "name_public_function":normalized_fn(name_probe,"public_review")==normalized_fn(probe,"public_review"),
 "name_Model_runner":normalized_fn(name_probe,"project_oracles")==normalized_fn(probe,"project_oracles"),
 "load_cases_probe_control_equal":normalized_fn(probe,"load_cases")==normalized_fn(control,"load_cases"),
 "public_verdict_probe_control_equal":normalized_fn(probe,"public_verdict")==normalized_fn(control,"public_verdict"),
 "budget_validation_probe_control_equal":normalized_fn(probe,"validate_budget_metrics")==normalized_fn(control,"validate_budget_metrics"),
}
for name in ("checked","create","write_json","environment","git","file_hashes"):
    preserved["controller_"+name+"_unchanged"]=normalized_fn(base_control,name)==normalized_fn(control,name)
for name in ("require","digest","canonical","checked","hashes"):
    preserved["probe_"+name+"_unchanged"]=normalized_fn(base_probe,name)==normalized_fn(probe,name)
assert all(preserved.values()),preserved
assert len([n for n in ast.walk(ast.parse(probe)) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=="exec"])==2
assert len([n for n in ast.walk(ast.parse(probe)) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=="compile"])==2
for text in (probe,control):
    assert "scalar_oracle" not in text and "scalar-class-composition" not in text
    assert "1768" not in text and "helper65" not in text and "generator70" not in text
    assert "engineer-depth-budget-probe-v5.py" not in text and "tests-depth-budget-control-v5.py" not in text
diff_probe="".join(difflib.unified_diff(base_probe.splitlines(True),probe.splitlines(True),fromfile="original-composition-ten-probe-v1.py",tofile="rewrite-r1-probe-v1.py"))
diff_control="".join(difflib.unified_diff(base_control.splitlines(True),control.splitlines(True),fromfile="original-composition-ten-control-v1.py",tofile="rewrite-r1-control-v1.py"))
static={
 "schema":"pontius-rewrite-r1-harness-static-v1","gate":"A","payload_executed":False,
 "candidate_or_Model_imported":False,"source_fixtures_regenerated":False,
 "static_runtime":list(sys.version_info[:3]),"population_sha256":sha(population.encode()),
 "probe_sha256":probe_sha,"control_sha256":control_sha,"plan_sha256":plan_sha,
 "observer_map_sha256":observer_sha,"preservation":preserved,
 "original_consume_source_segment_sha256":consume_sha,
 "public_case_count":6,"Model_projections":8,"classifications":{"clean":2,"refuse":3,"permitted-refusal":1},
 "ordered_case_ids":p["gates"]["A"]["ordered_case_ids"],
 "original_inputs":{str(path.relative_to(T)):sha(path.read_bytes()) for path in (
    T/"rewrite-r1-base-generator.py",T/"rewrite-early-population-v1.json",
    C/"original-composition-ten-control-v1.py",C/"original-composition-ten-probe-v1.py",
    C/"name-environment-probe-v1.py",C/"storage-composition-cases-v1.json",C/"name-environment-cases-v1.json")},
 "worktree_watches_at_authoring":{str(path):sha(path.read_bytes()) for path in (
    Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-core-v1\tools\generate_test_inventory.py"),
    Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1\tools\generate_test_inventory.py"))},
 "deltas":{"probe":sha(diff_probe.encode()),"control":sha(diff_control.encode())},
 "unexecuted_status":"AST/hash/provenance checks only; runtime custody and observer behavior remain review/run obligations",
}
handoff=f"""# Rewrite R1 Gate A harness — authoring handoff v1

Frozen, unexecuted. Root independently reviews these bytes before any dispatch.
Exactly Gate A6/8 from population {sha(population.encode())}; no Gate B.

- Probe: rewrite-r1-probe-v1.py {probe_sha}
- Control: rewrite-r1-control-v1.py {control_sha}
- Plan: rewrite-r1-plan-v1.md {plan_sha}
- Observer map: rewrite-r1-observer-map-v1.json {observer_sha}
- Static proof: rewrite-r1-static-v1.json (hash printed on issuance)
- Exact controller/probe predecessor diffs retained separately.

Original public functions and Model runners compare AST-equal (storage public
definition name alone is changed). Source strings remain original pack bytes;
only harmless Models compile/execute in the future child. Both complete packs,
population, observer map, plan, control, probe and retained candidate are pinned.
The control's filesystem/environment/Git/hash primitives are unchanged.

Budget observation wraps only original init/consume; source consume segment
{consume_sha} is verified before import on both slots. All epochs,
throwing requests and nearest caller/phase totals are retained and reconciled.
No original calls or charges are suppressed, no budget/cache/AST/frame retained.
Observer overhead is disclosed; production-operation accounting is a separate
source-review obligation. Gate A applies unchanged production caps only.

Root-owned future CLI (not executed here):
D:/Pontius-tools/py311/Scripts/python.exe -I -S -B -P <control> LABEL 311 <retained-source.py> SOURCE_SHA --control-sha256 {control_sha} --worktree-sha256 APPROVED_CORE_WORKTREE_SHA
Dev additionally requires --floor-receipt <path> --floor-sha256 <SHA> and an
intact matching semantic/accounting GREEN floor result. RED cannot unlock dev.
Each invocation creates a new snapshot/temp and exclusive outputs. Old-W v20
watch remains; new core-W watch is explicit and pinned per invocation.
The unmodified r010 generator is legal RED input and expects no tracked diff.

No source/W/candidate edits, payload, Git mutation, installation, fixture generation,
new expected outcome, old diagnostic, or orchestration owner was invoked.
Static checks do not establish that this unexecuted harness works at runtime.
"""
files={
 "rewrite-r1-plan-v1.md":plan_raw,"rewrite-r1-observer-map-v1.json":observer_raw,
 "rewrite-r1-probe-v1.py":probe_raw,"rewrite-r1-control-v1.py":control_raw,
 "rewrite-r1-probe-v1-from-original-ten.diff":diff_probe.encode(),
 "rewrite-r1-control-v1-from-original-ten.diff":diff_control.encode(),
 "rewrite-r1-static-v1.json":dump(static),"rewrite-r1-handoff-v1.md":handoff.encode()}
assert not any((C/name).exists() for name in files)
for name,raw in files.items(): create(C/name,raw)
print(json.dumps({"issued":{name:{"sha256":sha(raw),"bytes":len(raw)} for name,raw in files.items()},
                  "static_checks":preserved,"payload_executed":False},indent=2))
