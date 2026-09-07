# Independent Tier A metadata light review

Reviewer: Codex /root/evaluation_seal_light_review. Issued 2026-09-07.
Round: v0a-evaluation-seal/r001.

**CLEAN. Specification PASS. Engineering PASS. Design SOUND.**

Required findings: none. No incorporation or metadata correction remains. This
verdict completes only the independent light-review gate. The four exact-candidate
metadata checks and separate controller commit authorization remain pending.
No decision is adopted by this report.

## Binding identity and independence

- Candidate: 4f6096f274e4c8c8c05e4607651bf426d3b1ad9c.
- Ref: refs/heads/review/v0a-evaluation-seal/r001.
- Parent/base: 34616938c708b1ca306b9d8a17b9d98e2f9e451f.
- Tree: 54a257f4f2957696b9d33e7338ce140206a3f578.
- Manifest SHA256:
  983ed0dbf779f7fa96755ef4d87081506d0293cebcc8273aa187c6a3126dcc47.

I read handoff.md first, then the packet identities, manifest, metadata diff,
frozen metadata and incorporation audit. I read CLAUDE.md, the applicable workflow,
adopted ADR-0508/source-contract and ADR-0506 integration precedent. I authored
neither source nor metadata. No implementation transcript, coordinator conversation
or other current metadata review was used. The coordinator supplied only the missing
filesystem locator for the controller ruling already pinned by ADR-0509.

The two immutable Tier C source reports and raw retained acceptance records are
permitted evidence inputs for this mechanical incorporation/metadata review. I did
not conduct another substantive whole-source review or introduce an execution gate.

## Requirement-to-evidence assessment

| Requirement | Fresh inspection and result |
| --- | --- |
| Exact frozen identity | Native Git resolves both metadata and source refs, parents and trees. All fourteen packet files equal frozen raw blobs. Whole-row digest/two-space/POSIX-path/LF manifest bytes independently recompute to the bound digest. PASS. |
| Exact source incorporation | All twelve source paths equal bca326c6bfedd71324a19c809f617e267cc9e0a2 and both permanent/original packet copies. The source manifest recomputes to 02f06a3ae8a7cefb5ba8f5a5abaf94f2a91a661a1d5f1ade3e1b3f8c4ae02860. PASS. |
| Complete integration scope | Full-tree comparison shows exactly twelve source paths, new ADR-0509 and STATUS.md. Every other tracked baseline entry retains its mode/type/object identity; no deletion or hidden source change appears. PASS. |
| Source-review claims | Both actual reports bind the exact source commit/manifest, say CLEAN, specification PASS, engineering PASS and design SOUND, state no required corrections and document initial independent inventories. Raw hashes and original/permanent copy equality pass. |
| Source acceptance | All 32 receipt hashes and snapshot HEADs match. Every preflight and payload exits zero. The sixteen named commands run on actual 3.11.15 first and 3.14.6 second, with distinct snapshots and chronological ordering. Raw unittest summaries total 296 per interpreter with zero skips. PASS. |
| Retained prior outcomes | All 52 prior receipt hashes match. Actual nonzero failures remain separate from selected final acceptance. PASS for the cited index claims. |
| Census and budgets | Source audit, ruling, both comparisons and all eight raw capture hashes match. Counts and source identities agree with the ADR and source reports. Fresh line/AST counts confirm 1232 production lines, 1656 test lines and 24/28/19 tests; fixture is 20335 bytes. PASS. |
| Generated status | Successful generation and module-origin/version preflight match the pinned receipt. Its snapshot differs from this candidate only in STATUS. CRLF-to-LF normalization alone yields the frozen output. Independent 509-header digest matches STATUS. PASS. |
| Authority boundary | Conditional acceptance header, Decision and generated front door preserve separate adoption, prospective population and invocation boundaries. No comparative run or demonstration authority appears. PASS. |

## Raw evidence and factual claims

Incorporation audit SHA256:
2bfbb3cdcb35560d0c4b87d4ed8f5735d75a0ba0552bc77e8ecb42c2c2a4cbff.
Actual source review hashes:

- review-a.md: 034bc3a780b0e83c34519707183dff5dc33fedab6289efa4a0407f554b4e09cc.
- review-b.md: 255af51e120b379e371083724f011c5edc314a577a1b4a3655ed7b34d4786346.

The source checks/final-acceptance-summary.json hashes to
 de8544829b01d05d5f2ff2d3b3b5168bdff20b8de40355368aeb000af03e9bcb.
Its pinned run-source-snapshot-v2.ps1 hashes correctly; read-only inspection confirms
fresh create-only snapshots, detached exact candidate, scrubbed environment,
snapshot cwd/src, absolute native Git and -B -P. Raw receipts supply actual-version,
flags/cwd probes, argv, exits and test summaries. The selected population totals
592 executions across both interpreters. This is retained evidence, not a test run
performed by this reviewer.

