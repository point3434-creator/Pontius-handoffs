# Independent cold review A: r010

Reviewer ID: codex/cold_review_a
Candidate commit: 29c02f6fbd5eb0b7ddc9e816ef28f570b9839358
Manifest SHA-256: 8741fa20b1ebc7e9e9d226f463680c603c348f1332bf19c8ae12b29579f76deb
Defect verdict: FINDINGS
Design verdict: WRONG SHAPE

Three important false-negative defects remain in the helper-authority contract.
On both actual CPython 3.11.15 and 3.14.6, nine independent mutation witnesses
produce TypeError in a harmless runtime projection, while the real public
derive_design_review API returns no blocker and the stale subprocess capability
`["-m", "fixed"]`. Ten corresponding nonmutation/nonexecution controls pass.
The existing focused suites pass; they do not close these failures. This report
does not permit the later broad wall, finalization, or a capability grant.

## Required corrections

All three findings are Important (high severity), with high confidence. They
concern a classifier admitting stale callable authority; no sensitive fixture
body or experimental owner was executed to demonstrate them.

### A-01: returned callbacks lose later free-cell authority

Frozen locations: tools/generate_test_inventory.py:17279-17286, 17900-17903,
and the returned-value obligation path in _evaluate.

This body appears inside ColdTests.test_case; ColdTests._launch is the declared
static helper. The separately authored harmless helper returns `"fixed"`.
Only the source submitted to the analyzer has the literal subprocess sink.

```python
owner = None
def mutate():
    if owner is not None:
        owner._launch = None
def forward(callback):
    return callback
saved = forward(mutate)
owner = ColdTests
saved()
return self._launch()
```

Python's closure reads the later `owner` cell and invalidates _launch. The analyzer
returns no blocker and one fixed capability row. Returning `(callback,)[0]` or
`{"cb": callback}["cb"]` gives the same failure. Omitting the later owner rebind
is a lawful control and passes both the runtime and analyzer.

The return path selects obligations only when authority is discoverable in the
callee's current values. Free bindings are stored as value tuples, and call-time
refresh is conditional on lexical-scope identity. The demonstrated result is that
an authority-bearing callable can leave a helper without retaining the later
cell dependency. The exact internal causal contribution of each transfer helper
is inferred from those source paths; the public false negative is directly proved.

Required outcome: retain the callable's relevant free-cell dependency across
returns and container projections, or explicitly refuse its later unsupported
execution. A temporarily irrelevant cell value cannot prove absence of later
effects. Preserve the no-rebind and dormant controls, callee/argument ordering,
and the finite analysis budget. Add checks through the public API, not an assertion
about a particular internal field.

### A-02: dictionary extraction discards retained callback authority

Frozen locations: tools/generate_test_inventory.py:12440-12463,
17972-17981, and 19545-19625.

```python
def mutate(owner=ColdTests):
    owner._launch = None
box = {"cb": mutate}
callback = box.pop("cb")
callback()
return self._launch()
```

`box.get("cb")` and `box.popitem()[1]` also fail. All three harmless runtime
projections end in TypeError; all three analyzer results have zero blockers and
the fixed capability. Merely extracting and retaining the callback, without
calling it, remains lawful in the paired controls.

The container contains the callable's captured default, but unknown member/result
propagation carries only the owner's existing helper_obligations. The mutable
method fallback returns an unknown value using legacy sensitivity, which does
not include the new callable-authority fields. This is an authority-transfer
gap, not a request to implement every dictionary or Python heap operation.

Required outcome: an extracted authority-bearing value must preserve authority
through consumption, or the unsupported extraction/consumption must explicitly
refuse. Cover read and removing extraction, nested results, and alias routes.
Do not treat dropping a capability row as sufficient: an unresolved relevant
effect requires a blocker. Retention alone must not be reported as execution.

### A-03: earlier class methods are absent from later construction bindings

Frozen location: tools/generate_test_inventory.py:22338-22355.

```python
class Value:
    def mutate(function=None):
        ColdTests._launch = None
    def __call__(self, callback=mutate):
        callback()
Value()()
return self._launch()
```

