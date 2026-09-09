# Cold review 01 — Codex — v0a-eval-panel-design/r002

Reviewer: Codex, reviewer 01 (fresh cold session).
Date: 2026-09-08.
Defect verdict: **NOT CLEAN** — two Important specification findings.
Design verdict: **STRAINED** — the reduced-game bridge and per-hand teacher now have a
coherent shape, but the outcome oracle still conflates distinct runtime artifacts and the
missing-outcome rule does not protect the declared estimand. Both admit bounded design
corrections; the evidence does not justify replacing the bridge or widening sealed interfaces.

This verdict binds to candidate **61a1ce0ce964dc56b67636ff71a613e5525ab0ae** and manifest
SHA-256 **8e5b22c22e4f7a7d4a0eff603ed256cc18a66351a329f27b011e6c52c8bbd9e2**.
Base: **b378104cd2934f248a9545d7d482b0db25db813c**.
All candidate locations below refer to that exact commit. Base-source locations refer to that
exact base, not working files. No implementation, runtime, solver, host, test, historical owner,
fetch, commit, or push was executed.

## Important findings

### R002-R01-01 — v1 decision records cannot implement the stated delivery/failure oracle

Severity: **Important**. Confidence: **high**, direct frozen-source evidence.
Required contract: brief criteria 1–2 and 5; exhaustive outcome/exclusion accounting.
Candidate locations: `design.md:14–21`, `design.md:152–170`, `design.md:195–201`, and the
constructed-v1-record test at `design.md:286–287`, all under
`docs/architecture/v0a-eval-panel-r001/`. Also `brief.md:91–98`.

The label correction is right, but the design still treats delivery status as a field of the
v1 `DecisionRecord`: it says the observable contains timing, failure reason, and delivery
status, and declares a record-based mapping exhaustive. The actual v1 record has no delivery
status. It is a field of the separate `FailureRecord`, and a failed dispatch can contain no
`DecisionRecord` at all.

Frozen evidence:

- `src/pontius/v0a/model.py:444–461` defines the v1 decision fields; no delivery field exists.
  `model.py:491–499` defines failure fields including `delivery_status`.
- `src/pontius/v0a/trace.py:216–251` serializes these distinct shapes without adding the
  missing decision field. `tools/v0a_table_host.py:796–799` requires the exact v1 decision
  field set, so adding a field to a constructed record would not exercise the real contract.
- `src/pontius/v0a/runtime.py:1233–1264` raises a failure on rejection or ambiguous delivery
  without attaching a decision. `runtime.py:1345–1364` then returns `status='failed'`,
  `decision=None`, and the separate failure with its delivery status.
- `tools/v0a_event_adapter.py:238–247` emits separate `decision` and `failure` payloads.
  `tools/v0a_table_host.py:671–678,848–854` accepts v1 failed event shapes without a decision
  and raises `child_failed`; its outer report also carries status/failure and can lack a
  settlement (`table_host.py:920–925,990–995`).

Concrete failing scenario: play an in-pool river hand, and the action publication is rejected
(or its acknowledgement is ambiguous). The actual dispatch has a failure with
`delivery_status='rejected'` (or `'unknown'`) and `decision=None`. There is no river v1 record
on which the mechanism-5 predicate can read timing, failure reason, or delivery status.
A literal implementation either dereferences an absent field on ordinary successful records,
or omits/misclassifies this attempted cell while counting only existing decision records.
A constructed v1 record with a delivery field is not a faithful test fixture. The declared
four-way accounting and whole-unit exclusion are therefore not fully implementable as stated.

Smallest required correction: define the host observation as a cell/session outcome combining
successful v1 decision records with the real event/hand/outer failure envelopes. Name where
successful delivery is established by the host protocol and where failed or absent delivery
is read from a `FailureRecord` or outer failure. Give failure/absence precedence over decision
agreement, including failure before a river record and terminal/transport failure after one.
Keep the separate direct `BlueprintProvider.propose` check. Add planned schedules using the
actual v1 envelope shapes, with a real-boundary control, rather than inventing decision fields.
No sealed model, codec, or provider change is needed.

FIX relation: residual of the host-oracle category R01-01/R02-01. The wrong provider reason
names were removed; exhaustiveness across the actual record/envelope boundary remains open.

