"""Create pinned, reviewed prototype inputs; no payload execution."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

T = Path(r"D:\Pontius-handoffs\v0a-i01-c-authority")
W = Path(r"D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1\tools\generate_test_inventory.py")
PINS = {
    "engineer-name-cursor-prototype-v1.py": "67acb279510924311266b985e15e95e53ae9d0a11d64a50d108f254a690deb2a",
    "engineer-storage-control-v3.py": "882016384c6b9bc4e6a4d9d81e829dee9eb95120942650f63006fea8f0ad1cbf",
    "tests-checks/storage-oracle-v2.py": "6a58ef82832d53510f7d44d58cf5a8fa3764f8be5f2c28dcb7e555a83c72cfba",
    "tests-checks/storage-oracle-cases-v2.json": "3bd5678da334fb551c2f179906e8b4d2cf7a0b0e7a3779e0fad2fb4b4a9c548f",
    "tests-checks/cursor-oracle-v1.py": "15a4741e2532a755fd45f01d4d999dd5d293846b8ae4e9d4e7abedf84c0a8d1e",
    "tests-checks/cursor-oracle-cases-v1.json": "ecddd020ffb2a0d85e624aeb7fb544f631b302839f9a5f3542c998b36c37ac61",
    "tests-checks/cursor-oracle-spec-v1.md": "29c0238aa24e0c6d4a9f3834d6f94b46c4bd6ed29f263f0c57511e1ee1b0bfd1",
    "tests-checks/cursor-oracle-release-v1.md": "e95e4a155e6e843c2f99ee66e5fbc4201c3a2624b790b00837fec2ce5628e943",
    "coordinator-name-cursor-prototype-disposition-v1.md": "973191b8b26c71132185d42203a720bdc5b28d4fd23fc1bc4b9c9ec4da46a7b7",
}


def h(raw):
    return hashlib.sha256(raw).hexdigest()


def checked(path):
    assert path.is_absolute() and ".." not in path.parts
    for ancestor in (path, *path.parents):
        info = ancestor.lstat()
        assert not getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
    assert path.is_file()
    return path


def create(path, raw):
    assert path.parent.resolve() == T.resolve()
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def main():
    assert sys.version_info[:3] == (3, 11, 15)
    assert sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path and sys.dont_write_bytecode
    assert h(checked(W).read_bytes()) == "e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679"
    parsed = []
    for relative, expected in PINS.items():
        raw = checked(T / relative).read_bytes()
        assert h(raw) == expected, relative
        if relative.endswith(".py"):
            ast.parse(raw, filename=relative)
            parsed.append(relative)
    cases = json.loads((T / "tests-checks/cursor-oracle-cases-v1.json").read_bytes())
    assert cases["planned_cases"] == 16 and cases["planned_runs"] == 28
    config = {
        "schema": "owned-name-cursor-control-v3",
        "control_sha256": PINS["engineer-storage-control-v3.py"],
        "disposition_sha256": PINS["coordinator-name-cursor-prototype-disposition-v1.md"],
        "cursor_expected": {"planned_cases": 16, "planned_runs": 28},
    }
    for key, path in {
        "prototype": "engineer-name-cursor-prototype-v1.py",
        "old_oracle": "tests-checks/storage-oracle-v2.py",
        "old_cases": "tests-checks/storage-oracle-cases-v2.json",
        "cursor_oracle": "tests-checks/cursor-oracle-v1.py",
        "cursor_cases": "tests-checks/cursor-oracle-cases-v1.json",
    }.items():
        config[key] = {"path": path, "sha256": PINS[path]}
    config_raw = (json.dumps(config, indent=2, sort_keys=True) + "\n").encode()
    report = {
        "kind": "coordinator-engineering-source-review",
        "pins": PINS,
        "syntax_only_parsed": parsed,
        "config_sha256": h(config_raw),
        "source_read_in_full": ["engineer-name-cursor-prototype-v1.py",
                                "tests-checks/cursor-oracle-v1.py",
                                "engineer-storage-control-v3.py"],
        "review": [
            "Private tail ownership moves only after whole publication charges succeed.",
            "History and key-order recipes retain names and parent metadata, not data snapshots or values.",
            "Order/item memo commits follow all public-operation charges; writes invalidate content memo.",
            "Newest-effective pending entries, tombstones, immutable input validation and legacy union order are explicit.",
            "Oracle expects ordinary dictionary semantics independently and preserves original 28/34 pack.",
            "Fault cases retry the same object without refunds and compare both operation and continuation costs.",
            "Fresh snapshots, scrubbed environment, real interpreter identity and before/after manifests gate results.",
        ],
        "limits": [
            "No production fit, complete cost proof, authority-transfer correctness or cold approval is claimed.",
            "Run floor seed0 first; a mechanism failure stops further runtime/seed expansion.",
            "W remains exact rejected v20; no production write lease is opened.",
        ],
        "payload_executed_by_this_control": False,
    }
    outputs = {
        "engineer-cursor-prototype-v1-config.json": config_raw,
        "coordinator-cursor-prototype-v1-source-review.json":
            (json.dumps(report, indent=2, sort_keys=True) + "\n").encode(),
        "coordinator-release-cursor-prototype-v1.py": Path(__file__).read_bytes(),
    }
    assert not any((T / name).exists() for name in outputs)
    for name, raw in outputs.items():
        create(T / name, raw)
    print(json.dumps({name: h(raw) for name, raw in outputs.items()}, indent=2))


if __name__ == "__main__":
    main()
