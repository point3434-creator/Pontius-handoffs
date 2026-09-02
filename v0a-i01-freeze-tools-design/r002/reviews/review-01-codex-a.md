# Cold design review: v0a-i01-freeze-tools-design/r002

Reviewer ID: codex-a
Candidate commit: 48e590327c0a4bfd7ea5019e6770e1d582182b08
Manifest SHA-256: 010e96031f60afd8badc07ebb4dd97ab8db4102527be0eb42ee56c2d65e7c984
Defect verdict: NOT CLEAN
Design verdict: WRONG SHAPE

## Outcome

Two Important corrections remain. The first makes the current r002 bootstrap
review impossible to instantiate from its immutable handoff: the handoff's
report/ledger contract and artifact population cannot satisfy the candidate's
normative bootstrap-review receipt and publication schemas. The second is an
adopted-workflow violation: this FIX candidate adds 16,396 lines of normative
design, including a prospective Stage 0b authority system, without separating
new surface or declaring named review slices.

The four-role runtime and authority decomposition is materially stronger than
r001. The raw-object grammar, role separation, local and remote state models,
credential route, main graph, and failure-accounting design address the known
r001 mechanisms in substantial detail. Those improvements do not cure the
current bootstrap contradiction or the scope/reviewability violation.

## Finding 1 — Important: the current bootstrap review output is uninstantiable from the frozen handoff

Confidence: high.

### Exact frozen locations

- Immutable packet `handoff.md:128-154` permits each reviewer to issue one
  report and one ledger line. It fixes five mandatory report labels and requires
  the ledger line to contain date, round, reviewer, both verdicts, candidate,
  manifest, report path, and report digest. It names no reviewer-authored typed
  receipt artifact and supplies no bootstrap series-state or design-packet-
  publication canonical object.
- `docs/briefs/v0a-i01-freeze-tools-r002-brief.md:289-300` nevertheless says
  this documentation review returns a typed bootstrap-design-review receipt,
  report, and issuer line.
- `docs/superpowers/specs/2026-09-01-raw-object-workflow-amendment-v5.md:111-116`
  says each current reviewer publishes that typed receipt.
- `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-design.md:179-199`
  makes the same current-bootstrap claim and makes those publications inputs to
  the external-controller design disposition.
- `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-schemas.md:7050-7085`
  requires a complete canonical series-state object and packet publication
  chain for r002.
- `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-schemas.md:7106-7158`
  defines the bootstrap design-review receipt and publication. The report must
  begin with eight exact header lines, including packet-publication digest,
  series-state digest, and reviewer ordinal. The issuer line instead has the
  exact ordered fields reviewer, ordinal, candidate, manifest, report digest,
  defect value, and design value. The publication artifact population must
  contain the receipt, report, and line.
- The immutable packet tree at commit
  `14c1f5629024973b96f71c64a04f17ce9d7e01e2` contains the handoff,
  candidate identity, manifest, coverage, four frozen inputs, and the excluded
  check. It contains no canonical series-state, design packet publication,
  design-author set, convergence-policy artifact, or typed review-receipt input.

### Concrete state and wrong outcome

Start with the actual immutable r002 packet and an independent reviewer that
follows its output contract exactly. The reviewer produces the permitted report
and a line with date, round, report path, and report digest. That line cannot be
the schema's ordered seven-field line: it has required fields the schema omits,
omits the schema's ordinal field, and has a different order. The report also
cannot reproduce the required packet-publication and series-state digests
because the packet neither supplies those canonical preimages nor identifies
their artifacts. Finally, the handoff does not authorize the reviewer to emit
the receipt artifact required by the publication schema.

The strict candidate parser must therefore reject the real reviewer output. If
the coordinator instead invents the missing objects, rewrites the line, adds
headers after report freeze, or synthesizes the receipt, the result violates
the candidate's exact issuer authorship, report equality, artifact population,
and peer-blind bootstrap rules. The downstream design disposition and
implementation authorization consequently have only two possible outcomes:
they remain permanently unreachable, or an implementation weakens/bypasses the
normative bootstrap checks and lets non-issuer or unbound bytes open source
work.

### Violated invariant

Canonical review provenance must have one exact writer/reader contract, all
required preimages must be reachable from the immutable cold packet, and an
unaccepted utility must not repair or synthesize its own review authority. The
adopted packet contract and the proposed typed bootstrap cannot both govern the
same current review when their line formats and artifact populations differ.

