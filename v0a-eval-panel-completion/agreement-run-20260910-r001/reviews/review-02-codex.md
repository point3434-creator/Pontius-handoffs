# Focused opposing review 02: retained-file inventory correction

Verdict: **NOT CLEAN**. One Important finding and one Minor finding. The two intended
corrections are sound on their stated paths, and their controls are not vacuous. A separate
unchecked failure path remains at the here-string redirection. This is one bounded review
of the correction round, not a second review of the plan or project implementation.

## Reviewed identity and independent evidence

Packet: `D:/Pontius-handoffs/v0a-eval-panel-completion/agreement-run-20260910-r001`.
The packet declares source commit `1c7067448106cfa2aca3d57be879842d72293c61` and tree
`3d2fe79d2af20125e322dd4a668335e789810863`; this focused pass did not re-review those source
blobs or re-derive the plan, prerequisite pins, witness bank, or rehearsals.

| Reviewed artifact | Independently computed SHA-256 |
|---|---|
| `review-02-scope.md` | `b9e753c4446ec29d5bccb33aec5ec9285bc1a39005f0a62f29e9f4f7c77aa7f0` |
| `candidate.json` | `7e09c75a4bc935362dacf25fffd66b7920d188b9af1f2e1202341a49c5022b2e` |
| `manifest.sha256` | `9fca5f309234243515e579e5b47fa17ed99598ed56c4d018db8310490c2cd881` |
| Current `invoke.sh` | `6be387b24e9c81da9e0ff1d62116907877694b6feb0e0c188d7b5c1aee1f3f6d` |
| `reviews/reviewed-invoke-6581341a.sh` | `6581341aa1c5f9d32d9fdc67aad05973a4d58e385669a9c61c42a17147626eb3` |
| `reviews/review-02-wrapper.diff` | `73746c67ccab85aafb6719f18cf6f0c8bd2dcb467d8e285f10d0fcdd92ecc22e` |
| Exact current inventory slice | `b69613f70c9bbfc8b932561d11dfc1ec6e7b62c9286f17c988300822b63a4621` |
| `checks/wrapper-checks.py` | `b9f2838e7543aa7b61ca73d9f6dc07e6b74b1f78a9bb110b2addfd9c9ac22f26` |

The current wrapper matches the candidate and wrapper receipt. The old wrapper matches its
named digest. Recomputed diff content matches the supplied diff, and all bytes before and
after the inventory block are unchanged. The exact inventory slice matches its receipt pin.
The manifest has 60 distinct paths, correctly sorted whole-row bytes, LF joins and a trailing
LF, and its raw digest matches the candidate. All 12 manifest members in the focused read
set match their pins. The other three read files are manifest exclusions or the manifest
itself. **This is not a full 60-member manifest recomputation:** the manifest now includes
prior reviewer reports, inventory and coordination material, which the read contract
forbids opening. Those files remained closed. This limitation takes precedence over any
inference that the broad handoff's manifest step permits reading forbidden reviewer material.

The independent utility recalculated every expected/actual comparison in the two receipt
JSON files: 38 wrapper rows and 23 helper rows, zero comparison failures, and consistent
`passed` labels. Those are checks of retained receipt contents, not fresh executions or
independent confirmation that the recorded runs happened.

## Findings

### R2-I1 — Important: a failed here-string redirection can still leave evidence complete

Location: `invoke.sh:189` through `invoke.sh:195`, especially line 192 followed by line 194.
Related assertion: `coverage.md:45` through `coverage.md:48`.

The `while` compound command has an input redirection but no failure check:

```bash
while IFS= read -r f; do
  h=$(sha "$f") || exit 1; n=$(wc -c < "$f") || exit 1
  printf '%s  %s  %s\n' "$h" "$n" "$f" || exit 1
done <<< "$listing"
# ... for-loop ends ...
[ "$seen" -gt 0 ] || exit 1
```

Concrete current-invocation scenario: the agreement child completes normally, attribution
and capture hashing succeed, and the new run directory contains its ordinary generated
files. `find` and `sort` successfully produce a nonempty listing, and the retained inventory
output file on D: can be opened. Bash then fails to create the here-string's input backing
descriptor or temporary file. For a listing that requires temporary storage, a full or
unwritable temporary volume is one such external resource failure; it need not prevent
writing the packet on D:. A transient descriptor-allocation failure is another class of
redirection failure. No unusual filename, operator mutation, or concurrent producer is
required.

A redirection failure prevents the loop body from running and gives that compound command
a nonzero status. The wrapper enables `nounset` and `pipefail`, not `errexit`; neither enabled
option propagates this standalone redirection failure. The surrounding `for` loop continues
or ends, and `[ "$seen" -gt 0 ]` succeeds because the directory was counted before the
redirection. That final success makes the inventory subshell return zero, so its outer
`|| EVIDENCE=incomplete` does not run. With one new directory the file is empty; with several
it can be partial. If the other evidence succeeds and the child returned zero, lines
197–206 record complete evidence and return zero.

