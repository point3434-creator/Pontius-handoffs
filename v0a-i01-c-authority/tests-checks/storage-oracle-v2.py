"""Independent stdlib dict/legacy-order oracle; importing this module runs no tests."""
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import sys

CASE_SHA256 = "3bd5678da334fb551c2f179906e8b4d2cf7a0b0e7a3779e0fad2fb4b4a9c548f"
CASE_PATH = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority\tests-checks\storage-oracle-cases-v2.json")
MAXIMUM = 262144
ABSENT = object()


@dataclass(frozen=True, slots=True, eq=False)
class Token:
    term: tuple
    certifiable: bool


class Values:
    def __init__(self):
        self.tokens = {}

    def atom(self, name):
        return self.intern(("atom", name), True)

    def intern(self, term, certifiable):
        if term not in self.tokens:
            self.tokens[term] = Token(term, certifiable)
        return self.tokens[term]

    def merge(self, name, supplied):
        if supplied and supplied[0] is not ABSENT and all(
                value is supplied[0] for value in supplied):
            return supplied[0], supplied[0].certifiable
        term = ("merge", name, tuple(
            ("missing",) if value is ABSENT else value.term for value in supplied))
        return self.intern(term, False), False


def encode(value):
    return ("missing",) if value is ABSENT else value.term


@dataclass
class Reference:
    values: dict
    no_work: dict

    def fork(self):
        return Reference(dict(self.values), dict(self.no_work))


def legacy_join(states, values):
    """Literal legacy empty/singleton/set-union control flow, ordinary dicts only."""
    if not states:
        return Reference({}, {}), {}, set()
    if len(states) == 1:
        return states[0].fork(), {}, set()
    names = set().union(*(state.values.keys() for state in states))
    result = Reference({}, {})
    arguments = {}
    required = set()
    for name in names:
        supplied = tuple(state.values.get(name, ABSENT) for state in states)
        arguments[name] = supplied
        value, certified = values.merge(name, supplied)
        result.values[name] = value
        result.no_work[name] = certified
        if not (supplied[0] is not ABSENT
                and all(item is supplied[0] for item in supplied)
                and all(state.no_work.get(name, False) for state in states)):
            required.add(name)
    return result, arguments, required


def validate_items(actual, version, reference):
    """Validation is deliberately outside the measured ordered_items transaction."""
    expected = tuple(reference.values.items())
    assert type(actual) is tuple, "ordered_items must return an immutable tuple"
    assert len(actual) == len(expected) == len(version)
    for got, want in zip(actual, expected, strict=True):
        assert type(got) is tuple and len(got) == 2
        assert got[0] == want[0] and got[1] is want[1], "legacy order/value identity differs"


def count_delta(before, after):
    return {key: after.get(key, 0) - before.get(key, 0)
            for key in before.keys() | after.keys()
            if after.get(key, 0) != before.get(key, 0)}


