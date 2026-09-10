# Codex opposing review: agreement-run-20260910-r001

**Verdict: NOT CLEAN.** One Important finding remains in the new recursive retained-file
collector. It can report complete evidence after file enumeration fails. Three Minor
findings concern the resource derivation, stale evidence descriptions, and an overstated
test assertion. The measured successful rehearsal is internally consistent: no missing
primary hand, wrong action/reason, incomplete host capture, or incomplete final inventory
was found in the independently checked retained data.

**Specification judgment: NOT CLEAN** against the wrapper's explicit incomplete-evidence
failure contract, because of I1. The concrete plan, retained export binding, full census,
runtime, source identity, resource values and observed primary/control results pass the
checks described below. **Engineering judgment: NOT CLEAN** because I1 is an unchecked
failure boundary in the changed collector. This is a bounded wrapper finding; it is not a
request to consolidate or rewrite the infrastructure or reopen adopted project source.

Review date: 2026-09-10. Exactly one opposing review was performed. No authorization,
retained invocation, publication, commit or push is granted or performed by this review.

## Candidate identity

- Packet: D:/Pontius-handoffs/v0a-eval-panel-completion/agreement-run-20260910-r001
- Source commit: `1c7067448106cfa2aca3d57be879842d72293c61`
- Source tree: `3d2fe79d2af20125e322dd4a668335e789810863`
- Manifest: `4b5e3b7aa8214ef3f2016fa5efc62f8d2bfd5f4432953b08f655af7a75e62120`,
  42 members, raw-byte digest/whole-row sort/LF/trailing-LF rules independently verified.
- Plan: `525944ae6185ec683bb09dcd15727e665d9c9b2911048bd8bec210580ff60b01`
- Wrapper: `6581341aa1c5f9d32d9fdc67aad05973a4d58e385669a9c61c42a17147626eb3`
- Attribution helper: `a20e760a7e97eb5e37432b81e0dc3e3048bd582299c7e938fc83c8d319d00b14`
- Input helper: `3e85adaed78e56657c447161c172a7d3ef3ca67c32c10691593e4e5cef023d5c`
- Execution checkout: D:/Pontius-worktrees/eval-panel-agreement-20260910
- Source-scope raw-byte manifest over 892 files:
  `bac14bea3e9a4e4c8c120556311447262d7775de54e39ef121c02bb2c59eb204`.
  Every file matches its adopted blob under the admitted CRLF normalization; HEAD is the
  adopted commit and the source-scope Git status is clean. Raw CRLF worktree bytes are not
  claimed byte-identical to LF Git blobs. The execution plan is byte-identical to its packet copy.
- The execution venv actually reports CPython 3.14.6. Independent calculations used base
  CPython 3.14.6 with `-I -B`, stdlib only.

## Findings

### I1 - Important: recursive enumeration errors can become complete evidence

**Location:** `invoke.sh:171-176`, especially line 174; success decision at lines 184-187.
Confidence: high for the control-flow defect, static analysis; the failure was not executed.

The `find "$d" -type f | LC_ALL=C sort` pipeline runs in process substitution feeding the
`while` loop. Its exit status is not the loop's or the containing subshell's status.
`set -o pipefail` affects that pipeline inside the substitution; it does not propagate its
failure across this boundary. If enumeration produces no names and fails, the zero-iteration
loop succeeds. If enumeration produces a prefix and then fails, successful hashing/writing
of that prefix also leaves the loop successful. The checked redirection/subshell at line 176
therefore need not set `EVIDENCE=incomplete`.

**Reachability in this bound invocation:** after the agreement child returns zero and its
result/journal attribution succeeds, a directory enumeration I/O/access error, or failure
to start/complete `find` or `sort`, can omit `host-inputs/` or other regular files. No changed
plan, changed poker source, concurrent journal writer, adversarial input or future phase is
needed. The final path can then append `evidence:"complete"` and return zero. This is an
uncommon filesystem/tool failure path, not an observed failure of the successful rehearsal.
The green rehearsal's actual six-file inventory was complete and independently verified.

**Requirement and consequence:** the handoff asks whether supported failures can look
successful; the wrapper promises exit 99 for incomplete retained-file evidence and says
every regular file is listed. An omitted listing under this failure can be certified complete,
while the one-shot claim remains consumed. The successful subdirectory regression in
`checks/wrapper-checks.py:133-160` tests names on the happy path; it does not test a failing
enumerator. This is a correctness gap, not merely a demand for broader coverage.

