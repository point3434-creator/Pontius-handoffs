# Cold review 02 (Claude): v0a-eval-panel-impl/r002

Candidate: refs/heads/review/v0a-eval-panel-impl/r002 at
b13709ffddbf3000e019641fd123239a24f2cd75, manifest
98df5d549736200115732bc2a49f8cc1d3e9ec5e61c7083d710b8af87b1f0822, base
46f45298a405b967976413a4b8e45e7837602316, tree a29d1db3f4c03b8d9c19edb02cfa93af4b0fb7e7.
Round kind: FIX (I-01 numerical reference acceptance). Tier C, Stage 0/0b.
Reviewer: Claude, second independent cold pass. Issued 2026-09-09.

**Defect verdict: CLEAN.** No Critical or Important finding survives frozen-source
verification. One Minor finding (M-01) and seven advisories are recorded below; none
is a required correction for this manifest.
**Design verdict: SOUND.** Reasons in section 9.

All findings bind to the manifest above. Method: Git-blob inspection of the candidate and
of base 46f45298, exact rational arithmetic, and native float arithmetic labeled as
reviewer arithmetic. No runtime, solver, host, test suite, source tool or candidate edit
was executed. Line numbers cite base blobs (git cat-file blob 46f45298:<path>).

## 0. Cold-input disclosures

Two sequencing deviations from the handoff occurred and are stated so the controller
can weigh this pass:

1. coverage.md and checks/author-*.json were opened in my second tool call, before my
   independent inventory was recorded. The inventory at checks/review-02-inventory.md
   (SHA-256 b25ab5a0334cee8a5e7ec9e767fe06eaf7df5e3064c275bc646a0620e8fd6a9b, recorded
   2026-09-09T04:46:01Z) was built from frozen source, but it was not built blind to
   the author's stage table. Section 6 marks which of my members could have been primed.
2. After my analysis and verdict were formed, I read the last three lines of the task
   ledger to copy its line format; that exposed the verdict line of the concurrent
   Codex cold review of this round. I did not open reviews/review-01-codex.md,
   checks/review-01-inventory.md, any r001 review, addendum or check, or chat history.
   The handoffs repository's commit titles were also seen while checking its state.

Nothing in sections 1-9 changed after either exposure. One observation (M-01) uses a
commit title from the handoffs repository and a controller ruling I recall from
outside this packet; it is labeled as such and is not offered as a manifest-bound
defect.

## 1. Identity recomputation (checklist item 11)

| Check | Result |
|---|---|
| ref -> commit | b13709ff (matches candidate.json) |
| commit parent / tree | 46f45298 / a29d1db3 (match) |
| base..candidate diff-tree | exactly two added paths, the brief and design |
| manifest from blobs, whole-row byte sort, LF | 98df5d54... (matches handoff, candidate.json) |
| manifest.sha256 file bytes | hash equals the digest; LF rows; sorted |
| prior anchor e39d3b93 manifest | 4f16c97f... (matches coverage.md) |
| six pinned inputs | all SHA-256 pins match; inputs/workflow.md == base docs/workflow.md |
| dependencies.json | 34 blob pins recompute at base, 0 mismatches |
| candidate text | LF, no BOM, no trailing whitespace, <= 100 columns |
| brief lines 14-18 | parent docs at base byte-identical to 18b7527a; its manifest is 2664aca6... |

Base 46f45298 is a child of master b378104c, not on master; the brief states this (lines
29-31).

## 2. Independent inventory (summary)

Invariant: every per-hand teacher decision and reference acceptance is a function of
exact integer settlement totals only; a rounded value or argmax may neither veto a
validated exact tie nor admit a wrong non-tie action; a wrong total must fail through
an independent exact check. Members by stage, from frozen source:

