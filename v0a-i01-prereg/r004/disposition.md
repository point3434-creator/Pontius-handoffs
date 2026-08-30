# r004 disposition

Issuer: /root. Date: 2026-08-30. Disposition: rejected packet identity.
Advertised candidate: 98328440d4425fed1dbc7eb30b26b5f785709f05.
Advertised manifest: 402514df6aead93fc1495096d6f9647b0021992751b63566f90a695b89d2d8f0.

Both independent reviewers found the same Important defect: rows are path-sorted,
but the adopted workflow requires full-row lexicographic sorting. Accept that
finding. Individual file hashes and the source commit are correct. The corrected
canonical digest for that commit is
d972987187b78a2ac5fdb6dbaa74cd7b23e1ce7fdd3a73fae5ed96a0f532da17.

The original publication verifier repeated the builder's ordering assumption;
its passing result did not establish conformance to the required sort order.
Keep that receipt as historical output, not a valid packet-admission verdict.
R004 remains unchanged and unintegrated. R005 republishes the same source commit
with corrected identity metadata and full-row ordering. No source edit is needed.

The two genuine interpreter snapshot runs remain evidence for their named source
commit: 16 scoped documentation tests pass on each of CPython 3.11.15 and 3.14.6.
They did not test handoff-manifest conformance or runtime implementation.