Requirement and consequence: the inventory's own fail-closed claim in the review scope and
coverage is violated. This has the same externally visible false-completeness consequence
as the enumeration failure that this round intends to eliminate. Important is warranted
because an ordinary post-launch resource failure can be reported as success; this is not
an assertion that the resource failure has occurred or is likely in the next invocation.

Evidence strength: **static control-flow finding only**. The review did not execute Bash,
force resource exhaustion, or determine the installed Bash build's exact threshold or
temporary-storage implementation. Reachability depends on an external redirection resource
failure. The independent Python utility does not purport to reproduce this Bash behavior.

Remedy: explicitly propagate failure of the compound `while` command, for example by
checking the status after its redirection (`done <<< "$listing" || exit 1`), and have the
author verify a redirection-setup failure against the exact frozen slice. This recommendation
is limited to the inventory block and does not authorize reviewer mutation or execution.

### R2-M1 — Minor: the scoped prose correction still names an obsolete wrapper and counts

Locations: `authorization-request.md:25`, `authorization-request.md:64` through line 70;
`review-02-scope.md` under “Second question”; and `coverage.md:45` through line 47.

The authorization request still describes wrapper SHA-256 `1fec82ea...`, whereas the actual
reviewed wrapper, candidate and receipt agree on `6be387b2...`. It also says 59 total checks
and 36 wrapper cases; the retained receipts contain 23 helper plus 38 wrapper rows, or 61.
The scope says six inventory cases, four shadowing `find`; inspection of
`checks/wrapper-checks.py:160` through line 184 shows five inventory fixture executions:
normal, all directories treated as tracked, and three `find` shadows. Each produces two
assertion rows. Coverage describes four fixtures and omits the no-new-directory fixture.

Concrete scenario: the controller reads the current authorization request to assess what
would be authorized and receives a different wrapper identity and outdated coverage from
the exact candidate being reviewed. This requires no resource failure, unusual filename,
or operator mutation. The machine-readable candidate and receipt pins remain consistent,
so this is an Important finding's separate documentation companion, not a runtime bypass.

Remedy: update these passages together from the current frozen identity and actual control
fixtures. Preserve the historical review labels; this finding concerns the remaining current
text, not a revision of another reviewer's verdict. A documentation-only correction does
not itself justify another opposing review under the stated proportionality rule.

## Specification judgment and requested edge cases

The inventory requirement is clear enough to evaluate: at least one new run directory,
nonempty successful enumeration for each new directory, and checked output for every
enumerated regular file. The two changes implement their intended local predicates, but
R2-I1 prevents accepting the complete-evidence claim for all ordinary failure paths.

* **Failed or partial `find`:** command-substitution assignment status is checked before
  use. `pipefail` carries the failed pipeline component. Partial captured data are discarded.
* **Successful `find`, failed `sort`:** the assignment is nonzero even if `sort` emitted
  some output. The explicit `|| exit 1` refuses it. There is no retained sort-failure control;
  this conclusion is static.
* **Unreadable new run directory or nested directory:** when `find` reports traversal
  failure, its nonzero status refuses the inventory, including partial enumeration. This
  covers unreadability as a reported enumeration failure, rather than claiming an executed
  Windows ACL test.
* **Leading whitespace:** quoted paths and `IFS= read -r` preserve it, including whitespace
  in the filename. Each relative path starts with the fixed run prefix, so a leading dash
  in a basename is not passed as a command option. No leading-whitespace control is present.
* **Newlines:** the disposition's universal assertion that a split fragment “will not hash”
  (`disposition.md:35`–36) is too strong for arbitrary POSIX filenames. A data-only independent
  model has real run files `newrun/result.json` and `newrun/result.json\nREADME.md`, and an
  existing `README.md` at the checkout root, with the full run prefix applied. The newline
  splits the second path into two existing paths. Every fragment can hash, the ordinary
  result is listed twice, and the actual newline-named file is omitted. Trailing newlines
  also interact with command substitution's trailing-newline removal. This model is saved
  in the independent receipt. It is **not** an on-disk reproduction, and no such filename
  is established as reachable from the normal Windows agreement producer. Introducing it
  would require an unusual filesystem/name path or operator-owned content outside the
  stated normal ownership assumptions. I therefore do not grade it as another current
  invocation blocker. The prose should qualify its claim; general arbitrary-name support
  would require a lossless representation rather than line-delimited names.
* **Symbolic links:** default `find -type f` does not list interior symlink objects or
  recursively follow interior directory symlinks. This is consistent with the narrower
  claim about regular files in the run tree; it is not a complete symlink/target preservation
  claim. A root supplied with the glob's trailing slash can resolve through a root symlink.
  No normal producer path introducing a symlink was established in this bounded review.
  Operator replacement of a generated root is outside the exclusive ownership assumption.
* **`set -u`, `pipefail`, and `<<<`:** `seen` is initialized; the checked assignment sets
  `listing` before expansion; quoted here-string expansion does not word-split the listing.
  Removing the enumeration's trailing line terminator and appending the here-string's one
  newline is sound for ordinary newline-free paths. These facts do not check redirection
  setup, which is R2-I1.

