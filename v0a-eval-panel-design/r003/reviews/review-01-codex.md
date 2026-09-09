# Cold review 01: v0a-eval-panel-design/r003

Reviewer: Codex reviewer 01. Issued: 2026-09-08.
Scope: Tier C Stage 0 / Stage 0b specification review; FIX round.
Candidate: 18b7527a3989f7d38830a7881c976385fe9bc4de
Manifest SHA-256: 2664aca6f857999a4b45036b5cd3c250fbc3d8210b3132510d0e05a57e821975
Base: b378104cd2934f248a9545d7d482b0db25db813c
Tree: 26952b679cde91cc3c975500e2dd15a9270934ca
Ref: refs/heads/review/v0a-eval-panel-design/r003
Delivery target: reviews/review-01-codex.md

## Verdict

**CLEAN. No Critical or Important finding survives this specification review.**

**Design verdict: SOUND.** The design now separates hand success from decision agreement,
preserves completed prefix-diverged policy outcomes, and withholds the population claim
when any planned matched unit is missing. These are coherent corrections at the relevant
boundaries. Per-hand T1 and the fixed, equally weighted board strata remain appropriate to
the narrow declared game. No replacement of the design is indicated by this review.

This verdict establishes specification consistency against the frozen contracts. It does
not establish implemented correctness, empirical feasibility, test success or poker strength.
There is no implementation in the candidate and execution was expressly outside this review.

## Material findings

None. No source or candidate correction is required by this review.

## Cold-input order and verified identity

I read handoff.md first. I then read the candidate Git blobs and pinned governing inputs,
and recorded my own invariant and related-path inventory before opening coverage.md.
Only after that record existed did I read coverage.md and the permitted r002 disposition.
I did not read another r003 review, the task ledger, coordinator notes outside the handoff,
an implementer transcript, or sibling material.

Initial inventory: r003-review-01-inventory.md, SHA-256
f27d50c371c1500faf14d40dca924dd2519bef98e2075b437aa8388364895708.

The candidate resolves locally to the stated ref, has the stated tree and sole parent BASE,
and changes only the two named documents. Independent raw `git cat-file blob` reads produced
the same whole-row-sorted LF manifest bytes and the stated manifest SHA-256. Candidate
documents are LF-only, BOM-free, have no trailing whitespace and do not exceed 100 columns.
The workflow capture matches its BASE blob and the pinned SHA-256. Controller-ruling and
coverage hashes match the handoff. All 21 coverage inventory blob IDs match BASE.

Candidate citations below refer to:

- brief.md: docs/architecture/v0a-eval-panel-r001/brief.md at the candidate commit.
- design.md: docs/architecture/v0a-eval-panel-r001/design.md at the candidate commit.

Every other source citation refers to the full BASE commit above. Scratch copies were
extracted from those Git blobs, not from mutable source working files.

## Outcome classifier: r002 correction verified

Design mechanism 5, lines 160-197, is consistent with the frozen successful-session contract.
The actual session wrapper is `hands[i].result`: its initial status is failed, and the
completed result is constructed only after the consumer finishes and cleanup succeeds
(`tools/v0a_table_session.py:240-315`). This supplies the outer failure-first boundary.

The decisive paths are:

- **Rejected or ambiguous publication before a decision:** `src/pontius/v0a/runtime.py:1233-1265`
  raises with REJECTED/UNKNOWN. `_from_failure` at 1345-1365 emits the failure envelope.
- **Separate nullable payloads:** `tools/v0a_event_adapter.py:243-247` serializes decision and
  failure independently. `src/pontius/v0a/trace.py:216-252` keeps their shapes distinct.
- **Failed event with no decision:** `tools/v0a_table_host.py:671-678` and 844-854 validate failure
  and raise child_failed. No river record is required.
- **Accepted action followed by timing failure:** `tools/v0a_table_host.py:689-706`, 800-815 and
  844-854 reject invalid successful timing or a later failed event.
- **Incomplete hand or failed closure:** `tools/v0a_table_host.py:886-912` requires complete
  settlement, complete accounting, no interruptions, and successful final closure.
- **Protocol, cleanup or transport failure:** `tools/v0a_table_session.py:283-315` retains failure
  and does not promote the hand to completed.
- **Truncated retained output:** `tools/v0a_table_host.py:512-537` caps stdout at 2,097,152 bytes
  and records truncation/failure; session lines 293-301 retain and reject it.

