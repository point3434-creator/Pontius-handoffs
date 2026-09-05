"""Independent runtime census of the 14 controlled-reuse schedules."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


target = Path("tests/test_inventory_and_profiles.py").resolve()
spec = importlib.util.spec_from_file_location("review_a_inventory_tests", target)
if spec is None or spec.loader is None:
    raise AssertionError("test module could not be loaded")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

case = module.AtomicAndGitBoundaryTests(
    "test_windows_persistent_close_failures_are_truthful_and_retryable"
)
case.setUp()
observed: list[dict[str, object]] = []
expected = (
    ("_final3_windows_writer_reused_handles_are_role_isolated", 5),
    ("_round7_windows_file_owners_bind_before_caller_failure", 6),
    ("_round9_windows_disposition_absence_beats_same_inode_reuse", 3),
)

with module._ControlledWindowsHandles(case.generator.secure_filesystem) as routing:
    original_reuse = routing.reuse
    original_survived = routing.assert_replacement_survived
    pending: list[tuple[int, int]] = []

    def record_reuse(retired: int, replacement: int) -> int:
        token = original_reuse(retired, replacement)
        native, identity = routing.replacements[token]
        pending.append((token, native))
        observed.append(
            {
                "event": "reuse",
                "token": token,
                "native": native,
                "identity_size": len(identity[1]),
            }
        )
        return token

    def record_survival(token: int) -> None:
        original_survived(token)
        native, _ = routing.replacements[token]
        if not routing.native_is_open(native):
            raise AssertionError("raw native liveness changed after the survival assertion")
        observed.append({"event": "survived", "token": token, "native": native})
        pending.remove((token, native))

    routing.reuse = record_reuse
    routing.assert_replacement_survived = record_survival
    family_counts: dict[str, int] = {}
    for helper, count in expected:
        before = len([row for row in observed if row["event"] == "survived"])
        getattr(case, helper)(routing)
        after = len([row for row in observed if row["event"] == "survived"])
        family_counts[helper] = after - before
        if family_counts[helper] != count:
            raise AssertionError(
                f"{helper} exercised {family_counts[helper]} schedules, expected {count}"
            )
    if pending:
        raise AssertionError(f"reuse events lacked raw survival assertions: {pending!r}")

reuse_count = len([row for row in observed if row["event"] == "reuse"])
survival_count = len([row for row in observed if row["event"] == "survived"])
if (reuse_count, survival_count) != (14, 14):
    raise AssertionError(f"unexpected schedule totals: {(reuse_count, survival_count)!r}")
print(json.dumps({"family_counts": family_counts, "events": observed}, sort_keys=True))
