# C authority repair: current engineering state

2026-08-31. Navigation only. This page is not a frozen handoff, evidence seal,
acceptance result, or reviewer verdict. New reviews require a git snapshot ref
and its manifest SHA-256; no successor pair has been frozen yet.

## Latest checkpoint: two separate repairs, no integration

The isolated radix-store/bulk-builder replacement passed **558 checks**:
34 unchanged storage runs, 28 cursor-successor runs and 31 indexed-extension
runs per child, on actual Python3.11.15 and3.14.6 with seeds0/1/17. The
[coordinator verification](coordinator-indexed-verification-allsix01.json)
rehashed10665 files including manifests; same-seed complete records match
across interpreters. All14 preregistered P/C growth comparisons pass per child,
as do collision activation, direct obsolete-value release and15 injected
indexed-operation retries per child. The old cursor retention trigger was
explicitly made representation-neutral before results; do not call all62
predecessor executable checks byte-identical.

[Source/accounting inspection](coordinator-radix-prototype-inspection-v1.json)
and [independent oracle inspection](coordinator-indexed-oracle-inspection-v1.json)
preceded dispatch. This establishes finite pure-store behavior, **not production
fitness or wall-time speed**. The adapter must preserve full authority transfer,
cell writes and real input-preparation costs, then pass the original analyzer
gates. No radix implementation is installed in W or main.

The previous v22 cursor adapter remains RED:51/53 original design tests pass,
with helper1050 and generator70 exhausting the unchanged work budget. Both
[exact-case diagnostics](coordinator-v22-depth-budget-verification-v1.json)
locate failure in preparation, not deep execution. This is why the replacement
uses touched indexed paths and a direct unique-entry bulk builder. The original
caps and assertions remain unchanged; ordinary generation is still unverified
on the replacement. W remains rejected v20.

The added composition checks found an independent semantic defect on retained
v19. Both original class cases fail on both interpreters: an unsafe case is
approved and its safe counterpart is refused. The original shared-list pair
passes. [Initial finding](coordinator-class-adoption-finding-v1.md) preserves
the unchanged expectations and the initial, explicitly provisional diagnosis.

The subsequent [two-case trace](tests-checks/class-composition-original-class2-v19-mechanism01-311-receipt.json)
and [six-case extension](tests-checks/class-composition-scalar-class6-v19-mechanism01-311-receipt.json)
correct that initial lead: write-only nonlocal setters omit their captured
destination because discovery considers only Name loads. The setter changes
its private projection while the caller's cell retains the old value.
Class-body execution also continues past an explicit raise. Earlier protected
namespace rebinding guards cause additional safe-case refusals. A projection
refresh alone therefore cannot close this category.

Both trace scopes completed on both interpreters with intact infrastructure
and correct harmless oracles. The scalar extension fails four of its six
requirements on each slot (both normal cases and both safe exception cases).
The two unsafe exception cases are refused; that alone does not establish
correct exception semantics. A separate semantic repair must address captures,
normal and exceptional class exits, and precise versus unresolved rebinding.
All cases and issued evidence remain immutable.

The [fixed twelve-case extension](tests-checks/class-semantic-extension-cases-v1.json)
has now run on retained v19 under both actual interpreters. All twelve harmless
models pass and all analyzer calls complete, but ten semantic requirements
fail identically on each slot. All five required unsafe cases are incorrectly
clean. C01 also leaks the class-local module into the outer continuation;
C11 enters recursive review with the stale captured value and emits no row.
[Independent verification](coordinator-class-extension-red-verification-v1.json)
rehashes both full snapshots and compares all complete case records.

The [eight Name-boundary cases](tests-checks/class-name-boundary-cases-v1.json)
also completed on retained v19 under both actual interpreters. All harmless
Models pass; four semantic requirements fail identically: two safe cases are
refused, an unsafe direct class nonlocal write is incorrectly approved, and
the safe module-write case misses its required conservative refusal.
[Independent verification](coordinator-class-name-boundary-red-verification-v1.json)
retains the exact per-case results and3541 rehashed files.

A semantic-only v23 candidate is being authored under the
[coordinator disposition](coordinator-class-semantic-v23-disposition-v1.md).
It addresses lexical ownership/current-cell separation, normal and exceptional
class exits, Name routing, and historical callable/call-state pairing. The
class-only eager comprehension boundary is within that scope; unproved deferred
class-generator consumption must explicitly refuse. Six additional independent
[comprehension witnesses](tests-checks/class-comprehension-boundary-spec-v1.md)
are preregistered but unexecuted. No semantic candidate payload has run.

The storage and semantic edits remain separate until independently inspected
and checked. Original10 composition, class12, Name8 and comprehension6 checks
will precede focused analyzer/corpus gates. Only a coherent verified candidate
can be frozen for two new mutually blind cold reviewers and later integration.

The candidate is still not acceptable. Accepted A/B and other C paths remain
preserved; the class defect and ordinary-generation budget failure are both
open. The detailed prior engineering evidence follows.

