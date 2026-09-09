# Cold specification review — review-01 / Codex

Reviewer: independently dispatched Codex reviewer `review-01`.
Date: 2026-09-08. Round: `v0a-eval-panel-design/r001`, NEW-SURFACE, Tier C.

**Defect verdict: NOT CLEAN — four Important findings and one Minor finding.**
**Specification assessment: Fail. Engineering/design assessment: Partial.**
These assess a specification, not an implementation or an executed experiment.

## Binding identity and independence

- Candidate: `e1e1e357e71cce632aee2a9b50c62705595bf86a`.
- Ref: `refs/heads/review/v0a-eval-panel-design/r001`.
- Base and candidate parent: `b378104cd2934f248a9545d7d482b0db25db813c`.
- Tree: `bf0079d6f05da01df13108c347d840d429bc1d44`.
- Manifest SHA-256: `8798e05557bff9436ca3a057dc40a169f1b61c5e7d51379a288b5918b6d5ac5a`.

All findings below bind to that candidate and manifest. `C:path:Lx-Ly` means
lines in the candidate Git blob; `B:path:Lx-Ly` means lines in the base Git blob.
References are to those frozen objects, not working files.

I read the handoff, its permitted inputs, and candidate/base Git blobs. I did
not read another review, an implementer transcript, coordinator conclusions,
or earlier task conversation. I did not run a poker runtime, host, solver,
test, or historical owner. No candidate or old-project file was edited.

## Required findings, severity ordered

### R01-01 — Important: the declared host agreement oracle does not exist on the chosen runtime path

Confidence: high; established by frozen control flow and schemas.

Locations: `C:docs/architecture/v0a-eval-panel-r001/design.md:L14-L19`,
`L125-L132`, `L150-L155`, `L186-L188`, `L192-L196`.

The design requires the actual host running `blueprint-v1` to show
`blueprint_hit` / `blueprint_default` provider records. However:

- `B:src/pontius/v0a/runtime.py:L352-L370` explicitly sets `_provider = None`
  for `blueprint-v1`.
- `B:tools/v0a_table_session.py:L179-L182`, `L223-L237` select the v2 provider
  protocol only for `baseline-rules-v1`.
- `B:src/pontius/v0a/runtime.py:L1269-L1307` emits the ordinary `DecisionRecord`
  on the blueprint path, with `selection_reason = table_hit | passive_default`.
- `B:tools/v0a_table_host.py:L796-L814` validates that ordinary record. It has
  no `provider_outcome` or `proposal` field.
- Even on the provider path, `blueprint_hit` is a **proposal reason**, not a
  provider outcome: `B:src/pontius/decision_provider/model.py:L22-L28` and
  `B:src/pontius/decision_provider/codec.py:L63-L95`. The provider wire validator
  admits only `baseline-rules-v1` at `codec.py:L44-L48`.

Concrete failing scenario: a correct T1 table contains the hero's exact river
key, and an on-time `blueprint-v1` session reaches it. The actual host returns
`selection_reason = table_hit` with the correct action. Mechanism 5 requires
`blueprint_hit` and says any other label fails, so correct behavior cannot meet
the specified agreement gate. Similarly, blueprint-path clock failures are not
identified by the two v2 provider-selection labels named as Slice B's cutoff
exclusion. Looking only for those labels cannot establish the promised coverage
of clock-induced exclusions.

Violated requirements: brief criteria 1–2 and the real-host agreement boundary;
the protected outcome-oracle invariant; checklist items 1, 3 and 6.

Smallest correction: specify the existing v1 record fields as the host oracle,
including selected action, accepted settlement/delivery status and the v1
timing/failure fields. Give an exhaustive mapping of both actually supported
record types to hit, unsupported, disagreement and excluded failure. If proving
the `BlueprintProvider` API itself remains required, name a separate direct
provider check against the frozen teacher; do not say the current blueprint
host instantiates that provider. No provider label or codec change is necessary
to make this distinction.

### R01-02 — Important: the smaller-pool hand swap changes the calibration population

Confidence: high; conditional-probability contradiction with a concrete example.

Locations: `C:docs/architecture/v0a-eval-panel-r001/design.md:L72-L75`,
`L118-L123`, `L134-L160`, `L205-L209`;
`C:docs/architecture/v0a-eval-panel-r001/brief.md:L94-L106`.

