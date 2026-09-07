**Codex /root — independent cold metadata review: NOT CLEAN / SOUND.** Exact incorporation and the accessible qualification, cost, census, CI, and authority checks pass. The NOT CLEAN verdict is an **evidence-verification blocker**: this environment denied access to the 16 raw positive historical-launcher files needed to complete the requested verification. I found no demonstrated behavioral defect, numerical misstatement, or unauthorized expansion in the three metadata files.

This report applies exclusively to the following frozen identity:

| Binding | Independently verified value |
|---|---|
| Task | `v0a-blueprint-preparation-seal/r002` |
| Candidate | `06ccb89587478c09493ec0eda53f8e62a4dece95` |
| Parent/base | `c9a8aa95a1c8f65bcfb15288cbc5e4492314e457` |
| Candidate tree | `92c5f6d5637a342aeb38f5fffd540a27669dd27c` |
| Complete 27-path manifest SHA-256 | `e99482ab23a5d0538733e7ae0dc19b562c40a66a03a32bb544beb6ec4384d609` |
| Incorporated source | `666cb43b097707a54733a51cd7930d55920a5af7` |
| Source tree | `2515fe2cf7259b611f60e5b2582e846422cb0247` |
| Complete 24-path source manifest SHA-256 | `4ac5089861356eb3bfe25f8d4c2b45aff3c9b39b4306a51a66ea3f5d01fa4012` |
| Semantic source base B | `363c9fb669e19a30375537ee5e92ea338a840a2d` |

I conducted read-only inspection and calculations from `D:\pseal-review-r002\snapshot`, using `C:/Program Files/Git/cmd/git.exe` for every Git operation. I executed no repository tests, generators, profiles, poker, owner commands, publishing, or lifecycle operations. I changed no source, packet, index, ref, or ledger. I read no sibling metadata review or implementer transcript/helper directory. The three issued source-review reports were used only as evidence of the existing source checkpoint.

The severity-ordered required finding is:

1. **Important — historical acceptance remains unverified against its required raw primary records.**

   The affected claim is in [ADR-0514, lines 103–110](D:/pseal-review-r002/snapshot/docs/decisions/ADR-0514-source-seal-accounted-immutable-blueprint-preparation.md:103): both interpreters’ actual positive standalone historical invocations passed 55 tests with zero skips, with their source, argv, and child receipts retained separately.

   The qualification record binds eight files beneath each of these roots:

   - `D:\Pontius\tmp\blueprint-preparation-implementation-20260907-001\r002-qualified-311-002\temp\evaluation-history-62l9pqwk\positive`
   - `D:\pq-r002-314-001\temp\evaluation-history-rrv01i8p\positive`

   In each root, reads of `summary.json`, `intent.json`, and the runner, boundary, and v2 `stdout.bin`/`stderr.bin` files returned **Permission denied**. Thus, all 16 required files remain unread and their recorded hashes remain unreproduced in this review.

   The readable outer six-test launcher receipts and `historical-bridge.json` records support the reported 28/19/8 outcomes. The separate CI rehearsal also has readable, passing historical child records on 3.11. Those are useful supporting evidence, but they do not independently verify the inaccessible positive invocation records for both qualification cohorts.

   **Concrete review failure:** accepting the metadata claim solely from the derived bridge records would leave this review unable to detect a discrepancy in the bound raw historical outputs, including an omitted skip, wrong count, or different invocation. This is an access and verification failure; it is **not evidence that any historical suite actually failed**, nor proof that the retained files are absent.

   **Required closure:** make the exact bound primary bytes accessible to the reviewer, either at their retained paths or through explicitly identified byte-identical retained copies. Verify every recorded hash, the B commit/tree and actual interpreter identities, `--suite all` invocation, three child counts 28/19/8, zero skips, native exits, and separation from deliberate nonzero/skip controls. No source edit or test rerun is required merely to resolve this access problem. I requested an accessible-copy location during the review; none was supplied before this report.

   Until that verification is completed, I cannot issue the requested complete CLEAN verdict. No other required correction was established.

I read `CLAUDE.md`, `docs/workflow.md`, ADR-0509’s integration procedure, adopted ADR-0513, its immutable brief/design/source contract, the implementation plan, candidate ADR-0514, the performance report, and generated STATUS. I also inspected the relevant evidence protocol, architecture boundaries, roadmap prerequisites, and unchanged STATUS derivation logic.

**Identity and incorporation are reproduced.** For both source and integration candidates, I independently enumerated the complete parent-to-candidate delta with rename detection disabled, retrieved every changed blob through native Git, SHA-256-hashed the raw bytes, constructed the prescribed two-space/LF manifest rows, and sorted the complete rows by bytes. Both reconstructed manifests equal their packet `manifest.sha256` files byte-for-byte.

All 24 source paths have identical blob identities in the source and integration candidates. The complete source-to-integration tree delta contains exactly:

