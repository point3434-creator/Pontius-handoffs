# Cold review — reviewer 02 (Codex)

Task: `v0a-eval-panel-design/r002`, FIX round, Tier C specification review.
Reviewer: Codex, independently dispatched reviewer 02. Date: 2026-09-08.

**Defect verdict: NOT CLEAN.** Two Important findings survive source verification.
No Critical finding. No implementation, runtime, solver, host, or test was invoked.

**Design verdict: STRAINED.** The reduced river game, per-hand T1 computation,
and fixed-board paired instrument fit the bounded task. However, the design still
uses a decision record as the whole execution outcome and treats matched deletion
as preserving a population target. These are separate boundaries. Define a
session/event outcome classifier, then an explicit missing-outcome inference rule.
That is a bounded design correction; a new game, codec, or provider is unnecessary.

## Identity and cold-input discipline

This report and every finding bind to:

- Candidate: `61a1ce0ce964dc56b67636ff71a613e5525ab0ae`.
- Manifest SHA-256: `8e5b22c22e4f7a7d4a0eff603ed256cc18a66351a329f27b011e6c52c8bbd9e2`.
- Ref: `refs/heads/review/v0a-eval-panel-design/r002`.
- Base and sole parent: `b378104cd2934f248a9545d7d482b0db25db813c`.
- Tree: `cf5c090f80ceeaf5118214e08e4362a0062b5f3c`.

I read only `handoff.md` first. I then read the frozen candidate, pinned
requirements, and relevant frozen source, and recorded the independent invariant
and related-path inventory in `D:/Pontius/tmp/r002-review-02-inventory.md` before
opening `coverage.md`. Only then did I read coverage and the permitted r001
disposition. I did not read r001 reviewer reports, another r002 review, an
implementer transcript, coordinator conversation, or sibling-agent material.

Candidate locations below refer to Git blobs at the full candidate above. All
source locations refer to Git blobs at the full base above, not working files.
`design.md` and `brief.md` abbreviate
`docs/architecture/v0a-eval-panel-r001/design.md` and the companion `brief.md`.

## Required findings, severity ordered

### R02-01 — Important, high confidence: the v1 exclusion oracle still requires a nonexistent
decision field and misses decision-less failures

**Candidate locations:** `design.md:14-22`, `design.md:152-170`,
`design.md:195-201`, `design.md:285-287`; `brief.md`, acceptance criteria 1-2.

**Violated contract:** The actual host boundary must classify each execution
outcome correctly, retain failures as exclusions, and never mistake them for
policy decisions. The design expressly calls its mapping exhaustive and plans
cutoff/failure checks against constructed v1 decision records.

**Frozen evidence:**

- `src/pontius/v0a/model.py:445-461`: `DecisionRecord` has `timing` and
  `failure_reason`, but no `delivery_status`. That field belongs to
  `FailureRecord` at `model.py:492-499`.
- `src/pontius/v0a/trace.py:216-251`: the wire serializer preserves that
  separation. The decision payload has no delivery field; the failure payload
  carries `delivery_status` and may have nullable timing.
- `src/pontius/v0a/runtime.py:1233-1265`: publication rejection or ambiguity
  raises `_HandFailure` before a decision record is constructed. The normal
  record construction follows publication at `runtime.py:1014-1085`.
- `runtime.py:1345-1365` and `tools/v0a_event_adapter.py:238-247` publish a
  failed outcome with independently nullable `decision` and `failure` members.
- `tools/v0a_table_host.py:796-814` validates the exact v1 decision field set,
  which lacks delivery status. Its failed-event branch at `:848-854` permits
  a missing decision; in blueprint-v1 mode it requires that absence.

**Concrete failing scenario:** A valid in-pool river request selects its teacher
action, but publication is rejected. The runtime emits a failure with
`delivery_status = rejected` and no `DecisionRecord`. Applying mechanism 5's
record-only mapping has no record on which to evaluate its exclusion predicate;
the declared category fails to account for this cell. Even the ordinary successful
v1 record cannot supply the design's claimed delivery field. Constructing a
synthetic v1 decision with that field would contradict the frozen public schema.
Reading only successful records can silently omit this failure; requiring the
field on all records instead rejects valid successful sessions.

**Smallest required correction:** Define exclusion at the existing event/session
outcome boundary, with failure precedence. Name which retained failure/host report
supplies delivery information; handle failures with no decision and null timing.
Only after a successful outcome should the river decision be classified by
`table_hit`/`passive_default`, pool membership, and selected action. Keep the
separate direct provider check. Add planned cases for successful v1 payloads,
pre-publication failure with no decision, accepted delivery followed by timing
failure, and host/transport failure lacking an ordinary decision. Use real frozen
payload shapes, not invented fields. No sealed-source modification is required.

This is a residual of the r001 host-oracle contract: correcting the selection
labels was valid, but the enclosing failure representation remains wrong. The
missing `v0a/trace.py` serializer in the supplied dependency inventory is directly
relevant to this miss; it is not a separate product defect.

### R02-02 — Important, high confidence: whole-unit exclusion does not preserve the declared full
accepted-deal estimand