The teacher's declared population is hero in H, villain uniform over all 990
compatible hands. Mechanism 7 also requires both hands to be in H so that both
orientations hit. For a proper subset H, an accepted private-card draw can have
h in H and v outside H. There is no declared way to satisfy all three rules:
keep collision-only rejection, keep both orientations in H, and retain the
teacher's 990-hand villain conditional distribution.

If such draws are filtered, write `d_H(h)` for the number of members of H
compatible with h. Then the retained hero probability is proportional to
`d_H(h)`, and villain is uniform over only those `d_H(h)` hands. A uniform
strength-blind choice of H does not make its realized compatibility degrees
equal. If draws are retained, the swapped orientation may be a passive default,
so it is not a second observation of the stated in-pool T1 policy.

Concrete failing scenario: board `2c 7d 9h Js Qc`; a permitted small pool is
`H = {AsAd, KhKd, AsAh}`. The first and third hands overlap; the middle hand is
compatible with both. Both-in-H filtering admits four ordered pairs and gives
hero probabilities `(1/4, 1/2, 1/4)`, whereas the stated hero-H/all-villain joint
range gives `(1/3, 1/3, 1/3)`. More strongly, all three hands have greater than
half showdown equity against the unrestricted compatible range on this
unpaired, non-flush board, so T1 bets all three against a caller. Each admitted
hand-swap pair then has equal and opposite net returns, making its mean zero.
The teacher's unrestricted-range pooled expectation is positive. A correct
panel therefore fails the proposed calibration simply because it evaluates a
different population. This is an analytic example, not an executed result.

Frozen evaluator evidence: `B:src/pontius/legal_river_continuation.py:L103-L108`
normalizes the supplied joint weights; `L231-L234` supplies exactly that chance
range; `L288-L307` uses net chip returns. `B:src/pontius/evaluation.py:L54-L66`,
`L83-L86` evaluates that supplied range without correcting selection bias.
`B:tools/v0a_seeded_deals.py:L50-L66` deals without replacement and does not
apply an H restriction.

Violated requirements: amended criteria 4–5, truthful calibration and the
protected outcome-oracle invariant. The accepted rulings did not authorize
an additional strength/population selection rule or assert both hands are in H.

Smallest correction: define one joint sampling and analysis distribution before
building. Either retain all accepted triples and their swaps, explicitly model
off-pool fallback in the policy and exact control, or define a separately
reported, properly normalized both-in-H conditional analysis. For the latter,
use its actual compatible-pair weights in the exact control and state the
changed population; retain the mandated collision-only acquisition accounting.
Apply eligibility to the entire matched unit across all policies and both
orientations. Document whether one excluded cell excludes that whole unit.

Conditioning only on the original hero being in H is not itself a defect:
with uniform accepted dealing and unrestricted villain, every h has 990
compatible villains and the teacher and panel can match. It is the additional
both-in-H requirement, plus unspecified swap eligibility/weighting, that breaks
this design.

### R01-03 — Important: the precision/stop rule lacks an estimand and a mechanism compatible with four board clusters

Confidence: high for the specification gap and mathematical failure mode.

Locations: `C:docs/architecture/v0a-eval-panel-r001/design.md:L167-L175`,
`L277-L280`; `C:docs/architecture/v0a-eval-panel-r001/brief.md:L103-L108`,
`L116-L119`, `L140-L142`.

The design says boards are the sampling clusters and that the required number
of deals follows directly from the bound s. It does not decide whether the
pooled target is the finite mean of four selected boards or a mean over a
population of boards, how boards enter that population, the pooled weights,
the interval construction, or how paired units and exclusions enter it.
Deferring numerical seeds and a loss budget is reasonable; deferring this
mechanism leaves the outcome oracle unspecified at Stage 0b.

Concrete failing scenario: the four board-specific policy effects differ.
Increase private-card deals on each board without limit. Their four estimated
means become exact, but uncertainty about a broader board population remains
based on four clusters. Increasing the number of deals does not provide more
independent board draws or force a board-population interval below an arbitrary
loss budget. For a finite four-board target the board means are fixed strata;
the uncertainty calculation is different, and requires declared weights and
within-board sampling assumptions. The current instruction can either promise
an unattainable precision or cause a feasible conditional panel to be killed
using the wrong variance model.

Violated requirements: criterion 6, criterion 7's honest inconclusive result,
the feasible-sample-size kill rule, and Stage 0b's requirement to state the
mechanism and everywhere its invariant holds. A warning that four-cluster
inference is weak does not choose an estimand or estimator.