| Metadata path | Change | Raw blob SHA-256 |
|---|---|---|
| `STATUS.md` | Modified | `cb282c0e51d40f0dcb920a1e2cdb070b14453a1ce05cc6887b67a58449b6dce6` |
| `docs/architecture/v0a-blueprint-preparation-r001/performance-report.md` | Added | `96b30907d3efc60b9206f21ea4d96dbf7c375989c50d61f37bda123de41f1285` |
| `docs/decisions/ADR-0514-source-seal-accounted-immutable-blueprint-preparation.md` | Added | `62ac8179898bb61fbb02376dee9744958487bf36cf17bda2e52a1b4c58808ac7` |

All three resulting modes are `100644`; their raw blobs are LF-only, BOM-free, and have no trailing whitespace. There are no other source-to-integration path, mode, or blob changes.

**The Tier A integration classification fits the inspected delta.** The underlying source remains Tier C work supported by its existing review and qualification checkpoint. This metadata integration does not introduce another source implementation, alter an acceptance predicate, or change evidence semantics. ADR-0514 expressly conditions adoption on its separately authorized decision commit, and that restriction appears verbatim in STATUS. The draft grants no operating or research owner, training authority, demonstration, consumed-owner retry, or external publication authority.

The unchanged 14,000 ms work cutoff, 15,000 ms action wall, preparation-bank meaning, independent host reference, and distinction between historical and current acceptance remain explicit. The next-work language calls for prospective preregistration; it does not itself authorize that workload’s execution. The inaccessible evidence does not demonstrate a higher-tier metadata change, but it prevents completion of this light review.

**The source-review account is supported by the issued reports.** I verified the hashes of the two r001 reports and the r002 mechanical report against the closure record:

- Reviewer A: original **NOT CLEAN / SOUND**, solely for the required Minor restoration of three CI comment encoding spans.
- Reviewer B: original **CLEAN / SOUND**, with the same issue advisory.
- Reviewer M: **ELIGIBLE / CLEAN / SOUND** under Stage 4, closing the required correction without claiming a new substantive cold pass.

The metadata preserves those original verdicts. The closure record’s statement that broad gates had not yet run describes its historical checkpoint; the later qualification records supply the subsequent acceptance account. I did not repeat the whole-source substantive review.

**The accessible current acceptance and CI claims are reproduced from receipts.** I checked all 37 selected commands for each interpreter against their individual intents, receipts, and raw stdout/stderr: 74 commands total. Their recorded candidate, argv, `-B -P`, snapshot cwd/src, scrubbed environment, and absolute native Git agree with the reported qualification.

Each interpreter records 741 current tests, including one skip: 740 passed, zero failures/errors, and the unchanged Windows skip of the POSIX directory-descriptor mutation test. The five new suites account for 19/8/3/19/6 tests. The floor cohort’s accepted receipts belong to the three disclosed source segments; the current cohort uses one segment. The retained source checks bind these segments to the qualified source commit/tree. Runtime preflights identify actual 3.11.15 and 3.14.6. Retained file chronology supports floor completion before current, followed by CI rehearsal and timing; filesystem timestamps are corroboration, not an independent tamper-proof chronology.

For all eight changed CI blocks, I independently extracted the frozen block, reproduced its recorded hash, applied exactly the listed substitutions, and matched the resulting script bytes and hash. All eight corrected rehearsal receipts report native exit zero. The directly selected counts are correctly distinguished as 55 current outer tests and 55 historical tests. The separate historical rehearsal’s raw outputs show 28/19/8 passing tests. Hosted CI is explicitly unclaimed.

The retained failed floor outputs support the disclosed eight clone-setup errors and the later one-failure native-path spelling assertion. The failed CI rehearsal remains distinguishable from its corrected successor: six blocks exited nonzero, while boundary and v2 already exited zero. Raw output supports the missing NumPy failure and the separate B admission comparison supports the bare-interpreter layout refusal. These attempts are not relabeled successful.

The initial preflight root contains its source identity and no gate payload receipts. That is consistent with stopping before payload execution, but the exact LF/CRLF causal account was not independently reproduced from a retained failure output in the inspected inputs.

**Registration and census claims are reproduced without running the analyzer.** Native-blob inventory comparison establishes:

- 3,120 old stable IDs preserved; zero removals.
- Exactly 55 changed existing records, with only `assignment` changed, distributed 28/19/8 across the named historical suites.
- Exactly 60 additions, producing 3,180 IDs.
- Existing baseline-assignment fields preserved.
- The five new suites contribute 55 additions; four inventory tests and one manifest test contribute the remaining five.

I independently reproduced the old 167-row historical digest and the approved 170-row digest. All old rows and snapshots remain, with exactly the three named selected-test rows and one snapshot added. The new digest is `7311fbe67c736ae1d7c72e15aa438db8aee6efc063de3459d95abadbaa0754c8`. The retained current-file inputs checked at the original D-local paths and both final qualification snapshots match their recorded hashes.

