"""Three-phase v28 production-primitive control; no execution authorized by authoring.

Run using the exact floor interpreter with -I -S -B -P.
Arguments: LABEL SLOT SEED CONFIG_RELATIVE CONFIG_SHA256
For SLOT=314 append FLOOR_RECEIPT_RELATIVE FLOOR_RECEIPT_SHA256.
Root creates the fully pinned config only after reviewing every final input.
One invocation runs one selected slot/seed, never an automatic matrix.
The complete candidate/support references are static-only; only verified extracted
primitive nodes and original oracle code are imported in the isolated child.
"""
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import stat
import subprocess
import sys
import uuid

P = pathlib.Path
ROOT = P(r"D:\Pontius-handoffs\v0a-i01-c-authority")
WORKSPACE = P(r"D:\Pontius")
SNAPSHOTS = P(r"D:\pontius-snapshots")
GIT = P(r"C:\Program Files\Git\cmd\git.exe")
BASE_COMMIT = "29c02f6fbd5eb0b7ddc9e816ef28f570b9839358"
TRACKED_COUNT = 1761
SOURCE = P(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1"
           r"\tools\generate_test_inventory.py")
SOURCE_SHA = "e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679"
DISPOSITION = ROOT / "coordinator-radix-prototype-disposition-v1.md"
DISPOSITION_SHA = "e8f75e760d0bb2a4b1c37c8b7cfb571624f60321b804080445c1f2b4d8e1eafa"
OLD_ORACLE = {"path": "tests-checks/storage-oracle-v2.py",
              "sha256": "6a58ef82832d53510f7d44d58cf5a8fa3764f8be5f2c28dcb7e555a83c72cfba"}
OLD_CASES = {"path": "tests-checks/storage-oracle-cases-v2.json",
             "sha256": "3bd5678da334fb551c2f179906e8b4d2cf7a0b0e7a3779e0fad2fb4b4a9c548f"}
SLOTS = {
    "311": (P(r"D:\Pontius-tools\py311\Scripts\python.exe"), "3.11.15"),
    "314": (P(r"D:\Pontius\.venv\Scripts\python.exe"), "3.14.6"),
}
INDEXED_SPEC = {"path": "tests-checks/indexed-storage-extension-spec-v1.md",
                "sha256": "11d11003b3ce84d485df549e73a494e358db69cc6f5db6faea5dae8f50c330f9"}
INDEXED_CASES = {"path": "tests-checks/indexed-storage-extension-cases-v1.json",
                 "sha256": "795e893c4fbeee3963a3ea3cbbffdfacbea193f53063eb4848c8e9ac6d12984a"}
CURSOR_CASES = {"path": "tests-checks/cursor-oracle-cases-v1.json",
                "sha256": "ecddd020ffb2a0d85e624aeb7fb544f631b302839f9a5f3542c998b36c37ac61"}
EXTRA_INPUTS = {'candidate': {'path': 'engineer-generator-v28-storage.py', 'sha256': '4db6502350e59fe363998351384a62d9e669598241a644810e9a7ffd6b4b4d0e'}, 'support_reference': {'path': 'engineer-name-radix-prototype-v1.py', 'sha256': '0c4e9ae2bef9b5489cc00f11adb5dd3400be6f6d5ea90537fb5951bba8ba1a71'}, 'production_binding': {'path': 'engineer-generator-v28-storage-binding-proof-v1.json', 'sha256': 'd786b9a609a37bf88ea18d6d6585d2ffb6cafd6ced908d23c1e086291ed8650c'}, 'production_accounting': {'path': 'engineer-generator-v28-storage-accounting-v1.json', 'sha256': '077c1b4779709672a79368ea1081ecd9cb0499c651851a571a80f075e983c45b'}, 'old_accounting': {'path': 'engineer-name-radix-accounting-v1.json', 'sha256': '79f64e5e7bbb429bedd108654b69c8ab5893973ee742517b543129f762f68f2b'}, 'extractor': {'path': 'tests-checks/v28-primitive-extractor-v2.py', 'sha256': '96f3e980751e0d4851b95340e894c9519b96241fc726d1fac30d324fd99d6d9f'}, 'extraction_proof': {'path': 'tests-checks/v28-primitive-extraction-proof-v1.json', 'sha256': '8b6269d44aecaca6a4df93947439e0f54090b4dedb673a6574c5781e580d6c45'}, 'extraction_plan': {'path': 'tests-checks/v28-primitive-plan-v1.md', 'sha256': 'b9948d186f89e313f5eae829ab9fa4081f03b3260d4bb8f97237d70b4fbdd2ba'}}
EXTRA_COPIES = {'candidate-static.py': 'candidate', 'meter-support-reference-static.py': 'support_reference', 'production-binding.json': 'production_binding', 'production-accounting.json': 'production_accounting', 'old-accounting.json': 'old_accounting', 'extractor.py': 'extractor', 'extraction-proof.json': 'extraction_proof', 'extraction-plan.md': 'extraction_plan'}
FROZEN_DERIVED = {'prototype': {'path': 'tests-checks/v28-primitive-extracted-v1.py', 'sha256': 'bad767aab3b330666fbc4543224e28347a8cf93f8f69d5940c618737dbea2778'}, 'accounting': {'path': 'tests-checks/v28-primitive-accounting-v1.json', 'sha256': '4592e93634857015cd2befa227e7483db1b00895117881d919e6b0508cfa95ca'}, 'cursor_oracle': {'path': 'tests-checks/cursor-oracle-v2.py', 'sha256': '145fe1d59c48e23cdb426bcbe35edbecc3f941a81dc9780e8eeed849be5bc143'}, 'indexed_oracle': {'path': 'tests-checks/indexed-storage-extension-oracle-v2.py', 'sha256': '95ee5d3dd2e31ffd7ea6ecdd2f5e2b05dddb15e5a5ef1aa70ba8820bd82d2381'}}
SCHEMA = "v28-production-primitive-control-v1"
TIMEOUT = 60
PAYLOAD = ".storage-v28-primitive"