The badmit1 boundary failure, igen1 inherited-TestCase inventory refusal, bregred1
registration RED, FIX01 conflicting-prefix RED and FIX02 native-identity/retention
RED retain their nonzero exits. Earlier syntax/setup failures and deliberately
failing controls are likewise visible. Census 3.14 captures retain a SyntaxWarning;
neither the ADR nor this review claims warning-free execution. No failed receipt
was counted as selected final acceptance.

Source audit SHA256:
d9b949942d44643d228a544d50c5dcf71b656967dca1cb47a54a198a06464167.
Its 138 manual registration added/removed lines agree with both source reviews and
remain below 160; generated material is counted separately. The independent 1232
production-line count is above the historical 1200 cap but below the explicit 1250
ruling. The source packet coordination/controller-budget-ruling-2026-09-07.md equals
its original SDD copy and hashes to
82c997a7b7702adc5d35389b27234107177caf49c3ebf6e794597b52ea32e0d9.
It expressly increases 1200 to 1250 without weakening correctness, sealed-source
or population limits. Historical adopted documents remain unchanged.

The complete test comparison hashes to
1bf46c9f01fb4a62a2c94248858e1c28784e6fcb28030e4dd6af2c98a8c35cad;
the production comparison hashes to
81fe7ddaec4c7c1d6bf7b75d39ea7bb3747a7afc5a24ac1f534ed63098e7a317.
Every named raw input hashes correctly. Both baseline/candidate pairs are equal
across actual interpreters after removing only the interpreter string. Census
snapshot 6f59993ba2e5229e2d8ffdbb8de4187b576450b4 has the identical whole tree to the
accepted source, while its distinct commit identity remains explicit. Both records
preserve 141 expansions and account for 15 blockers, 6 analyzed sites, 146 helper
edges, one decoy, 72 universe and 72 deny-all additions: 312 bound occurrences each.
The preservation records and independent source reports support the ADR's 3041 old
inventory and 440 old payload claims. I did not redo the Tier C per-occurrence
semantic analysis or the reviewers' finite poker-start accounting.

Generation receipt mgen1-311.json hashes to
892bda7876e2486d4d03f4406599ce11fcdb11056a705b93f4e39048b65eff8c.
Its raw generated STATUS hashes to
5683e1e9be833b1376b25ca27026657daaf7237001321d5fb36664a013ec2438;
CRLF-to-LF conversion alone yields the candidate hash
fb13f499663e0a7fcf0ca5ec491fe50207ab3cfc4fc23cdabf4c656f17f36593.
The preparation refusal separately retains the failed culture-sensitive BOM
predicate after successful generation; no content edit or second generation is
needed to explain the incorporated output. Independent parsing of all 509 ADR
headers recomputes
300870b1d751c1de31a34ad6d134bc51d1b9c3bf54172dfea863739ae53124ad.

ADR-0509 retains research ADR-0280, runtime ADR-0307 and all four revoked owners.
The next step requires prospective population/invocation work. Accepted-prefixed
status remains explicitly conditional on a separately authorized decision commit,
consistent with ADR-0506; the frozen review ref does not adopt the decision.

## Design verdict, next gates and limitations

**SOUND.** The existing source-seal integration shape fits: exact source pins,
factual retained outcomes, generated front door and explicit later authority.
No competing runtime, acceptance rule or evidence meaning is introduced.
Required corrections and design remediation: none.

After this CLEAN verdict, retain the four prescribed metadata checks in order:
status --check and all twelve status tests on actual 3.11.15, then the same two on
actual 3.14.6. Each requires a fresh exact metadata candidate D-local snapshot,
-B -P, scrubbed environment, snapshot cwd/src, actual-version/flags/cwd and
status-module-origin preflight, and absolute native Git. This report certifies
neither those pending commands nor authorization of the ceremonial commit.

Inspection used absolute native Git with --no-replace-objects and per-command
safe.directory, plus standalone stdlib hash/JSON/AST/header inspection under
D:/Pontius-tools/py311/Scripts/python.exe -B -P -. Initial Git ownership refusal
was resolved without global configuration changes. The first report write found
that the reviews directory was absent and wrote no file; the directory was then
created solely to hold this create-new LF report. No payload, test, generator,
analyzer, poker process, subagent, source edit, commit, push or upload was run.

This establishes bounded incorporation and metadata consistency, not another
whole-source proof, performance result, universal OS-failure coverage, poker
strength, statistical population or invocation authority. The separate GitHub
handoff upload was reported blocked by automatic approval review and pending exact
user permission at freeze. I did not attempt it; local preservation is not remote
upload evidence. Source sealing remains inactive until its separately authorized
ceremonial decision commit.