- Domain: no_limit_betting.py:357-422 (legal_decision, _raise_bounds), 424-557
  (apply_action), 588-613 (advance_street). At s=4 the replayed root has exactly
  (CHECK, raise_to(2)); after the raise the villain has (FOLD, CALL); terminals are
  +/-2 (check line), +/-4 (bet/call), +2 (bet/fold), 0 (tie).
- Sealed construction: legal_river_continuation.py:103-108 (raw weights summed in
  float), river.py:203-227 (total = sum of 990 exact 1.0 = 990.0; each weight rounded
  once as 1.0/990.0; deals sorted), legal_river_continuation.py:195 and 241
  (dict(self.game.deals) rebuilt per state).
- Policy: evaluation.py:15-36 (missing key -> uniform default at 22-25; explicit
  {CALL: 1.0} -> exact 1.0/0.0 at 30-36).
- Accumulation A: evaluation.py:54-66, chance loop values[index] += probability * value
  (line 65); player nodes walk zero-probability children (73-77) with exact 1.0/0.0
  factors.
- Accumulation B: evaluation.py:227-265, best_response continuation and action values
  via built-in sum() and max(); returned value re-evaluated by expected_utilities (273).
- Integer validation and tie rule: caller-side, design section 3.
- Export: codec.py:187-204 (action wire object), 239-240 (entries sorted by key
  canonical bytes), 280-289 (encode_blueprint).
- Host path: v0a_table_session.py:204-231 (prepare; Path.cwd() at 207; artifact
  OwnedInput 1048576 at 213), 41-61 (Admission), 233-315 (play_hand);
  v0a_table_host.py:142-155 (Source -> begin_run inherited), 458-482 (child env with
  PONTIUS_RUN_CONTEXT at 474-475, cwd=source.repo at 479), 213-225 (opponent scripts),
  174-210 (TableInput), 951-952 (host artifact cap 1048576); execution.py:37-44
  (inherited root equality), 122-125 (inherited finish_run is a no-op).
- Records: v0a/model.py:445-461 (DecisionRecord: selection_reason, no delivery
  field), 492-499 (FailureRecord.delivery_status); v0a/runtime.py:1296-1302
  (selection_reason derived from table_hit), 363 (no provider in blueprint-v1);
  v0a_event_adapter.py:243-247, 278-285, 296-299 (event_result, hand_result,
  session_result frames); session hands[*].result nesting at v0a_table_session.py:252-254
  with capture_truncated at 296.
- Witnesses: v0a_seeded_deals.py:58-65 (index 0..15; twelve private cards; board
  deck[12:17]); holdem_cards.py:54-63 and 134-155 (board order preserved, never sorted).

## 3. The FIX against the prior disposition's four requirements

The deferred prior disposition asked for: (1) both fixed-action reference values from
expected_utilities, no invented best_response API; (2) a derived allowance covering
normalization, products and accumulation, and independent verification of both
production totals; (3) canonical CHECK at a validated exact tie, reference label
difference tolerated only when the reference values are indistinguishable within the
bound, never epsilon-widened ties; (4) all-zero control retained, a discriminating
cancellation control, a legal tie witness or a recorded domain limitation, labeled
arithmetic fixtures, wrong non-tie actions failing, correct ties not rejected.

Candidate design.md section 3 (lines 82-146) and brief criterion 2 (lines 101-109):

1. Lines 91-97: R_check and R_bet from expected_utilities with explicit deterministic
   hero policies and the explicit CALL villain; best_response retained separately for
   its value and map; "best_response exposes no per-action value table". Satisfied.
2. Lines 99-111 derive E = 2^-40 from the actual code path (one rounding of 1/n, exact
   power-of-two products, 990 sequential += roundings). Lines 117-119 require a unique
   lattice integer within E of each value and J_a == production_total_a. Lines 120-121:
   production cannot certify its own false tie. Satisfied; derivation verified in
   section 4.
