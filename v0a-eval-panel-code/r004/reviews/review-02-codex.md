# Cold review 02 - Codex - v0a-eval-panel-code/r004

Verdict: NOT CLEAN. Four Important findings; no Critical findings.
Design verdict: STRAINED.
Specification: Fail. Engineering quality: Fail at the orchestration boundaries below.

Reviewer: Codex, independent cold pass 02, 2026-09-09.
Candidate: 0bc19bcaad5c6660468094772216cac2dc27a651
Manifest SHA-256: 70ca4c76bc8bdefe8ffaab72fa8de5b7d24d49697157436d78a3e1c025a370c3
Ref: refs/heads/review/v0a-eval-panel-code/r004
Base: f647a7989394f084875a040b20c41891168163ed
Tree: 45c76c9c8f2d7fbfa4b00e4e5b8b8cffc538b4fc

Every finding below binds to that candidate and manifest. Source locations are frozen
Git blob line numbers, not mutable worktree locations. BASE locations identify unchanged
consumers or governing requirements. No fix is implemented by this report.

## Important findings, ordered by impact

### I-01 - Cleanup can certify success after recording a cleanup failure

Severity: Important. Confidence: high; directly established by frozen control flow.
Locations: tools/v0a_eval_panel.py:359-388, especially 372-375 and 388.
Related native boundary: BASE tools/v0a_table_host.py:441-445 (Job.close).
Requirement: handoff review contract 1 explicitly forbids cleanup_verified true when a
cleanup failure was recorded; implementation brief criterion 3 preserves failure status.

Concrete scenario: the real worker exits, all threads finish, and all streams close.
verify observes zero job members and sets cleanup_verified=true. The following close job
attempt calls Job.close; CloseHandle fails and raises HostRefusal("cleanup_failed").
attempt records the error, but never clears cleanup_verified. The returned and retained
report therefore contains both a failed job close and cleanup_verified=true. The final
status is downgraded to failed through errors; that does not repair the false cleanup
certificate. Job.close is material because it releases the native job handle, and it
occurs after the current verification snapshot.

The same contradiction is reachable earlier: one join fails, or wait is interrupted,
then independent verification finds the worker dead and streams/threads finished.
verify ignores the recorded cleanup outcomes and can set the flag true. The existing
interrupt-at-wait test, tests/test_eval_panel_tool.py:248-260, requires the later verify
attempt to be ok but never asserts cleanup_verified=false. Its success cannot certify
this contract. The active-query fault test forces verify itself to fail and therefore
cannot detect a failed release followed by successful verification.

Required correction: compute the final cleanup certificate only after all release
attempts, including job close, and require both verified resource state and absence of
failed/interrupted cleanup outcomes. Preserve earlier causes and do not retry ambiguous
native handles. A failed release must never leave a stale true certificate.

Required verification: exercise the actual supervisor with a real worker/job and a
controlled failure at close job after successful earlier verification; retain the native
outcome independently. Also assert false for an interrupted wait or failed join followed
by independently observed process death. Check the retained report, not just call order.

Residual classification: this is a surviving cleanup contract from r003 I-01, itself the
first residual of r001 A. It is a second residual on that contract; the separate-candidate
and written-root-cause rule applies before another cleanup fix is attempted.

### I-02 - Drained preflight records remain private until after cleanup

Severity: Important. Confidence: high for the specified interrupt schedule; source proof.
Locations: tools/v0a_eval_panel.py:277-280, 309-321, 389-391, 487-495.
Related writer: BASE src/pontius/execution.py:122-141.
Requirement: brief criterion 3 and handoff review contract 1 require completed observations
to survive interruption, including when supervise unwinds without returning to main.

Concrete scenario: the actual worker has emitted production and production_warm stages;
drain has consumed them into hands. Cleanup finishes. A user interrupt arrives at line 390
while the first missing_stages list is being built, before observations.append(record).
That operation is outside every KeyboardInterrupt handler in supervise. The exception
escapes to main, which records status=interrupted and invokes the real finish_run with
its original observations list. That list contains no preflight record: the drained stage
measurements were retained only in supervise's local hands dictionary and are discarded
when its frame unwinds. For later records, the same schedule retains only a prefix.

