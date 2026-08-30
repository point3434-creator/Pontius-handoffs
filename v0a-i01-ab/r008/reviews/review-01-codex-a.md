# Cold review A - v0a-i01-ab/r008

Defect verdict: **NOT CLEAN** - two Important findings, both high confidence.
Design verdict: **STRAINED** - advisory engineering assessment, separate from
required behavioral corrections.

Candidate: `00db06624ab25f10cd181badccf92c87a78f17ee`
Manifest SHA-256: `1e5814b2c04a0065586d8fa73f89edc1ffb0eae4830bea8c893630172d5798f2`
Base: `d1ed3cbda6107d61ea8e77133871720af04970cd`
Reviewer: Codex A, fresh independent cold context; issued 2026-08-30.

## Required corrections

### R008-A-01 - Important: comprehension-local receivers inherit outer instance authority

Location: `tools/generate_test_inventory.py:22637`, `_review_body` receiver-context
construction; `_helper_is_bound` at line 21682. Related lexical visitor:
`_ExceptionBindingVisitor._visit_comprehension` at line 9684.

The public `derive_design_review` boundary accepts a literal subprocess helper
call reached through a comprehension variable that shadows the unittest instance:

```python
class ReviewTests(unittest.TestCase):
    def _launch(self=None):
        subprocess.run(
            [sys.executable, "-m", "fixed"], cwd=".",
            env={**__import__("os").environ, "SAFE": "1"},
            timeout=7, check=False,
        )

    def test_static(self):
        [self._launch() for self in [None]]
```

Actual Python resolves the comprehension's `self` to `None` and raises
`AttributeError` before invoking `_launch`. Both CPython 3.11.15 and 3.14.6 static
reviews instead derive one `['-m', 'fixed']` subprocess row and **zero** unresolved
dynamic blockers. Separate pure Python projections establish the AttributeError;
no inspected subprocess body is executed.

Demonstrated related paths: list, set and dict comprehensions, plus a nested list
comprehension. The opposing `[self._launch() for item in [None]]` succeeds in the
pure projection and remains statically accepted. An ordinary `for self in [None]`
loop and direct `self = None` reassignment do produce blockers, so merely passing
those tests does not cover comprehension scope.

Cause demonstrated by source and behavior: one receiver-kind dictionary is
computed for the outer method and reused for helper calls. The reused lexical
visitor deliberately does not treat comprehension targets as outer bindings,
which is correct for the outer scope but does not prove a receiver inside the
comprehension. `_helper_is_bound` then consumes the outer `self: instance` fact.

Required outcome: prove receiver identity in the lexical context of each call,
or emit a typed unresolved blocker. Comprehension target shadowing must not inherit
outer receiver authority, including when sink argv is completely literal. Preserve
lawful captures of an unshadowed outer instance. Verify all four demonstrated forms,
ordinary loop/reassignment controls, and the unshadowed opposing comprehension
through `derive_design_review` on both supported slots. No particular implementation
technique is required.

Evidence: `checks/codex-a-07-binding-probes.py`,
`checks/codex-a-10-binding-confirmation.py`, and both
`checks/codex-a-11-binding-confirmation-<version>.log` receipts.

### R008-A-02 - Important: class-qualified helper resolution ignores lexical shadowing

Location: `tools/generate_test_inventory.py:21820`, `_resolved_helper` raw
class-name registry lookup; `_helper_is_bound` at lines 21688-21702.

For a declared static `_launch()` containing the same literal subprocess sink:

```python
    def test_static(self):
        ReviewTests = None
        ReviewTests._launch()
```

The public review again derives one `['-m', 'fixed']` row with no blockers on both
interpreters. The independent pure projection raises `AttributeError`: the actual
receiver is `None`, not the registered class.

This is also confirmed for a parameter named `ReviewTests` defaulting to `None` in
a forwarded helper, a `for ReviewTests in [None]` loop, a comprehension target,
a nested function capturing the shadowed class name, and a classmethod target.
The unshadowed `ReviewTests._launch()` opposing control succeeds and is accepted.
These are ordinary lexical binding cases, not reflection, descriptor mutation or
execution of arbitrary replacement objects.

