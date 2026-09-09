# r003 cold review 02 - Codex

Defect verdict: CLEAN. No Critical or Important finding survives frozen-source
verification. There is no required correction in this review.

Design verdict: SOUND. The revised shape separates completed-hand eligibility
from decision agreement, and sampling inclusion from agreement eligibility.
Those boundaries address the two recurring defect categories directly. The
remaining implementation work is substantial but does not require another
change of design shape on the evidence reviewed here.

Reviewer: Codex, independent cold reviewer 02. Issued: 2026-09-08.
Scope: Tier C Stage 0 / Stage 0b specification review, both complete documents.
This is not an implementation pass, execution authorization, or adoption decision.

## Binding identity and cold-input record

- Candidate: 18b7527a3989f7d38830a7881c976385fe9bc4de
- Manifest SHA-256:
  2664aca6f857999a4b45036b5cd3c250fbc3d8210b3132510d0e05a57e821975
- Base: b378104cd2934f248a9545d7d482b0db25db813c
- Tree: 26952b679cde91cc3c975500e2dd15a9270934ca
- Ref: refs/heads/review/v0a-eval-panel-design/r003
- Scope: docs/architecture/v0a-eval-panel-r001/{brief,design}.md only.

The handoff was read first. Candidate text was read from Git blobs; no mutable
candidate worktree was used. I recorded the invariant and related-path inventory
before opening coverage.md, then compared the claim against that inventory.
After that comparison I read the r002 disposition. No r003 sibling report,
task progress ledger, implementer conversation, or coordinator analysis was read.

The independent inventory is delivered separately as r003-review-02-inventory.md:
SHA-256 a10adc8db0579b18ea49c6c344ecf5df898a6fdc8fe957736c53c85019fd683a.
It remains the pre-coverage record; the comparison below does not overwrite it.

## Required findings

None.

## Main verification results

Locations below are frozen source line numbers: brief/design at CANDIDATE;
all other repository sources at BASE. Coverage is the pinned packet input.

### Outcome envelopes and retained stream

The revised mechanism 5, design.md:160-197, is supported by the real envelopes.
`runtime.py:1233-1266` raises on rejected or ambiguous publication before normal
v1 decision construction; `_from_failure` at 1345-1365 returns a failed outcome
with a nullable decision and a FailureRecord. `_reject` at 1375-1392 also covers
not-attempted delivery and null timing. `v0a/model.py:445-519` and
`v0a/trace.py:216-250` confirm the distinct wire shapes. Delivery status belongs
to the failure record, not the v1 decision record.

The adapter emits the nullable members at tools/v0a_event_adapter.py:243-247.
The host rejects failed events both before action publication and after the
expected action at tools/v0a_table_host.py:671-678 and 844-858. Successful v1
decisions must have completed timing and no failure at 797-815; timing cutoff
flags are checked at 689-707. A later timing failure therefore cannot leave a
hand eligible merely because an earlier decision was accepted.

Terminal handling at host:886-913 rejects incomplete hands, incomplete
accounting, interrupted responses, failure causes, inconsistent settlement,
failed session closure, and trailing frames. Session play_hand at
tools/v0a_table_session.py:235-315 retains the failed hand result, captures the
child streams, checks cleanup and exit status, and produces completed status
only after all those gates. The actual session path is hands[*].result; the
outer item supplies ordinal, button and starting_stacks. The design's term
"hand entry" denotes that retained result envelope, not a new flat schema.

ChildConnection.read_stream at host:512-538 captures stdout up to 2,097,152
bytes, flags overflow and records transport failure. Session completion also
requires capture_truncated to be false. Thus a truncated frame stream cannot
silently qualify for river-record classification. Missing or duplicate river
records in an otherwise eligible agreement hand are explicitly excluded with
protocol diagnostics. These checks do not require a decision to classify failure.

