# Indexed name-storage extension: independent schedule freeze v1

Engineering specification and design challenge only. No prototype source was read
or written for this extension, and no payload, analyzer, fixture or oracle was
executed. This freeze supplies independent schedules/oracle requirements for
coordinator review before implementation. It does not authorize a production port,
change any cap, or approve storage fitness.

## Pins and preserved evidence

All paths are under D:/Pontius-handoffs/v0a-i01-c-authority.

| Input | SHA-256 |
| --- | --- |
| engineer-v22-two-case-storage-decision-v1.md | 8ac28ed870ecd2fcf5c516aa034357f7d634b14181501960fc6bc44f76b384b6 |
| engineer-radix-api-boundary-plan-v1.md | 6e37ce7ce7d768c157bd00490f4d0bc8f92753385bfa375b73bab610d2e87150 |
| engineer-generator-v22.py | 61a0ce3bc3ea59bc09a7b14d45da843fb3c3a8614feb4c913132b67028916da3 |
| coordinator-name-cursor-prototype-disposition-v1.md | 973191b8b26c71132185d42203a720bdc5b28d4fd23fc1bc4b9c9ec4da46a7b7 |
| tests-checks/storage-oracle-v2.py | 6a58ef82832d53510f7d44d58cf5a8fa3764f8be5f2c28dcb7e555a83c72cfba |
| tests-checks/storage-oracle-cases-v2.json | 3bd5678da334fb551c2f179906e8b4d2cf7a0b0e7a3779e0fad2fb4b4a9c548f |
| tests-checks/cursor-oracle-v1.py | 15a4741e2532a755fd45f01d4d999dd5d293846b8ae4e9d4e7abedf84c0a8d1e |
| tests-checks/cursor-oracle-cases-v1.json | ecddd020ffb2a0d85e624aeb7fb544f631b302839f9a5f3542c998b36c37ac61 |
| tests-checks/indexed-storage-extension-cases-v1.json | 795e893c4fbeee3963a3ea3cbbffdfacbea193f53063eb4848c8e9ac6d12984a |

The new JSON is 4,766 bytes and contains exactly16 schedules and31 planned runs
per child. Eleven schedules run once; five operation-atomicity schedules run one
pristine baseline plus first/middle/last fault replays. The old storage28-case/
34-run pack stays unchanged. The old cursor16-case/28-run pack stays unchanged,
with the separately authorized retention-trigger successor described below.
A future combined child would therefore have34 +28 +31 =93 runs, six coordinated
children558. No such child is authorized or executed by this note.

Earlier62-run/372-result artifacts remain evidence of their original candidate
and oracle bytes. The successor is not relabeled as byte-identical old evidence.
The new case expectations and growth classifications below are fixed before any
indexed-prototype source/result is available.

## Qualified challenge to the proposed repair

The proposal addresses two distinct mechanisms only if both its mutation path and
its full rebuild path change. An index alone can still copy a growing prefix in
leaf/pending metadata, replay order ancestry quadratically, or retain obsolete
value-bearing roots in history. A bulk factory implemented as N persistent set()
calls can still repeat absence checks/path rebuilding. Neither is rescued by
a favorable lookup microbenchmark.

A bounded persistent index can avoid full-prefix copying on real frequent forks.
An ordered unique-entry bulk factory can avoid repeated persistent insertion when
the caller already has complete unique outputs. These are plausible mechanisms,
not measured wins. Required full-merge enumeration/transfer/cell work remains
linear work that must be charged in production; this pure factory does not
eliminate it or prove its ordering. The factory's input preparation is outside
primitive measurements and must be disclosed as such.

The exact legacy set-union sequence is an externally observable order recipe,
not the index's traversal order. History and order ancestry must remain name-only.
Old leaf values must leave the current published root when replaced/deleted,
while intentionally retained old snapshots still own them. A late failing
publication/read must not leave cheaper caches or earlier internal publication
behind. The schedules exercise these concerns directly.

This freeze admits no threshold sweep, arbitrary-hash exclusion, disabled-mode
discount, refcount ownership inference, new production hasher hook, cap increase,
or change to callback/authority semantics. A collision bucket may have legitimately
worse costs; those costs are reported rather than folded into favorable-hash claims.

## Representation-neutral public API

