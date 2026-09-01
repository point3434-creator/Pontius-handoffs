# Freeze-tools design r001 state-machine audit

Advisory author: `/root/freeze_tools_state_machine_audit`

Status: **ADVISORY / NON-GATE** — this is not either required cold verdict.

Candidate commit: `ad8fbcc1ae5a9e3c3b61ae93d5ae5c0b3e4d289e`

Manifest SHA-256: `862d245f838f4b7459b6ce2aae19eede3b77a4861575722817db12d63af7b689`

Advisory audit of candidate `ad8fbcc1ae5a9e3c3b61ae93d5ae5c0b3e4d289e` found six state-machine issues. This is not either required cold verdict.

1. **Important — Main publication cannot preserve concurrent packet histories. High confidence.**

   Frozen locations:

   - `docs/superpowers/specs/2026-09-01-raw-object-workflow-amendment-v4.md:131-142` makes each packet commit a single-parent child of its candidate.
   - Same file `:217-225` makes the main-publication commit a child of that packet.
   - Same file `:261-267` permits unrelated tasks to advance main but requires the current integrated packet to remain an ancestor.
   - `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-git-boundary.md:326-337` force-updates main under an exact lease.
   - `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-design.md:123-129` requires unrelated-main preservation.
   - Pinned workflow `inputs/workflow.md:436-449` requires append-only packet publication and later reachability.

   Scenario: task A publishes `I_A`, whose only ancestry is `I_A -> P_A -> C_A`. While A’s reviews run, task B publishes `I_B -> P_B -> C_B`. The explicit lease protects the expected tip but permits this non-fast-forward replacement; Git documents that behavior for `--force-with-lease`. `I_A` is no longer an ancestor of main, so A’s finalizer must refuse forever under amendment line 262. Its integration receipt may also become remotely unreachable before A’s output refs exist. Copying A’s tree into B’s commit cannot repair ancestry, and making `I_B` a child only of `P_B` cannot retain `I_A`.

   Required outcome: define a graph that preserves both fresh-main ancestry and exact packet ancestry. A two-parent integration commit with fresh main as first parent and the exact packet as second parent is one coherent option; it requires replacing the single-parent-only verifier with explicit first-parent and packet-parent rules. Alternatively, parent the integration commit from fresh main and retain packet authority permanently under another exact ref, then amend every ancestry and retirement predicate consistently.

   Verification must interleave two tasks’ packet integration, reviews, lost acknowledgements, and finalization in both orders and prove neither task’s ancestry, subtree, or ability to finish is lost.

2. **Important — The five-state alphabet cannot represent valid main descendants or descendant-after-lost-ack states. High confidence.**

   Frozen locations:

   - Design `:128-129` allows unrelated single-parent main descendants.
   - Design `:174-185` defines only `ABSENT`, `EXACT`, `PARTIAL`, `DIFFERENT`, and `UNKNOWN`, and permits only exact state to close a lost acknowledgement.
   - Runtime appendix `:197-203` says authorization binds an exact predecessor and any changed predecessor refuses.
   - Git appendix `:306-308` defines fetching a freshly observed main descendant.
   - Amendment `:261-266` treats an integrated-packet descendant as acceptable later main state.

   Scenario: authorization binds main `M0`; another task advances main to valid descendant `M1` without changing this task. The design says `M1` may be accepted, while the runtime rule says changed predecessor must refuse. If implementation silently treats `M1` as `EXACT`, it broadens exact authorization to an unbound OID. After a successful push whose acknowledgement is lost, an unrelated commit `U` atop the integrated commit similarly becomes `DIFFERENT` under the stated definition, so recovery cannot recognize success.

   Required outcome: add main-specific states such as exact predecessor, allowed predecessor descendant, exact result, allowed result descendant, protected-subtree conflict, and unknown. State exactly which observations require fresh controller authorization and which close a lost acknowledgement. Every lease must still bind the exact observed OID.