No statement here treats a malicious successful-but-incomplete replacement `find`, a
concurrent file writer, or arbitrary operator mutation as normal supported execution.

## Engineering judgment: do the controls falsify the corrections?

Yes, for the two stated corrections. `checks/wrapper-checks.py:136`–146 selects the frozen
slice and supplies the same `set -u -o pipefail`, hash helper, tracked-directory state and
initial evidence state. The real recursive fixture checks the two expected basenames and
complete evidence. Assertions do not check those files' digest or size columns, so they
should not be described as a full inventory-content oracle.

Static reversion reasoning, not executed mutation testing:

| Change reverted | Fixture whose assertion fails | Why |
|---|---|---|
| Return to process substitution | `enumeration-fails` | Empty loop leaves complete evidence, violating the incomplete-evidence assertion. |
| Return to process substitution | `enumeration-partial-then-fails` | The valid emitted file is hashed; evidence remains complete and the no-partial-output assertion also fails. |
| Remove empty-enumeration guard while retaining capture | `enumeration-returns-no-names` | The here-string supplies an empty record; hashing the empty path fails. This isolated mutation still fails closed, so this fixture is not uniquely sensitive to the explicit nonempty guard. |
| Restore the old block, including process substitution | `enumeration-returns-no-names` | No iteration occurs and evidence remains complete, violating the expected assertion. |
| Remove the new-directory counter/check | `no-new-run-directory` | `TRACKED_RUNS="newrun"` makes every directory skip; the subshell succeeds, so the evidence assertion fails. |

The no-new-directory fixture models the actual “only tracked directories remain” state;
it does not physically delete the directory. Its assertion is still non-vacuous. The outer
fixture shell intentionally returns zero after printing `EVIDENCE=...`; the evidence value
is the relevant assertion. The suite's final failure count and nonzero exit make a mismatch
effective. No existing fixture tests a failing here-string redirection, a failing `sort`,
unreadable directories, symlinks, or unusual filenames. The five fixture executions produce
ten inventory assertion rows, not six fixture executions.

The strengthened helper assertion at `checks/helper-checks.py:85`–96 compares actual
target bytes with the new row plus one LF, including the explicit CRLF input fixture, and
requires the target to be absent on refusal. This closes the stated copied-byte assertion
gap for those fixtures without re-reviewing the helper implementation.

The resource arithmetic in the correction prose independently recalculates to 3,328 MiB
for `ceil(1625.1 * 1.9 / 256) * 256`; the adopted 3,072 MiB is approximately 1.890345 times
the quoted peak. Leaving the adopted envelope unchanged while disclosing the explanation
discrepancy is appropriate. This is an arithmetic/prose check, not fresh envelope validation.

## Exposure, execution limits and delivery

Initial context was **not NONE**. The harness injected a general Pontius memory summary
with repository history, training measurements, research results and baseline-watch rules.
I opened no memory file and used no historical result to decide the inventory finding.
The dispatch supplied no particular prior finding or verdict. The first document opened was
`review-02-scope.md`, which itself supplies review-01's verdict/findings, author reproduction
claims and passing-result claims. `handoff.md`, `identity.json`, `candidate.json`, the manifest,
the specified diff and current wrapper followed. Mandatory wrapper/header prose also exposes
historical review context. This is a disclosed focused opposing pass, not a claim of wholly
history-free coldness. The provided contracts specify disclosure and no applicable abort rule.

I wrote and SHA-256 sealed `review-02-inventory.md` before opening any deferred checks,
coverage or disposition material. Its original seal is
`185e6548c35ded47b8dcafce76ea232c5073702df3d8e4fb8d4d57551ce56f95`, created at
`2026-09-10T18:29:52.416733+00:00`, and it remains unchanged. No prior reviewer report,
inventory, coordination file, ledger, INDEX.md, conversation or memory file was opened.
`disposition.md` was read after sealing because this scope explicitly invites its assessment;
its descriptions of the earlier findings and coldness were consequently exposed.

No project source, wrapper, check script, shell slice, solve/export/agreement phase or
rehearsal was executed. No agents were spawned. Read-only shell inspection and independent
CPython 3.14.6 stdlib calculations were used. The sandbox initially denied launching both
the packet's venv stub and base Python, after which approved elevated execution of the base
interpreter ran only the independent utilities. Runtime discovery read the venv configuration
and listed uv interpreter directories; no different Python version was run.

The first independent receipt had a false diff comparison caused by the utility retaining
difflib control-line newlines while comparing split lines. The utility was corrected using
`lineterm=''`; `independent-results-v2.json` is authoritative and confirms the diff matches.
The original receipt remains preserved. This correction changed no packet or sealed inventory.

All deliverables are in exclusive scratch:
`D:/Pontius/tmp/review02-focused-2642096b-fcef-4a45-be87-7608f670ef53/`.
The coordinator may byte-exact copy this report to `reviews/review-02-codex.md` and the sealed
inventory to `checks/review-02-inventory.md` in the packet. Hashes are supplied in the separate
delivery receipt. The packet location is outside this agent's writable roots. No publication,
commit, push, authorization or invocation is granted or performed by this review.
