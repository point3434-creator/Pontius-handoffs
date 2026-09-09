# Cold specification review — review-02

Reviewer: Codex independent cold reviewer, assignment `/root/review_02`.
Issued: 2026-09-08.
Packet: `v0a-eval-panel-design/r001`, NEW-SURFACE, Tier C specification review.
Candidate: `e1e1e357e71cce632aee2a9b50c62705595bf86a`.
Manifest SHA-256: `8798e05557bff9436ca3a057dc40a169f1b61c5e7d51379a288b5918b6d5ac5a`.
Base: `b378104cd2934f248a9545d7d482b0db25db813c`.

**Defect verdict: NOT CLEAN.** Three Important specification findings remain.
No Critical identity or blob-pin finding was found. These are findings against
the frozen design, not claims that an implementation or test failed.

**Required design verdict: STRAINED.** The kernel-backed river bridge is a useful,
bounded shape, and the accepted tiny-stack choice makes the action mapping simple.
However, the proposed observation mechanism assumes a provider path the selected
host mode does not execute; the capacity-dependent pool is inconsistent with the
pairing population; and the proposed solve overlooks a large cost in the sealed
teacher state. Correct the boundary and population contracts before implementation.
These defects do not require replacing the betting kernel or widening the codec.

All candidate references below mean Git blobs at the full candidate commit above;
all BASE references mean Git blobs at the full base commit above. Line numbers
refer to decoded frozen blobs, not the mutable worktrees. Every finding binds to
the candidate and manifest pair at the top of this report.

## Important findings, ordered by impact

### R02-01 — The declared host mode cannot produce the provider records required for agreement

Severity: **Important**. Confidence: **high**, directly established by source
control flow.

Frozen candidate locations:

- `docs/architecture/v0a-eval-panel-r001/design.md:14-19`, especially the claim
  that the selected host records `blueprint_hit` and `blueprint_default`.
- `docs/architecture/v0a-eval-panel-r001/design.md:125-132`, which makes those
  labels mandatory and any other label a failure.
- `docs/architecture/v0a-eval-panel-r001/design.md:150-155,186-188`, selecting
  provider-specific cutoff labels while fixing play to `blueprint-v1`.
- `docs/architecture/v0a-eval-panel-r001/brief.md:19-26,85-89`, requiring the
  existing provider's decisions and separately reported fallback outcomes.

BASE evidence:

- `src/pontius/v0a/runtime.py:363-370` assigns `_provider = None` for
  `strategy == "blueprint-v1"`; `make_provider` is used for the other strategy.
- `tools/v0a_event_adapter.py:319-339` selects protocol v1, no provider identity,
  no provider source manifest, and the ordinary trace codec for `blueprint-v1`.
- `tools/v0a_table_host.py:937-941,961-971` makes the same baseline-only distinction.
- `tools/v0a_table_host.py:760-815` accepts provider decision records only when
  an identity exists; otherwise it validates the ordinary `DecisionRecord` fields.
- `tools/v0a_table_session.py:179-182,223-226,259-263` preserves this distinction.
- `src/pontius/decision_provider/providers.py:38-44` does define
  `blueprint_hit`/`blueprint_default`, but that class is bypassed by this mode.

Concrete failing scenario: take any valid board, an in-pool hero hand, a compatible
villain hand, the stated `s=4` prefix, and a correctly encoded CHECK or RAISE entry.
The specified worker invokes the existing host/session with `blueprint-v1`.
The runtime can select the entry and report an ordinary `table_hit`; it cannot
emit the provider proposal required at design line 127. The agreement run therefore
rejects a correct artifact, or an implementer silently substitutes labels and
claims to have tested `BlueprintProvider` although that path never executed.
The provider-specific cutoff exclusion likewise does not cover the selected v1
path's actual timing/failure representation.

Smallest correction: distinguish the runtime blueprint path from the provider
class in the design. Use actual v1 hit/default and timing records for host
integration, and separately drive the existing `BlueprintProvider` public boundary
if provider agreement remains required. Specify the observations for both paths
and their actual cutoff/failure categories. Alternatively, an actual provider-mode
host integration needs an explicit scope change; merely relabeling v1 records
does not establish it. No new provider name or codec version is needed to correct
the specification.

Required future verification: an in-pool hit, an off-pool miss, and a real selected
mode's cutoff/failure record must cross the actual chosen boundary; the coverage
record must identify which case proves runtime behavior and which proves provider
behavior. Do not infer execution of one from the other.

### R02-02 — A restricted H makes the required duplicate and calibration population inconsistent

Severity: **Important**. Confidence: **high**, from incompatible requirements and
finite conditional-probability arithmetic.