3. **Important — Retirement creates an ABA replay hole for “one-use” publication authority. High confidence.**

   Frozen locations:

   - Design `:69-72` and runtime appendix `:168-180,197-203,485-491` call the dispatch/authorization one-use.
   - Design `:174-189` and amendment `:182-203` authorize creation whenever the pair is `AA`/`ABSENT`.
   - Amendment `:273-295` later permits both candidate and packet refs to be retired.
   - Git appendix `:274-282,339-341` queries only the live pair and rejects unenumerated routes; it cannot observe an archive, disposition, or spent marker.

   Scenario: authorization `A` publishes the pair, integration and disposition finish, and both live refs are lawfully retired. Replaying the identical `A` now observes `AA`, which is indistinguishable from never-published initial state, and recreates the retired refs. The nonce is per launch and supplies no durable consumption state.

   Required outcome: preserve a permanent monotonic spent/retired marker visible to the publisher, make initial publication atomically create that marker, or prohibit deletion of the create-authorizing refs. Post-retirement replay of the exact authorization must make no push and return a distinct terminal `SPENT`/`RETIRED` result.

4. **Important — Fresh-repository adoption has no role that owns the complete transition. High confidence.**

   Frozen locations:

   - Design `:104-113` gives local object/ref creation to the offline builder.
   - Design `:115-121` denies building to the network publisher and requires it to begin with an accepted local graph.
   - Runtime appendix `:168-203` permits only builder, publisher, and integrator checkpoints.
   - Git appendix `:293-304` defines a network adoption fetch.
   - Runtime appendix `:547-551` and amendment `:205-209` require fresh-repository recovery ending in transactional local authority refs.

   Scenario: a fresh repository has no local objects or authority refs while the remote pair is exact. The publisher cannot pass its accepted-local-graph precondition; the builder cannot fetch; and no adopter role exists. Letting the publisher fetch and create local authority silently adds builder authority to the publisher. Keeping the stated roles leaves recovery permanently blocked.

   Required outcome: specify an exact, authorized adoption transition. For example, a network role may fetch expected objects as nonauthority residue, followed by an offline adoption/build authorization that validates the complete graph and transactionally creates the local tuple. Define all crash, partial, and lost-ack states across that handoff.

5. **Important — GCM is allowed a durable mutation that the publisher contract forbids and the state machine does not classify. High confidence.**

   Frozen locations:

   - Brief `docs/briefs/v0a-i01-freeze-tools-r001-brief.md:39-51` limits publisher mutation to the exact ref pair and requires failures to preserve authority.
   - Git appendix `:110-144` explicitly permits GCM `get`, `store`, and `erase`, and itself says a separate credential-preauthorization design is needed if mutation is forbidden.
   - Design `:115-121,172-189` models only repository/ref mutations and their recovery.

   Scenario: a read-only query or failed push invokes GCM `erase`, deleting a usable credential. The pair remains `AA` or becomes `UNKNOWN`, yet a durable out-of-scope mutation occurred and future noninteractive operations may fail indefinitely. No receipt or state class records or reconciles it.

   Required outcome: use the separately reviewed credential-preauthorization route contemplated by the appendix, or explicitly amend the publisher authority and state model to cover exact credential mutations. Merely recording side effects in rehearsal does not satisfy the current “only the pair” criterion.

6. **Medium — The complete local atomic tuple is inconsistent about intent refs. Medium-high confidence.**

   Frozen locations:

   - Design `:104-113` and brief `:36-38` include local intent ref(s) with candidate and packet anchors.
   - Amendment `:59-62` transactionally creates only the candidate ref and packet anchor.
   - Amendment `:144-147,175-180,205-209` and runtime appendix `:197-203,526-530` later require exact builder intent.

   Scenario: an implementation follows the amendment’s two-ref transaction and creates the intent ref separately. A crash can leave candidate/packet exact but intent absent. Pair-only recovery may report exact success while publisher authorization cannot bind the required intent; the opposite ordering can leave intent-only residue with no defined classification.

   Required outcome: enumerate every governed local ref, including exact intent-ref names, and create/classify the complete tuple in one `update-ref` transaction. Recovery succeeds only when every member and graph binding is exact.

All handoff, workflow, runtime-closure, and five candidate hashes matched their frozen declarations. Evidence was limited to read-only Git blob inspection, JSON parsing, and primary Git documentation; no mutable files, formal review outputs, runtime, tests, or refs were read or changed.