I hash-verified all eight raw census captures and reconstructed the complete ordered collection comparisons for both interpreters and both test/production captures. After the recorded historical removals, additions, source-line maps, and the explicit `_assignment(row)` mapping, the retained collections match with no discrepancy. Added anchors match their named native Git source blobs.

The literal-refresh claim also reproduces: exactly 23 scalar changes, equal 30,830-line lengths, and identical ASTs after scalar erasure. The metadata accurately discloses that the eight full captures were not rerun after this refresh and distinguishes those captures from the final full inventory suites.

**The cost tables are reproduced from raw observations.** I verified the published hashes of the qualification record, pre-timing definition, measurement summary, and performance report. I inspected the fixed diagnostic definition and measurement/consumer scripts as text, without executing them.

From the four raw `blueprint-costs.json` records, I independently recalculated every published row:

- 40 warm-call comparison rows, including all medians, minimum/maximum batch means, and matched ratios.
- 24 construction comparison rows from five fresh observations per size/version.
- 16 retained/peak allocation comparison rows.

All match the report’s displayed rounding. The fixed records specify three warmups, five batches, and 20 calls per batch. Source digests and provider configurations agree between versions. The reported 1,024-entry provider range and 80.6–100.3× matched ratios are supported.

The report honestly includes the empty-table warm-call slowdown, distinguishes B’s identity-wrapper lookup setup from owned preparation, includes prepared ownership/index/canonical-byte allocations, and states tracemalloc’s exclusions. Batch means are not presented as individual-call percentiles or tail latency.

I independently compared all eight raw three-hand session outputs with their retained derived records, predeclared literal action vectors, settlements, carried stacks, child outcomes, and decoded decision frames. All 24 hands complete consistently; the eight session IDs are distinct. The parent elapsed times match their receipts. These one-entry controls do not establish large-table throughput.

For the single v3 matrix, all 12 unit records and six completed pairs support the reported compatibility result. I compared full applied actions, settlements, carried stacks, and selected policy/fallback counters with the retained historical control. Cleanup and failure fields match the reported successful disposition. The result hash reproduces as `1016b785adf9be44c4c1883617b521878b687a939e691c05dc6aea750d865afb`, and the parent receipt records 46.1445104 seconds. The retained reader-consumption records identify B’s two readers and the candidate’s three readers.

The older 49.2236669-second matrix is correctly labeled historical context, not a simultaneous A/B comparison. No strength, universal deadline, million-entry resource bound, or native-migration conclusion is inferred. The absence of unrelated concurrent activity remains a recorded measurement condition; retained output alone cannot independently establish a complete machine-activity history.

**STATUS is consistent with the candidate’s metadata.** Independent parsing of all 514 raw ADR headers reproduces its header digest, `b1f18140c8203b9c7c2f93141263975967c211164e6d80745778277a72466a1e`. Its current-decision section equals ADR-0514’s Decision section exactly, including the adoption restriction. The research result, governing runtime contract, revoked authorities, process decision, blockers, and next boundary agree with the candidate. This static verification does not replace the prescribed post-closure STATUS gates.

The evidence-hash traversal found no mismatch among readable indexed files. Besides the 16 historical files described above, direct rehashing of the recorded base 3.14 executable was access-denied; its retained runtime records remained readable. I excluded the referenced implementer registration report under `blueprint-implementation-work` and used the permitted raw registration evidence instead.

The design verdict is **SOUND**. Exact source incorporation, conditional adoption language, separate current/historical accounting, and explicit performance limitations fit the adopted integration procedure. The unresolved problem is access to required evidence, not a demonstrated structural weakness requiring redesign.

**Advisory only:** no additional source, metadata, or design change is recommended from the completed checks. Resolve the evidence-access blocker and issue an attributed verification record. Applicable unchanged STATUS checks still follow review closure: generator `--check` and all twelve status tests on actual 3.11.15 first, then 3.14.6, in four fresh exact-candidate D-local snapshots. None was run in this review.

Confidence is high in the reproduced identities, numerical tables, accessible current-gate records, CI substitution checks, census comparisons, and authority assessment. The largest unresolved question is agreement between the derived historical acceptance summaries and their inaccessible raw positive records. The cheapest falsifying check is read-only hash and content verification of those exact 16 files. A hash, invocation, count, skip, or exit discrepancy would require a factual qualification correction before closure.

External packet publication remains recorded as pending after an earlier automatic approval rejection. I performed no publication attempt and independently establish no remote-upload state. This report authorizes no decision commit, push, external publication, invocation, or lifecycle action.

Codex /root (independent cold metadata reviewer) | task=v0a-blueprint-preparation-seal/r002 | candidate=06ccb89587478c09493ec0eda53f8e62a4dece95 | manifest_sha256=e99482ab23a5d0538733e7ae0dc19b562c40a66a03a32bb544beb6ec4384d609 | defect=NOT CLEAN | design=SOUND | reason=required raw historical-acceptance verification blocked by access denial