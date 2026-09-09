# Codex cold review: v0a-eval-panel-ownership/r002

Verdict: CLEAN. Design: SOUND.
Findings: 0 Critical, 0 Important, 0 Minor.
Reviewer: Codex, independent cold pass, 2026-09-09.

Candidate: d8d291cc1f813ce798f2d3a990b2a8bf2297e124
Manifest: 86a583d27d71c251f89f507b4761318433218f0450be649fb768c83b3d8c6926
Base: 72954e1331c9b191d927c1c4b82f277bcd322a4c
Tree: 2b542a78b5a96963a154ed1da6408834eea3e3e8
Ref: refs/heads/review/v0a-eval-panel-ownership/r002
Tier C, FIX. This is one independent pass, not completion of the two-review gate.

No surviving material defect was established in the frozen ownership contract or its
combined sample consumers. Both the specification review and engineering review are
satisfactory within the authorized static review and supplied focused-evidence scope.
No source correction is required by this report.

## Independence and review method

The sole substantive dispatch input was the frozen handoff.md. I read the governing
brief/design and permitted authority inputs, then the complete tool and test module,
native Job, execution writer, status consumer and relevant bridge producer interfaces.
I searched the frozen tree for ownership fields, consumers and suite registration.
I used the code-verification skill; I did not execute Python, tests or project code.

Before opening deferred inputs I created:
D:/Pontius/tmp/eval-ownership-r002-review-01-inventory.md
SHA-256: 9b39a6aff7cac70fbd962c9c3a5bf9c9181ec348d701fe7de605abd41f25dd98

Only after that file existed did I open coverage.md, checks/, the pinned dispositions
and repair plan. No implementer transcript, prior review report or sibling output was
read. Disposition statements were checked against source and receipts, not adopted as
review conclusions. All source was read from Git objects, not mutable source files.

## Frozen identity and scope verification

Read-only Git rev-parse/cat-file verifies the full ref, sole parent and tree above.
The complete immediate diff contains exactly tools/v0a_eval_panel.py and
 tests/test_eval_panel_tool.py (67 additions, 6 deletions in total).
The cumulative diff from rejected 0bc19bcaad5c6660468094772216cac2dc27a651 also
contains only those two files: 486 additions and 118 deletions. This preserves the
separate sample candidate as parent while reviewing the final combined contract.

Using PowerShell/.NET raw subprocess stdout bytes, I independently hashed both blobs,
sorted complete lowercase hash/two-space/path rows with ordinal ordering, added LF
per row, and compared the result byte-for-byte to manifest.sha256. It matches exactly.

- tests/test_eval_panel_tool.py, 601 lines:
  2b7cebc8dbf18abc816d5e714f9d737db0320089f2bd809787fedc94e4427ead
- tools/v0a_eval_panel.py, 626 lines:
  4bc3bae53f78d747d69d5c4cca4cc39c7ac58d309fc4a3d4a9c453d39f3e1763

Both changed blobs are LF-only, BOM-free, <=100 columns and free of trailing whitespace.
All 22 listed packet pins match their handoff SHA-256 values. Deferred coverage matches:
5d0c4c730b7fd65f0276d63d78a845d8002442a037c363f415542db5dde9e4f5

All 34 dependencies.json blob pins match their explicitly stated original base:
f647a7989394f084875a040b20c41891168163ed
They are historical direct-dependency pins, not pins at this candidate's immediate
parent. The whole immediate/cumulative diffs verify unchanged bridge and sealed source.
The original-base src diff contains the added eval_bridge.py; that is not a change
made by this ownership repair. Runtime authority is the explicit CPython 3.14.6 ruling;
stale older-runtime prose in inherited documents does not authorize another runtime.

## Contract assessment and inventory-to-coverage comparison

Locations below refer to the candidate above. Tool locations mean tools/v0a_eval_panel.py.

1. Acquisition, containment and ownership: tool 335-353 and 403-421 initialize the
   report and empty owners before acquiring the Job inside both the cleanup try and
   SIGINT deferral. A console interrupt during successful acquisition is recorded,
   assignment to job still completes, and 406-407 stops before worker launch. The
   finally path closes that Job at 479-480. Suspended process assignment refusal still
   reaches direct kill/wait and independent pipe cleanup at 466-478. Native Job's
   assign/resume/active/terminate/close methods remain unchanged in
   tools/v0a_table_host.py:326-446; close consumes its handle before the native release.
   Coverage invariant 1 and the acquisition regression correspond to this inventory.

2. Cleanup and certification: tool 441-450 records each release outcome separately;
   452-457 observes process, Job, I/O-thread and stream state. Job.close is attempted
   last, then defer_interrupts restores the original handler at 311-313. Only afterward
   do 483-485 compute cleanup_verified from observed state and every recorded outcome.
   Under the supported CLI's normal SIGINT handler, interrupting that assignment
   unwinds with the original false certificate instead of storing a stale true value.
   Failed/interrupted cleanup cannot complete a successful report at 490-493.
   Coverage invariant 2 covers the lifetime edge my inventory required, including the
   final assignment rather than merely the final native close.

