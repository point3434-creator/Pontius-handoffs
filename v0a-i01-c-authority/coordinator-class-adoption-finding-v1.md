# Class-body authority adoption: engineering finding

2026-08-31. Additional coverage found a behavioral defect in retained v19,
SHA256 3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1.
This is an engineering finding, not an attributed cold verdict or new round.
No production edit or acceptance permission is implied.

The predeclared four-case composition pack
faa0026181653881737e15af0effe6e670fbad3ad20e684c1d019851dd0dd709
was executed through the public derive_design_review boundary on actual
Python 3.11.15 in a fresh r010 snapshot with only exact v19 overlaid.
All four independent harmless oracle traces passed. Both shared-list cases
passed; both class-adoption cases failed their fixed semantic expectations.
There was no analyzer exception, cap refusal or infrastructure error.

Unsafe case: owner starts None. A class body calls a direct local helper
that nonlocally sets owner to ReviewTests. A later reader reaches
owner._launch = None. The harmless oracle records change, read, write and
TypeError; the sink is never reached. The analyzer instead returns an
unblocked stale [-m, outer] subprocess capability. An explicit blocker
is required by the existing source-point/captured-cell contract.

Safe counterpart: owner starts ReviewTests, and the class-body helper sets
it to None. The later reader does not mutate the sink; the oracle records
change, read, sink and returns outer. The analyzer returns no row and four
helper namespace blockers. The ordinary class-local module = inner must
not replace the enclosing module = outer; preserving namespace isolation
does not justify dropping a captured-cell effect.

Category under investigation: authority adoption across a namespace boundary
must expose current captured-cell values to subsequent represented reads,
while preserving caller names/bindings and expression observations. The two
explicit authority-only adoption sites are helper completion and class-body
completion. The construction/adoption inventory also covers parent
inheritance, state replacement/overlay, joins and raw cell hydration.

Static lead, not yet a measured mechanism: in v20's corresponding source,
helper completion at 19020 refreshes existing bound projections at 19025;
class completion at 23596 adopts only authority. Later local-helper review
at 25895 derives its entry projection from source_flow.values_by_call.
The hypothesis is updated cells paired with a stale outer name projection.
Instrument original delegation and inspect both projections/cells before
choosing a correction; do not patch only the last failed assertion.

The source-contract requirements already demand later free-variable lookup,
source-ordered class construction and refusal of stale literal capabilities.
These cases require neither a metaclass nor reflection nor new execution
support. No case expectation or classification has been weakened.

Receipt: tests-checks/storage-composition-storage-composition-v19-01-311-receipt.json
SHA256 210890c5e24e2eb227a99fba0c5a859c131c53d77fa4cf41e6069d56275e001f.
Raw log: tests-checks/storage-composition-storage-composition-v19-01-311.txt
SHA256 87ce72db48e176abcf6e944ceda6423edd89e50ce2cca1e5496dcf7837832e0f.
The coordinator independently rehashed all retained receipt paths and
checked the four oracle/analyzer records before issuing this note.

This semantic finding is separate from v20's storage-budget regression.
The cursor prototype must not encode a workaround for it. A bounded
semantic repair needs the category inventory, original RED and integrated
GREEN, with the shared-list controls and existing authority/focused suites
preserved. Developer-slot replication, final-source checks and cold review
remain outstanding. Accepted A/B, other C paths and main source are unchanged.
