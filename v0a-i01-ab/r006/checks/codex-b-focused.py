import importlib.util
import json
from pathlib import Path
import runpy
import unittest

runpy.run_path(str(Path(__file__).with_name('codex-b-identity.py')))
snapshot = Path.cwd()
def module(name, relative):
    spec = importlib.util.spec_from_file_location(name, snapshot / relative)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result
trace_tests = module('review_b_trace_tests', 'tests/test_v0a_trace.py')
hand_tests = module('review_b_hand_tests', 'tests/test_v0a_hand_replay.py')
suites = [
    ('tests/test_v0a_trace.py', unittest.defaultTestLoader.loadTestsFromModule(trace_tests)),
    ('tests/test_v0a_hand_replay.py::EventValueContractTests',
     unittest.defaultTestLoader.loadTestsFromTestCase(hand_tests.EventValueContractTests)),
]
ok = True
for name, suite in suites:
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps({'suite':name,'tests_run':result.testsRun,'failures':len(result.failures),
                      'errors':len(result.errors),'skipped':len(result.skipped)}))
    ok &= result.wasSuccessful()
raise SystemExit(0 if ok else 1)
