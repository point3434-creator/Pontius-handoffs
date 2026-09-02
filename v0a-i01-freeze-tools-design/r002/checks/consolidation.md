# Freeze-tools design r002 review consolidation

Status: **COORDINATOR INPUT / NON-VERDICT**. This consolidates the two fixed,
peer-blind formal reviews. It is not a third review and does not change either
issuer's verdict or report bytes.

## Verified identities

- Candidate commit:
  `48e590327c0a4bfd7ea5019e6770e1d582182b08`
- Candidate parent:
  `d1ed3cbda6107d61ea8e77133871720af04970cd`
- Candidate tree:
  `27e0503a7f6f4efd44122078aeab62f3151420d5`
- Candidate manifest SHA-256:
  `010e96031f60afd8badc07ebb4dd97ab8db4102527be0eb42ee56c2d65e7c984`
- Immutable initial handoff commit:
  `14c1f5629024973b96f71c64a04f17ce9d7e01e2`
- Immutable initial handoff tree:
  `3aa5f285d8b1f55eedcdf6339845ee6a6fcc583a`
- Review-output publication commit:
  `de0b9de1beb053e2ec2e51561fbac0126747ace6`
- Review-output publication tree:
  `a4d12422370d8c95513b16e25b48d3fb32535fa7`
- Adopted workflow SHA-256:
  `ab5202b170a5fd9c2cf1540aa198d4a82c742cb336134b0f9a8db944fd64f91a`
- Deferred coverage SHA-256:
  `72fff2541772140f558bc40ef3e137a165c240f29feabd9faac139467a030e46`
- Formal review A SHA-256:
  `f8a65509d64be686b1f06ffbb59af1b8f364508e683fb0036910540ae27fe675`
- Formal review B SHA-256:
  `6a5a3f466044b060204cbcfcce95a5c5ba9b65b3a90b92e38916f192988d1f76`

The candidate is an add-only six-path documentation diff containing 941,640
bytes and 16,396 lines. Both formal reports bind the candidate and manifest
above, contain the required independent pre-coverage inventories, and return
defect verdict `NOT CLEAN`. Neither reviewer opened the peer report.

## Required verdicts

- `codex-a`: defect `NOT CLEAN`; design `WRONG SHAPE`; two Important findings.
- `codex-b`: defect `NOT CLEAN`; design `STRAINED`; two Important findings.

There are no Critical findings. The design-verdict disagreement is preserved.
The coordinator applies the stricter scope and replacement boundary required by
the formal `WRONG SHAPE` finding while retaining the four-role decomposition
that both reviews found materially stronger than r001.

## Consolidated finding clusters

### C1 — Current bootstrap review outputs are unproducible

`codex-a` finding 1 and `codex-b` CB-01 are the same material defect and count
once. The adopted handoff permits one five-label report and one issuer ledger
line. The candidate instead requires a differently rendered report and line,
an issuer-authored typed receipt, reviewer ordinal, canonical series state, and
design-packet publication identity that the immutable packet neither supplies
nor assigns. Exact packet-following outputs therefore fail the proposed parser;
coordinator synthesis or rewriting would violate issuer attribution and fixed
bytes.

This is the first residual of r001 correction class 6, canonical review
provenance. It is blocking and has high confidence in both reports.

### C2 — The FIX candidate adds unsliced new authority surface

`codex-a` finding 2 is unique. The adopted workflow confines a FIX round to its
finding-required surface, sends new surface to its own candidate, and requires
named slices from the first review for candidates above roughly 3,000 changed
lines. R002 instead presents 16,396 lines as one review target and adds a
prospective Stage 0b convergence, activation, publication, disposition, and
build-authority system not required to close the eleven r001 classes.

This is a workflow and reviewability defect, not another count of an r001
contract residual. It is blocking and has high confidence.

### C3 — Two accepted HTTPS mutation operations have no real campaign case

