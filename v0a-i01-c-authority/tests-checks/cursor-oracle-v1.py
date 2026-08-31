"""Independent builtin-dict oracle for the frozen cursor extension; no autorun."""
from __future__ import annotations

import gc
import hashlib
import json
import os
from pathlib import Path
import sys
import traceback
import weakref

MAXIMUM = 262144
CASE_SHA256 = "ecddd020ffb2a0d85e624aeb7fb544f631b302839f9a5f3542c998b36c37ac61"
CASE_PATH = Path(__file__).with_name("cursor-oracle-cases-v1.json")
ABSENT = object()
KEY_VIEW_TYPE = type({}.keys())


class UnmetStructuralPrecondition(AssertionError):
    pass


class Value:
    __slots__ = ("term", "__weakref__")

    def __init__(self, term):
        self.term = term


class Values:
    def __init__(self):
        self.known = {}

    def intern(self, term):
        if term not in self.known:
            self.known[term] = Value(term)
        return self.known[term]

    def atom(self, label):
        return self.intern(("atom", label))

    def merge(self, name, supplied):
        first = supplied[0]
        if first is not ABSENT and all(value is first for value in supplied):
            return first, True
        term = ("join", name, tuple(
            ("absent",) if value is ABSENT else value.term for value in supplied))
        return self.intern(term), False


class Reference:
    def __init__(self, values=None, no_work=None):
        self.values = dict(values or {})
        self.no_work = dict(no_work or {})

    def fork(self):
        return Reference(self.values, self.no_work)

    def set(self, key, value, no_work):
        self.values[key] = value
        self.no_work[key] = no_work

    def delete(self, key):
        del self.values[key]
        del self.no_work[key]


def legacy_join(states, values):
    if not states:
        return Reference(), {}, set()
    if len(states) == 1:
        return states[0].fork(), {}, set()
    result, arguments, required = Reference(), {}, set()
    # This is deliberately the actual legacy algorithm, evaluated in this child.
    for name in set().union(*(state.values.keys() for state in states)):
        supplied = tuple(state.values.get(name, ABSENT) for state in states)
        arguments[name] = supplied
        first = supplied[0]
        if (first is ABSENT or any(value is not first for value in supplied)
                or any(not state.no_work.get(name, False) for state in states)):
            required.add(name)
        value, certified = values.merge(name, supplied)
        result.set(name, value, certified)
    return result, arguments, required


def count_delta(after, before):
    return {key: after.get(key, 0) - before.get(key, 0)
            for key in sorted(set(after) | set(before))
            if after.get(key, 0) != before.get(key, 0)}


class Ledger:
    def __init__(self, api, report):
        self.meter = api.Meter(limit=MAXIMUM)
        self.events = []
        self.report = report
        report["cost_events"] = self.events
        self.events.append({"phase": "meter-init", "operation": "Meter",
                            "units": self.meter.used, "counts": dict(self.meter.counts)})

    def call(self, phase, operation, function):
        before, counts = self.meter.used, dict(self.meter.counts)
        event = {"phase": phase, "operation": operation}
        try:
            return function()
        except BaseException as error:
            event["raised"] = type(error).__name__
            raise
        finally:
            event["units"] = self.meter.used - before
            event["counts"] = count_delta(self.meter.counts, counts)
            assert event["units"] >= 0, "meter refunded work"
            self.events.append(event)

    def finish(self):
        meter = self.meter
        assert meter.limit == MAXIMUM
        assert 0 <= meter.used <= MAXIMUM
        assert sum(event["units"] for event in self.events) == meter.used
        phase_units = {}
        for event in self.events:
            phase = event["phase"]
            phase_units[phase] = phase_units.get(phase, 0) + event["units"]
        self.report.update(meter_used=meter.used, meter_counts=dict(meter.counts),
                           phase_units=phase_units, maximum_meter_limit=MAXIMUM)


def checked_keys(got, reference):
    assert type(got) is KEY_VIEW_TYPE, "keys did not return a genuine dict_keys view"
    assert tuple(got) == tuple(reference.values), "key order/membership differs from dict"


def checked_items(got, reference):
    assert isinstance(got, tuple), "ordered_items did not return a tuple"
    assert len(got) == len(reference.values)
    for pair, (key, value) in zip(got, reference.values.items(), strict=True):
        assert isinstance(pair, tuple) and len(pair) == 2
        assert pair[0] == key and pair[1] is value, "item order or value identity differs"


def encoded_items(items):
    return [(name, value.term) for name, value in items]


