# Cold review 02 - Codex B - v0a-i01-ab/r001

Defect verdict: CLEAN for the frozen R2-03 scope. No required correction remains.
Design verdict: SOUND within that scope.
Reviewer: independent Codex cold B, 2026-08-30. Tier C, FIX round.

Candidate: refs/heads/review/v0a-i01-ab/r001
Commit: 256bcf5b1e721c70216f4d8937166cbb9c25a7ce
Manifest SHA-256: 7a4cbf46c9eb34693d605ae43a0b9048b709d65f9c3fed40610c5c1b5ae3b384
Base: c74b80628a89938ca585ef3240b5c267a7174d0f
Tree: 9ddf33f3c1ccb7735a25a3eb3502ee50644c9bb1

## Findings and design

No Critical or Important finding was demonstrated. The required R6-01/R6-02
outcomes in the predecessor disposition pass through the real public host paths:
source failure and later dead-witness refusal remain one cause; independent
same-code body failures remain separate; genuine body clock faults survive;
hostile exception presentation and metadata do not escape the completion receipt;
and body causes precede cleanup causes. Accepted action records survive.

The design now fits the contract. One explicit context-manager class owns entry,
body transfer and exit for both operations, replacing the generator protocol
that could interact with arbitrary exception traceback metadata. Classification
uses actual type ancestry; transfer uses a constant owned exception rather than
rendering the caller's exception. The witness retains the first source occurrence
separately from the refusal identity, distinguishing an echo from an independent
equal-code cause without enum deduplication. This bounded correction addresses
the demonstrated mechanisms. No redesign recommendation remains for R2-03.

## Independence and frozen identity

Read current CLAUDE.md/workflow.md, frozen source/tests, ADR-0485 and the ADR-0484
brief, and D:/Pontius-handoffs/v0a-i01-impl/r006/disposition.md via the corrected
absolute locator. No implementer self-report/transcript or other reviewer
inventory/findings was read.

The initial invariant/path inventory was recorded before opening coverage:
checks/cold-b-initial-inventory.md, SHA-256
090b6e023571cfc949da09720a2a7c08acfd75472c182ddce7a2d163a0bf6ae8.
Then coverage.md SHA-256 independently verified as
e74a65f6ad1d33816b36bc69d7ba6936d61a078b3b6dc429e81ae901ec633b9f.
The claim matches the independently discovered source, classification,
retention, interval-owner, dispatch cleanup and receipt assembly paths. No
omitted supported member or unsound coverage conclusion was demonstrated.
Structural guards are supporting evidence, not the basis of the verdict.

Ref, parent, tree, changed paths, frozen blob digests and whole-row-byte-sorted
manifest were independently recomputed. Exactly clock.py, runtime.py, replay.py
and test_v0a_replay.py changed. A new no-hardlinks clone was detached at the
candidate with checkout conversion disabled:
D:/pontius-snapshots/cold-b-ab-r001-d28f9c462053443a8b096f18b50addc1.
The final check confirms clean Git status, unchanged HEAD and exact equality of
all four checkout files to their frozen blobs. See checks/cold-b-identity.json
and checks/cold-b-final-verification.json; the latter binds diagnostic hashes.

## Fresh executable evidence

Actual CPython 3.11.15 ran first at D:/Pontius-tools/py311/Scripts/python.exe,
then actual CPython 3.14.6 at D:/Pontius/.venv/Scripts/python.exe. Every process
asserted literal version/implementation, -B/-P flags, snapshot cwd, exact
canonical snapshot/src PYTHONPATH and absolute PONTIUS_GIT before payload imports.
PATH, PYTHONHOME, VIRTUAL_ENV and Git checkout overrides were absent. Imported
clock/runtime/replay origins were asserted inside the snapshot. Git was
C:/Program Files/Git/cmd/git.exe, checked as regular/non-reparse. No safe.directory
setting was changed.

| Fresh check | 3.11.15 | 3.14.6 |
| --- | --- | --- |
| test_v0a_hand_replay.py | 35 pass | 35 pass |
| test_v0a_trace.py | 25 pass | 25 pass |
| test_v0a_replay.py | 45 pass | 45 pass |
| test_v0a_contract_faults.py | 22 pass | 22 pass |
| Independent public-boundary schedules | 1,964 pass | 1,964 pass |