`codex-b` CB-02 is unique. `FINALIZE_REVIEWS` and `PUBLISH_DISPOSITION` are
accepted integrator operations with operation-specific authorization, overlay,
lease, lineage, protected-content, lost-ack, and result behavior. The frozen
real-HTTPS campaign expressly excludes both. Exercising shared `PUSH_MAIN`
machinery under other operations cannot falsify defects in these higher-level
bindings.

This is the first residual of r001 correction class 7, exact real-HTTPS
mutation rehearsal. It is blocking and has high confidence.

The `codex-b` shape assessment overlaps the structural cause behind C1 and C2,
but it is not an additional formal finding. The two reports therefore establish
three distinct Important correction classes, not four.

## Root-cause and recurrence assessment

R002 combined three protocols in one normative surface: the reusable four-role
authority utility, the current pre-utility rule-6 bootstrap adapter, and a
future post-acceptance Stage 0b automation protocol. The current bootstrap was
then described using prospective typed artifacts that its actual immutable
packet could not produce. This duplication caused C1 and made C2 unavoidable.

Separately, the campaign enumerated selected operations rather than deriving a
total accepted-operation-to-public-case relation. Shared lower-level tables
masked the two missing higher-level members and caused C3.

C1 and C3 are first residuals of their respective r001 contracts. The adopted
second-residual stop rule is not yet triggered. Repeating either contract defect
in its next FIX would be a second residual and would stop further in-place
patching of that contract. The two successive adverse design verdicts make a
narrower replacement boundary the default for the successor even though the
four-role core remains salvageable.

## Binding successor correction matrix

| Gate | Required correction | Verification criterion |
| --- | --- | --- |
| C1 bootstrap writer/reader agreement | Use one exact current-bootstrap output contract. Prefer the already adopted rule-6 report plus issuer line, with any controller-derived wrapper outside reviewer testimony. If reviewer receipts remain, the immutable packet must supply every canonical preimage, ordinal, path, grammar, and digest before review. | Starting only from the new immutable packet, two cold issuers render every assigned output. Strict independent parsers accept the report, the same one physical issuer line, any receipt, publication, joined disposition, and implementation authorization without coordinator-added or rewritten issuer bytes. Mutating each field or preimage refuses at its exact consumer. |
| C2 scope and slicing | Remove the prospective Stage 0b automation system from the r001 FIX. Publish it later as a separate NEW-SURFACE candidate rooted in an accepted utility. Map every retained FIX member to an r001 formal/advisory requirement. If the successor remains above roughly 3,000 lines, freeze named, nonoverlapping review slices in its initial handoff. | The immutable path/section map accounts for every FIX member and contains no future activation/counter/publication/build-authority interface. Independent line count and slice coverage reproduce. Every Tier-C reviewer covers every named slice from the outset. |
| C3 complete real-HTTPS operation coverage | Add case-qualified real-HTTPS campaign families for `FINALIZE_REVIEWS` and `PUBLISH_DISPOSITION`, or remove those operations from the accepted bundle and narrow all claims. Cases must traverse their complete authorization, build, overlay, broker, Git, lease, observation, reconciliation, and cleanup paths without production coordinates. | Mechanically compare the accepted network-mutation operation set with campaign membership and require one real public-boundary family for every member. Independently fault each operation-specific authorization, package/disposition binding, copied path, parent/tree, line order, lease, refspec, observation, descendant, protected conflict, and cleanup consumer. |

## Successor shape

Any successor uses a new immutable candidate and manifest; r002 bytes, reports,
ledger lines, and packet inputs remain unchanged. A permissible r003 is a
narrow FIX for the r001 utility corrections plus the minimal current rule-6
bootstrap adapter. It must declare named slices if still above the adopted
threshold and carry a revised coverage claim that includes C1 through C3.

The prospective Stage 0b automation protocol becomes a separate NEW-SURFACE
task after the utility has an accepted external root. It cannot be approved by,
retroactively authorize, or share a FIX disposition with this bootstrap series.

No implementation, runtime execution, test run, retained-evidence operation,
production source change, ceremonial integration, or implementation-start
publication is authorized by this consolidation.