def req(value, message):
    if not value:
        raise RuntimeError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def is_digest(value):
    return type(value) is str and re.fullmatch("[0-9a-f]{64}", value) is not None


def validate(path, *, regular=False):
    req(path.is_absolute() and ".." not in path.parts, "unsafe absolute path")
    for ancestor in (path, *path.parents):
        info = ancestor.lstat()
        req(not (getattr(info, "st_file_attributes", 0)
                 & stat.FILE_ATTRIBUTE_REPARSE_POINT), "reparse path: " + str(ancestor))
        if ancestor != path:
            req(stat.S_ISDIR(info.st_mode), "non-directory ancestor: " + str(ancestor))
    if regular:
        req(stat.S_ISREG(path.lstat().st_mode), "non-regular file: " + str(path))
    return path


def local_file(relative):
    req(type(relative) is str and relative, "input path type")
    relative_path = P(relative)
    req(not relative_path.is_absolute() and not relative_path.drive
        and ".." not in relative_path.parts, "unsafe relative input")
    path = ROOT / relative_path
    req(path.is_relative_to(ROOT), "input outside handoff")
    return validate(path, regular=True)


def read_input(entry, suffix):
    req(type(entry) is dict and set(entry) == {"path", "sha256"}, "input schema")
    req(is_digest(entry["sha256"]), "input SHA256")
    path = local_file(entry["path"])
    req(path.suffix == suffix, "input suffix: " + str(path))
    raw = path.read_bytes()
    req(digest(raw) == entry["sha256"], "input changed: " + str(path))
    return path, raw


