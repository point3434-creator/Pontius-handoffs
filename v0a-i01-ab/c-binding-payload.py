from pathlib import Path
import importlib.util
import json
import os
import sys
import unittest

root = Path.cwd().resolve()
expected_version, expected_executable = sys.argv[1:3]
assert sys.version.split()[0] == expected_version, sys.version
assert Path(sys.executable).resolve() == Path(expected_executable).resolve()
assert sys.flags.safe_path and sys.dont_write_bytecode
assert os.environ["PYTHONPATH"] == str(root / "src")
assert Path(os.environ["TEMP"]).resolve().drive == "D:"
assert Path(os.environ["PONTIUS_GIT"]).resolve() == Path(
    r"C:\Program Files\Git\cmd\git.exe"
).resolve()
path = root / "tests" / "test_inventory_and_profiles.py"
spec = importlib.util.spec_from_file_location("binding_inventory_tests", path)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
assert Path(module.__file__).resolve() == path
assert module.GENERATOR_PATH.resolve() == root / "tools" / "generate_test_inventory.py"
generator = module._load_generator()
assert Path(generator.__file__).resolve() == module.GENERATOR_PATH.resolve()
print(json.dumps({"identity_before_test_payload": {
    "version": sys.version, "executable": sys.executable,
    "cwd": str(root), "test_origin": module.__file__,
    "generator_origin": generator.__file__, "safe_path": sys.flags.safe_path,
    "dont_write_bytecode": sys.dont_write_bytecode,
}}), flush=True)
selected = sys.argv[3:]
suite = unittest.TestSuite(
    unittest.defaultTestLoader.loadTestsFromName(name, module) for name in selected
)
result = unittest.TextTestRunner(verbosity=2).run(suite)
print(json.dumps({"tests_run": result.testsRun, "failures": len(result.failures),
                  "errors": len(result.errors), "skipped": len(result.skipped)}), flush=True)
raise SystemExit(not result.wasSuccessful())
