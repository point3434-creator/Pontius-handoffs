# Independent cold review A - r009

Reviewer ID: codex/cold_review_a
Candidate commit: 8d240db477b8c141e6142e055dbfbedc75c6a2f8
Manifest SHA-256: 4f91aa7ce728c3eff6a7ad30a7c131985d5b86b615875df978d30ac39386aa51
Defect verdict: NOT CLEAN
Design verdict: STRAINED

One Important required correction remains. The helper analyzer can omit a reached
namespace mutation behind a local forwarding call and emit an unblocked capability
for the old helper body. Four related forms reproduce on both required interpreters.
The design judgment is advisory; the demonstrated contract failure is what blocks.

## A-01 - Important: incomplete default-name provenance lets forwarding skip effects

Confidence: high. Frozen location: tools/generate_test_inventory.py:23562
(referenced-name discovery and later helper seeds), :17391 (effect early return),
and :17210 (direct effect-shape inventory). Generator blob SHA-256 is
9031a42ded45bbd8af3afb3044c683be40ed45121c375b3de04e5bdf05b8c924.

Acceptance requires source-ordered callable authority across local helper paths,
definition-time defaults, effective inputs and reached effects. Unknown owner or
callable provenance must refuse explicitly; a historical literal sink is not
permission to expand the old callable. This finding violates that requirement.

A minimal test body is:

```python
def test_static(self):
    def mutate(owner=ReviewTests):
        owner._launch = None
    def invoke(callback=mutate):
        callback()
    invoke()
    self._launch()
```

Here ReviewTests is the containing unittest.TestCase class and _launch is a
staticmethod containing a literal subprocess.run([sys.executable, "-m", "fixed"],
...) sink. The entire data-only reproduction is retained in
checks/codex-a-reproduction-source.txt; its SHA-256 is
2aa584a7ba0a3a54aaab4a69acaf33ab1013030f1fd660e7ed04454be01bc82e.

Python captures the class in mutate's default, invokes mutate via invoke's default,
sets that class member to None, and then raises TypeError at self._launch(). A
separate harmless projection that replaces only the subprocess expression with
an event append confirms zero sink events and that TypeError. The sensitive
source itself was supplied as bytes to the real derive_design_review boundary;
it was never executed.

Actual candidate result on both 3.11.15 and 3.14.6:

- expanded subprocess argv: [["-m", "fixed"]]
- unresolved_dynamic_blockers: []

Thus the public review describes a sensitive invocation that the current callable
cannot perform, with no refusal. No approval, capability write, or actual child
execution was attempted. The defect is the unsound admission description, not a
claim that this review executed a dangerous capability.

The minimized 20-case comparison found four false-clean forms: positional callback
default, keyword-only callback default, explicit callback argument whose callable
captures the owner default, and a tuple-held owner default forwarded to a mutator.
All four execute the mutation and raise before the final sink in the harmless
projection. The other 16 cases explicitly refuse. Adding only
`unused = ReviewTests` before the definitions, changing the final lookup to
`ReviewTests._launch()`, or capturing `self` instead makes each form refuse.
The extra unused read and equivalent class/instance staticmethod access do not
remove the actual mutation. They change only which owner names the analyzer seeds.

Mechanism supported by source and these paired controls: referenced_names collects
assignment names, call-root names, direct callable names and decorators, but does
not generally seed a name used only as a local function default. _evaluate returns
a qname without helper provenance for that unseeded class reference. The forwarding
helper has no direct store, and its effective input carries no discovered helper
identity; _apply_helper_call_effects then returns early rather than following the
callee effect or refusing the unresolved effect. This is absence of discovered
proof being used as proof of absence. Direct mutation without forwarding does
produce an unresolved-owner refusal, further isolating the lost transitive effect.

Required behavioral correction and verification:

1. Preserve source-point authority for effective default/closure/receiver inputs
   through forwarding, or refuse when the required owner/effect cannot be proved.
   Do not emit an unblocked stale helper row in any of the four demonstrated forms.