### Required outcome

Issue a new frozen round whose current-bootstrap specification has one coherent
contract. Either:

1. the immutable handoff supplies every canonical packet/series/author/policy
   preimage, authorizes the reviewer to issue the receipt, and requires report
   and line bytes exactly equal to the schema; or
2. the candidate removes the current-review typed-receipt claim and defines an
   acyclic bootstrap using only the actual adopted rule-6 report and issuer
   line, without later coordinator synthesis masquerading as reviewer output.

The same byte grammar must appear in the handoff, brief, amendment, design, and
schemas. Existing packet or report bytes must not be retroactively upgraded.

### Verification criterion

From only the new immutable cold-input packet, a reviewer can deterministically
produce every authorized output artifact. Independent strict parsers accept the
report, line, receipt if required, and rule-6 publication without filling any
missing field. Every required count/digest resolves to a supplied complete
preimage. Independently change the date, round, ordinal, report path, any
header, series-state field, packet-publication field, report byte, line byte,
receipt byte, issuer, or artifact population; the exact consumer refuses.
Prove that no coordinator-created object is represented as reviewer-authored.

### Advisory engineering technique

Generate the handoff output section and the strict report/line parser fixtures
from one versioned bootstrap-output schema, then run a frozen-packet round-trip
fixture before publication. This is a technique, not an additional required
gate; the required behavior is the exact cross-boundary agreement above.

## Finding 2 — Important: this FIX round adds unsliced new authority surface

Confidence: high.

### Exact frozen locations

- Adopted `inputs/workflow.md:288-292` says a FIX round changes only what its
  findings require and that new surface goes in its own candidate.
- Adopted `inputs/workflow.md:330` says any candidate over roughly 3,000
  changed lines is reviewed as named slices from round one.
- `inputs/r001-disposition.md:29-59` fixes eleven binding correction classes.
  They concern role/runtime closure, deterministic commits, credentials,
  provenance, HTTPS rehearsal, main graph, replay, adoption, and the local
  tuple. They do not require a general Stage 0b convergence/publication system.
- The raw candidate diff is six add-only `100644` files totaling 941,640 bytes
  and 16,396 lines. The base contains none of the six paths.
- Immutable `handoff.md:19-39,92-93` presents the six files as one complete
  design review scope, not named slices.
- `docs/briefs/v0a-i01-freeze-tools-r002-brief.md:217-279` provides future
  implementation source budgets but no named slice plan for this design
  candidate; `:339-342` expressly identifies the prospective Stage 0b counter,
  round-freeze, disposition, and build-authority schemas as implementation
  targets for a different activated series.
- `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-schemas.md:4445-5953`
  defines the Stage 0b proportionality counter and disposition system;
  `:6806-7384` defines packet inventory and utility acceptance authority; and
  `:7385-8292` adds the freeze-tools implementation-start/bootstrap system.
  These are substantial new authority interfaces, not merely corrections to a
  named r001 member.
- Deferred `coverage.md:749-844` calls this R2-26 and explains the new
  convergence mechanism, but it does not identify a binding r001 finding that
  requires the full new system, classify it as NEW-SURFACE, or reconcile the
  16,396-line candidate with the mandatory named-slice rule.

### Concrete state and wrong outcome

Use the actual r002 state: an eleven-class FIX is frozen as one 16,396-line
review target, and the same candidate also normatively specifies future Stage
0b activation, counter, atomic publication, review, disposition, and build
authority. If both reviewers return clean on the correction classes, the
candidate's bootstrap design authorization can open implementation of all
candidate-approved targets, including the unrelated prospective meta-workflow.
Those new interfaces have never been classified as first-contact NEW-SURFACE
and were not assigned independent named slices despite being more than five
times the adopted slicing threshold. A defect or authority cycle in that
surface is therefore allowed to pass under a FIX disposition whose predecessor
never required it; later activation can depend on a design approval obtained
under the wrong review category and review granularity.

### Violated invariant

FIX scope is frozen to demonstrated correction classes, and review ceremony
must scale with blast radius. New authority interfaces require their own
candidate, while a candidate above the threshold requires named slices from the
first review. A frozen handoff cannot waive those adopted rules merely by
listing the extra surface.

### Required outcome