### R002-R01-02 — whole-unit deletion preserves pairing but can change the estimand

Severity: **Important**. Confidence: **high**, mathematical counterexample to the specification.
Required contract: brief criteria 4–7; mechanism 8's full accepted-deal calibration population;
mechanism 9's fixed-board full-population paired mean and uncertainty.
Candidate locations: `design.md:183–201`, `design.md:204–211`, `design.md:221–238`;
`brief.md:103–121` in the same candidate directory.

The collision-only acquisition law and off-pool default rule repair the membership bias.
However, the next stage deletes every matched unit with any prefix divergence, cutoff, or
failure. Mechanism 9 only charges those deletions against the sample-size floor. It supplies
no condition that makes missing units independent of their chip outcomes, no missing-outcome
bound, and no rule withholding the full-population verdict when this condition is unknown.
The mean of survivors targets E[X | every cell survives], while the declared target is E[X]
over collision-accepted draws. Equal board weights and a larger surviving sample cannot remove
that difference. Whole-unit deletion protects within-unit comparisons, not sampling validity.

Concrete legal scenario: on board `2c 7d 9h Js Qc`, compare a deployed table that bets 2 with
`As Ad` and defaults for the other two example hands against an empty passive table, at s=4
and the declared passive opponent. Both policies use the required prefix. For matched unit
`{As Ad, Kh Kd}`, the first orientation changes hero net chips from +2 to +4 and the swapped
orientation defaults for both policies, so X=+2. For `{As Ad, Td 8d}`, villain has a straight,
so the first orientation changes -2 to -4 and the swapped orientation again defaults: X=-2.
Each unit has positive acquisition probability and admits many collision-free folder hands.
These are ordinary deterministic deployed-policy cells in the declared comparison scope.

Now an admissible cutoff/failure schedule excludes the first positive unit class in one cell
while the negative class completes. The prescribed whole-unit rule removes the positive class
from every policy/orientation. Increasing draws until the surviving count meets the Hoeffding
floor yields an increasingly precise conditional mean, not the full-population mean. No rule
in the design excludes this dependence; it expressly models outcome-dependent prefix behavior
and real resource failures. This is a counterexample to the inference rule, not a claim that
this schedule has been observed on the machine. Kernel settlement semantics support the chip
values (`legal_river_continuation.py:288–306`); fixed passive opponent behavior is defined at
`tools/v0a_table_host.py:213–225`.

Smallest required correction: specify how excluded units affect the full-population claim.
For example, withhold that claim when exclusions are unexplained, or carry conservative
missing-unit bounds into the interval and the loss-budget decision. A declared independently
justified missingness rule is another route. If a conditional-survivor estimand is intended,
state it explicitly and recompute its population/calibration; that changes the currently
promised target and must not be silently substituted. Retain whole-unit accounting and add a
planned hand-calculated case where failures correlate with X and enough survivors remain.
Do not treat a count-only floor or successful T1/empty calibration on a separate run as a
proof that missingness is harmless for every later comparison.

FIX relation: related-path extension of the population/estimand corrections. The original
both-in-H filter is closed; the post-play selection path was not covered by that correction.

## Advisory observations (not additional blocking findings)

### A01 — the advertised semantic inventory omits two direct dependencies

`design.md:253–266` and deferred `coverage.md` call the inventory the key/oracle dependency
inventory. It omits `src/pontius/v0a/trace.py` (base blob
`8440aa0274b642af3e03326813989ff5b3333766`), which actually serializes v1 decisions/failures,
and `src/pontius/legal_decision_spine_v2.py` (base blob
`824f4938788769be4165dcad04926bf9f2ec22e8`), which supplies the public-state digest and
spine reason contract used by the runtime, host and teacher. Both were discovered from direct
imports/calls; the initial inventory already identified the spine dependency. The whole-tree
identity guard passes, so these omissions are not proof of changed or faulty library bytes.
Add the direct dependencies or state a deliberately narrower inventory boundary. The trace
omission is useful evidence of why R002-R01-01 escaped the claimed field-exhaustive check.

### A02 — write the calibration normalization explicitly in the preregistration

