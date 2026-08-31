"""Validate final evidence, then optionally publish the immutable r010 snapshot.

No Pontius code or test payload runs here. validate is read-only; freeze invokes
only the separately pinned create-only Git snapshot helper after full preflight.
"""
import argparse
import ast
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(r"D:\Pontius-handoffs\v0a-i01-ab")
WORK = Path(r"D:\Pontius-worktrees\codex-v0a-i01-abc")
MAIN = Path(r"D:\Pontius")
PACKET = ROOT / "r010"
BASE = "d1ed3cbda6107d61ea8e77133871720af04970cd"
PRIOR = "8d240db477b8c141e6142e055dbfbedc75c6a2f8"
AB = "ddea6efbeb55cb8b71da1ebd5a359a0c2c901cf1"
C_BASE = "00db06624ab25f10cd181badccf92c87a78f17ee"
BASELINE = "docs/architecture/dependency-baseline.toml"
BASELINE_BLOB = "5fe6ee47f3380b65887b528efef05b72c8e6ac0a"
REF = "refs/heads/review/v0a-i01-ab/r010"
FIX_PATHS = {
    "tools/generate_test_inventory.py", "tests/test_inventory_and_profiles.py",
    "tests/test-inventory.json", "tests/test-profiles.toml",
}
OTHER_C = (
    ".github/workflows/ci.yml", "tools/check_stabilization_boundaries.py",
    "tests/test_v0a_boundaries.py",
)
PINS = {
    "freeze-scoped-round.py":
        "1fdfeca618f7d0cd0bd1f76444b83f9cfa17042ce0ef599df6cf7a7849156eab",
    "snapshot-run-abc-v2.py":
        "62bf07eb88845dfc30c3820aeb8c899ccfbe8111d811192485e2826a5ecfc20c",
    "run-abc-acceptance-v2.py":
        "53a341aa117215e14a930f26b44fc5d8a12ec4fd48540c20bcd1771dc04d5e82",
    "run-abc-focused-v3.py":
        "5e26410c9969c06877cad3384328adf80edfa5bec460a84c60a84706f41b0fbf",
    "run-abc-independent-owner-probes.py":
        "25149df227ee07cbfde7bf67efc8c347917672a30b809a4935f1d5c071afdf12",
    "run-abc-callback-probes-v5.py":
        "7e611a8e83bd7e47a4802b86ea7a9e5ed2edc1f31bbe47e6752cbc0f0ba2b67b",
    "abc-provenance-v2-owner-probe.py":
        "8083601baea0a807d4eb88d5269ec85904e7e782a9c98bec13de23fb6275da53",
    "abc-provenance-v2-effective-input-probe.py":
        "cad4619b60cdc0ccac4a8cb72d894cd5679a22f836c16fc51630f6464f1f6667",
    "r009/checks/coordinator-closure-escape-probe.py":
        "8d1aec927fcc0875724788c1340c14c0fdc83ccd3489f356d38d4b447475808e",
    "r009/checks/coordinator-provenance-metamorphic.py":
        "a3ef4e78e83abec935a84044ba67be800d417ea820ec09fc1f250a3266e375f8",
    "r009/checks/codex-a-probe-forwarding.py":
        "c56e1a8aae327d2f9c1fa25ecbd58a38f5074abc37e107b61ad5fa360e16ff3e",
    "abc-provenance-v4-implicit-class-probe.py":
        "4b6c96eec1ce3c7cf0502ba1551f333ab7df2dcc9a7accfb258b3926cb16ed64",
}
DOCUMENT_PINS = {
    "CLAUDE.md": "af06aad6ec36b91a4e942d7cfc1d3560555ae60e50b023270a0807f247b32b76",
    "docs/workflow.md": "d9de38ede87fb619b3045a60ee7fab137ae23ba3b580c0a6d6b3ca14e567a170",
}
FOCUSED = (
    ("tests/test_inventory_and_profiles.py", ()),
    ("tests/test_stabilization_boundaries.py", ()),
    ("tests/test_v0a_boundaries.py", ()),
    ("tests/test_v0a_hand_replay.py", ()),
    ("tests/test_v0a_trace.py", ()),
    ("tests/test_v0a_replay.py", ()),
    ("tests/test_v0a_contract_faults.py", ()),
    ("tools/generate_test_inventory.py", ("--check",)),
    ("tools/check_stabilization_boundaries.py", ()),
)
OWNER_CASES = {
    "owner": {
        "bound-write": True, "default-owner-write": True,
        "bound-unrelated": False, "default-owner-read": False,
    },
    "effective-input": {
        **{name: True for name in (
            "kw-default-write", "posonly-default-write", "global-owner-write",
            "closure-owner-write", "closure-self-write", "container-default-write",
            "mutation-before-raise",
        )},
        "overridden-default": False, "dormant-mutator": False,
    },
}
CALLBACK_FILES = {
    "closure": "r009/checks/coordinator-closure-escape-probe.py",
    "metamorphic": "r009/checks/coordinator-provenance-metamorphic.py",
    "forwarding": "r009/checks/codex-a-probe-forwarding.py",
    "implicit-class": "abc-provenance-v4-implicit-class-probe.py",
}
CALLBACK_CASES = {
    "closure": {
        kind + "/" + owner: owner != "readonly"
        for kind in ("map-consumed", "sorted-key")
        for owner in ("local-cell", "global-owner", "receiver-cell", "default-owner", "readonly")
    },
    "metamorphic": {name: True for name in ("self-only", "inert-class-name", "class-tail")},
    "forwarding": {
        kind + "-" + tail: True
        for kind in ("callback-default", "callback-keyword", "explicit-callback",
                     "forwarded-owner", "direct-mutation")
        for tail in ("none", "read", "tail", "receiver")
    },
    "implicit-class": {
        "implicit-class-mutation": True, "implicit-class-readonly": False,
        "direct-implicit-class": True,
    },
}


