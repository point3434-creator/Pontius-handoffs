# Review 02 sealed independent invariant inventory

Scope: only the retained-file inventory correction and the controls that falsify it,
with the stated helper assertion/prose changes considered only as bounded context.
Created before reading any deferred checks, rehearsal or coverage input. Never revised.

## Exposure and input order
Initial injected context contained a Pontius memory summary with repository history,
training results, architecture results and baseline-watch governance. NONE is false.
No memory file, conversation, ledger, INDEX.md, previous review or previous inventory
was opened. The new dispatch supplied no particular finding or verdict. The first read
was review-02-scope.md, which itself supplies review-01 NOT CLEAN, its finding summaries,
author reproductions and claimed passed results. handoff.md, identity.json, candidate.json,
manifest.sha256, reviews/review-02-wrapper.diff and invoke.sh followed, in that order.
Mandatory documents expose other prior review context; this is a focused opposing review
with disclosed exposure, not an assertion of historical blindness. No abort rule was found.
Runtime discovery read pyvenv.cfg and listed installed uv Python directories; no project
source or other packet content was opened for that discovery. Sandbox initially denied
Python startup; elevated read-only version verification confirmed CPython 3.14.6.

## Invariants fixed before controls
1. The exact current wrapper and reconstructed old wrapper must match their raw-byte
   digests. The diff must describe only the retained inventory block. Confirm whole-row
   manifest byte ordering, LF framing and candidate binding. Do not open forbidden reviewer
   material merely to recreate the entire manifest; disclose that coverage limit.
2. Inventory success requires a newly created run directory and at least one enumerated
   regular file per new directory. Tracked directories must be excluded faithfully.
3. find failure, sort failure, partial output followed by failure, empty successful output,
   missing new directory and unreadable directory must all fail closed before complete
   evidence can be claimed. All output/status paths must be checked under actual inherited
   shell options, including nounset and pipefail.
4. Every intended regular file must occur exactly once in an unambiguous inventory with
   its real path, correct byte count and digest. Assess newline, leading whitespace,
   backslash and unusual path spelling; distinguish benign refusal from false completeness.
5. Directory traversal, symlink behavior, root symlinks and inaccessible subdirectories must
   match the stated regular-file scope. Assess enumeration/reading mutation assumptions
   under the documented exclusive checkout ownership rather than invent concurrent writers.
6. Here-string and command-substitution normalization must not drop or invent a successful
   file entry. Hash, byte count and write failures must mark evidence incomplete; a nonzero
   child status takes precedence, otherwise incomplete inventory yields 99.
7. Controls must select the exact frozen slice and recreate required helper/options/state.
   Both original enumeration failure and reverted no-new-directory counter must cause a
   control failure. Check each fixture and assertion independently of author receipt labels.
8. Check which requested edge cases are actually covered by retained controls and mark
   static-only conclusions clearly. No wrapper, script, shell slice, test or phase execution.
9. Stronger attribution assertion must require exact copied bytes on success and no content
   on refusal. Do not repeat attribution implementation review or the full packet review.
10. Preserve the scope's resource decision authority: arithmetic disclosure does not by itself
    authorize replacing an adopted envelope. Review prose only for the stated correction.

## Execution and publication boundaries
Only independent CPython 3.14.6 stdlib utility calculations and read-only inspection.
No source mutation, solve/export/agreement phase, wrapper/control execution, agents,
commit, push or publication. Report and inventory stay in exclusive scratch for coordinator
byte-exact copying to reviews/review-02-codex.md and checks/review-02-inventory.md.
