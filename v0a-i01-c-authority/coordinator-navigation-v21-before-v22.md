# C integration: partial core replacement selected

2026-08-31. Navigation only. No new implementation candidate, cold verdict,
acceptance claim or main integration. Frozen implementation handoffs remain a
git snapshot ref plus manifest SHA-256; issued evidence is unchanged.

## Current decision

The controller authorized choosing the most effective repair/rewrite strategy.
The coordinator selected a partial replacement of C's analyzer-state/helper-
authority core. Accepted A/B and working C boundary/CI/publication paths stay.
The design replaces overlapping live value/authority/cell/deferred representations
and the helper-entry/review bridges that reconstruct execution from projections.
It explicitly supersedes only the old Stage0 representation choice, retaining
all behavioral contracts, limits, evidence and final review gates.

Read the [short brief](rewrite-stage0-v1.md), [design](rewrite-design-v1.md), and
[design-review disposition](rewrite-design-disposition-v1.md). Engineering review
found six design gaps; the coordinator's successor addresses them. The original
review input is retained byte-exact. No engineering review is a cold pass.
The [design manifest](rewrite-design-manifest-v1.sha256) binds retained inputs.

No replacement production code or controller has been written or executed.
Next: category/coverage plan and concrete R1 implementation plan, then a small
whole public-analyzer path through six existing temporal cases. R2 adds two exact
depth contracts and four ambient-size cases while rerunning the six (12 total).
Gate B has a preselected196608-unit continuation ceiling under the unchanged
262144 production cap; its sufficiency is unproved. Gate A records all budget
epochs under the original cap. No old-engine rescue, fixture-specific routing,
or stand-alone storage test substitutes for public behavior.

## Prior repairs are held, with their actual verdicts intact

V30 includes the two added enumeration-pair accounting charges. Its verified
actual3.11.15 run remains52/53: generator70 hits the262144 work cap before the
required deferred-generator-depth64 refusal. No dev/matrix/corpus expansion ran.
[V30 verification](coordinator-v30-design-verification-v1.json).

Diagnostic v5 is frozen and unexecuted. Its bounded static engineering review
found no dispatch blocker, but it is held during the strategy change. The
mechanism of v30's remaining cap failure has not been measured.

V23 remains42/52 on the fixed semantic packs on both interpreters, with ten
unsafe examples wrongly approved. V25 was source-reviewed and blocked before
execution. V31 is unfinished held scratch, not an issued or tested candidate;
[custody receipt](strategy-hold-v31-v1/custody-receipt-v1.json) retains it. No
further layered patching is authorized by this navigation update.

The original558 passes were93 finite storage checks repeated across two actual
interpreters and three seeds. V28's changed primitives later passed93 checks on
each interpreter at seed0. These remain useful bounded primitive evidence;
they do not establish full analyzer or integration readiness. The replacement
does not inherit obsolete adapter APIs just to reproduce those counts.

## Preservation and final gates

Accepted A/B remains r007. Other C paths and the generated pair are preserved.
W remains rejected v20. Main remains d1ed3cb with user-owned CLAUDE.md and
docs/workflow.md unchanged. Last implementation pair remains rejected r010:
29c02f6fbd5eb0b7ddc9e816ef28f570b9839358 /
8741fa20b1ebc7e9e9d226f463680c603c348f1332bf19c8ae12b29579f76deb.

The new core still owes all fixed design/matrix/semantic/corpus gates, preserved
capability rows and census accounting, one coherent freeze, two fresh mutually
blind cold reviews, permitted CPU acceptance, and the named finalizer checkpoint.
Claude remains finalizer; main commit/push needs candidate-specific controller
authorization. No guarded/GPU run or live15000 ms product result is implied.

[Previous navigation](coordinator-navigation-v15-before-v16.md) preserves the
earlier status, including what was still in progress at that checkpoint.

## Final design review and exact early population

The [bounded rereview](rewrite-design-engineering-rereview-codex-a-v2.md) verified
the frozen design pair and found all six concerns addressed. Its comprehension
wording clarification is retained in [the scope addendum](rewrite-scope-clarification-v1.md):
implicit comprehension locals belong to their own frame; free-name lookup skips
the class namespace. Read that addendum with the v1 design; issued bytes are unchanged.

[The early population](rewrite-early-population-v1.json) binds exactly Gate A6 and
Gate B12 to the original cases and depth assertions. [Static verification](coordinator-rewrite-population-verification-v1.json)
rehashes12 whole inputs,10 source/Model case records and36 original source spans.
No payload ran. These are design checks, not implementation or performance results.
The combined [design manifest v2](rewrite-design-manifest-v2.sha256) includes the
clarification, rereview and population. Category/API implementation planning,
operation accounting and a reviewed controller still precede production edits/runs.
[Navigation before this addendum](coordinator-navigation-v16-before-v17.md).