Cause demonstrated by source and behavior: `_resolved_helper` offers the raw
`<file>::<class-name>::<method-name>` registry candidate before proving that the
qualifier still denotes that class. `_helper_is_bound` checks provenance for
`self`/`cls` but accepts the registered static/class-qualified target without an
equivalent proof of the qualifier's current binding. Default/keyword argument
correctness cannot repair resolution to the wrong receiver.

Required outcome: class-qualified static, class and ordinary helper calls must
retain a proven class qualifier at the call site. Local assignments, parameters,
loop/comprehension targets and captured lexical names must invalidate an unproved
registry shortcut and produce a typed blocker, even with literal sink arguments.
Preserve the legal unshadowed class-qualified case and existing default/positional/
keyword behavior. Verify the six demonstrated invalid contexts and opposing control
through the public API on both slots. The required correction is behavioral, not
a demand for a particular resolver design.

Evidence: the same independent probe sources and two confirmation receipts above.
The first probe receipt additionally records existing invalid-arity, duplicate,
unknown-context and legal default/positional-only controls.

For both findings, the observed error is an unsupported capability derivation
without the required refusal. This review does not claim that the invalid fixture
actually launches a subprocess, that an approval was issued, or that any capability
writer was invoked. Both findings violate acceptance.md's explicit unknown-receiver
refusal requirement. The candidate cannot be CLEAN while either remains.

## Design verdict and advisory engineering guidance

**STRAINED.** The new descriptor metadata is a useful improvement, and computing
defaults before removing a bound receiver correctly addresses Python argument
alignment. However, callable registry selection, receiver-kind tracking, lexical
binding collection and source-ordered value flow are separate partial models.
The demonstrated failures occur where a fact from one model is treated as proof
in another: outer lexical ownership in a comprehension, and a source-level class
name after local rebinding. Both are already observable within this candidate;
no earlier review history is used to support this assessment.

Advisory technique: consolidate helper-call admission around one explicit per-call
resolution result containing the proven target, descriptor kind, bound/unbound
receiver context and argument binding, with an explicit unknown/refused state.
Use or extend the existing lexical/flow machinery rather than giving the raw
registry shortcut independent authority. This is a bounded refactor of helper
resolution and recursive/local entry propagation, with moderate integration and
regression-test cost; it need not replace the entire generator or alter inventory
formats, capability documents or approval semantics. A smaller patch remains a
controller/implementer choice if it closes the required contexts above.

A cheap falsifier for any proposed correction is already retained: run the public
review over the ten invalid pure-oracle cases and the two lawful opposing cases.
Then rerun the legal defaulted receiver, static all-default, positional-only,
unknown-decorator, direct-entry and nested/cross-file checks. This guidance is
advisory; only the required outcomes and verification criteria in A-01/A-02 bind.

## Identity, independence and scope

The whole-row-sorted blob manifest was recomputed from the frozen commit and
matched the packet bytes and published digest exactly. The candidate parent and
base match. All ten A/B files match r007 source commit
`ddea6efbeb55cb8b71da1ebd5a359a0c2c901cf1` byte-for-byte as Git blobs: the six
`src/pontius/v0a` modules and the four non-boundary v0a suites. No prior r007 review,
disposition, self-report or checks were read. The baseline blob remains
`5fe6ee47f3380b65887b528efef05b72c8e6ac0a`, and no sealed-kernel path is in the diff.

The seven C paths reviewed are CI, the boundary checker, the inventory generator,
the new boundary suite, inventory/profile tests, and the generated inventory and
profile pair. The source review followed module/origin normalization, import
policy, registry/descriptors, helper binding and recursive/local entry context,
direct unittest preflight, census changes, generated assignments and CI consumers.
It was not a fresh whole-history audit of accepted A/B implementation semantics.

Initial inputs followed the handoff allowlist. Independent path/invariant inventory
was written before coverage was opened:
`checks/codex-a-03-initial-inventory.md`, SHA-256
`2ba5628dc5f43f221fc6104015a7ff761e452815a10bab8542426e7654dd83a9`.
Acceptance SHA-256 and deferred coverage SHA-256 were independently verified.
Implementation narratives/status/plans, parent implementation discussion and prior
or peer review artifacts were not inspected.

