"""Disposable snapshot runner; no payload runs when this module is imported."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import uuid

ROOT = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
WORK = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
REPOSITORY = Path(r"D:\Pontius")
SNAPSHOTS = Path(r"D:\pontius-snapshots")
G = r"C:\Program Files\Git\cmd\git.exe"
BASE = "29c02f6fbd5eb0b7ddc9e816ef28f570b9839358"
SLOTS = {
    "311": (r"D:\Pontius-tools\py311\Scripts\python.exe", "3.11.15"),
    "314": (r"D:\Pontius\.venv\Scripts\python.exe", "3.14.6"),
}
PATHS = tuple("src/pontius/v0a/" + n + ".py" for n in
              ("__init__", "clock", "model", "replay", "runtime", "trace"))
PATHS += tuple("tests/" + n + ".py" for n in
               ("test_v0a_contract_faults", "test_v0a_hand_replay",
                "test_v0a_replay", "test_v0a_trace"))
PATHS += (".github/workflows/ci.yml", "tools/check_stabilization_boundaries.py",
          "tools/generate_test_inventory.py", "tests/test_v0a_boundaries.py",
          "tests/test_inventory_and_profiles.py", "tests/test-inventory.json",
          "tests/test-profiles.toml")
TARGETS = (
    ('inventory', 'tests/test_inventory_and_profiles.py', ()),
    ('old-boundary', 'tests/test_stabilization_boundaries.py', ()),
    ('inventory-check', 'tools/generate_test_inventory.py', ('--check',)),
    ('boundary', 'tools/check_stabilization_boundaries.py', ()),
    ('v0a-boundary', 'tests/test_v0a_boundaries.py', ()),
    ('v0a-hand', 'tests/test_v0a_hand_replay.py', ()),
    ('v0a-trace', 'tests/test_v0a_trace.py', ()),
    ('v0a-replay', 'tests/test_v0a_replay.py', ()),
    ('v0a-faults', 'tests/test_v0a_contract_faults.py', ()),
)

SCRIPT_NAMES = ("snapshot-run-authority-v1.py",)


class Blocker(RuntimeError):
    """A failed precondition or evidence binding; never a payload pass."""


def require(condition, reason):
    if not condition:
        raise Blocker(reason)


def is_digest(value, width=64):
    return type(value) is str and re.fullmatch("[0-9a-f]{" + str(width) + "}", value) is not None


def digest_bytes(value):
    return hashlib.sha256(value).hexdigest()


def checked_path(value, directory=False):
    path = Path(value)
    require(path.is_absolute() and ".." not in path.parts, "non-absolute/traversing path")
    for ancestor in (path, *path.parents):
        info = ancestor.lstat()
        require(not (getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT),
                "reparse path: " + str(ancestor))
    require(path.is_dir() if directory else path.is_file(), "wrong path kind: " + str(path))
    return path


def digest(path):
    return digest_bytes(checked_path(path).read_bytes())


def object_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def json_bytes(raw):
    def bad_constant(value):
        raise Blocker("non-finite JSON constant: " + value)
    return json.loads(raw.decode("utf-8"), object_pairs_hook=object_pairs,
                      parse_constant=bad_constant)


def create(path, value):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write("\n")


def runtime_identity():
    return {"executable": sys.executable, "implementation": sys.implementation.name,
            "version": sys.version, "version_info": list(sys.version_info[:3])}


def require_control_runtime():
    exe, version = SLOTS["311"]
    require(sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path
            and sys.dont_write_bytecode, "control requires -I -S -B -P")
    require(sys.implementation.name == "cpython", "control is not CPython")
    require(Path(sys.executable).resolve() == Path(exe).resolve(), "wrong control executable")
    require(".".join(map(str, sys.version_info[:3])) == version, "wrong control version")


def control_environment(temporary, snapshot=None):
    windows = checked_path(os.environ["SYSTEMROOT"], directory=True)
    system = checked_path(windows / "System32", directory=True)
    env = {"SYSTEMROOT": str(windows), "WINDIR": str(windows),
           "COMSPEC": str(system / "cmd.exe"), "PATH": str(system),
           "TEMP": str(temporary), "TMP": str(temporary),
           "PONTIUS_GIT": G, "GIT_CONFIG_NOSYSTEM": "1",
           "GIT_CONFIG_GLOBAL": "NUL", "GIT_CONFIG_SYSTEM": "NUL",
           "GIT_ATTR_NOSYSTEM": "1", "PYTHONNOUSERSITE": "1"}
    if snapshot is not None:
        env["PYTHONPATH"] = str(snapshot / "src")
    return env


def git_bytes(repository, temporary, *args):
    checked_path(G)
    command = [G, "-c", "core.autocrlf=false", "-c", "core.hooksPath=NUL",
               "-c", "init.templateDir=", "-c", "core.attributesFile=NUL",
               "-c", "core.fsmonitor=false", "-C", str(repository), *args]
    return subprocess.run(command, cwd=repository, env=control_environment(temporary),
                          capture_output=True, check=True).stdout


def source_hashes(snapshot):
    return {path: digest(snapshot / path) for path in PATHS}


def stored_hashes(snapshot, base, temporary):
    raw = git_bytes(snapshot, temporary, "ls-tree", "-r", "-z", "--name-only", base, "--", *PATHS)
    present = set(raw.decode("utf-8").rstrip("\0").split("\0")) if raw else set()
    require(present <= set(PATHS), "unexpected stored source paths")
    return {path: (digest_bytes(git_bytes(snapshot, temporary, "cat-file", "blob", base + ":" + path))
                   if path in present else "0" * 64) for path in PATHS}


def harness_hashes():
    return {name: digest(ROOT / name) for name in SCRIPT_NAMES}


def validate_target(target, args, slot):
    require(slot in SLOTS, "unknown interpreter slot")
    allowed = {(name, arguments) for _, name, arguments in TARGETS}
    allowed.add(("tools/generate_test_inventory.py", ("--write",)))
    require((target, tuple(args)) in allowed, "target/arguments outside finite wall")


def validate_setup_value(setup):
    keys = {"schema_version", "label", "source", "base", "snapshot", "temporary",
            "environment", "source_sha256", "stored_blob_sha256", "harness_sha256"}
    require(type(setup) is dict and set(setup) == keys, "snapshot metadata schema")
    require(setup["schema_version"] == "pontius-c-authority-snapshot-v1", "snapshot metadata version")
    require(type(setup["label"]) is str and
            re.fullmatch("[a-z0-9][a-z0-9-]{0,100}", setup["label"]), "invalid snapshot label")
    require(is_digest(setup["base"], 40), "invalid snapshot base")
    require(setup["source"] == "working" or setup["source"] == setup["base"],
            "snapshot source/base mismatch")
    for field in ("source_sha256", "stored_blob_sha256"):
        mapping = setup[field]
        require(type(mapping) is dict and set(mapping) == set(PATHS)
                and all(is_digest(item) for item in mapping.values()), "source hash schema")
    require(type(setup["harness_sha256"]) is dict
            and set(setup["harness_sha256"]) == set(SCRIPT_NAMES)
            and all(is_digest(item) for item in setup["harness_sha256"].values()),
            "harness hash schema")


def load_setup(metadata, metadata_sha256):
    require(is_digest(metadata_sha256), "invalid metadata digest")
    metadata = checked_path(metadata)
    raw = metadata.read_bytes()
    require(digest_bytes(raw) == metadata_sha256, "snapshot metadata changed")
    setup = json_bytes(raw)
    validate_setup_value(setup)
    require(metadata == ROOT / (setup["label"] + "-snapshot-v2.json"), "metadata path mismatch")
    snapshot = checked_path(setup["snapshot"], directory=True)
    temporary = checked_path(setup["temporary"], directory=True)
    require(snapshot.name == "harness" and snapshot.parent.parent == SNAPSHOTS,
            "snapshot outside disposable root")
    require(re.fullmatch(re.escape(setup["label"]) + "-[0-9a-f]{32}", snapshot.parent.name),
            "snapshot identity mismatch")
    require(temporary == snapshot.parent / "temp", "temporary root mismatch")
    require(setup["environment"] == control_environment(temporary, snapshot),
            "snapshot environment changed")
    require(setup["harness_sha256"] == harness_hashes(), "harness bytes changed")
    require(git_bytes(snapshot, temporary, "rev-parse", "--verify", "HEAD").decode().strip()
            == setup["base"], "snapshot HEAD changed")
    expected = stored_hashes(snapshot, setup["base"], temporary)
    require(expected == setup["stored_blob_sha256"], "stored blob hashes changed")
    if setup["source"] != "working":
        require(setup["source_sha256"] == expected, "frozen source differs from stored blobs")
    return setup


def prepare(label, source):
    require(type(label) is str and re.fullmatch("[a-z0-9][a-z0-9-]{0,100}", label),
            "invalid preparation label")
    require(source == "working" or is_digest(source, 40), "preparation needs exact commit")
    metadata = ROOT / (label + "-snapshot-v2.json")
    require(not metadata.exists(), "snapshot metadata already exists")
    checked_path(SNAPSHOTS, directory=True)
    parent = SNAPSHOTS / (label + "-" + uuid.uuid4().hex)
    parent.mkdir()
    snapshot, temporary = parent / "harness", parent / "temp"
    temporary.mkdir()
    git_bytes(parent, temporary, "clone", "--shared", "--no-checkout", str(REPOSITORY), str(snapshot))
    base = BASE if source == "working" else source
    git_bytes(snapshot, temporary, "checkout", "--detach", base)
    require(git_bytes(snapshot, temporary, "rev-parse", "--verify", "HEAD").decode().strip()
            == base, "checkout did not select candidate")
    expected = stored_hashes(snapshot, base, temporary)
    if source == "working":
        for path in PATHS:
            destination = snapshot / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            checked_path(destination.parent, directory=True)
            if destination.exists():
                checked_path(destination)
            destination.write_bytes(checked_path(WORK / path).read_bytes())
    hashes = source_hashes(snapshot)
    require(source == "working" or hashes == expected, "checkout bytes differ from stored blobs")
    setup = {"schema_version": "pontius-c-authority-snapshot-v1", "label": label,
             "source": source, "base": base, "snapshot": str(snapshot),
             "temporary": str(temporary), "environment": control_environment(temporary, snapshot),
             "source_sha256": hashes, "stored_blob_sha256": expected,
             "harness_sha256": harness_hashes()}
    create(metadata, setup)
    load_setup(str(metadata), digest(metadata))
    print(json.dumps({"metadata": str(metadata), "sha256": digest(metadata)}))


WRAPPER = """import sys, runpy, json, importlib.util
from pathlib import Path
exe, version, target, *args = sys.argv[1:]
def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)
require(sys.implementation.name == 'cpython', 'payload is not CPython')
require(Path(sys.executable).resolve() == Path(exe).resolve(), 'wrong payload executable')
require('.'.join(map(str, sys.version_info[:3])) == version, 'wrong payload version')
require(sys.flags.safe_path and sys.dont_write_bytecode and not sys.flags.optimize,
        'payload flags differ')
