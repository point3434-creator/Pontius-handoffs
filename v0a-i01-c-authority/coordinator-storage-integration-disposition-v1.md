# Coordinator storage-integration disposition v1

2026-08-31. Continue the existing C authority FIX in its isolated worktree.
This is an engineering decision, not a cold verdict, acceptance, or permission
to integrate main. The prior bounded design remains the scope authority.

The reviewed prototype is engineer-storage-prototype-v2.py, SHA-256
22cc3966435fd4e6e0cecbcbb242275e72d34b36c835b4e960c7c712613822ff.
The independently authored oracle and case bytes were pinned before execution:
oracle6a58ef82832d53510f7d44d58cf5a8fa3764f8be5f2c28dcb7e555a83c72cfba;
cases3bd5678da334fb551c2f179906e8b4d2cf7a0b0e7a3779e0fad2fb4b4a9c548f.
Root inspected both, corrected a measurement-boundary defect in the unexecuted
oracle v1, and inspected control v2 before dispatching six serial children.
Actual3.11.15 seeds0/1/17 preceded actual3.14.6 seeds0/1/17.

All204 checks completed without failure. Root independently rehashed every
snapshot, log, receipt and input, verified retained-case preservation, and
compared complete same-seed observations and costs across interpreters.
Coordinator receipt: coordinator-storage-verification-v1.json, SHA-256
e77700c7f8ee03cfb7c16cc590ba561454956e6e7410a692542e6091975ef381.
Production remains exact v19 at this decision point:
3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1.

The later storage-oracle-plan-v2.md is post-execution documentation. Its
statement that no payload had run at issuance is stale and is corrected here;
its hash is not a preregistration hash for these runs. The earlier bounded
disposition, fixed case/oracle/control bytes and root dispatch record establish
the actual pre-run scope. All issued predecessor bytes remain retained.

The optimistic operation is demonstrated: zero-change name joins cost36 units
per join at both8 and64 ambient names. Deferred work remains visible. At64
names, construction costs10909/10911 for two/four joins; first terminal order
costs3459/5211, repeated reads260, retained-version audits2470/4810. Total
costs17183/21357 include validation. These are pure-storage workloads, not
the public analyzer or a before/after corpus benchmark. They justify trying
the bounded port; they do not establish corpus headroom.

Static adapter inventory9617c9b5d9d502a707e124483586b59488f7b1ec670d3f375f0615132a762180
found no current consumer requiring live values/items during same-map mutation.
It does identify exact alias ordering, raw projection, semantic deletion,
constructor Mapping input, and state overlay versus replacement obligations.
Object-order note748e19189c35865cf9d486c48557a7ed60d6c60c2893815f2b0c4961b779033d
supports reordering independent registrations only up to consistent opaque-ID
renaming. Explicit refs, retained/cell tuples and first-owner traversal order
remain observable and must be preserved. Foreign fabricated forward IDs are
outside this internal-state proof. Public falsifiers remain required.

Authorize one bounded production port in
D:/Pontius-worktrees/codex-v0a-i01-c-authority-v1/tools/generate_test_inventory.py.
The engineering agent owns this one source write surface until it returns the
v20 patch; root will not write it concurrently. No test or generated-output edit
is included in this lease. W must be checked against the exact predecessor
before editing, and the exact resulting source/full patch/static checks must
be retained under new T filenames. No payload execution before root review.

Carry forward coordinator-storage-disposition-v1.md in full: immutable AVL
names and exact lazy order, the narrow completed-transfer no-work certificate,
raw installations pending, unchanged transfer/cell semantics and all five caps.
Map the prototype meter's semantic storage charges to the original budget;
do not silently discard costs or claim allocator-perfect CPU accounting.
Preserve v15-v18 corrections and the shared cell-write helper. Retire v19's
sparse planner only when the replacement owns its complete merge behavior.

Use the optimized join only for compatible execution states. A plain Mapping
input must retain its original full path; converting extra inputs into states
must not introduce new transfers. Keep full ordered fallback for overlapping
or missing cells. Every participating bound-name write remains, even when
name versions are identical. Preserve authority-only adoption and raw timing.
Do not change object/cell/result/observation map representations in this port.

Then root reviews the combined diff and preservation census. Run the frozen
public24 family with representation-correct counters and terminal reads,
design53, matrix192/212 and the required supplemental controls on the floor
first. Only ordinary generation under the unchanged caps can establish corpus
GREEN. A failure requires diagnosis of that exact candidate, not a cap increase
or another independent store rewrite. No broad CPU wall or cold-review claims
are authorized by this disposition.