Coverage comparison: the claim's named methods and focused suite counts reproduce,
and its declared import controls are consistent with direct results. Its receiver
context enumeration is incomplete: the two lexical categories above are not closed
by the ordinary reassignment and nested-parameter tests. This is demonstrated
behavioral failure, not a claim that missing cases alone prove a defect. General
reflection and arbitrary object alias analysis remain outside this review.

## Fresh verification evidence

A fresh D-local no-hardlink detached clone was created at:
`D:\Pontius-review-snapshots\codex-a-r008-b4138cf23699407a901e6c699771d00d\snapshot`.
Frozen blobs were checked out with conversion disabled, with no mutable working
source overlay. Actual CPython 3.11.15 ran first, then actual 3.14.6. Every payload
ran under `-B -P`, snapshot-root cwd and `PYTHONPATH=<snapshot>\src`, a scrubbed
environment, D-local TEMP/TMP and absolute Git. The bootstrap asserts executable,
full version, safe path, bytecode-disabled state and package origin before payload
execution; loaded v0a origins are checked afterward. The independent probes also
assert the exact frozen tool origin. Git is validated regular and non-reparse.

| Focused suite | 3.11.15 | 3.14.6 |
| --- | --- | --- |
| test_v0a_boundaries.py | 18 pass | 18 pass |
| test_inventory_and_profiles.py | 92 pass | 92 pass |
| test_stabilization_boundaries.py | 47 pass, 1 skip | 47 pass, 1 skip |
| test_v0a_hand_replay.py | 45 pass | 45 pass |
| test_v0a_trace.py | 53 pass | 53 pass |
| test_v0a_replay.py | 62 pass | 62 pass |
| test_v0a_contract_faults.py | 22 pass | 22 pass |
| generate_test_inventory.py --check | exit 0 | exit 0 |
| check_stabilization_boundaries.py | exit 0 | exit 0 |

Each slot ran 340 focused tests: 339 passed, one existing POSIX directory-descriptor
mutation test skipped on Windows. Both independent confirmation runs establish ten
invalid receiver approvals and two lawful opposing controls. Independent real
`check_repository` controls pass in both slots: unchanged source and legal visible
state accepted; foreign river import, deferred complete-deal attribute, initializer
host import, undeclared origin, new SCC, legacy-edge drift and malformed source
refused. Mutations were restricted to disposable control copies.

Independent inventory comparison preserves all 2,641 existing entries exactly as
parsed records, including assignments; all 205 additions are current-profile
entries (200 v0a tests plus five inventory tests). The CI difference is exactly an
additive insertion of the five v0a suite commands, each with `!cancelled()` and no
`continue-on-error`. Existing gates remain unchanged. Ordinary generator --check
proves the final generated pair is fresh without writing it. Existing census tests
pass; no approval/digest grant file is in the candidate diff.

Command/environment/exit receipts are `checks/codex-a-06-<version>-<label>.log`.
The retained harness is `checks/codex-a-04-bootstrap.py` and
`checks/codex-a-05-run-focused.py`. Independent integration sources/receipts are
`checks/codex-a-15-integration-probes-v2.py` and
`checks/codex-a-16-integration-probes-v2-<version>.log`.
Final receipt index, hashes and source verification:
`checks/codex-a-17-final-verification.json`.

One reviewer-harness failure is retained honestly: the first integration probe
compared UTF-8 Git text with default-codepage-decoded checkout text on CPython 3.11.
The append-only v2 specifies UTF-8. The separate diagnostic proves exact raw CI
insertion equality; both v2 slot runs pass. No candidate repair or retry-to-hide
product failure occurred.

Final verification confirms the snapshot is Git-clean and all seventeen physical
source hashes still match the manifest. No source edits, installs, GPU runs,
guarded profiles, broad CI wall, capability grants, source seals, rehearsals,
lifecycle invocation or authority publication were performed. No claim is made
about non-Windows native behavior, performance, timing campaigns or adversarial
Python introspection. Focused green suites do not override the demonstrated
receiver-binding defects.