Retain Meter(limit, used, counts, charge), BudgetExceeded, immutable Entry(value,
no_work), MISSING, NameVersion empty/get/set/delete/fork/keys/ordered_items/len,
NameCursor construction/get/set/delete/snapshot/fork/keys/ordered_items/len, and
join(meter, immutable_versions, pure_merge). Existing no_work invalidation,
input-tuple order, snapshot stability, genuine read-only dict_keys snapshots,
value identity, cross-meter refusal and cursor-input refusal remain unchanged.
No direct tree/layer/root introspection supplies semantic expectations.

Add only NameVersion.from_unique_entries(meter, entries). The supplied iterable
is consumed once. Each element is an exact two-element tuple (name, Entry),
with exact Entry and exact-bool no_work, using the existing supported name domain.
Bad shape/type raises TypeError; duplicate names raise ValueError. One explicitly
charged membership attempt in the name-only order staging dictionary is allowed
per valid supplied entry. The optimization forbids an additional predecessor
index absence lookup or repeated immutable set solely to discover uniqueness.

The factory preserves input key order, Entry/value/proof contents, returns a fresh
detached lineage, and does not normalize/transfer/merge or invoke the join callback.
Value identity and effective proof are checked through public operations; any
private Entry-identity guarantee additionally needs the coordinator's source
inspection because the public API does not return stored Entries.

All factory effects are staged until success. It mutates no existing receiver,
version or source tuple. Iterator consumption is not rolled back; replay uses
a fresh iteration of the same immutable input sequence, not a half-consumed
generator. Source iterables used by the oracle are pure except for independent
enumeration counters and contain only harmless tokens.

## Independent semantic oracle

Use ordinary builtin dictionaries with a separate name-to-proof dictionary.
Cursor fork/snapshot copies the reference dictionary; version edits derive an
independent dictionary. Overwrite preserves position, delete removes it, and
reinsertion appends. Values are independent harmless identity tokens, never
sensitive source fixtures or owners. Retention sentinels are excluded from any
global token registry or saved encoded-object graph.

For each join, execute the actual legacy expression in that same child:
set().union(*(reference_dict.keys() for reference_dict in input_states)).
Iterate that result to form the expected final name order. Pure reference merge
uses value/MISSING tuples in supplied-state order and the old identity-on-equal
law. Verify all changed or pending names receive the callback, and verify every
callback's ordered arguments/results. Additional callbacks for unchanged
certified entries remain allowed. No cross-name callback order is newly required
by this primitive; production full-merge order remains a separate obligation.

Never freeze hash-dependent expected order as a literal. Use seeds0,1,17 on
actual3.11.15 before actual3.14.6 in fresh isolated children. Compare same-seed
runtime results while allowing genuinely runtime-dependent builtin order;
each runtime's own builtin oracle is authoritative. Different hash-seed order
is not a failure if its independent oracle agrees.

Public reads, verification reads, historical audits, factory input preparation,
and oracle bookkeeping are distinct phases. Only prototype Meter deltas are
charged prototype work. Oracle copying/encoding is not smuggled into that meter
or used as a claimed implementation cost.

## Closed collision domain

For I06/I07 and the collision portion of atomic preparation, every stored
collision key and every equal/absent lookup/delete comparand is CollidingName,
one str subclass with hash0 and ordinary string comparison. Its equality method,
if instrumented, delegates to str equality without changing the result; ordering
is inherited unchanged. All equal-text comparands are the same class/hash.

No equal-text plain str enters a prototype operation, reference dict/set, or the
comparison pool. Ordinary u-names in mixed atomic preparation have different text
from every c-name. Check equality implies equal hash across the finite supplied
key/comparand pool outside measured calls. Reporting converts labels to text
only after operations and never reuses those labels as keys.

This is a closed consistent test domain, not a claim that a constant-hash str
subclass can interoperate lawfully with arbitrary equal-text plain strings.
It uses the previously permitted controlled-subclass collision contract. No
production hasher is injected or replaced, and no prototype method is monkeypatched.

Independent key-protocol hash/equality counters may count actual calls during
each primitive operation, reset only their observer counters outside the call,
and exclude builtin-oracle/validation comparisons from that phase. They must
not mutate keys, comparison results, prototype source, Meter or implementation
state. Record the actual collision bucket/path activation using the reviewed
operation-accounting map. If the intended collision path was not reached,
report an unmet structural precondition, not a collision pass. Normalizing away
the collision schedule cannot establish collision coverage.

Dictionary-attempt charges and actual key-protocol comparisons are different
quantities. Report both. A unit charged for one builtin dictionary attempt is
not a claim that its internal C-level probes/comparisons cost one operation.
Do not invent extra charged units or hide collision comparison work in a
favorable physical-cost claim.