def create(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def write_json(stream, value):
    raw = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")
    stream.seek(0)
    stream.write(raw)
    stream.truncate()
    stream.flush()
    os.fsync(stream.fileno())


def environment_for(temp, snapshot=None, seed=None):
    windows = validate(P(os.environ["SYSTEMROOT"]))
    system = validate(windows / "System32")
    env = {
        "SYSTEMROOT": str(windows), "WINDIR": str(windows),
        "COMSPEC": str(validate(system / "cmd.exe", regular=True)),
        "PATH": str(system), "TEMP": str(temp), "TMP": str(temp),
        "PONTIUS_GIT": str(validate(GIT, regular=True)),
        "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "NUL",
        "GIT_CONFIG_SYSTEM": "NUL", "GIT_ATTR_NOSYSTEM": "1",
        "PYTHONNOUSERSITE": "1",
    }
    if snapshot is not None:
        env["PYTHONPATH"] = str(snapshot / "src")
    if seed is not None:
        env["PYTHONHASHSEED"] = seed
    return env


def git(repository, temp, *arguments):
    command = [
        str(validate(GIT, regular=True)), "-c", "core.autocrlf=false",
        "-c", "core.hooksPath=NUL", "-c", "init.templateDir=",
        "-c", "core.attributesFile=NUL", "-c", "core.fsmonitor=false",
        "-C", str(repository), *arguments,
    ]
    return subprocess.run(
        command, cwd=repository, env=environment_for(temp),
        capture_output=True, check=True, timeout=TIMEOUT,
        creationflags=subprocess.CREATE_NO_WINDOW,
    ).stdout


def hashes(snapshot, names):
    result = {}
    for name in names:
        relative = P(name)
        req(not relative.is_absolute() and not relative.drive
            and ".." not in relative.parts, "unsafe manifest name")
        path = snapshot / relative
        req(path.is_relative_to(snapshot), "manifest outside snapshot")
        result[name] = digest(validate(path, regular=True).read_bytes())
    return result


def check_summary(summary, expected, case_sha, version, seed):
    req(type(summary) is dict, "oracle summary missing")
    req(summary.get("all_completed") is True, "oracle not all_completed")
    req(summary.get("failures") == [], "oracle failures")
    for key in ("planned_cases", "planned_runs"):
        req(type(summary.get(key)) is int and summary[key] == expected[key],
            "unexpected oracle " + key)
    req(type(summary.get("completed_runs")) is int
        and summary["completed_runs"] == expected["planned_runs"], "incomplete runs")
    req(summary.get("case_pack_sha256") == case_sha, "oracle case SHA mismatch")
    req(summary.get("runtime") == [int(part) for part in version.split(".")],
        "oracle runtime mismatch")
    req(summary.get("hash_seed") == seed, "oracle seed mismatch")
    req(type(summary.get("maximum_meter_limit")) is int
        and summary.get("maximum_meter_limit") == 262144, "oracle meter limit mismatch")


def check_extraction_record(record, config):
    req(record.get("candidate_sha256") == config["candidate"]["sha256"]
        and record.get("extracted_sha256") == config["prototype"]["sha256"]
        and record.get("accounting_sha256") == config["accounting"]["sha256"]
        and record.get("proof_sha256") == config["extraction_proof"]["sha256"]
        and is_digest(record.get("current_runtime_proof_sha256"))
        and type(record.get("production_nodes_verified")) is int
        and record["production_nodes_verified"] == 47
        and record.get("static_only") is True, "extraction verification pins/claims")


WRAPPER = r'''"""Finite stdlib bootstrap; no Pontius import or target body execution."""
import hashlib
import importlib.util
import json
import os
import pathlib
import stat
import sys

P = pathlib.Path

def req(value, message):
    if not value:
        raise RuntimeError(message)

def h(raw):
    return hashlib.sha256(raw).hexdigest()

def checked(path):
    req(path.is_absolute() and ".." not in path.parts, "unsafe child path")
    for ancestor in (path, *path.parents):
        info = ancestor.lstat()
        req(not (getattr(info, "st_file_attributes", 0)
                 & stat.FILE_ATTRIBUTE_REPARSE_POINT), "child reparse path")
        if ancestor != path:
            req(stat.S_ISDIR(info.st_mode), "child non-directory ancestor")
    req(stat.S_ISREG(path.lstat().st_mode), "child non-regular file")
    return path

def emit(record):
    print(json.dumps({"v28_primitive_control": record}, sort_keys=True), flush=True)

def no_pontius():
    req(not any(name == "pontius" or name.startswith("pontius.")
                for name in sys.modules), "Pontius was imported")

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, checked(path))
    req(spec is not None and spec.loader is not None, "payload import spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    no_pontius()
    return module

def check(summary, expected, case_sha, version, seed):
    req(type(summary) is dict and summary.get("all_completed") is True,
        "oracle incomplete or missing summary")
    req(summary.get("failures") == [], "oracle failures")
    for key in ("planned_cases", "planned_runs"):
        req(type(summary.get(key)) is int and summary[key] == expected[key],
            "unexpected oracle " + key)
    req(type(summary.get("completed_runs")) is int
        and summary["completed_runs"] == expected["planned_runs"], "incomplete oracle runs")
    req(summary.get("case_pack_sha256") == case_sha, "case pack SHA mismatch")
    req(summary.get("runtime") == list(map(int, version.split("."))), "runtime mismatch")
    req(summary.get("hash_seed") == seed, "seed mismatch")
    req(type(summary.get("maximum_meter_limit")) is int
        and summary.get("maximum_meter_limit") == 262144, "meter limit mismatch")

def main():
    req(len(sys.argv) == 7, "child argument count")
    exe, version, seed, manifest_sha, environment_sha, payload_name = sys.argv[1:]
    req(sys.implementation.name == "cpython", "child implementation")
    req(".".join(map(str, sys.version_info[:3])) == version, "child version")
    req(P(sys.executable).resolve() == checked(P(exe)).resolve(), "child executable")
    req(sys.flags.safe_path and sys.flags.no_site and sys.dont_write_bytecode
        and not sys.flags.optimize and not sys.flags.isolated
        and not sys.flags.ignore_environment, "child flags")
    req(seed in {"0", "1", "17"} and os.environ.get("PYTHONHASHSEED") == seed,
        "child seed")
    actual_environment = dict(os.environ)
    req(h(json.dumps(actual_environment, sort_keys=True).encode()) == environment_sha,
        "child environment differs from exact scrubbed environment")
    snapshot = P.cwd()
    req(os.environ.get("PYTHONPATH") == str(snapshot / "src"), "child PYTHONPATH")
    req(P(os.environ["PONTIUS_GIT"]) == P(r"C:\Program Files\Git\cmd\git.exe"),
        "child Git")
    no_pontius()
    pontius_spec = importlib.util.find_spec("pontius")
    req(pontius_spec is not None and pontius_spec.origin is not None,
        "missing read-only Pontius origin")
    req(P(pontius_spec.origin).resolve() == (snapshot / "src/pontius/__init__.py").resolve(),
        "Pontius origin outside snapshot")
    no_pontius()
    req(payload_name == ".storage-v28-primitive", "payload directory")
    payload = snapshot / payload_name
    manifest_raw = checked(payload / "manifest.json").read_bytes()
    req(h(manifest_raw) == manifest_sha, "manifest SHA mismatch")
    manifest = json.loads(manifest_raw)
    wanted_files = 1787 if version == "3.14.6" else 1782
    req(type(manifest) is dict and len(manifest) == wanted_files, "manifest file count")
    for name, wanted in manifest.items():
        relative = P(name)
        req(not relative.is_absolute() and not relative.drive
            and ".." not in relative.parts, "manifest name")
        req(h(checked(snapshot / relative).read_bytes()) == wanted,
            "manifest input changed: " + name)
    config = json.loads(checked(payload / "config.json").read_bytes())
    emit({"kind": "identity_before_payload_imports", "executable": sys.executable,
          "version": sys.version, "version_info": list(sys.version_info[:3]),
          "implementation": sys.implementation.name, "cwd": str(snapshot),
          "flags": str(sys.flags), "hash_seed": seed,
          "hash_probe": hash("pontius-storage-order-probe"),
          "environment": actual_environment, "manifest_sha256": manifest_sha,
          "verified_files": len(manifest), "pontius_imported": False,
          "prototype_sha256": config["prototype"]["sha256"],
          "accounting_sha256": config["accounting"]["sha256"],
          "candidate_sha256": config["candidate"]["sha256"],
          "extraction_proof_sha256": config["extraction_proof"]["sha256"]})
    req(h(checked(payload / "prototype.py").read_bytes()) == config["prototype"]["sha256"],
        "prototype content pin")
    accounting_raw = checked(payload / "accounting.json").read_bytes()
    req(h(accounting_raw) == config["accounting"]["sha256"], "accounting content pin")
    accounting = json.loads(accounting_raw)
    req(accounting["schema"] == "pontius-indexed-storage-accounting-v1"
        and accounting["prototype_sha256"] == config["prototype"]["sha256"],
        "accounting source identity")
    verifier = load("static_extraction_verifier", payload / "extractor.py")
    extraction = verifier.verify_extraction(*[checked(payload / name).read_bytes() for name in (
        "candidate-static.py", "meter-support-reference-static.py", "production-binding.json",
        "production-accounting.json", "old-accounting.json", "prototype.py",
        "accounting.json", "extraction-proof.json")])
    req(extraction["candidate_sha256"] == config["candidate"]["sha256"]
        and extraction["extracted_sha256"] == config["prototype"]["sha256"]
        and extraction["accounting_sha256"] == config["accounting"]["sha256"]
        and extraction["proof_sha256"] == config["extraction_proof"]["sha256"]
        and type(extraction["production_nodes_verified"]) is int
        and extraction["production_nodes_verified"] == 47
        and extraction["static_only"] is True, "static extraction verification")
    emit({"kind": "static_extraction_verified", **extraction})
    prototype = load("v28_extracted_primitive_under_test", payload / "prototype.py")
    passed = True
    definitions = (
        ("storage", "old_oracle.py", "verify_storage", "old_cases.json",
         {"planned_cases": 28, "planned_runs": 34}, config["old_cases"]["sha256"]),
        ("cursor", "cursor_oracle.py", "verify_cursor", "cursor_cases.json",
         config["cursor_expected"], config["cursor_cases"]["sha256"]),
        ("indexed", "indexed_oracle.py", "verify_indexed", "indexed_cases.json",
         config["indexed_expected"], config["indexed_cases"]["sha256"]),
    )
    for phase, oracle_name, function_name, case_name, expected, case_sha in definitions:
        summary = None
        try:
            oracle = load("independent_" + phase + "_oracle", payload / oracle_name)
            kwargs = {"case_path": payload / case_name}
            if phase == "indexed":
                kwargs.update(accounting_path=payload / "accounting.json",
                              accounting_sha256=config["accounting"]["sha256"])
            summary = getattr(oracle, function_name)(prototype, **kwargs)
            no_pontius()
            check(summary, expected, case_sha, version, seed)
            if phase == "indexed":
                req(summary.get("accounting_sha256") == config["accounting"]["sha256"]
                    and summary.get("prototype_sha256") == config["prototype"]["sha256"],
                    "indexed summary input pins")
                req(summary.get("accounting_complete") is True
                    and summary.get("fitness_passed") is True,
                    "indexed accounting or finite fitness incomplete/failed")
        except BaseException as error:
            passed = False
            emit({"kind": "phase_result", "phase": phase, "ok": False,
                  "summary": summary, "error_type": type(error).__name__,
                  "error": str(error)})
        else:
            emit({"kind": "phase_result", "phase": phase, "ok": True, "summary": summary})
    no_pontius()
    emit({"kind": "completed", "ok": passed})
    return 0 if passed else 1

if __name__ == "__main__":
    raise SystemExit(main())
'''


def main():
    req(sys.implementation.name == "cpython"
        and sys.version_info[:3] == (3, 11, 15), "control version")
    req(P(sys.executable).resolve() == validate(SLOTS["311"][0], regular=True).resolve(),
        "control executable")
    req(sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path
        and sys.dont_write_bytecode and not sys.flags.optimize, "control flags")
    req(len(sys.argv) in {6, 8}, "control argument count")
    label, slot, seed, config_relative, config_sha = sys.argv[1:6]
    req(re.fullmatch("[a-z0-9][a-z0-9-]{0,70}", label) is not None, "label")
    req(slot in SLOTS and seed in {"0", "1", "17"}, "slot/seed")
    req(is_digest(config_sha), "root-pinned config SHA256 required")
    req((slot == "311" and len(sys.argv) == 6)
        or (slot == "314" and len(sys.argv) == 8), "floor receipt arguments")
    validate(ROOT)
    checks = validate(ROOT / "tests-checks")
    prefix = "v28-primitive-" + label + "-" + slot + "-seed" + seed
    paths = {key: checks / (prefix + suffix) for key, suffix in (
        ("setup", "-setup.json"), ("receipt", "-receipt.json"),
        ("stdout", ".stdout.txt"), ("stderr", ".stderr.txt"), ("log", ".txt"),
    )}
    req(not any(path.exists() for path in paths.values()), "retained outputs already exist")
    streams = {key: path.open("x+b") for key, path in paths.items()}
    setup = {"schema": SCHEMA, "label": label, "slot": slot, "seed": seed,
             "base_commit": BASE_COMMIT, "config_sha256": config_sha,
             "production_watch_sha256": SOURCE_SHA, "candidate_sha256": EXTRA_INPUTS["candidate"]["sha256"],
             "disposition_sha256": DISPOSITION_SHA}
    receipt = dict(setup)
    receipt.update({"success": False, "integrity_ok": False, "payload_started": False})
    phase = "preflight"
    process = None
    snapshot = None
    before = {}
    input_paths = {}
    manifest_sha = None
    exit_code = None
    write_json(streams["setup"], setup)
    try:
        config_path = local_file(config_relative)
        config_raw = config_path.read_bytes()
        req(digest(config_raw) == config_sha, "root-pinned config changed")
        config = json.loads(config_raw)
        fields = {"schema", "control_sha256", "disposition_sha256", "prototype",
                  "old_oracle", "old_cases", "cursor_oracle", "cursor_cases", "cursor_expected",
                  "indexed_oracle", "indexed_cases", "indexed_expected", "accounting", "indexed_spec"}
        fields |= set(EXTRA_INPUTS)
        req(type(config) is dict and set(config) == fields
            and config["schema"] == SCHEMA, "config schema")
        req(config["disposition_sha256"] == DISPOSITION_SHA, "historical disposition pin")
        req(all(config[key] == value for key, value in {**EXTRA_INPUTS, **FROZEN_DERIVED}.items()),
            "frozen production extraction or unchanged oracle inputs differ")
        req(config["old_oracle"] == OLD_ORACLE and config["old_cases"] == OLD_CASES,
            "old oracle/cases are frozen")
        req(config["indexed_cases"] == INDEXED_CASES and config["indexed_spec"] == INDEXED_SPEC
            and config["cursor_cases"] == CURSOR_CASES, "frozen successor/extension inputs")
        req(config["cursor_expected"] == {"planned_cases": 16, "planned_runs": 28}
            and config["indexed_expected"] == {"planned_cases": 16, "planned_runs": 31},
            "fixed finite populations")
        expected = config["cursor_expected"]
        req(type(expected) is dict and set(expected) == {"planned_cases", "planned_runs"},
            "cursor expected schema")
        req(type(expected["planned_cases"]) is int and 1 <= expected["planned_cases"] <= 16,
            "cursor planned cases")
        req(type(expected["planned_runs"]) is int
            and expected["planned_runs"] >= expected["planned_cases"], "cursor planned runs")
        req(all(type(config["indexed_expected"][key]) is int
                for key in ("planned_cases", "planned_runs")), "indexed population exact types")
        control_path = validate(P(__file__).absolute(), regular=True)
        control_raw = control_path.read_bytes()
        req(is_digest(config["control_sha256"])
            and digest(control_raw) == config["control_sha256"], "control SHA mismatch")
        req(digest(validate(SOURCE, regular=True).read_bytes()) == SOURCE_SHA,
            "production watch changed")
        disposition_raw = validate(DISPOSITION, regular=True).read_bytes()
        req(digest(disposition_raw) == DISPOSITION_SHA, "root disposition changed")
        inputs = {}
        for key, suffix in (("prototype", ".py"), ("old_oracle", ".py"),
                            ("old_cases", ".json"), ("cursor_oracle", ".py"),
                            ("cursor_cases", ".json"), ("indexed_oracle", ".py"),
                            ("indexed_cases", ".json"), ("accounting", ".json"),
                            ("indexed_spec", ".md")):
            path, raw = read_input(config[key], suffix)
            input_paths[key] = path
            inputs[key] = raw
        for key, entry in EXTRA_INPUTS.items():
            path, raw = read_input(config[key], P(entry["path"]).suffix)
            input_paths[key], inputs[key] = path, raw
        req(len(set(input_paths.values())) == 17, "input paths must be distinct")
        accounting = json.loads(inputs["accounting"])
        req(accounting.get("schema") == "pontius-indexed-storage-accounting-v1"
            and accounting.get("prototype_sha256") == config["prototype"]["sha256"],
            "accounting map must bind this prototype")
        input_paths.update({"control": control_path, "config": config_path,
                            "disposition": DISPOSITION, "production_watch": SOURCE})
        input_hashes = {key: digest(validate(path, regular=True).read_bytes())
                        for key, path in input_paths.items()}
        wanted_hashes = {key: config[key]["sha256"] for key in (
            "prototype", "old_oracle", "old_cases", "cursor_oracle", "cursor_cases",
            "indexed_oracle", "indexed_cases", "accounting", "indexed_spec") }
        wanted_hashes.update({key: entry["sha256"] for key, entry in EXTRA_INPUTS.items()})
        wanted_hashes.update({"control": digest(control_raw), "config": config_sha,
                              "disposition": DISPOSITION_SHA, "production_watch": SOURCE_SHA})
        req(input_hashes == wanted_hashes, "input changed during preflight")
        exe, version = SLOTS[slot]
        validate(exe, regular=True)
        floor_files = {}
        if slot == "314":
            floor_relative, floor_sha = sys.argv[6:8]
            req(is_digest(floor_sha), "root-pinned floor receipt SHA256")
            floor_path = local_file(floor_relative)
            floor_raw = floor_path.read_bytes()
            req(digest(floor_raw) == floor_sha, "floor receipt changed")
            floor = json.loads(floor_raw)
            req(floor.get("schema") == SCHEMA and floor.get("slot") == "311"
                and floor.get("seed") == seed, "floor slot/seed/schema")
            req(floor.get("config_sha256") == config_sha
                and floor.get("control_sha256") == digest(control_raw), "floor input pins")
            req(floor.get("success") is True and floor.get("integrity_ok") is True
                and type(floor.get("exit")) is int and floor["exit"] == 0
                and floor.get("payload_started") is True
                and floor.get("result_ok") is True
                and type(floor.get("process_returncode")) is int
                and floor["process_returncode"] == 0
                and "error" not in floor and "cleanup_error" not in floor
                and not floor.get("timeout"), "floor did not succeed")
            req(floor.get("input_hashes_before") == input_hashes
                and floor.get("input_hashes_after") == input_hashes, "floor source input hashes")
            req(floor["before"] == floor["after"]
                and floor["manifest_after_sha256"] == floor["manifest_sha256"],
                "floor manifest receipt differs")
            floor_snapshot = validate(P(floor["snapshot"]))
            req(floor_snapshot.is_relative_to(SNAPSHOTS), "floor snapshot root")
            req(hashes(floor_snapshot, floor["before"]) == floor["before"], "floor files changed")
            req(digest(validate(floor_snapshot / PAYLOAD / "manifest.json", regular=True).read_bytes())
                == floor["manifest_sha256"], "floor manifest changed")
            floor_files["floor-receipt.json"] = floor_raw
            for key in ("setup", "stdout", "stderr", "log"):
                item = floor["outputs"][key]
                path = validate(P(item["path"]), regular=True)
                req(path.is_relative_to(ROOT), "floor output root")
                raw = path.read_bytes()
                req(digest(raw) == item["sha256"], "floor output changed: " + key)
                floor_files["floor-" + key + (".json" if key == "setup" else ".txt")] = raw
                input_paths["floor_" + key] = path
                input_hashes["floor_" + key] = item["sha256"]
            floor_records = []
            for line in floor_files["floor-stdout.txt"].splitlines():
                obj = json.loads(line)
                if isinstance(obj, dict) and isinstance(obj.get("v28_primitive_control"), dict):
                    floor_records.append(obj["v28_primitive_control"])
            floor_identities = [x for x in floor_records if x.get("kind") == "identity_before_payload_imports"]
            floor_results = [x for x in floor_records if x.get("kind") == "phase_result"]
            floor_completed = [x for x in floor_records if x.get("kind") == "completed"]
            floor_extractions = [x for x in floor_records if x.get("kind") == "static_extraction_verified"]
            floor_setup = json.loads(floor_files["floor-setup.json"])
            req(type(floor_setup) is dict
                and all(key in floor and floor[key] == value
                        for key, value in floor_setup.items()), "floor setup/receipt differ")
            req(floor_records == floor.get("retained_control_records")
                and floor_identities == floor.get("identity_records")
                and floor_completed == floor.get("completed_records")
                and floor_extractions == floor.get("extraction_records"),
                "floor raw identity/completion streams differ")
            req([x.get("kind") for x in floor_records] == [
                    "identity_before_payload_imports", "static_extraction_verified", "phase_result", "phase_result",
                    "phase_result", "completed"]
                and [x.get("phase") for x in floor_results] == ["storage", "cursor", "indexed"]
                and floor_completed == [{"kind": "completed", "ok": True}]
                and floor_completed[0].get("ok") is True,
                "floor record order/completion")
            req(len(floor_extractions) == 1, "floor extraction record population")
            check_extraction_record(floor_extractions[0], config)
            floor_identity = floor_identities[0]
            req(floor_identity.get("implementation") == "cpython"
                and floor_identity.get("cwd") == str(floor_snapshot)
                and floor_identity.get("environment") == floor_setup["environment"]
                and floor_identity.get("manifest_sha256") == floor_setup["manifest_sha256"]
                and floor_identity.get("verified_files") == len(floor["before"]) == 1782
                and floor_identity.get("prototype_sha256") == config["prototype"]["sha256"]
                and floor_identity.get("accounting_sha256") == config["accounting"]["sha256"]
                and floor_identity.get("candidate_sha256") == config["candidate"]["sha256"]
                and floor_identity.get("extraction_proof_sha256") == config["extraction_proof"]["sha256"]
                and floor_identity.get("pontius_imported") is False,
                "floor raw identity context")
            req(floor_setup["config"] == config
                and floor_setup["snapshot"] == str(floor_snapshot)
                and floor_setup["before"] == floor["before"]
                and floor_setup["input_hashes_before"] == wanted_hashes,
                "floor setup input context")
            req(len(floor_identities) == 1
                and floor_identities[0]["version_info"] == [3, 11, 15]
                and P(floor_identities[0]["executable"]).resolve() == SLOTS["311"][0].resolve()
                and floor_identities[0]["hash_seed"] == seed, "actual floor identity")
            req(floor_results == floor["phase_results"] and len(floor_results) == 3,
                "floor result streams differ")
            for result, want, case_key in zip(floor_results,
                    ({"planned_cases": 28, "planned_runs": 34}, expected, config["indexed_expected"]),
                    ("old_cases", "cursor_cases", "indexed_cases"), strict=True):
                req(result.get("ok") is True, "floor phase failed")
                check_summary(result["summary"], want, config[case_key]["sha256"], "3.11.15", seed)
            indexed_summary = floor_results[-1]["summary"]
            req(indexed_summary.get("accounting_complete") is True
                and indexed_summary.get("fitness_passed") is True
                and indexed_summary.get("accounting_sha256") == config["accounting"]["sha256"]
                and indexed_summary.get("prototype_sha256") == config["prototype"]["sha256"],
                "floor indexed fitness/accounting")
            setup["floor_receipt"] = {"path": str(floor_path), "sha256": floor_sha}
            input_paths["floor_receipt"] = floor_path
            input_hashes["floor_receipt"] = floor_sha
        phase = "clone"
        validate(SNAPSHOTS)
        validate(WORKSPACE)
        folder = SNAPSHOTS / ("v28-primitive-" + uuid.uuid4().hex)
        req(folder.is_relative_to(SNAPSHOTS), "snapshot outside D-local root")
        folder.mkdir()
        validate(folder)
        temp = folder / "temp"
        temp.mkdir()
        validate(temp)
        snapshot = folder / "snapshot"
        git(folder, temp, "clone", "--shared", "--no-checkout", str(WORKSPACE), str(snapshot))
        validate(snapshot)
        git(snapshot, temp, "checkout", "--detach", BASE_COMMIT)
        head = git(snapshot, temp, "rev-parse", "HEAD").decode().strip()
        req(head == BASE_COMMIT, "wrong snapshot commit")
        req(not git(snapshot, temp, "status", "--porcelain", "--untracked-files=all"),
            "dirty initial snapshot")
        tracked = git(snapshot, temp, "ls-files", "-z").decode("utf-8").split("\0")[:-1]
        req(len(tracked) == TRACKED_COUNT and len(set(tracked)) == TRACKED_COUNT,
            "r010 tracked-file count mismatch")
        before = hashes(snapshot, tracked)
        payload = snapshot / PAYLOAD
        payload.mkdir()
        validate(payload)
        files = {
            "prototype.py": inputs["prototype"], "old_oracle.py": inputs["old_oracle"],
            "old_cases.json": inputs["old_cases"], "cursor_oracle.py": inputs["cursor_oracle"],
            "cursor_cases.json": inputs["cursor_cases"], "control.py": control_raw,
            "config.json": config_raw, "disposition.md": disposition_raw,
            "wrapper.py": WRAPPER.encode("utf-8"),
            "indexed_oracle.py": inputs["indexed_oracle"],
            "indexed_cases.json": inputs["indexed_cases"],
            "accounting.json": inputs["accounting"],
            "indexed-storage-extension-spec-v1.md": inputs["indexed_spec"],
            **{name: inputs[key] for name, key in EXTRA_COPIES.items()},
            **floor_files,
        }
        for name, raw in files.items():
            create(payload / name, raw)
            before[PAYLOAD + "/" + name] = digest(raw)
        req(len(before) == TRACKED_COUNT + len(files), "complete manifest count")
        manifest_raw = (json.dumps(before, indent=2, sort_keys=True) + "\n").encode()
        create(payload / "manifest.json", manifest_raw)
        manifest_sha = digest(manifest_raw)
        env = environment_for(temp, snapshot, seed)
        environment_sha = digest(json.dumps(env, sort_keys=True).encode())
        command = [str(exe), "-S", "-B", "-P", str(payload / "wrapper.py"),
                   str(exe), version, seed, manifest_sha, environment_sha, PAYLOAD]
        setup.update({"control_sha256": digest(control_raw), "config": config,
                      "input_hashes_before": input_hashes, "input_paths": {
                          key: str(path) for key, path in input_paths.items()},
                      "tracked_file_count": len(tracked), "snapshot": str(snapshot),
                      "payload_directory": str(payload), "temp": str(temp),
                      "head_before": head, "before": before, "manifest_sha256": manifest_sha,
                      "command": command, "environment": env, "timeout_seconds": TIMEOUT})
        receipt.update(setup)
        write_json(streams["setup"], setup)
        phase = "payload"
        receipt["payload_started"] = True
        process = subprocess.Popen(
            command, cwd=snapshot, env=env,
            stdout=streams["stdout"], stderr=streams["stderr"],
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        try:
            exit_code = process.wait(timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=TIMEOUT)
            exit_code = 124
            receipt["timeout"] = True
            raise RuntimeError("finite v28 primitive oracle timed out after 60 seconds")
        phase = "result_validation"
        streams["stdout"].flush()
        stdout = paths["stdout"].read_bytes()
        records = []
        for line in stdout.splitlines():
            try:
                value = json.loads(line)
            except (ValueError, UnicodeError):
                continue
            if isinstance(value, dict) and isinstance(value.get("v28_primitive_control"), dict):
                records.append(value["v28_primitive_control"])
        identities = [item for item in records
                      if item.get("kind") == "identity_before_payload_imports"]
        results = [item for item in records if item.get("kind") == "phase_result"]
        completed = [item for item in records if item.get("kind") == "completed"]
        extractions = [item for item in records if item.get("kind") == "static_extraction_verified"]
        receipt["extraction_records"] = extractions
        req(len(extractions) == 1, "extraction record population")
        check_extraction_record(extractions[0], config)
        receipt["identity_records"] = identities
        receipt["phase_results"] = results
        receipt["completed_records"] = completed
        req(len(identities) == 1 and identities[0].get("verified_files") == len(before),
            "missing/duplicate pre-import identity")
        identity = identities[0]
        req(identity.get("implementation") == "cpython"
            and identity.get("version_info") == [int(p) for p in version.split(".")]
            and P(identity["executable"]).resolve() == exe.resolve(), "actual payload runtime")
        req(identity.get("cwd") == str(snapshot) and identity.get("environment") == env
            and identity.get("hash_seed") == seed and identity.get("manifest_sha256") == manifest_sha
            and identity.get("prototype_sha256") == config["prototype"]["sha256"]
            and identity.get("accounting_sha256") == config["accounting"]["sha256"]
            and identity.get("candidate_sha256") == config["candidate"]["sha256"]
            and identity.get("extraction_proof_sha256") == config["extraction_proof"]["sha256"]
            and identity.get("pontius_imported") is False, "payload identity context")
        req(len(results) == 3 and [item.get("phase") for item in results] == ["storage", "cursor", "indexed"],
            "missing or unordered oracle results")
        for item, want, case_key in zip(
            results, ({"planned_cases": 28, "planned_runs": 34}, expected, config["indexed_expected"]),
            ("old_cases", "cursor_cases", "indexed_cases"), strict=True,
        ):
            req(item.get("ok") is True, "oracle phase failed: " + str(item.get("phase")))
            check_summary(item.get("summary"), want, config[case_key]["sha256"], version, seed)
            if case_key == "indexed_cases":
                summary = item["summary"]
                req(summary.get("accounting_sha256") == config["accounting"]["sha256"]
                    and summary.get("prototype_sha256") == config["prototype"]["sha256"],
                    "indexed summary inputs")
                req(summary.get("accounting_complete") is True
                    and summary.get("fitness_passed") is True, "indexed fitness/accounting failed")
        req([item.get("kind") for item in records] == [
                "identity_before_payload_imports", "static_extraction_verified", "phase_result", "phase_result",
                "phase_result", "completed"]
            and completed == [{"kind": "completed", "ok": True}]
            and completed[0].get("ok") is True,
            "child record order/completion")
        req(exit_code == 0, "payload returned nonzero")
        receipt["result_ok"] = True
    except BaseException as error:
        receipt["error"] = {"phase": phase, "type": type(error).__name__, "message": str(error)}
    finally:
        if process is not None and process.poll() is None:
            process.kill()
            try:
                process.wait(timeout=TIMEOUT)
            except BaseException as error:
                receipt["cleanup_error"] = {"type": type(error).__name__, "message": str(error)}
        receipt["exit"] = exit_code
        receipt["process_returncode"] = process.returncode if process is not None else None
        integrity_errors = []
        if before and snapshot is not None:
            try:
                after = {}
                file_errors = []
                for name in before:
                    try:
                        after.update(hashes(snapshot, [name]))
                    except BaseException as error:
                        file_errors.append({"file": name, "type": type(error).__name__,
                                            "message": str(error)})
                receipt["after"] = after
                receipt["after_file_errors"] = file_errors
                req(not file_errors, "snapshot files missing, unsafe, or unreadable")
                req(before == after, "snapshot manifest files changed")
                manifest_after = digest(validate(
                    snapshot / PAYLOAD / "manifest.json", regular=True).read_bytes())
                receipt["manifest_after_sha256"] = manifest_after
                req(manifest_after == manifest_sha, "snapshot manifest changed")
                head_after = git(snapshot, temp, "rev-parse", "HEAD").decode().strip()
                receipt["head_after"] = head_after
                req(head_after == BASE_COMMIT, "snapshot HEAD changed")
                dirty = git(snapshot, temp, "status", "--porcelain",
                            "--untracked-files=all").decode("utf-8")
                receipt["dirty_after"] = dirty
                expected_dirty = {"?? " + PAYLOAD + "/" + name
                                  for name in (*files, "manifest.json")}
                req(set(dirty.splitlines()) == expected_dirty, "unexpected snapshot changes")
            except BaseException as error:
                integrity_errors.append({"check": "snapshot", "type": type(error).__name__,
                                         "message": str(error)})
        else:
            integrity_errors.append({"check": "snapshot", "message": "snapshot not fully prepared"})
        if input_paths:
            try:
                after_inputs = {}
                original_errors = []
                for key, path in input_paths.items():
                    try:
                        after_inputs[key] = digest(validate(path, regular=True).read_bytes())
                    except BaseException as error:
                        original_errors.append({"input": key, "type": type(error).__name__,
                                                "message": str(error)})
                receipt["input_hashes_after"] = after_inputs
                receipt["after_original_errors"] = original_errors
                req(not original_errors, "original inputs missing, unsafe, or unreadable")
                req(after_inputs == input_hashes, "original inputs or production watch changed")
            except BaseException as error:
                integrity_errors.append({"check": "originals", "type": type(error).__name__,
                                         "message": str(error)})
        else:
            integrity_errors.append({"check": "originals", "message": "inputs not validated"})
        receipt["integrity_errors"] = integrity_errors
        receipt["integrity_ok"] = not integrity_errors
        for key in ("stdout", "stderr"):
            streams[key].flush()
            os.fsync(streams[key].fileno())
        stdout = paths["stdout"].read_bytes()
        stderr = paths["stderr"].read_bytes()
        partial_records = []
        for line in stdout.splitlines():
            try:
                value = json.loads(line)
            except (ValueError, UnicodeError):
                continue
            if isinstance(value, dict) and isinstance(value.get("v28_primitive_control"), dict):
                partial_records.append(value["v28_primitive_control"])
        receipt["retained_control_records"] = partial_records
        log = stdout + b"\nCONTROL STDERR\n" + stderr
        if "error" in receipt:
            log += b"\nCONTROL FAILURE\n" + json.dumps(receipt["error"]).encode() + b"\n"
        streams["log"].write(log)
        streams["log"].flush()
        os.fsync(streams["log"].fileno())
        receipt.update({"stdout": str(paths["stdout"]), "stdout_sha256": digest(stdout),
                        "stderr": str(paths["stderr"]), "stderr_sha256": digest(stderr),
                        "log": str(paths["log"]), "log_sha256": digest(log)})
        receipt["outputs"] = {
            key: {"path": str(paths[key]), "sha256": digest(paths[key].read_bytes())}
            for key in ("setup", "stdout", "stderr", "log")
        }
        receipt["success"] = (
            receipt.get("result_ok") is True and receipt["integrity_ok"]
            and "error" not in receipt and "cleanup_error" not in receipt and exit_code == 0
        )
        write_json(streams["receipt"], receipt)
        for stream in streams.values():
            stream.close()
    print(json.dumps({"success": receipt["success"], "exit": exit_code,
                      "receipt": str(paths["receipt"]),
                      "receipt_sha256": digest(paths["receipt"].read_bytes()),
                      "log_sha256": receipt["log_sha256"],
                      "error": receipt.get("error")}, indent=2))
    return 0 if receipt["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
