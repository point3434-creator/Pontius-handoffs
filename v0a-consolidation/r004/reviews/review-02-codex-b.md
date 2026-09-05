# Independent Tier-C cold review B: v0a consolidation r004

**Verdict: CLEAN. Spec: PASS. Quality: PASS. Design: SOUND.**

Critical: 0. Important: 0. Minor: 0. Required corrections: none.

This verdict applies only to the controller-approved narrow replacement, exact r007 imports, reduced registration, boundaries and CI. It does not approve integration or reopen the parked general analyzer repair.

## Candidate and immutable inputs

- Commit: `fe1e2fc68675c6c92a1263450b455011b5987207`
- Manifest SHA-256: `6eb5ec280b6a8051e88d7659920ef74b46ea682a06dc80f688ed951d75f3f221`
- Ref: `refs/heads/review/v0a-consolidation/r004`
- Base: `bb959371eec17e76ab46ee6e42f1bac49c26d54a`
- Tree: `27fa787e80f504f17233c29961d9df545f8eb7dd`
- Requirements SHA-256: `962e70309bdee53edfb54f266c1cd14c2cf6ed17452e81b1b2c4479e3f38f4c9`
- Deferred coverage SHA-256: `cd4116d5f6f0e0a99f71935145d1a1017b25a18f6a09d8154369964709b1fec4`

The first task input read was the handoff. I read the replacement requirements, candidate CLAUDE.md, workflow/checklist v1, increment-one brief and ADR-0485/0486. I recorded `initial-inventory.md` from requirements and source before opening the deferred coverage claim. No implementer conversations, earlier reviews or sibling review output were read; no subagents were used.

`identity.py` independently recomputed digest-first whole-row sorting from Git blobs, compared the actual manifest row file, verified every file-identities row, and checked the exact ref, parent and tree. All match. The six package blobs and four suite blobs equal r007 commit `ddea6efbeb55cb8b71da1ebd5a359a0c2c901cf1` byte-for-byte. The dependency baseline retains blob `5fe6ee47f3380b65887b528efef05b72c8e6ac0a`. The changed path set contains only the permitted imports, generated artifacts, generator/tests, boundary checker/tests and CI. No inherited kernel, ADR, STATUS, dependency file or ledger changed. Manual additions are 357 lines under the stated exclusions, below 600. Git diff whitespace checking passes.

## Findings and design assessment

No blocking or nonblocking candidate defect was established within the approved contract.

The implementation keeps the baseline binder and introduces a small typed refusal at the exact inconsistent-alignment boundary (`tools/generate_test_inventory.py:21644`, `:21667`). Both consumers explicitly append its reason and stop that invocation before sensitivity-based handling (`:22948`, `:23067`). The approval gate still checks blockers before accepting matching tokens (`:24617`). No descriptor scanner or receiver-provenance extension is present in the candidate diff.

**SOUND** is the design verdict for this replacement: the reason-bearing result makes the exceptional binding state explicit, and each consumer owns propagation into the public review. It fits the limited crash-to-blocker obligation without growing the inference engine. This verdict does not endorse the broader analyzer's known-unsound architecture, which ADR-0486 deliberately parks. No advisory redesign is needed to satisfy the present contract.

Strengths include exact preservation of the accepted core, unchanged approval rejection, real writer/check verification, independent public-boundary refusal probes, and unchanged supported control outputs rather than private-binder-only assertions.

## Requirement-to-evidence assessment

| Requirement | Independent evidence | Result |
| --- | --- | --- |
| Inconsistent receiver/default alignment refuses explicitly | Eight independently constructed sources through `derive_design_review`; unchanged baseline module loaded from its Git blob produces the strict-zip ValueError for each; candidate produces the specified reason | PASS |
| Sensitive and non-sensitive helpers; nested propagation | Single default, positional-only default and multiple-default signatures each with a subprocess sink or inert return; two nested wrappers around a sensitive helper; classmethod with a defaulted receiver | PASS |
| No exact row from refused invocation | Every refusal probe asserts an empty expanded-row list | PASS |
| Blocker prevents approval | Every refusal probe passes the freshly derived matching tokens into public `validate_design_approval` and observes rejection | PASS |
| Supported baseline binding remains supported | Independent instance-method, ordinary classmethod and class-qualified staticmethod controls return one exact row with no blockers; complete review objects equal baseline outputs | PASS |
| Both binding consumers retain typed refusal | Source tracing confirms exactly two call sites and immediate reason propagation at both; nested public fixture exercises propagation through analyzed local wrappers | PASS within the stated reachability limit |
| Ordinary registration still derives review and grants nothing | Real `--write`, `--check`, public review export and parsed generated artifacts on both interpreters | PASS |
| Retained origins/import/complete-deal boundaries | 52-test boundary suite, actual public repository gate, and independently constructed relative/aliased replay, complete-deal, river and CuPy negatives | PASS on Windows |
| Exact r007 imports and protected paths | Git-blob identities, complete changed-path inventory and baseline blob pin | PASS |
| Four additive CPU CI gates, no hard-gate demotion | Complete CI diff is four direct commands with existing downstream conditions; all four commands pass locally on both required slots | PASS for candidate configuration; hosted CI was not invoked |