The earlier function is bound in the live class namespace when the later default
is created. The analyzer misses the reached mutation and emits the stale fixed
capability with no blocker. Two independent construction variants also fail:
`def method(self, ignored=mutate()): ...` and `@mutate` applied to a later method.
Those effects occur during class construction even when the later method is
never called. Replacing mutate's body with `return function` makes each control
lawful; all three controls pass.

The class-body loop records a method's metadata and appends its authority but
does not install that method into class_values before processing the next body
statement. Assignments advance class_values; function definitions do not. The
existing class-order matrix exercises assignment aliases, so it does not cover
this admitted binding statement.

Required outcome: every admitted class-body binding statement must contribute
its effective source-point binding before subsequent defaults and decorators
are evaluated. If an effective construction binding is unsupported, refuse it
explicitly. Preserve the distinction between construction effects, deferred body
effects, and portable annotation refusal; the correction must not execute source.

## Design assessment and advisory engineering guidance

The current helper-authority replacement remains dependent on several partial
representations: legacy sensitivity, callable/default/free-value fields, embedded
helper obligations, AST-keyed evaluated values, and a separate call-result map.
Three independent public failures show authority being silently lost at a return,
a collection result, and a class-definition binding. The concern is not file size
or personal style: the representations do not enforce the same transfer invariant.

Recommend redesigning the bounded helper-authority slice before another local
symptom patch. Keep the existing parser, capability schema, legacy analyzer,
exception semantics and budgets. Give the slice a single transfer contract:
every operation receiving a value returns its abstract result together with
retained callable identity, relevant cell dependencies and unresolved effects.
Represent supported callable identity separately from the current value of a
captured cell. Constructors, container/method results, returns, merges and class
binding steps must use that contract, with an explicit refuse fallback when a
represented authority cannot be preserved or discharged. This need not become
a general Python interpreter or introduce new capabilities.

This is a medium-sized refactor of the helper-authority slice and its contract
tests, larger than adding three method-name cases, but smaller than replacing
the entire generator. Main transition risks are false positives for dormant or
readonly callbacks, loss of precise exception successors, duplicated effects,
and budget bypass. Verify with public-boundary transfer matrices containing both
late-binding and captured-default variants, paired dormant/reached controls,
and real harmless ordering oracles. The 19 retained checks are a starting set,
not an exhaustive proof or prescribed implementation.

This recommendation is advisory; A-01 through A-03's outcomes are required.
The pinned protocol interpretation says a second residual on this contract
requires a separate root-cause/design reassessment. These failures are within
the stated existing identity/effect contract; the coordinator must apply that
rule without treating packet numbers as residual counts. This review itself
authorizes no replacement or scope expansion.

## Independent inputs, identity, and coverage comparison

The only initial inputs were the assigned handoff, candidate/manifest,
acceptance, protocol interpretation, pinned CLAUDE/workflow, and allowed frozen
requirements/source. No prior or peer review, status, self-report, transcript,
implementation discussion, or mutable production source was opened.

The handoff and every pinned initial-input hash matched. I recomputed the 17
whole-row-sorted SHA-256 rows from Git blobs and matched the manifest byte for
byte. The six A/B modules and four suites match the specified preservation ref;
CI, boundary checker and v0a boundary suite match their specified preservation
ref. The actual FIX delta is exactly the generator, its contract tests, and
tests/test-inventory.json. The legacy dependency-baseline blob remains
5fe6ee47f3380b65887b528efef05b72c8e6ac0a. All 17 checked-out manifest hashes also
match the independently recomputed blob hashes.

Before opening coverage.md I recorded checks/codex-a-independent-inventory.md,
SHA-256 77d8aaf6ba42b623f8a31bc9d24cbaa1f8a1b7c8498f5a6ab91dd0db058340ae.
The later coverage hash matched 75513c3217e4f8bde476f6dcd7ddb214a4bd14b78161a0c980e31a39b3a3875f.

My inventory already identified late cells, returned callbacks, collection
transfer and class/default/decorator ordering. The deferred claim covers those
categories, but the exercised cases omit return-before-rebind, dictionary method
extraction, and prior method definitions as class-namespace bindings. Thus the
claim's category discovery does not establish the required transfer closure.
The failures directly meet its stated stale-capability/no-refusal falsifiers.
I did not reuse the implementation's raw checks as independent pass evidence.

