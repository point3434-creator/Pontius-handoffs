Issuer: /root/cold_review_r3_b

**r004: NOT CLEAN — one Important packet-identity finding. Confidence: high.**

**[P2] Manifest rows use the wrong sort order.**  
Locations: `D:/Pontius-handoffs/v0a-i01-prereg/r004/manifest.sha256:1–3` and `candidate.json:9`.

The pinned workflow requires lexicographically sorted **complete rows**, explicitly implemented by `sorted(rows)` (`inputs/workflow.md:97–100,135,234–237`). The packet instead orders rows by pathname.

All three individual blob hashes are correct. Sorting the complete rows produces:

```text
625b644223a4f29fae9e7a2b48360dfa177e6e18045fb1d951e5e05e9d48bdc3  docs/decisions/ADR-0485-preregister-the-blueprint-only-v0a-hand-contract.md
c0fcc666ae44113e05e2aee410cdaf0ad1136bfc2101a07be7f96dc2b34ac63c  docs/workflow-amendment-2026-08-30.md
dcdb2bba691f0c5032f59e883cc8eed70bb6a0b852ecb99eb1f6ba3af7f84ada  STATUS.md
```

Their canonical manifest SHA-256 is:

`d972987187b78a2ac5fdb6dbaa74cd7b23e1ce7fdd3a73fae5ed96a0f532da17`

The supplied `402514df6aead93fc1495096d6f9647b0021992751b63566f90a695b89d2d8f0` hashes the path-sorted packet instead.

Concrete failure: an independent reviewer following the pinned manifest algorithm computes `d972…`, cannot verify the advertised commit/manifest pair, and must refuse identity admission despite inspecting the same candidate blobs.

Minimal direction: preserve r004 unchanged and publish corrected immutable identity metadata and manifest rows under the packet’s append-only rules. No candidate source correction is required.

The ref, commit `98328440d4425fed1dbc7eb30b26b5f785709f05`, base, tree, three-path scope, pinned input hashes, and preserved workflow/brief/baseline identities otherwise match.

The r3 broken-link finding is closed at candidate `STATUS.md:27` and ADR-0485:36. The complete candidate’s substantive contracts are unchanged apart from that correction; no additional material source-specification issue survived review of privacy, blueprint outcomes, events/replay, accounting/publication failures, authority, or sealed-API feasibility.

No tests, runtime, owner, or generator ran. No r004 files or ledger were written.

Separately, r3 persistence is complete: its attributed report is retained, and exactly one r3 NOT CLEAN ledger line was appended after A’s entry.
