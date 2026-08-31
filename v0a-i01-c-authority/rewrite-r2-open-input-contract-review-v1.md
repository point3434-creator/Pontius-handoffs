# Gate B open-input contract engineering review v1

Author: codex/cold_review_a, engineering participant and author of the original
name-environment case/Model pack. This is a static contract finding, not an
independent cold review or a runtime failure report.

Finding: the four frozen Gate B scale cases require clean results without
supplying an analyzer-visible inert-scalar premise for self.choice. Their
independent Models establish the stated integer projections, not a universal
proof over open receiver values. Preserve strict refusal of unproved protocol
effects; do not introduce a fixture-keyed rule or silently interpret every
absent receiver fact as an inert scalar to satisfy these labels.

All four original clean labels, sources, Models, expected traces and old
results remain unchanged. This note changes no acceptance input. Root owns a
prospective corrected cost-premise disposition under a new round after Gate A.
R1 continues; this finding does not stop its current work.

## Exact inputs

Paths are relative to D:/Pontius-handoffs/v0a-i01-c-authority unless stated.

| Input | SHA-256 |
| --- | --- |
| rewrite-design-v1.md | 701552c177840e4c5c0dd9c5985776256af5b31e7e997067dd662638a67c3ca8 |
| rewrite-stage0-v1.md | 8c84baa92400716efee2d4dd23eeafefa88a794125bafd4cc97432572ca7e077 |
| stage0-design.md | 78bebca5279bf81e30181787f962d40c73826259d0bb3ffb1c7804804c1211e8 |
| ../v0a-i01-ab/r010/acceptance.md | 889f0bb7508e22ac668b99165cdccf4b75ee0ada67ce50c1e12e20a1f2153da4 |
| rewrite-r1-implementation-plan-v1.md | 18f8124432880016d6dd0690ed4d3b582b8e202c5bdda21ae48a65efa0ae521d |
| rewrite-r1-plan-disposition-v1.md | 64fbb4b0690d5555c6eebd7b96d0e8129115df01d44c4441e95cb8d98dd177a8 |
| rewrite-r1-task4-coordinator-disposition-v1.md | c12b0455954e90e3ee4f9ecaba888079002c6374aa85615439a9e959228bea37 |
| rewrite-early-population-v1.json | 3dd0ec8b6130b38d5138724b43e233e4e1a3e595f089c182291b00912d8423ce |
| tests-checks/name-environment-cases-v1.json | d07ccfd6d72daee378d1a67468290e7e30fd8f2a0e608bad9cc16fc4b51b2e9c |
| tests-checks/name-environment-plan-v1.md | 969b3acb781cca11ccd10b26eddaab300a5af7a24b4199ae235136a68f4f62ef |
| tests-checks/name-environment-probe-v1.py | 94a91ff970aa0df12c4334d72a2476ca5d58a4b76aa3a412c5440e93411806b4 |
| rewrite-r1-base-generator.py | 29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692 |

The original tests/test_inventory_and_profiles.py was read from
D:/Pontius-worktrees/codex-v0a-i01-c-core-v1/tests/test_inventory_and_profiles.py
and verified unchanged at SHA-256
c46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf.
This is the r010 blob a62562fbba5969e33cc04786d91064afad30e580 from candidate
29c02f6fbd5eb0b7ddc9e816ef28f570b9839358. The old generator above is the retained
r010 source; no in-progress replacement source was inspected for this question.

Context-only documents searched/read under D:/Pontius (raw hashes, not new
claims about their Git publication):
- docs/decisions/ADR-0480-absorb-the-test-orchestration-stabilization.md:
  c1a10126ebffbb3d105006d2dd5e0adc75260b15dd6e40d65c9bd22423a74f99.
- docs/superpowers/plans/2026-08-27-test-profile-orchestration.md:
  ea92587f014d08eff4c6533e1e223045680ca5ec32115733a89edc976bc650fa.
- docs/superpowers/specs/2026-08-27-evidence-test-stabilization-design.md:
  93ae8c01ee2e63bf829fd2fdcaadd7dd6f0aab25d8eba140c385a92b426677fc.

## Four-case source/Model inventory

Line numbers below are in each decoded sensitive source string; JSON pointers
refer to the unchanged name-environment case pack. Source and Model hashes are
UTF-8 of the exact decoded strings, with no normalization.

| ID / pointer | self.choice comparison lines | Source SHA-256 | Model SHA-256 |
| --- | --- | --- | --- |
| scale-n8-s4-d0-normal /cases/4 | 17,19,21 | 7a496280160092f1389045b0d640f9871f4080b1807db988d04725730fa8b1c7 | c3085cc320db1712eb6a2ef5c4777b18d28278004235579ffd85cb29100c47fa |
| scale-n64-s4-d0-normal /cases/12 | 73,75,77 | 8cd92fb80500595801e3948c1cb9a7ac825334457139b70933307714ad09fe10 | 00a3a4792a10e0279efc591401f7856bd157b580b234f6d2972246912c780ed4 |
| scale-n8-s4-d2-exceptional /cases/7 | 18,22,26 | 0e22e6aa9144d52d49c0c9a1a398b4fec9d7213b03e64b3af39278b92e3a2303 | 335cf692d739f50143151b2429fd34d8f22328661701f95c91acc1767feac3b0 |
| scale-n64-s4-d2-exceptional /cases/15 | 74,78,82 | a67c06db53e8804496c85cf9437e5fbfa9c68a235e27e0af69b454713167b33d | 12818b59ac4dc3d9ed3768c28afef434e34b6ebf387a5c3b4bf469d44cc9740f |