The v1 `DecisionRecord` indeed has no delivery field (`src/pontius/v0a/model.py:445-461`);
`FailureRecord` has delivery status and nullable timing at 492-518. The revised classifier
does not require the invented field that invalidated r002. Its exact-one-river-record
predicate is appropriate after successful completion for the declared s=4 blueprint path.

The host validates the applied action and state/card/policy identities, but its v1 expected
dictionary contains no lookup reason (`tools/v0a_table_host.py:817-843`). Runtime sets the
provider to None for blueprint-v1 at `src/pontius/v0a/runtime.py:363`. Its v1 reason follows
the lookup's hit flag at 1298-1302. Accordingly, the planned independent replay and
`PreparedBlueprint.action_for` check is necessary, including a teacher check-hand where
hit and default have identical applied actions. The lookup's actual key and flag construction
are at `src/pontius/blueprint_preparation/lookup.py:51-68`.

The separate direct provider check is correctly limited to its own boundary:
`src/pontius/decision_provider/providers.py:23-44` emits blueprint_hit/blueprint_default.
It cannot substitute for the v1 host/runtime observation, and the design no longer says it can.

## Missingness, divergence and arithmetic: r002 correction verified

Design mechanisms 7 and 9 explicitly retain completed prefix-diverged outcomes for chip
comparison and exclude them only from agreement. This is necessary because the baseline's
premium-card predicate can raise preflop (`src/pontius/decision_provider/providers.py:66-85`).
A completed baseline hand with no target river decision remains a chip observation; only
the hand-outcome portion of mechanism 5 governs chip eligibility. Applying its later
agreement-only river-count predicate to chip comparisons would contradict mechanism 7.

The exact net-chip extraction is sound: the host publishes final stacks at
`tools/v0a_table_host.py:304-308`, while the kernel defines net returns and final stacks at
`src/pontius/no_limit_betting.py:735-744`. With only the two live seats contributing, a hero
orientation payoff is within [-s,s]. A two-policy difference is within [-2s,2s], and the
sum of both orientation differences is within [-4s,4s]. The Hoeffding range width is thus
8s, matching design mechanism 9. Splitting alpha across four boards and using fixed 1/4
weights supports simultaneous per-board coverage and a conservative pooled interval.

The equations `2*m_P,B` and `2*(m_A,B-m_C,B)` consistently distinguish orientation means
from matched-unit totals. Equal board weights apply to exact controls as well as estimates.
The single-board result remains conditional on that board, with no sampled-board inference.

Independent static counterexample: let s=4, alpha=0.05 split over four boards and epsilon=1.
The stated planned-unit floor is 2,599. In a planned sample of 10,000 units, let 9,000 observed
differences be zero and 1,000 missing differences be +8. Survivors exceed that floor; their
mean is zero, while the complete planned-sample mean is 0.8. A survivor Hoeffding radius
using these numbers is about 0.5373. Replacing each missing value by -16/+16 gives bounds
[-1.6,1.6] over the planned denominator. The design requires withholding the board and pooled
claims despite the survivor count. It therefore rejects the survivor substitution that
made r002 unsound. This is arithmetic, not an executed runtime schedule or sampling result.

The reported completion bounds bound the missing completed sample values. They do not by
themselves remove sampling uncertainty about the population mean. The design's unconditional
claim is withheld, so this distinction does not create a surviving acceptance defect.
Completion-based restoration must retain the original sampled units, policies and plan;
substitution of new successful deals would not satisfy the stated rerun condition.

## Earlier corrections and whole-candidate requirements

- **T1 and oracle:** Preserved. Fixed villain makes per-hero evaluation separable at s=4. Sealed
  singleton best_response remains the reference; T2 stays deferred.
- **Static s=4:** Preserved. Kernel `_raise_bounds` at `src/pontius/no_limit_betting.py:392-422`
  gives [2,2] at the declared root. Hero then has no further action after betting.
- **Teacher tie order and settlement:** `src/pontius/legal_river_continuation.py:44-66` lists check
  before raises; `src/pontius/evaluation.py:257-273` selects first maximizing action. Continuation
  returns use kernel settlement at 288-307.
- **Ground truth limitation:** Brief expressly states that teacher agreement tests export, not
  teacher quality. New per-hand code has a separate sealed-game comparison and cost preflight.
- **Exact key:** `src/pontius/immutable_blueprint.py:27-102` includes cards, board order, stacks and
  complete history. Spine digest at `src/pontius/legal_decision_spine_v2.py:28-70` binds public
  state.