Smallest correction: retain the accepted four boards, but specify the pooled
population, weights, pairing unit, interval method and confidence level, and
the loss-budget/sample-size rule. State which part of uncertainty additional
deals can reduce. If the target extends beyond those boards, identify the board
sampling frame and report any irreducible few-cluster limitation as such;
otherwise state the pooled result is conditional on the four declared boards.
Carry this same definition through calibration, per-board output, pooling,
exclusion handling, and preregistration. No runtime is needed to decide it.

### R01-04 — Important: the retained teacher traversal has quadratic range work, omitted from the feasibility design

Confidence: high for the operation-count bound; no elapsed-time claim is made.

Locations: `C:docs/architecture/v0a-eval-panel-r001/design.md:L77-L85`,
`L99-L112`, `L157-L160`, `L313-L316`;
`C:docs/architecture/v0a-eval-panel-r001/brief.md:L19-L24`, `L54-L59`.

The design chooses H primarily by wire capacity, calls both teachers exact in
seconds, and identifies a million deals per CFR iteration as the large-range
barrier. The frozen game does more than linear tree enumeration:

- `B:src/pontius/legal_river_continuation.py:L238-L248` constructs
  `dict(self.game.deals)` for every chance action membership check.
- The resulting state's constructor does it again at `L188-L197`, including
  on subsequent betting transitions.
- `B:src/pontius/evaluation.py:L187-L224` traverses every chance outcome for
  T1 collection; its final `expected_utilities` traversal at `L267-L273` repeats
  the range traversal. The exact calibration has the same issue.

Concrete failing scenario: full H gives `N = 1,081 * 990 = 1,070,190` joint
deals. Just constructing the N dealt states during the first traversal requires
at least `2*N*N = 2,290,613,272,200` dictionary-entry insertions, before the
additional hero/villain transitions, settlement work, and final evaluation.
A slightly smaller capacity-fitting H has the same quadratic structure. The
proposed monolithic retained-solver invocation therefore inherits a major
unaccounted cost; artifact fit does not establish teacher feasibility. T1 is
affected even if T2 is deferred. This is derived from source, not a benchmark.

Violated requirement/risk: the declared small feasible export bridge, measured
budget discipline, and the Stage 0b requirement to identify barriers to the
chosen mechanism. The protected teacher file is explicitly out of edit scope,
so an implementer cannot silently optimize it to make the claim true.

Smallest correction: remove the seconds claim and make bounded teacher
construction/evaluation cost an explicit preflight and stop condition, covering
T1 and calibration as well as T2. Decide a feasible exact evaluation mechanism
within the sealed-game constraint before authorizing a full-range solve. If
using decomposition in new caller code, specify how action values are
aggregated across hidden villain hands before choosing a best-response action;
independently solving each known deal would leak opponent cards and would not
preserve T1. Any need to modify the teacher remains outside this candidate's
authorized surface.

### R01-05 — Minor: one changed line exceeds checklist v1's 100-column bound

Confidence: high; checked from raw candidate blob bytes.

Location: `C:docs/architecture/v0a-eval-panel-r001/brief.md:L77`.
The line beginning “teacher's own policy for decision agreement” is 106
characters. Checklist v1 item 10 requires changed files to be at most 100
columns. Reflow the sentence without changing its meaning. Both candidate
files are LF-only, BOM-free and have no trailing whitespace.

## Separate required design verdict

**STRAINED.** A kernel-backed, single-decision river bridge can be a small and
useful integration instrument. The core game choice, pure primary teacher,
existing codec and explicit unsupported-state accounting fit that goal. The
current specification strains that shape by treating a non-instantiated
provider as its host oracle, combining incompatible calibration populations,
and promising a precision/feasibility story without the relevant mechanisms.
These problems require a bounded design correction, not a general tournament
framework or a wider codec. There is not sufficient evidence to recommend
replacing the whole lane.

## Independent claim and requirement assessment