Each source has three loaded choice attributes, equality comparisons against
0,1,2, and no choice store or class-level choice fact. Each retains classification
clean, requiring no blockers and exactly argv [-m,fixed]. Each has four Model
projections with exact integer choices 0,1,2,3. The normal branches leave ambient
and work values unchanged; exceptional branches update work0/work1 and raise a
matching handled exception. Those expectations are not changed by this review.

The original plan lines9-13 and26 made all sixteen scale cases required-clean
from the finite arithmetic/event schedules. The four selected records are bound
in early-population lines415-570; Gate B selects them at lines952-955 and976-979.
The public envelope at original probe lines104-122 passes source, inventory and
item universe only. It passes no choice value/type or closed harmless-input
domain. Separately, project_oracles at lines125-138 creates a fresh Model and
sets instance.choice from each integer witness. That assignment is absent from
the sensitive source and public analyzer input.

## Contract and original-test evidence

- R1 plan lines41-43 says the absent receiver choice fact is unknown, not proved
  AttributeError. Its record table at line75 keeps unittest instances open;
  lines192 and211 admit ordinary unknown receiver observations and boolean
  alternatives. None says the unknown is an exact scalar, proves inert equality,
  or proves inert truth testing of an equality result. The later coordinator
  Task4 note lines40-42 explicitly requires proved inert truth or refusal.
  Open lookup cannot simultaneously serve as positive protocol-safety proof.

- Detailed rewrite design lines188-190 says harmless runtime behavior alone
  does not make unsupported shapes required-clean. Lines210-214 retain the
  original acceptance and existing populations. Original Stage0 line60 says
  unknown is not an empty proof. r010 acceptance lines40-47 requires explicit
  handling of unresolved callable/member provenance and relevant sensitive
  paths; its no-general-heap/reflection allowance permits refusal, not a guessed
  inert-input fact. The component-separation non-sandbox clause is not an
  explicit scalar-input promise for these analyzer comparisons.

- Original tests lines12356-12544 require ordinary safe receiver behavior,
  but the safe receiver there is the concrete builtin list [1] and list.copy.
  It is not an absent unittest attribute. The clean protocol inverses at
  lines18254-18302 define explicit harmless protocol methods. Sensitive
  comparison/truth cases include lines17552-17562 and17583-17593 and are
  adjudicated through lines18186-18188. Their obligations do not permit dropping
  effects from an unproved object merely because a branch is unknown.

- Existing self.condition at original tests lines13312-13336 is a
  deferred-provenance refusal control, not a required-clean scalar premise.
  self.flag branch examples at lines15119-15152 explicitly install class
  flag=True and require sensitive coverage. Searches of the pinned original
  module did not find the exact self.choice comparison family or a general
  promise that all open receiver values are inert scalars.

- ADR-0480 lines41-45 describes an exact AST/source-order analyzer with typed
  fail-closed blockers. The orchestration plan lines470-474 requires static
  derivation with unresolved-dynamic blockers. These contexts do not supply
  an input-type premise. This was a bounded search of controlling documents
  and relevant original tests, not a fresh audit of every historical contract.

## Why legacy clean behavior is not the missing proof

In r010 source, _unittest_receiver_attributes at25461-25488 seeds only a
unittest_receiver marker. Entry preflight at25643-25673 rejects discovered
sensitive fixture/class facts; absence of such a fact does not prove int.
Attribute handling at18026-18039 records receiver access, while comparison
handling at20079-20130 visits protocol hooks then returns an unknown result.
_record_implicit_protocol_blocker at14982-15012 records discovered sensitive
descriptors or its designated unresolved-sensitive class case, and otherwise
returns. This explains a legacy path that can accept an ordinary unknown
comparison without establishing an inert scalar domain. It is evidence of
historical implementation behavior, not a new permission to reproduce the
inference in the canonical engine.

Python allows comparison methods to return non-bool values, followed by truth
testing in a boolean context; truth testing may call __bool__ or __len__.
Those operations can contain effects. This ordinary language behavior does
not require malicious reflection or an introspection sandbox.
Sources: https://docs.python.org/3.11/reference/expressions.html#comparisons
and https://docs.python.org/3.11/reference/datamodel.html#object.__bool__.
No new witness, protocol body or runtime result is asserted here.

## Recommended disposition and limits

Preserve strict unproved-protocol refusal. Do not key behavior to these four
IDs, self.choice spelling, Model output, an empty metadata map, or the old
absence of a blocker. Preserve the old pack, labels and evidence unchanged and
record the missing premise explicitly before any prospective cost-gate
correction. Root will determine the corrected premise in a new round after
Gate A; this note defines no new API/domain and authors no corrected fixture.

An early explicit blocker would be honest unsupported behavior, but would not
prove that the intended successor joins and ambient-name scaling executed.
The cost experiment must retain that mechanism distinction. Conversely, four
passing integer Models cannot justify a universal clean capability claim.
I authored the original structural family and acknowledge that its required-
clean classification did not separately establish this input premise.

Verification here was hashes, JSON selection, source reading and AST-only
inspection under actual3.11.15 -I -S -B -P. No candidate, test, sensitive source,
Model or owner was executed; no case, source, expectation, ledger or production
file was edited. This is a planning conflict to resolve, not a reported R1
runtime regression or authorization to stop R1.
