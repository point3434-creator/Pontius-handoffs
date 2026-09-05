# Independent implementation review request: v0a-blueprint-artifact-impl/r001

Round kind: NEW-SURFACE. Tier C. Review the whole candidate for specification and engineering quality; this single-unit task is also the whole-branch review scope. Do not read other reviewers, implementation chats or the controller execution ledger.

Candidate: refs/heads/review/v0a-blueprint-artifact-impl/r001 at 6fb7f840d31d946e6b5dcb45faf82939dafd46ec. Base c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98; tree 6f8e17c12da42ad901c90bc764fc39958cca5854; manifest SHA-256 26b8fb178aecaf3dccf038ee2e108dc4ce913f7f07baff10cff5efbe11011aee.

Git object repository: D:/Pontius/tmp/v0a-blueprint-artifact-impl-r001/authoring. Candidate source is the frozen Git commit, not that directory's mutable working bytes. This packet's files/ contains the changed raw blobs, source.diff is the complete non-generated diff, and review.diff additionally includes both generated outputs. Parse large generated JSON/TOML structurally instead of dumping their single long lines. Independently recompute all12 raw blob hashes and the digest-first whole-row manifest.

## Binding requirements

Read CLAUDE.md, docs/workflow.md checklist v1 and ADR-0490 at the base. Read all three adopted documents under docs/architecture/v0a-blueprint-artifact-r002/. ADR-0490 activates their specified mechanisms/scope; retained draft wording is historical, not a source-opening blocker.

The controller subsequently approved two exact prospective extensions. Read packet inputs/driver-amendment-authorization.md (SHA-256 0d5cd53eb456a47a0ff346034fdfad173c77a39e37b030c99205c4913eeb2af7) and inputs/inventory-amendment-authorization.md (SHA-256 666d89a6708c9d749265d816d063857432be42d754b6e76ad2dbafff6ba98ea3). They permit only the existing driver's source origin and3internal edges, plus registration of its unchanged12-test suite and attributable census data. No runtime/driver/test-method/analyzer edits or capability grants. Other original bounds remain:300source lines,300new-test lines,2fixtures <=8192bytes,100manual added+removed registration lines, initial candidate plus at most one bounded correction.

Review every adopted requirement: complete fixed JSON schema and exact graph; independent field/canonical-byte oracles; genuine HandRuntime hit/miss/illegal-hit and complete ReplayHost outcome checked by independent expected policy; numeric and Unicode closure at both public APIs; malformed/duplicate/partial admissions; no artificial capacity cap; real boundary-gate positives/negatives; precise registration without relaxing unrelated rules. Check implementation and tests, not only self-report claims. Preserve the zero-grant distinction: registration is not proof the parked analyzer is sound or permission to execute its blocked paths.

## Permitted evidence and execution

In implementation-report.md, only the sections headed TDD and focused execution evidence, Registration and generated outputs, Census attribution, and Budgets and final hygiene are permitted evidence; implementation narrative/other review reports are not. Raw receipts under this task's run-records/ are permitted. Relevant families: codec-focused*, codec-min-digits*, boundary-shape*, registration-stable-final*, inventory-focused*, inventory-fingerprint-attribution*, and frozen-codec*. Failed attempts are retained; read exits rather than infer PASS from filenames. The premature full inventory run contains a sandbox hardlink permission failure plus then-unupdated census/ordering failures; it is not post-CLEAN acceptance. Broad acceptance has not run and must wait for both CLEAN reviews.

Do not duplicate all already executed focused suites on identical bytes merely for ceremony. Select independent targeted falsifiers for material risks, using fresh snapshots. D:/Pontius/tmp/v0a-blueprint-artifact-impl-r001/run-snapshot.ps1 accepts unique RunName, Slot311/314, PythonArgs and MinimumDigits; critically pass Overlay D:/Pontius/tmp/v0a-blueprint-artifact-impl-r001/packets/r001/files so source comes from the frozen blobs. Floor first, exact development interpreter second if needed; -B -P, scrubbed environment, absolute PONTIUS_GIT, snapshot cwd/src. Inspect the helper before use. No payload in primary/authoring checkout; no operating, rehearsal, scientific, optional-dependency or network execution. A native-launch escalation may be needed for the fixed3.14 slot. Never substitute interpreters or hide refusals.

No source/index/ref mutations, fixes, dependency installs, commits, pushes, publication, cleanup of retained artifacts or subagents. Reviewer-owned report/probe files may be created only in the assigned reviewer directory under this packet. Both reviewers are blind; do not read sibling reviewer directories or outputs.

## Report contract

Bind report to commit+manifest. State Spec PASS/FAIL, Quality PASS/FAIL, C/I/M counts, CLEAN or required-corrections verdict, and SOUND/STRAINED/WRONG SHAPE with reason. Include strengths, requirement-to-evidence mapping, exact fresh checks, limitations and any unverified claims. Every Critical/Important finding requires a concrete input/state -> wrong outcome scenario or directly demonstrated missing acceptance contract. Distinguish required outcomes and verification from advisory implementation choices. Do not implement fixes. Write one attributed verdict-line file beside your report; do not update another issuer's ledger.

This candidate and packet are local, not yet remotely published or adopted. The requested result is an independent technical review, not a publication, broad-acceptance, source-seal or invocation authorization.
