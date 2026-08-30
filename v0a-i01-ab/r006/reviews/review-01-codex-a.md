# Review 01 - Codex A - v0a-i01-ab/r006

2026-08-30. Independent cold Tier-C pass A; FIX scope T-01/T-02.

Candidate: 52bd941e9fa1fb90ff6d2d14df2286e2ee4f4ec8
Manifest: 7e1575b18c7a9cf0c74bd956a54e899aad670349d198d7863ae1f67463583d7a
Base: 6cdf7b00dac653a9a295bbb86cdc3b5782317491
Tree: 8f5e35e5c266d8a8fa4c63e96550a4e9ef894216

## Verdicts

**Defect verdict: CLEAN. Specification result: PASS for this declared correction.**
No Critical, Important, or other required correction remains from this review.
Contradictory failed terminals and invalid event values receive TraceInvalidError;
real failure prefixes and successful replay controls remain accepted where required.

**Design verdict: SOUND for this bounded reader change. Engineering result: PASS.**
Exact wire-key admission followed by the four known pure event constructors gives
runtime ingress and trace parsing one primitive-value authority. The separate
all-outcome terminal implication pass runs after exact values, counts, and paired
records have been checked. That organization fits the contract and removes the two
identified duplication/branching causes without expanding into legal replay or host
publication ownership. The limited source-clock compatibility exception is explicit
about information the schema does not record. No redesign is required by this review.

## Independence and identity

Started with handoff.md, then only its permitted packet identity, frozen source/tests,
ADR0485 and ADR0484 brief contracts, current CLAUDE.md/workflow, and r005 T-01/T-02
required outcomes. Did not open implementation plans, self-report, transcripts,
sibling checks, or peer reviews. The independent invariant/path inventory was written
before coverage.md was opened:

- checks/codex-a-inventory.md, SHA256
  437becbd1d4f0000ec8e233a919dd339e5fc867bd3ccd65ccfd6f94e9b94d0c3.
- Deferred coverage bytes independently matched
  8316fc9dc13bac5b66142f73ffc992b537f009736bde77694eb9eec7b0a6ee46.

The frozen ref, commit parent, tree, and exactly two changed paths were independently
verified. SHA256 was computed from git cat-file blob output, not checkout contents;
complete manifest rows were sorted digest-first and compared byte-for-byte with the
packet manifest. The rows are:

```text
0aadfeb915d530048a4bf8f3b117cc922826d4731f3ebe00dc2a52fc65d7bbc8  tests/test_v0a_trace.py
df742bcf7d516d31a9e155bdd55d68fa85847d83c2c47c23942f914ad5dc1e9c  src/pontius/v0a/trace.py
```

Snapshot checkout bytes also matched those blobs. Both changed blobs are LF-only,
BOM-free and have no trailing whitespace. git diff --check passed; no added line
exceeds 100 columns. Final snapshot git status was clean.

## Required outcomes and evidence

| Inventory | Required behavior and concrete exercised scenarios | Result |
| --- | --- | --- |
| I1, I8 | Stored-blob identity; intended module resolution; exact interpreter and launch flags; unchanged source | PASS; identity assertions on both runtimes and static audit |
| I2 | Real accepted-but-interrupted, unknown-acknowledgement, and rejected delivery; all eight complete/passed/accounting tuples; only all-false admitted | PASS; independent checks plus retained suite's null-timing unknown-delivery control |
| I3 | Real late, interrupted, unknown, rejected, pre-start clock failure, and terminal-only settlement failure; attach successful settlement or erase primary reason after independently rebinding both digests | PASS; every contradictory mutation refused, original traces parse |
| I4 | Failed late/settlement traces with each null/present category-total pair; complete accounting needs both totals; incomplete accounting preserves valid independently available category values | PASS; independent checks plus five failure variants in frozen suite |
| I5 | Real source-invalid/source-reversed fault before acknowledgement, exception, or actual mailbox rejection; assert observed fault occurrence and actual accepted count | PASS; six independent compound schedules, plus frozen prefailed-witness/opposing host-body and cleanup-first controls |
| I6 | Descending/duplicate/bool/out-of-range private cards; exact event field types and start boundaries; preserve ascending pair and unsorted board reveal order | PASS; independent mutations and full frozen constructor-domain tests across all four variants |
| I7 | Real fixture A and B through ReplayHost and verify_successful_trace with explicit expected bindings; value-valid event mutations remain merely parseable | PASS; both public replay controls and focused replay regressions |

