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