Passing a caller-owned top-level report did not make the preflight records caller-owned.
Capacity events append directly at line 308 and do not share this particular defect.
An interrupt between cleanup attempts can additionally escape their individual handlers;
there is no outer finally publishing the local hands on that route either.

The new ownership test at tests/test_eval_panel_tool.py:344-354 substitutes a supervisor
that directly inserts observations into report before raising. It proves finish_run
preserves already-attached data; it skips the actual producer-to-report ownership gap.
The wait-interrupt test proves the caught wait path proceeds to ordinary final aggregation,
not that aggregation or an escape before it preserves the actual records.

Required correction: attach each newly discovered preflight record to caller-owned report
storage when it is created, then mutate that same object as stages arrive. Keep derived
missing-stage annotation separate from ownership so interruption cannot remove observed
measurements. Ensure supported cleanup unwinds still attempt remaining owned releases.

Required verification: use the real supervisor/event path to receive a known completed
stage, then inject an interrupt at the cleanup-to-finalization boundary before aggregation.
Run main through its real disposable result/journal writer and independently read back the
stage payload, one interrupted result, and one journal entry. An injected supervisor that
preloads report is not a falsifier for this defect.

Residual classification: this is also r003 I-01's observation-preservation contract and
belongs in the same second-residual cleanup candidate/root-cause treatment as I-01.

### I-03 - Declared-full admission discards the development/control role

Severity: Important. Confidence: high; exact plan mutation and frozen dataflow establish it.
Locations: tools/v0a_eval_panel.py:124-136, 236-239, 436-441, 481-486.
Requirement: brief criterion 2 declares four development measurements and the separate
royal control, followed by a full-H work estimate; handoff contract 2 requires admission
to bind exactly the declared board, four declared hands, and royal control.

Concrete input: start with the frozen plan-preflight.json. Set development_hands=[] and
append four objects to controls, one for each original development hand, each using the
unchanged plan board. Retain the existing royal control and every common plan field.
The five canonical (board, hand) identities are unchanged, distinct, and compatible.
validate_plan compares their unlabeled union with declared_sample and accepts the plan.
The worker now labels every observation control because labels are assigned from the
input list, while full_pool_estimate requires label=development. If all five real
measurements complete, the run returns status=completed and coverage=declared-full, but
its estimate says all four required development hands are missing. Required measurements
have been classified under the wrong role and the required work estimate is omitted.

A pure-data check over the frozen fixture independently confirmed that this mutation
preserves the complete admitted identity multiset while scheduling zero development
units. This check imports or executes no project code. The source proof is sufficient:
common validation is unchanged, and the only changed sample predicate sees the same set.
The same mechanism allows an unrelated plan board with no development_hands if its common
universe/permutation fields are updated and all five required observations are controls.

This does not resurrect the old sample=1 estimate: the new estimator correctly refuses
an incomplete development membership. The remaining defect is admission/completion
claiming a valid declared-full preflight whose categories cannot satisfy that estimator.
Canonicalizing hand order and refusing duplicates are correct and should be preserved.

Required correction: bind the declared board and the development/control partition during
admission, using canonical identities within each role. Require exactly the four declared
development identities and exactly the royal control. Keep legitimate hand ordering
canonicalization and labeled test-subset behavior. Completion must not silently certify
an unmet required preflight prerequisite.

Required verification: at admission, reject moving one or all development hands into
controls, moving the royal control into development, and changing the main board while
relocating every required identity to controls. Preserve the valid reordered-hand case.
Through the real worker path, a valid declared-full schedule must produce four complete
development records named exactly as the estimator expects and the separate control.

Residual classification: the unlabeled union still fails the declared-sample contract of
r003 I-02, itself the first residual of r001 D. This is its second residual; that contract
requires its own candidate and a written note explaining why both earlier fixes missed.

### I-04 - Rename can publish a complete artifact before its binding exists