The illustrative subprocess calls in probe source were analyzed as bytes and never executed.

## Deferred coverage comparison and limits

The deferred claim agrees with the independent inventory on the failure category, the two consumers, refusal-before-sensitivity requirement, zero grants, and the need to preserve supported baseline controls. I challenged the supplied examples with positional-only defaults, multiple positional defaults, a defaulted classmethod receiver, two levels of local wrapping and baseline-equal supported calls. These additional public cases pass on both slots.

A valid ordinary local function normally does not undergo receiver removal. I did not manufacture a private malformed binding object to claim public reachability of the local consumer's typed-refusal branch. Its handling is source-verified; the public nested case demonstrates forwarding from an analyzed wrapper to the registered helper and back to the top-level review. Skipped non-sensitive outer closures, star/variadic arguments, aliases, descriptor rebinding and arbitrary Python reachability remain inherited limits under the expressly narrowed contract. No universal descriptor or analyzer soundness claim follows.

The ten exact core imports received identity and suite regression checks, not a new full design audit. POSIX native mutation behavior was not executed on this Windows host. No hosted CI run, GPU/optional-dependency campaign, broad profile, source seal, rehearsal, owner invocation, integration, commit or push was performed or authorized.

## Fresh execution evidence

Final execution used the normal-Windows-identity disposable clone at `D:/Pontius/tmp/v0a-consolidation-r004-review-b/normal-snapshot`, detached at the candidate. Each Python command used `-B -P`, snapshot cwd, snapshot `/src` PYTHONPATH, scrubbed PYTHON/GIT_/PONTIUS_ variables, absolute `C:/Program Files/Git/cmd/git.exe`, and this review directory's D:-local TEMP/TMP/TMPDIR. CPython 3.11.15 ran first, then 3.14.6. No global trust configuration or dependencies were changed.

| Check | 3.11.15 | 3.14.6 |
| --- | --- | --- |
| `tests/test_v0a_hand_replay.py` | 45 tests, exit 0 | 45 tests, exit 0 |
| `tests/test_v0a_trace.py` | 53 tests, exit 0 | 53 tests, exit 0 |
| `tests/test_v0a_replay.py` | 62 tests, exit 0 | 62 tests, exit 0 |
| `tests/test_v0a_contract_faults.py` | 22 tests, exit 0 | 22 tests, exit 0 |
| `tests/test_inventory_and_profiles.py` | 88 tests, exit 0 | 88 tests, exit 0 |
| `tests/test_stabilization_boundaries.py` | 52 tests, exit 0; 1 expected skip | 52 tests, exit 0; 1 expected skip |
| `tools/check_stabilization_boundaries.py` | exit 0 | exit 0 |
| `tools/generate_test_inventory.py --write` | exit 0 | exit 0 |
| `tools/generate_test_inventory.py --check` | exit 0 | exit 0 |
| Public review export | exit 0 | exit 0 |
| Independent public probes | exit 0 | exit 0 |
| Generated-artifact audit and unchanged clone diff | exit 0 | exit 0 |

The boundary skip is `test_posix_write_rejects_staged_entry_substitution_before_replace`, explicitly a POSIX directory-descriptor mutation test. Inventory logs include expected negative CLI messages; 3.14 also emits a syntax warning for an intentional return-in-finally fixture. Their suites pass.

Both exports report 141 exact rows, **zero v0a exact rows**, and seven alignment blockers. The exact-row population digest is `d303a26e373f0b173a4283dcede5735fdae6b849fdb0cb0ffcddec9017e8012a`. This review-population digest is distinct from the profile grant digests: both `spec_capabilities_sha256` and `capability_bindings_sha256` in the profiles remain all zero. All 2,641 existing inventory entries are unchanged; 187 entries are added, 184 from the exact v0a suites. Four v0a payloads have no probes, no environment additions, temporary-only write roots and no serialization grant. Ordinary writer output leaves the candidate clone diff empty.

Logs are the `311-*.log` and `314-*.log` files beside this report; independent scripts are `identity.py`, `probes.py` and `artifact-check.py`. Public exports are `temp-311/export` and `temp-314/export`.

## Reviewer execution caveat

`execution-note.md` records excluded sandbox/ownership attempts and a process-coordination mistake during transition. A stop was attempted on two formerly listed PIDs before their owned-runner ancestry had been established; the immediately preceding PID query returned no rows, so whether it affected any process is unconfirmed. A later ancestry check associated their prior parent with the other review seat, and the coordinator was informed to check that seat's execution receipt. No sibling report/test output was read. That uncertainty concerns coordination, not candidate behavior; this report's success results come from review B's complete fresh normal-snapshot runs. No more process cleanup was performed.

No production fixes or integration authorization are issued by this review.