Full commands, environments and exits are in checks/cold-b-v2-focused-311.json,
checks/cold-b-v2-focused-314.json, checks/cold-b-v3-diagnostic-311.json and
checks/cold-b-v3-diagnostic-314.json. Each referenced process exited zero.
The scripts are cold-b-runner-v2.py (focused), cold-b-runner-v3.py (independent),
and cold-b-payload.py under checks/. The runners launch absolute interpreter
paths with -B -P, the identity wrapper, literal version, snapshot and target.

The 1,964 diagnostic rows per interpreter are not an exhaustive combination
claim and are not added to unittest subcase counts:

- 2 complete A/B baselines: 138/72 source reads. Settlement entry is independently
  observed through the oracle at reads 134/68.
- 1,676 complete host runs sweep all baseline read positions for invalid values,
  ordinary source exceptions, typed reversals and backwards values, with and
  without real create-new writer refusal. Backwards-value schedules exclude
  the first read because reversal requires an earlier successful sample.
- 160 entry/body schedules cover echo, caught return, later ordinary error,
  independent clock error and returned mismatch, repeated dead reads and
  optional real writer refusal. Source calls stop at the genuine failure.
- 96 settlement/publication schedules cover normal messages, hostile arguments,
  spoofed __class__, hostile attribute access/assignment, true clock subclasses,
  StopIteration, BaseException and ExceptionGroup values, without cleanup failure
  and with invalid/reversed cleanup failure. No hostile hook was invoked.
- 30 compound schedules combine a fresh ordinary/invalid/reversed body exception,
  absent or invalid/exception/reversed/backwards cleanup failure, and subsequent
  actual existing-file writer refusal. Complete sequence and equal-code
  multiplicity match independently observed faults.

Every row compares the complete receipt cause sequence, pass/fail result and
accepted action conservation. Retained DecisionRecord action/hand/index match
actual mailbox envelopes and accepted_delivery_count. Settlement/publication
faults preserve all four/two accepted deliveries. Actual existing-file refusal
leaves file bytes unchanged. Diagnostics use public source, oracle, PathLike
writer and host APIs, with no source patch, private-state mutation, fabricated
retention marker or helper replacement.

Per-schedule records:
checks/cold-b-independent-v2-311.json SHA-256
edbfd191c0c341de142878ec24044a12935f127a3ec1358945c932c48531b153;
checks/cold-b-independent-v2-314.json SHA-256
a5597b8938d80abd9c8ed16c0f78d467bbc5b81f7f4978d0d82ec1993841315d.
Diagnostic checks/cold-b-independent-v2.py SHA-256:
d8a8ef5fcf554c5385f54141c4f753d4d3723f7f561685712a55208f32370d1a.

## Harness classifications and limits

Two preliminary harness errors remain retained. cold-b-focused-311.json stopped
before payload import because Path.resolve normalized Windows directory casing
while the first runner supplied noncanonical spelling; runner v2 canonicalizes
it. The first independent diagnostic stopped after its baseline because it
iterated mailbox mapping keys as envelopes; diagnostic v2 observes mapping
values and the fixture's declared expected action count. Neither is a product
finding. Corrected receipts above are admitted evidence; no old file was edited.

The first report publication encountered a missing reviews directory. PowerShell
continued after the write error and appended the verdict with an empty report
hash. The original 177-byte ledger prefix was preserved, SHA-256
209e361aa48e5210664c34119d87e89cb27efad410a8a2804464d06d1a995d71.
This report is now issued after creating the directory. A separate metadata
correction binds its hash to the existing verdict without rewriting the first
entry or issuing another verdict. Both append receipts remain under checks/.
This bookkeeping error does not change the verified candidate or test results.

No new nesting support, fabricated/foreign markers, private mutation, exhaustive
higher-order combination claim or separate policy/value/trace-schema/publication-
accounting correction is accepted here. Permanently dead witnesses make later
source faults unreachable; schedules count actual occurrences. Unchanged event,
trace and pre-settlement surface remains outside this round's specified scope.

No production or repository test source was edited. No broad suite, installation,
GPU work, historical owner, production lifecycle, performance claim, source
commit, merge or push occurred. This is one cold R2-03 review pass, not whole-v0a
acceptance or operational/ceremonial-commit authorization.