Frozen candidate locations:

- `docs/architecture/v0a-eval-panel-r001/design.md:72-75`: villain uniform over
  all 990 board/hero-compatible hands.
- `docs/architecture/v0a-eval-panel-r001/design.md:118-123`: capacity may select
  a proper subset H, by a strength-blind rule.
- `docs/architecture/v0a-eval-panel-r001/design.md:134-150`: collision-only
  rejection, then a swapped triple with both hands in H.
- `docs/architecture/v0a-eval-panel-r001/design.md:157-165`: calibration against
  the same teacher joint range and a claimed direction control.
- `docs/architecture/v0a-eval-panel-r001/brief.md:94-106`: collision-only
  rejection and the played hand-swap, as accepted by controller rulings 1-3.

BASE evidence:

- `tools/v0a_seeded_deals.py:49-65` deals all six private hands from a shuffled
  deck; it does not constrain either active hand to H.
- `src/pontius/immutable_blueprint.py:355-368` makes an off-table hero hand a
  passive default, not a teacher decision.
- `src/pontius/river.py:203-226` normalizes precisely the supplied joint weights.
- `src/pontius/evaluation.py:54-66,83-86` evaluates precisely that chance law;
  it does not discover or apply the panel's later inclusion rule.

Concrete failing scenario: capacity chooses a proper H. An admissible dealer
output has `h in H`, `v not in H`, and all twelve private cards disjoint from B.
The original triple has a teacher hit. Its required `(v,h,B)` duplicate has an
off-pool hero and a passive default, contradicting "both hands being in H".
Rejecting the original or dropping the duplicate introduces an extra selection
rule beyond the stated collision-only rule. Playing it is possible, but is then
a different, partly-default policy comparison from the all-in-pool duplicate
described by the design. No disposition of this ordinary supported input is
specified coherently.

Conditioning both hands into H does not repair calibration automatically. Put
`C(h) = {v: v is compatible with B and h}` and `m(h) = |H intersect C(h)|`.
The stated teacher law has
`P(v | h,B) = 1/990` for every `v in C(h)`.
An all-in-pool pair population instead has
`P(v | h,B,h in H,v in H) = 1/m(h)` on `H intersect C(h)` and zero elsewhere.
It also weights hero h proportionally to m(h) when sampling ordinary deals and
retaining both-in-pool pairs. A seeded uniform selection of H does not undo these
conditional laws after the realized H is frozen.

For an elementary concrete compatibility example, let a board exclude card IDs
0 through 5 and let a small H contain hands `{0,1}`, `{2,3}`, `{2,4}`, `{0,5}`.
Their compatible partner counts within H are respectively 2, 2, 2, and 2 in this
particular example, but every included h still has only two allowed villain hands
instead of 990. Even equal degrees therefore do not restore the declared villain
law. For unequal hero weights, use H = `{0,1}`, `{2,3}`, `{0,4}`: compatible
partner counts are 1, 2, 1, so the accepted hero weights are 1/4, 1/2, 1/4 rather
than 1/3 each. These small-pool cases are also directly relevant to the proposed
calibration test at design lines 205-209.

The oracle can consequently reject correct settlement arithmetic or validate the
wrong population. An exact best response under one range is not necessarily a
best response under the other, so the downstream sign control also loses its
stated justification.

Smallest correction: specify one inclusion/weighting law for original and swapped
cells, including every off-pool case, and derive the calibration law from it.
A straightforward option is to play every valid original and swap, record hits
and defaults separately, and calibrate the complete deployed policy including
defaults with the exact same weights. A both-in-pool analysis requires explicitly
declaring that analysis population, preserving the required played observations,
and normalizing the oracle on precisely the admitted ordered pairs. The full
teacher range and a separately conditioned analysis range must not share an
unqualified "same joint range" label. Any departure from the accepted criteria
needs an explicit new ruling, rather than an implicit filter.

Required future verification: include a valid `h in H, v not in H` original/swap,
and an unequal-degree small H. Derive the expected weights independently and
verify all observations, exclusions, normalization, and paired contributions.

### R02-03 — The planned full-range solve overlooks quadratic range validation in the sealed game

Severity: **Important**. Confidence: **high** for the structural cost; elapsed
time and memory limits are **unmeasured**, not claimed as observed failures.

Frozen candidate locations:

- `docs/architecture/v0a-eval-panel-r001/design.md:77-85`: capacity selects H
  and the resulting teachers are claimed exact "in seconds".
- `docs/architecture/v0a-eval-panel-r001/design.md:99-112`: retained
  `evaluation.best_response` and a walk of every joint-range deal.