3. Lines 124-129: unequal validated totals require exact action equality; equal totals
   require production/export CHECK and accept either reference label. Under the
   lattice, J_check == J_bet is equivalent to |R_check - R_bet| <= 2E, so the
   candidate's condition is the disposition's condition. No second tolerance is
   introduced (lines 115, 125). Satisfied.
4. Lines 136-146 and brief 105-107, 138-139: all-zero royal control retained; nonzero
   cancellation with both signs, false production tie, changed total and smallest
   lattice gap as labeled arithmetic fixtures; the legal tie witness is sought during
   an authorized full-H solve, absence stated only over a completed census, otherwise
   reported unverified. Satisfied as a specification; the witness itself is deferred
   (advisory A-03).

Advisories carried from r001: worker cwd is addressed at design 270-273 and verified
against v0a_table_session.py:207 and execution.py:41-43 (a mismatched root raises,
which Session.run retains as source_invalid); bank sizing at design 193-198;
coverage category and method in coverage.md; budgets at brief 166-169.

The tie rule does not reopen the accepted parent: the parent's mechanism 2 states
best_response "breaks exact ties by first legal-action order", which is CHECK, and
the candidate keeps CHECK as the exported action on every validated tie. Only the
acceptance predicate changed, exactly as the disposition requested.

## 4. Numerical acceptance, independently checked

Model verified against evaluation.py:54-66 and river.py:221-225: each deal weight is
p = fl(1/990) with |p - 1/990| <= u/990; each term p*v with v in {-4,-2,0,2,4} is exact;
the chance loop performs 989 rounded additions. Recursive-summation error is bounded
by gamma_989 * sum|p v| <= 4(1+u) gamma_989; the normalization contributes at most
4u. Total 4(u + (1+u) gamma_989), as the design states.

Reviewer arithmetic (exact rationals unless noted; not a test receipt):

| Claim | Result |
|---|---|
| 4(u+(1+u)gamma_989) < 4 gamma_1000 | true |
| 4 gamma_1000 < E = 2^-40 | true; margin factor 2.048 |
| 2E < 1/990 (lattice uniqueness) | true; 1980 < 2^40 |
| 4000*2^40 < 2^53-1000 (author check) | true |
| p*4.0 exact; p within u/990 of 1/990 | true (binary64) |
| sequential 495 x (-2p) then 495 x (+2p) | 3.122502256758253e-17; bet sum doubles; argmax BET |
| reversed order | -3.122502256758253e-17; argmax CHECK |
| lattice search on those floats | unique J = 0 for both actions |

The last three rows reproduce checks/author-arithmetic.json and the disposition's
illustration; they demonstrate the mechanism only, not a legal hand.

Predicate walk-through (design 113-134):

- Correct tie (W = L > 0): totals (0, 0), production CHECK; both floats validate to
  J = 0; production action maximizes; best_response value within E of 0; either
  reference label accepted. Not rejected.
- Wrong non-tie action with correct totals: "production's action maximizes" fails.
- Wrong total or false production tie: J_a == production_total_a fails.
- Reference misconfigured (missing villain entry -> uniform default): per-deal bet
  values become 1 + w/2, still on the lattice, so only the equality with production
  detects it; see A-01 for the coincidence class that escapes.
- NaN, inf, malformed map, changed root shape: refused (lines 87-89, 131-132).
- Shared enumeration bug producing 989 deals in both paths: values leave the /990
  lattice unless integer-valued, so the fixed n = 990 detects it in general.

Structural fact used in A-02: with the villain always calling, both lines showdown the
same cards, so J_bet = 2 * J_check for every hand (no_limit_betting.py settlement of
pots 4 and 8 with equal contributions). Hence an exact tie is exactly W = L with both
totals zero; T1 bets iff W > L.

## 5. Other sections against frozen source

