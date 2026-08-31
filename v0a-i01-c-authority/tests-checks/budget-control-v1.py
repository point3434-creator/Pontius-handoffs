"""Test-author control: stdlib only; no test payload executes on import."""
import ast
import difflib
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import uuid

ROOT = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
WORK = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
REPO = Path(r"D:\Pontius")
GIT = Path(r"C:\Program Files\Git\cmd\git.exe")
BASE = "29c02f6fbd5eb0b7ddc9e816ef28f570b9839358"
TEST = "tests/test_inventory_and_profiles.py"
ORIGINAL = "c46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf"
GENERATOR = "29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692"
OVERLAY = Path(r"D:\pontius-snapshots\c-authority-gen01-0221f3260438426bb9eabf92ce4c3765\harness\tools\generate_test_inventory.py")
OVERLAY_SHA = "cb83045209fd9fcdbc6f4c0afc320ce44235dec9956f33ec1417a92dab8a9fea"
SLOTS = {
    "311": (r"D:\Pontius-tools\py311\Scripts\python.exe", (3, 11, 15)),
    "314": (r"D:\Pontius\.venv\Scripts\python.exe", (3, 14, 6)),
}

def require(ok, reason):
    if not ok:
        raise RuntimeError(reason)

def checked(path, directory=False):
    p = Path(path)
    require(p.is_absolute() and ".." not in p.parts, "nonabsolute/traversing path")
    for part in (p, *p.parents):
        require(not part.lstat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT,
                "reparse path: " + str(part))
    require(p.is_dir() if directory else p.is_file(), "wrong path kind")
    return p

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def create(path, raw):
    with Path(path).open("xb") as stream:
        stream.write(raw)

def emit(path, value):
    create(path, (json.dumps(value, indent=2) + "\n").encode())

def environment(temp, snapshot=None):
    windows = checked(os.environ["SYSTEMROOT"], True)
    env = {
        "SYSTEMROOT": str(windows), "WINDIR": str(windows),
        "COMSPEC": str(windows / "System32/cmd.exe"), "PATH": str(windows / "System32"),
        "TEMP": str(temp), "TMP": str(temp), "PONTIUS_GIT": str(GIT),
        "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "NUL",
        "GIT_CONFIG_SYSTEM": "NUL", "GIT_ATTR_NOSYSTEM": "1", "PYTHONNOUSERSITE": "1",
    }
    if snapshot is not None:
        env["PYTHONPATH"] = str(snapshot / "src")
    return env

def git(repo, temp, *args):
    return subprocess.run([
        str(checked(GIT)), "-c", "core.autocrlf=false", "-c", "core.hooksPath=NUL",
        "-c", "init.templateDir=", "-c", "core.attributesFile=NUL",
        "-c", "core.fsmonitor=false", "-C", str(repo), *args,
    ], env=environment(temp), cwd=repo, check=True, capture_output=True).stdout

def hashes(snapshot, names):
    return {name: sha((snapshot / name).read_bytes()) for name in names}

WRAPPER = """import sys, runpy, json, importlib.util, os
from pathlib import Path
exe, expected = sys.argv[1:3]
assert sys.implementation.name == "cpython"
assert Path(sys.executable).resolve() == Path(exe).resolve()
assert ".".join(map(str, sys.version_info[:3])) == expected
assert sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize
print(json.dumps({"identity_before_import": {
    "executable": sys.executable, "implementation": sys.implementation.name,
    "version": sys.version, "version_info": list(sys.version_info[:3]),
    "cwd": str(Path.cwd()), "pythonpath": os.environ.get("PYTHONPATH"),
}}), flush=True)
assert Path(importlib.util.find_spec("pontius.v0a.trace").origin).resolve() == (
    Path.cwd() / "src/pontius/v0a/trace.py").resolve()
sys.argv = ["D:/Pontius-handoffs/v0a-i01-c-authority/tests-checks/budget-probe-v1.py"]
runpy.run_path(sys.argv[0], run_name="__main__")
"""

