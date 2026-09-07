**Codex /root — fresh independent evidence-verification supplement: CLEAN / SOUND. The sole required raw-evidence access finding is CLOSED.**

This is the focused, non-cold completion of the access check for **`v0a-blueprint-preparation-seal/r002`**, limited to ADR-0514 lines 103–110. It is not another full source or metadata review. The [original metadata report](D:/Pontius-handoffs/v0a-blueprint-preparation-seal/r002/reviews/review-001-codex.md) retains its issued **NOT CLEAN / SOUND** verdict.

| Binding | Independently verified value |
|---|---|
| Candidate | `06ccb89587478c09493ec0eda53f8e62a4dece95` |
| Complete 27-path manifest SHA-256 | `e99482ab23a5d0538733e7ae0dc19b562c40a66a03a32bb544beb6ec4384d609` |
| Qualification SHA-256 | `9e79a7d7d53512fa00058f95521ff0a9bf9ba5c820625cac4ce7815f518155db` |
| Readable-copy mapping SHA-256 | `793bb7d79c8c23b4bde3d6efa901a4052585762373aef3e7e5754f2b3a361134` |
| Original report SHA-256 | `139878d537796d0be50df93e6bd35087160e9ff87120d530acb2a8a1e5e952a1` |

I read `CLAUDE.md`, the applicable workflow evidence-closure instructions, ADR-0514 and the original report. I independently rehashed the qualification, mapping and **all sixteen readable primary copies**, including the six empty stdout files. The mapping’s original `(cohort, path, SHA-256, byte length)` tuples equal the qualification’s complete historical-file population exactly: eight per interpreter, sixteen unique records, no omissions or extras. Every copy matches both its original qualification pin and its mapping entry in digest and length. The mapping writer’s success assertion was not used as the outcome oracle.

I read both actual historical intents and summaries and every child’s raw stdout/stderr. Direct parsing of the terminal unittest results establishes:

| Actual recorded interpreter | Runner | Boundary | V2 | Historical total | Skips | Recorded native child exits |
|---|---:|---:|---:|---:|---:|---|
| CPython 3.11.15 — `D:\Pontius-tools\py311\Scripts\python.exe` | 28 | 19 | 8 | 55 | 0 | 0 / 0 / 0 |
| CPython 3.14.6 — `D:\Pontius\.venv\Scripts\python.exe` | 28 | 19 | 8 | 55 | 0 | 0 / 0 / 0 |

All six stderr records end in unqualified `OK`. Both summaries are complete with null failure fields. Both intents bind **semantic B `363c9fb669e19a30375537ee5e92ea338a840a2d`**, exact tree **`10cc82ff78a84ef901242b2f69540f6a74ec498b`**, `suite: all` and native Git `C:\Program Files\Git\cmd\git.exe`. Each child’s argv selects its expected historical test file with the recorded interpreter and `-B -P`; each cwd is its cohort’s retained `positive\snapshot`.

I hash-verified and compared the supporting bridge, runtime and outer-launcher records. Each bridge’s complete intent and result arrays equal the corresponding primary records, and its 55-test/zero-skip totals reproduce directly from the raw outputs. Runtime records agree with the historical interpreter identities.

Static inspection of the unchanged fixed launcher and its positive-control source establishes the standalone CLI command with `--suite all`, the positive control’s native-exit-zero assertion, and the launcher’s native child-exit recording. It also establishes the scrubbed child environment: historical snapshot `src`, cohort/suite temporary paths, disabled user site, UTF-8 I/O, absolute native Git and isolated Git configuration. The retained outer environments agree with that construction. The launcher checks the complete pinned historical tree before and between child launches and afterward.

The **six current outer tests remain a separate population**. The deliberate exit-7 and skipped-test controls use the separate `nonzero` path and contribute nothing to the selected 55 historical tests. The `REFUSED [WinError 183]` text in both positive runner outputs corresponds to B’s existing-output-root refusal test; its source explicitly expects that refusal and preserved sentinel bytes. It does not indicate failure of either 28-test invocation.

**Candidate identity remains unchanged.** The authoritative local review ref resolves to the specified candidate; parent and candidate tree remain `c9a8aa95a1c8f65bcfb15288cbc5e4492314e457` and `92c5f6d5637a342aeb38f5fffd540a27669dd27c`. I checked all 27 manifest file hashes against native Git raw blob identities and the exact parent-to-candidate path set. All 24 incorporated source blobs match the qualification pins. The source-to-metadata delta remains exactly STATUS, the performance report and ADR-0514.

**No required metadata finding remains open when the original report and this supplement are read together.** No discrepancy or behavioral defect was exposed. SOUND applies to this evidence-verification scope.

The evidentiary limit remains retained-record verification: child exits come from the primary summaries; CLI exit and full child-environment construction are corroborated through the passing outer records and unchanged source. I did not rerun historical processes or independently observe their past operating-system state. The original report’s other residual uncertainties remain unchanged, including its inability to directly rehash the recorded base 3.14 executable.

All work was read-only inspection/calculation using absolute native Git. I executed no tests, generators, profiles, poker, owners, publication or lifecycle operations, changed no files or refs, and read no implementer transcripts/helper directories or sibling source findings. This report authorizes no commit or publication and does not replace the prescribed final STATUS gates.

Codex /root (fresh independent evidence-verification supplement; non-cold) | task=v0a-blueprint-preparation-seal/r002 | candidate=06ccb89587478c09493ec0eda53f8e62a4dece95 | manifest_sha256=e99482ab23a5d0538733e7ae0dc19b562c40a66a03a32bb544beb6ec4384d609 | qualification_sha256=9e79a7d7d53512fa00058f95521ff0a9bf9ba5c820625cac4ce7815f518155db | mapping_sha256=793bb7d79c8c23b4bde3d6efa901a4052585762373aef3e7e5754f2b3a361134 | access_finding=CLOSED | defect=CLEAN | design=SOUND | required_metadata_findings_open=0 | original_verdict=NOT CLEAN/SOUND preserved | commit_publication_authority=none | final_status_gates=not replaced