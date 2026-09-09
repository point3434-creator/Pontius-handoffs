# Increment-one preregistration preparation report

Issuer: /root, implementer/coordinator. Date: 2026-08-30.
State: prepared and independently review-clean; not an accepted mainline opening.

## Exact candidate and scope

- Ref: `refs/heads/review/v0a-increment-1-prereg-r2`
- Commit: `119411fda2376d61d9ff310bada71f25aa64de70`
- Manifest SHA-256: `da3c4ad5290a49f9d6e600b61e3190047ca6221394a4fc4ad06e40af727d799c`
- Parent: `ca0b2e41bbf5d9fc1649de20379299331de6591a`
- Tree: `c7630b5a84b4ab694c7f04469007b9ca4640d024`
- Worktree: `D:/Pontius-worktrees/codex-v0a-increment-1-preregistration`
- Branch: `codex/v0a-increment-1-preregistration`
- Proposed ceremonial title: `Preregister the blueprint-only v0a hand contract`

Only the new ADR-0485 and generated STATUS.md are in the candidate. The full
handoff is r2-handoff.md; the manifest rows are r2-manifest.txt. Identity is
derived from stored git blobs, not working-file hashes. Both refs are local,
create-only snapshots, not decision commits. Neither was pushed or rewritten.

## Contracts prepared

The ADR binds public events, immutable-blueprint outcomes, hidden-card isolation,
one authoritative outer ActionClockLedger through acknowledged mailbox delivery,
typed trace/failure/settlement schemas, interrupted timing, exact replay projection,
source/dependency boundaries, future controls, and the brief's ten acceptance criteria.
It permits no resolver, GPU, h32, new producer, trained policy, or experiment owner.

A prospective lane-specific clarification requires controller adoption: freeze
the source contract first, build and source-seal, rehearse separately, then bind
measured operating budgets and population in an append-only closure before asking
for one-shot authority. ADR-0482 otherwise asks for measurements before the source
needed to produce them exists. No number was invented to satisfy that dependency.
The inherited 15-second wall and 14-second work cutoff are not relaxed. The proposed
eight lifecycles/six weeks remain nonbinding until measured closure.

## Independent reviews and fix round

Reviewers received only the frozen ref/manifest pair, brief, checklist, and governing
source documents. They did not receive the implementer conversation, design agents'
reasoning, or one another's findings. The same independent reviewers assessed r2;
neither authored either candidate. Each wrote its own findings file and serialized
one-line progress.md verdict entry.

| Round | Reviewer A | Reviewer B | Outcome |
| --- | --- | --- | --- |
| r1 / 073f0c5b | NOT CLEAN | NOT CLEAN | Clock-failure representation; replay run-ID projection |
| r2 / 119411fd | CLEAN | CLEAN | No surviving material specification finding |

Reports: r1-review-a.md, r1-review-b.md, r2-review-a.md, r2-review-b.md.
The r1-counterexamples.md file records deterministic specification counterexamples
before the edit. They are not executable runtime RED; the runtime does not exist.
R2 adds explicit interrupted timing and incomplete accounting without inventing a
delivery timestamp, and an exhaustive semantic projection independent of run IDs.
Production-path controls are required for later implementation, not claimed run now.

## Fresh local verification

Focused r1 and r2 receipts are retained. After both r2 CLEAN verdicts, verification
was repeated in separate fresh disposable snapshots with actual child interpreter
identity assertions, clean detached HEAD, no object alternates, absolute Git,
scrubbed environments, snapshot PYTHONPATH, and `python -B -P`.

| Interpreter | STATUS check | Status suite | Selected documentation checks | Snapshot |
| --- | --- | --- | --- | --- |
| CPython 3.11.15 / NumPy 2.4.6 | exit 0 | 12 pass | 4 pass | clean |
| CPython 3.14.6 / NumPy 2.5.2 | exit 0 | 12 pass | 4 pass | clean |

Final receipts: r2-acceptance-py311-verification.json and
r2-acceptance-py314-verification.json. Each records exact argv, executable, full
version, snapshot path, exits, and logs. The documentation selectors check maintained
links, front-door visibility, the fifteen-second contract, and preparation/clock
successor visibility. `git diff --check BASE CANDIDATE` passed.

These scoped documentation checks do not establish runtime correctness or broad-suite
acceptance. No broad scientific profile was invoked. The complete documentation suite
also contains historical retained-artifact tests outside this two-document change;
they were not presented as run. No tests ran from the primary checkout.

## Remaining gates

1. CodeRabbit has not reviewed this candidate. The native 0.7.5 executable at
   `C:/Users/point/AppData/Local/Programs/coderabbit/coderabbit.exe` is authenticated.
   An earlier absence report was superseded by that fresh successful check; WSL is
   not needed by this native executable. The actual review launch was rejected by
   the approval system before execution because it would transmit private repository
   content and instructions to the external CodeRabbit service. No review process
   launched, no review output was produced, and no workaround was attempted.
2. Controller adoption of the explicit bootstrap-sequencing clarification is pending.
3. Specific ceremonial-commit/push authorization remains pending under CLAUDE.md rule 4
   and docs/workflow.md Stage 5. No branch integration, decision commit, or push occurred.

The prepared external-review argv is in run_coderabbit_r2.py. It targets the clean
detached r2 snapshot, uses `review --agent --committed --base-commit BASE`, and sends
CLAUDE.md, docs/workflow.md, and the revised brief as review instructions. The service
may read relevant repository context beyond the two-file diff. Explicit permission
for that private-repository transfer is required before retrying the blocked action.

Primary HEAD remains ca0b2e41bbf5d9fc1649de20379299331de6591a. Its pre-existing
`.tmp.driveupload/` remains untouched. No runtime, source seal, lifecycle identity,
rehearsal, owner invocation, retained evidence, guarded capability, or CI gate changed.