**Candidate locations:** `design.md:183-211`, `design.md:221-238`,
`design.md:281-291`; `brief.md`, acceptance criteria 5-7.

**Violated contract:** Calibration and policy comparisons claim the full
collision-accepted population, with hero uniform on 1,081 and villain uniform on
990, and valid uncertainty around its mean. Mechanism 7 discards a whole matched
unit whenever any compared cell diverges, times out, or fails. Mechanism 9 only
counts these deletions against the sample-size floor. It states no missingness
assumption, stopping rule for informative loss, or missing-outcome bound.

**Concrete failing scenario:** On an ordinary nonconstant board with profitable
T1 table entries, consider T1 versus the empty blueprint. A permitted failure
schedule causes a cutoff whenever an orientation would take T1's bet, while
check/check units complete. The all-or-nothing rule removes every unit containing
a T1 bet from both policies and orientations. Every retained difference is then
zero, although the full-population T1 advantage is positive. Acquiring more
completed check/check units satisfies any finite retained-sample floor and makes
their interval narrow around zero; it does not recover the missing profitable
units. This is a falsifying schedule, not a claim that such timing was observed.

The issue does not depend on a clock mechanism changing the mathematical poker
outcome. If `D` is the planned matched-unit difference and `R` indicates that all
cells survive, the estimator after deletion targets `E[D | R = 1]`, whereas the
design declares `E[D]`. Pairing ensures that all policies use the same `R`; it
does not imply independence of `R` and `D`. The same problem is possible with
card-dependent prefix divergence: the frozen baseline makes premium preflop
raises (`decision_provider/providers.py:66-81`), and the design explicitly
excludes its diverged units across policies. The acquisition law can remain
collision-only while the analysis population is nevertheless filtered.

**Consequence:** Full-population calibration can fail because a correct policy
has selectively missing outcomes, and precision/ranking on another comparison
can be biased even if a separate T1 calibration passes. Calibration against one
known expectation is not a proof that missingness is ignorable in all comparisons.
The loss-budget guarantee cannot follow from a Hoeffding bound on retained units
alone. The frozen runtime explicitly admits cutoff/deadline failures
(`runtime.py:1056-1093`); they are not declared impossible in this specification.

**Smallest required correction:** Preserve whole-unit pairing, but specify what
inferential statement is allowed when units are excluded. The simplest bounded
option is to withhold the full-population acceptance/ranking result when there
are missing units, while retaining diagnostic counts and completed observations.
Alternatively, preregister valid worst-case missing-outcome bounds using the
original planned denominator, or an explicitly justified observation/recovery
mechanism. A survivor-population target is another possible design, but it is a
changed estimand and requires corresponding calibration and limitations; it must
not be silently substituted for the accepted full population. Include a planned
case with exclusion correlated with a known nonzero unit difference and verify
that more survivor deals cannot erase the resulting uncertainty or bias.

This extends the population correction beyond membership rejection to its
related post-acquisition selection path. It does not ask to reinstate the
both-in-H filter or weaken pairing.

## Independent coverage assessment and corrections that do hold

The pre-coverage inventory explicitly separated record-less failures, outcome
serialization, missingness, population marginalization, unit scaling, key
identity, and teacher partition. The supplied coverage category is organized
around prior finding IDs. That is useful for tracking edits, but is narrower than
the design's claimed category, every path from teacher to recorded outcome plus
every exclusion. Its observation for the host mapping should include the
enclosing failed event, not only a v1 decision shape. Its population falsifier
should include post-acquisition selection, not only membership/rejection rules.

The inventory additionally misses `src/pontius/v0a/trace.py` (base blob
`8440aa0274b642af3e03326813989ff5b3333766`), which serializes the actual v1
oracle, and `src/pontius/legal_decision_spine_v2.py` (base blob
`824f4938788769be4165dcad04926bf9f2ec22e8`), which supplies public-state
binding used by the continuation and host. Add the relevant serializer and
state-binding members when repairing the coverage claim. A missing pin by itself
is not evidence that frozen source bytes changed; the verified whole-tree diff
already rules that out.

The following conclusions are supported by static inspection, without runtime
claims:


**Actual selection labels and direct provider.**

Runtime record constructor at `runtime.py:1286-1306` uses table hit/default;
`decision_provider/providers.py:23-44` accepts an exact observation and returns blueprint
hit/default proposals. The separate direct check is well-defined. Selection-label correction passes;
the enclosing failure oracle does not, per R02-01.

**Prefix and s=4 legal tree.**

Fixture prefix at `tests/test_legal_river_continuation.py:26-55` and `_raise_bounds` at
`no_limit_betting.py:392-421` support remaining stacks 2, minimum/maximum raise-to 2, no villain
raise against the all-in hero, and one hero decision. Source derivation passes.

**Per-hand T1 partition.**

The information key includes the hero hand at `legal_river_continuation.py:273-295`; with fixed
passive villain and one hero root, each conditional action maximization is independent. The
singleton-hero game preserves the conditional villain distribution. `evaluation.py:257-273` chooses
the first action on exact ties. Cross-check and cost preflight are appropriate Stage 0b obligations.

