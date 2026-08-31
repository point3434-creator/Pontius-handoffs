# V20 name-storage fitness disposition

Coordinator engineering disposition, 2026-08-31. This is not a cold review,
frozen successor, acceptance result or permission to integrate source.

The universal AVL name-store adapter is rejected for production fitness.
The earlier pure-storage compatibility result remains valid but does not
admit this adapter to the full analyzer. W is retained at v20 SHA256
e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679;
the port lease is closed. No further v20 acceptance campaign is planned.

The unchanged floor DesignReview population completed 53 tests with two
failures and one error. Bounded chain32 now exhausts the 262144 work budget,
and two deep-helper checks reach that work refusal before their expected
depth refusal. Receipt: engineer-checks/release20-design-311-receipt.json,
SHA256 fbecc06b5f59318468d225cfae4f43fa2b6f8ebf92554e841b6b6da50c75a2e6.
This is a product regression, not an infrastructure or interpreter failure.

The single floor chain32 diagnosis delegates the original budget unchanged.
At refusal, 160983 units were in joins, 60301 in ordered reads, 27392 in
lookups, 4993 in construction, 3705 in assignments/overlays, 3264 in forks
and 1507 elsewhere. Name storage accounts for 250815 of 262145 units.
The pass is helper-disabled receiver preflight; the optimized name-version
join is never entered. Full joins repeatedly clear and reconstruct AVL
trees, despite there being no authority work to avoid. Receipt:
engineer-checks/chain32-v20-diagnosis01-311-receipt.json,
SHA256 03c82035d15ed8218e8a0ac9907eb189738402215e4bd4e93a72de6d81c14a47.

Before another production edit, the coordinator reviewed and dispatched the
already-prepared public24 measurement on the floor only. All 24 fixed public
expectations and 58 harmless runtime witnesses pass. The localized
improvement is real: 5415 state copies share names; 115 enabled common-base
joins perform zero ambient-name normalizations. Nevertheless total consumed
budget rises from 168331 to 1357663, or 8.0654 times. This is a budget ratio,
not a runtime or physical-work ratio: v19 and v20 charge different storage
operations at different granularity. No charge may be hidden to recover the
old number. The [independent assessment](tests-checks/name-environment-v20-floor-report-v1.md)
retains every case, phase and limitation, including unexercised fallbacks
and the lack of a whole enabled-only budget partition.

The coordinator's [verification](coordinator-v20-diagnostics-verification-v3.json)
independently rehashes the retained snapshots, reconciles diagnostic units,
checks all 24/58 expected results and unchanged public/oracle function ASTs.
SHA256 bb85cea1a3215499be58469d983c57a241626c198abd8a469deef1af70cd883c.
No v20 developer-slot, matrix, ordinary generation or broad suite was run.

Failure category: snapshot storage with per-edit immutable reconstruction
was imposed on dense construction, full-rebuild fallbacks and demanded
ordered reads. A passing sparse-join prototype did not establish fit for
these production lifetimes. The engineering design assessment is WRONG SHAPE
for the universal adapter under the existing cap. This is the coordinator's
adopted design conclusion, not a new attributed cold verdict.

Disposition: reassess only the name-store boundary. Preserve immutable
published snapshots, exact exposed ordering, raw versus semantic writes,
parent inheritance, narrow transfer certificates, every cell write, and
authority/binding adoption. Compare owned branch deltas published at actual
fork/adoption with compact immutable history and exact ordered materialization.
Dense construction must not pay a persistent-tree path for every transient
entry. Merely replacing AVL nodes with a new immutable dictionary layer
per assignment can retain the same lifetime problem; publication frequency
and compaction must be part of the design and its measurements.

A disabled-only exemption, a bulk AVL loader, and a fixed partitioned store
are alternatives to assess, not presumed fixes. The replacement must show
its full construction, publication, lookup, join, ordering and failure costs.
Existing finite case expectations remain fixed; new ownership/fault coverage
must be independently specified. No production edit is authorized by this
design exploration alone. A reviewed bounded prototype disposition precedes
its implementation; its result cannot substitute for the real focused and
ordinary-generation gates.

All five analysis caps, transfer/object/cell semantics, accepted A/B, other C
paths and generated files remain fixed. No additional authority-map rewrite,
support-contract change, guarded profile, research owner, GPU work, source
seal or live action-wall claim is included.

Control history: the coordinator's first static verifier stopped on a copied
receipt digest typo; its second stopped on the legacy receipt's nested
identity schema. Neither ran a test payload or created an output artifact.
The third verifier corrected those control defects and completed; earlier
control files remain retained. These are control failures, not product runs.
