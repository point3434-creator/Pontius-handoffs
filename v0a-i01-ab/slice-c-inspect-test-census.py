"""Read-only census inspection for a finalized disposable combined snapshot.

No generator CLI, publication writer, capability approval, test invocation,
assertion patching, experiment owner, or output-file writer is called here.
JSON is emitted on stdout only. Run after the generated pair is refreshed.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import importlib.util
import json
import os
from pathlib import Path
import platform
import stat
import sys
import tomllib

BASELINE_COMMIT = "a842c4b6a73a2991a63a481f4107580b72750582"
BASELINE_ROOT_TREE = "80feb736d287bb271905b3eb7ee3a878e026cd62"
GIT_PATH = Path("C:/Program Files/Git/cmd/git.exe")
SLOTS = {
    "3.11.15": Path("D:/Pontius-tools/py311/Scripts/python.exe"),
    "3.14.6": Path("D:/Pontius/.venv/Scripts/python.exe"),
}
ALLOWED_ENVIRONMENT = frozenset({
    "SYSTEMROOT", "WINDIR", "COMSPEC", "PATH", "TEMP", "TMP", "PONTIUS_GIT",
    "PYTHONPATH", "GIT_CONFIG_NOSYSTEM", "GIT_CONFIG_GLOBAL",
})


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise RuntimeError(reason)


def digest(raw: bytes) -> str:
    return sha256(raw).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--expected-version", choices=tuple(SLOTS), required=True)
    args = parser.parse_args()
    root = args.snapshot.resolve(strict=True)
    expected = tuple(int(part) for part in args.expected_version.split("."))
    require(os.name == "nt", "this helper requires the declared Windows slots")
    require(platform.python_implementation() == "CPython", "CPython is required")
    require(sys.version_info[:3] == expected, "actual interpreter version differs")
    require(Path(sys.executable).resolve() == SLOTS[args.expected_version].resolve(),
            "actual interpreter executable differs from the declared slot")
    require(sys.flags.dont_write_bytecode and sys.flags.safe_path, "-B -P required")
    require(sys.flags.optimize == 0, "optimized Python is outside this inspection command")
    require(root.drive.casefold() == "d:", "snapshot must be D-local")
    require(root != Path("D:/Pontius").resolve(), "primary checkout is forbidden")
    require((root / ".git").is_dir(), "a disposable clone, not a linked worktree, is required")
    require(Path.cwd().resolve() == root, "cwd must be the snapshot root")
    require(os.environ.get("PYTHONPATH") == str(root / "src"), "snapshot src PYTHONPATH required")
    require(set(os.environ) <= ALLOWED_ENVIRONMENT, "environment is not the declared scrubbed set")
    require(os.environ.get("GIT_CONFIG_NOSYSTEM") == "1", "system Git config must be disabled")
    require(os.environ.get("GIT_CONFIG_GLOBAL", "").casefold() == os.devnull.casefold(),
            "global Git config must be disabled")
    require(os.environ.get("PONTIUS_GIT") == str(GIT_PATH), "absolute declared Git required")
    git_info = GIT_PATH.lstat()
    require(stat.S_ISREG(git_info.st_mode) and not git_info.st_file_attributes & 0x400,
            "Git must be a regular, non-reparse executable")
    for key in ("TEMP", "TMP"):
        temp = Path(os.environ[key]).resolve(strict=True)
        require(temp.is_dir() and temp.drive.casefold() == "d:", "D-local TEMP/TMP required")
    require(os.environ["TEMP"] == os.environ["TMP"], "TEMP and TMP must use one declared root")

    generator_path = root / "tools" / "generate_test_inventory.py"
    before_generator = generator_path.read_bytes()
    spec = importlib.util.spec_from_file_location("slice_c_read_only_census", generator_path)
    require(spec is not None and spec.loader is not None, "exact generator cannot be loaded")
    generator = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = generator
    spec.loader.exec_module(generator)
    require(Path(generator.__file__).resolve() == generator_path, "wrong generator resolved")
    require(generator.BASELINE_COMMIT == BASELINE_COMMIT, "baseline commit changed")
    require(generator.BASELINE_ROOT_TREE_OID == BASELINE_ROOT_TREE, "baseline tree changed")

    bound_inputs = {}
    for relative in (
        "tools/generate_test_inventory.py", "tools/generate_dependency_baseline.py",
        "tests/test-inventory.json", "tests/test-profiles.toml",
    ):
        bound_inputs[relative] = generator.secure_filesystem.read_regular_snapshot(
            root / relative, maximum_bytes=generator.MAXIMUM_SOURCE_BYTES, root=root,
        )
    require(bound_inputs["tools/generate_test_inventory.py"].raw == before_generator,
            "generator changed during exact-path import")
    raw = bound_inputs["tests/test-inventory.json"].raw
    document = json.loads(raw)
    profiles = tomllib.loads(bound_inputs["tests/test-profiles.toml"].raw.decode("utf-8"))
    require(raw == generator.canonical_json_bytes(document) + b"\n",
            "inventory is not canonical LF JSON")
    require(document["baseline_commit"] == BASELINE_COMMIT, "inventory baseline differs")
    entries = tuple(document["entries"])

    # Exactly the test's _working_sources(root) corpus; intentionally false.
    working = generator._capture_working_sources(root, include_support_modules=False)
    sources = working.sources
    discovery = generator.discover_test_sources(sources)
    stable_ids = [row["stable_id"] for row in entries]
    require(len(stable_ids) == len(set(stable_ids)), "duplicate inventory stable IDs")
    require(set(discovery.stable_ids) == set(stable_ids), "source/inventory stable IDs differ")
    profile_by_id = {}
    for row in entries:
        assignment = row.get("assignment")
        require(type(assignment) is dict, "inventory entry has no assignment")
        profile_by_id[str(row["stable_id"])] = str(assignment["profile_name"])
    design_profiles = {"core", "current", "gpu"}
    universe = {
        ("stable_id", stable_id)
        for stable_id, profile in profile_by_id.items() if profile in design_profiles
    }
    for fixture in discovery.lifecycle_fixtures:
        member_profiles = {profile_by_id[member] for member in fixture.member_ids}
        if member_profiles <= design_profiles:
            universe.add(("fixture", fixture.fixture_id))
        else:
            require(member_profiles == {"historical"}, "mixed lifecycle fixture ownership")
    historical_probe_ids = set()
    for payload in profiles["payload"]:
        probe_ids = {str(probe) for probe in payload["probe_ids"]}
        if payload["profile_name"] in design_profiles:
            universe.update(("probe", probe) for probe in probe_ids)
        else:
            historical_probe_ids.update(probe_ids)
    universe = tuple(sorted(universe))
    review = generator.derive_design_review(
        baseline_commit=BASELINE_COMMIT,
        baseline_root_tree_oid=BASELINE_ROOT_TREE,
        inventory_document=document,
        inventory_document_bytes=raw,
        sources=sources,
        item_universe=universe,
    )
    blockers = review["unresolved_dynamic_blockers"]
    require(blockers == sorted(blockers, key=lambda row: (
        row["item_id"], row["relative_path"], row["line"],
    )), "blocker production ordering changed")
    locations = {}
    for row in blockers:
        locations.setdefault(row["reason"], []).append([row["relative_path"], row["line"]])
    working.revalidate()
    for snapshot in bound_inputs.values():
        snapshot.revalidate()
    result = {
        "schema_version": "slice-c-read-only-test-census-v1",
        "standing": "inspection only; not generation, capability approval, or acceptance",
        "matched_test": (
            "CheckedInInventoryTests.test_working_discovery_binds_every_entry_and_introduced_id"
        ),
        "execution": {
            "executable": sys.executable, "implementation": platform.python_implementation(),
            "version": sys.version, "version_tuple": list(sys.version_info[:3]),
            "cwd": str(root), "pythonpath": os.environ["PYTHONPATH"],
            "git": str(GIT_PATH), "temp": os.environ["TEMP"], "sys_path": sys.path,
            "dont_write_bytecode": sys.flags.dont_write_bytecode,
            "safe_path": sys.flags.safe_path, "environment_keys": sorted(os.environ),
        },
        "input_sha256": {path: digest(snapshot.raw) for path, snapshot in bound_inputs.items()},
        "helper_sha256": digest(Path(__file__).read_bytes()),
        "source_corpus": {
            "include_support_modules": False,
            "source_count": len(sources),
            "reason": "matches _working_sources used by the named checked-in test",
            "raw_sha256": {path: digest(value) for path, value in sorted(sources.items())},
            "canonical_lf_rows": review["receipt"]["derivation_sources"],
        },
        "generated_discovery": document["discovery"],
        "parsed_stable_id_count": len(discovery.stable_ids),
        "item_universe": [list(item) for item in universe],
        "item_universe_counts": dict(sorted(Counter(kind for kind, _ in universe).items())),
        "excluded_historical_probe_ids": sorted(historical_probe_ids),
        "analysis_census": review["analysis_census"],
        "expanded_row_count": len(review["receipt"]["expanded_rows"]),
        "deny_all_count": len(review["receipt"]["deny_all"]),
        "blocker_count": len(blockers),
        "blocker_reason_counts": dict(sorted(Counter(row["reason"] for row in blockers).items())),
        "blocker_locations_by_reason": locations,
        "review": review,
        "inputs_revalidated_after_derivation": True,
        "writes_to_snapshot": False,
    }
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"census inspection refused: {type(error).__name__}: {error}", file=sys.stderr)
        raise SystemExit(2) from error