2. Do not let semantically irrelevant reads or equivalent alias/static lookup forms
   decide whether a reached mutation is considered. Include paired metamorphic
   controls through derive_design_review, not only helper-internal assertions.
3. Exercise defaults in positional, positional-only and keyword-only positions,
   explicit callback forwarding, container-held owners and nested calls, with
   reached writes, dormant writes, invalid bindings and before/after-raise controls.
   Preserve lawful captured callees/defaults and retained aliases; unsupported
   shapes may refuse explicitly. Keep the existing finite work/depth budgets.

Evidence: checks/codex-a-probe-forwarding.py (SHA-256
c56e1a8aae327d2f9c1fa25ecbd58a38f5074abc37e107b61ad5fa360e16ff3e),
checks/codex-a-forwarding-311.txt (SHA-256
f5933b5594d8cafefa2374dcb0d1cab3563dfde6bdbab4b71c6ab147836a2952), and
checks/codex-a-forwarding-314.txt (SHA-256
d511f0fdec1b90fdb05ee0efa685edf79af3216d179ce0e86a3ac0c2a4a883a4).
Adjacent *-receipt.json files bind exact command, environment, exit, log digest,
snapshot identity and unchanged manifest-path bytes. Both focused probes exit 1
because the required refusals are absent, not because their setup failed.

## Independent inventory and coverage challenge

Before opening coverage.md, I independently reconstructed the whole-row-sorted
Git-blob manifest and saved checks/codex-a-inventory.md, SHA-256
500b705aaf5f935fe1dad315c041c966fa4398d96b127ecf9f7c77750e5ad342.
The saved inventory identifies definition-time capture, call forwarding, effective
inputs, exception successors, source-order identity and absent-proof risks.
The deferred coverage hash then verified as
a6c049cdc6681bb08218e2909d0150dc24352abe85bc6b9eea78047cf1f70f88.
No implementation discussion, old/peer review, coordination note or peer check
was opened. The optional linked coordinator evidence was not needed for this verdict.

The claim's seven-channel/five-scenario matrix and existing projections are useful
but do not cover owner identity used only in a default and then passed through a
store-free forwarding helper. Their usual final ReviewTests._launch() access seeds
the class and masks this omission. The independent 20-case comparison directly
falsifies the claim's stated no-unblocked-stale-row property. That coverage gap is
part of A-01, not a second duplicate defect.

The initial 29-case adversarial probe exits 1 with five strict-oracle mismatches:
three false-clean forwarding cases plus two conservative refusals of lawful code
(nonlocal rebinding with a retained alias; a nonliteral callable argument).
The latter two retain the correct capability row and refuse explicitly; I classify
them as precision limits/advisory observations, not additional blocking findings.
The dedicated 20-case comparison adds explicit-callback forwarding and separates
four confirmed false-clean cases from 16 correctly refused controls. All observed
results are identical between the two slots.

## Fresh verification and preservation

Each payload ran in the fresh D-local clone
D:/pontius-snapshots/cold-r009-a-56b2a4a4e9d546edb90aedb516039e8b/harness,
at the exact candidate, using an inspected independent wrapper. Control ran with
-I -S -B -P on actual CPython 3.11.15. Payloads ran with -B -P, snapshot-root cwd,
snapshot/src PYTHONPATH, scrubbed environment, D-local TEMP/TMP and a validated
absolute C:/Program Files/Git/cmd/git.exe. Full executable and version were asserted
and logged before Pontius import. For every target, 3.11.15 ran before 3.14.6.
The latter executable was D:/Pontius/.venv/Scripts/python.exe; the floor executable
was D:/Pontius-tools/py311/Scripts/python.exe. No inspected sensitive fixture body ran.

