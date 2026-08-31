"""Independently rehash completed class-extension RED evidence; no analyzer import."""
from pathlib import Path
import hashlib
import json

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
PINS = {
    "311": "88467325038d7d2395c28c291daa42014f562b66f961a8d7983d6dd02cb4c2f9",
    "314": "e3b19f47b0b976fa22e4294dc39dda8422021aeceab8a8a03cd201591f2b0cd8",
}
PACK_SHA = "925ae5b9354377a5957f0c32c8bf5b58fea01612498b835abd6392f9cc87d268"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def create(name, raw):
    with (T / name).open("xb") as stream:
        stream.write(raw)


pack_raw = (T / "tests-checks/class-semantic-extension-cases-v1.json").read_bytes()
assert sha(pack_raw) == PACK_SHA
pack = json.loads(pack_raw)
results = []
public_cases = []
for slot, pin in PINS.items():
    prefix = T / ("tests-checks/class-extension-v19-red01-" + slot)
    receipt_path = Path(str(prefix) + "-receipt.json")
    raw = receipt_path.read_bytes()
    assert sha(raw) == pin
    receipt = json.loads(raw)
    assert receipt["schema"] == "pontius-class-semantic-extension-v1"
    assert receipt["slot"] == slot and receipt["completed"] is True
    assert receipt["integrity_ok"] is True and receipt["success"] is False
    assert receipt["exit"] == receipt["process_returncode"] == 1
    assert "error" not in receipt and "cleanup_error" not in receipt
    assert receipt["before"] == receipt["after"]
    snapshot = Path(receipt["snapshot"])
    assert snapshot.is_relative_to(Path(r"D:\pontius-snapshots"))
    for name, expected in receipt["before"].items():
        assert not Path(name).is_absolute() and ".." not in Path(name).parts
        assert sha((snapshot / name).read_bytes()) == expected, name
    manifest = snapshot / ".class-semantic-extension/manifest.json"
    assert sha(manifest.read_bytes()) == receipt["manifest_sha256"] == receipt["manifest_after_sha256"]
    assert json.loads(manifest.read_bytes()) == receipt["before"]
    assert receipt["input_hashes_before"] == receipt["input_hashes_after"]
    for name, expected in receipt["input_hashes_before"].items():
        assert sha(Path(receipt["input_paths"][name]).read_bytes()) == expected, name
    outputs = {}
    for role, item in receipt["outputs"].items():
        outputs[role] = Path(item["path"]).read_bytes()
        assert sha(outputs[role]) == item["sha256"], role
    assert outputs["log"] == outputs["stdout"] + b"\nCONTROL STDERR\n" + outputs["stderr"]
    records = [json.loads(line) for line in outputs["stdout"].splitlines() if line.startswith(b"{")]
    identity = records[0]["identity_before_imports"]
    assert identity == receipt["identity"]
    assert identity["version_info"] == ([3, 11, 15] if slot == "311" else [3, 14, 6])
    cases = [r for r in records if "class_extension_case" in r]
    assert len(cases) == 12
    semantic_failures = []
    for actual, expected in zip(cases, pack["cases"], strict=True):
        assert actual["class_extension_case"] == expected["id"]
        assert actual["oracle_passed"] is True and actual["oracle_error"] is None
        assert actual["oracle_actual"] == expected["expected"]
        assert not set(actual["oracle_actual"]["trace"]).intersection(expected["unreachable_events"])
        assert actual["analyzer_error"] is None
        kind = expected["classification"]
        passed = (bool(actual["blockers"]) if kind == "refuse" else
                  bool(actual["blockers"]) or actual["argv"] == expected["required_argv"]
                  if kind == "permitted-refusal" else
                  not actual["blockers"] and actual["argv"] == expected["required_argv"])
        assert actual["semantic_passed"] is bool(passed)
        if not passed:
            semantic_failures.append(expected["id"])
    summary = records[-1]
    assert summary == receipt["summary"] and summary["completed"] is True
    assert summary["semantic_failures"] == semantic_failures and len(semantic_failures) == 10
    assert summary["oracle_errors"] == summary["analyzer_errors"] == []
    recursive = next(c for c in cases if c["class_extension_case"] == "recursive-row-safe")
    assert recursive["route_evidence"]["status"] == "entry-without-row"
    entry, returned = recursive["route_evidence"]["events"]
    assert entry["event"] == "entry" and entry["closure_depth"] == 1
    assert entry["projected"] == {
        "armed": {"kind": "scalar", "scalar": True},
        "module": {"kind": "scalar", "scalar": "outer"},
    }
    assert returned["event"] == "return" and returned["subprocess_argv"] == []
    results.append({
        "slot": slot, "receipt": str(receipt_path), "receipt_sha256": pin,
        "log_sha256": receipt["outputs"]["log"]["sha256"],
        "rehash_file_count_including_manifest": len(receipt["before"]) + 1,
        "semantic_failures": semantic_failures, "harmless_models_passed": 12,
        "analyzer_errors": 0, "recursive_route": recursive["route_evidence"],
    })
    public_cases.append(cases)
assert public_cases[0] == public_cases[1], "complete per-case records differ across runtimes"
report = {
    "schema": "coordinator-class-extension-red-verification-v1",
    "pack_sha256": PACK_SHA, "results": results,
    "all_per_case_records_equal_across_runtimes": True,
    "standing": "Pre-repair v19 RED. No semantic implementation or cold verdict.",
}
create("coordinator-class-extension-red-verification-v1.json",
       (json.dumps(report, indent=2) + "\n").encode())
create("coordinator-verify-class-extension-red-v1.py", Path(__file__).read_bytes())
note = """# Class/capture extension: replicated pre-repair RED

All twelve fixed harmless models pass on actual Python 3.11.15 and 3.14.6.
The public analyzer completes all twelve sources without errors on both slots.
Ten semantic requirements fail identically: all five required-unsafe cases
are incorrectly clean; five of six required-clean cases are refused. The
explicit read/write control passes; the permitted-refusal forwarding control
is refused as allowed.

The unsafe known-raise case also emits the class-local module inner instead
of outer. This is an observed public namespace leak, not just an inferred
exception-join risk. The recursive clean case enters invoke at closure depth
one with armed=True, although the harmless model changed it to False. It
returns no subprocess row and two blockers. Route coverage is entry-without-row;
it is not correct to call this route unexecuted.

The coordinator rehashed every snapshot/payload/input/output file. Complete
per-case records are equal across runtimes. See
coordinator-class-extension-red-verification-v1.json for receipt and log pins.
The fixed source/model pack is tests-checks/class-semantic-extension-cases-v1.json.

These are failures already present in retained v19. They do not attribute a
regression to v22 storage. The original ten composition cases remain unchanged.
No semantic source repair, acceptance result, integration or cold verdict is
claimed. Next: approve a concrete lexical-ownership and class-successor design,
implement it as a separate retained candidate, then rerun the fixed scopes.
"""
create("coordinator-class-extension-red-disposition-v1.md", note.encode())
print(json.dumps({"verified": True,
                  "report_sha256": sha((T / "coordinator-class-extension-red-verification-v1.json").read_bytes()),
                  "note_sha256": sha((T / "coordinator-class-extension-red-disposition-v1.md").read_bytes()),
                  "semantic_failures_each_slot": 10, "harmless_models_passed": 24}))