- `docs/architecture/v0a-eval-panel-r001/design.md:313-316`: recognizes a
  million-deal concern for T2 but leaves T1 feasible by assumption.
- `docs/architecture/v0a-eval-panel-r001/brief.md:54-59`: the teacher game is
  sealed, so an unmentioned optimization there is unavailable.

BASE evidence:

- `src/pontius/legal_river_continuation.py:194-197` constructs
  `dict(self.game.deals)` for every dealt state validation.
- The same file at `241-248` constructs the whole dictionary again to admit each
  chance action, then constructs a dealt state which performs the first check.
- At `249-264`, ordinary action transitions also create fresh validated states.
- `src/pontius/evaluation.py:187-224` collects every chance outcome and all
  target-player actions; `211-213` retains those states for best response.
- `src/pontius/evaluation.py:257-273` then evaluates continuations and performs
  a final exact full-tree evaluation. Zero-probability actions are still walked
  by `expected_utilities_from_state` at `74-77`.

Concrete failing design scenario: the first capacity measurement permits near
full H, as the design expects, and implementation puts the declared uniform
range into one `LegalHeadsUpRiverContinuation`. At full H the number of ordered
deals is `N = 1081 * 990 = 1,070,190`. Merely admitting the N initial chance
children builds two dictionaries containing N rows each: at least
`2*N*N = 2,290,613,272,200` row insertions before counting their continuations,
repeated traversals, invariant checks, ranking, or retained states. The constant
number of hero decision nodes does not make this a small execution. A capacity
fit therefore sends the mandatory T1 path into an enormous unbudgeted operation,
while the stated feasibility barrier and deferral discuss T2 only.

This is a static lower-bound calculation, not a benchmark or proof of a specific
number of elapsed seconds. It establishes that the actual mechanism has a major
cost absent from the stated solve model, so the unqualified "in seconds" claim
and capacity-only selection of the working range are not justified.

Smallest correction: add an explicit feasible solve construction and bounded
cost-calibration/stop plan for T1 as well as T2 before choosing the executable
population. At s=4 each hero information set is independent given its declared
conditional villain law, so partitioning the exact calculation into separately
weighted hero problems is a possible bounded approach that can preserve the
sealed game; it needs a stated aggregation and provenance invariant and its own
cost check. Alternatively, select a declared smaller solving population and
reconcile it with pairing and calibration. Do not silently edit the sealed class
or present a new evaluator as the retained teacher.

Required future verification: compare a partitioned result against the original
exact evaluator on a genuinely small joint range, then measure bounded scaling
under separate execution authority. No such execution was performed here.

## Independent claim and contract assessment

