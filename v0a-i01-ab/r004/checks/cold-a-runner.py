"""Manifest-bound cold A runner; execute only in the isolated snapshot."""
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import platform
import stat
import subprocess
import sys
import unittest

SNAPSHOT = Path(r"D:\Pontius-review-snapshots\v0a-i01-ab-r004-cold-a")
PACKET = Path(r"D:\Pontius-handoffs\v0a-i01-ab\r004")
COMMIT = "c6adbcaa048988361d2388970eaca772711b797b"
BASE = "30df7bce8da51715e6f1d7576892dd689421c516"
TREE = "1b6edef1e943483e0a83ec33f1bcc61348ada166"
MANIFEST = "a810c89b7342fb1bcb4f1498fdcf53cd11a589b70424c7da48f6619a45da67cb"
expected_version, label = sys.argv[1:3]
receipt_path = PACKET / "checks" / ("cold-a-" + label + "-receipt.json")
assert not receipt_path.exists(), "issued receipt exists"
assert platform.python_implementation() == "CPython"
assert platform.python_version() == expected_version
assert sys.flags.dont_write_bytecode and sys.flags.safe_path
assert Path.cwd().resolve() == SNAPSHOT.resolve()
assert os.environ["PYTHONPATH"] == str(SNAPSHOT / "src")
assert set(os.environ) <= {"SYSTEMROOT", "WINDIR", "TEMP", "TMP", "PYTHONPATH",
                            "PONTIUS_GIT", "PYTHONDONTWRITEBYTECODE", "PYTHONNOUSERSITE"}
git = Path(os.environ["PONTIUS_GIT"])
assert git.is_absolute() and git.is_file()
assert not git.stat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT
identity = dict(executable=sys.executable, implementation=platform.python_implementation(),
                version=sys.version, version_info=list(sys.version_info),
                cwd=str(Path.cwd()), flags=dict(dont_write_bytecode=sys.flags.dont_write_bytecode,
                                                safe_path=sys.flags.safe_path),
                environment=dict(os.environ), command=[sys.executable, "-B", "-P", *sys.argv],
                timestamp_utc=__import__("datetime").datetime.now(
                    __import__("datetime").timezone.utc).isoformat())
print(json.dumps({"identity_before_payload_import": identity}), flush=True)
def gitrun(*args):
    result = subprocess.run([str(git), "-c", "safe.directory=" + str(SNAPSHOT),
                             "-C", str(SNAPSHOT), *args],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return result.stdout
assert gitrun("rev-parse", "HEAD").decode().strip() == COMMIT
assert gitrun("rev-parse", COMMIT + "^").decode().strip() == BASE
assert gitrun("rev-parse", COMMIT + "^{tree}").decode().strip() == TREE
raw = gitrun("diff-tree", "-r", "-z", "--no-renames", "--no-commit-id",
             "--name-status", BASE, COMMIT).decode().split("\0")
rows = []
for index in range(0, len(raw) - 1, 2):
    status, path = raw[index:index+2]
    blob = b"" if status[0] == "D" else gitrun("cat-file", "blob", COMMIT + ":" + path)
    digest = "0" * 64 if status[0] == "D" else hashlib.sha256(blob).hexdigest()
    rows.append(f"{digest}  {path}\n")
    if status[0] != "D":
        assert (SNAPSHOT / path).read_bytes() == blob, ("checkout bytes differ", path)
manifest_bytes = "".join(sorted(rows)).encode()
assert hashlib.sha256(manifest_bytes).hexdigest() == MANIFEST
assert (PACKET / "manifest.sha256").read_bytes() == manifest_bytes
assert len(rows) == 3
status_before = gitrun("status", "--porcelain", "--untracked-files=all").decode()
assert status_before == ""
print(json.dumps({"manifest_verified": MANIFEST, "rows": sorted(rows)}), flush=True)

def load_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

modules = []
for filename in ("test_v0a_hand_replay.py", "test_v0a_contract_faults.py",
                 "test_v0a_replay.py", "test_v0a_trace.py"):
    modules.append(load_file("cold_a_" + filename.removesuffix(".py"),
                             SNAPSHOT / "tests" / filename))
probes = load_file("cold_a_independent_probes", PACKET / "checks" / "cold-a-probes.py")
origins = {}
for name, module in sorted(sys.modules.items()):
    if name == "pontius" or name.startswith("pontius."):
        origin = getattr(module, "__file__", None)
        assert origin and Path(origin).resolve().is_relative_to((SNAPSHOT / "src").resolve()), name
        origins[name] = origin
assert not any(name.startswith(("cupy", "numpy", "torch")) for name in sys.modules)
print(json.dumps({"payload_module_origins": origins}), flush=True)

class RecordedResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.success_ids = []
    def addSuccess(self, test):
        self.success_ids.append(test.id())
        super().addSuccess(test)

def execute(title, selected):
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromModule(m)
                               for m in selected)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2,
                                    resultclass=RecordedResult).run(suite)
    print(title + "\n" + stream.getvalue(), flush=True)
    return dict(title=title, tests=result.testsRun, successful=result.wasSuccessful(),
                failures=[(test.id(), error) for test, error in result.failures],
                errors=[(test.id(), error) for test, error in result.errors],
                skipped=[(test.id(), reason) for test, reason in result.skipped],
                successes=result.success_ids, output=stream.getvalue())

results = [execute("existing focused v0a suites", modules),
           execute("independent real-boundary probes", [probes])]
status_after = gitrun("status", "--porcelain", "--untracked-files=all").decode()
assert status_after == ""
receipt = dict(candidate=COMMIT, base=BASE, tree=TREE, manifest=MANIFEST, identity=identity,
               manifest_rows=sorted(rows), module_origins=origins,
               status_before=status_before, status_after=status_after,
               results=results, observations=probes.OBSERVATIONS,
               probe_sha256=hashlib.sha256((PACKET/"checks"/"cold-a-probes.py").read_bytes()).hexdigest(),
               runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n")
exit_code = 0 if all(result["successful"] for result in results) else 1
print(json.dumps({"receipt": str(receipt_path), "exit": exit_code,
                  "counts": [r["tests"] for r in results]}), flush=True)
sys.exit(exit_code)
