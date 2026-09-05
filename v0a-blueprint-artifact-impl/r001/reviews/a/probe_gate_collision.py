from __future__ import annotations

import importlib.util
from pathlib import Path


root = Path.cwd()
checker_path = root / "tools" / "check_stabilization_boundaries.py"
spec = importlib.util.spec_from_file_location("review_a_checker", checker_path)
assert spec is not None and spec.loader is not None
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

target = root / "src" / "pontius" / "blueprint_artifact.py"
assert not target.exists(), target
try:
    target.write_bytes(b'"""Undeclared colliding module probe."""\n')
    checker.check_repository(root)
finally:
    target.unlink()
print("DEFECT REPRODUCED: public gate accepted undeclared src/pontius/blueprint_artifact.py")