Independent mutations use a fresh json/hashlib implementation of ADR0485's semantic
field projection and prefix hashing. Neither the production semantic helper nor the
new consistency helper supplies the expected outcomes. Real ActionMailbox and
MonotonicWitness paths execute inside faulting adapter/source schedules; actual
acceptance is checked independently from claimed trace delivery status.

The deferred claim matches the independently discovered event/terminal paths. Its
72 flag cases, 471 observed-read fault schedules (138 normal plus 19 rejected-input
positions, each with three faults), and 12 retained input-primary cleanup controls
were freshly executed in the frozen trace suite on each interpreter. These counts
are bounded schedule coverage, not an exhaustive claim about future producer paths.
The claim's explicit unknown chronology and final-publication limits are appropriate.
No missing in-scope acceptance scenario was found that warrants a coverage finding.

## Execution receipts

Fresh disposable snapshot:
D:/Pontius-review-codex-a-r006-6c3f4d, cloned from D:/Pontius with --shared,
--no-checkout and --no-hardlinks, then detached at the frozen candidate with
core.autocrlf=false. No test payload ran from the primary checkout.

Actual D:/Pontius-tools/py311/Scripts/python.exe 3.11.15 ran first. Actual
D:/Pontius/.venv/Scripts/python.exe 3.14.6 ran second. Each entry point and child used
-B -P, snapshot cwd, snapshot/src PYTHONPATH, disabled user site/bytecode, an explicit
scrubbed launch environment, and absolute C:/Program Files/Git/cmd/git.exe. Git was
checked as regular/non-reparse. Module paths were asserted beneath snapshot/src.

Final reproducible entry commands use checks/codex-a-run-v3.ps1 with:

```text
-Version 3.11.15 -Python D:\Pontius-tools\py311\Scripts\python.exe -Label 311-final
-Version 3.14.6 -Python D:\Pontius\.venv\Scripts\python.exe -Label 314-final
```

The runner records exact Python argv, cwd, identity, environment and outputs. Its
receipt labels are create-only; a reproduction must use new labels.

| Checks | 3.11.15 | 3.14.6 |
| --- | --- | --- |
| Independent codex-a-checks-v3.py groups | 6 pass | 6 pass |
| tests/test_v0a_trace.py | 48 pass | 48 pass |
| tests/test_v0a_hand_replay.py | 45 pass | 45 pass |
| tests/test_v0a_replay.py | 53 pass | 53 pass |
| tests/test_v0a_contract_faults.py | 22 pass | 22 pass |
| Final runner exit | 0 | 0 |

Final receipt SHA256 values:

- checks/codex-a-311-final.json:
  e62db0c4dd9cc0cdf593e7d10c73a9989d85ca8644b57501c24477de28f93238.
- checks/codex-a-314-final.json:
  96506415c25f1e5d9b973ec221fe36c3a12d8373719c122ac48f55eaf89baf0b.
- checks/codex-a-checks-v3.py:
  dbf56806334434e681425fa093ee547a695f91685faddcd6543ac227e13fc6aa.

checks/codex-a-static-audit.json records frozen-ref/source hygiene and hashes of all
previous own scripts/receipts. Earlier files remain retained: the first runner had
a reviewer-only missing verifier-argument error and wrong fourth-suite filename;
v2 corrected those. v3 additionally saves the initial scrubbed environment before
importing pontius and uses that environment for every child. Existing package
initialization adds CUDA location variables under the 3.14 environment; final
receipts distinguish launch from post-import state, and do not inherit those
additions into test-child launches. No GPU computation or optional-package work
was run. These were check-harness corrections, not product defects or flaky tests.

## Required corrections, advice, and limits

Required corrections: none.

Optional advice only: if a future schema needs independently verifiable primary and
secondary fault chronology, add explicit ordered typed cause records at that future
boundary. The present schema cannot derive chronology hidden between a source and
adapter body. This is not a gate or permission to expand r006.

No broad suite, install, capability, lifecycle/owner execution, source edit, source
seal, evidence-repository commit, or publication acceptance was performed. The known
premature scripted-schedule/null-reason producer issue was explicitly excluded and
was not used to weaken the reader. Publication/accounting integration remains
separately owned. This verdict establishes neither authoritative work measurements
nor final host receipt success, and does not broaden the unchanged legal checker or
settlement oracle's acceptance claim. Historical implementer RED receipts were not
used as fresh independent evidence.