## R1 implementation preparation

The controller said to proceed. The isolated r010 worktree is prepared; the
[concrete plan](rewrite-r1-implementation-plan-v1.md) and [coordinator disposition](rewrite-r1-plan-disposition-v1.md)
define the sole source writer, public-path replacement, accounting and2500-line
first-attempt boundary. [Static checks](coordinator-rewrite-r1-static-v1.json)
confirm the six original public cases/eight Models and preserved harness helpers.
[The preparation manifest](rewrite-r1-preparation-manifest-v1.sha256) freezes
the exact plan/harness/baseline inputs. Independent harness review and root
baseline dispatch still precede source GO. No replacement source or payload
has been executed at this entry; it does not imply implementation acceptance.
See [R1 progress](rewrite-r1-progress.md); [prior navigation](coordinator-navigation-v17-before-v18.md).


## Canonical core engineering checkpoint

The original Gate A baseline is RED with intact evidence. State primitives have
completed the bounded ownership/cost review and its two prewiring corrections;
scope facts and the source-order evaluator are now retained as Task3. The Task2
review identified missing compile-time bindings in dormant pattern/comprehension
syntax; Task3 includes that category correction, pending independent rereview.
Construction, invocation and public-path replacement are in progress. No
replacement candidate has executed, and no acceptance verdict follows.

[R1 progress](rewrite-r1-progress.md) records current checkpoints. The prepared
[Gate B harness](tests-checks/rewrite-r2-handoff-v1.md) is unexecuted and held;
Gate A and a separate source/harness disposition precede its use. The
[private-API inventory](rewrite-private-api-compatibility-inventory-v1.md)
records a later migration decision; no original test or legacy-engine exception
has been authorized. [Prior navigation](coordinator-navigation-v18-before-v19.md).


## R1 Gate A completed on both interpreters

The corrected canonical source is frozen at H b1d15de062ac45c351f0254b358ee1e5fc35bdee,
manifest beb50fab0fe159249de1397529b78a71e2b176b8e3643ea64ccb37dbf1a1c15a,
source c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f.
Its two engineering source reviews closed the bounded corrections. Root then
ran the unchanged six-case/eight-Model Gate A on actual3.11.15 and3.14.6; both
passed with independent receipt/snapshot/accounting verification. The two
original class-adoption failures are corrected. See [the result record](rewrite-r1-gate-a-core01-results-v1.md).

The largest epoch is6692 under the unchanged262144 cap. Both hidden cases
refuse unproved truth before a join: no joined-cell or branch-scaling claim.
R2 planning is next; the original Gate B remains held for its recorded missing
comparison premise and a separately frozen correction. No broad suite, original
test migration, main integration, final cold acceptance or live-hand result yet.
Source remains held while the next plan is reviewed. Earlier entries describe
their historical checkpoints and are not relabeled by this addendum.


## R2 inputs and harness authoring

R1 Gate A remains green on both actual interpreters; no later runtime has run.
The next population uses four new identity-partition sources and independent
Models, preserving all six original controls and both original depth cases.
The source-visible identity premise replaces only the previously identified
unproved equality premise; old evidence and twelve later sibling obligations
remain unchanged.

The independent input review found one missing original envelope reference.
The population-only v2 correction adds that exact entry; all twelve references
now resolve and all eight original descriptors/envelopes remain exact. See
[the closure review](rewrite-r2-population-v2-closure-review-v1.md).
The corrected population is frozen at H 2393d9b3680426f5a3169ddb19e7b542ce68531d,
manifest 3ca45c9839ae6f7101d6405607260d766a18ed6ab260886c65a92bffb1a2471d.

The bounded exception/generator plan and natural-operation observer spec have
SOUND engineering reviews. [Harness authoring](rewrite-r2-harness-authoring-disposition-v1.md)
is authorized at H d50db9a83ba86ac9711676af700c9db814c0e752, manifest
387b77ff2790486cfc00924c2e05ea77cde703b166e67f12246bcf858ead8174.
Next: freeze/review exact harness, retain full twelve-case R1 baseline, then
R2 source GO under its separate 1500-line limit. Intermediate source checks
remain static. Production, broad acceptance, final cold reviews and main
integration are still open; no new performance or live-hand claim follows.

[Navigation before this entry](coordinator-navigation-v20-before-v21.md).