The independent lookup cross-check is necessary. Host v1 validation checks the
applied action and state identities, but its expected dictionary at 832-838
contains no independently computed selection_reason. Provider-mode lookup at
741-758 is a different branch. `PreparedBlueprint.action_for` at
src/pontius/blueprint_preparation/lookup.py:49-67 constructs the complete key and
returns an explicit table_hit flag. Comparing that flag with the retained reason
separates an in-pool check hit from an off-pool check default even when both
produce the same applied action. The direct BlueprintProvider check separately
covers its observation/proposal contract (providers.py:24-44); runtime:363
confirms blueprint-v1 does not instantiate that provider.

### Population, missingness and arithmetic

Mechanisms 7 and 9, design.md:210-299, preserve the accepted sampling law.
Collision-only rejection and both orientations remain explicit; no H-membership
filter survives. Dealer generation at tools/v0a_seeded_deals.py:33-65 is a
seeded permutation with an unbiased bounded-index mapping under its stated
random-word model. Given a board and hero hand, the compatible villain count is
choose(45,2) = 990; marginalizing the other eight private cards gives the same
number of folder completions for every compatible hero/villain pair. The hero
count is choose(47,2) = 1,081. Conditioning on realized folder cards would be a
different population and is correctly disclaimed.

BaselineProvider at decision_provider/providers.py:65-91 demonstrates the
card-dependent premium preflop raise. Retaining its completed settlement in chip
comparisons is necessary for the declared deployed-policy estimand. Excluding
it from river agreement alone does not select the chip population. Mechanism
7's explicit retention rule takes precedence over the river-record requirement,
which belongs to Slice A agreement, not universal chip eligibility.

A cutoff correlated with the intended bet still causes nonrandom missingness.
The revision no longer claims that whole-unit exclusion repairs that problem.
Any exclusion withholds the affected board and pooled full-population claims;
meeting a survivor sample floor cannot restore them. This satisfies brief
criteria 5 and 7 without silently replacing the estimand with survivors.

The stated normalization is consistent: unit totals sum both orientations,
so their expected value is 2*m_P,B; differences have expectation
2*(m_A,B-m_C,B). With the declared opponents, only the two blind seats invest
chips. Hero net chips lie within [-s,s], each orientation difference within
[-2s,2s], and the two-orientation unit difference within [-4s,4s]. The range
width is therefore 8s. Hoeffding's two-sided bound gives the stated planned
floor (8s)^2*ln(2/alpha_B)/(2*epsilon^2). Allocating alpha across four boards
and averaging their simultaneous intervals with fixed 1/4 weights is coherent
and requires no sampled-board or few-cluster asymptotics.

For n planned units, k observed unit differences summing to T, the proposed
missing-unit bounds are [T-4s*(n-k), T+4s*(n-k)]/n. These are worst-case bounds
on the complete planned sample mean, not by themselves confidence intervals for
the dealer expectation. The candidate withholds that population claim, so it
does not misuse them as a replacement confidence result. A sample with half its
units at 8 and half at 0, losing all 8-valued units at s=4, illustrates the
fix: survivor mean 0; full planned mean 4; bounds [-8,8]; no ranking claim.
This is an algebraic illustration, not an executed test or experiment.

### Earlier corrections, oracle and scope

The per-hero T1 partition at design.md:119-143 is valid at s=4 because the
opponent is fixed and the sole hero information set is the root. Frozen
no_limit_betting.py:392-422 yields minimum and maximum raise-to 2 after the
prefix; the hero is all-in after betting. Legal continuation action order at
legal_river_continuation.py:44-66 places check before raise. Evaluation's
best_response at evaluation.py:169-273 selects the first maximizing action.
Singleton-hero best_response remains the independent algorithmic check; the
new enumeration is not allowed to replace that ground truth. The expensive
sealed membership checks remain real (continuation.py:195 and 241), and the
preflight/cost stop is explicit rather than assumed measured.

