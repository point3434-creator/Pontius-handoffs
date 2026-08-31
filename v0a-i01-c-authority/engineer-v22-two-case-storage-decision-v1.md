# v22 two-case storage fitness: diagnosis and bounded next decision

Status: read-only engineering recommendation; no candidate, payload or cap change.
Source: engineer-generator-v22.py SHA
61a0ce3bc3ea59bc09a7b14d45da843fb3c3a8614feb4c913132b67028916da3.
Both logs were independently parsed; diagnostic completion is not a product pass.

## What the two traces establish

helper1050 receipt 7ebaa9657dbd47f91ecad3d5f20c18930a84b746d05feda356b8bc21247bcfe2;
stdout 1fae6fe81c2b4bf99e6732b001cdfa9be6b756e452f2f4f4b1b4008be331a27f.
Its only original budget fails at 262143+2, registering helper_540 in
_definition_time_protocol_resolver, with disabled authority, evaluation depth0
and zero active helper/deferred sets. Publication117670 + compaction93844 =
211514 (80.69%) charged units. There are544 completed changed publications,
1089 fork requests,67 completed full compactions and an interrupted68th;
18241 compaction-entry visits and18703 seal/pending-entry visits.
The nearest-phase publication bucket includes sealing after compaction.
This is repeated growing-prefix copying, not deep helper execution.

generator70 receipt bbb9b75f161f7d9a06f1295d5cf3ae5a62ba11f1dfe1e01f152fb9d246059f57;
stdout e640909ca295f7f0ebbcd67f13de183a433efb0120db815755f513b8c922bcb4.
Epoch6 fails at262143+6 inside receiver preflight, creating the GeneratorExp
at line53 (g48), evaluation depth2 and zero active consumption/helper sets.
Ordering89193, assignment67584, lookup37727, publication31750,
state-join22560, compaction2616. It completed145 state merges but no
_version_join calls;94 keys reads,98 items reads,94 snapshots,95 changed
publications. Full legacy rematerialization and demanded-order work dominate.
This does not measure recursive consumption at depth64.

Both are real charged-budget regressions under unchanged caps. They do not
establish runtime ratios, enabled-corpus fitness, or that the five caps are wrong.
helper1050 accepts a depth OR budget category; changing its message now would
conceal this diagnosis, not establish storage fitness.

## Recommendation

Do not port another candidate yet. A plain disabled dict/COW backend alone is
not sufficient evidence of a remedy: first write after each real fork copies
the growing N-name dict, again quadratic for sequential declarations.
v19's uncharged dict.__init__(result,self) copies cannot be our cost baseline.
A disabled-only backend also adds mode/adoption conversion obligations.

The next bounded experiment should replace only name lookup storage with
a genuinely indexed persistent chunk map, plus linear bulk building at the
already-required full-merge boundary. Retain the cursor/version ownership,
name-only histories, exact order recipes, proof/pending contract and the
old authority/object/cell/results/observations. No resolver-control rewrite.
This is an isolated prototype decision, not authorization to integrate it.

Concrete candidate shape: a 16-way hash-radix index with immutable branch
nodes (bitmap + packed child tuple), and small immutable dictionary leaves.
Split a leaf above a structural size threshold such as16 using successive
4-bit hash groups. Hash-width exhaustion uses an ordinary collision dictionary,
with every actual traversal/copy charged; it never refuses on a storage limit.
Keep each leaf's effective pending-name metadata alongside that leaf.
Publication copies only touched index paths/leaves, sharing untouched siblings.
The cursor retains private writes until actual fork/snapshot as today;
staged publication may reuse exclusively owned temporary paths for multiple
writes but must expose no mutable alias or publish before all charges succeed.

This addresses helper1050's mechanism: insertion into a new name no longer
copies/reseals every earlier name merely because eight publications occurred.
Ordinary reads visit a bounded hash path and one leaf instead of probing
each historical layer. Worst case remains explicit: hash-depth is bounded by
hash width, and a fully colliding bucket can require linear copying/search;
there is no blanket O(1), cap-fit or favorable-hash-seed claim.

For generator70, use an internal unique-entry bulk builder at the exact full
fallback and construction seams. Preserve the legacy set-union name sequence,
flow merge, full transfer, and strong/weak cell writes in their original order;
collect final entries, then build the name index and one known-order dictionary.
Do not create an insert recipe and perform an absence lookup for each known
unique output key. Bulk building must charge every entry, route, dictionary
write/reference and allocated node; staged order is published only on success.
Existing _merge_flow_values and transfer/cell operations do not read the
partially built projected name map, as the earlier construction inventory shows.
Plain mappings, disabled inputs, overlapping/missing cells and exact-order
fallbacks retain their semantic route. This is not disabled no_work certification.

## Costs and invariants that cannot move

A fork shares an immutable root; a changed publication pays for dirty entries,
path traversal/copied child refs/leaf copies, pending metadata and plan/wrapper.
Frequent forks still incur those real costs. No amortized refunds or omitted
copies; report construction, mutation, publication, full/sparse join and terminal
ordered-read costs separately. Indexed lookup is not a promise the whole
analysis fits; full joins still cost at least their supplied names and transfers.

On overwrite/delete, the current root must cease owning the old leaf value
except through legitimate retained snapshots; history/order ancestry stores
names only. Do not keep an obsolete large backing layer until enough unrelated
writes arrive. This is why size-tiered/LSM compaction alone is not selected:
it risks delayed stale-value retention and still needs a separate lookup index.

Ordered keys/items keep exact legacy union and delete/reinsert order.
Changing hash layout never changes observable iteration or cross-name
authority/cell sequencing. Entry no_work requires the same four-fact proof;
disabled entries remain pending across enabled adoption.
Raw same-object writes invalidate proof as before. Live wrapper views remain
live, immutable snapshots remain stable, and meter/context ownership cannot mix.
Failed ordered read/snapshot/fork must leave all backing/history/memo state
unchanged: exact retry and short continuation must match pristine charged work.

Rejected without a separate ownership proof: return the singleton successor
wrapper directly or consume _flow_expression_statement's input. The resolver's
_current_effect_values, exception pre-states, enclosing values and retained
states can observe that input; distinct Python wrappers alone do not prove
the backing name map is exclusive. Refcount/GC heuristics are not a proof.

## Bounded falsifiers before any production lease

Preserve all372 existing pure-oracle/retention/failure-atomicity obligations.
Add only bounded storage schedules that expose growing unique inserts with
fork-after-each-write, hot overwrite/delete/reinsert, retained old snapshots,
collision buckets and full unique-key bulk construction. Compare visited/copy
growth over increasing N; count every retained audit and terminal realization.
Require semantic/order/proof parity and all failed-read retry invariants before
porting. Then the two exact original floor cases, remaining focused gates,
public24, and ordinary live generation remain separate required evidence.
A small pure prototype win cannot authorize a corpus claim.

Stop if indexing requires changes outside the name-store/adapter boundary,
if exact ordering or pending projection needs weakened semantics, if collision
handling cannot remain bounded by the original analysis budget, or if complete
charged costs still dominate. Do not start another chain of threshold tuning.
