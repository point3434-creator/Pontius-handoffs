"""Independent cold-B diagnostics. No source/test/configuration modifications."""
import sys
import os
import platform
from pathlib import Path

ROOT = Path(r"D:\pontius-snapshots\v0a-r006-cold-b-9b68bc30697143659ff72e0007e9789e\harness")
PACKET = Path(r"D:\Pontius-handoffs\v0a-i01-impl\r006")
GIT = r"C:\Program Files\Git\cmd\git.exe"
COMMIT = "c74b80628a89938ca585ef3240b5c267a7174d0f"
MANIFEST = "2078d59a4a112bf29a2bd9faca9a2ca070bbd1028a940f2eeb617c9e1c31555f"
VERSIONS = {
    "311": (r"D:\Pontius-tools\py311\Scripts\python.exe", "3.11.15"),
    "314": (r"D:\Pontius\.venv\Scripts\python.exe", "3.14.6"),
}
slot = sys.argv[1]
expected_exe, expected_version = VERSIONS[slot]
assert os.path.normcase(sys.executable) == os.path.normcase(expected_exe), sys.executable
assert platform.python_implementation() == "CPython"
assert platform.python_version() == expected_version, platform.python_version()
assert Path.cwd() == ROOT
assert os.environ["PYTHONPATH"] == str(ROOT / "src")
assert os.environ["PONTIUS_GIT"] == GIT
assert sys.flags.safe_path and sys.dont_write_bytecode
identity = {
    "executable": sys.executable,
    "implementation": platform.python_implementation(),
    "version": platform.python_version(),
    "cwd": str(Path.cwd()),
    "argv": sys.argv,
    "environment": dict(os.environ),
    "safe_path": sys.flags.safe_path,
    "dont_write_bytecode": sys.dont_write_bytecode,
}
# Everything above executes before any production import.
import hashlib
import json
import subprocess
import runpy
import traceback


def emit(value):
    print(json.dumps(value, sort_keys=True), flush=True)


def git(*args):
    return subprocess.run([GIT, "-C", str(ROOT), *args], check=True, capture_output=True).stdout


def frozen_identity():
    assert git("rev-parse", "HEAD").strip().decode() == COMMIT
    assert git("rev-parse", COMMIT + "^{tree}").strip().decode() == "a22414541973b76ddd1efa1ca8fc41f51b7a4065"
    assert git("status", "--porcelain") == b""
    raw = git("diff-tree", "-r", "-z", "--no-renames", "--no-commit-id", "--name-status", COMMIT + "^", COMMIT)
    fields = raw.split(b"\0")
    rows = []
    checkouts = []
    for i in range(0, len(fields) - 1, 2):
        status, name = fields[i:i + 2]
        assert status in (b"A", b"M", b"T", b"D"), (status, name)
        path = name.decode("utf-8")
        if status == b"D":
            digest = "0" * 64
        else:
            blob = git("cat-file", "blob", COMMIT + ":" + path)
            digest = hashlib.sha256(blob).hexdigest()
            checkout = (ROOT / path).read_bytes()
            assert checkout.replace(b"\r\n", b"\n") == blob
            checkouts.append({"path": path, "blob_sha256": digest, "checkout_exact": checkout == blob, "crlf_checkout_lines": checkout.count(b"\r\n")})
        rows.append(digest.encode("ascii") + b"  " + name + b"\n")
    rebuilt = b"".join(sorted(rows))
    recorded = (PACKET / "manifest.sha256").read_bytes()
    assert rebuilt == recorded
    assert hashlib.sha256(rebuilt).hexdigest() == MANIFEST
    return {"commit": COMMIT, "manifest": MANIFEST, "row_count": len(rows), "whole_row_sorted": True, "checkout_comparison": checkouts}

emit({"identity": identity})
emit({"frozen_identity": frozen_identity()})

if len(sys.argv) > 2 and sys.argv[2] == "suite":
    test = sys.argv[3]
    sys.argv = [str(ROOT / "tests" / test)]
    runpy.run_path(sys.argv[0], run_name="__main__")
    raise SystemExit(0)

from dataclasses import replace
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.v0a.clock import MonotonicWitness
from pontius.v0a.model import FailureCode
from pontius.v0a.replay import ReplayHost, FIXTURE_A, FIXTURE_B, PROTOCOL_ID, chip_depth_settlement
from pontius.v0a.runtime import OperationFailed
from pontius.v0a.trace import write_trace

for name, module in sorted(sys.modules.items()):
    if name.startswith("pontius") and getattr(module, "__file__", None):
        assert Path(module.__file__).resolve().is_relative_to(ROOT / "src"), (name, module.__file__)
emit({"production_imports": {name: module.__file__ for name, module in sorted(sys.modules.items()) if name.startswith("pontius") and getattr(module, "__file__", None)}})


class Source:
    def __init__(self, at=None, kind="invalid"):
        self.reads = 0
        self.now = 1000000
        self.at = at
        self.kind = kind
        self.faults = []

    def __call__(self):
        self.reads += 1
        if self.reads == self.at:
            self.faults.append({"read": self.reads, "kind": self.kind})
            if self.kind == "reversed":
                return self.now - 10000
            if self.kind == "source":
                raise OSError("independent source failure")
            return True
        result = self.now
        self.now += 1000
        return result


def host_for(name, source, oracle=chip_depth_settlement, fixture=FIXTURE_A, witness=None):
    return ReplayHost(fixture, run_id=f"{PROTOCOL_ID}-correctness-cold-b-{slot}-{name}",
                      blueprint=ImmutableBlueprintActionSource(source_id="cold-b-empty"),
                      clock=source if witness is None else witness, settlement_oracle=oracle,
                      source_commit=COMMIT, source_manifest_sha256=MANIFEST)