def expand_operations(operations):
    for operation in operations:
        if operation["op"] != "repeat":
            yield operation
            continue
        def substitute(value, index):
            if isinstance(value, str):
                return value.format(i=index, next=index + 1)
            if isinstance(value, list):
                return [substitute(item, index) for item in value]
            if isinstance(value, dict):
                return {key: substitute(item, index) for key, item in value.items()}
            return value
        for index in range(operation["count"]):
            for item in operation["body"]:
                yield substitute(item, index)


class Harness:
    def __init__(self, api, report):
        self.api, self.report = api, report
        self.ledger = Ledger(api, report)
        self.values = Values()
        self.actual, self.expected, self.kinds = {}, {}, {}
        self.saved_views, self.saved_items = [], []
        self.raw_sets = 0
        report["observations"], report["callbacks"] = [], []
        report["auxiliary_meters"] = []

    def save(self, name, actual, expected, kind):
        assert name not in self.actual, "state identifier reused"
        public_type = self.api.NameCursor if kind == "cursor" else self.api.NameVersion
        assert isinstance(actual, public_type), "operation returned the wrong public state type"
        self.actual[name], self.expected[name], self.kinds[name] = actual, expected, kind

    def read(self, target, kind, repeats=1, phase=None):
        actual, reference = self.actual[target], self.expected[target]
        for index in range(repeats):
            selected = phase or (("terminal-" if index == 0 else "repeated-") + kind)
            got = self.ledger.call(selected, kind, getattr(actual, kind))
            if kind == "keys":
                checked_keys(got, reference)
                self.saved_views.append((got, tuple(reference.values)))
                encoded = list(got)
            else:
                checked_items(got, reference)
                self.saved_items.append((got, tuple(reference.values.items())))
                encoded = encoded_items(got)
            self.report["observations"].append(
                {"state": target, "operation": kind, "phase": selected, "value": encoded})

    def join(self, operation):
        names = operation["inputs"]
        refs = [self.expected[name] for name in names]
        reference, arguments, required = legacy_join(refs, self.values)
        calls = []
        def merge(name, supplied):
            assert name in arguments, "callback key absent from legacy union"
            converted = tuple(ABSENT if item is self.api.MISSING else item for item in supplied)
            wanted = arguments[name]
            assert len(converted) == len(wanted)
            assert all(a is b for a, b in zip(converted, wanted, strict=True)), (
                "callback input-state order or current effective value identity changed")
            calls.append(name)
            value, certified = self.values.merge(name, converted)
            return self.api.Entry(value, no_work=certified)
        got = self.ledger.call("joins", "join", lambda: self.api.join(
            self.ledger.meter, [self.actual[name] for name in names], merge))
        assert required <= set(calls), "changed/pending name skipped callback"
        self.report["callbacks"].append({
            "state": operation["id"], "required_names": sorted(required),
            "actual_names": calls, "legacy_order": list(reference.values),
            "inter_name_invocation_order_asserted": False})
        self.save(operation["id"], got, reference, "version")

    def reject_join(self, inputs, label):
        calls = []
        def merge(name, supplied):
            calls.append(name)
            return self.api.Entry(self.values.atom("unexpected"))
        try:
            self.ledger.call("invalid-boundary", label, lambda: self.api.join(
                self.ledger.meter, inputs, merge))
        except self.api.BudgetExceeded:
            raise AssertionError("budget exhaustion is not invalid-input rejection")
        except Exception as error:
            assert not calls, "invalid join invoked a callback before rejection"
            self.report["observations"].append(
                {"operation": label, "refusal": type(error).__name__,
                 "exception_class_is_not_contract_assertion": True})
        else:
            raise AssertionError("invalid join input was accepted")

    def operation(self, operation):
        op = operation["op"]
        api, ledger = self.api, self.ledger
        if op == "new":
            empty = ledger.call("construction", "empty", lambda: api.NameVersion.empty(ledger.meter))
            cursor = ledger.call("construction", "NameCursor", lambda: api.NameCursor(empty))
            self.save(operation["id"], cursor, Reference(), "cursor")
            for key, label, certified in operation["entries"]:
                self.operation({"op": "set", "target": operation["id"], "key": key,
                                "value": label, "no_work": certified})
        elif op in {"set", "delete"}:
            target, key = operation["target"], operation["key"]
            assert type(key) is str and self.kinds[target] == "cursor"
            cursor, reference = self.actual[target], self.expected[target]
            if op == "set":
                value = self.values.atom(operation["value"])
                if not operation["no_work"]:
                    self.raw_sets += 1
                use_default = not operation["no_work"] and self.raw_sets % 2 == 1
                if use_default:
                    result = ledger.call("private-writes", "set-default",
                                         lambda: cursor.set(key, value))
                else:
                    result = ledger.call("private-writes", "set", lambda: cursor.set(
                        key, value, no_work=operation["no_work"]))
                assert result is None, "mutable set must return None"
                reference.set(key, value, operation["no_work"])
            elif operation.get("expect_error", False):
                assert key not in reference.values
                try:
                    ledger.call("private-writes", "delete-missing", lambda: cursor.delete(key))
                except KeyError:
                    pass
                else:
                    raise AssertionError("absent delete did not raise KeyError")
            else:
                result = ledger.call("private-writes", "delete", lambda: cursor.delete(key))
                assert result is None, "mutable delete must return None"
                reference.delete(key)
        elif op in {"snapshot", "fork", "cursor_from"}:
            target = operation["target"]
            if op == "cursor_from":
                assert self.kinds[target] == "version"
                got = ledger.call("construction", "NameCursor", lambda: api.NameCursor(self.actual[target]))
                kind = "cursor"
            else:
                assert self.kinds[target] == "cursor"
                got = ledger.call("publication" if op == "snapshot" else "forks",
                                  op, getattr(self.actual[target], op))
                kind = "version" if op == "snapshot" else "cursor"
            self.save(operation["id"], got, self.expected[target].fork(), kind)
        elif op in {"keys", "items"}:
            self.read(operation["target"], "keys" if op == "keys" else "ordered_items",
                      operation["repeats"])
        elif op == "get":
            target = operation["target"]
            default = self.values.atom(operation["default"])
            for key in operation["keys"]:
                got = ledger.call("lookups", "get",
                                  lambda: self.actual[target].get(key, default))
                assert got is self.expected[target].values.get(key, default)
        elif op == "join":
            self.join(operation)
        elif op == "reject_cursor_join":
            self.reject_join([self.actual[name] for name in operation["inputs"]],
                             "join-mutable-cursor")
        elif op == "reject_foreign_join":
            auxiliary = {}
            foreign = Ledger(api, auxiliary)
            other = foreign.call("construction", "empty",
                                 lambda: api.NameVersion.empty(foreign.meter))
            value = self.values.atom("foreign")
            other = foreign.call("construction", "set",
                                 lambda: other.set("foreign", value, no_work=True))
            self.reject_join([self.actual[operation["target"]], other], "join-foreign-meter")
            got = foreign.call("retained-audit", "ordered_items", other.ordered_items)
            checked_items(got, Reference({"foreign": value}, {"foreign": True}))
            foreign.finish()
            self.report["auxiliary_meters"].append(auxiliary)
        else:
            raise AssertionError("unknown scheduled operation: " + op)

    def audit(self):
        for name in self.actual:
            self.read(name, "keys", phase="retained-audit")
            self.read(name, "ordered_items", phase="retained-audit")
            got = self.ledger.call("validation", "len", lambda: len(self.actual[name]))
            assert got == len(self.expected[name].values)
        for view, expected in self.saved_views:
            assert tuple(view) == expected, "previously returned key view changed"
        for items, expected in self.saved_items:
            assert len(items) == len(expected)
            for (name, value), (old_name, old_value) in zip(items, expected, strict=True):
                assert name == old_name and value is old_value, "old returned items changed"