Severity: Important. Confidence: high for the specified post-rename interrupt schedule.
Locations: tools/v0a_eval_panel.py:409-421, main:479 and 487-495.
Related writer: BASE src/pontius/execution.py:139-160.
Requirement: handoff contract 3 explicitly asks whether interruption can leave a completed
artifact unbound; the r003 I-03 correction requires completed bindings and recoverable
unwritten encodings in the single result.

Concrete scenario: staging.write_bytes succeeds for a boundary and os.replace publishes
capacity-boundary-<count>.blueprint.json. A KeyboardInterrupt arrives after the real rename
but before assignment to retained[count] (including during the digest computation).
finally sees pending nonempty, labels it "unwritten encodings remain", and main writes
its interrupted result. A final-name, complete boundary file exists, but boundary_artifacts
has no entry for it. finish_run serializes only report and does not discover or bind that
file; its journal binds result.json and runtimes.json, not arbitrary directory contents.

The original catastrophic data loss is reduced: the raw encoding remains recoverable in
boundary_base64, and earlier successful bindings survive. That is useful but does not
meet the separate completed-artifact-binding requirement, and the retention label is
factually wrong for this schedule. A write failure before rename safely leaves at most
an explicitly suffixed .partial file. Retry after fully complete retention is safe:
row.get returns {}, and the empty pending map takes the complete branch without a KeyError.

The added failure test raises before the second write. It proves earlier binding and
unwritten-byte recovery, but never crosses rename-success/bind-failure. Reading the
completed artifacts back on the success path cannot distinguish this failure window.

Required correction: make publication ownership and its immutable identity available to
the result before the publication can become visible, or reconcile a successful/ambiguous
rename in failure handling before finalizing the report. Distinguish pending publication
from completed binding and preserve recoverable bytes until completion is authoritative.
No change to the sealed execution writer is necessary to own this tool's artifacts.

Required verification: perform the actual temporary-file write and rename, then inject an
interrupt immediately after the successful native rename. Independently inspect the final
file and the real result: every final-name artifact must have its byte count/hash binding,
remaining bytes must be recoverable, and the interrupted run must remain unsuccessful.
Also retain partial-write and already-complete retry controls.

Residual classification: first residual of r003's new I-03 retention finding. It does not
independently invoke the second-residual rule, but still prevents CLEAN.

## Required design verdict and engineering guidance

STRAINED. The numerical bridge remains a narrow, coherent use of existing kernel, codec,
and singleton evaluator contracts. The orchestration's state is split across a local
hands dictionary, a caller report, a cleanup map, a separately cached boolean, and disk
publication followed by binding. Those multiple sources of truth invite exactly the
surviving cleanup, observation, and publication defects. Admission similarly validates
an identity with fewer fields than the downstream consumer uses.

Advisory shape change: use caller-owned per-observation records from first receipt;
canonical admitted sample records that include their role; final cleanup certification
computed from monotonic resource outcomes; and a publication record that spans staging,
rename, and binding. These are bounded changes within the existing tool, not a new
framework or a rewrite of the teacher/reference. The work is approximately the admission,
supervision/finalization, and retention functions plus boundary tests. Preserve native
kill-on-close ownership and one parent result/journal owner during transition.

The permitted r003 disposition reports that I-01 and I-02 already were first residuals.
With those contracts still surviving, the workflow now stops in-place fixing: each
contract gets a separate candidate and a written root-cause note before another fix.
Redesign is the default after the second residual; choosing another patch requires an
explicit written explanation in the disposition. This report authorizes neither option.

## Independent inventory compared with deferred coverage

The initial inventory was recorded and validated before opening coverage, checks, or the
prior disposition. Staged inventory SHA-256:
d5285ab327baf2b8e2d7fd54a575906d4fec5bb4ebeedaf73bd296b5990c59a8

- Inventory 1 and 5: malformed, repeated and overlapping hands are now rejected; canonical
  record names match estimator names. Exact required estimator membership is enforced.
  The coverage's unlabeled sample discovery misses role movement (I-03).
- Inventory 2-4: frozen bridge code uses the real replay/key/codec, conservative wire
  capacity, per-hand kernel settlement, raw unit-weight singleton reference, explicit CALL,
  two forced values, and exact rational lattice comparisons. No material defect found.