def describe(host, outcome, source):
    receipt = outcome.receipt
    return {
        "reported": [code.value for code in (receipt.failure_reason, *receipt.secondary_failures) if code is not None],
        "journal": [code.value for code in host.runtime.closure_failures],
        "passed": receipt.passed, "accounting_complete": receipt.accounting_complete,
        "publication_seconds": receipt.terminal_publication_compute_seconds,
        "trace_digest": receipt.trace_sha256,
        "trace_length": len(outcome.trace), "source_reads": source.reads,
        "source_faults": source.faults, "accepted": len(host.mailbox.accepted),
        "decisions": len(outcome.decisions),
    }


results = []

def case(name, function):
    try:
        value = function()
        results.append({"case": name, **value})
    except BaseException as error:
        results.append({"case": name, "diagnostic_error": type(error).__name__, "details": traceback.format_exc()})
    emit(results[-1])


def baseline(fixture):
    source = Source()
    host = host_for("baseline-" + fixture.name, source, fixture=fixture)
    outcome = host.run()
    result = describe(host, outcome, source)
    assert outcome.receipt.passed and result["reported"] == []
    assert result["accepted"] == fixture.expected_controlled_actions
    return result

case("baseline-A", lambda: baseline(FIXTURE_A))
case("baseline-B", lambda: baseline(FIXTURE_B))

# Establish the settlement entry position from the independent oracle boundary,
# not by hard-coding production read counts or wrapping a ledger helper.
positions = []
calibration_source = Source()
def locating_oracle(**kwargs):
    positions.append(calibration_source.reads)
    return chip_depth_settlement(**kwargs)
calibration_host = host_for("locate-entry", calibration_source, locating_oracle)
assert calibration_host.run().receipt.passed and len(positions) == 1
entry_at = positions[0]
emit({"settlement_entry_read": entry_at, "calibration_total_reads": calibration_source.reads})


def settlement_body(kind, where):
    source = Source(kind=kind)
    witness = MonotonicWitness(source)
    def oracle(**kwargs):
        if where == "raised-exit":
            source.at = source.reads + 1
            raise ValueError("settlement body failed")
        if where == "returned-exit":
            result = chip_depth_settlement(**kwargs)
            source.at = source.reads + 1
            return replace(result, final_stacks=tuple(v + 1 for v in result.final_stacks))
        if where == "direct-body":
            source.at = source.reads + 1
        witness()
        return chip_depth_settlement(**kwargs)
    if where == "entry-then-witness":
        source.at = entry_at
    host = host_for(kind + "-" + where, source, oracle, witness=witness)
    outcome = host.run()
    result = describe(host, outcome, source)
    clock_code = "clock_reversed" if kind == "reversed" else "clock_invalid"
    expected = ["settlement_mismatch", clock_code] if where.endswith("exit") else [clock_code]
    result["expected"] = expected
    result["exact_match"] = result["reported"] == expected
    return result

for kind in ("invalid", "reversed", "source"):
    for where in ("raised-exit", "returned-exit", "direct-body", "entry-then-witness"):
        case("settlement-" + kind + "-" + where, lambda kind=kind, where=where: settlement_body(kind, where))


def publication_path_failure(kind):
    source = Source(kind=kind)
    class FailingPath:
        # PathLike is the documented standard-library path boundary. The writer
        # itself is real; only this external input conversion fails.
        def __fspath__(self):
            source.at = source.reads + 1
            raise ValueError("publication destination conversion failed")
    host = host_for("publication-" + kind, source)
    outcome = host.run(destination=FailingPath(), run_root=PACKET / "checks")
    result = describe(host, outcome, source)
    result["expected"] = ["trace_write_failed", "clock_reversed" if kind == "reversed" else "clock_invalid"]
    result["exact_match"] = result["reported"] == result["expected"]
    return result

for kind in ("invalid", "reversed"):
    case("publication-destination-body-plus-exit-" + kind, lambda kind=kind: publication_path_failure(kind))


def nested_owned(fail):
    source = Source()
    holder = {}
    def oracle(**kwargs):
        with holder["host"].runtime.owned_bookkeeping(body_failure=FailureCode.SETTLEMENT_MISMATCH):
            if fail:
                raise ValueError("nested body failed")
            return chip_depth_settlement(**kwargs)
    host = host_for("nested-" + str(fail), source, oracle)
    holder["host"] = host
    result = describe(host, host.run(), source)
    result["nested_body_fails"] = fail
    return result

case("public-same-runtime-nesting-success", lambda: nested_owned(False))
case("public-same-runtime-nesting-failure", lambda: nested_owned(True))


def exceptional_formatting():
    source = Source()
    class Unprintable(ValueError):
        def __str__(self):
            raise RuntimeError("exception formatting failed")
    def oracle(**kwargs):
        raise Unprintable()
    host = host_for("unprintable", source, oracle)
    try:
        result = describe(host, host.run(), source)
        result["escaped"] = None
    except BaseException as error:
        result = {"escaped": type(error).__name__, "message": str(error), "journal": [code.value for code in host.runtime.closure_failures]}
    return result

case("exception-message-conversion", exceptional_formatting)
emit({"summary": {"cases": len(results), "exact_sequence_mismatches": [v["case"] for v in results if v.get("exact_match") is False], "diagnostic_errors": [v["case"] for v in results if "diagnostic_error" in v]}})
assert git("status", "--porcelain") == b""