3. Bounded stream release: tool 316-332 gives one daemon closer each stream and reports
   timeout without replaying the close. Cleanup joins share a finite deadline and each
   later attempt remains independent at 459-480. Pending I/O/closure means unverified
   cleanup, not observed success. The real OS-pipe backpressure test at test lines
   569-597 uses actual pipe bytes and eventual closure; it does not replace close with
   a successful double. Coverage invariant 4 matches the blocking-lock question.

4. Observation ownership and failure: tool 349 aliases the caller's list; drain at
   373-401 inserts each new preflight row directly there before later stage mutations.
   Missing-stage annotation no longer determines ownership transfer. A budget kill,
   comparison failure or unwind after native cleanup therefore keeps already drained
   rows. Final drain runs even after earlier cleanup failures. main's handlers and
   finally at 612-620 retain that report. Coverage invariant 3 and real-worker tests
   at 461-490 cover the producer-to-report seam; the fake-supervisor tests alone would
   not establish it. Queue entries not yet drained are distinct from retained rows.

5. Publication: tool 504-514 keeps measured encodings and registers intended identity
   before staging/rename. The finally at 519-529 reconciles actual final bytes before
   binding and removing pending bytes. An interrupted or failed reconcile retains the
   intended path/hash/size and recoverable encoding; it does not claim a completed
   binding. The outer finally labels incomplete retention whenever pending data remains.
   Coverage invariant 5 includes pre-write, partial write, rename and binding boundaries.
   Tests 159-186 and 545-567 separately exercise second-write failure/retry and a real
   successful rename followed by interruption, comparing actual file bytes/identities.
   I found no loss or falsely completed publication in those paths or their consumers.

6. Combined sample consumers: role-bearing ScheduledHand/AdmittedPlan at tool 52-71
   links admission 149-170, worker schedule 271-279, event record identity 380-387,
   completion 539-553 and estimator 556-573. declared-full requires the development
   board, four development identities and royal control in their correct roles.
   Duplicate/missing/unknown completed sample rows and failed comparisons cannot satisfy
   complete_sample. Only development roles enter the four-hand estimate. Tests 72-86
   reject role movement/rebinding; tests 444-459 assert literal identities, complete
   comparisons and the estimate through the real worker/result path. The deferred
   inherited-sample paragraph covers the related contract identified independently.

7. Parent writer and status: tool main 588-620 invokes one begin_run and one finish_run,
   sets the run output directory, preserves failure and uses the same report. Worker
   282-294 emits events without owning a journal. execution.py:122-162 writes result
   bytes and their digest, appends the outcome once, and regenerates status through
   status_generation.py:28-79. RealRunOwnershipTests.run_and_read at 409-424 checks
   one added journal row, verified source and actual result-file digest for its cases.
   This is ordinary retained-run behavior; the unchanged writer does not promise an
   atomic filesystem transaction under failed storage or externally killed parents.

## Supplied focused evidence assessed, not executed by this reviewer

The valid RED candidate b6ede27a2c737f2a77344908fb3ebe8a88088f54 has the stated
immediate base as parent and changes tests only. Its tests are byte-identical to GREEN;
only the tool changes between RED and GREEN. The RED output contains exactly the
cleanup-certificate and native-acquisition assertion failures, with no unittest errors.
The journal reports 35 cases and zero skipped; pytest reports one failed suite and one
passed suite. The other 33 unittest cases pass, consistent with the recorded disposition.

GREEN receipt and journal both name d8d291cc1f813ce798f2d3a990b2a8bf2297e124.
They report CPython 3.14.6, pytest exit 0, 35 unittest cases, zero skipped, two selected
pytest suites passed and 44 deselected. The command is the existing parameterized
harness selecting eval_bridge or eval_panel_tool, with -B -P, ResourceWarning-as-error,
no cacheprovider, a scrubbed environment and PONTIUS_GIT. The supplied Ruff receipt
names the same candidate, the two changed files, CPython 3.14.6 and exit 0.

The ee98f51f5b6a4af3ef11c2f17d14f6087a1b1f1c locator diagnostic failed before
injecting the certificate fault because it assumed a single matching instruction.
It is correctly excluded as product RED. The final regression accepts all matching
STORE_SUBSCR offsets and asserts its signal schedule actually fired. Both new tests
retain real native effects and actual result/journal reads; only timing is controlled.

## Design judgment and limits

SOUND for this bounded checkpoint: one admitted schedule supplies its consumers;
observations stay in caller-owned storage; publication carries its intended identity;
and cleanup has a clear ownership lifetime ending before certificate computation.
The present changes repair the lifetime boundary without changing native ownership or
introducing a second evidence owner. I do not recommend a replacement of this slice.

This verdict does not claim exhaustive simultaneous-fault coverage, arbitrary process
termination recovery, failed-device durability, externally measured failure rates,
capacity/preflight measurement, full-pool feasibility, agreement or poker strength.
No broad suite was run or inferred from focused results. The second Tier C review,
later broad acceptance gates and per-commit authorization remain separate requirements.
No missing test alone was promoted to a product defect or blocking coverage finding.

This report and its inventory/ledger are create-only local staging artifacts. I made
no source edit, commit, push, hook invocation or network write, and did not publish.