| Requirement or claim | Evidence and assessment |
| --- | --- |
| Candidate identity and two-file scope | Verified from Git objects and byte hashes; details below. |
| Every-deal prefix, four folders contribute zero | Supported at accepted s=4 for admitted deals and the declared passive pre-river policies. BASE `no_limit_betting.py:276-303` posts only seats 1/2 and orders seats 3,4,5,0,1,2. Host `select_opponent`, `tools/v0a_table_host.py:213-225`, folds a folder facing the blind and makes the SB call. The BB checks. `no_limit_betting.py:615-637` orders postflop seats 1 then 2; the continuation's exact entry checks are `legal_river_continuation.py:111-143`. This does not establish reachability for a pre-river-raising baseline; the design separately excludes it. |
| One legal bet, one hero decision at s=4 | Supported statically. At the river each live seat has two chips, pot four, current bet zero, last full raise two. BASE `no_limit_betting.py:392-421` gives raise bounds [2,2]. Root check finishes the round; after hero bets, hero has no chips and villain can only fold/call, after which the hand is terminal (`479-529`). `legal_river_continuation.py:44-63` enumerates those bounds. This is one hero information set per hand, though many underlying states differ in villain cards. |
| Villain uniform over 990 | Supported as the ordinary marginal before an H-on-villain inclusion rule: choose(47-2,2)=990. Marginalizing the eight folded cards leaves the same number of folded-card completions for every compatible h,v. Rejection of all private/board collisions is symmetric. Conditional on the actual eight known folder cards there would instead be choose(37,2)=666 hands; "regardless" must refer to marginalizing them, not conditioning on them. The sealed seeded generator is deterministic pseudorandom generation, not an exact mathematical uniformity proof over its finite seed space. R02-02 identifies the later selection that breaks the intended marginal. |
| Capacity representation | Correct to measure encoded wire bytes. BASE codec `280-285` encodes full entry/key documents; `immutable_blueprint.py:323-342` canonical source bytes carry key digests instead. Host `951-959` and session `212-219` impose 1,048,576 bytes on the raw artifact. The codec itself is not the source of that input cap. |
| Capacity arithmetic | At s=4 there is exactly one exported root key per h, so entry count is exactly |H|. choose(47,2)=1081 and eleven public actions in the declared prefix are correct. Near-cap wire size and the precise first overflow remain a future measurement. `s=6` has three distinct hero decision histories in the full continuation (root, response to 2→4, response to 3→4), so "roughly four" is not a kernel-derived exact count; s=6 is outside current acceptance. |
| Amended criterion 4 | The accepted fixed-board composition is coherent and preserves a scoped conditional oracle if all 12 private cards, including folders, are checked for collisions. BASE `holdem_cards.py:73-84` requires all 17 playable cards distinct. The amendment narrows population claims; it does not itself invalidate the measurement. |
| Amended criterion 5 | Identical triples and a hand-swap can be paired coherently at fixed seats. Seat rotation is unavailable for this particular fixed prefix, but this is a restriction of the chosen game construction, not a general requirement of `LegalHeadsUpRiverContinuation`, which accepts an arbitrary root/other live-seat mapping (`145-151`). R02-02 is the unresolved capacity-related violation. |
| Amended criterion 6 | Four declared boards with per-board and pooled reporting are an accepted narrow target, not evidence about an unspecified population of boards. Few-cluster caution is properly stated. The actual pooled weighting, interval, and sample-size calculation remain to be frozen; more deals cannot by itself create more independent board clusters. |
| T1 purity and lossless export | Supported for the selected s=4 game. BASE `evaluation.py:252-273` selects one legal action per information key, with `max` choosing the first action on exact ties, then constructs a degenerate distribution. A single-action codec loses no mass from that deterministic policy. Supply the declared passive villain explicitly; missing information keys default to uniform in `evaluation.py:22-25`. |
| Reachability definition | Well-founded for a frozen pure policy in this finite acyclic game: resolve chance, take the sole selected hero edge and all legal villain edges. At s=4 all root hero information sets are reached and no later hero information sets exist; one compatible villain representative suffices to exercise each identical key/action shape, though it does not exercise all settlements. No circular reachability defect found. |
| Calibration control | Exact evaluator and host settlement refer to the same net chips: BASE `legal_river_continuation.py:288-306`, `no_limit_betting.py:735-750`, host `304-308`. Host final-stack minus starting-stack is an independent extraction of the net value. The proposed calibration is invalid until the actual conditioning and weights are resolved (R02-02). |
| Hand-swap under restricted H | Not specified coherently; R02-02. |
| Frozen source dependencies | All files are pinned by the full BASE/candidate tree for this review, and the may-change list excludes edits to the other existing sources. Therefore no current unidentified-byte defect is demonstrated. The four-row table actually contains one allowed registration change and only three explicitly byte-identical files. It is not an exhaustive invariant inventory: the key constructor, betting kernel, card view, lookup/preparation, runtime, provider, event adapter, host/session and evaluator all matter. R02-01 demonstrates why inspecting only label sets is insufficient. Name these dependencies in the future coverage record and retain a whole-tree diff allowlist, or pin their exact bytes explicitly. |

## Additional non-blocking corrections and limits

- A largest-pool wire-byte check needs a declared ordering/seed, source_id
  length, and placeholder action rule, followed by a final-artifact size check.
  CHECK/null and RAISE/2 do not serialize to the same length (codec `187-204`).
  Use a conservative placeholder or reserve its variation; do not report the
  first overflow as universal over all tables. The design already requires an
  actual measurement, so I have not invented an observed overflow finding.
- Keep ordered board identity explicit. The teacher sorts its board
  (`legal_river_continuation.py:90-108`); table card views preserve board order
  (`holdem_cards.py:54-63,89-92`) and the key copies the view
  (`immutable_blueprint.py:85-101`). Export and sessions must use the same declared
  order, as the design's board-equality invariant requires.
- The direction control must derive its actual expected effect after T2
  determinization and population selection, allow an exact zero effect, and
  specify the statistical decision before holdout. A best response guarantees
  weak superiority in its own range, not a strictly positive effect against
  every control or a guaranteed observed sign in a finite sample. A board that
  itself is a royal flush is a simple all-zero showdown control. Respect brief
  criterion 7's inconclusive outcome rather than using sign alone as a mechanical
  correctness oracle.
- A per-hand outcome bound is useful for a fixed-board/fixed-board-set mean.
  It is not a complete cluster-inference or power calculation: specify the
  original/swap aggregate, policy difference, board weights, target population,
  confidence level and assumptions. Under genuine board-cluster inference the
  number of clusters is four even if every board receives many more deals.
