# Cold-A independent Tier-C review — v0a-i01-ab/r001

Reviewer: Codex cold A. Date: 2026-08-30.
Defect verdict: CLEAN for the frozen R2-03 scope.
Design verdict: SOUND.
Confidence: high for the required supported boundaries and the exercised schedules.

No Critical or Important finding survives verification. No required correction is
issued by this review. This is one independent cold pass, not source integration,
broad-suite authorization, a source seal, experiment authority, or a timing claim.

## Bound identity and scope

- Ref: refs/heads/review/v0a-i01-ab/r001
- Commit: 256bcf5b1e721c70216f4d8937166cbb9c25a7ce
- Manifest SHA-256:
  7a4cbf46c9eb34693d605ae43a0b9048b709d65f9c3fed40610c5c1b5ae3b384
- Base: c74b80628a89938ca585ef3240b5c267a7174d0f
- Tree: 9ddf33f3c1ccb7735a25a3eb3502ee50644c9bb1

The manifest was independently recomputed from git cat-file blob bytes for every
changed path, with rename detection disabled and whole row byte sorting. Its exact
bytes match manifest.sha256 and its SHA-256 matches candidate.json. The only changed
paths are clock.py, runtime.py, replay.py, and test_v0a_replay.py. The final snapshot
checkout hashes also match all four blob hashes; all four blobs are LF-only.

The review examines failure occurrence order/type/multiplicity, safe operation-error
containment, and preservation of accepted actions. It does not reopen policy
authority, value ingress, trace schema/legal verification, or the separate
publication/accounting corrections. Fabricated OperationFailed markers, foreign
owner propagation, private-state mutation, and unsupported nested intervals were
not used as acceptance gates.

## Independence and initial inventory

I read current CLAUDE.md/workflow.md, frozen ADR-0485 and the ADR-0484 brief, the
frozen source, and the required outcomes at the corrected absolute location
D:/Pontius-handoffs/v0a-i01-impl/r006/disposition.md. I did not read implementer
transcripts, self-report.md, another cold review, or another reviewer's inventory.

Before reading coverage.md, I recorded checks/cold-a-initial-inventory.md:
275d2fcb9ee8f1058310688db63ac03e3e93ef4e1667389637818ee044c96554

The deferred coverage SHA-256 independently matches:
e74a65f6ad1d33816b36bc69d7ba6936d61a078b3b6dc429e81ae901ec633b9f

The independent inventory traces source occurrence and later refusal, dispatch
wrapping/abort, both operation owners, body errors, finalization, receipt assembly,
and already delivered decisions. Coverage.md describes the same required boundary
and accurately limits its higher-order claim. Its source searches and structural
guard are supporting discovery evidence; this verdict instead relies on complete
observable cause sequences from real production host/ledger/writer paths.

## Required outcomes and fresh evidence

| Required outcome | Direct evidence | Result |
| --- | --- | --- |
| Original source fault versus dead-witness refusal | 120 source/body schedules | Pass |
| Fresh independent typed body clock failure | Body and three-cause schedules | Pass |
| Ordinary/hostile error containment | 128 operation schedules, zero hook calls | Pass |
| Body before later cleanup, writer and finalization | 24 real-writer compound schedules | Pass |
| Equal-code multiplicity, no enum deduplication | Eight three-equal-code schedules | Pass |
| Rejected-input cause before abort-clock failure | 12 actual public abort schedules | Pass |
| Accepted action/context preservation | Envelope/decision comparisons in every probe | Pass |
| Whole scope, every clean-hand source read | 1,260 single-source schedules | Pass |
| Existing behavior | Four focused suites, 127 tests per interpreter | Pass |

Each interpreter executes 1,556 independent schedules, in addition to the existing
127 tests. The independent schedules are:

- 1,260 whole-hand source schedules: both fixtures, every source observation
  (138 in A, 72 in B), six fault kinds. Every requested injection actually occurred.
  Fault kinds are boolean, negative sample, reversal, ordinary source exception,
  BaseException, and hostile typed reversal. The complete receipt cause list must
  equal the independently observed source occurrence; no membership-only check.
- 120 settlement source-identity schedules: entry versus body origin, six source
  fault kinds, then direct refusal, caught return, caught mismatch, ordinary error,
  or independent same-code body error. All 120 source faults actually occurred.
- 128 hostile operation schedules: settlement and actual writer path conversion,
  both fixtures, eight exception shapes, with no cleanup failure or one of three
  genuine cleanup fault kinds. All 96 requested cleanup source faults occurred.
  Exception shapes include hostile str/repr/class/traceback/context access,
  hostile arguments, a spoofed class, StopIteration, SystemExit, GeneratorExit,
  and a real typed clock subclass. No presentation/metadata hook was touched.
- 24 compound schedules: genuine settlement error, actual create-new writer
  refusal on an existing file, and no source failure or a source failure at one of
  five settlement/publication/finalization boundaries. All 20 requested source
  faults occurred. Every existing output file remained byte-identical.
- Four typed body-error then real writer-refusal schedules.
- 12 rejected-event schedules: early/late controlled-seat opponent inputs, both
  fixtures, three clock fault kinds at the real sealed abort boundary.
- Eight three-equal-code schedules: source failure at entry or cleanup, a separate
  oracle clock exception, and a separate writer-path clock exception. Both clock
  codes and both fixtures are covered. Three repeated dead-witness reads at each
  later body do not add a fourth occurrence; all three independent causes remain.

