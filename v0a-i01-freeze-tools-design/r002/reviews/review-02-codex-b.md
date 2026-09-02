Reviewer ID: codex-b
Candidate commit: 48e590327c0a4bfd7ea5019e6770e1d582182b08
Manifest SHA-256: 010e96031f60afd8badc07ebb4dd97ab8db4102527be0eb42ee56c2d65e7c984
Defect verdict: NOT CLEAN
Design verdict: STRAINED

# Formal cold Tier-C design review

## Scope and identity result

I reviewed the complete six-document frozen r002 design against the immutable
handoff, adopted workflow, runtime closure, rejected r001 source population,
r001 disposition, and r001 consolidation permitted by the packet. The frozen
candidate ref resolved to the OID above, with sole parent
`d1ed3cbda6107d61ea8e77133871720af04970cd`, tree
`27e0503a7f6f4efd44122078aeab62f3151420d5`, and exactly six add-only mode-100644
paths. The base contains none of those paths. I independently reproduced all six
blob identities and the candidate manifest digest. I also reproduced the five
r001 blob identities and r001 manifest digest, and verified the permitted packet
input hashes and runtime-closure cardinality of 2,614 files and 63,499,244 bytes.

This was read-only specification inspection. I did not execute the pinned
runtime or a candidate artifact, run implementation tests, query or mutate a
network service, inspect mutable drafts or retained evidence, or read a peer
report.

## Independent inventory recorded before deferred coverage

I fixed my independent governing-invariant and related-path/seam inventory
before opening `coverage.md`. The fixed standalone artifact is
`D:\Pontius\tmp\freeze-tools-design-r002-review-codex-b\initial-inventory.md`,
11,048 bytes, SHA-256
`e140a2a7fe05e21548468b12331fe8f5ba2d149343c2fa8509635a83fa6de4a2`.
The following is the inventory included in this report, condensed only to avoid
repeating identity rows.

### Governing invariants

1. Authority and provenance are closed: every transition has a complete
   canonical preimage, one issuer, one digest relation, and no after-the-fact
   synthesis of reviewer testimony.
2. The bootstrap DAG is acyclic and reachable: the utility cannot authorize its
   own design, and every required bootstrap artifact is producible from the
   immutable handoff by its named issuer.
3. Reviewer/output cardinality and issuer attribution are exact: two reviewers,
   two reports, two issuer-authored lines, with one unambiguous grammar and all
   required preimages available before bytes freeze.
4. Role authority is closed before execution: each role has a finite input,
   operation, source, dependency, argv, and result vocabulary, with builder-
   loaded code physically unable to reach network or main authority.
5. Reviewed source, native dependency, loader, namespace, runtime-data, file-
   identity, process, handle, environment, and final-revalidation populations
   are complete; post-load inventories are secondary evidence only.
6. Raw blob, tree, commit, and manifest construction is byte-deterministic and
   cannot inherit identity, time, ordering, normalization, config, index,
   attribute, or filter state.
7. Local authority tuples and remote pairs change atomically under exact
   create-only or leased transitions; every partial, different, unknown, and
   lost-ack state remains distinct and monotonic.
8. Main transitions preserve fresh-main and designated packet/publication
   history, distinguish predecessor and result descendants, protect the frozen
   subtree, and require fresh authority after an unapproved change.
9. Fresh-repository adoption divides network residue from offline authority;
   neither publisher nor builder silently acquires the other's capability.
10. Durable credentials are monotonic across success, refusal, timeout,
    cancellation, and lost acknowledgement; no accepted branch stores or erases
    ambient credential state.
11. Every claimed accepted operation/result equation is exercised through its
    actual public supervisor, Git, helper, credential, HTTPS, observation, and
    cleanup route. A shared helper, local transport, or structural table
    equality cannot stand in for an omitted operation.
12. Process, transport, cancellation, output, storage, residue, and cleanup
    semantics are finite, measured, sticky, and independently observable.
13. Every schema field, union branch, digest preimage, equality, receipt,
    carrier, publication, and result edge is typed, reachable, unambiguous, and
    acyclic across all six documents.
14. The complete candidate, not only the r001 correction rows, remains subject
    to adopted scope, hygiene, slice, blind-review, fixed-byte, and append-only
    workflow rules.

### Related-path and seam inventory

