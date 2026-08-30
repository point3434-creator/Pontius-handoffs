import sys
import platform
sys.stdout.reconfigure(encoding="utf-8", newline="\n")
sys.stderr.reconfigure(encoding="utf-8", newline="\n")
assert sys.executable == sys.argv[1]
assert platform.python_version() == sys.argv[2]
assert platform.python_implementation() == "CPython"
print("BOOTSTRAP", repr(sys.executable), platform.python_implementation(), platform.python_version(), flush=True)
import os
import json
import unittest
import importlib.util
from pathlib import Path
assert Path.cwd() == Path(r"D:\pontius-snapshots\v0a-r005-cold-b-e6ac13a682804562a53621e8fab883e1\harness")
assert os.environ["PYTHONPATH"] == str(Path.cwd()/"src")
assert os.environ["PONTIUS_GIT"] == r"C:\Program Files\Git\cmd\git.exe"
path=Path.cwd()/"tests/test_v0a_replay.py"
spec=importlib.util.spec_from_file_location("cold_b_focused",path)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
import pontius.v0a.replay as replay
assert Path(replay.__file__) == Path.cwd()/"src/pontius/v0a/replay.py"
print("PAYLOAD_MODULE",replay.__file__,flush=True)
result=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromModule(module))
print("FOCUSED_RESULT",json.dumps({"run":result.testsRun,"failures":len(result.failures),"errors":len(result.errors),"skipped":len(result.skipped)}))
assert result.wasSuccessful()