def run_case(api, case, *, fault=None, calibrated_cost=None, calibrated_counts=None):
    """Drive only the published primitive API; never inspect prototype internals."""
    meter = api.Meter(limit=MAXIMUM)
    values = Values()
    actual = {}
    expected = {}
    observations = []
    callback_records = []
    retained_reads = []
    fault_record = None
    costs = [{"phase": "meter_initialization", "units": meter.used,
              "counts": dict(meter.counts)}]

    def record(phase, before, counts_before, **details):
        item = {"phase": phase, "units": meter.used - before,
                "counts": count_delta(counts_before, dict(meter.counts)), **details}
        assert item["units"] >= 0, "meter refunded spent work"
        costs.append(item)
        return item

    def measured_order(name, phase, index):
        target, reference = actual[name], expected[name]
        before, counts_before = meter.used, dict(meter.counts)
        items = target.ordered_items()
        measured = record(phase, before, counts_before, op=index, state=name)
        # Nothing else touching the primitive runs inside the transaction measurement.
        validate_before, validate_counts = meter.used, dict(meter.counts)
        validate_items(items, target, reference)
        record("validation", validate_before, validate_counts, op=index, state=name)
        assert measured["units"] > 0 or not items, "nonempty ordered read did not meter entries"
        return items, measured

    for index, operation in enumerate(case["operations"]):
        kind = operation["op"]
        operation_before, operation_counts = meter.used, dict(meter.counts)
        if kind == "new":
            reference = Reference({}, {})
            version = api.NameVersion.empty(meter)
            for key, label, certified in operation["entries"]:
                assert type(key) is str
                value = values.atom(label)
                reference.values[key] = value
                reference.no_work[key] = certified
                version = version.set(key, value, no_work=certified)
        elif kind == "fork":
            reference = expected[operation["from"]].fork()
            version = actual[operation["from"]].fork()
        elif kind == "set":
            reference = expected[operation["from"]].fork()
            value = values.atom(operation["value"])
            reference.values[operation["key"]] = value
            reference.no_work[operation["key"]] = operation["no_work"]
            version = actual[operation["from"]].set(
                operation["key"], value, no_work=operation["no_work"])
        elif kind == "delete":
            reference = expected[operation["from"]].fork()
            if operation["expect_error"]:
                assert operation["key"] not in reference.values
                try:
                    actual[operation["from"]].delete(operation["key"])
                except KeyError:
                    pass
                else:
                    raise AssertionError("deleting absent key did not raise KeyError")
                record("construction", operation_before, operation_counts, op=index,
                       operation=kind, raised="KeyError")
                observations.append({"op": index, "kind": "missing-delete", "raised": "KeyError"})
                continue
            del reference.values[operation["key"]]
            del reference.no_work[operation["key"]]
            version = actual[operation["from"]].delete(operation["key"])
        elif kind == "join":
            references = [expected[name] for name in operation["inputs"]]
            reference, arguments, required = legacy_join(references, values)
            calls = []

            def merge(name, supplied):
                assert name in arguments, "callback received a key outside legacy union"
                converted = tuple(ABSENT if value is api.MISSING else value for value in supplied)
                wanted = arguments[name]
                assert len(converted) == len(wanted)
                assert all(a is b for a, b in zip(converted, wanted, strict=True)), (
                    "callback arguments changed input-state order/value identity")
                calls.append(name)
                value, certified = values.merge(name, converted)
                return api.Entry(value, no_work=certified)

            version = api.join(meter, [actual[name] for name in operation["inputs"]], merge)
            assert required <= set(calls), "changed/pending key skipped its merge callback"
            callback_records.append({
                "op": index, "id": operation["id"], "required_names": sorted(required),
                "actual_names": calls, "legacy_output_names": list(reference.values),
                "inter_name_callback_order_asserted": False,
            })
        elif kind in {"read", "fault_read"}:
            name = operation["state"]
            target = actual[name]
            if kind == "fault_read" and fault is not None:
                assert calibrated_cost is not None and calibrated_cost > 0
                assert calibrated_counts is not None
                allowed = {"first": 0, "middle": calibrated_cost // 2,
                           "last": calibrated_cost - 1}[fault]
                assert 0 <= allowed < calibrated_cost
                before, counts_before = meter.used, dict(meter.counts)
                meter.limit = before + allowed
                configured_limit = meter.limit
                assert configured_limit <= MAXIMUM
                try:
                    target.ordered_items()
                except api.BudgetExceeded:
                    used_after_failure = meter.used
                    assert used_after_failure > configured_limit and used_after_failure >= before
                else:
                    raise AssertionError("configured materialization fault did not raise BudgetExceeded")
                failed_cost = record("failed_order_attempt", before, counts_before,
                                     op=index, state=name)
                meter.limit = MAXIMUM
                retry_before = meter.used
                items, measured = measured_order(name, "ordered_retry", index)
                assert measured["units"] == calibrated_cost, (
                    "retry ordered_items charge differs from pristine identical version")
                assert measured["counts"] == calibrated_counts, (
                    "retry ordered_items public count delta differs from pristine identical version")
                fault_record = {
                    "offset": fault, "allowed_units": allowed, "configured_limit": configured_limit,
                    "used_before": before, "used_after_failure": used_after_failure,
                    "used_before_retry": retry_before, "retry_cost": measured["units"],
                    "retry_counts": measured["counts"], "failed_cost": failed_cost,
                    "clean_first_read_cost": calibrated_cost,
                    "clean_first_read_counts": calibrated_counts, "limit_restored": meter.limit,
                    "validation_reads_excluded_from_equivalence": True,
                }
            else:
                items, measured = measured_order(name, "terminal_order", index)
                if kind == "fault_read":
                    fault_record = {"calibration_cost": measured["units"],
                                    "calibration_counts": measured["counts"]}
            prior_encoded = tuple((key, encode(value)) for key, value in items)
            retained_reads.append((items, prior_encoded))
            repeat_costs = []
            for _ in range(operation["repeats"] - 1):
                again, repeat = measured_order(name, "repeated_order", index)
                repeat_costs.append(repeat)
                assert again == items
            observations.append({"op": index, "kind": kind, "state": name,
                                 "ordered": prior_encoded, "first_cost": measured,
                                 "repeat_costs": repeat_costs})
            continue
        elif kind == "get":
            name = operation["state"]
            default = values.atom(operation["default"])
            for key in operation["keys"]:
                got = actual[name].get(key, default)
                want = expected[name].values.get(key, default)
                assert got is want, "get/default identity differs from dict"
                observations.append({"op": index, "kind": "get", "key": key, "value": encode(got)})
            record("lookup_audit", operation_before, operation_counts, op=index, state=name)
            continue
        else:
            raise AssertionError("unknown scheduled operation")
        assert operation["id"] not in actual, "version ids must be create-only"
        actual[operation["id"]] = version
        expected[operation["id"]] = reference
        record("joins" if kind == "join" else "construction",
               operation_before, operation_counts, op=index, operation=kind)
        validate_before, validate_counts = meter.used, dict(meter.counts)
        assert len(version) == len(reference.values)
        record("validation", validate_before, validate_counts, op=index)
    # Final reads deliberately occur after all scheduled merges/edits, preserving lazy-order coverage.
    retained = []
    for name in actual:
        items, measured = measured_order(name, "retained_order_audit", "final")
        retained.append({"version": name, "ordered": [(key, encode(value)) for key, value in items],
                         "read_cost": measured})
    for items, old in retained_reads:
        assert tuple((key, encode(value)) for key, value in items) == old, "old returned snapshot changed"
    assert 0 <= meter.used <= MAXIMUM and meter.limit == MAXIMUM
    assert sum(item["units"] for item in costs) == meter.used, "phase cost accounting gap"
    phase_units = {}
    for item in costs:
        phase_units[item["phase"]] = phase_units.get(item["phase"], 0) + item["units"]
    return {"case": case["id"], "phase": fault or "baseline",
            "family": case.get("family", "compatibility"), "parameters": case.get("parameters"),
            "operations": len(case["operations"]), "observations": observations,
            "callbacks": callback_records, "retained_versions": retained,
            "fault": fault_record, "meter_used": meter.used, "meter_counts": dict(meter.counts),
            "phase_units": phase_units, "cost_events": costs}

