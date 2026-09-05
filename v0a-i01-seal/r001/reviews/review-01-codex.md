# Independent Tier-A metadata review — v0a-i01-seal/r001

Verdict: **CLEAN**. **Specification: PASS. Engineering quality: PASS.
Design: SOUND.** Critical: **0**; Important: **0**; Minor: **0**.
Required corrections: none.

This verdict is limited to the three-file source-seal metadata surface and its
identity/claim integration with the already reviewed r004 payload. It is not a
new review of the v0a core or the parked analyzer, and it is not source-seal
activation, commit authorization, rehearsal authorization, invocation
authorization, integration, merge, or push authority.

## Bound identity

- Ref: `refs/heads/review/v0a-i01-seal/r001`
- Commit: `95d9435c79b01303a5d809e567569a0cfb1ac096`
- Parent/base: `bb959371eec17e76ab46ee6e42f1bac49c26d54a`
- Tree: `e5e31225d3f8e1fa6b73e5c81051af94bd3d1a1b`
- Manifest SHA-256:
  `d347a0589a1a27c2b37cea80f6c97815eac6bc596cc93827ccb921f081f6c79d`
- Preserved r004 source candidate:
  `fe1e2fc68675c6c92a1263450b455011b5987207`
- Preserved r004 source tree:
  `27fa787e80f504f17233c29961d9df545f8eb7dd`
- Preserved r004 source manifest SHA-256:
  `6eb5ec280b6a8051e88d7659920ef74b46ea682a06dc80f688ed951d75f3f221`
- Review date: 2026-09-04

The final manifest was independently rebuilt from the 20 changed Git blobs as
lexicographically whole-row-sorted
`<lowercase-sha256><two spaces><relative-posix-path><LF>` bytes. Its digest is
the bound manifest above. The same procedure over r004 rebuilt 17 rows and the
preserved r004 manifest above.

## Findings

No metadata defect, false identity, unsupported acceptance claim, or added
operational authority was established.

## Requirement-to-evidence assessment

| Requirement or risk | Independent evidence | Result |
| --- | --- | --- |
| The seal candidate changes exactly three files beyond r004 | Git comparison `fe1e2fc...95d9435` reports only modified `STATUS.md`, added ADR-0487, and added `docs/architecture/v0a-increment-1-source-bindings.json` | PASS |
| Preserve every r004 source byte | All 17 blob-derived manifest rows are identical; all ten `pontius.v0a` module/test paths also compare byte-exactly with r007 core candidate `ddea6efbeb55cb8b71da1ebd5a359a0c2c901cf1` | PASS |
| Preserve inherited dependency identity | `docs/architecture/dependency-baseline.toml` remains Git blob `5fe6ee47f3380b65887b528efef05b72c8e6ac0a` | PASS |
| Copy the source-binding JSON exactly | Candidate JSON SHA-256 is `4136020b369eabcd1dd7c160a7b4f9dd05d9fc587fc8276993cc807b9f9e034b`, byte-identical to both published r004 materializations and to fresh 3.11.15 and 3.14.6 materializations | PASS |
| Bind fixtures, schemas, APIs, reader, and dependency origins accurately | Independent JSON audit found no duplicate keys; recomputed both suit permutations, materialized deals, deal digests, configuration digests, and payout/pot conservation; all 31 origin byte counts and SHA-256s match the frozen tree; fresh reflection matches both API signatures | PASS |
| Record the controller's bounded CPU acceptance without upgrading it | Controller ruling, acceptance report, result receipts, review reports, and addendum authenticate at their cited hashes; both result sets contain 23 unique zero-exit commands and 19 suites totaling 526 tests with one existing Windows platform skip | PASS |
| Preserve the inherited fixture caveat | ADR-0487 and generated STATUS retain it as open, do not call it fixed, do not waive or skip its assertion, and do not relabel failed receipts | PASS |
| Keep the library/argv boundary explicit | The binding record names `ReplayHost.run` and `verify_successful_trace`; the v0a package and project metadata expose no CLI/argv surface; ADR-0487 says a future driver requires separate identity, review, exact argv, run-root constraints, and controller execution authorization | PASS |
| Add no operational authority | `Invocation-Authority` is `none`; activation is conditional on a separately authorized ceremonial commit; no owner, production attempt, journal, result, consumed-launch identity, rehearsal, or campaign is added by the three-file delta | PASS |
| Generate STATUS from the final ADR metadata | `pontius.status_generation --check` reports current and `tests/test_status_generation.py` passes 12/12 on 3.11.15 first and 3.14.6 second | PASS |
| Preserve governance byte hygiene | All three files are LF-only, BOM-free, terminal-LF-terminated, and free of trailing whitespace; `git diff --check` passes | PASS |

## Identity and claim details

The final commit has the stated sole parent and tree. Its base diff has exactly
20 files. Seventeen are the unchanged r004 rows; the added rows are:

- `docs/decisions/ADR-0487-source-seal-the-blueprint-only-v0a-hand-runtime.md`
  — SHA-256
  `66ebe50e4836dd1b3e7aa0ce5738bd07adac6202899096d217fab21f4d4bedb9`
- `docs/architecture/v0a-increment-1-source-bindings.json` — SHA-256
  `4136020b369eabcd1dd7c160a7b4f9dd05d9fc587fc8276993cc807b9f9e034b`