- **Wire capacity:** Codec action shape at `src/pontius/blueprint_artifact/codec.py:187-204` makes
  check/null three bytes longer than raise/2; encoder at 280-285 is deterministic compact JSON.
  Final remeasurement remains required.
- **Collision-only acquisition:** Dealer shuffle and private-card assignment at
  `tools/v0a_seeded_deals.py:33-65` support the declared model. Compatible folder completions are
  symmetric for every accepted ordered hero/villain pair.
- **Board/card handling:** `src/pontius/holdem_cards.py:54-84` preserves board order and rejects
  overlaps. Declared ascending composition matches the teacher's sorted board.
- **Root and one-hand sessions:** Opponent logic at `tools/v0a_table_host.py:213-225` is card-blind;
  session carry/rotation is explicit at `tools/v0a_table_session.py:328-329`.
- **Pairing and off-pool cells:** Every accepted draw supplies both orientations under all policies;
  off-pool default observations stay in calibration and chip comparisons.
- **Recording:** Parent run ownership is compatible with `src/pontius/execution.py:37-44`, 118-125:
  inherited children do not verify or record separate runs. Mechanism 10 requires one result and
  journal row.
- **Stage 0 and 0b:** Scope, tier, oracle limits, dependencies, budgets, stop rule, seams,
  alternatives, invariant locations and unresolved T2 choice are explicit and reviewable.

The expected-test plan covers discriminating negative cases: a perturbed prefix, a check-hand
hit versus default, off-pool swaps, zero/duplicate river records, rejected/unknown delivery,
later timing failure, truncation, divergence retention and correlated missingness. Those are
future verification obligations, not results established by the specification review.

## Coverage comparison and nonblocking implementation notes

The deferred claim now follows the data and inferential stages rather than merely naming
old findings. It covers the principal paths in my initial inventory, and the added trace and
spine surfaces repair the specific semantic omissions named in the r002 disposition. The
coverage inventory also includes river.py, which supplies card evaluation and normalization.

The 21 entries are not an exhaustive transitive dependency closure. My inventory additionally
identified clock and lifecycle contracts. Frozen inspection confirms runtime imports
v0a/clock.py and action_clock.py, and the recording stage directly depends on execution.py.
The spine also imports preparation_bank.py. Their BASE blobs are:

- src/pontius/v0a/clock.py: 32cdc99e2e8e6c074dd925410c39330fa413af18
- src/pontius/action_clock.py: 844643c5497b1bb18d5a9346dd35f77cf7aabb0a
- src/pontius/execution.py: c46cd0e8a7f88b8cfe564ed23fda19cbfba63d8b
- src/pontius/preparation_bank.py: 75c381fbcb7222db2db2e64339cafbdbee43fa91

Calling the 21 rows a direct semantic inventory, or extending the pins when those boundaries
are tested, would be more precise than claiming complete closure. I found no concrete
unclassified failure caused by these omissions: frozen outer failure handling covers the
emitted outcomes, and the whole-tree comparison protects all unchanged source bytes.
This is a coverage limitation, not a material product finding.

Three details should be kept explicit when implementing the already required plan:

1. Read `hands[i].result`, not the ordinal/button wrapper, for session outcome fields.
   Keep agreement-only river-record diagnostics separate from chip eligibility.
2. A recorded seed supplies only hand indices 0 through 15 in the sealed helper
   (`tools/v0a_seeded_deals.py:58-60`). The preregistration must supply enough recorded seeds
   for the planned sample and collision rejection; repeated triples remain separate draws.
3. Label the missing-unit completion bounds separately from population confidence intervals.
   Do not replace failed units with newly sampled survivors when restoring the original plan.

These are consequences of existing requirements, not new gates or requested source edits.

## Verification scope and operational record

Executed only native Git reads, raw-byte SHA-256/format comparisons, source searches and
plain arithmetic in PowerShell. Hashing used raw Git stdout bytes, whole-row ordinal sort
and LF rows. All final identity checks succeeded. The initial handoff-repository lookup
had no candidate object; the evidence repository at D:/Pontius supplied the frozen objects.
A Python interpreter launch was denied by the sandbox and its escalation was aborted;
native PowerShell completed the hashing check, leaving no verification gap.

No runtime, solver, host, historical owner or test was invoked. No fetch, commit, push,
candidate edit or source edit occurred. No runtime acceptance verdict is implied.
The controller's explicit request authorizes this r003 review round only; it does not
resolve the general budget interpretation or authorize implementation or integration.
