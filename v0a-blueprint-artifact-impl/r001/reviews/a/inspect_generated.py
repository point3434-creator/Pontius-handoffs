from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tomllib


REPOSITORY = Path(r"D:\Pontius\tmp\v0a-blueprint-artifact-impl-r001\authoring")
PACKET_FILES = Path(r"D:\Pontius\tmp\v0a-blueprint-artifact-impl-r001\packets\r001\files")
BASE = "c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98"


def base_blob(path: str) -> bytes:
    return subprocess.run(
        [r"C:\Program Files\Git\cmd\git.exe", "-C", str(REPOSITORY), "cat-file", "blob", f"{BASE}:{path}"],
        check=True,
        capture_output=True,
    ).stdout


base_inventory = json.loads(base_blob("tests/test-inventory.json"))
new_inventory = json.loads((PACKET_FILES / "tests" / "test-inventory.json").read_bytes())
base_entries = {row["stable_id"]: row for row in base_inventory["entries"]}
new_entries = {row["stable_id"]: row for row in new_inventory["entries"]}
added_entries = sorted(set(new_entries) - set(base_entries))
assert not (set(base_entries) - set(new_entries))
assert all(new_entries[key] == value for key, value in base_entries.items())
assert len(base_entries) == 2828 and len(new_entries) == 2851 and len(added_entries) == 23
expected_counts = {
    "tests/test_blueprint_artifact.py": 7,
    "tests/test_blueprint_artifact_boundary.py": 4,
    "tests/test_v0a_rehearsal_driver.py": 12,
}
actual_counts = {
    path: sum(key.startswith(path + "::") for key in added_entries)
    for path in expected_counts
}
assert actual_counts == expected_counts

base_profiles = tomllib.loads(base_blob("tests/test-profiles.toml").decode("utf-8"))
new_profiles = tomllib.loads(
    (PACKET_FILES / "tests" / "test-profiles.toml").read_text(encoding="utf-8")
)
base_payloads = {row["payload_id"]: row for row in base_profiles["payload"]}
new_payloads = {row["payload_id"]: row for row in new_profiles["payload"]}
assert not (set(base_payloads) - set(new_payloads))
assert all(new_payloads[key] == value for key, value in base_payloads.items())
added_payloads = sorted(set(new_payloads) - set(base_payloads))
assert len(base_payloads) == 422 and len(new_payloads) == 425 and len(added_payloads) == 3
added_paths = sorted(set(new_profiles["stabilization_test_files"]) - set(base_profiles["stabilization_test_files"]))
assert added_paths == sorted(expected_counts)
assert new_profiles["capability_bindings_sha256"] == "0" * 64
for payload_id in added_payloads:
    payload = new_payloads[payload_id]
    assert payload["probe_ids"] == []
    assert payload["environment_additions"] == {}

print("generated structure PASS")
print(f"inventory entries {len(base_entries)} -> {len(new_entries)}; added={actual_counts}")
print(f"payloads {len(base_payloads)} -> {len(new_payloads)}; added_ids={added_payloads}")
print(f"stabilization paths added={added_paths}")
print(f"capability_bindings_sha256={new_profiles['capability_bindings_sha256']}")
