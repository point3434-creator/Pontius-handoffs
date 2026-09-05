"""Read-only diagnostic of the unchanged Windows test's failed precondition."""
import json
from pathlib import Path
import runpy
import sys

target = Path("tests/test_inventory_and_profiles.py").resolve()
observations = []

def trace(frame, event, argument):
    if (event == "exception"
            and frame.f_code.co_name == "_round7_windows_file_owners_bind_before_caller_failure"
            and argument[0] is AssertionError):
        local = frame.f_locals
        caught = local.get("caught")
        chain = []
        seen = set()
        while caught is not None and id(caught) not in seen:
            seen.add(id(caught))
            chain.append({"type": type(caught).__name__, "message": str(caught)})
            caught = caught.__cause__ or caught.__context__
        observations.append({
            "family": local.get("family"), "line": frame.f_lineno,
            "assertion": str(argument[1]), "selected_handle": local.get("selected_handle"),
            "replacement": local.get("replacement"),
            "replacement_blockers": len(local.get("replacement_blockers", ())),
            "close_attempts": local.get("close_attempts"), "caught_chain": chain,
        })
    return trace

sys.argv = [str(target),
            "AtomicAndGitBoundaryTests.test_windows_persistent_close_failures_are_truthful_and_retryable"]
sys.settrace(trace)
try:
    runpy.run_path(str(target), run_name="__main__")
finally:
    sys.settrace(None)
    print(json.dumps({"diagnostic_only": True, "observations": observations}, indent=2))