**Quadratic path and T2.**

`legal_river_continuation.py:195,241` rebuilds the deal dictionary. Avoiding the monolithic
production T1/calibration path is a valid correction. The document confines this partition to
fixed-opponent T1 and defers coupled T2. Cost feasibility remains unmeasured, honestly.

**Collision-only acquisition and hand swap.**

`v0a_seeded_deals.py:33-65` supplies the six private hands. Conditioning all twelve private cards to
avoid the fixed board leaves each compatible ordered hero/villain pair with the same number of
folder completions. The marginal counts 1,081 and 990, and 666 when conditioned on the realized
eight folder cards, are correct. Playing the swap with an off-pool default removes the former
compatible-degree filter. Post-acquisition exclusion remains R02-02.

**Fixed strata and bounded observation.**

Equal weights over four fixed boards are coherent. Each hero net outcome is in [-s,s], each policy
difference in [-2s,2s], and the sum of two orientations in [-4s,4s]. Extra deals only reduce
within-board sampling uncertainty. A bounded-difference floor can be preregistered for this unit.

**Advisory corrections from r001.**

s=6's three histories agree with fixture branches at
`tests/test_legal_river_continuation.py:94-110`. Weak dominance permits zero; a royal-flush board is
a correct all-zero control. `check`/`null` is three bytes longer than `raise`/`2`; final wire
remeasurement remains necessary. Board order is carried by `immutable_blueprint.py:85-101`, so
consistent ascending composition is appropriate. The marginalization qualifier and softened
random-board claim are sound within the stated approximation.

**Stage 0/0b and scope.**

Goals, invariants, seams, alternatives, rulings, dependency limits, budgets, stop/kill rules,
barriers, and forbidden claims are present. T2 determinization and measured budgets are explicitly
deferred. Production/runtime acceptance remains a future gate.

Two implementation-facing clarifications are advisory, not additional blocking
findings. First, state the arithmetic linking mechanism 8's mean chips per cell
to mechanism 9's sum per matched unit: the latter expectation is twice the former
for one policy, and twice the per-cell policy gap for a comparison. The current
definitions are reconcilable, but an explicit equation avoids a factor-of-two
mistake. Second, a declared variance estimate alone cannot justify a smaller
distribution-free floor: any variance-based tightening must name a valid bound
and its estimation uncertainty before holdout. Keeping the original Hoeffding
floor is sufficient. Neither advisory item is a reason to execute anything now.

Coverage's limits correctly say there is no implementation, no measured cost,
no executed partition, and no tests yet. Those are the correct limits of this
checkpoint, not automatically missing runtime evidence for a documentation review.

## Verification receipts and limits

All verification operations were read-only Git blob reads, source searches,
PowerShell/.NET byte hashing, or creation of this reviewer-owned staged report.
No candidate or sealed source was edited. No fetch, commit, or push occurred.

- `git cat-file -p` verified the candidate tree and sole base parent.
- `git rev-parse` verified the local candidate ref resolves to the full commit.
- `git diff --name-status BASE CANDIDATE` returned only the two added documents.
- Independent raw `git cat-file blob COMMIT:PATH` reads, SHA-256 hashing,
  whole-row ordinal sorting, and LF joining reproduced the manifest digest.
  The packet manifest's own bytes have the same digest.
- Brief blob SHA-256:
  `a34e5e0aa6591fe420010cf93dc2e7c08cd03a8bb504f93054a6b64bca8fbb86`.
- Design blob SHA-256:
  `c0248683f2b204aa44ebb9dce3bde2cde9cdece95956b966d506448bc544e5d8`.
- Both candidate documents are LF-only, BOM-free, and contain no trailing
  whitespace; maximum line lengths are 84 and 94 respectively.
- All 19 base blob pins in the design/coverage tables matched Git. The README
  and roadmap pins also matched. Packet workflow bytes and the base workflow
  both hash to `c71e3963ff726e06158878bcc10dd7dd761b32597af1c8ed39e21ebf60b58a37`.
- Controller-rulings SHA-256 verified as
  `2649ae254b3cd7692082920a2cc07d9b85dac2360cbcd71d375d0faa56a6ebd6`.
- Deferred coverage SHA-256 verified as
  `da5487bc8e2144f8ec7d4514353ddbfa6d4be3d7ce19c67818c6d083bb17408e`.
- These commands completed with exit status 0. Relevant frozen source was
  inspected directly; no result relies on an old test run or reviewer agreement.

Checklist v1 identity/exactness and Stage 0/0b structure are verified to the
extent applicable here. Public-boundary semantics are not clean for the two
reasons above. Subprocess execution, snapshot import identity, runtime ownership,
and future tests are unexecuted and make no pass claim in this specification
review. This report gives neither execution nor integration authorization.

The report is staged inside the writable workspace for delivery as
`r002/reviews/review-02-codex.md`. The separate reviewer-authored ledger line is
staged alongside it for append-only delivery to the task ledger.