def need(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def zero(value):
    return type(value) is int and value == 0


def integer(value, minimum=0):
    return type(value) is int and value >= minimum


def canonical(value):
    return (json.dumps(value, indent=2, allow_nan=False) + "\n").encode("utf-8")


def put(path, raw):
    if isinstance(raw, str):
        raw = raw.encode("utf-8")
    need(b"\r" not in raw and not raw.startswith(b"\xef\xbb\xbf"), "output not LF/BOM-free")
    with path.open("xb") as stream:
        stream.write(raw)


def load_harness():
    path = ROOT / "snapshot-run-abc-v2.py"
    need(sha(path.read_bytes()) == PINS[path.name], "snapshot helper pin differs")
    spec = importlib.util.spec_from_file_location("r010_snapshot", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.require_control_runtime()
    need(not sys.flags.optimize, "optimized control is prohibited")
    return module


class Evidence:
    def __init__(self, helper):
        self.h = helper
        self.raw = {}
        self.times = {}

    def read(self, path, expected=None):
        path = self.h.checked_path(path)
        need(path.is_relative_to(ROOT) or path.is_relative_to(MAIN), "input outside allowed roots")
        raw = path.read_bytes()
        if expected is not None:
            need(self.h.is_digest(expected) and sha(raw) == expected,
                 "digest differs: " + str(path))
        if path in self.raw:
            need(raw == self.raw[path], "input changed while reading: " + str(path))
        self.raw[path] = raw
        self.times[path] = path.stat().st_mtime_ns
        return raw

    def json(self, path, expected=None):
        return self.h.json_bytes(self.read(path, expected))

    def verify_unchanged(self):
        for path, raw in self.raw.items():
            need(self.h.checked_path(path).read_bytes() == raw, "input drift: " + str(path))

    def rows(self):
        return [{"path": str(path), "sha256": sha(raw)} for path, raw in sorted(self.raw.items())]


def git(helper, setup, repository, *args):
    return helper.git_bytes(repository, Path(setup["temporary"]), *args)


def repository_state(helper, setup, repository):
    head = git(helper, setup, repository, "rev-parse", "HEAD").decode().strip()
    index = Path(git(helper, setup, repository, "rev-parse", "--path-format=absolute",
                     "--git-path", "index").decode().strip())
    raw = helper.checked_path(index).read_bytes() if index.exists() else None
    staged = git(helper, setup, repository, "diff", "--cached", "--name-only", "-z")
    return {"head": head, "index_path": str(index),
            "index_sha256": sha(raw) if raw is not None else None,
            "staged_paths": staged.decode().rstrip("\0").split("\0") if staged else []}


def runtime(identity, helper, slot, complete=False, cwd=None):
    exe, version = helper.SLOTS[slot]
    need(type(identity) is dict, "runtime identity missing")
    need(Path(identity.get("executable", "")).resolve() == Path(exe).resolve(), "wrong executable")
    full = identity.get("version")
    need(type(full) is str and full.startswith(version + " "), "full version differs")
    if complete:
        need(identity.get("implementation") == "cpython", "not CPython")
        need(identity.get("version_info") == [int(x) for x in version.split(".")], "version tuple")
    if cwd is not None:
        need(Path(identity.get("cwd", "")).resolve() == Path(cwd).resolve(), "identity cwd differs")


def parse_objects(helper, raw):
    decoder = json.JSONDecoder(object_pairs_hook=helper.object_pairs)
    rest = raw.decode("utf-8")
    result = []
    while rest.strip():
        rest = rest.lstrip()
        value, end = decoder.raw_decode(rest)
        need(type(value) is dict, "probe output is not an object")
        result.append(value)
        rest = rest[end:]
    return result


def common_receipt(receipt, setup, metadata_sha, helper, slot):
    need(receipt.get("metadata_sha256") == metadata_sha, "receipt metadata differs")
    need(receipt.get("snapshot") == setup["snapshot"], "receipt snapshot differs")
    need(receipt.get("environment") == setup["environment"], "receipt environment differs")
    need(receipt.get("before_sha256") == receipt.get("after_sha256") == setup["source_sha256"],
         "receipt did not execute unchanged final source")
    runtime(receipt.get("runtime_identity"), helper, slot)


def focused_leg(ev, setup, metadata_sha, slot, label):
    helper = ev.h
    path = ROOT / (label + "-" + slot + "-summary.json")
    summary = ev.json(path)
    need(summary.get("slot") == slot and summary.get("metadata_sha256") == metadata_sha,
         "focused summary slot/metadata")
    need(summary.get("source_sha256") == setup["source_sha256"], "focused summary source")
    need(summary.get("driver_sha256") == PINS["run-abc-focused-v3.py"], "focused driver pin")
    rows = summary.get("results")
    need(type(rows) is list and len(rows) == len(FOCUSED), "focused target count")
    receipts, counts, times = [], [], [ev.times[path]]
    for index, ((target, arguments), row) in enumerate(zip(FOCUSED, rows), 1):
        runlabel = label + "-" + str(index).zfill(2)
        rp = ROOT / "abc-checks" / (runlabel + "-" + slot + "-receipt.json")
        lp = rp.with_name(rp.name.replace("-receipt.json", ".txt"))
        need(row.get("target") == target and row.get("args") == list(arguments), "target order")
        need(zero(row.get("exit")) and Path(row.get("receipt", "")) == rp, "focused row failed")
        need(helper.is_digest(row.get("receipt_sha256")), "receipt digest missing")
        receipt = ev.json(rp, row["receipt_sha256"])
        common_receipt(receipt, setup, metadata_sha, helper, slot)
        exe, version = helper.SLOTS[slot]
        expected = [exe, "-B", "-P", "-c", helper.WRAPPER, exe, version, target, *arguments]
        need(receipt.get("schema_version") == "pontius-abc-receipt-v2", "receipt schema")
        need(receipt.get("slot") == slot and receipt.get("label") == runlabel, "receipt label")
        need(receipt.get("command") == expected, "focused command differs")
        need(receipt.get("base") == BASE and receipt.get("changed_paths") == [],
             "receipt base/delta")
        need(receipt.get("harness_sha256") == setup["harness_sha256"], "receipt harness differs")
        need(receipt.get("stored_blob_sha256") == setup["stored_blob_sha256"],
             "stored blobs differ")
        need(zero(receipt.get("exit")) and Path(receipt.get("log", "")) == lp,
             "focused exit/log")
        runtime(receipt.get("control_runtime_identity"), helper, "311", complete=True)
        need(helper.is_digest(receipt.get("sha256")), "log digest missing")
        raw = ev.read(lp, receipt["sha256"])
        lines = raw.decode("utf-8").splitlines()
        need(bool(lines), "empty focused log")
        first = helper.json_bytes(lines[0].encode()).get("identity_before_payload_import")
        runtime(first, helper, slot, complete=True)
        need(first == receipt["runtime_identity"], "log/receipt identity differs")
        need(row.get("summary") == lines[-1], "summary does not match log")
        matches = re.findall(r"^Ran (\d+) tests? in ([0-9.]+)s$", "\n".join(lines), re.MULTILINE)
        if target.startswith("tests/"):
            need(len(matches) == 1, "missing/ambiguous unittest summary")
            count, seconds = int(matches[0][0]), float(matches[0][1])
            need(integer(row.get("tests"), 1) and row["tests"] == count, "test count differs")
            need(type(row.get("seconds")) is float and row["seconds"] == seconds,
                 "duration differs")
            skipped = int(target == "tests/test_stabilization_boundaries.py")
            need(lines[-1] == ("OK (skipped=1)" if skipped else "OK"), "unittest not clean")
            counts.append({"target": target, "tests": count, "skips": skipped})
        else:
            need(not matches and row.get("tests") is None and row.get("seconds") is None,
                 "CLI reported an unexpected unittest count")
        receipts.append({"path": str(rp), "sha256": sha(ev.raw[rp]),
                         "log": str(lp), "log_sha256": sha(raw), "family": "focused",
                         "slot": slot, "target": target, "exit": 0})
        need(ev.times[lp] <= ev.times[rp] <= ev.times[path], "focused file order differs")
        times.extend((ev.times[lp], ev.times[rp]))
    return {"path": str(path), "sha256": sha(ev.raw[path]), "counts": counts,
            "tests": sum(row["tests"] for row in counts),
            "skips": sum(row["skips"] for row in counts), "cli_checks": 2}, receipts, times


def literal_assignment(raw, name):
    values = [node.value for node in ast.parse(raw).body if isinstance(node, ast.Assign)
              and any(isinstance(target, ast.Name) and target.id == name
                      for target in node.targets)]
    need(len(values) == 1, "runner literal missing or repeated")
    value = ast.literal_eval(values[0])
    need(type(value) is str, "runner literal is not a string")
    return value


def probe_leg(ev, setup, metadata_sha, slot, label, callbacks=False):
    helper = ev.h
    exe, version = helper.SLOTS[slot]
    runner = "run-abc-callback-probes-v5.py" if callbacks else "run-abc-independent-owner-probes.py"
    names = CALLBACK_FILES if callbacks else OWNER_CASES
    bootstrap = literal_assignment(ev.raw[ROOT / runner], "bootstrap") if callbacks else None
    receipts, times, total = [], [], 0
    for name in names:
        filename = CALLBACK_FILES[name] if callbacks else "abc-provenance-v2-" + name + "-probe.py"
        payload = ROOT / filename
        rp = ROOT / (label + "-" + name + "-" + slot + "-receipt.json")
        lp = rp.with_name(rp.name.replace("-receipt.json", ".txt"))
        receipt = ev.json(rp)
        common_receipt(receipt, setup, metadata_sha, helper, slot)
        expected = ([exe, "-B", "-P", "-c", bootstrap, str(payload), exe, version]
                    if callbacks else [exe, "-B", "-P", str(payload), exe, version])
        need(receipt.get("command") == expected, "independent command differs")
        need(receipt.get("runner_sha256") == PINS[runner], "independent runner pin")
        need(receipt.get("payload_sha256") == PINS[filename], "independent payload pin")
        if callbacks:
            need(zero(receipt.get("payload_exit")) and zero(receipt.get("contract_exit")),
                 "callback payload/contract failed")
            need(receipt.get("contract_failures") == [], "callback failures remain")
        else:
            need(zero(receipt.get("exit")), "independent owner probe failed")
        need(helper.is_digest(receipt.get("log_sha256")), "independent log digest missing")
        raw = ev.read(lp, receipt["log_sha256"])
        objects = parse_objects(helper, raw)
        need(bool(objects) and "identity_before_import" in objects[0],
             "pre-import identity missing")
        identities = [obj["identity_before_import"] for obj in objects
                      if "identity_before_import" in obj]
        for identity in identities:
            runtime(identity, helper, slot, cwd=None if callbacks else setup["snapshot"])
        need(identities[0] == receipt["runtime_identity"], "independent log identity differs")
        data = [obj for obj in objects if "identity_before_import" not in obj]
        case_map = CALLBACK_CASES[name] if callbacks else OWNER_CASES[name]
        if callbacks and name == "forwarding":
            need(len(data) == 21 and data[-1] == {"cases": 20, "refused": 20, "false_clean": []},
                 "forwarding rollup differs")
            cases = data[:-1]
        else:
            need(len(data) == 1 and type(data[0].get("results")) is list, "probe result shape")
            cases = data[0]["results"]
        need(len(cases) == len(case_map), "independent case count differs")
        need({row.get("case") for row in cases} == set(case_map),
             "independent case identities differ")
        for row in cases:
            mutation = case_map[row["case"]]
            need(type(row.get("blockers")) is list, "probe blockers not a list")
            if callbacks and name == "forwarding":
                need(row.get("pure_error") == "TypeError" and row.get("pure_events") == []
                     and row["blockers"] and row.get("passed") is True, "forwarding false clean")
                continue
            projection = row.get("projection" if callbacks else "pure_projection")
            need(type(row.get("process_rows")) is list, "probe process rows not a list")
            need(projection == ("TypeError" if mutation else "fixed"), "pure projection differs")
            need(bool(row["blockers"]) == mutation, "mutation/readonly refusal differs")
            if not mutation:
                need(len(row["process_rows"]) == 1, "lawful process row not retained")
            elif not callbacks:
                need(not row["process_rows"], "old owner probe retains a stale process row")
            if not callbacks:
                need(row.get("expected_blocked") is mutation and row.get("matched") is True,
                     "owner expected result differs")
            elif name == "closure":
                need(row.get("expected_mutation") is mutation, "callback mutation label differs")
        if callbacks:
            need(integer(receipt.get("contract_cases")) and receipt["contract_cases"] == len(cases),
                 "callback receipt case count differs")
        need(ev.times[lp] <= ev.times[rp], "independent file order differs")
        times.extend((ev.times[lp], ev.times[rp]))
        total += len(cases)
        receipts.append({"path": str(rp), "sha256": sha(ev.raw[rp]), "log": str(lp),
                         "log_sha256": sha(raw), "family": "callback-v5" if callbacks else "owner",
                         "slot": slot, "name": name, "cases": len(cases), "exit": 0})
    need(total == (36 if callbacks else 13), "independent total count")
    return receipts, times


def preserved_paths(helper, setup):
    hashes = setup["source_sha256"]
    rows = []
    for path in helper.PATHS:
        if path in FIX_PATHS:
            continue
        reference = C_BASE if path in OTHER_C else AB
        blob = git(helper, setup, WORK, "cat-file", "blob", reference + ":" + path)
        need(sha(blob) == hashes[path], "preserved source differs: " + path)
        rows.append({"path": path, "source_ref": reference, "sha256": sha(blob), "exact": True})
    need(len(rows) == 13 and len([r for r in rows if r["source_ref"] == AB]) == 10,
         "preservation path count")
    prior = {path: sha(git(helper, setup, WORK, "cat-file", "blob", PRIOR + ":" + path))
             for path in helper.PATHS}
    delta = sorted(path for path in helper.PATHS if prior[path] != hashes[path])
    need(bool(delta) and set(delta) <= FIX_PATHS, "FIX scope expansion or empty repair")
    return rows, delta


def census_binding(ev, args, setup):
    census = ev.json(args.census, args.census_sha256)
    stable = ev.json(args.stability, args.stability_sha256)
    need(census.get("schema_version") == "slice-c-read-only-test-census-v1", "census schema")
    need(census.get("matched_test") ==
         "CheckedInInventoryTests.test_working_discovery_binds_every_entry_and_introduced_id",
         "census bound to wrong test")
    need(census.get("inputs_revalidated_after_derivation") is True
         and census.get("writes_to_snapshot") is False, "census mutation/revalidation")
    need(census.get("helper_sha256") ==
         "37af79be6de2de31171b3b8bdf16ac4b58daeaa1391697b78f0244a68ab372ff", "census helper")
    execution = census["execution"]
    runtime(execution, ev.h, "311")
    need(execution.get("implementation") == "CPython"
         and execution.get("version_tuple") == [3, 11, 15], "census interpreter")
    need(execution.get("safe_path") is True
         and type(execution.get("dont_write_bytecode")) is int
         and execution["dont_write_bytecode"] == 1, "census interpreter flags")
    snap = ev.h.checked_path(execution["cwd"], directory=True)
    need(snap.name == "harness" and snap.parent.parent == ev.h.SNAPSHOTS, "census snapshot")
    need(Path(execution["temp"]) == snap.parent / "temp"
         and Path(execution["pythonpath"]) == snap / "src"
         and execution["git"] == ev.h.G, "census environment paths")
    inputs = census["input_sha256"]
    need(set(inputs) == {"tools/generate_test_inventory.py",
                         "tools/generate_dependency_baseline.py",
                         "tests/test-inventory.json", "tests/test-profiles.toml"}, "census inputs")
    for path, digest in inputs.items():
        need(ev.h.is_digest(digest) and ev.h.digest(WORK / path) == digest
             and ev.h.digest(snap / path) == digest, "census input differs: " + path)
    corpus = census["source_corpus"]
    need(corpus.get("include_support_modules") is False, "census corpus mode")
    source_hashes = corpus["raw_sha256"]
    need(integer(corpus.get("source_count"), 1) and len(source_hashes) == corpus["source_count"],
         "census source count")
    for path, digest in source_hashes.items():
        need(type(path) is str and path.startswith("tests/") and ".." not in Path(path).parts,
             "census source path")
        need(ev.h.is_digest(digest) and ev.h.digest(WORK / path) == digest
             and ev.h.digest(snap / path) == digest, "census corpus differs: " + path)
    need(source_hashes["tests/test_inventory_and_profiles.py"] ==
         setup["source_sha256"]["tests/test_inventory_and_profiles.py"], "census test pin")
    review = census["review"]
    rows = review["receipt"]["expanded_rows"]
    blockers = review["unresolved_dynamic_blockers"]
    need(integer(census.get("expanded_row_count")) and len(rows) == census["expanded_row_count"],
         "census row count")
    need(integer(census.get("blocker_count")) and len(blockers) == census["blocker_count"],
         "census blocker count")
    need(dict(Counter(row["reason"] for row in blockers)) == census["blocker_reason_counts"],
         "census blocker reason count")
    prior = ev.json(ROOT / "slice-c-provenance-v3-census-311-03.json",
                    "42013dfbe68bf17a04dc48080f40191b3b89bde617bda59177c31a15edcef9a4")
    need(rows == prior["review"]["receipt"]["expanded_rows"], "capability rows changed")
    need(review["spec_capabilities_sha256"] == prior["review"]["spec_capabilities_sha256"]
         == review["receipt"]["spec_capabilities_sha256"], "capability spec changed")
    need(stable.get("all_asserted_census_values_stable") is True, "census not stable")
    for key, count in (("all_expanded_rows_identical", len(rows)),
                       ("all_blocker_records_identical", len(blockers))):
        need(integer(stable.get(key)) and stable[key] == count, "stability count differs: " + key)
    need(stable.get("decoy_digest") == census["analysis_census"]["string_sink_decoy_sha256"],
         "stability decoy pin")
    need(stable.get("generator_sha256") ==
         setup["source_sha256"]["tools/generate_test_inventory.py"]
         and stable.get("test_sha256") ==
         setup["source_sha256"]["tests/test_inventory_and_profiles.py"],
         "stability source pins")
    pins = stable["input_sha256"]
    need(pins.get(Path(args.census).name) == args.census_sha256, "stability lacks final census pin")
    for name, digest in pins.items():
        need(type(name) is str and Path(name).name == name, "stability input path")
        ev.read(ROOT / name, digest)
    inventory = ev.h.json_bytes((WORK / "tests/test-inventory.json").read_bytes())
    old_inventory = ev.h.json_bytes(git(ev.h, setup, WORK, "cat-file", "blob",
                                       PRIOR + ":tests/test-inventory.json"))
    need(type(inventory.get("entries")) is list, "inventory entries schema")
    current_entries = {row["stable_id"]: row for row in inventory["entries"]}
    prior_entries = {row["stable_id"]: row for row in old_inventory["entries"]}
    need(len(current_entries) == len(inventory["entries"]), "duplicate inventory id")
    need(all(current_entries.get(key) == value for key, value in prior_entries.items()),
         "existing inventory assignment changed")
    need(len(current_entries) == census["parsed_stable_id_count"]
         == census["generated_discovery"]["stable_id_count"],
         "inventory/census stable IDs differ")
    return {"path": str(Path(args.census)), "sha256": args.census_sha256,
            "stability_path": str(Path(args.stability)), "stability_sha256": args.stability_sha256,
            "expanded_rows": len(rows), "blockers": len(blockers),
            "spec_capabilities_sha256": review["spec_capabilities_sha256"],
            "cross_file_helper_edges": census["analysis_census"]["cross_file_helper_edge_count"],
            "inventory_entries": len(current_entries),
            "prior_entries_preserved": len(prior_entries),
            "new_inventory_entries": len(current_entries) - len(prior_entries),
            "source_corpus_count": len(source_hashes)}


def arguments(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("validate", "freeze"))
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--metadata-sha256", required=True)
    parser.add_argument("--focused-label", required=True)
    parser.add_argument("--owner-label", required=True)
    parser.add_argument("--callback-label", required=True)
    for name in ("census", "stability", "coverage"):
        parser.add_argument("--" + name, required=True)
        parser.add_argument("--" + name + "-sha256", required=True)
    parser.add_argument("--requirements-sha256", required=True)
    parser.add_argument("--protocol-sha256", required=True)
    result = parser.parse_args(argv)
    for label in (result.focused_label, result.owner_label, result.callback_label):
        need(re.fullmatch(r"[a-z0-9][a-z0-9-]{0,85}", label) is not None, "invalid evidence label")
    return result


def preflight(args, helper):
    ev = Evidence(helper)
    for path in (args.census, args.stability, args.coverage):
        need(Path(path).is_absolute() and Path(path).is_relative_to(ROOT),
             "census/stability/coverage must be absolute task-root paths")
    for path, digest in PINS.items():
        ev.read(ROOT / path, digest)
    ev.read(Path(__file__).resolve())
    ev.read(args.metadata, args.metadata_sha256)
    setup = helper.load_setup(args.metadata, args.metadata_sha256)
    need(setup["source"] == "working" and setup["base"] == BASE, "final metadata base/source")
    need(len(setup["source_sha256"]) == 17, "full source manifest needs 17 paths")
    need(helper.source_hashes(WORK) == helper.source_hashes(Path(setup["snapshot"]))
         == setup["source_sha256"], "final source drift")
    states = {name: repository_state(helper, setup, path)
              for name, path in (("main", MAIN), ("work", WORK))}
    need(all(state["head"] == BASE for state in states.values()), "main/work HEAD moved")
    need(states["main"]["staged_paths"] == [], "main index is not empty")
    for path, digest in DOCUMENT_PINS.items():
        ev.read(MAIN / path, digest)
    baseline = git(helper, setup, MAIN, "rev-parse", BASE + ":" + BASELINE).decode().strip()
    need(baseline == BASELINE_BLOB, "baseline object changed")
    baseline_bytes = git(helper, setup, MAIN, "cat-file", "blob", BASELINE_BLOB)
    need(helper.checked_path(MAIN / BASELINE).read_bytes() == baseline_bytes
         and helper.checked_path(WORK / BASELINE).read_bytes() == baseline_bytes,
         "baseline bytes changed")
    preserved, delta = preserved_paths(helper, setup)
    summaries, receipts, chronology = {}, [], {}
    family_times = {family: {} for family in ("focused", "owner", "callback-v5")}
    for slot in ("311", "314"):
        summary, found, times = focused_leg(
            ev, setup, args.metadata_sha256, slot, args.focused_label
        )
        summaries[slot] = summary
        receipts.extend(found)
        family_times["focused"][slot] = times
        for family, label, callbacks in (("owner", args.owner_label, False),
                                         ("callback-v5", args.callback_label, True)):
            found, times = probe_leg(ev, setup, args.metadata_sha256, slot, label, callbacks)
            receipts.extend(found)
            family_times[family][slot] = times
    need(summaries["311"]["counts"] == summaries["314"]["counts"], "slot test counts differ")
    need(summaries["311"]["skips"] == 1 and len(receipts) == 30, "skip/receipt total differs")
    for family, slots in family_times.items():
        last_floor, first_dev = max(slots["311"]), min(slots["314"])
        need(last_floor <= first_dev, "retained file chronology contradicts floor-first: " + family)
        chronology[family] = {"last_floor_mtime_ns": last_floor, "first_dev_mtime_ns": first_dev,
                              "floor_before_dev_corroborated_by_file_metadata": True}
    census = census_binding(ev, args, setup)
    coverage = ev.read(args.coverage, args.coverage_sha256)
    requirements = ev.read(ROOT / "abc-r010-requirements-draft.md", args.requirements_sha256)
    protocol = ev.read(ROOT / "abc-r010-protocol-interpretation.md", args.protocol_sha256)
    for raw in (coverage, requirements, protocol):
        need(raw.strip() and not raw.startswith(b"\xef\xbb\xbf")
             and b"\r" not in raw.replace(b"\r\n", b"\n"), "empty/BOM/non-LF document input")
    need(not PACKET.exists(), "r010 already exists; never overwrite an issued packet")
    ev.verify_unchanged()
    return ev, setup, states, {
        "schema_version": "pontius-r010-preflight-v1", "metadata": str(Path(args.metadata)),
        "metadata_sha256": args.metadata_sha256, "all_17_blob_sha256": setup["source_sha256"],
        "summaries": summaries, "receipts": receipts, "census": census,
        "preserved_source_paths": preserved, "fix_delta_from": PRIOR,
        "fix_changed_paths": delta, "fix_allowed_paths": sorted(FIX_PATHS),
        "repository_state_before": states, "controller_document_sha256": DOCUMENT_PINS,
        "baseline_blob": BASELINE_BLOB, "slot_order_corroboration": chronology,
        "chronology_limit": "No receipt carries a signed execution-time chain. Retained file "
                            "metadata corroborates floor-first within each runner family only.",
        "input_pins": ev.rows(), "all_goals_exit_zero": True,
    }


def frozen_identity(helper, setup):
    candidate = helper.json_bytes((PACKET / "candidate.json").read_bytes())
    need(set(candidate) == {"schema_version", "task_id", "round", "ref", "commit", "base",
                           "tree", "manifest_sha256", "date"}, "candidate schema keys")
    need(candidate["schema_version"] == "pontius-handoff-candidate-v1"
         and candidate["task_id"] == "v0a-i01-ab" and candidate["round"] == "r010"
         and candidate["base"] == BASE and candidate["ref"] == REF, "candidate identity fields")
    commit = candidate["commit"]
    need(helper.is_digest(commit, 40) and helper.is_digest(candidate["tree"], 40), "Git identity")
    need(git(helper, setup, WORK, "rev-parse", commit + "^{tree}").decode().strip()
         == candidate["tree"], "candidate tree")
    need(git(helper, setup, WORK, "show", "-s", "--format=%P", commit).decode().strip() == BASE,
         "candidate has wrong/multiple parents")
    fields = git(helper, setup, WORK, "diff-tree", "--no-renames", "-r", "-z", "--no-commit-id",
                 "--name-status", BASE, commit).decode().split("\0")
    changed = []
    for index in range(0, len(fields) - 1, 2):
        status, path = fields[index:index + 2]
        need(status in ("A", "M") and path in helper.PATHS, "unexpected frozen change")
        changed.append(path)
    need(len(changed) == 17 and set(changed) == set(helper.PATHS), "full main-based delta differs")
    blobs = {path: sha(git(helper, setup, WORK, "cat-file", "blob", commit + ":" + path))
             for path in helper.PATHS}
    need(blobs == setup["source_sha256"], "frozen blobs differ from executed bytes")
    manifest = b"".join(sorted((digest + "  " + path + "\n").encode()
                                for path, digest in blobs.items()))
    need((PACKET / "manifest.sha256").read_bytes() == manifest
         and candidate["manifest_sha256"] == sha(manifest), "whole-row manifest differs")
    delta = git(helper, setup, WORK, "diff", "--no-renames", "--name-only", "-z",
                PRIOR, commit).decode().rstrip("\0").split("\0")
    need(bool(delta) and set(delta) <= FIX_PATHS, "frozen FIX scope expansion")
    need(git(helper, setup, WORK, "rev-parse", "--verify", REF).decode().strip() == commit,
         "local review ref differs")
    # Host Git credentials belong to publication control, not the test environment.
    remote = subprocess.run(
        [helper.G, "--no-optional-locks", "-C", str(WORK), "ls-remote", "origin", REF],
        capture_output=True, check=True,
    ).stdout.decode().splitlines()
    need(remote == [commit + "\t" + REF], "remote review ref differs")
    return candidate, sorted(delta)


def write_packet(ev, args, setup, binding, candidate):
    binding["candidate"] = candidate["commit"]
    binding["manifest"] = candidate["manifest_sha256"]
    binding["frozen_blob_bytes_equal_executed_source"] = True
    put(PACKET / "checks/focused-evidence-binding.json", canonical(binding))
    inputs = PACKET / "inputs"
    inputs.mkdir()
    pins = {}
    for path, digest in DOCUMENT_PINS.items():
        raw = ev.raw[MAIN / path].replace(b"\r\n", b"\n")
        destination = inputs / Path(path).name
        put(destination, raw)
        pins[destination.relative_to(PACKET).as_posix()] = {
            "sha256": sha(raw), "origin": path, "origin_raw_sha256": digest,
        }
    put(PACKET / "checks/protocol-input-pins.json", canonical(pins))
    for source, destination in ((ROOT / "abc-r010-requirements-draft.md", "acceptance.md"),
                                (ROOT / "abc-r010-protocol-interpretation.md",
                                 "protocol-interpretation.md")):
        put(PACKET / destination, ev.raw[source].replace(b"\r\n", b"\n"))
    coverage = ev.raw[Path(args.coverage)].replace(b"\r\n", b"\n")
    coverage += b"\nFrozen evidence inputs (deferred until independent inventory):\n"
    for path in (PACKET / "checks/focused-evidence-binding.json",
                 Path(args.census), Path(args.stability)):
        relative = (path.relative_to(PACKET).as_posix() if path.is_relative_to(PACKET)
                    else "../" + path.relative_to(ROOT).as_posix())
        coverage += ("- " + relative + " SHA256 " + sha(path.read_bytes()) + "\n").encode()
    put(PACKET / "coverage.md", coverage)
    coverage_sha = sha(coverage)
    acceptance_sha = sha((PACKET / "acceptance.md").read_bytes())
    protocol_sha = sha((PACKET / "protocol-interpretation.md").read_bytes())
    wall = [[target, *arguments] for _, target, arguments in ev.h.TARGETS]
    need(len(wall) == 17, "finite wall target count")
    put(PACKET / "checks/permitted-cpu-wall.json", canonical({
        "authority": "ADR-0485 finite currentCI12+v0a5 after two fresh CLEAN reviews",
        "guarded_profile_authority": False, "targets": wall,
    }))
    handoff = f"""# Cold review: v0a-i01-ab/r010

Round kind FIX; Tier C. Implementer Codex, original C drafter Claude;
checkpoint finalizer Claude. Candidate commit {candidate['commit']};
ref {candidate['ref']}; manifest SHA-256 {candidate['manifest_sha256']}.
Main parent {BASE}. Review this frozen Git snapshot and blob manifest,
never mutable source or chat history. A changed byte requires a new round.

Initial allowed inputs: this handoff, candidate.json, manifest.sha256,
acceptance.md SHA256 {acceptance_sha}, protocol-interpretation.md SHA256
{protocol_sha}, pinned inputs/CLAUDE.md and inputs/workflow.md below,
and frozen source/tests/ADR-0485/ADR-0484/revised brief. The pinned current
workflow governs rather than older copies inside the candidate.
A/B preservation reference: {AB} (ten paths).
Other C preservation reference: {C_BASE} (three paths).
FIX comparison reference: {PRIOR}. These are source comparisons only.
Do not read prior or peer reviews, dispositions, checks, self-reports,
status, plans, transcripts or implementation discussions.

The full 17-path manifest is relative to main. Actual FIX changed paths:
{', '.join(binding['fix_changed_paths'])}.
Independently reconstruct the whole-row-sorted Git-blob manifest and applicable
invariant/related-path inventory BEFORE opening deferred coverage.md SHA256
{coverage_sha}. Save and hash your inventory first. Coverage and its named raw
evidence may be assessed afterward; implementation narratives remain excluded.

Use fresh D-local disposable clones of this exact candidate. Run actual3.11.15
FIRST, then3.14.6: full version/executable assertion before Pontius imports,
-B -P, snapshot-root cwd, src PYTHONPATH, scrubbed environment, D-local TEMP/TMP,
and absolute validated PONTIUS_GIT. Focused affected checks and independently
chosen adversarial controls only. Sensitive fixture source is inspected, never
executed as the oracle. Do not repair frozen source. No full wall before two
fresh mutually blind CLEAN reviews; no guarded/GPU/install/capability grant,
source-seal, rehearsal, performance or live wall claim follows from this packet.

Execution infrastructure ../snapshot-run-abc-v2.py SHA256
{PINS['snapshot-run-abc-v2.py']} may be inspected. Independently inspect any
additional probe wrapper for the same isolation/identity policy. Write only your
assigned checks/report. Neither reviewer may have implemented this repair or
read the other review. Sequential execution does not relax mutual blindness.

Reports bind this exact pair. State each label exactly once:
Reviewer ID: <assigned reviewer_id>
Candidate commit: <full commit above>
Manifest SHA-256: <full manifest above>
Defect verdict: <actual verdict>
Design verdict: <SOUND, STRAINED, or WRONG SHAPE>
Required corrections and advisory engineering guidance must be separate.
After your final report/hash, request an exclusive task-ledger append slot.
Each issuer appends their own verdict without opening a peer report.

Only after two fresh CLEAN verdicts may the coordinator run the finite
current-CI12+v0a5 CPU wall listed in checks/permitted-cpu-wall.json, floor first
then dev. This is not a guarded profile grant. Controller approval must then
name this exact round/candidate before Claude's ceremonial main commit/push.
"""
    for path, pin in pins.items():
        handoff += ("\nPinned " + path + " SHA256 " + pin["sha256"]
                    + "; origin raw SHA256 " + pin["origin_raw_sha256"] + ".\n")
    put(PACKET / "handoff.md", handoff)
    summary, census = binding["summaries"]["311"], binding["census"]
    report = f"""# Combined FIX engineering evidence

Candidate {candidate['commit']}; manifest {candidate['manifest_sha256']}.
All 17 frozen Git blobs equal the executed final snapshot bytes. On each actual
interpreter (3.11.15 then3.14.6), the seven affected test targets ran
{summary['tests']} tests: {summary['tests'] - summary['skips']} passed, one existing
POSIX-only skip, zero failures/errors. Both C CLI checks passed. The independent
13 owner/effective-input controls and 36 callback/provenance controls passed on
each slot. All 30 receipts and log hashes bind in checks/focused-evidence-binding.json.
This combines retained evidence and does not replace independent cold review.

All ten A/B blobs remain exact r007 bytes; CI, the boundary checker and its new
suite remain exact r008 bytes. Against r009, all {census['prior_entries_preserved']}
prior inventory entries retain their assignments; {census['new_inventory_entries']}
new entries produce {census['inventory_entries']} total. The {census['expanded_rows']}
capability rows and their specification digest are unchanged. The final census
records {census['blockers']} blockers and {census['cross_file_helper_edges']} cross-file
helper edges. These conservative-refusal costs and the bounded correction are
explained in deferred coverage. A complete Python heap model is not claimed.

Prior failures remain separately retained. The final source, generated pair and
mechanical census refresh all precede this freeze. There are no post-freeze fixes.
Receipt formats do not provide a signed execution-time chain; file metadata only
corroborates floor-before-dev within each runner family. Runtime/source/command
and raw-log bindings are checked directly, not inferred from labels.

No broad wall, guarded/GPU grant, source seal, rehearsal, performance/live wall
claim or ceremonial main commit has run through this builder. Two fresh cold
passes are next, followed by the permitted finite wall and exact controller
approval for Claude's finalization.
"""
    put(PACKET / "self-report.md", report)
    return {"coverage_sha256": coverage_sha, "acceptance_sha256": acceptance_sha,
            "protocol_sha256": protocol_sha}


def main(argv):
    args = arguments(argv)
    helper = load_harness()
    ev, setup, states, binding = preflight(args, helper)
    if args.mode == "validate":
        print(json.dumps({"validated": True, "freeze_executed": False,
                          "tests_per_slot": binding["summaries"]["311"]["tests"],
                          "receipts": len(binding["receipts"]),
                          "fix_changed_paths": binding["fix_changed_paths"],
                          "input_pins": binding["input_pins"]}, indent=2))
        return 0
    ev.verify_unchanged()
    need(helper.source_hashes(WORK) == setup["source_sha256"],
         "source drift immediately before freeze")
    for name, path in (("main", MAIN), ("work", WORK)):
        need(repository_state(helper, setup, path) == states[name], "repository state drift")
    # The sole mutation dispatch publishes a new review ref through a temporary
    # index. The pinned helper does not commit, merge or update main.
    subprocess.run([sys.executable, "-I", "-S", "-B", "-P",
                    str(ROOT / "freeze-scoped-round.py"), str(WORK), BASE, "r010",
                    *helper.PATHS], check=True)
    candidate, delta = frozen_identity(helper, setup)
    need(delta == binding["fix_changed_paths"], "frozen delta differs from preflight")
    ev.verify_unchanged()
    need(helper.source_hashes(WORK) == setup["source_sha256"], "source changed during freeze")
    for name, path in (("main", MAIN), ("work", WORK)):
        need(repository_state(helper, setup, path) == states[name], "freeze changed HEAD/index")
    binding["repository_state_after"] = states
    result = write_packet(ev, args, setup, binding, candidate)
    print(json.dumps({"packet": str(PACKET), "candidate": candidate, **result,
                      "fix_delta": delta, "main_unchanged": True}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except Exception as exc:
        print(json.dumps({"blocker": type(exc).__name__, "reason": str(exc)}), file=sys.stderr)
        raise SystemExit(2)