def ordinary_case(api, case, report):
    harness = Harness(api, report)
    operations = list(expand_operations(case["operations"]))
    report["expanded_operations"] = len(operations)
    for operation in operations:
        harness.operation(operation)
    harness.audit()
    harness.ledger.finish()


def retention_case(api, case, report):
    ledger = Ledger(api, report)
    empty = ledger.call("construction", "empty", lambda: api.NameVersion.empty(ledger.meter))
    cursor = ledger.call("construction", "NameCursor", lambda: api.NameCursor(empty))
    sentinel = Value(("weak-sentinel", case["id"]))
    weak = weakref.ref(sentinel)
    assert ledger.call("private-writes", "set",
                       lambda: cursor.set("victim", sentinel, no_work=True)) is None
    if case["kind"] == "retention_private":
        del sentinel
        latest = None
        for index in range(case["writes"]):
            latest = Value(("replacement", index))
            assert ledger.call("private-writes", "set",
                               lambda: cursor.set("victim", latest, no_work=True)) is None
        gc.collect()
        report["private_sentinel_released"] = weak() is None
        assert weak() is None, "never-published overwritten private value retained"
        assert ledger.call("lookups", "get", lambda: cursor.get("victim")) is latest
    else:
        saved = ledger.call("publication", "snapshot-positive-owner", cursor.snapshot)
        del sentinel
        before_compaction = ledger.meter.counts.get("compaction_entry_visits", 0)
        for index in range(case["publications"]):
            latest = Value(("replacement", index))
            assert ledger.call("private-writes", "set",
                               lambda: cursor.set("victim", latest, no_work=True)) is None
            # Each returned intermediate version is intentionally discarded.
            ledger.call("publication", "snapshot-discarded", cursor.snapshot)
        compaction = ledger.meter.counts.get("compaction_entry_visits", 0) - before_compaction
        report["successful_compaction_entry_visits"] = compaction
        report["structural_precondition_met"] = compaction > 0
        if compaction <= 0:
            raise UnmetStructuralPrecondition(
                "no successful full-compaction work observed; history leak inference withheld")
        gc.collect()
        report["retained_snapshot_positive_owner"] = weak() is not None
        assert weak() is not None, "retained original snapshot lost its value"
        assert ledger.call("lookups", "positive-owner-get",
                           lambda: saved.get("victim")) is weak()
        assert ledger.call("lookups", "current-get", lambda: cursor.get("victim")) is latest
        del saved
        gc.collect()
        report["sentinel_released_after_old_snapshot_dropped"] = weak() is None
        assert weak() is None, "obsolete value retained after compaction and old snapshot release"
    expected = Reference({"victim": latest}, {"victim": True})
    for index in range(3):
        items = ledger.call("terminal-items" if index == 0 else "repeated-items",
                            "ordered_items", cursor.ordered_items)
        checked_items(items, expected)
    ledger.finish()


