import sys, os, platform, json, hashlib, subprocess, pathlib, importlib, importlib.util, unittest
snapshot = pathlib.Path(sys.argv[1]).resolve()
expected_version = sys.argv[2]
mode = sys.argv[3]
expected_executable = pathlib.Path(sys.argv[4]).resolve()
assert pathlib.Path(sys.executable).resolve() == expected_executable
assert platform.python_implementation() == "CPython"
assert platform.python_version() == expected_version
assert sys.flags.dont_write_bytecode and sys.flags.safe_path
assert pathlib.Path.cwd().resolve() == snapshot
assert os.environ["PYTHONPATH"] == str(snapshot / "src")
assert os.environ["TEMP"] == os.environ["TMP"] == str(snapshot / "codex-a-temp")
assert os.environ["PONTIUS_GIT"] == r"C:\Program Files\Git\cmd\git.exe"
assert "PATH" not in os.environ and "PYTHONHOME" not in os.environ
print(json.dumps({"executable": sys.executable, "version": sys.version,
    "implementation": platform.python_implementation(), "cwd": str(snapshot),
    "flags": {"B": sys.flags.dont_write_bytecode, "P": sys.flags.safe_path},
    "environment": dict(os.environ)}, sort_keys=True), flush=True)
packet = pathlib.Path(r"D:\Pontius-handoffs\v0a-i01-ab\r007")
commit = "ddea6efbeb55cb8b71da1ebd5a359a0c2c901cf1"
def git(*args):
    return subprocess.run([os.environ["PONTIUS_GIT"], "-C", str(snapshot), *args],
        capture_output=True, check=True).stdout
assert git("rev-parse", "HEAD").decode().strip() == commit
fields = git("diff-tree", "-r", "-z", "--no-renames", "--no-commit-id",
    "--name-status", commit + "^", commit).decode().split("\0")
rows = []
for i in range(0, len(fields)-1, 2):
    status, path = fields[i:i+2]
    blob = b"" if status == "D" else git("cat-file", "blob", commit + ":" + path)
    digest = "0" * 64 if status == "D" else hashlib.sha256(blob).hexdigest()
    rows.append(f"{digest}  {path}\n")
    if status != "D":
        assert (snapshot/path).read_bytes() == blob, path
        assert not blob.startswith(b"\xef\xbb\xbf") and b"\r" not in blob, path
manifest = "".join(sorted(rows)).encode()
assert manifest == (packet/"manifest.sha256").read_bytes()
assert hashlib.sha256(manifest).hexdigest() == "c234b4271bd665e869689fb5d976e629703b678faeb3f55532a3615edc98b189"
assert hashlib.sha256((packet/"acceptance-r2-04-09-10.md").read_bytes()).hexdigest() == "01a3c00fa24ba4b44e68ffd711095b1c222249dfd468af7b57343a98595068ad"
print("BLOB_MANIFEST_VERIFIED " + hashlib.sha256(manifest).hexdigest(), flush=True)
origins = {}
for name in ("pontius", "pontius.v0a.runtime", "pontius.v0a.replay", "pontius.v0a.trace", "pontius.v0a.clock"):
    module = importlib.import_module(name)
    origin = pathlib.Path(module.__file__).resolve()
    assert origin.is_relative_to(snapshot/"src")
    origins[name] = str(origin)
print("ORIGINS " + json.dumps(origins, sort_keys=True), flush=True)
if mode == "identity":
    raise SystemExit(0)
if mode == "focused":
    suite = unittest.TestSuite()
    for name in ("test_v0a_replay", "test_v0a_trace"):
        spec = importlib.util.spec_from_file_location(name, snapshot/"tests"/(name + ".py"))
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    print(json.dumps({"tests": result.testsRun, "failures": len(result.failures),
        "errors": len(result.errors), "skipped": result.skipped}), flush=True)
    raise SystemExit(0 if result.wasSuccessful() else 1)
if mode == "adversarial":
    spec = importlib.util.spec_from_file_location("codex_a_adversarial", packet/"checks"/"codex-a-adversarial-v6.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.main()
else:
    raise AssertionError(mode)