## Exact finite schedules

Ordinary names are u followed by four zero-padded decimal digits; collision names
are c with the same index format, constructed in the closed domain. Missing
comparands use a distinct u-missing or CollidingName c-missing text. Values are
independent token objects keyed by their specified round/index labels. Each
schedule starts with a fresh Meter whose maximum remains262144.

| IDs | Shape | Purpose |
| --- | --- | --- |
| I01-I03 | Growing unique writes, N=32,128,512 | Real fork after every write; detect growing-prefix work and deferred order work. |
| I04-I05 | Ambient N=32,512;32 hot cycles | Fixed mutation count as ambient state grows; overwrite/delete/reinsert, proof and order. |
| I06-I07 | Closed collisions, N=16,64;3 hot cycles | Actual collision handling, cursor publication, bulk building, extraction and joined order. |
| I08-I10 | Unique bulk construction, N=32,128,512;4 rebuilds | Linear unique-output construction and immediate demanded order, including all-pending rounds. |
| I11 | Ambient64,2 weak victims,1 changed publication | Current root/history releases replaced/deleted values once the last old owner is dropped. |
| I12-I16 | snapshot/fork/keys/ordered_items/bulk;64 ordinary+16 collision names | Whole-operation failure atomicity, exact retry cost and subsequent continuation. |

Growing family: start from empty version/cursor. For each i from0 throughN-1,
set u_i to token v_i, with no_work true except i divisible by4. Fork immediately;
retain the pre-fork cursor and continue only on the returned independent cursor.
There are exactlyN real cursor forks. On the next write, read its new key from
the preceding retained cursor and require the missing default, proving isolation
at every boundary rather than substituting a no-op version alias. Retain all
parents until the end; terminal keys/items and their second reads are measured.
Fully audit retained prefixes N/4,N/2,N in a separately labeled historical phase.
The reference oracle controls the expected prefix/order/value identities.

Hot family: bulk-build the ambient u0..u(N-1) state, recording setup separately.
Retain its original snapshot. For each of32 cycles r, overwrite u0 with round-r
token (alternating explicit certified/raw installation), fork; delete u1, fork;
reinsert u1 with a fresh round-r token, fork. Continue on the new child each time.
There are96 mutation-triggered forks at either ambient size. Retain a midpoint
snapshot after cycle16 and the original; discard other unneeded cursors.
Parent/child mutation isolation, absent delete state, appended reinsert order and
effective pending proof are checked. Final keys/items, repeat reads, retained
audits and a pure join of midpoint/final snapshots are separate cost phases.
A raw same-object overwrite is included in the last cycle before its first fork.

Collision family: use N closed-domain c-names with constant hash0. First perform
the growing fork-after-each-write schedule, including fresh equal-key lookups
at indices0,N/2,N-1 and a missing comparand. Then three cycles overwrite c0,
delete c1 and reinsert c1, forking after each mutation. Bulk-build a detached
version from the reversed c-name sequence, with the same projected values and
raw/pending metadata. Join it with the final cursor snapshot using the builtin
reference algorithm; retain old snapshots and measure first/repeated ordered
reads and historical audit. N=64 exceeds the proposed leaf threshold but this
oracle does not assert a particular internal node shape. Actual collisions and
all charged/comparison work must be disclosed. These cases have no favorable
subquadratic growth requirement.

Bulk family: each of four rounds builds a fresh detached version of the same N
u-names. Form input name order using the child builtin set-union algorithm from
ascending and descending reference dictionaries, with their insertion rotations
by the round number. Expected values are token v_(floor(round/2),index): rounds0/1
share value identities, as do2/3. Even rounds certify indices not divisible by3;
odd rounds mark every entry pending. The factory sees the completed immutable
unique (name,Entry) sequence; input preparation is not factory work.
Immediately read keys and ordered_items after EACH build, then repeat the final
reads. Retain all four results and audit earlier identities. Finally join
round2 and round3: all names must be considered pending because round3 is raw,
even though values are identical. Verify callback tuples and exact legacy order.
At N32 only, add a separate invalid-boundary phase for a duplicate pair and a
malformed pair: require ValueError/TypeError respectively, preserve inputs and
earlier results, record consumed input/charges, then complete a valid build.
These boundary operations are not included in the bulk growth metric.