- Section 2 capacity: the wire action object is {"kind","raise_to"} (codec.py:204),
  so check/null is three bytes longer than raise/2; entries are sorted by key
  canonical bytes and metadata is fixed, so wire length is strictly increasing in the
  nested prefix family. Row length varies by up to two bytes with the private-hand
  digits, which is why the boundary is specific to the frozen permutation, as the
  design says (lines 43-52). Both session (v0a_table_session.py:213) and host
  (v0a_table_host.py:952) cap the artifact at 1,048,576 bytes.
- Section 4 witnesses: deal_for_hand rotates seat assignment by index and never
  touches the declared board; SixSeatHoldemDeal and OneSeatCardState keep board order
  as given (holdem_cards.py:54-63, 79, 147-150), so ascending order must be enforced
  by the new code in both places, as lines 206-207 require.
- Section 5 records: DecisionRecord carries no delivery field (v0a/model.py:445-461);
  FailureRecord does (492-499); event_result carries nullable decision and failure
  (v0a_event_adapter.py:243-247); hands[*].result nesting and capture_truncated match
  v0a_table_session.py:252-254, 296.
- Section 6 ownership: the child adapter constructs Source(Path.cwd()) with the
  inherited context (v0a_event_adapter.py:49-52, 324) and never calls finish_run;
  the host launches it with cwd=source.repo and the context in its environment
  (v0a_table_host.py:474-479); finish_run on an inherited context returns without a
  journal row (execution.py:122-125). "Each Session still runs its own prepare" is
  accurate (v0a_table_session.py:204-231).
- Brief numbers: 1,081 = C(47,2); 990 = C(45,2); both boards ascend under the
  rank*4+suit encoding; the four development hands and 2c 3d avoid their boards.

## 6. coverage.md compared with the recorded inventory

Category, invariant and the eleven stages match my inventory at the stage level.
Members primed by the author table are possible for stages 1-9 (opened early); the
worker-root and witness members and every line citation above were traced from
source. Differences:

- coverage.md treats accumulation as one member (expected_utilities). My inventory
  separates best_response's built-in sum() selection path, whose only consumer is
  the advisory tie label; the design text does cover it (lines 107-109).
- coverage.md lacks the structural identity J_bet = 2 J_check and the explicit domain
  assertions (A-01, A-02) as falsifiers.
- The discovery method (symbol search in the documents and dependencies) reached the
  same members as structural tracing for this category; it would not by itself have
  found the identity above.
- Planned cases match mine; the stated limits (no execution, no legal witness, both
  interpreters unexecuted) are honest and correctly scoped.

## 7. Findings, severity-ordered

No Critical findings. No Important findings.

**M-01 (Minor; advisory until the controller confirms scope): two-interpreter wording
against a standing ruling.** brief.md:156-157 and design.md:110-111, 141-142, 312
require verification on Python 3.11.15 before 3.14.6 and "on both supported
interpreters". The handoffs repository records, at 00:13:55 -0400 on 2026-09-09, a
commit titled "Downgrade I-01 to Minor ... after 3.14-only ruling", ten minutes before
this candidate's freeze (00:23:57). The packet's inputs/controller-rulings.md (dated
2026-09-08) does not carry that ruling, so within the pinned inputs the text is
consistent; against the ruling it is stale. Unverified scenario: the code checkpoint's
self-report is obliged by design steps 1-3 and line 312 to run focused suites on
3.11.15, which the ruling forbids, producing conflicting Stage 5 obligations.
Smallest correction: replace the two-interpreter language with CPython 3.14.6 at the
next byte change; do not open a round for this alone. Evidence effect: none. The E
bound assumes only binary64 round-to-nearest on +, *, / and holds on either
interpreter; interpreter dependence of built-in sum() touches only the advisory
reference label.

Advisories (engineering guidance; not acceptance gates):

