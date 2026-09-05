# Independent Tier-C cold review A — v0a consolidation r004

Verdict: **CLEAN** for the controller-approved scope. **Specification: PASS.
Engineering quality: PASS. Design: SOUND.** Critical: **0**; Important: **0**;
Minor: **0**. No required corrections or separate advisory findings.

This is a review finding, not acceptance, integration, source-seal, rehearsal,
experiment, commit, merge, or push authorization.

## Bound identity and scope

- Candidate: `fe1e2fc68675c6c92a1263450b455011b5987207`
- Manifest: `6eb5ec280b6a8051e88d7659920ef74b46ea682a06dc80f688ed951d75f3f221`
- Ref: `refs/heads/review/v0a-consolidation/r004`
- Parent/base: `bb959371eec17e76ab46ee6e42f1bac49c26d54a`
- Tree: `27fa787e80f504f17233c29961d9df545f8eb7dd`
- Review date: 2026-09-04

I independently verified the ref, parent and tree, recomputed the manifest from
Git blobs with rename detection disabled and whole-row digest-first sorting,
and compared the resulting row bytes with `manifest.sha256`. All agree.
`checks-311-identity-native/00.log` records the result.

All six `src/pontius/v0a/` modules and all four `tests/test_v0a_*.py` suites
are exact Git-blob matches to r007 commit
`ddea6efbeb55cb8b71da1ebd5a359a0c2c901cf1`. The dependency-baseline blob remains
`5fe6ee47f3380b65887b528efef05b72c8e6ac0a`. The complete changed-path inventory
contains only those ten imports, two generated artifacts, and the five declared
manual files. No inherited kernel, ADR, STATUS, dependency file, or ledger is
changed, and existing CI hard gates remain in place. Manual additions total
**357**, below 600.
`git diff --check` passed; no added manual line exceeds 100 columns.

The authoritative replacement requirements and deferred coverage file match
their handoff SHA-256 pins. I read the handoff first, then the requirements,
candidate CLAUDE.md, workflow checklist v1, increment-one brief, ADR-0485,
ADR-0486, and relevant frozen source. `initial-inventory.md` was written before
the deferred coverage claim was opened. No other review, implementation
conversation, or previous-round narrative report was used.

## Specification and quality evidence

| Invariant | Independent evidence | Result |
| --- | --- | --- |
| An attempted receiver/default misalignment yields an explicit refusal | Eleven independent public-review fixtures; ten deterministically raise the baseline strict-zip ValueError, while the candidate returns the specified blocker in all eleven | PASS |
| Refused invocation produces no exact capability row and blocks approval | Every refusal fixture has zero expanded rows; approval is attempted with that review's own tokens and rejects for unresolved blockers | PASS |
| Sensitive, inert, and nested-helper paths retain the refusal | Fixtures cover sensitive subprocess-shaped source, plain-return source, and an analyzed local wrapper reaching the helper | PASS |
| Supported bindings retain baseline behavior | Ordinary instance method, classmethod, and static method through the class each retain one identical exact row and identical blocker lists | PASS |
| Normal registration still derives the review and grants nothing | Real --write, --check, review export, and artifact audit on both interpreter versions | PASS |
| v0a origin/import/complete-deal boundaries remain enforced | Thirteen independent boundary cases, the 52-test boundary suite, and the real public repository boundary command | PASS |
| Four direct CPU CI gates are added without demoting existing gates | Full workflow diff and inherited environment inspected; only four direct gate steps are added | PASS |
| Ten core imports and retained baseline remain exact | Independent Git-blob comparisons and focused regression suites | PASS |

The independent review fixture is `probes.py`, using `derive_design_review`
directly with independently constructed source bytes and inventory input. It
does not call the private binder and does not execute the illustrative
subprocesses. Cases extend beyond the supplied regression to multiple defaults,
positional-only parameters, a keyword-only default, explicit positional
arguments, and an explicit keyword. The explicit-keyword case also receives the
required refusal although its baseline outcome does not reach the strict-zip
crash. Expectations follow the replacement refusal rule, not positive Python
descriptor inference.

The generator production diff is limited to four registration strings, the
frozen reason-bearing refusal value, the alignment guard, and the two consumer
adjustments. `_bind_helper_arguments` has exactly two consumers, in
`_review_body` at candidate lines 22948 and 23062. Both append the refusal and
continue before their helper-sensitivity filtering and before row derivation.
The registered path retains its ordinary `None` semantics. The local path moves
binding ahead of its filter without otherwise changing supported binding logic.
`validate_design_approval` checks blockers before accepting approval tokens.
The normal writer and checker still call `derive_design_review`; there is no
derivation bypass, failure suppression, descriptor scanner, or new receiver
provenance machinery.