| Seam inventoried before coverage | Cross-document path followed |
| --- | --- |
| Current design-review output production | Handoff output contract and Stages 3-5 of the adopted workflow against the brief's bootstrap review plan, central design bootstrap section, amendment bootstrap route, and `pontius-utility-bootstrap-design-review-*` schemas |
| Future utility review provenance | Brief cardinality, runtime receipt bindings, report/receipt/manifest/publication schemas, self-exclusion, and reviewer/author distinctness |
| Role surface versus loaded dependencies | Central role sections, Git operation/argv tables, runtime source projections and AST graph, schema role-operation and schedule sets |
| Campaign membership versus accepted operations | Central test claims, Git HTTPS rehearsal, runtime `RUN-*` gates, schema campaign step membership, finalizer, and disposition operations |
| Main graph and review publication | Amendment transitions, Git integration/finalizer/disposition paths, commit/tree schemas, and predecessor/result observations |
| Fresh adoption and local tuple | Publisher fetch, offline adoption, local transaction, authorization/receipt schemas, and every subset state |
| Remote live/archive state | Pair publication, permanence/replay, observation algebra, leases, and spent evidence |
| Runtime pre-execution enforcement | Native launcher, AppContainer, CPython archives, loader policy, held projection, lock/attach handshake, and final reconciliation |
| Commit/tree determinism | Raw-object amendment, offline builder Git boundary, schema byte grammars, metadata, parent and entry ordering |
| Error/reconciliation algebra | Per-operation result equations, timeout/cancel/job behavior, waiting records, attempt identity, and lost-ack recovery |
| Credential and campaign containment | Askpass/broker lifecycle, profile/netrc closure, production-ref exclusion, case namespace, storage residue, and post-case observations |
| Normative consistency | Every literal, field set, operation name, cardinality, digest relation, artifact path, and required publication repeated across the six documents |

The initial adversarial questions specifically asked whether the immutable
packet lets both reviewers produce every schema-required current-bootstrap
artifact without coordinator invention, and whether review finalization and
disposition publication are actually dispatched by the real-HTTPS campaign.
Both questions preceded and then falsified the deferred claim.

## Coverage comparison

The deferred claim is coordinator evidence, not a verdict. Most of its member
inventory usefully expands the r001 correction matrix, but it misses or masks
two material members already named above.

| Independent seam | Deferred claim | Comparison result |
| --- | --- | --- |
| Current design-review output production | `coverage.md:765-775` asserts that each reviewer publishes a typed receipt, report, and line and that the controller joins two typed publications. Its own falsifier at `817-825` rejects a missing object, artifact, count, digest, or rewritten issuer output. | Falsified. The actual immutable packet supplies no canonical series-state artifact or design-packet publication-object digest, assigns no receipt artifact, and requires a different line grammar. The claim repeats the prospective schema instead of showing that the current rule-6 issuer can populate it. |
| Accepted operation versus real-HTTPS campaign membership | `coverage.md:256-274` says the campaign exercises mutations through the same Git/process/askpass/credential/reconciliation route; `R2-19` names finalizer and disposition staging. | Falsified. The normative campaign schema excludes both accepted main-publishing operations, so shared tables and staging assertions replace public-boundary execution of their distinct authorization, overlay, lease, and result paths. |
| Remaining inventoried authority, runtime, object, tuple/pair, main-history, adoption, credential, lifecycle, and storage members | The claim supplies typed mechanisms and falsifiers across R2-01 through R2-26. | No additional Critical or Important contradiction was established by this read-only pass. That is not executable proof; the frozen design itself defers native, Git, server, and calibration evidence to implementation. |

## Findings

### CB-01 — Current bootstrap review outputs cannot satisfy both the packet and the normative schema

Severity: Important
Confidence: High

Exact frozen locations:

- immutable packet
  `v0a-i01-freeze-tools-design/r002/handoff.md:128-155` at
  `14c1f5629024973b96f71c64a04f17ce9d7e01e2` requires each report to contain
  five named fields exactly once and, after the report freezes, one issuer line
  containing date, round, reviewer, both outcomes, candidate, manifest, report
  path, and report digest;
- candidate brief
  `docs/briefs/v0a-i01-freeze-tools-r002-brief.md:291-301` says this review also
  returns a typed bootstrap receipt and is joined as a typed publication;
- central design
  `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-design.md:195-205`
  makes the same claim for this r002 review;
- workflow amendment
  `docs/superpowers/specs/2026-09-01-raw-object-workflow-amendment-v5.md:111-123`
  requires that typed receipt, while `:800-813` says current reviewers publish
  reports and lines through the already adopted rule-6 route;