identity = dict(executable=sys.executable, implementation=sys.implementation.name,
                version=sys.version, version_info=list(sys.version_info[:3]))
print(json.dumps(dict(identity_before_payload_import=identity)), flush=True)
origin = Path(importlib.util.find_spec('pontius.v0a.trace').origin)
require(origin.resolve() == (Path.cwd()/'src/pontius/v0a/trace.py').resolve(),
        'payload imported outside snapshot')
sys.argv = [target, *args]
if target.startswith('module:'):
    runpy.run_module(target.split(':', 1)[1], run_name='__main__')
else:
    runpy.run_path(target, run_name='__main__')
"""


def run(metadata, metadata_sha256, slot, label, target, *args):
    validate_target(target, args, slot)
    require(re.fullmatch("[a-z0-9][a-z0-9-]{0,100}", label) is not None, "invalid run label")
    setup = load_setup(metadata, metadata_sha256)
    snapshot, temporary = Path(setup["snapshot"]), Path(setup["temporary"])
    before = source_hashes(snapshot)
    require(before == setup["source_sha256"], "snapshot source changed before payload")
    directory = ROOT / "coordinator-checks"
    directory.mkdir(exist_ok=True)
    checked_path(directory, directory=True)
    log = directory / (label + "-" + slot + ".txt")
    receipt_path = directory / (label + "-" + slot + "-receipt.json")
    require(not log.exists() and not receipt_path.exists(), "payload output already exists")
    exe, version = SLOTS[slot]
    checked_path(exe)
    command = [exe, "-B", "-P", "-c", WRAPPER, exe, version, target, *args]
    result = subprocess.run(command, cwd=snapshot, env=setup["environment"], capture_output=True)
    with log.open("xb") as stream:
        stream.write((result.stdout + result.stderr).replace(b"\r\n", b"\n"))
    after = source_hashes(snapshot)
    changed = [path for path in PATHS if before[path] != after[path]]
    allowed = {"tests/test-inventory.json", "tests/test-profiles.toml"} if (
        target == "tools/generate_test_inventory.py" and tuple(args) == ("--write",)) else set()
    require(set(changed) <= allowed, "payload changed disallowed source: " + repr(changed))
    load_setup(metadata, metadata_sha256)
    require(stored_hashes(snapshot, setup["base"], temporary) == setup["stored_blob_sha256"],
            "stored blobs changed after payload")
    first_line = result.stdout.splitlines()[0] if result.stdout.splitlines() else b"{}"
    identity = json_bytes(first_line).get("identity_before_payload_import")
    require(type(identity) is dict and identity.get("implementation") == "cpython"
            and identity.get("version_info") == [int(part) for part in version.split(".")]
            and Path(identity.get("executable", "")).resolve() == Path(exe).resolve(),
            "missing or mismatched pre-import runtime identity")
    receipt = {"schema_version": "pontius-c-authority-receipt-v1", "label": label, "slot": slot,
               "base": setup["base"], "snapshot": str(snapshot), "command": command,
               "environment": setup["environment"], "metadata_sha256": metadata_sha256,
               "harness_sha256": setup["harness_sha256"], "runtime_identity": identity,
               "control_runtime_identity": runtime_identity(), "exit": result.returncode,
               "log": str(log), "sha256": digest(log), "before_sha256": before,
               "after_sha256": after, "stored_blob_sha256": setup["stored_blob_sha256"],
               "changed_paths": changed}
    create(receipt_path, receipt)
    print(json.dumps({"receipt": str(receipt_path), "exit": result.returncode}))
    return result.returncode


def main(argv):
    require_control_runtime()
    require(bool(argv), "missing operation")
    mode, *args = argv
    if mode == "prepare":
        require(len(args) == 2, "prepare needs label and source")
        prepare(*args)
        return 0
    if mode == "run":
        require(len(args) >= 5, "run needs metadata, digest, slot, label, target")
        return run(*args)
    raise Blocker("unknown operation")


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:
        print(json.dumps({"blocker": type(exc).__name__, "reason": str(exc)}), file=sys.stderr)
        sys.exit(2)