**Smallest remedy:** collect the sorted file list through an explicitly checked foreground
command/pipeline (or otherwise wait for and check the enumerator), then consume that verified
list. Preserve nonzero-child precedence, the consumed claim and exit 99 on evidence failure.
Add a bounded collector failure assertion proving that zero-name and partial-name enumeration
failures cannot leave evidence complete. No runner consolidation is required for this remedy.

### M1 - Minor: the resource rule does not derive the explicitly adopted memory value

**Location:** `inputs/resource-decision-20260910.md:57` and `:62-63`.
Confidence: high, independent arithmetic.

The stated rule is 1.9 times observed peak, rounded up to a 256 MiB boundary. The driver
result records 1,625.078125 MiB; the prose rounds that to 1,625.1. Either value produces
**3,328 MiB**, not 3,072 MiB. Even before rounding, 1.9 times 1,625.1 is 3,087.69 MiB.

**Reachability and consequence:** an operator applying the adopted derivation rule obtains a
different number from the adopted table/plan. The current plan's 3,072 MiB is explicitly
adopted and was not exceeded in the rehearsals; this finding does not establish an
unauthorized envelope or require a resource increase. It is a documentary contradiction.
**Remedy:** have the finalizer distinguish the explicitly adopted 3,072 MiB exception/value
from the general rule, or record the intended corrected rule. Do not silently change the
plan or the pinned prerequisite decision. This Minor alone does not require a new round.

### M2 - Minor: frozen narrative describes superseded identities and race evidence

**Locations:** `authorization-request.md:25`, `:53-64`; `coverage.md:29-34`;
`design-note.md:3-5` and its preparation-status passages. Confidence: high.

The request names wrapper prefix `a1e4df0c`, while the bound wrapper is `6581341a`.
It says 51 checks/28 wrapper checks; the bound receipts contain **53 checks: 23 helper,
30 wrapper**. The final green rehearsal's loser explicitly stopped at the pre-claim
existence check (`rehearsal/caller-a-console.txt:4`). Actual atomic-mkdir contention is in
the earlier RED rehearsal, where both callers printed preconditions and the loser printed
`mkdir ... File exists`; its receipt does not retain the earlier wrapper digest
(`defect.wrapper_before` is null). The frozen prose attributes that contention to the exact
final frozen wrapper without this distinction. The design note still calls the packet
unfrozen preparation and the measured report still calls its envelope a proposal.

**Reachability and consequence:** an operator/reviewer reading the request or coverage prose
can select the wrong wrapper identity or overstate exact-candidate race coverage. The
candidate, manifest, final wrapper receipt and authorization template carry the correct full
digest; the template was independently inspected. No double launch was observed, and static
inspection supports the final wrapper's atomic claim. **Remedy:** update the finalizer's
disposition/operator summary to the final identity/counts and explicitly distinguish the
green existence-check refusal from the prior RED atomic contention; label carried preparation
documents as historical. Do not claim a retained digest for the earlier wrapper that is absent.
This documentation Minor alone does not require another execution or review round.

### M3 - Minor: helper coverage claims a copied-byte assertion that the tests do not make

**Location:** `coverage.md:36-40`; `checks/helper-checks.py:77-88`.
Confidence: high from the check source.

The coverage claims assertions on copied row bytes, but `attribution()` checks the exit
code, first printed token and `target.exists()`. It never reads and compares the target
bytes, including in `bound-crlf`. A helper that creates an incorrect file and prints BOUND
would satisfy those assertions. **Reachability and consequence:** this overstates regression
coverage for the existing byte-copy contract; it does not demonstrate wrong copies by the
present helper. The present helper statically writes `raw + LF`, and this review independently
compared both actual rehearsal journal rows to the last source journal line byte-for-byte.
**Remedy:** correct the coverage statement or add an exact-byte assertion when the checks
are next adjusted. This Minor alone does not require another round.

No Critical findings. I1 is the only material unresolved finding identified here. The labels
above are this review's original findings and should be preserved in the disposition even
if the finalizer disagrees or carries a Minor.

## Independent evidence and acceptance coverage