| Claim / requirement | Frozen evidence and assessment |
| --- | --- |
| Every-deal prefix, omitted seats contribute zero | Supported for admitted deals with `s=4` and passive pre-river hero behavior. `B:tools/v0a_table_host.py:L213-L225` uses no cards. `B:src/pontius/no_limit_betting.py:L276-L304` posts only seats 1/2 and starts after seat 2; `L479-L505`, `L616-L636` preserve the stated fold/check order. The sequence is also present in the unexecuted test source at `B:tests/test_legal_river_continuation.py:L26-L55`. Contributions are `(0,2,2,0,0,0)`, live seats `(1,2)`, river pending `(2,)`, and eleven history records. It meets `B:src/pontius/legal_river_continuation.py:L110-L143`. It does not cover a prefix-diverging policy, invalid deal, or interrupted session. |
| `s=4`, one bet size and one hero decision | Supported by `B:src/pontius/no_limit_betting.py:L357-L422`, `L479-L529`. The root has current bet 0, minimum full bet 2 and maximum 2. Check ends the river; bet 2 leaves hero all-in, and villain can only fold/call. There is no later hero decision. The design can replace “to be confirmed” with this static derivation, without claiming a test run. |
| Counts 1,081 / 990 and marginal villain distribution | `choose(47,2)=1,081`; after hero removal, `choose(45,2)=990`. Under the intended uniform shuffled-deck sampling model, rejection of any of the twelve private cards colliding with B leaves equal completion counts for each compatible hero/villain pair. Integrating out eight folded cards preserves uniform villain marginal. Conditioning on the actual folded cards instead leaves only `choose(37,2)=666` possibilities. Thus “regardless of what the folders hold” is sound only as a marginalization claim, not conditional on their realized cards. The both-in-H filter is the separate defect in R01-02. |
| Three accepted amendments | All six rulings are faithfully recorded, including primary T1, `s=4`, placement and the explicitly deferred T2 rule. Fixed-board composition and matched hand swaps can preserve a narrowly scoped oracle; a conditional result does not establish general poker strength. Four boards and a few-cluster caveat do not supply the missing estimator. R01-02 and R01-03 concern implementation of the amendments, not a demand to reverse the rulings. |
| T1 purity and lossless representability | Supported: `B:src/pontius/evaluation.py:L252-L273` selects exactly one legal action per information set, with deterministic action-order tie handling. `B:src/pontius/blueprint_artifact/codec.py:L187-L204` represents that action. Purity says nothing about equilibrium quality; the brief correctly distinguishes this. Solver runtime cost is separate, R01-04. |
| Reachability enumeration for pure T1 | Well-founded: traverse all nonzero chance deals, all villain legal actions, and the chosen hero action. There is no circular definition because the frozen teacher is already a total selected-action map. At `s=4` every hero information set is a root hand in H, so root-only export is complete for this teacher. `B:src/pontius/legal_river_continuation.py:L267-L285` excludes villain private cards from hero's information key. Agreement need not sample every villain hand for action coverage, though the test plan should still distinguish full enumeration from sampled host checks. |
| Wire versus canonical capacity | The distinction is correct. `B:src/pontius/immutable_blueprint.py:L323-L342` canonicalizes entry key digests; `B:src/pontius/blueprint_artifact/codec.py:L232-L240`, `L280-L288` writes the expanded full key. The 1 MiB cap is in `B:tools/v0a_table_session.py:L212-L219` and `B:tools/v0a_table_host.py:L950-L953`, not the codec itself. `B:experiments/blueprint-performance.md:L27` confirms the retained 883/884 wire boundary as a historical report, not a fresh measurement. This review did not independently recalculate the historical 71,939 canonical bytes. |
| Capacity arithmetic and preflight | Eleven root history records and one entry per hero hand at `s=4` are supported. The approximately 1 KB estimate is an estimate, not established fit; the design correctly calls for measuring final wire bytes. A pre-solve placeholder must conservatively cover action and `source_id` lengths. Check/null is three wire bytes longer than raise/2 under the frozen compact JSON codec. Fix the placeholder convention and check actual final bytes. The `s=6` estimate is also rough: root plus responses to `2 -> 4` and `3 -> 4` gives three possible hero nodes, with policy reachability potentially reducing them; four is not an exact count. `s=6` is outside this round's acceptance. |
| Calibration against hit-conditional hero distribution | Sound if the analysis distribution is exactly uniform h in H and unrestricted compatible v and uses the same policy including any fallback. Not sound under the additional both-in-H swap requirement without reweighting/redefining the control; R01-02. |
| Freeze surfaces | Every Base-blobs table value matches. The table has four rows, but only three are declared byte-identical; `tests/cases.json` is expressly allowed to change. Entire base/candidate commits pin the runtime, kernel, key constructor, provider, host and dealer now, and the brief's positive edit allowlist excludes unlisted existing production modules. Therefore absent duplicate blob rows alone are not an identity breach or Critical finding. The review/coverage dependency list should nevertheless explicitly include `immutable_blueprint.py`, `no_limit_betting.py`, card-state projection, `v0a/runtime.py`, provider model/codec/selection, and both host/session routes. R01-01 demonstrates why checking only the four named surfaces is inadequate semantic discovery. |
| Stage 0 / Stage 0b fields | Tier, invariant, baseline, allowed/forbidden scope, seams, size budget, ground truth, dependencies, stop rule, review budget, forbidden claims and future test plan are present. Design goals, elements, risks, alternatives, rulings, coverage category, project ties, barriers and exclusions are present. T2's open rule is explicitly authorized as deferred. The material failure is that several mechanisms/invariants remain internally inconsistent or undecided (findings above), not missing section headings. FIX coverage planning does not apply to this NEW-SURFACE round. |
| Workflow execution rules | The specification states boundary-only admission, one journal record, fresh seed separation, preregistration, raw evidence, and Python/environment requirements. No execution or implementation evidence exists in the candidate; future isolated checks, module resolution, process environment, native ownership and fault coverage remain unverified. |

