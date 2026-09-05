from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import tomllib


ROOT = Path(__file__).resolve().parents[4]
PACKET = ROOT / "packets" / "r002"
REPO = ROOT / "authoring"
GIT = Path(r"C:\Program Files\Git\cmd\git.exe")
CANDIDATE = "5e56e4454f7b8ccb360d3e36245abc33318349bb"
BASE = "c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98"
REJECTED = "6fb7f840d31d946e6b5dcb45faf82939dafd46ec"
TREE = "dc18ed133504fe6c7677b494bcefba311cc73704"
MANIFEST = "6d5e14a64466f8aaa874d4bdf62ada439703eb74911a7b4dc4445c14b2af13b5"


def git(*arguments: str) -> bytes:
    return subprocess.run(
        [str(GIT), "-c", f"safe.directory={REPO.as_posix()}", "-C", str(REPO), *arguments],
        check=True,
        capture_output=True,
    ).stdout


def blob(revision: str, path: str) -> bytes:
    return git("cat-file", "blob", f"{revision}:{path}")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def changed_paths(old: str, new: str) -> tuple[str, ...]:
    raw = git("diff", "--name-only", "--no-renames", "-z", old, new)
    return tuple(item.decode("utf-8") for item in raw.split(b"\0") if item)


def main() -> None:
    expected_paths = (
        ".github/workflows/ci.yml",
        "src/pontius/blueprint_artifact/__init__.py",
        "src/pontius/blueprint_artifact/codec.py",
        "tests/fixtures/blueprint_artifact/history_control.json",
        "tests/fixtures/blueprint_artifact/raise_control.json",
        "tests/test-inventory.json",
        "tests/test-profiles.toml",
        "tests/test_blueprint_artifact.py",
        "tests/test_blueprint_artifact_boundary.py",
        "tests/test_inventory_and_profiles.py",
        "tools/check_stabilization_boundaries.py",
        "tools/generate_test_inventory.py",
    )
    assert git("rev-parse", "refs/heads/review/v0a-blueprint-artifact-impl/r002").decode().strip() == CANDIDATE
    assert git("rev-parse", f"{CANDIDATE}^").decode().strip() == BASE
    assert git("rev-parse", f"{CANDIDATE}^{{tree}}").decode().strip() == TREE
    assert changed_paths(BASE, CANDIDATE) == expected_paths
    assert changed_paths(REJECTED, CANDIDATE) == (
        "src/pontius/blueprint_artifact/codec.py",
        "tests/test_blueprint_artifact.py",
        "tests/test_blueprint_artifact_boundary.py",
        "tools/check_stabilization_boundaries.py",
    )

    rows = []
    for path in expected_paths:
        raw = blob(CANDIDATE, path)
        rows.append(f"{sha256(raw)}  {path}\n")
        assert (PACKET / "files" / Path(path)).read_bytes() == raw
    manifest_bytes = "".join(sorted(rows)).encode("utf-8")
    assert manifest_bytes == (PACKET / "manifest.sha256").read_bytes()
    assert sha256(manifest_bytes) == MANIFEST
    candidate_record = json.loads((PACKET / "candidate.json").read_bytes())
    assert candidate_record == {
        "schema_version": "pontius-handoff-candidate-v1",
        "task_id": "v0a-blueprint-artifact-impl",
        "round": "r002",
        "ref": "refs/heads/review/v0a-blueprint-artifact-impl/r002",
        "commit": CANDIDATE,
        "base": BASE,
        "tree": TREE,
        "manifest_sha256": MANIFEST,
        "date": "2026-09-05",
    }

    pins = {
        "tools/check_stabilization_boundaries.py": "c3f739f001fd70d5326bc7ec4609f483e1ba5525",
        "tools/generate_test_inventory.py": "da0fb1efd0f38747ad90f91aea572789ace7e0aa",
        "tests/test_inventory_and_profiles.py": "45c65de9cde1506db8ad900d624ec69fce5b9893",
        "tests/test-inventory.json": "d655d205053c13da2634e8a22b36c58b72ee340b",
        "tests/test-profiles.toml": "ada2c73eb0834fe9822b84e5d31b2ffdfb78b4a6",
        ".github/workflows/ci.yml": "0585dcd6191dbe97b4f00f3866cc5da9798b4c51",
    }
    for path, oid in pins.items():
        assert git("rev-parse", f"{BASE}:{path}").decode().strip() == oid
    authorizations = {
        "driver-amendment-authorization.md": "0d5cd53eb456a47a0ff346034fdfad173c77a39e37b030c99205c4913eeb2af7",
        "inventory-amendment-authorization.md": "666d89a6708c9d749265d816d063857432be42d754b6e76ad2dbafff6ba98ea3",
    }
    for name, digest in authorizations.items():
        assert sha256((PACKET / "inputs" / name).read_bytes()) == digest

    init_raw = blob(CANDIDATE, "src/pontius/blueprint_artifact/__init__.py")
    codec_raw = blob(CANDIDATE, "src/pontius/blueprint_artifact/codec.py")
    test_raw = blob(CANDIDATE, "tests/test_blueprint_artifact.py")
    boundary_raw = blob(CANDIDATE, "tests/test_blueprint_artifact_boundary.py")
    fixture_bytes = sum(len(blob(CANDIDATE, path)) for path in expected_paths if "/fixtures/" in path)
    assert len(init_raw.splitlines()) + len(codec_raw.splitlines()) == 290
    assert len(test_raw.splitlines()) + len(boundary_raw.splitlines()) == 300
    assert fixture_bytes == 1699
    for path in expected_paths:
        raw = blob(CANDIDATE, path)
        assert not raw.startswith(b"\xef\xbb\xbf")
        assert b"\r" not in raw
        assert all(line.rstrip(b" \t") == line for line in raw.splitlines())
    python_paths = [path for path in expected_paths if path.endswith(".py")]
    patch = git("diff", "--no-prefix", "--unified=0", BASE, CANDIDATE, "--", *python_paths)
    added_lines = [line[1:] for line in patch.splitlines()
                   if line.startswith(b"+") and not line.startswith(b"+++")]
    assert max(map(len, added_lines)) == 99

    numstat = git("diff", "--numstat", BASE, CANDIDATE).decode().splitlines()
    counts = {path: (int(added), int(removed)) for added, removed, path in
              (row.split("\t") for row in numstat)}
    manual = (
        ".github/workflows/ci.yml",
        "tests/test_inventory_and_profiles.py",
        "tools/check_stabilization_boundaries.py",
        "tools/generate_test_inventory.py",
    )
    assert sum(sum(counts[path]) for path in manual) == 97

    old_inventory = json.loads(blob(BASE, "tests/test-inventory.json"))
    new_inventory = json.loads(blob(CANDIDATE, "tests/test-inventory.json"))
    old_entries = {entry["stable_id"]: entry for entry in old_inventory["entries"]}
    new_entries = {entry["stable_id"]: entry for entry in new_inventory["entries"]}
    assert len(old_entries) == 2828 and len(new_entries) == 2851
    assert all(new_entries[key] == value for key, value in old_entries.items())
    added_entries = [entry for key, entry in new_entries.items() if key not in old_entries]
    assert len(added_entries) == 23
    by_path = {}
    for entry in added_entries:
        by_path[entry["relative_path"]] = by_path.get(entry["relative_path"], 0) + 1
        assert entry["assignment"] == {
            "expectation": {"kind": "pass"},
            "payload_id": "current:" + Path(entry["relative_path"]).stem,
            "profile_name": "current",
        }
    assert by_path == {
        "tests/test_blueprint_artifact.py": 7,
        "tests/test_blueprint_artifact_boundary.py": 4,
        "tests/test_v0a_rehearsal_driver.py": 12,
    }

    old_profiles = tomllib.loads(blob(BASE, "tests/test-profiles.toml").decode())
    new_profiles = tomllib.loads(blob(CANDIDATE, "tests/test-profiles.toml").decode())
    assert new_profiles["spec_capabilities_sha256"] == "0" * 64
    assert new_profiles["capability_bindings_sha256"] == "0" * 64
    old_payloads = {item["payload_id"]: item for item in old_profiles["payload"]}
    new_payloads = {item["payload_id"]: item for item in new_profiles["payload"]}
    assert all(new_payloads[key] == value for key, value in old_payloads.items())
    added_payload_ids = set(new_payloads) - set(old_payloads)
    assert added_payload_ids == {
        "current:test_blueprint_artifact",
        "current:test_blueprint_artifact_boundary",
        "current:test_v0a_rehearsal_driver",
    }
    for key in added_payload_ids:
        assert new_payloads[key] == {
            "payload_id": key,
            "profile_name": "current",
            "target_kind": "current_snapshot",
            "allowed_interpreter_slots": ["cpython311", "development"],
            "probe_ids": [],
            "environment_additions": {},
            "environment_removals": ["PYTHONHOME", "PYTHONPATH", "PYTHONSTARTUP"],
            "allowed_write_roots": ["temporary"],
            "forbidden_relative_paths": ["artifacts/work_preflight"],
            "serialized": False,
        }
    print("IDENTITY PASS", CANDIDATE, MANIFEST)
    print("SCOPE PASS", len(expected_paths), "candidate paths; 4 FIX paths")
    print("BOUNDS PASS", "source=290 tests=300 fixtures=1699 manual=97 width=99")
    print("REGISTRATION PASS", by_path, sorted(added_payload_ids), "zero grants")


if __name__ == "__main__":
    main()