Direct retention I11: build64 ambient harmless entries, then place two fresh
weak-reference sentinels under victim-overwrite and victim-delete. Publish and
retain exactly one old snapshot as an explicit positive owner. Drop local strong
sentinel references. Overwrite the first victim with a fresh current token,
delete the second, then perform exactly one successful changed publication.
Keep the current cursor and new snapshot; verify their replacement/absence.
The old snapshot must still return both original objects while it is retained.
Release that last old snapshot and collect; BOTH obsolete weak references must
be gone while current cursor/new snapshot remain usable. No input tuple, prior
cursor, saved item tuple, oracle registry, diagnostic frame or logger may retain
the victims. Record public successful changed publication and actual reviewed
replacement accounting. This proves that a retaining current path/leaf/history
did not survive the replacement; it does not rely on a layer-compaction label.
Afterward perform a new insertion/fork and repeated order reads to establish
continuation. Keys-only history is allowed to remain; obsolete values are not.

## Explicit successor for the layer-specific old retention trigger

Independent source inspection confirmed cursor-oracle-v1.py:368-380 requires
compaction_entry_visits>0 and raises UnmetStructuralPrecondition otherwise.
That was an appropriate reachability trigger for the selected eight-layer
prototype, not a generic semantic requirement that every map must compact.
Do not fabricate that counter, force obsolete full compaction solely for the
oracle, or silently mark the unchanged run as a pass.

The coordinator authorized a create-only cursor-oracle successor. Preserve the
old casepack, all24 overwrite/publication operations of
cursor-history-retention-after-compaction, retained-old positive ownership,
current-value identity, drop-last-owner weakref release and subsequent reads.
Replace only the structural trigger with completed changed publication(s),
current replacement identity, and explicit owner accounting. The original
saved snapshot is the positive control; after releasing it, no other object
except current versions/cursors/history may own the sentinel, and the weakref
must disappear. This is a direct lifetime proof, independent of path shape.

Keep optional raw compaction counts as descriptive evidence if present, never as
an invented prerequisite. The new stronger one-publication I11 control separately
prevents24 later unrelated changes from masking obsolete-value retention.
The exact future successor diff must be reviewed before execution. Report61
unchanged old run paths plus this one semantic-preserving trigger successor,
not62 byte-identical executions. Original oracle/data/results remain immutable.
No other old assertion, fault schedule, API behavior or expected output changes.

## Atomicity/retry family

Use one finite preparation: bulk-build64 u-names plus16 closed-domain c-names.
Create a cursor and retain its original snapshot, keys view and item tuple as
old witnesses. Apply unpublished overwrite u0, delete/reinsert u1, overwrite c0,
and insert the new collision key c16. This requires real changed data and order.
I12-I15 target the named cursor primitive. For I16 the target is a fresh bulk
factory call on the resulting immutable entry sequence in independent expected
order; it has no mutable receiver. Its source sequence is retained unchanged.

For each target, calibrate only the primitive call: read Meter.used/counts just
before and after. Do not include len, content checks, returned-view iteration,
or any later validation in that delta. Require a positive actual cost C.

Rebuild preparation independently for each replay. Lower the existing meter
limit to used_before +0, +floor(C/2), or +(C-1). The target must throw the public
BudgetExceeded and retain all spent/throwing charges. Restore only the permitted
262144 limit, without refund/reset. Retry the SAME failed cursor for I12-I15,
or a fresh iteration of the SAME immutable factory input for I16. Exact retry
used-unit delta AND every per-category delta must equal pristine C/counts.
A failed read may not publish data, history, order or item caches that make its
retry cheaper. A failed factory may not publish a global/shared memo.

Then run the same finite continuation for pristine and replay: derive a cursor
from the successful result where appropriate, fork it, raw same-object overwrite
u0 on the parent, delete/reinsert u1 on the child, publish both, join their
snapshots, read keys/items twice, and re-read original retained witnesses.
Compare every continuation primitive's output, value/proof behavior, cost and
category delta with pristine. Validation remains separately charged/labeled.
For keys/items targets the current cursor is the continuation source; immutable
returned views/tuples remain additional witnesses. Existing normal missing-delete,
cross-meter and mutable-join boundary tests retain their old role.

Only these five targets and three offsets are admitted here. No exhaustive
fault fuzzing, write-rollback contract, arbitrary callback side effects or
hostile iterator transaction is inferred. Incomplete infrastructure is not a
storage failure; BudgetExceeded from an intended unmodified-budget primitive
is real bounded-work evidence, classified separately from semantic wrong output.