def prepare_atomic(api, case, report):
    h = Harness(api, report)
    h.operation({"op": "new", "id": "c",
                 "entries": [["alpha", "A", True], ["beta", "B", True], ["gamma", "G", True]]})
    h.operation({"op": "snapshot", "target": "c", "id": "old"})
    h.read("c", "keys", phase="preparation-read")
    h.read("c", "ordered_items", phase="preparation-read")
    for index in range(case["prepared_publications"]):
        h.operation({"op": "set", "target": "c", "key": "step" + str(index),
                     "value": "step" + str(index), "no_work": True})
        h.ledger.call("preparation-publication", "snapshot-discarded", h.actual["c"].snapshot)
    h.operation({"op": "set", "target": "c", "key": "alpha", "value": "tail-A", "no_work": True})
    h.operation({"op": "delete", "target": "c", "key": "beta"})
    h.operation({"op": "set", "target": "c", "key": "tail", "value": "tail-T", "no_work": False})
    return h


def public_signature(events):
    return [{key: value for key, value in event.items()}
            for event in events]


def atomic_case(api, case, report, offset=None, baseline=None):
    h = prepare_atomic(api, case, report)
    ledger, cursor = h.ledger, h.actual["c"]
    operation = case["operation"]
    report["preparation_costs"] = public_signature(ledger.events)
    if offset is not None:
        assert report["preparation_costs"] == baseline["preparation_costs"]
        calibration = baseline["calibration"]
        cost = calibration["units"]
        assert cost > 0
        allowance = {"first": 0, "middle": cost // 2, "last": cost - 1}[offset]
        before = ledger.meter.used
        configured = before + allowance
        assert 0 <= allowance < cost and configured <= MAXIMUM
        ledger.meter.limit = configured
        try:
            ledger.call("failed-operation", operation, getattr(cursor, operation))
        except api.BudgetExceeded:
            spent = ledger.meter.used
            assert spent > configured and spent >= before
        else:
            raise AssertionError("configured primitive fault did not raise BudgetExceeded")
        failed_event = dict(ledger.events[-1])
        ledger.meter.limit = MAXIMUM
        retry_before = ledger.meter.used
        got = ledger.call("retry-operation", operation, getattr(cursor, operation))
        measured = ledger.events[-1]
        assert measured["units"] == calibration["units"], "same-cursor retry units changed"
        assert measured["counts"] == calibration["counts"], "same-cursor retry category delta changed"
        report["fault"] = {"offset": offset, "allowed_units": allowance,
                           "configured_limit": configured, "used_before": before,
                           "used_after_failure": spent, "used_before_retry": retry_before,
                           "failed_operation": failed_event, "retry_units": measured["units"],
                           "retry_counts": measured["counts"], "restored_limit": MAXIMUM,
                           "validation_reads_excluded": True}
    else:
        got = ledger.call("target-operation", operation, getattr(cursor, operation))
        measured = ledger.events[-1]
    report["calibration"] = {"units": measured["units"], "counts": measured["counts"]}
    assert measured["units"] > 0, "prepared operation supplied no injectable charged work"
    after_target = len(ledger.events)
    expected = h.expected["c"].fork()
    if operation in {"snapshot", "fork"}:
        h.save("operation-result", got, expected,
               "version" if operation == "snapshot" else "cursor")
        h.read("operation-result", "keys", phase="result-validation")
        h.read("operation-result", "ordered_items", phase="result-validation")
    elif operation == "keys":
        checked_keys(got, expected)
        h.saved_views.append((got, tuple(expected.values)))
    else:
        checked_items(got, expected)
        h.saved_items.append((got, tuple(expected.values.items())))
    # Identical bounded continuation, including mutation and later publication.
    h.operation({"op": "fork", "target": "c", "id": "branch"})
    h.operation({"op": "set", "target": "c", "key": "after-parent",
                 "value": "after-parent", "no_work": True})
    h.operation({"op": "delete", "target": "branch", "key": "alpha"})
    h.operation({"op": "set", "target": "branch", "key": "alpha",
                 "value": "after-child", "no_work": False})
    h.operation({"op": "snapshot", "target": "c", "id": "parent-final"})
    h.operation({"op": "snapshot", "target": "branch", "id": "branch-final"})
    for name in ("parent-final", "branch-final"):
        h.read(name, "keys", repeats=2, phase="continuation-read")
        h.read(name, "ordered_items", repeats=2, phase="continuation-read")
    h.audit()
    report["after_target_costs"] = public_signature(ledger.events[after_target:])
    report["continuation_observations"] = list(report["observations"])
    if offset is not None:
        assert report["after_target_costs"] == baseline["after_target_costs"], (
            "same-cursor post-retry validation/fork/write/read costs differ from pristine")
        assert report["continuation_observations"] == baseline["continuation_observations"], (
            "same-cursor continuation outputs differ from pristine")
    ledger.finish()


def verify_cursor(api, case_path=CASE_PATH):
    """Coordinator entrypoint. Does not invoke or replace the separate old oracle."""
    raw = Path(case_path).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == CASE_SHA256
    pack = json.loads(raw)
    assert pack["planned_cases"] == 16 and pack["planned_runs"] == 28
    assert len(pack["cases"]) == 16
    assert len({case["id"] for case in pack["cases"]}) == 16
    assert sum(case["kind"] == "atomic" for case in pack["cases"]) == 4
    assert pack["maximum_meter_limit"] == MAXIMUM
    seed = os.environ.get("PYTHONHASHSEED")
    assert seed in {"0", "1", "17"}
    assert sys.version_info[:3] in {(3, 11, 15), (3, 14, 6)}
    assert sys.dont_write_bytecode and sys.flags.safe_path
    completed, failures = [], []
    for case in pack["cases"]:
        baseline = None
        offsets = [None] + (case["offsets"] if case["kind"] == "atomic" else [])
        for offset in offsets:
            report = {"case": case["id"], "phase": offset or "baseline", "kind": case["kind"]}
            try:
                if case["kind"] == "operations":
                    ordinary_case(api, case, report)
                elif case["kind"].startswith("retention_"):
                    retention_case(api, case, report)
                elif case["kind"] == "atomic":
                    atomic_case(api, case, report, offset, baseline)
                else:
                    raise AssertionError("unknown case family")
                completed.append(report)
                print(json.dumps({"cursor_oracle_case": report}), flush=True)
                if offset is None:
                    baseline = report
            except Exception as error:
                failure = {"case": case["id"], "phase": offset or "baseline",
                           "type": type(error).__name__, "message": str(error),
                           "traceback": traceback.format_exc(), "partial_report": report}
                failures.append(failure)
                print(json.dumps({"cursor_oracle_failure": failure}), flush=True)
                # Stop this child at its first mechanism failure; preserve partial costs.
                break
        if failures:
            break
    summary = {
        "cursor_oracle_summary": "stdlib-dict-and-legacy-set-union-cursor-v1",
        "case_pack_sha256": CASE_SHA256, "runtime": list(sys.version_info[:3]),
        "hash_seed": seed, "planned_cases": 16, "planned_runs": 28,
        "completed_runs": len(completed), "failures": failures,
        "all_completed": len(completed) == 28 and not failures,
        "maximum_meter_limit": MAXIMUM,
        "prototype_internals_inspected": False,
        "expected_order_computed_in_this_child": True,
        "pure_callback_inter_name_order_asserted": False,
        "old_case_pack_is_separate_and_unchanged": True,
    }
    print(json.dumps(summary), flush=True)
    assert summary["all_completed"], "cursor oracle did not complete every planned run"
    return summary