- All Stage 0 substantive fields are present: tier/invariant, base/scope, numbered
  acceptance, seams, size, ground truth, dependencies, stop/budget, forbidden
  claims and test plan. FIX coverage planning is inapplicable to NEW-SURFACE.
  Stage 0b includes goals, mechanisms, invariants, places, hazards, alternatives,
  rulings, coverage category, ties, barriers and exclusions. Field presence is
  not substantive correctness; R02-01/R02-02 prevent acceptance of the central
  mechanisms. T2 determinization is explicitly open by the controller ruling,
  so leaving it open is not itself a missed decision.
- The practical track is supported by BASE `experiments/research-roadmap.md:121-142`.
  Its statement that it unlocks the scientific work should remain an ambition:
  a fixed board, card-blind folders, one-size policy cannot itself discriminate
  bunching or adaptive-menu improvements outside that restricted target. The
  limitations at design `211-214,329-333` are valuable and should constrain later
  family-summary claims.

## Identity, actions and evidence limits

Verified independently:

- Ref resolves to the candidate above; its parent is the BASE above; candidate
  tree is `bf0079d6f05da01df13108c347d840d429bc1d44`.
- `git diff-tree --no-commit-id --name-status -r BASE CANDIDATE` reports exactly
  the two additions declared in the packet.
- Raw `git cat-file blob CANDIDATE:path` bytes were hashed with SHA-256. Whole
  rows were byte-sorted and terminated with LF; the resulting manifest bytes
  exactly equal the packet manifest and hash to the digest above.
- Candidate `design.md` SHA-256:
  `5382e3a522d0f683050f696d213695173ae2329c44d84257d02435800d48474c`.
- Candidate `brief.md` SHA-256:
  `7e3d586e3da6f01a34fc3cba0d21b660f1f844b187355e48b0f6f47d1deb4482`.
- BASE README blob `99bc05dcfcbbf1786e1ea2e70bfbb1894b68151f`, workflow blob
  `503fd1701800710e344905589f3ccadbd002b980`, and roadmap blob
  `08fb65f04459b9b485287ba9cadca60590de4570` match handoff pins.
- Packet workflow copy is byte-identical to BASE and hashes to
  `c71e3963ff726e06158878bcc10dd7dd761b32597af1c8ed39e21ebf60b58a37`.
- Controller rulings hash to
  `2649ae254b3cd7692082920a2cc07d9b85dac2360cbcd71d375d0faa56a6ebd6`.
- All four design base-blob rows match: cases
  `53497f56ab0ac4b05c4dba7ca21e022f5bf62813`; continuation
  `dc82aa748a195391143a09958e4e0dade827c45b`; codec
  `c8a21b91cc4d285ff6e82b1f1b187c4e178bb5ce`; dealer
  `2963004e38c6e66f76ae9ce3bd474063eee870fe`.

Commands were read-only Git `rev-parse`, `diff-tree`, `ls-tree`, `show`,
`cat-file`, and `status`, plus packet/skill text reads and standalone standard
library hashing/text inspection. The hashing helper used the installed
`C:/Users/point/AppData/Roaming/uv/python/cpython-3.11.15-windows-x86_64-none/python.exe`
with `-B -P`, imported no Pontius module, and executed no candidate/library code.
Git object reads used `git -c safe.directory=D:/Pontius -C D:/Pontius`.
Completed identity checks exited successfully. An initial unquoted PowerShell
tree suffix, an unavailable bare `python`, and a CP1252 output encoding error
were inspection-tool failures only; they were corrected and the pertinent reads
completed. They are not product failures or test results.

The primary checkout had tracked status changes in `STATUS.md` and
`execution_journal.jsonl`; their contents were not used as review evidence and
neither file was modified. The only created file is this attributed report,
created in the coordinator-authorized writable staging location for packet filing.

No runtime, solver, table host, test suite, historical owner, benchmark, or remote
service was invoked. No dependencies were installed. No candidate, sealed source,
old project file, ledger, branch, or ref was edited. No other review, implementer
transcript, or coordinator conclusion was read, and no other reviewer was contacted.
Historical figures cited in the candidate were cross-checked where available
against the frozen bot-validation and blueprint-performance summaries; their
external retained reports were not rerun or treated as fresh experimental evidence.

Specification verdict: **Fail** because the frozen design contains the material
contradictions above. Engineering-quality verdict: **Partial**, with viable core
mapping but unresolved observation, population and feasibility contracts.
Runtime correctness and performance remain unverified, as this packet requires.
