# r005 disposition and integration preparation

Issuer: /root. Date: 2026-08-30.
State: review-clean and locally verified; awaiting specific ceremonial authorization.

## Frozen identity

- Ref: refs/heads/review/v0a-i01-prereg/r005
- Commit: 98328440d4425fed1dbc7eb30b26b5f785709f05
- Base: ca0b2e41bbf5d9fc1649de20379299331de6591a
- Tree: f13e21e07721bb97ff4e6308229c724dd8ce16a0
- Canonical manifest: d972987187b78a2ac5fdb6dbaa74cd7b23e1ce7fdd3a73fae5ed96a0f532da17

R005 corrects only r004's packet identity. The source commit is identical.
Both independent reviewers recomputed the canonical full-row-sorted manifest and
returned CLEAN; their attributed reports and task-ledger entries are retained.

## Decisions on returned findings

- Claude's r2 CLEAN review was bound correctly and remains preserved. Its N1 note
  prompted a ready-to-emit checkpoint that separates decision work from reserve use.
- N2's private_cards/private_hand mapping is explicit. N3's run-identity validation
  remains implementation/source-seal guidance under the already declared namespaces
  and measured limits; it changes no semantic identity or authority.
- N4 could not be adopted as written: raw timing after finalization is not a
  public-ledger total. The corrected contract keeps the outer ledger open, partitions
  public preparation intervals, and measures terminal publication in a separate
  returned host receipt. A terminal row does not claim its own future write duration.
- R3's relative-link defect was accepted and corrected at the ADR source; STATUS
  was regenerated. No sealed generator or test changed.
- R004's manifest-ordering defect was accepted. Its source bytes and individual
  hashes were correct; the metadata is corrected append-only here. An independent
  row-order predicate now rejects r004 and accepts r005. The original passing
  validator had repeated the builder's wrong sorting assumption and is not treated
  as a valid packet-admission result.

The controller's CodeRabbit retirement and coherent bootstrap sequence are recorded
in the new prospective amendment. Those decisions no longer require approval.
No historical result or issued review was relabeled.

## Verification and integration preview

The source-commit receipts remain in r004/checks: each actual CPython 3.11.15 and
3.14.6 snapshot passed the complete 12-test status-generation suite plus four
clone-safe documentation checks. STATUS freshness also passed.

After r005 review, fresh integration snapshots overlaid exactly the three reviewed
blobs onto master commit 448296a (Adopt the handoff-packet convention). The merged
tree is e8bc0965bcd86e38d060925856b5242e180e36e3, matching git merge-tree's clean
preview. Both interpreters again passed all 16 scoped checks and STATUS freshness.
The snapshot index/working bytes remained exactly the declared overlay. Receipts:

- checks/r005-integration-py311-verification.json
- checks/r005-integration-py314-verification.json
- checks/manifest-red-green.json

The new master workflow bytes match the packet's pinned workflow input. Integration
preserves that already committed update. The reviewed change remains only ADR-0485,
the new workflow amendment, and generated STATUS.md. No runtime, tests, capability,
lifecycle identity, retained result, or legacy dependency baseline changes.

These are scoped documentation checks, not broad scientific-suite or runtime
acceptance. No experiment owner, rehearsal, source seal, measured operational
closure, or authoritative replay population has been executed or established.

## Specific decision awaiting authorization

Proposed ceremonial title: **Preregister the blueprint-only v0a hand contract**.
Integrate the reviewed candidate with current master while retaining exactly the
three reviewed document blobs and the tested combined tree, then push to origin.
A merge-shaped decision can retain the frozen candidate as an ancestor; the original
review refs remain until the workflow's reachability/archive predicate is satisfied.
If master or any proposed file changes, repeat the integration verification before
committing. No integration, ceremonial commit, evidence-repository push, or ref
retirement has happened yet. Routine packet-repository commits are separately
authorized by the adopted workflow and do not open the experiment lane themselves.

## Addendum: returned Claude r005 review

Issuer: /root, coordinator assessment. Date: 2026-08-30.
Binding: candidate 98328440d4425fed1dbc7eb30b26b5f785709f05 /
manifest d972987187b78a2ac5fdb6dbaa74cd7b23e1ce7fdd3a73fae5ed96a0f532da17.

Claude returned CLEAN in reviews/review-02-claude.md, SHA-256
f04f444005c9af6c0eca2579e379edf54e938f9b7d66efad8eaf36465e493113,
and appended its own attributed task-ledger line. Its binding was independently
verified against the frozen blobs and canonical manifest. This is the third CLEAN
review for r005; no Critical or Important finding was introduced.

M1 is accepted as a minor historical/current wording ambiguity. The amendment's
ADR-0478 hash 2ea6b7c849ec4d991ae68fcc9b069b6892b51c5831f5d21a424a709fec05b7bf
identifies the historically accepted workflow bytes, preserved in Git and unchanged
by this amendment. It is not the current-master workflow hash. The separately
adopted handoff-packet changes at 448296aa8410966c253ead6620f42565226eeec8
produce workflow hash c70581f35cc1b424a1734c9dbbdb17bea530622461225cd54ca23297c1db4e4a,
identical to this packet's pinned workflow input. Integration preserves that live
workflow and applies only the three declared changed blobs. This clarification
changes neither the candidate contract nor review scope; candidate bytes and issued
reviews remain untouched. Explicitly historical source wording can wait unless
another candidate round opens for a substantive reason.

The run_id validation note remains assigned to implementation/source seal. The
controller-ruling provenance note requires no change: the packet records the direct
controller instructions and grants no additional authority.

A fresh canonical-manifest verification and integration preview still reproduce
manifest d972987187b78a2ac5fdb6dbaa74cd7b23e1ce7fdd3a73fae5ed96a0f532da17
and combined tree e8bc0965bcd86e38d060925856b5242e180e36e3. The existing isolated
3.11.15 and 3.14.6 receipts bind to those exact candidate blobs and that tree.
Specific ceremonial authorization remains outstanding; no evidence-repository
integration or experiment has occurred. The review and this addendum are routine
coordination publication only.