The retained prefix fixture at tests/test_legal_river_continuation.py:26-55,
host opponent selection at tools/v0a_table_host.py:213-225, full key construction
at immutable_blueprint.py:48-102, and ordered card views at holdem_cards.py:52-61
support replay and shared board order. Settlement net_returns at
no_limit_betting.py:735-749 equals final stack minus initial stack. Teacher
returns use the same sealed game/settlement semantics at
legal_river_continuation.py:288-309, with river.py supplying ranking and range
normalization. This tests the export and instrument against the declared game,
not the truth of a broader poker model; the brief says so explicitly.

Wire-byte measurement, strength-blind pool choice, final artifact recheck,
fixed four-board strata and s=4 survive. T2 is deferred pending its declared
determinization and has no T1 partition shortcut. The existing codec/provider
labels stay closed. No source changes outside the two documents are frozen.

## Deferred coverage comparison and advisory guidance

The path-based claim now matches the material category in my independent
inventory: teacher, export, acquisition, composition, child frames, validation,
retention, classification, provider, settlement, pairing, divergence, exclusion,
inference and recording. Its falsifiers address behavior, including missing
records and correlated failure, rather than just recurrence of finding text.
All 21 stated base blob pins recompute correctly, including river.py, trace.py
and legal_decision_spine_v2.py. No material semantic hole was found in the key
or primary teacher/oracle path.

The inventory is not a transitive import closure: my initial list also named
game.py, deferred cfr.py, the retained prefix test and future lifecycle helpers.
The recording row names execution.begin_run/finish_run without a corresponding
inventory pin. The whole frozen tree already binds those bytes, and no current
finding follows merely from their absence in a selected semantic inventory.
Advisory: carry the source-admission and execution/status writer-consumer paths
into the implementation round's coverage inventory once orchestration exists.
This is not a new acceptance gate or a reason to block this specification.

Advisory implementation details: preserve the actual hands[*].result nesting;
keep agreement eligibility separate from chip eligibility; distinguish
planned-sample missingness bounds from population confidence intervals; record
each sampled draw even if the unordered pair repeats; and preregister enough
seed/index pairs for the planned floor, respecting dealer indices 0 through 15.
These implement existing requirements, rather than granting new behavior.

## Workflow and evidence limits

Stage 0 fields are present: tier and protected invariant, scope and seams,
numbered acceptance/ground truth, dependencies, size budget, stop/kill rules,
round budget, forbidden claims and verification plan. Stage 0b names mechanisms,
invariants and covered places, failure traps, alternatives, rulings, category,
project dependencies, barriers, permanence and exclusions. The explicit request
for this review authorizes r003 only; it does not settle a general budget rule.

Checklist v1: (1) the oracle and real-boundary controls are specified; (2), (4)
and (5) subprocess environment, module resolution and disposable execution are
future implementation checks, not established here; (3) real producer/consumer
shapes were traced; (6) negative schedules preserve real failure preconditions;
(7) capacity and cost gates require future measurements; (8) exclusion and
acceptance predicates now test their intended boundary; (9) no ownership code
changes, with cleanup failure retained through the session; (10) candidate and
review artifact text hygiene checked, exact value typing remains an execution
obligation; (11) candidate manifest and all supplied identity pins recomputed.

Specification assessment: pass at the design-review scope. Engineering-quality
assessment: sound architecture with implementation validation pending. No host,
runtime, solver, historical owner or test was invoked; none is evidence here.
No capacity, cost, strength, live-clock, calibration or sample result was measured.

Fresh checks: Git ref/commit/parent/tree and two-file diff; raw-blob SHA-256
whole-row manifest reconstruction; workflow/rulings/coverage SHA-256; all 21
base inventory pins; README/workflow/roadmap blob pins; candidate and delivered
report/inventory text hygiene. The raw candidate manifest exactly matches the
packet row file and its stated digest. Native PowerShell/.NET performed hashing.
An earlier Python hash-only attempt failed with access denied; its escalation
was aborted without executing the script. This is an environment event, not a
product failure or a test run.

The report and reviewer-authored single ledger line are staged under
D:/Pontius/tmp for coordinator delivery to the packet. No fetch, commit, push,
source/candidate edit, lifecycle write or sibling-review access occurred.