Real review exports are byte-identical across 3.11 and 3.14, SHA-256
`efbcb651f35792326ae78d95f7bba7162a8a77b297730fb8f1d3021d95af62e4`.
Each has **141** existing exact rows, **zero v0a rows**, and **seven** explicit
alignment blockers at real `TerminalAdmissionTests.host_case` call sites.
The generated inventory has **182** v0a entries in **four** payloads. Both
`spec_capabilities_sha256` and `capability_bindings_sha256` remain all-zero.
The four payloads have no probes or environment additions, allow only temporary
write roots, and are not serialized. After ordinary generation, both artifacts
match the frozen Git blobs byte-for-byte. Both normal-user clones finish clean.

## Deferred coverage assessment and design verdict

The claim's discovery method agrees with the independently recorded inventory:
trace the concrete failing binding and enumerate both consumers, then verify
that refusal reaches the public review and approval boundary. Its stated limits
are appropriate to the controller's replacement contract. The additional
argument-shape probes and independent boundary matrix found no missed in-scope
member or new false exact result.

A valid local function normally does not undergo receiver removal. The nested
public case proves propagation through an analyzed local wrapper; it does not
prove discovery of arbitrary wrappers or directly exercise an otherwise
unreachable local-function misalignment. Source inspection supplies the evidence
that the local consumer handles the typed result before its sensitivity filter.
This is an explicit coverage limit, not a demonstrated missing acceptance case.

**SOUND** applies to this narrow replacement: a small typed refusal at the
inconsistent alignment point, consumed explicitly before filtering, fits the
crash-to-blocker contract and is straightforward to audit. The same verdict is
not extended to the parked general analyzer, whose known unsoundness remains
accepted only within ADR-0486's zero-grant registration scope. No broader
analyzer redesign or descriptor patch series is recommended by this review.

## Fresh execution receipts

All payload execution used disposable D:-local clones, snapshot cwd, `-B -P`,
`PYTHONPATH=<snapshot>/src`, scrubbed PYTHON/GIT_/PONTIUS_ variables, absolute
`PONTIUS_GIT=C:/Program Files/Git/cmd/git.exe`, and scratch-local TEMP/TMP/TMPDIR.
CPython **3.11.15** at `D:/Pontius-tools/py311/Scripts/python.exe` ran first;
CPython **3.14.6** at `D:/Pontius/.venv/Scripts/python.exe` followed completion
of the required floor checks. A redundant normal-user floor export continued
in its separate clone while confirmation began; no mutable clone was shared
between interpreter runs.

| Check | 3.11.15 | 3.14.6 |
| --- | --- | --- |
| `tests/test_v0a_contract_faults.py` | 22 tests, exit 0 | 22 tests, exit 0 |
| `tests/test_v0a_hand_replay.py` | 45 tests, exit 0 | 45 tests, exit 0 |
| `tests/test_v0a_replay.py` | 62 tests, exit 0 | 62 tests, exit 0 |
| `tests/test_v0a_trace.py` | 53 tests, exit 0 | 53 tests, exit 0 |
| `tests/test_inventory_and_profiles.py` | 88 tests, exit 0 | 88 tests, exit 0 |
| `tests/test_stabilization_boundaries.py` | 52 tests, one platform skip, exit 0 | 52 tests, one platform skip, exit 0 |
| `tools/check_stabilization_boundaries.py` | exit 0 | exit 0 |
| `tools/generate_test_inventory.py --write` | exit 0 | exit 0 |
| `tools/generate_test_inventory.py --check` | exit 0 | exit 0 |
| `tools/generate_test_inventory.py --emit-design-capability-review <temp-child>` | exit 0 | exit 0 |
| Independent binding and boundary probes | 14 + 13 cases, exit 0 | 14 + 13 cases, exit 0 |
| Independent artifact audit | exit 0 | exit 0 |

The principal complete receipts are `checks-311-native/commands.json` and logs
00–11, and `checks-314-native314/commands.json` and logs 00–12. Supplemental
floor probe receipts are `checks-311-probes/`; 3.14 probe receipts are
`checks-314-probes-native314/`. Floor artifact audits are in
`checks-311-audit/` and `checks-311-audit-native/`. The executable recipes and
fixtures are `run_checks.py`, `probes.py`, `boundary_probes.py`,
`audit_artifacts.py`, and `identity.py` in this review directory.

Initial restricted-user attempts are retained separately: the floor inventory
suite completed with one WinError 5 while hardlinking the installed executable;
Git identity checks met repository-ownership restrictions; a supplemental 3.14
launch was denied by the sandbox. Normal-user reruns resolved these environment
limitations without changing global Git trust settings. No partial or failed
receipt is counted as passing. The boundary suite's one skip is the existing
POSIX directory-descriptor mutation test on Windows.

## Coverage limits and authority boundary

No hosted GitHub Actions run was initiated; CI evidence is the workflow diff
plus local execution of the exact added suite commands. No POSIX environment,
broad test profile, GPU workload, experiment, performance campaign, or lifecycle
owner was run. This review does not re-review the whole r007 core design or
establish general Python binding, alias, descriptor, or reachability soundness.
The frozen repository and prior candidates were read-only; execution and
generated review artifacts stayed inside the assigned scratch directory.
No fixes were implemented and no integration was authorized.