- **A-01 Explicit domain assertions for the singleton reference.** State as
  predicates: len(game.deals) == 990; every probability identical; the villain policy's
  key set equals collect_information_sets(game, 1); the hero key set has one member.
  Reason: n = 990 and "one rounding" are premises of E, and the value checks alone do
  not close every misconfiguration. Concrete escape: with the villain policy missing
  (uniform default), a hand with W - L = 495 yields reference J_bet = 990 + J_check =
  1980, equal to production's 4(W - L) = 1980, and every value and action predicate
  passes. The positive assertion costs one tree walk or 990 key constructions.
- **A-02 Structural identity as a falsifier.** Require J_bet == 2 * J_check on validated
  totals. It is exact for this game under the fixed-CALL villain, catches shared
  domain/policy errors, and shows the "smallest nonzero lattice gap" case (gap 1/n) is
  unreachable by a legal hand, so it stays a labeled fixture. It also makes the tie
  class explicit: W = L, both totals zero, matching lines 143-144.
- **A-03 Witness search timing.** The legal non-degenerate tie witness is deferred to
  the authorized full-H solve. Consider allowing a bounded, resource-limited scan
  inside the preflight (it needs only production's enumeration, no sealed game) so the
  sealed-reference tie check can be exercised on a real hand before a full pool is
  authorized. The current text is acceptable; its limits are stated (line 146).
- **A-04 Reference cost shape.** expected_utilities walks zero-probability children
  (evaluation.py:73-77), so each forced-action call is a full two-subtree walk with a
  990-entry dict rebuild per state (legal_river_continuation.py:195, 241);
  best_response adds a collection walk, per-action continuation walks and one more
  expected_utilities walk. The separate attribution requirement (lines 154-155)
  covers this; the full-H estimate should exclude the sample-only reference.
- **A-05 Per-session preparation overhead.** Each Session.prepare builds a new host
  Source, inserts the src path into sys.path again (v0a_table_host.py:146, 158) and
  re-reads and decodes the artifact (v0a_table_session.py:213, 218). Linear in |H|;
  a measurement matter, not correctness. The design describes it accurately.
- **A-06 Budget wording.** Brief 166-169 states r001 and r002 exhaust the two-round
  allowance; design step 3 says "Obtain two cold Tier C reviews". Add "after the
  reauthorization the brief names" to step 3 so the order cannot be read as
  self-authorizing. Step 7 already says checkpoints grant none.
- **A-07 Packet hygiene (controller).** inputs/controller-rulings.md omits a ruling
  recorded before the freeze. Future packets should pin every ruling in force at
  freeze so cold reviewers do not depend on memory or repository metadata for it.

## 8. Engineering guidance

Cause of I-01 (demonstrated by arithmetic, not by a legal hand): coupled residuals;
a residual e in the check sum becomes 2e in the bet sum under exact power-of-two
scaling, so on an exact tie the floating argmax follows the sign of e. The candidate's
technique, exact-rational lattice validation of both values with a derived bound and
a canonical tie action, is the right class: it validates through the real public
boundary (expected_utilities on the sealed game) and stops depending on the argmax at
the one place it is unreliable. Cheapest falsifying checks for the implementation:
the cancellation fixture in both orders (already planned), the A-02 identity, and the
A-01 domain assertions.

## 9. Design verdict: SOUND

The shape fits the contract. The sealed game, kernel and evaluator are unchanged; the
correction lives in the caller's acceptance rule; the rule is exact arithmetic with a
conservative derived bound (margin about 2x) and a lattice uniqueness argument; the
tie action equals the parent's stated first-action tie-break; failure paths refuse
rather than default. Nothing in this round invites the defect class to recur.

Evidence limits: no code exists; no legal tie witness; no interpreter executed; the
bound's premises were verified by reading evaluation.py, river.py and
legal_river_continuation.py at base, not by running them. The reference shares the
ranker and kernel with production, which the brief states plainly (lines 90-91).

## 10. What this review does not establish

No runtime, capacity, cost, agreement, strength or transfer claim. No verdict on the
concurrent Codex pass. No authorization of implementation, execution or commit.
