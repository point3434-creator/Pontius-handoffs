"""Mutate each governed ambiguous-close occurrence and require a raw-oracle failure."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from unittest import mock


target = Path("tests/test_inventory_and_profiles.py").resolve()
spec = importlib.util.spec_from_file_location("review_a_inventory_tests", target)
if spec is None or spec.loader is None:
    raise AssertionError("test module could not be loaded")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

matrix = (
    (
        "_final3_windows_writer_reused_handles_are_role_isolated",
        "_WindowsGovernanceFileOwner",
        "_resolve_ambiguous_close",
        ("staging", "published", "recovery", "deterministic_lock"),
    ),
    (
        "_final3_windows_writer_reused_handles_are_role_isolated",
        "_WindowsHandleOwner",
        "_reconcile_ambiguous_close",
        ("directory",),
    ),
    (
        "_round7_windows_file_owners_bind_before_caller_failure",
        "_WindowsGovernanceFileOwner",
        "_resolve_ambiguous_close",
        ("staging", "original", "recovery", "published", "readback", "published_disposal"),
    ),
    (
        "_round9_windows_disposition_absence_beats_same_inode_reuse",
        "_WindowsGovernanceFileOwner",
        "_resolve_ambiguous_close",
        ("staging", "published_disposal", "recovery"),
    ),
)
results: list[dict[str, object]] = []

for helper, owner_type, method_name, schedule_names in matrix:
    for target_occurrence, schedule_name in enumerate(schedule_names, start=1):
        case = module.AtomicAndGitBoundaryTests(
            "test_windows_persistent_close_failures_are_truthful_and_retryable"
        )
        case.setUp()
        generator = case.generator
        owner_class = getattr(generator, owner_type)
        original = getattr(owner_class, method_name)
        state: dict[str, int | None] = {"seen": 0, "native": None}
        detected = False
        with module._ControlledWindowsHandles(generator.secure_filesystem) as routing:

            def replay(owner: object, *labels: object) -> object:
                token = owner.ambiguous_handle
                if token in routing.replacements:
                    state["seen"] = int(state["seen"] or 0) + 1
                    if state["seen"] == target_occurrence:
                        state["native"] = routing.replacements[token][0]
                        if not generator._windows_try_close_file(token):
                            raise AssertionError("mutant replay close was refused")
                        if routing.native_is_open(state["native"]):
                            raise AssertionError("mutant did not close the native replacement")
                return original(owner, *labels)

            try:
                with mock.patch.object(owner_class, method_name, replay):
                    getattr(case, helper)(routing)
            except AssertionError as error:
                detected = "native replacement was closed" in str(error)
                if not detected:
                    raise
            else:
                raise AssertionError(
                    f"{helper}/{schedule_name} did not reject the replay mutant"
                )
        if state["seen"] != target_occurrence or state["native"] is None or not detected:
            raise AssertionError(
                f"incomplete replay evidence for {helper}/{schedule_name}: "
                f"seen={state['seen']}, native={state['native']}, detected={detected}"
            )
        results.append(
            {
                "helper": helper,
                "owner_type": owner_type,
                "schedule": schedule_name,
                "occurrence": target_occurrence,
                "native": state["native"],
                "raw_oracle_detected": detected,
            }
        )

if len(results) != 14:
    raise AssertionError(f"unexpected replay matrix size: {len(results)}")
print(json.dumps(results, sort_keys=True))