## Advisory clarifications, separate from required findings

- The strongest guaranteed direction control is T1 weakly dominating a compared
  deterministic policy under the *same* exact distribution and passive villain.
  Strict improvement is not guaranteed: e.g. a royal flush on the board ties
  every deal and gives zero difference. Specify the exact expected gap and
  finite-sample decision rule; do not turn an unqualified positive-sign check
  into an acceptance gate. This also applies after determinizing T2.
- Calling this the project's outcome oracle should remain scoped to this
  instrument's stated game and population. Card-independent folders make this
  a useful control for bunching, not a discriminating general bunching study.
  The brief's forbidden claims mostly supply this limitation already.
- “No artifact can cover randomly dealt boards” is too absolute; a finite exact
  table can hit particular random boards with small nonzero probability. The
  practical capacity reason for using declared boards is sufficient.

## Identity receipts and commands performed

All substantive source reads used `git -c safe.directory=D:/Pontius -C D:/Pontius`
with `rev-parse`, `diff`, `ls-tree`, `cat-file blob` or read-only `grep`. These
were object inspection commands, not project execution. A first unquoted
PowerShell `^{tree}` expression failed to parse; the quoted retry returned the
tree listed above. An attempted generic Python hash script did not start
because `python` was unavailable. Hash verification was then completed using
PowerShell/.NET raw stdout streams and SHA-256, without importing project code.

Fresh direct identity results:

| Item | Result |
| --- | --- |
| Candidate ref, tree and parent/base | Exact match to handoff and candidate.json |
| Changed paths | Exactly `docs/architecture/v0a-eval-panel-r001/brief.md` and `design.md`, both additions; no other diff |
| Brief blob | `5d9e780` abbreviated object ID; raw length 9,154 bytes; file SHA-256 `7e3d586e3da6f01a34fc3cba0d21b660f1f844b187355e48b0f6f47d1deb4482` |
| Design blob | `b78e5c9` abbreviated object ID; raw length 20,345 bytes; file SHA-256 `5382e3a522d0f683050f696d213695173ae2329c44d84257d02435800d48474c` |
| Manifest recomputation | Frozen blob hashes, lowercase digest + two spaces + POSIX path + LF; whole-row ordinal byte-compatible sort; SHA-256 exactly `8798e05557bff9436ca3a057dc40a169f1b61c5e7d51379a288b5918b6d5ac5a`; row bytes equal packet manifest |
| README base blob | `99bc05dcfcbbf1786e1ea2e70bfbb1894b68151f` |
| Workflow base blob | `503fd1701800710e344905589f3ccadbd002b980`; packet workflow byte-identical, SHA-256 `c71e3963ff726e06158878bcc10dd7dd761b32597af1c8ed39e21ebf60b58a37` |
| Roadmap base blob | `08fb65f04459b9b485287ba9cadca60590de4570` |
| Controller rulings input | SHA-256 `2649ae254b3cd7692082920a2cc07d9b85dac2360cbcd71d375d0faa56a6ebd6`, exact match |
| Base `tests/cases.json` | `53497f56ab0ac4b05c4dba7ca21e022f5bf62813`, exact match |
| Base legal continuation | `dc82aa748a195391143a09958e4e0dade827c45b`, exact match |
| Base blueprint codec | `c8a21b91cc4d285ff6e82b1f1b187c4e178bb5ce`, exact match |
| Base seeded dealer | `2963004e38c6e66f76ae9ce3bd474063eee870fe`, exact match |

No test result, runtime measurement, solver output, or new poker evidence is
claimed. Historical numerical statements were treated as source assertions
unless independently covered above. The only created file is this attributed
review report, for coordinator publication in the round packet.