The whole host, runtime, witness, ledgers and writer execute unchanged. The only
inputs varied are the public source/oracle/destination/fixture seams. The abort
probe observes the current stack to select the real abort read, without replacing
the ledger. Expected causes come from invalid-input semantics and external fault
events, never from the runtime journal. Whole and compound probes compare mailbox
envelopes against full decision identity/action/context, compare completed
decisions with fault-free controls, require failed receipts where appropriate,
and verify no dead-source retry. Repeated public journal/finalization observations
do not change the sequence.

The tests establish these finite supported schedules, not exhaustive arbitrary
higher-order coverage. No failing schedule, missing required boundary, vacuous
scheduled fault, or unresolved environment gap remains in this review.

## Design assessment

SOUND: the bounded error adapter now has a shape that fits the contract. One
explicit context-manager class owns entry, body transfer, and cleanup for both
operations. Classification uses actual type ancestry without exception-defined
metadata. Only a trusted constant exception crosses to the host handler. The
witness separately retains the original fault and its later refusal by identity;
the runtime drains that occurrence once before a later cause. Independent errors
with the same code remain independent.

These changes directly address the required source/refusal distinction and unsafe
exception-transfer boundary instead of depending on a body-entry liveness guess
or on exception rendering. The frozen hand loop, sealed public ledgers and
delivery boundary remain in place. No further replacement is recommended for the
reviewed contract on the present evidence. This design verdict does not promote
the excluded foreign-marker/nested-interval cases into new requirements.

## Execution procedure and location correction

Final accepted snapshot:
D:/pontius-snapshots/v0a-i01-ab-r001-cold-a-20260830

It is a fresh D-local clone, detached at the bound commit, with no overlay and no
source changes. Actual CPython 3.11.15 completed all focused/probe runs first,
followed by actual CPython 3.14.6:

- D:/Pontius-tools/py311/Scripts/python.exe
- D:/Pontius/.venv/Scripts/python.exe

Every payload uses -B -P, snapshot cwd, exact snapshot/src PYTHONPATH, a scrubbed
environment, and absolute C:/Program Files/Git/cmd/git.exe via PONTIUS_GIT. The
driver asserts implementation/version/executable/flags/environment before imports;
the child identity probe records actual imported module paths inside the snapshot.
All commands exit zero, all focused suites have zero skips, and before/after blob
identity plus final git status and git diff --check are clean.

The earlier checks/cold-a-snapshot clone was placed inside the handoff repository.
On root's direction it was superseded by the second fresh external clone. Earlier
scripts/receipts remain unchanged but are not counted as final acceptance evidence.
checks/cold-a-location-addendum.md records this correction. The earlier disposable
clone is no longer used; root owns any verified removal. No packet file was staged.

No primary-checkout payload, broad suite, GPU, dependency installation, historical
owner, experiment, source edit, commit, merge, push or source-ref mutation occurred.

## Final accepted receipts and scripts

All paths below are relative to this round's checks/ directory. JSON receipts
contain exact argv, environment, interpreter identity, stdout/stderr, exit code,
and before/after frozen-blob verification. Data JSON files retain every schedule.

cold-a-v2-focused-31115.json
  fd3c9aa86647651c1e854a7262e2910b111ec80f62d62b9e85618f1b059ee24d
cold-a-v2-focused-3146.json
  82df4e38997f187d4e676abe881aa99068381db637bcd5f49cd1a6b18dc2a6fa
cold-a-v2-probes-v2-31115.json
  64e9a96fa43a632c12b843dcbe95a8aca8d0b2699f92bb865037f5763e6bcad0
cold-a-v2-probes-v2-3146.json
  f3639ec5b4c0ee9d778ea783aeb0338101520bd1623d072d9f6b92740b35e10d
cold-a-v2-probes-extra-v2-31115.json
  23da249b270b77458bc67621aee5539c4d1af4c7a32d4ebdc1288faaede8325d
cold-a-v2-probes-extra-v2-3146.json
  2823e177cdadebe75a81bd923f81322c3b215e869282de4e843b9680f1484c43
cold-a-probes-v2-data-31115.json
  1cc92df3091547bfc893069d224c3a59c78a29f3df588ec574ad2b1ce67c90f0
cold-a-probes-v2-data-3146.json
  f7c2a33fecd1df772059e4388a0c8a5bec78e5b9f5470ca978ea19239393c8ad
cold-a-probes-extra-v2-data-31115.json
  b3209dc2b4232938f9e69b127ed4661d045ee5319f98f4971d826f7a213e0e85
cold-a-probes-extra-v2-data-3146.json
  3cd48c4b71dfb9083d11af60a7a89a9ff996be9acc47572d660fe840cfa05be3
cold-a-driver-v2.py
  57e2ba6a01e61b6b1f706a02eab5934ab012ea3649ed502576dee934b26697a2
cold-a-probes-v2.py
  77b141b87f27d92de0949fad99c8d9b4fc26fa2d564118bd37c00ff89f507c0c
cold-a-probes-extra-v2.py
  baa340e6edeca6798cfec0f949a50a4ad02bac33f7df9664388159fe4c5f7f34
cold-a-location-addendum.md
  6a13257e9ddc2acb301d42943fc536cb7148df4523ec84b08fac3c273eec83db