def verify_storage(api, case_path=CASE_PATH):
    """Entry point for the coordinator's isolated child; never auto-runs on import."""
    raw = Path(case_path).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == CASE_SHA256
    pack = json.loads(raw)
    assert len(pack["cases"]) == 28
    assert sum(len(case["operations"]) for case in pack["cases"]) == 336
    assert len({case["id"] for case in pack["cases"]}) == 28
    seed = os.environ.get("PYTHONHASHSEED")
    assert seed in {"0", "1", "17"}, "coordinator must select the hash seed before child start"
    assert sys.version_info[:3] in {(3, 11, 15), (3, 14, 6)}
    assert sys.dont_write_bytecode and sys.flags.safe_path
    results = []
    failures = []
    planned_runs = 34
    for case in pack["cases"]:
        try:
            baseline = run_case(api, case)
            results.append(baseline)
            print(json.dumps({"storage_oracle_case": baseline}), flush=True)
            fault_operations = [op for op in case["operations"] if op["op"] == "fault_read"]
            for operation in fault_operations:
                for offset in operation["offsets"]:
                    trial = run_case(api, case, fault=offset,
                                     calibrated_cost=baseline["fault"]["calibration_cost"],
                                     calibrated_counts=baseline["fault"]["calibration_counts"])
                    results.append(trial)
                    print(json.dumps({"storage_oracle_case": trial}), flush=True)
        except Exception as error:
            failure = {"case": case["id"], "type": type(error).__name__, "message": str(error)}
            failures.append(failure)
            print(json.dumps({"storage_oracle_failure": failure}), flush=True)
    summary = {
        "storage_oracle_summary": "stdlib-dict-and-legacy-set-union-v2",
        "case_pack_sha256": CASE_SHA256, "runtime": list(sys.version_info[:3]),
        "hash_seed": seed, "hash_alpha": hash("alpha"),
        "planned_cases": 28, "planned_runs": planned_runs, "completed_runs": len(results),
        "failures": failures, "all_completed": len(results) == planned_runs and not failures,
        "maximum_meter_limit": MAXIMUM,
        "prototype_internals_inspected": False,
        "expected_order_computed_in_this_child": True,
        "pure_callback_inter_name_order_asserted": False,
    }
    print(json.dumps(summary), flush=True)
    assert summary["all_completed"], "storage oracle did not complete every planned run"
    return summary
