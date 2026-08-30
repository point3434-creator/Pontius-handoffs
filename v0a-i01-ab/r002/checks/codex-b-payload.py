import json
import os
from pathlib import Path
import runpy
import sys
slot, payload = sys.argv[1:]
expected_version, expected_executable = {"311": ((3, 11, 15), r"D:\Pontius-tools\py311\Scripts\python.exe"), "314": ((3, 14, 6), r"D:\Pontius\.venv\Scripts\python.exe")}[slot]
assert sys.version_info[:3] == expected_version, sys.version
assert Path(sys.executable).resolve() == Path(expected_executable).resolve()
snapshot = Path(r"D:\pontius-snapshots\v0a-i01-ab-r002-cold-b-20260830")
assert Path.cwd().resolve() == snapshot.resolve()
assert os.environ["PYTHONPATH"] == str(snapshot / "src")
assert sys.flags.dont_write_bytecode and sys.flags.safe_path
import pontius.v0a.runtime as runtime
import pontius.v0a.replay as replay
import pontius.immutable_blueprint as immutable
for module in (runtime, replay, immutable):
    assert Path(module.__file__).resolve().is_relative_to(snapshot / "src")
assert not any(name == "cupy" or name.startswith("cupy.") or name == "torch" or name.startswith("torch.") for name in sys.modules)
print(json.dumps({"python": sys.version, "executable": sys.executable, "cwd": str(Path.cwd()), "safe_path": sys.flags.safe_path, "dont_write_bytecode": sys.flags.dont_write_bytecode, "modules": {m.__name__: m.__file__ for m in (runtime,replay,immutable)}}), flush=True)
sys.argv = [payload]
runpy.run_path(payload, run_name="__main__")