Mechanism 8 describes a per-cell empirical mean and a per-orientation exact expectation;
mechanism 9 uses the sum of the two orientations and says the same definitions govern
calibration. These can be reconciled without changing the design, but the preregistration
should write the normalization rather than leave a factor-of-two trap. If m_B is the exact
per-orientation policy value, the expected matched-unit policy total is 2*m_B. If calibration
uses a per-cell mean, cluster its interval by the paired unit and divide the paired total by
two. For paired policy difference X, the expected unit difference is 2*(m_A,B - m_C,B).
Apply the same fixed 1/4 board weights to empirical and exact quantities when sample counts
differ. This is an implementation precision recommendation, not a separate defect verdict.

## Independent inventory and deferred coverage challenge

Ordering was preserved: I read only `handoff.md` first. I next read the whole candidate from
Git blobs, pinned rules/rulings, and initial base source surfaces. Before opening `coverage.md`
or r001's disposition I recorded a dated-session invariant/path inventory at
`D:/Pontius/tmp/r002-review-01-initial-inventory.txt`. No other r002 reviewer output, sibling
material, or coordinator conversation was used. The later r001 disposition was used only for
FIX disposition/category comparison.

The initial inventory covered identity; host decision versus delivered/failure shapes;
provider observation/propose; replayed root and settlement; T1 partition/ties/cost; wire
capacity; twelve-card acquisition and folder marginalization; off-pool swaps; board order;
paired sum versus calibration mean; post-play selection; fixed-strata uncertainty; and Stage
0/0b authority, dependency, budget and evidence boundaries.

Deferred claim assessment:

- **Category/method:** mapping r001 findings to corrections is appropriate for a specification
  FIX, but textual survivors alone are not a sufficient discovery method. The wider design
  category, every path to a chip result plus exclusions, requires following the serialized
  event/failure boundary and post-play selection. The two Important findings above are those
  concrete omissions; no generic missing-coverage accusation is being treated as a defect.
- **Host falsifier:** checking for obsolete `blueprint_hit` names passes, but the record-shape
  falsifier fails on an absent decision plus a separate failure envelope. The direct provider
  method is well-defined for valid constructed `DecisionObservation` values:
  `decision_provider/providers.py:23–44` returns the stated proposal reasons. It proves only
  that boundary, not host runtime behavior, as the corrected design correctly says.
- **Population falsifier:** no both-in-H rule survives. The full accepted-deal law is correct
  before exclusions; its preservation after exclusions remains unestablished. R002-R01-02
  supplies the specific failing inference rather than inferring a defect from missing tests.
- **Estimand falsifier:** fixed weights and bounded range are defined. Confidence level and
  numerical loss budget can properly wait for the explicitly frozen preregistration. The
  historical ruling's word “clusters” is quoted and then refined; its presence is not a defect.
- **Cost/partition falsifier:** no claim of measured cheapness or production monolithic T1
  survives. At s=4, per-hand root action values depend only on that hand's conditional villain
  distribution and fixed response policy. Singleton-hero `best_response` is the appropriate
  reference for those action values; the design confines this to T1/calibration, not T2.
- **Advisory corrections:** s=6's three hero histories, zero direction effect, marginalization,
  conservative row action, and identical ascending board order are adopted correctly. The
  dependency claim is incomplete as noted in A01.
- **Exercised cases/limits:** the claim honestly labels derivations as static and tests as
  future plans. No execution evidence is implied. A cost preflight with a stop condition is
  sufficient at this stage; measured cost and an actual stop threshold remain future gates.

## Requirement-to-evidence assessment

- **Frozen identity and scope:** PASS: ref, parent, tree and only two added documents match;
  raw-blob manifest independently recomputed.
- **Stage 0 and 0b structure:** Present: tier rationale, scope, ground truth, dependencies, stops,
  budget, mechanisms/invariants, hazards, alternatives, authority and limits. Material correctness
  is qualified by the findings above.
- **Host agreement/exclusions:** FAIL: reason labels corrected, direct provider separated, but v1
  decision/failure envelope accounting is incomplete.
- **s=4 root and prefix:** PASS, static: fixture replay and `_raise_bounds` give check or all-in
  raise-to 2; check terminates and a bet leaves only villain fold/call. One hero node.
