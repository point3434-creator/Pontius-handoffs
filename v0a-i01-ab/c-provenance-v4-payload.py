from pathlib import Path
import ast
import hashlib
import json
import os
import sys

root = Path.cwd().resolve()
expected_version, expected_executable, selection = sys.argv[1:]
assert sys.version.split()[0] == expected_version
assert Path(sys.executable).resolve() == Path(expected_executable).resolve()
assert sys.implementation.name == 'cpython'
assert sys.flags.safe_path and sys.dont_write_bytecode
assert os.environ['PYTHONPATH'] == str(root / 'src')
assert Path(os.environ['TEMP']).resolve().drive == 'D:'
assert os.environ['PONTIUS_GIT'] == r'C:\Program Files\Git\cmd\git.exe'
print(json.dumps({'identity_before_import': {'version': sys.version,
    'implementation': sys.implementation.name, 'executable': sys.executable,
    'cwd': str(root), 'safe_path': sys.flags.safe_path,
    'dont_write_bytecode': sys.dont_write_bytecode}}), flush=True)
source = root / 'tests/test_inventory_and_profiles.py'
cls = next(node for node in ast.parse(source.read_text(encoding='utf-8')).body
           if isinstance(node, ast.ClassDef) and node.name == 'DesignReviewTests')
names = [node.name for node in cls.body
         if isinstance(node, ast.FunctionDef) and node.name.startswith('test_')]
assert len(names) == len(set(names))
if selection == 'new':
    names = [name for name in names if name.startswith('test_callable_authority_')]
else:
    assert selection == 'all'
print(json.dumps({'selected_methods': names, 'method_count': len(names)}), flush=True)
import importlib.util
import unittest
spec = importlib.util.spec_from_file_location('v4_inventory_tests', source)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
assert Path(module.__file__).resolve() == source
assert module.GENERATOR_PATH.resolve() == root / 'tools/generate_test_inventory.py'
suite = unittest.TestSuite(module.DesignReviewTests(name) for name in names)
result = unittest.TextTestRunner(verbosity=2).run(suite)
print(json.dumps({'tests_run': result.testsRun, 'failures': len(result.failures),
                  'errors': len(result.errors), 'skipped': len(result.skipped)}), flush=True)
raise SystemExit(not result.wasSuccessful())