| Area | Fresh evidence and result |
|---|---|
| Freeze and identities | All 42 manifest rows/digests and candidate pins matched. Both governing documents matched adopted Git blobs. The exact execution plan, runtime and all 892 source-scope files verified. |
| Input/prerequisite chain | Original and packet-copy bytes matched all six plan bindings. Blueprint 1,010,990 bytes; teacher 241,587 bytes; export result 194,697 bytes. Producer phase/completion/artifact bindings and capacity/preflight cleanup verified. Preflight's five stored forced-value/best-response observations satisfy the exact rational lattice bounds. No solver was rerun. |
| Universe/export | Independently enumerated 1,081 compatible hands, reproduced seeded permutation digest `344e7eeb06d72b97313f470880b8d169c4674e83bb440de827fa6fb87d97648a`, checked exact exported membership and actions for every hand, common root key fields, and source-id/teacher binding. Canonical blueprint digest recomputed as `38dc88b85d905f29b1212664aa5572179a42054d87ad5b0891219f1769971fe9`. Wire is below the 1,048,576-byte cap. |
| Bank/census | Independently translated the frozen SHA-256 counter/rejection/Fisher-Yates dealer using stdlib; all 98,304 draw records and all first-selected witnesses match all three rehearsal reports. Counts: 73,226 collisions, 23,997 unused, 1,081 witnesses, zero missing. Full twelve-card hands preserved. Seed ranges are disjoint and non-overflowing; holdout draws were never generated. |
| Sizing | Collision-free probability 0.2531812725090036, per-hand probability 0.00023421024283904124 and IID union estimate 1.0802982173046996e-7. The plan explicitly states dependence and actual-census acceptance. |
| Host raw captures | For each of three rehearsal results: 1,084 sessions, 22,225 decoded physical frames and 4,336 controlled decisions checked. Nested outcomes completed/settled/untruncated, zero child exits, ordered event indices, terminal/closure agreement, identities and four expected street decisions per session checked. Every primary river selected action matches the teacher and exported row; reasons distinguish hits/defaults. There are 545 primary raises and 536 primary checks. |
| Controls/accounting | Exactly 1,081 primaries plus labelled off-pool, CHECK-hit and changed-stack controls in the admitted order. Witnesses match scheduled/observed attempts. Proper-subset control removes exactly the first key; CHECK control contains exactly that key. Off-pool is chip-eligible/unsupported, CHECK hits, changed-stack is chip-eligible with zero hits. All scheduled/observed/missing counts reconcile. Full-pool complement is empty and explicitly disclosed. |
| Ownership/cleanup | Adopted producer, completion consumer, Session/Source admission, execution writer, status journal writer and Job cleanup paths inspected. One inherited worker context; one result and journal row; suspended worker assignment and bounded cleanup sequence confirmed statically. Both wrapper rehearsal journals have 60 rows versus 59 before, exact copied final row and correct result/runtime digests. Stored cleanup states are all ok. No new live cleanup experiment was run. |
| Wrapper changes | Required environment is checked before any claim, with correct SystemRoot/SYSTEMROOT fallback. Input guard follows a pinned-plan check and verifies every fixed input. Mode/override/authority refusals and consumed-claim behavior are sound under declared operator ownership. Attribution retains its sole-writer assumption. Recursive collector has I1. |
| Test assertions | Independently recomputed receipt pass/fail comparisons and final slice hashes: 23 helper and 30 wrapper rows, zero recorded failures. Check source has a real deliberate-mismatch gate; guard cases reject later-input failures. Tests were inspected, not rerun. M3 bounds the copied-byte claim; enumeration error injection is absent. |
| Race | Green console proves pre-claim existence refusal and one successful launch. RED console proves actual mkdir contention and one launch whose collector failed closed. The pre-claim/claim mechanics match the predecessor export wrapper on inspection. The previous RED wrapper itself lacks a bound digest; the final green evidence is not misrepresented as a final-candidate atomic-race execution. |

The green result is SHA-256
`1a9cec464ccf3c47ea89cb0a1ec55a4484c1dcec59c94e1d6e2ef53fb09c27d2`, 48,933,231 bytes.
Its worker duration is 1,141.7019331 seconds, peak Job memory 1,623.625 MiB, and wrapper
wall 1,146 seconds. All six retained files (including both `host-inputs/` files) match
the recursive actual inventory. RED result SHA-256 is
`cfd9e98fa2510ca555d989aee3e8d88f54d2203ddd03a56accced0ccc52e1f60`.
The original envelope-measurement driver result is
`2352b0cb087abe94df5c69df8b0aa215c3dbc262b4452cb3d0028df46efaa4c1`, 48,934,237 bytes,
1,194.4433609 worker seconds and 1,625.078125 MiB. These are rehearsal observations only.

## Exposure, coldness and coverage limits