- schema appendix
  `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-schemas.md:7106-7162`
  requires the reviewer to supply a receipt containing a complete canonical
  series-state artifact/count/digest and a design-packet publication digest;
  its exact report prefix adds the packet-publication digest, state digest, and
  ordinal; its exact line order is reviewer, ordinal, candidate, manifest,
  report digest, defect outcome, design outcome; and its publication population
  is receipt, report, and line;
- the same schema at `:7209-7261` makes two such publication digests mandatory
  inputs to the controller disposition; and
- immutable packet tree at the handoff commit contains only `candidate.json`,
  `manifest.sha256`, the six-source pointers and permitted inputs, `coverage.md`,
  `handoff.md`, and a forbidden check. It contains no canonical series-state
  artifact or complete design-packet publication object whose digest a reviewer
  can reproduce.

Concrete inputs/state-to-wrong-outcome scenario:

1. Both cold reviewers start from the exact immutable packet and follow its
   issuer contract, as required.
2. Each fixes a report and emits the packet-required one-line record with date,
   round, report path, and report digest. Neither can truthfully name the absent
   canonical state artifact or complete design-packet publication-object digest,
   and neither has been assigned a receipt artifact.
3. The strict parser at schema lines 7125-7149 rejects both reports and both
   lines because the report prefix and line field population/order differ. No
   typed review publication can be formed, so the controller cannot form the
   disposition or the only implementation-opening authorization.
4. If the coordinator instead invents the missing reviewer receipt, state
   identity, ordinal-bearing line, or rewritten report bytes, it violates the
   issuer-only line rule, attributed human assertions, fixed report bytes, and
   the candidate's own prohibition on invented or rewritten review members.

Violated invariant:

The bootstrap/evidence DAG must be both acyclic and reachable, every required
preimage must exist before the issuer freezes dependent bytes, and reviewer
testimony and ledger bytes may only be authored by the attributed issuer. This
also violates the handoff's minimum rule at lines 104-105 that every schema,
preimage, carrier, receipt, and publication edge be reachable and unambiguous.

Required outcome:

Freeze a successor whose current-bootstrap schema and immutable handoff expose
one identical output contract. The smallest coherent correction is to model the
already adopted rule-6 report plus issuer line as the reviewer outputs and put
any controller-derived wrapper outside reviewer testimony. If typed reviewer
receipts are retained instead, the new packet must, before reviewer access,
include the canonical state artifact, its exact grammar/count/digest, the
complete design-packet publication object/digest, reviewer ordinal, receipt
artifact path, exact report grammar, and the same exact line field population
and order used by the schema. One physical line must satisfy both the adopted
issuer ledger and typed parser; no coordinator rewrite or synthetic attestation
is permitted.

Verification criterion:

Starting only from the new immutable packet, independently render every
reviewer-owned preimage before report freeze. Have two cold issuers follow the
single written contract and then prove, with independent strict parsers, that
the fixed report, one physical issuer line, any assigned receipt, rule-6 review
publication, joined disposition, and implementation-opening authorization all
validate byte-for-byte without adding, rewriting, or reattributing issuer bytes.
Mutate or omit each state, packet-publication, ordinal, date, round, path,
outcome, digest, and peer-access assertion independently and require refusal at
its exact consumer.

Advisory technique, not part of the required correction: generate the handoff
output paragraph, report parser fixture, line renderer, and current-bootstrap
schema from one small canonical declaration, and keep the prospective
post-acceptance Stage 0b schema in a separately named namespace.

### CB-02 — Two accepted HTTPS main-publishing operations are excluded from the real-boundary campaign

Severity: Important
Confidence: High

Exact frozen locations:

- schema appendix
  `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-schemas.md:2697-2734`
  defines `FINALIZE_REVIEWS` and `PUBLISH_DISPOSITION` as accepted integrator
  operations with distinct authorizations/results and a `PUSH_MAIN` mutation;
- the same appendix at `:6327-6365` limits campaign steps to eight other
  operations and expressly leaves both operations normal-route-only;
- Git boundary
  `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-git-boundary.md:1061-1119`
  gives each excluded operation distinct authorization, overlay, parent/tree,
  output/ledger or disposition, lease, push, lineage, descendant, and protected-
  conflict behavior;
- its rehearsal contract at `:1250-1323` requires the same public route and
  includes review-output creation and waiting subsets, but no finalization or
  disposition-publication dispatch;
- runtime boundary
  `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-runtime-boundary.md:1938-1941`
  requires every accepted broker operation and result equation to be exercised;
- central design
  `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-design.md:958-967`
  says category inventories cover every operation-table member and public-
  boundary behavior; and