## Accounting and frozen finite growth classifications

Before any payload, coordinator/source review must bind each actual Meter
category to a physical operation class. Capture all categories, including
allocation/wrapper/reference work, private writes, dictionary attempts,
entry scans/copies, branch-child references, pending metadata, history,
index routes/hash requests, order realization, returned copies, and publication.
A new empty/miscellaneous category cannot make work disappear from totals.

Define P for a phase as the sum of its actual entry/reference visit-or-copy
events: old backing entries revisited/copied, index child references visited/
copied, pending/history/order entries visited/copied, and newly stored entry/
reference writes. One physical event is classified once, not under multiple
labels. Allocations, lookup/hash/dictionary attempts and wrapper work remain
reported separately and remain in C, the FULL Meter.used delta for that phase.
These are same-candidate metrics, not a conversion of old dict-copy entries into
new node counts. Actual event mapping needs static review, not observer guessing.

Meter.counts deltas must account for all C units at their declared granularity.
Independent iterable/key-protocol observer counts are separately labeled and
are not presented as charged units. A requested throwing charge remains counted.
Report construction, mutation, publication, lookup, join, first ordered read,
repeated read, historical audit, invalid boundaries, failures and continuation
separately, plus the complete per-case total. No terminal or retained audit cost
is omitted merely because it spoils a favorable mutation result.

The following are finite FITNESS falsifiers, frozen now, not universal complexity
theorems or new semantic admission caps:

| Comparison | Required finite growth for favorable indexed-storage fitness |
| --- | --- |
| Growing family,32->128->512 | For each adjacent4x N, mutation+publication P and C grow by at most8x; independently the first terminal keys+items P and C grow by at most8x. |
| Hot family, ambient32->512, fixed32 cycles | Mutation+publication P and C grow by at most8x despite16x ambient size. Setup and terminal costs remain separately reported. |
| Bulk family,32->128->512 | For each adjacent4x N, total four factory builds plus their immediate first keys/items P and C grow by at most6x. |
| Collision16->64 | No favorable-growth threshold; exact semantics, actual collision activation, complete charge/comparison disclosure and original-budget result are required. |

For P use larger <= factor * max(smaller, smaller N); for C use larger <=
factor * max(smaller,1). This fixed small-denominator rule is part of the freeze,
not fitted to a result. Report raw metrics and each ratio/inequality, including
failures; do not replace them with a single total-pass label. Repeated/historical
reads and all other phases stay in the complete total even where no standalone
ratio is prescribed.

For each successful bulk call also require actual input visits=N, staging
uniqueness attempts=N, and final order writes=N. Input iterator is entered once.
The static accounting map must confirm no repeated immutable-set build or
predecessor index absence lookup was hidden under route/allocation names.
Actual routing/splitting can revisit entries and is charged, not falsely forced
to zero. The finite6x criterion allows bounded radix routing overhead; it does
not assert an implementation-independent constant-time operation.

These deliberately loose8x/6x comparisons distinguish the measured near-quadratic
growing-prefix mechanism (about16x under4x N) from the targeted bounded indexed/
bulk behavior without selecting a leaf threshold or favorable seed. A threshold
failure is evidence that this candidate has not demonstrated the proposed fit,
not automatically an incorrect dictionary result. No threshold is revised after
opening results. If a case hits262144 before completion, preserve the partial
phase ledger, name the exhausted phase, and mark its growth comparison incomplete;
do not extrapolate a missing total or call the case passed. Root decides any
further run after reviewing that failure.

## Dispatch gate and limitations

This is the completed pre-source schedule/oracle-requirement freeze. Prototype
authoring still requires the coordinator's review/authorization. Executable
oracle, neutral successor, prototype, accounting map and isolated controller
must be separately pinned and read before any payload. Dispatch remains serial,
root-owned, floor first, fresh snapshots, seeds0/1/17, existing identity/env/
watchdog/custody rules. No author dispatch, source patch, cap edit, owner/GPU,
broad suite, install, ledger or commit is authorized.

If API expectations conflict with this note, resolve them in a new version before
source; preserve these bytes. Do not retrofit oracle outputs to implementation.
A pure93-run child can support storage semantics and these finite cost claims
only. It cannot prove actual resolver transfer/cell order, class behavior, full
corpus budget fitness, runtime speed ratios, universal collision behavior or
general memory reclamation. Exact original depth cases, design/matrix/public24,
ordinary generation and later approval gates remain separate required evidence.