- **s=6 history correction:** PASS, static: root; response after 2→4; response after 3→4. An opening
  4 is already all-in.
- **T1 partition and reference:** PASS at specification level: fixed villain, one independent root
  per h, 990 compatible villains; singleton sealed reference, tie sample and cost preflight
  required. No performance result established.
- **Calibration acquisition law:** PASS before execution exclusions: C(47,2)=1,081; C(45,2)=990;
  folder completions are constant after marginalization. Conditional on eight realized folder cards,
  C(37,2)=666.
- **Pairing/population after exclusions:** Pair integrity specified; full-population inference FAILS
  for outcome-dependent missingness.
- **Wire capacity:** PASS as plan: compact JSON `check/null` is three bytes longer than `raise/2`;
  probe before solving and final remeasurement. No measured fit is asserted.
- **Fixed strata and range:** PASS absent the missingness issue: four fixed equal weights, paired
  sum in [-4s,4s], uncertainty conditional on boards only.
- **Sample-size discipline:** A bounded Hoeffding rule is feasible in principle; numerical
  confidence/loss/variance plan is deferred until before holdout. Counts alone do not repair the
  identified bias.
- **Direction control:** PASS as plan: weak dominance, exact gap before run, zero permitted; a raw
  empirical sign is not the gate.
- **Boundary/controlled testing:** Plans include discriminating prefix and board controls, singleton
  teacher checks and host settlement reconciliation. Missing/failed real-envelope schedules need the
  correction above.
- **Frozen-input hygiene:** PASS: candidate LF-only, BOM-free, all lines ≤100 columns, no trailing
  whitespace; supplied base blob pins match.

For clarity, if X is the specified unit sum, its range width is 8s. For a single board with
n independent complete units, Hoeffding permits
`P(|mean(X)-E[X]| >= e) <= 2*exp(-2*n*e^2/(8*s)^2)`.
Thus `n >= (8*s)^2*log(2/alpha)/(2*e^2)` is one conservative per-board floor. A simultaneous
four-board construction can allocate alpha/4 to each board and average the interval endpoints;
other correctly derived stratified constructions are possible. This derivation confirms that
the stated range/strata mechanism is coherent, but applies to the target draws, not an
unjustified outcome-selected subset. No numerical budget or performance threshold is invented.

## Fresh verification record and limits

Read-only Git commands resolved `refs/heads/review/v0a-eval-panel-design/r002`, read the commit
object, and used `git diff-tree` against the exact base. Candidate tree:
`cf5c090f80ceeaf5118214e08e4362a0062b5f3c`. The parent is exactly the declared base. The only
differences are the two scoped added Markdown files.

Raw `git cat-file blob` stdout was captured as bytes with .NET streams, hashed with SHA-256,
and converted to complete digest/path rows, ordinal whole-row sorted, with LF endings:

- brief: `a34e5e0aa6591fe420010cf93dc2e7c08cd03a8bb504f93054a6b64bca8fbb86`
- design: `c0248683f2b204aa44ebb9dce3bde2cde9cdece95956b966d506448bc544e5d8`
- recomputed manifest: `8e5b22c22e4f7a7d4a0eff603ed256cc18a66351a329f27b011e6c52c8bbd9e2`

Packet `manifest.sha256`, workflow copy, controller rulings, and deferred coverage hashes all
match their stated values. The base workflow blob hashes to the same SHA-256 as the packet
copy. README, roadmap, four candidate base-table pins, and all 15 deferred dependency pins
were independently resolved and match. The formatting check found zero offending lines in
10,238 brief bytes and 28,360 design bytes. All substantive inspection commands completed
successfully. A `Get-Command python,git` availability probe found no PATH Python; it did not
invoke Python or block the byte checks, which used .NET and Git.

This is a Tier C Stage 0/0b specification review, not an implementation pass or test receipt.
The source-based schema counterexample and mathematical selection counterexample require no
prohibited runtime execution. Python 3.11.15/3.14.6 suites, real-boundary failure schedules,
source admission behavior, capacity and cost measurements, actual calibration and held-out
uncertainty remain future implementation/execution evidence. No production or packet input
was edited. The report and reviewer-authored ledger line were staged within the writable
workspace for coordinator delivery to the assigned immutable report path and task ledger.