- `STATUS.md` — SHA-256
  `d1987460551e18eb434461cdf882adb4a282a37f628abd5f7580f7b512046988`

The five manual registration/boundary/CI files retain the stated diff count:
357 additions and 29 removals, below the 600-addition cap. ADR-0487 is 171
lines, below its 220-line expectation.

The source-binding audit independently recomputed:

- control A permutation `hcsd`, deal SHA-256
  `fe1fd7c42a3d23693e58fac58829d87d2618cfffc293e5c76cbcdfd99e2bbb17`,
  and configuration SHA-256
  `69861c84550f07d2d72ae1466f90a838a1ceaa345645376d7797a129a9a9f0bf`;
- control B permutation `hdsc`, deal SHA-256
  `897e3ffdd49aab7a4c34b008526da256eb03ff9f19dc79b968af2a473370f3e7`,
  and configuration SHA-256
  `762fb7122087739a2d9c16b5749568165919e8318e220dca5338efa0ee4125f2`.

The JSON correctly limits its own claim to materialized source bindings and
describes the 31-module list as an observed import closure, not arbitrary
future dynamic reachability. The exact r004 source tree remains the broader
inherited-source identity.

The following ADR-0487 documentary hashes were independently authenticated:

- review A:
  `d6dc616d2c5d24ce4737b01a067481c07a37d1969bf8ca027283e24594c71561`;
- review B:
  `f67b53dde991cd7867d14c5097cfadbeadd21a0885364e9d91fb60688803aad0`;
- review B count addendum:
  `c28bee942de1722348a9a159aaf98f7271e5dc26402099920f9d05cdf0aae194`;
- bounded acceptance report:
  `dfbe1a6b3db4d9480d0994744f0d7fc34ba022a3002855600a9ec6a01e91db37`;
- CPython 3.11 result receipt:
  `bfd918a728aca921806f9c050ae0f37e265f87202729177b4925224b1897f74e`;
- CPython 3.14 result receipt:
  `32e9545edb009f001a37651197424e0dc63961a590e26a6c27986815fbbcb448`.

The controller ruling itself hashes to
`91c7e574f1936462cd30e246b997b0f2248508bd4378e05fc739f40f6e3e8e9f`.
Its two bound inputs also authenticate: the acceptance report at the hash above
and the pre-ruling source-seal draft at
`3a11a1f84b68ef4679b11c335567c25e2c3f6dee2882eadf7fe1da924a4a696f`.

## Generated metadata and exactness

Fresh status checks used the final LF-only snapshot, snapshot cwd and
`PYTHONPATH`, `-B -P`, scrubbed Python/Git/Pontius environment variables,
absolute `PONTIUS_GIT=C:/Program Files/Git/cmd/git.exe`, and D:-local temporary
roots. The 3.11.15 floor completed before the 3.14.6 run. On both interpreters:

- `python -B -P -m pontius.status_generation --check` exited 0 and reported
  `STATUS.md is current`;
- `python -B -P tests/test_status_generation.py` ran 12 tests, all passing;
- the published read-only source-binding materializer exited 0, wrote no
  stderr, and emitted exactly 14,093 bytes with SHA-256
  `4136020b369eabcd1dd7c160a7b4f9dd05d9fc587fc8276993cc807b9f9e034b`.

The three long ADR lines are the required single-line status, active-next, and
blocker metadata; the JSON's one long line is the required reader signature.
STATUS contains generator-required one-row ledger and metadata lines. These
intentional parser/identity lines were not rewrapped. No unrelated line-ending,
whitespace, or format defect was found.

## Design verdict

**SOUND** for this Tier-A seal metadata. The design uses a conditional ADR for
the future ceremonial boundary, a non-executable copied binding record for the
reviewed payload, and the existing generator for the status projection. Those
three responsibilities are narrow, separately checkable, and do not turn the
binding JSON or review candidate into an authorization token. The future
operational driver, argv, budgets, population, and invocation authority remain
explicitly outside the seal.

## Execution limitations and excluded attempts

An initial scratch checkout inherited global `core.autocrlf=true`; its working
source bytes differed from the frozen LF blobs, and the binding comparison
failed as it should. That checkout was excluded. A fresh clone with
`core.autocrlf=false` materialized the exact Git bytes and supplied all reported
passing evidence. This is an environment limitation consistent with the open
line-ending hazard in ADR-0486, not a candidate defect. The first restricted
3.14 process launch was also denied by the sandbox; the complete normal-Windows-
identity rerun passed and is the only 3.14 result counted.

No dependency was installed. No guarded or broad profile, full 526-test rerun,
lifecycle, rehearsal, experiment, owner, process termination, hosted CI, GPU
work, source fix, commit, merge, or push was performed. No source-correctness
claim beyond the existing r007/r004 evidence was reopened. The frozen repository
and source worktree were not changed; review artifacts stayed under
`D:/Pontius/tmp/v0a-i01-seal-r001-review/`.

## Readiness boundary

The metadata is ready to be presented for the controller's **specific commit-
authorization request** for commit
`95d9435c79b01303a5d809e567569a0cfb1ac096` and manifest
`d347a0589a1a27c2b37cea80f6c97815eac6bc596cc93827ccb921f081f6c79d`.
This review does not grant that authorization or activate the source seal.
