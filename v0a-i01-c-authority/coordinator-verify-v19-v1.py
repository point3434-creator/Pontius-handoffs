"""Verify retained focused evidence and preservation; do not run repository code."""
from pathlib import Path
import hashlib
import json
import sys

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
W = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1")
sha = lambda raw: hashlib.sha256(raw).hexdigest()
assert sys.version_info[:3] == (3, 11, 15)
assert Path(sys.executable).resolve() == Path(r"D:\Pontius-tools\py311\Scripts\python.exe").resolve()
assert sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path and sys.dont_write_bytecode
summary_raw = (T / "engineer-checks/release19-focused-evidence.json").read_bytes()
assert sha(summary_raw) == "a4d41468b3d021d0ea4f0746d832f1c99475a7763eee15e7a7eb9ed58eab5ace"
summary = json.loads(summary_raw)
verified = []
for entry in summary["entries"]:
    receipt_raw = Path(entry["receipt"]).read_bytes()
    assert sha(receipt_raw) == entry["receipt_sha256"]
    receipt = json.loads(receipt_raw)
    assert receipt["exit"] == entry["exit"] == 0
    log = Path(receipt["log"]).read_bytes()
    assert sha(log) == entry["log_sha256"]
    expected = f"Ran {entry['test_methods']} tests".encode()
    assert expected in log and b"\nOK" in log
    verified.append({"label": entry["label"], "receipt_sha256": sha(receipt_raw),
                     "log_sha256": sha(log), "test_methods": entry["test_methods"]})
baseline_raw = (T / "coordinator-preservation-baseline-v2.json").read_bytes()
assert sha(baseline_raw) == "a2f848258a6f7622161e92962b594568400bc4582bb32461aedd3c41a85d768e"
baseline = json.loads(baseline_raw)
scope = {"tools/generate_test_inventory.py", "tests/test_inventory_and_profiles.py",
         "tests/test-inventory.json", "tests/test-profiles.toml"}
preserved = {name: pin for name, pin in baseline["paths"].items() if name not in scope}
assert len(preserved) == 13
for name, pin in preserved.items():
    assert sha((W / name).read_bytes()) == pin, name
for name in ("tests/test-inventory.json", "tests/test-profiles.toml"):
    assert sha((W / name).read_bytes()) == baseline["paths"][name]
assert sha((W / "tools/generate_test_inventory.py").read_bytes()) == summary["source_sha256"]
assert sha((W / "tests/test_inventory_and_profiles.py").read_bytes()) == "06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd"
report = {"standing": "Independent evidence/hash inspection, not corpus or cold approval.",
          "generator_sha256": summary["source_sha256"], "verified_focused_runs": verified,
          "preserved_paths": preserved, "generated_pair_unchanged_from_r010": True}
out = T / "coordinator-v19-preservation-v1.json"
with out.open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(report, stream, indent=2)
    stream.write("\n")
print(json.dumps({"receipt": str(out), "sha256": sha(out.read_bytes()),
                  "verified_runs": len(verified), "preserved_paths": len(preserved)}))