| Check | 3.11.15 | 3.14.6 | Evidence prefix under checks |
| --- | --- | --- | --- |
| 22 selected existing helper/descriptor/provenance contracts | PASS | PASS | codex-a-helper-contracts |
| Existing finite-analysis budget test | PASS, 1 test | PASS, 1 test | codex-a-budgets |
| v0a boundary suite, including real repository gate | PASS, 18 tests | PASS, 18 tests | codex-a-boundaries |
| Ordinary generator --check | PASS, no mutation | PASS, no mutation | codex-a-generator-check |
| Frozen inventory/CI/baseline preservation probe | PASS | PASS | codex-a-structure |
| Independent adversarial cases | 24/29 strict checks | 24/29 strict checks | codex-a-adversarial |
| Minimized forwarding comparison | 4 false-clean / 20 | 4 false-clean / 20 | codex-a-forwarding |

Each prefix has -311/-314 logs and receipts. Exact selected method names and
commands are in those receipts. Manifest-path source hashes remained unchanged
before/after every payload. The independent manifest reconstruction, ref, parent,
checkout bytes and pinned initial-input hashes are in codex-a-identity.json.

The full integration object contains 17 paths relative to main parent
 d1ed3cbda6107d61ea8e77133871720af04970cd. The FIX against
00db06624ab25f10cd181badccf92c87a78f17ee changes only generator, its contract test
and generated inventory. The six v0a source modules and four A/B suites exactly
match accepted preservation source ddea6efbeb55cb8b71da1ebd5a359a0c2c901cf1 as blobs.
No source or test was repaired. No sealed kernel or capability-grant path changed.

Independent structural checks establish all 2,641 main inventory entries remain
byte-equivalent as parsed entries, with 219 additions; all 2,846 FIX-base entries
remain unchanged, with 14 additions. The five v0a suites are present (18 boundary,
45 hand, 53 trace, 62 host replay and 22 contract-fault IDs). Profile bytes equal
the FIX base. CI preserves every old line and adds all five suite commands as
hard gates with !cancelled() reachability. The legacy dependency baseline remains
blob 5fe6ee47f3380b65887b528efef05b72c8e6ac0a.

A/B preservation is established here by exact source/test blob comparison;
this report does not claim a new exhaustive A/B runtime revalidation. I did not
run the full CI wall, guarded profiles, GPU/capability operations, installs,
source sealing, rehearsal, an owner or any experimental invocation. No fresh
full-corpus capability census or performance result is claimed. These limits do
not weaken the direct reproduction of A-01, and broad execution cannot cure it.

## Advisory engineering guidance and design assessment

The helper path's source values, demand-selected provenance seeds, direct
store-shape summary, effect resolver and later body expansion must all agree on
one Python call. The current code can preserve a qname while losing its authority,
then treat missing authority as harmless enough to skip transitive effects. The
four paired failures and their unused-read controls demonstrate that this risk is
already present; the extra 392 conservative effect refusals disclosed by coverage
show a precision cost, not a proof that mutation handling is closed.

Prefer a bounded refactor of this helper-admission/effect slice: one source-ordered
call context containing captured callable identity, effective defaults/arguments/
receiver and a typed effect conclusion. Make "proved no relevant effect" distinct
from "effect not resolved". Reuse the binder and finite resolver, and cache only
proofs whose input authority and state are bound; do not skip a reached callee
because its surface body contains only a call. Preserve definition-time versus
later closure lookup explicitly. This is moderate work confined to the helper
path and contract tests, not a rewrite of the entire inventory generator or a
request to reopen A/B. A local correction is possible, but merely adding the
four failing spellings would retain the structural weakness.

Use public-boundary metamorphic tests that vary only an irrelevant read, an owner
alias, or a default/explicit forwarding channel. A supported pure case should keep
its exact rows; an unresolved/mutated case must never become unblocked solely
because a discovery hint disappeared. Pair mutation schedules with dormant,
failed-binding and exception-before-effect controls. These implementation choices
are advisory; the three behavioral outcomes under A-01 are the required corrections.

No ledger entry was appended while authoring this report. The issuer will request
an exclusive append slot only after this report and its hash have been saved.