Accepted A/B remains byte-identical to r007. The other three C integration paths
(CI, boundary checker, boundary tests) are unchanged. Main remains d1ed3cb;
no source integration, ceremonial commit, or main push has happened.
[Independent preservation check](coordinator-v19-preservation-v1.json) verifies
all thirteen preserved paths and the unchanged generated pair.

The latest frozen combined candidate is rejected r010:
29c02f6fbd5eb0b7ddc9e816ef28f570b9839358 /
8741fa20b1ebc7e9e9d226f463680c603c348f1332bf19c8ae12b29579f76deb.
Its findings and reports remain immutable. The [separate repair design](stage0-design.md)
replaces the bounded callable-authority state/transfer representation.

Last successful full focused checks: v19 source
3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1
passes the original 53 DesignReview tests and the new matrix's 192 schedules /
212 harmless projections on actual Python 3.11.15 first and 3.14.6 second.
[Hash-bound receipts](engineer-checks/release19-focused-evidence.json) document
focused engineering only; they are not corpus GREEN or cold approval.

Ordinary generation on v19 still reaches the unchanged 262144-unit analysis
limit. [Write06 receipt](coordinator-checks/c-authority-write06-311-receipt.json)
records exit 2 and no generated-file change. [The completed v19 diagnosis](tests-checks/budget-gen06-diagnosis-v1.md)
confirms 492 selected merge plans and 15780 net work units saved for those traced
merge operations, including fallback overhead. Full generation still refuses in
the same inventory-structure item. The dominant costs remain authority transfers,
map reads, copies, joins and forks. These totals stop at refusal; the savings are
not a whole-corpus before/after comparison or a performance acceptance claim.

The v19 edit preserves every transfer and cell write while batching eligible
binding lookups. [Prerepair reasoning](engineer-merge-batch-prerepair-v19.md) and
[exact v18 delta](engineer-generator-v19-from-v18.diff) remain engineering inputs.
Following repeated generation failures, the [bounded storage decision](coordinator-storage-disposition-v1.md)
accepts an isolated prototype of persistent names with exact legacy-order recipes.
Reuse is restricted to a proved context-independent no-work transfer; live-reference,
rebuilt and raw entries remain pending. No store-lineage cache is included. The
[independent proof](tests-checks/name-environment-transfer-proof-v1.md) states the
restriction and preserves every cell write and consumer analysis.

The [structural family](tests-checks/name-environment-report-v1.md) passes all 24
semantic expectations and 58 harmless projections on each actual interpreter.
All four zero-change comparisons demonstrate repeated ambient-name work; this is
structural RED, with no analyzer or oracle failure. [Coordinator verification](coordinator-name-environment-verification-v1.json)
checks the pinned evidence and identical cross-slot counters. The hidden tuple-return
sentinel demonstrates safe refusal, not precise joined-cell resolution.

The isolated storage prototype passed 204 checks across actual Python 3.11.15
and 3.14.6, each with hash seeds 0, 1 and 17. [Coordinator verification](coordinator-storage-verification-v1.json)
rehashes the six snapshots and verifies exact order, retained versions, failed-read
cache behavior and equal same-seed records across interpreters. Zero-change joins
cost 36 units each at both 8 and 64 ambient names; construction, terminal ordering
and retained-version reads still carry substantial, separately recorded costs.
This establishes pure-storage compatibility, not ordinary-corpus GREEN.

The port produced v20 source
e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679,
which is rejected for production fitness. Its first floor DesignReview run
completed 53 tests with two failures and one error: bounded helper analysis
exhausts the unchanged work cap. The [single-chain diagnosis](engineer-checks/chain32-v20-diagnosis01-311-receipt.json)
locates the dominant cost in helper-disabled joins that repeatedly rebuild name
trees, followed by ordered reads.

The [v20 public24 assessment](tests-checks/name-environment-v20-floor-report-v1.md)
confirms all 24 public expectations and 58 harmless witnesses still pass on 3.11.
Shared forks and enabled sparse joins improve locally, but total charged work
rises 8.07 times versus v19. This is a consumed-budget comparison, not a runtime
multiplier. [Coordinator verification](coordinator-v20-diagnostics-verification-v3.json)
rehashes the retained snapshots and checks these results.

The [fitness disposition](coordinator-v20-storage-fitness-disposition-v1.md)
closes the port lease and reassesses the name-store lifetime before another edit.
W remains exact v20; v19 is the last source with both focused populations green.
No further v20 acceptance run, developer-slot run, matrix or ordinary generation
is planned. All five caps, test contracts, accepted A/B and the other three C paths
remain fixed. No main source integration or new frozen handoff is implied.

Remaining order: complete the bounded repair; ordinary generation; preservation
of all 2873 existing inventory entries and 141 canonical capability rows;
mechanical census refresh; nine focused targets on both interpreters; freeze the
successor pair; two fresh mutually blind cold reviews; the permitted CPU acceptance
wall. Only then does candidate-specific controller authorization permit Claude,
the checkpoint finalizer, to commit/push.

No guarded profile, GPU execution, source seal, research owner, rehearsal, or live
15-second action-wall claim is authorized by this repair.