- Inventory 6-7: independent release attempts improve the earlier monolithic try block,
  including close job after Popen raises. Process poll is independent of the active-query
  and join injectors. Coverage does not establish a final no-failed-cleanup certificate
  or actual early record ownership (I-01/I-02).
- Inventory 8: staging names, incremental successful bindings, preserved pending bytes,
  and completed retry improve retention. Discovery/test selection does not cover successful
  rename followed by interruption before binding (I-04).
- Inventory 9-10: real finish_run and journal operations execute in disposable repositories
  in the ownership tests; actual supervisor tests retain native jobs and processes. The
  fake-supervisor ownership control proves the writer only, not worker-to-writer assembly.
- Inventory 11: only the seven declared files differ from BASE. Production and reference
  stay within steps 1-3; no full-H, export, host-agreement, or retained measurement claim
  follows from the supplied focused receipt.

Declared uncovered repeated-observation guard, stream-close failure, real-worker main,
pipe-fill stall, and run-directory failure remain explicit. I do not turn those omissions
alone into product defects. Proposed schedules above target demonstrated contract gaps;
there is no claim of exhaustive cleanup schedule or OS failure-population coverage.

## Evidence, identity, and limitations

I independently resolved the local ref and its parent/tree, recomputed the manifest from
raw candidate blobs using no-renames scope and whole-row byte sorting with LF rows, and
matched the packet row file byte-for-byte. Every one of 34 direct BASE dependency pins
matches its raw Git blob identity. All pinned workflow/ruling/dependency, deferred-input,
and receipt SHA-256 values match the handoff. This is a direct dependency inventory, not
a transitive closure. I did not read r003 reviews or another r004 reviewer's output.

Read-only commands used Git cat-file/show/rev-parse/diff-tree/ls-tree with
-c safe.directory=D:/Pontius, plus filesystem reads of authorized packet/skill inputs.
Standalone isolated Python performed stdlib hashing, raw-blob identity checks, JSON/data
inspection, hygiene checks, and create-only review-artifact staging. It never imported
or executed project code. Initial convenience interpreter discovery failed because python
was absent from PATH and the repository venv launcher was inaccessible; the bundled
interpreter subsequently completed the independent stdlib checks successfully.

The supplied focused receipt reports CPython 3.14.6, a disposable detached candidate
snapshot with its own uv-synced dev environment, env -i, -B -P, ResourceWarning as error,
absolute PONTIUS_GIT, and pytest exit 0. Its journal reports 27 unittest cases, zero skips,
source_verified=true and the exact candidate. The pytest summary is two parameterized
suites passed, 44 deselected. Frozen registration adds exactly test_eval_bridge and
test_eval_panel_tool; source counts agree with 11 bridge and 16 tool test cases.
These are implementer-supplied execution receipts independently identity-checked here,
not tests rerun by this reviewer. No broad-suite or measurement result is inferred.

The sealed reference normalization adds 990 unit binary64 weights exactly, normalizes once,
and the evaluator explicitly accumulates weighted terminal values with +=. Integer
kernel returns at this fixed two-action root, deterministic policies, and power-of-two
utility scaling support the pinned domain-specific error argument. Tests cover a real
royal tie and one nonzero development singleton plus labeled arithmetic boundary cases;
they do not establish a completed full development measurement or nonzero-tie census.

I independently reproduced 333+501=834 production lines and 198+358=556 test lines.
All seven changed raw blobs have no CR, BOM, trailing whitespace, or line over 100 columns.
The pinned hard ceiling is 3,000 whole-slice production lines. The stated 1,050-1,150
projection is the drafter's estimate, not measured future code. Current production is
below the 1,200 working figure; tests leave 44 lines against the 600 working figure and
bridge completion is expected to exceed it. This budget observation is not a blocker
under the controller's clarified ceiling.

No production/test edits, project execution, live lifecycle writes, Git mutations,
retained experiments, broad suites, integration, or ceremonial commit were performed.
The only writes are this attributed report, the prior initial inventory, and its ledger
line, staged create-only for the parent to publish unchanged.
