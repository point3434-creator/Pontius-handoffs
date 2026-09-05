# Independent FIX review: v0a-blueprint-artifact-impl/r002

Tier C. Fresh context, specification and engineering quality. Review the bounded
correction and its effects on the full adopted codec acceptance contract. Do not
read sibling reviewers, implementation transcripts, reports or controller ledger.
No source edits or broad acceptance execution. No subagents.

Candidate ref: refs/heads/review/v0a-blueprint-artifact-impl/r002.
Commit: 5e56e4454f7b8ccb360d3e36245abc33318349bb.
Base: c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98.
Tree: dc18ed133504fe6c7677b494bcefba311cc73704.
Manifest SHA-256: 6d5e14a64466f8aaa874d4bdf62ada439703eb74911a7b4dc4445c14b2af13b5.
Prior rejected commit: 6fb7f840d31d946e6b5dcb45faf82939dafd46ec.

Object repository: D:/Pontius/tmp/v0a-blueprint-artifact-impl-r001/authoring.
Use frozen Git blobs, not authoring working bytes. files/ contains the twelve
changed raw blobs relative to base, source.diff the full non-generated diff,
review.diff additionally the generated outputs. The r001-to-r002 FIX diff changes
only codec.py, two new test files and the boundary checker. Obtain it with git
diff on the two bound commits. Independently verify identity and exact scope.

## Input order (binding)

First read base CLAUDE.md, docs/workflow.md checklist v1 and FIX/cold-input rules,
ADR-0490, and all three adopted docs under
docs/architecture/v0a-blueprint-artifact-r002/. Read the two exact subsequent
controller extensions in inputs/driver-amendment-authorization.md (SHA-256
0d5cd53eb456a47a0ff346034fdfad173c77a39e37b030c99205c4913eeb2af7) and
inputs/inventory-amendment-authorization.md (SHA-256
666d89a6708c9d749265d816d063857432be42d754b6e76ad2dbafff6ba98ea3).
ADR-0490 activates the reviewed proposal despite its retained draft wording.

Then inspect requirements and frozen source and RECORD an initial invariant and
related-path inventory in your reviewer directory before reading the FIX claim.
Deferred input: coverage.md, SHA-256
ad3a47e26c2c8ff8a2d9b63422996d27e338f4041019c84235bfc4ffb1c20417.
After your inventory is recorded, open that claim and compare category/discovery,
exercised cases, limits and falsifiers. At that point the prior r001 reports at
../r001/reviews/a/review.md and ../r001/reviews/b/review.md may be read as the
binding correction requirements. Their implementation advice remains advisory.
Do not read current r002 sibling reviewer files or outputs.

Check exact graph/schema, independent fixtures and canonical bytes, numeric and
Unicode closure, real runtime/replay/independent reader, typed refusal, actual
public source boundary and no lost acceptance controls during test consolidation.
The exact driver origin/three edges and its unchanged test-suite registration
are authorized; analyzer logic, driver/runtime edits and capability grants are
not. Original budgets remain: source300, combined new tests300, two fixtures8192
bytes, existing manual registration added+removed100. Initial-plus-one-correction
cap binds; no further edits are authorized by a review finding.

## Permitted evidence and targeted checks

Raw receipts in task-root/run-records/ are permitted. Relevant corrected families:
correction-final-codec-*, correction-boundary-green-*, correction-inventory-focused-*,
correction-registration-check-* and correction-registration-write-final-*.
The two correction-*-red-r001-311 receipts prove behavioral RED on old frozen
production with expanded tests. Prior reports and coverage explain older failed
attempts; no filename implies success. The substring r001 in run names is an
invocation label; candidate r002 is identified by frozen commit and manifest.
Parent has an independent verify-frozen.py metadata audit; recompute identities
yourself rather than relying solely on its reported success.

Inspect run-snapshot.ps1 before use. For tests/probes always pass
-Overlay D:/Pontius/tmp/v0a-blueprint-artifact-impl-r001/packets/r002/files,
unique RunName, exact Slot311/314 and PythonArgs. It uses fresh snapshots,
scrubbed child environment, absolute PONTIUS_GIT, -B -P and snapshot src imports.
MinimumDigits adds -X int_max_str_digits=640. Run floor first; exact 3.14 may need
native escalation, never substitute an interpreter. Probe actual material risks
and public boundaries; don't duplicate the entire unchanged test population for
ceremony. Do not run payloads in the primary or authoring checkout.

All recorded ordinary correctness tests are permitted, not operating/rehearsal/
scientific runs. No dependency installation, network, primary mutations, fixes,
index/ref writes, commits, pushes, publication, source seal or cleanup. Create
only reviewer-owned reports/probes in the assigned r002 reviewer directory.
The broad population runs only after BOTH reviewers are CLEAN.

## Deliverable

Issue review.md and attributed verdict-line.md bound to commit and manifest.
State Spec PASS/FAIL, Quality PASS/FAIL, C/I/M, CLEAN or REQUIRED CORRECTIONS,
and SOUND/STRAINED/WRONG SHAPE with reason. Map prior required findings to actual
verification; challenge related paths and missing controls independently. Every
Critical/Important finding needs concrete input/state -> wrong outcome or a
directly demonstrated missing binding acceptance contract. Include strengths,
requirement/evidence mapping, exact fresh checks and limitations. Do not turn
optional suggestions into blockers or imply a finite probe is an exhaustive proof.

This local frozen candidate is not published or adopted. Finish the bounded
independent technical review; no source correction or operating authority follows.