The fresh static check confirms all 2,860 existing inventory entries remain
identical, 13 entries are added, and profile bytes are unchanged. All 193 prior
top-level class methods remain present; the sole changed existing method AST is
the mechanical CheckedInInventoryTests census method. The added methods are
the 13 declared callable-authority tests. The six-origin boundary/legacy policy
checks pass, and source inspection confirms all five new CI gates retain
!cancelled() reachability without deleting or demoting old gates.

## Fresh verification and evidence

All floor payloads completed before the first dev payload. Control wrappers run
under actual CPython 3.11.15 with -I -S -B -P. Payloads assert full executable,
implementation and patch version before Pontius imports, run with -B -P from
the exact-candidate clone root, resolve the package from that clone's src,
and use a scrubbed environment, D-local TEMP/TMP and an absolute non-reparse Git
executable. Each receipt records command/environment/log hashes and confirms
all 1,761 tracked clone files are unchanged after execution.

| Fresh check | 3.11.15 | 3.14.6 |
| --- | --- | --- |
| tests/test_inventory_and_profiles.py | 119 tests, exit 0 | 119 tests, exit 0 |
| tools/generate_test_inventory.py --check | exit 0 | exit 0 |
| tests/test_v0a_boundaries.py | 18 tests, exit 0 | 18 tests, exit 0 |
| tools/check_stabilization_boundaries.py | exit 0 | exit 0 |
| Independent 19-case assertion probe | 9 failures, exit 1 | same 9 failures, exit 1 |

The assertion probe is checks/codex-a-probe-targets-v2.py, SHA-256
b0171cf48c0905f558829173c549c85cee760786565fe88fe2a5f3cfd00d1669.
It imports the frozen generator and calls derive_design_review directly. It
never compiles or executes the sensitive source mapping. A separate source
builder constructs harmless runtime programs containing only unittest plus
local functions/classes/mutations; their helper returns a string. These programs
are compiled with dont_inherit=True. Each emitted record includes the exact
submitted source, its digest, oracle result, public rows and blockers.

Detailed logs and command/environment receipts:

- checks/codex-a-inventory-311[-receipt.json / .txt]
- checks/codex-a-inventory-314[-receipt.json / .txt]
- checks/codex-a-v0a-boundaries-311[-receipt.json / .txt]
- checks/codex-a-boundary-check-311[-receipt.json / .txt]
- checks/codex-a-probe2-inventory-check-311[-receipt.json / .txt]
- checks/codex-a-probe2-inventory-check-314[-receipt.json / .txt]
- checks/codex-a-probe2-v0a-boundaries-314[-receipt.json / .txt]
- checks/codex-a-probe2-boundary-check-314[-receipt.json / .txt]
- checks/codex-a-probe2-targets-v2-311[-receipt.json / .txt]
- checks/codex-a-probe2-targets-v2-314[-receipt.json / .txt]
- checks/codex-a-probe2-static-314[-receipt.json / .txt]

The failing probe log SHA-256 values are
3ac7f58791a173ea868d428244431ad954fdd34e3657c31f258696d133e36435
(floor) and
1b54cf362517618017acc01f9749f7c878b11f9837966c850c1258f2b3615194
(dev). Ten controls pass on each slot, including a proved local failed lookup
before argument evaluation. Exploratory refusal-only/unsupported class-member
cases were not elevated to product defects. The initial 16-case exploratory
probe and receipt are retained separately as codex-a-probe-v1.py and
codex-a-probe2-independent-v1-311 artifacts.

Setup notes: an initial sandbox denial prevented assigned artifact creation;
subsequent authorized escalation was restricted to reviewer-owned artifacts and
disposable clones. An unused second-clone wrapper safely refused a create-only
manifest-name collision before any payload; a uniquely named wrapper/clone was
then used. Neither event is a candidate-test failure. No issued artifact was
overwritten, and no production/source/test file was edited.

No full 17-target wall, guarded profile, GPU run, installation, owner invocation,
source seal, rehearsal, performance measurement, commit, or push was performed.
A/B behavior was preserved by exact blob comparison, not re-certified as a new
live hand result. No CLEAN review or broader acceptance claim is made.