**Initial context probe: NOT NONE.** Before handoff.md, injected memory summaries already
described repository training, bucket scaling, evaluator research, milestone policy and
ADR-0507 baseline-watch governance, including older throughput observations and
prepared-but-unlaunched review/authority history. No r001 author verdict or prior reviewer
findings were supplied. This was candidate-blind, not wholly history-free. No memory file
or memory index was opened or used as an evidentiary source. The handoff contains a
disclosure requirement and no abort-on-exposure rule; the coordinator confirmed proceeding
under that rule. Mandatory identity/wrapper/plan/resource documents exposed inherited
environment/digest observations, previous rehearsal claims and carried limitations before
sealing. Those were disclosed, not treated as verification.

The independent inventory was sealed **2026-09-10T17:10:53.845884Z**, before parsing or
displaying deferred checks/rehearsal/coverage/design-note/measured-report/request/next-phase
contents. Opaque deferred bytes were read solely for step-1 manifest hashing. Inventory
SHA-256: `0a33bbf821f915b62d512ed82c11edf616849482208ab0a2e6c9b67c210be872`; unchanged.
After sealing, the deferred documents necessarily exposed their historical findings and
labels. Only the predecessor export wrapper was subsequently inspected to compare changed
mechanics. No predecessor reviewer material, ledgers, progress.md, INDEX.md or conversation
history was read. Filename-only searches for missing stdout captures exposed some unrelated
snapshot filenames; no such file contents were opened.

No wrapper, supplied check script, project module, solver, export or agreement entry point
was executed or imported. No new host session, race, filesystem fault or cleanup fault was
triggered. I1 rests on static shell exit-status semantics, not an executed reproduction.
The independent dealer calculation reproduces the specified algorithm; it does not establish
statistical independence. Capture checks independently reconcile retained raw fields and
actions, but do not rerun the poker kernel, exact ranker, PreparedBlueprint API or provider
boundary. Adopted code for those connections was inspected; retained labels do not become
fresh execution evidence. The driver and wrapper rehearsals are diagnostic inputs, never a
retained agreement result or poker-strength finding.

The original standalone wrapper stdout duplicates were not located at the described snapshot
locations. The full host captures are retained inside result.json and were decoded directly.
For both wrapper runs, reconstructing the stdout bytes as result.json with its final LF
changed to Windows CRLF exactly matches the logged stdout SHA-256 and byte count. This is a
successful digest reconstruction, not a claim to have opened the original stdout files.
Parent live memory remains unmeasured; no new sample was attempted. The reported parent
reconstruction/stub diagnosis was not independently rerun. Parent memory and disk are outside
the worker Job limit; exclusive checkout/journal ownership, authorization authentication,
preservation/mirroring, and controller disposition of abandoned claims remain operator duties.

## Execution record and deliverables

Exclusive scratch:
`D:/Pontius/tmp/agreement-r001-codex-cold-20260910-c9c00207c4274b7b8dbaa18149a23e9f`.
All created files stay there; no source, packet, worktree implementation or shared scratch
was changed. The packet's requested delivery locations are outside writable roots, so the
coordinator must copy these completed report/inventory bytes exactly if publishing locally.

Independent scripts and their retained calculation results:

- `initial_checks.py` -> `initial-checks.json`: exit 0, initial byte and blob identities.
- `inspect_shapes.py`: exit 0, bounded JSON structure inspection.
- `verify_retained.py` -> `retained-verification.json`: final exit 0, full census and all
  three result/capture/accounting calculations. Its first invocation failed in review code
  because the utility expected numeric teacher-board cards; the teacher encodes card names.
  Only that utility expectation was corrected; target bytes were unchanged. This was a
  utility schema-assumption error, not a candidate failure or a retried invocation.
- `final_identity.py` -> `final-identity.json`: exit 0, all 892 source files, actual venv
  runtime, exact execution plan and stdout reconstruction.
- Read-only Git: adopted tree/blob reads, exact execution HEAD and source-scope status.

Initial sandbox launches of the venv/base Python executable were denied. Tool approval then
allowed the authorized independent CPython 3.14.6 calculations and pure runtime inspection;
no project execution was substituted. Final report, unchanged inventory and calculation
files are returned with SHA-256 hashes in the accompanying delivery checksum file.

This report preserves the original NOT CLEAN verdict and finding labels. I1 is a material
unresolved finding that merits a bounded fix/disposition under the handoff. M1-M3 are
finalizer-carryable advisories and do not independently require further rounds.