Produce a new round that confines the r001 FIX to the required role/runtime,
Git, provenance, rehearsal, graph, replay, adoption, and tuple corrections.
Move the prospective Stage 0b convergence/publication/activation machinery to a
separate NEW-SURFACE candidate after the authority bundle has an accepted root.
For any design candidate still above roughly 3,000 changed lines, freeze named,
nonoverlapping review slices in its first handoff and require both Tier-C
reviews to cover every slice. A changed scope or byte population must receive a
new candidate identity; no current frozen artifact is edited.

### Verification criterion

The successor's complete path/section-to-requirement map ties every normative
FIX member to one of the eleven binding r001 classes or a retained advisory
criterion. No prospective Stage 0b activation/counter/publication/build-
authority interface remains in that FIX. Independently recompute the changed
line count. If it exceeds the adopted threshold, the immutable handoff names
the slices, their exact path/section populations, overlap rules, and complete
Tier-C review coverage from the outset. A separate future Stage 0b candidate is
declared NEW-SURFACE and cannot authorize or retrospectively upgrade this
bootstrap series.

### Advisory engineering technique

Keep three specifications separate: the minimal authority-tool correction,
the adopted-workflow bootstrap adapter, and a future Stage 0b automation
protocol. Give each a small interface registry and an independent review
packet. This is advisory; the binding correction is scope and slice compliance.

## Design assessment

The replacement role/runtime core is promising, but the candidate combines too
many authority layers in one 941,640-byte design: Windows/CPython confinement,
Git object and remote publication, credential brokering, main graph semantics,
review packaging, current utility bootstrap, external retention, and a future
Stage 0b meta-workflow. The current handoff/schema contradiction is direct
evidence that this shape invites the very cross-carrier mismatches it is meant
to prevent. The adopted workflow also makes redesign the default after the
r001 architectural rejection.

Build instead a narrower correction design for the reusable four-role utility,
leaving its own current bootstrap entirely on the already adopted rule-6 path.
After that utility is accepted, design Stage 0b automation as a separate
NEW-SURFACE protocol using the accepted utility as an external root. The cost is
at least two newly frozen design candidates and explicit interface adapters;
the benefit is that neither protocol must model its own not-yet-existing
authority, and each can be reviewed and falsified at a tractable boundary.

## Initial invariant and seam inventory

The following inventory was fixed in
`D:\Pontius\tmp\freeze-tools-design-r002-review-codex-a\initial-inventory.md`
before `coverage.md` was opened. The deferred claim did not influence it.

1. Immutable packet/candidate identity: exact ref, commit, single parent, tree,
   six-path mode/scope, raw blob manifest, r001 manifest, input hashes, and
   runtime-closure count/byte population.
2. Acyclic authority/bootstrap: adopted temporary-index and rule-6 root,
   current design outputs/disposition/authorization/start, implementation
   reviews/tests/rehearsal/controller decision, P ceremony, H record and durable
   disposition, external retention, and future activation.
3. FIX scope and reviewability: correction-only surface, NEW-SURFACE separation,
   and named slices above the adopted size threshold.
4. Complete role closure: four source projections; execution-role operation,
   schedule, owner-request, table, argv, predecessor, result, and refusal sets;
   no builder network/main/output capability.
5. Complete pre-execution runtime closure: source/archive/native/data/system
   image projections, loader-before-Python, isolated configuration,
   AppContainer/ACL/Job boundary, lock/ACK, late influence denial, and final
   revalidation.
6. Typed planner/owner seam: canonical framing, capability-safe input/output,
   exact sequence and predecessor digests, no caller-selected authority, and
   sticky refusal.
7. Deterministic Git bytes: raw blobs/trees/commits/manifests/overlays, complete
   metadata and parent order, no ambient identity/clock/index/filter, and
   independent parsing.
8. Local atomicity: complete builder and integration-attempt tuples, exact
   stdin/EOF evidence, all partial/different/unknown states, shared mutex, and
   lost-ack recovery.
9. Fresh adoption: publisher no-ref fetch and receipt followed by offline
   builder graph validation and full tuple creation; no cross-row or result-
   selected fixture.
10. Remote monotonicity: atomic create-only candidate/packet pair, permanent
    spent semantics or coherent retirement supersession, fatal partials,
    independent reviewer slots, natural-return reconciliation, and timeout no-
    new-child behavior.
11. Credential/HTTPS closure: GCM/store/erase and ambient routes absent;
    one-shot broker PID/image/Job/URL/refspec binding, pipe and prompt grammar,
    write/flush cancellation, zeroization, and server one-use lifecycle.