- brief `docs/briefs/v0a-i01-freeze-tools-r002-brief.md:142-166` requires the
  same pinned route to perform real HTTPS mutations at the rehearsal target.

Concrete inputs/state-to-wrong-outcome scenario:

1. An implementation correctly passes every frozen campaign case, including
   `INTEGRATE_PACKET` and two `PUBLISH_REVIEW_OUTPUT` operations.
2. Its `FINALIZE_REVIEWS` dispatch nevertheless reverses the two issuer-line
   append order when constructing the operation-specific overlay, or binds the
   wrong output package to its finalizer authorization. The common process,
   askpass, and `PUSH_MAIN` machinery still works.
3. Because no campaign step may select `FINALIZE_REVIEWS`, the campaign never
   exercises that authorization-to-overlay-to-lease path. Static table equality
   and another operation's successful push do not observe the defect.
4. The bundle is accepted under the current gate. The first production
   finalization then pushes a wrong protected review/progress result or refuses
   irrecoverably after consuming live authority. The same gap independently
   permits an operation-specific disposition authorization, record, or lineage
   defect to survive until its first production use.

Violated invariant:

Every claimed accepted authority operation and result equation must be
falsified through its real public boundary. A common lower-level Git/helper
route proves neither the higher operation's distinct authorization and build
bindings nor its exact protected overlay, lease, observation, and recovery
algebra. The adopted workflow explicitly says helper routing and structural
guards do not replace contract behavior through real public boundaries.

Required outcome:

Add rehearsal-table variants and case-qualified inputs for both operations so
they are structurally unable to select production main or production output
coordinates while still traversing their complete supervisor, broker, askpass,
Git, HTTPS, authorization, build-binding, overlay, push, observation,
reconciliation, and cleanup paths. Cover at least exact success, wrong package
or disposition binding, exact-lease rejection, clean predecessor advance and
reauthorization, exact result and clean result-descendant lost-ack recovery,
protected conflict, timeout, cancellation, broker failure, and post-case
capability/storage evidence. Alternatively, remove those operations from the
accepted/live bundle and narrow every acceptance claim until a separately
reviewed real-boundary gate exists; normal-route-only first use is not an
acceptable substitute.

Verification criterion:

Mechanically compare the accepted network-mutation operation set with campaign
step membership and require a real-HTTPS public-boundary case for every member,
with only explicitly typed nonnetwork operations eligible for an exception.
Run the two new case families against case-qualified main/output/disposition
fixtures through the same paired table and supervisor. Inject a fault in each
operation-specific authorization, build-receipt equality, copied/added path,
commit parent/tree, issuer-line order, disposition triple, lease, refspec,
fresh-observation, descendant, protected-conflict, and cleanup consumer; each
must fail at that consumer while production refs remain unreachable.

Advisory technique, not part of the required correction: derive the campaign's
required-operation coverage matrix from the accepted operation table and make
an explicit reviewed row explain every offline-only exception. Do not infer
coverage from byte-identical lower-level argv or schedule sets.

## Shape assessment and adopted-workflow justification

The four-role topology, offline/network split, raw-object construction, and
typed state algebras remain capable of satisfying the requirements, so a full
architectural replacement is not yet warranted. The shape is nevertheless
strained: 16,396 normative lines, including one 10,646-line schema appendix,
couple the current pre-utility bootstrap, future Stage 0b mechanism, utility
acceptance, and eleven authority operations. Two high-risk seams then drifted
in exactly the ways the adopted workflow warns against: a prospective typed
model no longer matches its governing issuer contract, and structural sharing
is treated as public-boundary coverage for omitted operations.

A bounded refactor is preferable to another prose-only patch: isolate the
current rule-6 bootstrap contract from prospective post-acceptance schemas, and
derive operation-to-campaign coverage from the accepted operation population.
This preserves the architecture while reducing the number of independently
edited equality surfaces. The two Important corrections remain blocking even
if that advisory refactor is declined.

## Residual limits

- This design-only cold pass could not establish native-host compilation,
  AppContainer behavior, CPython startup closure, Windows handle/job semantics,
  Git/libcurl behavior, askpass delivery, server fault provenance, or timeout
  calibration. The candidate itself defers those to implementation evidence.
- Static review cannot prove that generated schemas/readers will agree with the
  prose or that the real HTTPS fixture will enforce its advertised namespace;
  the required implementation-stage falsifiers remain necessary.
- No peer output was read or awaited, so this assessment contains no consensus
  claim and no inference about the other review.