def main():
    require(sys.implementation.name == "cpython" and sys.version_info[:3] == (3, 11, 15),
            "wrong control interpreter")
    require(Path(sys.executable).resolve() == Path(SLOTS["311"][0]).resolve(),
            "wrong control executable")
    require(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
            and sys.flags.safe_path, "wrong control flags")
    mode, label, *args = sys.argv[1:]
    require(label.replace("-", "").isalnum(), "invalid control label")
    checks = ROOT / "tests-checks"
    checks.mkdir(exist_ok=True)
    if mode == "apply":
        addition_path, expected = args
        current = (WORK / TEST).read_bytes()
        require(sha(current) == expected, "owned test bytes changed unexpectedly")
        original = git(REPO, ROOT, "cat-file", "blob", BASE + ":" + TEST)
        require(sha(original) == ORIGINAL, "wrong original test blob")
        addition = checked(addition_path).read_bytes()
        require(b"\r" not in addition and not addition.startswith(b"\xef\xbb\xbf"),
                "addition must be LF, no BOM")
        require(all(len(line) <= 100 for line in addition.decode().splitlines()),
                "addition line exceeds 100 columns")
        footer = b'\n\nif __name__ == "__main__":\n    unittest.main()\n'
        require(original.endswith(footer), "unexpected main guard")
        revised = original[:-len(footer)] + addition + footer
        old_tree, new_tree = ast.parse(original), ast.parse(revised)
        added = [node for node in new_tree.body if isinstance(node, ast.ClassDef)
                 and node.name == "AuthorityTransferMatrixTests"]
        require(len(added) == 1, "new test class missing/duplicated")
        new_tree.body.remove(added[0])
        require(ast.dump(new_tree, include_attributes=False)
                == ast.dump(old_tree, include_attributes=False), "old AST changed")
        methods = [node.name for node in added[0].body if isinstance(node, ast.FunctionDef)
                   and node.name.startswith("test_")]
        candidate = ROOT / ("tests-candidate-" + label + ".py")
        patch = ROOT / ("tests-patch-" + label + ".diff")
        require(not candidate.exists() and not patch.exists(), "issued release already exists")
        create(candidate, revised)
        difference = "".join(difflib.unified_diff(
            original.decode().splitlines(keepends=True), revised.decode().splitlines(keepends=True),
            fromfile="a/" + TEST, tofile="b/" + TEST,
        )).encode()
        create(patch, difference)
        (WORK / TEST).write_bytes(revised)
        receipt = {
            "base": BASE, "before_sha256": sha(current), "original_sha256": sha(original),
            "tests_sha256": sha(revised), "candidate": str(candidate),
            "patch": str(patch), "patch_sha256": sha(difference),
            "addition_sha256": sha(addition), "new_methods": methods,
            "all_old_ast_unchanged": True, "old_source_prefix_unchanged": True,
            "control_sha256": sha(Path(__file__).read_bytes()),
        }
        emit(checks / ("apply-" + label + ".json"), receipt)
        print(json.dumps(receipt))
        return 0
    if mode == "prepare":
        candidate_path, expected = args
        candidate = checked(candidate_path)
        require(sha(candidate.read_bytes()) == expected, "released tests changed")
        parent = Path(r"D:\pontius-snapshots") / ("c-authority-tests-" + label + "-" + uuid.uuid4().hex)
        parent.mkdir()
        temporary = parent / "temp"
        temporary.mkdir()
        snapshot = parent / "snapshot"
        git(parent, temporary, "clone", "--shared", "--no-checkout", str(REPO), str(snapshot))
        git(snapshot, temporary, "checkout", "--detach", BASE)
        require(git(snapshot, temporary, "rev-parse", "HEAD").decode().strip() == BASE,
                "wrong snapshot commit")
        require(sha((snapshot / "tools/generate_test_inventory.py").read_bytes()) == GENERATOR,
                "snapshot generator is not r010")
        require(sha((snapshot / TEST).read_bytes()) == ORIGINAL, "snapshot test base differs")
        overlay = checked(OVERLAY).read_bytes()
        require(sha(overlay) == OVERLAY_SHA, "wrong immutable cb830-budget generator")
        (snapshot / "tools/generate_test_inventory.py").write_bytes(overlay)
        (snapshot / TEST).write_bytes(candidate.read_bytes())
        require(git(snapshot, temporary, "diff", "--name-only").decode().splitlines() == [TEST, "tools/generate_test_inventory.py"],
                "snapshot overlay changed extra paths")
        names = git(snapshot, temporary, "ls-tree", "-r", "--name-only", BASE).decode().splitlines()
        meta = {
            "base": BASE, "snapshot": str(snapshot), "temporary": str(temporary),
            "released_tests": str(candidate), "tests_sha256": expected,
            "generator_sha256": OVERLAY_SHA, "frozen_r010_generator_sha256": GENERATOR,
            "overlay_source": str(OVERLAY), "source_hashes": hashes(snapshot, names),
            "environment": environment(temporary, snapshot),
            "control_sha256": sha(Path(__file__).read_bytes()),
        }
        out = checks / ("snapshot-" + label + ".json")
        emit(out, meta)
        print(json.dumps({"metadata": str(out), "sha256": sha(out.read_bytes()),
                          "snapshot": str(snapshot)}))
        return 0
    if mode == "run":
        slot, = args
        meta_path = checks / ("snapshot-" + label + ".json")
        meta = json.loads(meta_path.read_text())
        snapshot, temporary = checked(meta["snapshot"], True), checked(meta["temporary"], True)
        require(git(snapshot, temporary, "rev-parse", "HEAD").decode().strip() == BASE,
                "snapshot HEAD changed")
        before = hashes(snapshot, meta["source_hashes"])
        require(before == meta["source_hashes"], "snapshot bytes changed")
        probe = checked(r"D:\Pontius-handoffs\v0a-i01-c-authority\tests-checks\budget-probe-v1.py")
        require(sha(probe.read_bytes()) == "6bd57451ed6ef2568a01f5f660a4a43c18b5111949f1ced82cd90a3b9452e2a6",
                "probe bytes changed")
        exe, version = SLOTS[slot]
        checked(exe)
        command = [exe, "-B", "-P", "-c", WRAPPER, exe, ".".join(map(str, version))]
        result = subprocess.run(command, cwd=snapshot, env=meta["environment"], capture_output=True)
        output = (result.stdout + result.stderr).replace(b"\r\n", b"\n")
        log = checks / ("red-" + label + "-" + slot + ".txt")
        create(log, output)
        require(hashes(snapshot, meta["source_hashes"]) == before, "payload changed source")
        identity = json.loads(result.stdout.splitlines()[0])["identity_before_import"]
        require(identity["version_info"] == list(version), "wrong payload identity")
        summaries = [json.loads(line) for line in result.stdout.splitlines()
                     if line.startswith(b'{"matrix_summary"')]
        receipt = {
            "base": BASE, "slot": slot, "command": command, "environment": meta["environment"],
            "identity": identity, "metadata_sha256": sha(meta_path.read_bytes()),
            "tests_sha256": meta["tests_sha256"], "generator_sha256": meta["generator_sha256"],
            "frozen_r010_generator_sha256": GENERATOR, "focus": "ordinary-corpus-budget", "probe_sha256": sha(probe.read_bytes()),
            "exit": result.returncode, "log": str(log), "log_sha256": sha(output),
            "all_tracked_paths_unchanged": len(before), "matrix_summaries": summaries,
            "control_sha256": sha(Path(__file__).read_bytes()),
        }
        out = checks / ("red-" + label + "-" + slot + "-receipt.json")
        emit(out, receipt)
        print(json.dumps({"receipt": str(out), "exit": result.returncode,
                          "summaries": len(summaries), "log_sha256": sha(output)}))
        return result.returncode
    raise RuntimeError("unknown mode")

if __name__ == "__main__":
    raise SystemExit(main())