12. Process/storage/cleanup truth: durable dispatch consumption; complete or
    exact-prefix schedule; every process, Job, broker, transport, object write,
    scratch/storage/mutex fact; quiescence and revalidation; no semantic result
    when cleanup is unprovable.
13. Main graph/state: two-parent packet integration, one-parent later commits,
    exact-lease plus ancestry, all-parent spent result, independent lineage and
    task axes, full phase history to `NO_TASK`, descendant/interleaving/revert/
    lost-ack cases.
14. Current and later review provenance: actual handoff writer contract, two
    reviewers/reports/lines, two later four-role receipt documents, author
    exclusion, report/receipt/line/manifest/ref/finalizer equality, peer
    blindness, and no synthesized issuer bytes.
15. Real-boundary rehearsal: paired production/rehearsal tables, disjoint
    namespaces, capability observations, fixtures/derived inputs/adoption
    chains, reviewed fault provenance, signed server lifecycle, all failure
    schedules, and post-case observations.
16. Stage 0b convergence: explicit current-series exclusion, terminal-r005
    declaration equality, counter/predecessor/interface/residual/ambiguity/
    override/parking/build states, no r006, and later activation only.
17. Cross-document agreement: brief, design, schemas, runtime/Git appendices,
    amendment, adopted workflow, r001 corrections, actual handoff, and deferred
    claim must agree on every schema, carrier, equality, state, cardinality,
    current/future route, and public verification boundary.

Systematic seams inventoried were controller-to-authorization-to-dispatch;
source/author evidence to role/runtime projections; bootstrap-to-Python-to-lock;
planner frames to owner tables and process grammar; repository projection to
object store and local transactions; broker/askpass to HTTPS queries,
fetches, and pushes; remote pair to adoption; main scratch/readiness/fetch to
overlay/attempt/push; raw DAG and phase bundles to recovery; report/line to
receipt/manifest/output/finalizer; current rule-6 design outputs to
implementation start; implementation acceptance to P/H/external retention; and
every timeout/cancel/loss/host-failure route to containment, storage accounting,
final revalidation, and either a typed envelope or no-envelope failure.

## Coverage-claim comparison

The deferred claim hash reproduced as
`72fff2541772140f558bc40ef3e137a165c240f29feabd9faac139467a030e46`.
Its R2-01 through R2-25 members substantially cover the initial inventory's
role, source/runtime, owner-frame, raw-object, local tuple, adoption, remote
pair, credential, transport, process, storage, main, review-package, rehearsal,
parser, and evidence-DAG seams. Its falsifiers are generally public-boundary
observations rather than structural assertions.

The comparison nevertheless falsifies the claim in two places:

- R2-06 and R2-26 assume that the current typed design-review receipt and
  publication can be issued. They never compare the normative report/line
  grammar and required artifact population with the actual immutable handoff.
  Initial-inventory items 2, 14, and 17 exposed that missing writer/reader seam.
- R2-26 describes the new convergence system as coverage, but it does not map
  the prospective Stage 0b authority surface to a binding r001 correction or
  address the adopted 3,000-line named-slice rule. Initial-inventory items 3,
  16, and 17 exposed that scope and granularity gap.

Coverage therefore is broad but not complete. Its discovery method found many
internal schema relations but did not test the candidate against the external
packet contract that must instantiate the current bootstrap, and it treated a
new meta-workflow as a correction without checking the adopted round-kind and
slice requirements.

## Verification evidence and limits

Read-only evidence obtained:

- the candidate ref resolves to the stated commit;
- the commit has the stated single parent and tree;
- the diff is exactly six add-only `100644` paths and those paths are absent at
  the base;
- raw blob SHA-256 rows reproduce the exact r002 manifest, whose own bytes
  reproduce the stated digest;
- the five r001 raw blobs reproduce the stated r001 manifest digest;
- all four frozen input hashes and stated sizes reproduce;
- the runtime closure parses to 2,614 unique ordinal-sorted rows and the
  declared byte total; and
- the deferred claim hash reproduces before comparison.

No candidate artifact, pinned CPython runtime, implementation test, credential,
remote query, network mutation, ref update, packet publication, retained
evidence, peer report, excluded check, mutable draft, or current advisory audit
was opened or executed. This is a design/specification verdict. OS, CPython,
Git, server, process, and credential behaviors remain implementation-stage
falsification limits exactly where the candidate says they do.
