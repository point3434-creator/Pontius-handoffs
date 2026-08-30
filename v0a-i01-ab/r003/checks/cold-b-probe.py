"""Independent r003 cold-B evidence; no source/test modification."""
from __future__ import annotations
import contextlib
import dataclasses
import hashlib
import inspect
import io
import json
import os
from pathlib import Path
import platform
import runpy
import subprocess
import sys
import traceback

snapshot = Path(sys.argv[1]).resolve()
version = sys.argv[2]
commit = sys.argv[3]
mode = sys.argv[4]
receipt_path = Path(sys.argv[5])
assert not receipt_path.exists(), "receipt is append-only"
report = {"mode": mode, "expected_commit": commit, "command": sys.argv[:],
          "executable": sys.executable, "version": platform.python_version(),
          "cwd": str(Path.cwd()), "environment": dict(os.environ),
          "flags": {"dont_write_bytecode": sys.dont_write_bytecode,
                    "safe_path": sys.flags.safe_path}, "sys_path": sys.path}

def git(*args):
    result = subprocess.run([os.environ["PONTIUS_GIT"], "-C", str(snapshot), *args],
                            capture_output=True, check=True)
    return result.stdout

try:
    assert platform.python_version() == version
    assert sys.dont_write_bytecode and sys.flags.safe_path
    assert Path.cwd().resolve() == snapshot
    assert os.environ["PYTHONPATH"] == str(snapshot / "src")
    assert "PATH" not in os.environ
    assert os.environ["PONTIUS_GIT"] == r"C:\Program Files\Git\cmd\git.exe"
    assert git("rev-parse", "HEAD").decode().strip() == commit
    assert git("status", "--porcelain") == b""
    import pontius.v0a.runtime as runtime
    from pontius.holdem_cards import OneSeatCardState
    from pontius.immutable_blueprint import (ImmutableBlueprintActionSource,
        BlueprintActionEntry, BlueprintDecisionKey)
    from pontius.no_limit_betting import (NoLimitBettingState, LegalBettingDecision,
        RaiseBounds, BettingActionKind, BettingStreet, CALL, CHECK, FOLD, raise_to)
    assert Path(runtime.__file__).resolve() == snapshot / "src/pontius/v0a/runtime.py"
    report["module_origin"] = runtime.__file__
    report["signature"] = list(inspect.signature(runtime.select_blueprint_action).parameters)
    assert report["signature"] == ["source", "cards", "betting", "decision"]
    if mode == "identity":
        parent = git("rev-parse", "HEAD^").decode().strip()
        tree = git("rev-parse", "HEAD^{tree}").decode().strip()
        raw = git("diff-tree", "-r", "-z", "--no-commit-id", "--no-renames",
                  "--name-status", "HEAD^", "HEAD").decode().split("\0")
        rows = []
        checks = {}
        for offset in range(0, len(raw) - 1, 2):
            status, path = raw[offset:offset + 2]
            blob = git("cat-file", "blob", f"HEAD:{path}")
            digest = hashlib.sha256(blob).hexdigest()
            rows.append(f"{digest}  {path}\n")
            checks[path] = {"status": status, "sha256": digest, "bytes": len(blob),
                "CR": b"\r" in blob, "BOM": blob.startswith(b"\xef\xbb\xbf"),
                "long_lines": [n for n, line in enumerate(blob.decode().splitlines(), 1)
                               if len(line) > 100],
                "trailing_whitespace": [n for n, line in enumerate(blob.splitlines(), 1)
                                        if line != line.rstrip()]}
        manifest = "".join(sorted(rows)).encode()
        packet = receipt_path.parent.parent
        report.update(parent=parent, tree=tree, changed_blobs=checks,
                      manifest_sha256=hashlib.sha256(manifest).hexdigest())
        assert set(checks) == {"src/pontius/v0a/runtime.py", "tests/test_v0a_hand_replay.py"}
        assert parent == "2f4287f68a83fac4225a05a91daffdb3f2977a43"
        assert tree == "fbf234bfffcdb51113b3b137a36afa3460bc94b5"
        assert manifest == (packet / "manifest.sha256").read_bytes()
        assert report["manifest_sha256"] == "21d9686c9918d9d0648fd98edf35219dfb5e0b4dc1dcfe5e4f28171b7d94e513"
        assert git("rev-parse", "refs/heads/review/v0a-i01-ab/r003").decode().strip() == commit
        for check in checks.values():
            assert not any(check[k] for k in ("CR", "BOM", "long_lines", "trailing_whitespace"))
        git("diff", "--check", "HEAD^", "HEAD")
        for path in ("src/pontius/immutable_blueprint.py", "src/pontius/no_limit_betting.py",
                     "src/pontius/v0a/replay.py"):
            assert git("cat-file", "blob", f"HEAD:{path}") == git("cat-file", "blob", f"HEAD^:{path}")
        report["sealed_and_replay_unchanged"] = True
    elif mode.startswith("suite:"):
        suite = mode.split(":", 1)[1]
        stream = io.StringIO()
        saved_argv = sys.argv
        sys.argv = [str(snapshot / "tests" / suite)]
        result = 0
        try:
            with contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
                try:
                    runpy.run_path(sys.argv[0], run_name="__main__")
                except SystemExit as error:
                    result = error.code
        finally:
            sys.argv = saved_argv
        report["suite_output"] = stream.getvalue()
        report["suite_exit"] = result
        assert result == 0, report["suite_output"]
    elif mode == "probe":
        hooks = []
        class IntHook(int):
            def __eq__(self, other):
                hooks.append("int-eq")
                raise AssertionError("caller int equality")
        class TupleHook(tuple):
            def __iter__(self):
                hooks.append("tuple-iter")
                raise AssertionError("caller tuple iteration")
            def __len__(self):
                hooks.append("tuple-len")
                raise AssertionError("caller tuple length")
        class BoundsHook(RaiseBounds):
            def __getattribute__(self, name):
                hooks.append("bounds-attr")
                raise AssertionError("caller bounds access")
        class SourceHook(ImmutableBlueprintActionSource):
            def action_for(self, **kwargs):
                hooks.append("source-lookup")
                raise AssertionError("caller source lookup")
        base = NoLimitBettingState.six_max_100bb(button=0)
        check_state = base
        for _ in range(4):
            check_state = check_state.apply_action(FOLD)
        check_state = check_state.apply_action(CALL)
        states = [
            ("raise", base),
            ("no-raise", NoLimitBettingState.new_hand(button=0, starting_stacks=(2,) * 6,
                                                     small_blind=1, big_blind=2)),
            ("short-all-in", NoLimitBettingState.new_hand(button=0,
                starting_stacks=(200, 200, 200, 3, 200, 200), small_blind=1, big_blind=2)),
            ("history", base.apply_action(CALL)), ("check", check_state)]
        assert states[0][1].legal_decision().raise_bounds is not None
        assert states[1][1].legal_decision().raise_bounds is None
        assert states[2][1].legal_decision().raise_bounds.all_in_only is True
        assert states[3][1].history
        assert states[4][1].legal_decision().can_check
        deep = 1
        for _ in range(2000):
            deep = (deep,)
        cases, controls, observations = [], [], []
        lookup_code = ImmutableBlueprintActionSource.action_for.__code__
        def invoke(source, cards, state, decision):
            lookup = []
            def observe(frame, event, arg):
                if event == "call" and frame.f_code is lookup_code:
                    values = frame.f_locals
                    lookup.append({"owned_source": values["self"] is not source,
                                   "owned_cards": values["cards"] is not cards,
                                   "owned_betting": values["betting"] is not state,
                                   "derived_decision": values["decision"] is not decision})
            caught = None
            value = None
            hooks.clear()
            sys.setprofile(observe)
            try:
                value = runtime.select_blueprint_action(source, cards, state, decision)
            except Exception as error:
                caught = type(error).__name__
            finally:
                sys.setprofile(None)
            return value, caught, lookup, list(hooks)
        for label, state in states:
            cards = OneSeatCardState.preflop(controlled_seat=state.acting_seat,
                                            private_hand=(0, 13))
            decision = state.legal_decision()
            source = ImmutableBlueprintActionSource("cold-b-independent")
            mutations = []
            for field in dataclasses.fields(decision):
                original = getattr(decision, field.name)
                for category, wrong in (("depth-2000", deep), ("shallow-tuple", (1,)),
                                        ("list", []), ("mapping", {})):
                    mutations.append((f"{field.name}/{category}",
                                      dataclasses.replace(decision, **{field.name: wrong})))
                if type(original) is int:
                    for category, wrong in (("float-alias", float(original)),
                                            ("bool-alias", bool(original)),
                                            ("different-int", original + 1),
                                            ("int-subtype", IntHook(original))):
                        mutations.append((f"{field.name}/{category}",
                                          dataclasses.replace(decision, **{field.name: wrong})))
            for index in range(len(decision.action_kinds)):
                values = list(decision.action_kinds)
                values[index] = deep
                mutations.append((f"action_kinds/element-{index}/depth-2000",
                                  dataclasses.replace(decision, action_kinds=tuple(values))))
            for category, wrong in (("subtype", TupleHook(decision.action_kinds)),
                                    ("extra-element", (*decision.action_kinds, BettingActionKind.RAISE)),
                                    ("wrong-enum", (BettingStreet.PREFLOP,))):
                mutations.append((f"action_kinds/{category}",
                                  dataclasses.replace(decision, action_kinds=wrong)))
            mutations.append(("street/wrong-member",
                              dataclasses.replace(decision, street=BettingStreet.RIVER)))
            if decision.raise_bounds is not None:
                bounds = decision.raise_bounds
                for field in dataclasses.fields(bounds):
                    original = getattr(bounds, field.name)
                    wrong_values = [("depth-2000", deep), ("shallow-tuple", (1,)),
                                    ("numeric-alias", int(original) if type(original) is bool
                                     else float(original)),
                                    ("wrong-value", not original if type(original) is bool
                                     else original + 1)]
                    for category, wrong in wrong_values:
                        bad_bounds = dataclasses.replace(bounds, **{field.name: wrong})
                        mutations.append((f"raise_bounds.{field.name}/{category}",
                                          dataclasses.replace(decision, raise_bounds=bad_bounds)))
                mutations.append(("raise_bounds/absent", dataclasses.replace(decision, raise_bounds=None)))
                subclass = BoundsHook(**{f.name: getattr(bounds, f.name)
                                         for f in dataclasses.fields(bounds)})
                mutations.append(("raise_bounds/subtype", dataclasses.replace(decision, raise_bounds=subclass)))
            else:
                mutations.append(("raise_bounds/unexpected-present", dataclasses.replace(
                    decision, raise_bounds=base.legal_decision().raise_bounds)))
            for category, bad in mutations:
                value, caught, lookup, called_hooks = invoke(source, cards, state, bad)
                cases.append({"case": f"{label}/{category}", "exception": caught,
                              "lookups": len(lookup), "hooks": called_hooks,
                              "pass": caught == "InvalidDecisionContextError" and
                              not lookup and not called_hooks and value is None})
            key = BlueprintDecisionKey.from_state(cards=cards, betting=state, decision=decision)
            hit_action = raise_to(decision.raise_bounds.minimum_raise_to) if decision.can_raise else CALL
            passive = CHECK if decision.can_check else CALL
            other_cards = OneSeatCardState.preflop(controlled_seat=state.acting_seat, private_hand=(1, 14))
            other_key = BlueprintDecisionKey.from_state(cards=other_cards, betting=state, decision=decision)
            sources = [("miss", source, passive, False, None),
                       ("hit", ImmutableBlueprintActionSource("hit", (BlueprintActionEntry(key, hit_action),)),
                        hit_action, True, None),
                       ("other-key", ImmutableBlueprintActionSource("other", (BlueprintActionEntry(other_key, CALL),)),
                        passive, False, None),
                       ("illegal", ImmutableBlueprintActionSource("illegal", (BlueprintActionEntry(key,
                        raise_to(decision.raise_bounds.maximum_raise_to + 1 if decision.can_raise else 1)),)),
                        None, None, "InvalidBlueprintEntryError")]
            for kind, supplied, action, table_hit, exception in sources:
                value, caught, lookup, called_hooks = invoke(supplied, cards, state, decision)
                good = caught == exception and len(lookup) == 1 and all(lookup[0].values()) and not called_hooks
                if exception is None:
                    good = good and value.action == action and value.table_hit is table_hit
                    good = good and value.source_digest == supplied.digest
                controls.append({"case": f"{label}/{kind}", "exception": caught,
                                 "lookup": lookup, "hooks": called_hooks, "pass": good})
            _, caught, lookup, called_hooks = invoke(SourceHook("hook"), cards, state, decision)
            controls.append({"case": f"{label}/source-subtype", "exception": caught,
                             "lookup": lookup, "hooks": called_hooks,
                             "pass": caught == "InvalidDecisionContextError" and not lookup and not called_hooks})
        report.update(cases=cases, controls=controls, case_count=len(cases), control_count=len(controls),
                      case_failures=[row for row in cases if not row["pass"]],
                      control_failures=[row for row in controls if not row["pass"]])
        assert not report["control_failures"], "valid/authority control failed"
        assert not report["case_failures"], "malformed context did not receive typed pre-lookup refusal"
    else:
        raise AssertionError("unknown mode")
    optional = [name for name in sys.modules if name.split(".")[0] in {"cupy", "torch"}]
    report["optional_imports"] = optional
    assert not optional
    assert git("status", "--porcelain") == b""
    report["exit"] = 0
except BaseException as error:
    report["exit"] = 1
    report["failure"] = traceback.format_exc()
finally:
    receipt_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"receipt": str(receipt_path), "mode": mode, "exit": report["exit"],
                  "case_count": report.get("case_count"), "case_failures": len(report.get("case_failures", [])),
                  "control_failures": len(report.get("control_failures", []))}))
sys.exit(report["exit"])
