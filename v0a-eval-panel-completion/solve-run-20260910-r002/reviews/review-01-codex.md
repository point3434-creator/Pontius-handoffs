# Codex follow-up review: retained solve packet r002

Verdict: **CLEAN / SOUND for the bound retained-solve use.**
Findings: **0 Critical, 0 Important, 4 Minor**. All six r001 findings are closed for
the supported invocation, with explicit residual assumptions and check limitations below.

Packet: v0a-eval-panel-completion/solve-run-20260910-r002.
Published handoffs commit: 6cae4f810e5a8d0ccde6918fea444392d64e6854.
Adopted source: 1c7067448106cfa2aca3d57be879842d72293c61.
Reviewer: Codex, 2026-09-10. This report grants no run, repair, commit or push authority.

Specification: the unchanged concrete solve plan and corrected wrapper satisfy the retained
invocation's material admission, reservation and evidence-failure requirements under the
bound checkout and trusted-producer assumptions. Engineering quality: the exclusive claim,
checked writes, capture protection and explicit journal absence are sound improvements.

## Review context and order

This is a FIX follow-up in the existing reviewer/coordinator session, **not a cold pass**.
The conversation and r001 findings were already present. I disclosed that before substantive
review and did not dispatch another agent. This is one review pass under the current request.
It must not be recorded as CONTEXT_PROBE_NONE or used to claim a cold-review gate was met.

I read r002 handoff.md, identity.json, invoke.sh and journal_attribution.py, then wrote and
hashed my invariant inventory before opening r002 checks, rehearsal receipts or the r001
disposition. Inventory SHA-256:

`86ab43478c0d730a216cb1ed6e68eac643c6a24fb6416b3e04c41771dc9afcc6`

I then inspected the check script/receipts/captures, rehearsal records, authorization request,
campaign note and r001 disposition. The r001 reports and coordinator note were already read
in the preceding review; I reconciled their findings without presenting that as independence
from history. Frozen validator, bridge, execution and governing brief/design reads followed.
Workflow memory was used for Git safe.directory and authority separation, not as code evidence.

Packet files were verified byte-for-byte against the published Git blobs. Behavioral source
inspection used the adopted Git blobs. Current checkout reads were identity/metadata checks.

## Closure of the six prior findings

1. **Exclusive reservation: closed.** invoke.sh:77-94 rejects existing records and then
   acquires claim.d with a single mkdir. Only the successful claimant can reach the start
   append and launch at 101-103. No path removes the claim. C9's captures show both callers
   completing preconditions; the loser fails at mkdir, exits 97, and never reaches capture
   redirection. The winner produces one start/end pair and one new journal row. This is
   direct race evidence in addition to the static exclusivity argument.
2. **Rehearsal/root separation: closed for the bound use.** Lines 43-55 fix retained roots
   and refuse operative overrides. Rehearsal requires an explicit root, compares its physical
   path against the retained root, and rejects an attached branch. C1/C3/C4/C5 exercise those
   refusals. The current retained checkout is attached to claude/eval-panel-solve. Detached
   does not itself prove disposable; that remains an operator responsibility. M-04 concerns
   unsupported mode values, not a path to authorize a different retained source or solve.
3. **Checked records: closed for success/failure admission.** Lines 85-94 check directory,
   claim record and start append/readability before launch. Lines 97-103 protect captures
   with noclobber. Pipefail propagates hashing failures. Lines 111-136 mark missing captures,
   failed attribution, hashes and retained-list writes incomplete; line 141 prevents success
   on that outcome. A partial end-log write also sets incomplete. Claims survive failures.
   Test coverage and nonzero exit precedence are qualified in M-02/M-03.
4. **Old-row substitution: closed under the actual journal producer.** The helper requires
   exactly one row beyond the recorded baseline before examining it, then checks commit,
   result digest and any supplied runtimes digest. Zero/extra/mismatching rows do not attach
   a row. The wrapper uses helper exit/status, not journal tail, and fails when attribution
   is incomplete. The current retained journal is 59 well-formed, LF-terminated JSON rows.
   Six fresh synthetic runs reproduced ABSENT, EXTRA, wrong-commit, wrong-digest, BOUND and
   CRLF BOUND. Attribution still depends on exclusive ownership of the journal; see M-01.
5. **Manifest ordering: closed.** All 26 member hashes match raw files and published blobs.
   The stored LF rows are sorted as whole byte rows. Hashing that exact manifest produces
   the advertised 8acaaa389fc152e4127e98fe879df758fd819961085c717dd5c2601b9d145f1a.
6. **Agreement memory claim: closed.** campaign-note.md now distinguishes the 1,560-MiB
   worker Job observation from unmeasured parent retention, acknowledges bank and H growth,
   and makes no larger-bank forecast. The chain receipt is unchanged byte-for-byte. A later
   agreement envelope remains a separate measured decision and authorization.

## Minor findings

### M-01: helper binding depends on the trusted producer and journal ownership

Location: journal_attribution.py:39-59; invoke.sh:81,113-117.

The helper checks commit and file digest but does not enforce a relative, resolved-inside-root
output path or identify a newly created run directory. `root / output` accepts an absolute
path; a copied historical row appended after the baseline could also meet its checks. Thus
the helper alone does not prove its stronger phrase "bind this attempt." Its safe use here
depends on the existing owner producing the new row and no other process editing the journal.

This is Minor for this bound invocation: the adopted finish_run constrains output beneath its
root, and the run entry creates a fresh UUID directory; the retained claim excludes duplicate
wrapper callers. No path in that producer was found to emit an old or external result as the
new run. Manually altered journals or unrelated writers are outside that ownership model.
Document that dependency; a future standalone helper should explicitly check containment and
new-run identity. This is a static domain limitation, not an executed adversarial-journal test.

### M-02: the check runner is weaker than a general failure-path gate

Location: checks/wrapper-checks.sh:18-24,52-57,66-85,89-95; r001 disposition closure table.

C7 exercises failure to create OUT because a file occupies it. It does not exercise failure
of claim.json/start-log writing after successful directory creation or post-launch evidence
writes. C6 exercises an existing claim. Those cases should not be described as executed
coverage of every recording failure; those closures currently rely on checked control flow.

The record function marks pass from exit-code equality only. Launch absence, attached-row
presence and launch count are printed in notes rather than folded into that pass predicate.
The final failure count is echoed without a failing process exit. A future regression can
therefore weaken an observable while retaining a green-looking runner result.

The present captures and static paths support the reported 14 outcomes: seven refusals, six
helper outcomes and one race. Nothing in this review invalidates that receipt. On the next
check-runner change, assert the named observables and propagate failures, and add selective
record-write failure cases. The full runner was not rerun because C9 launches a real solve.

### M-03: incomplete evidence does not always produce the documented exit 99

Location: invoke.sh:140-141; authorization-request.md:27-31; identity.json invocation wording.

The script returns a nonzero child rc before checking EVIDENCE. A child failure plus ABSENT
journal evidence therefore returns that child rc, not 99. The prose says anything short of
complete evidence exits 99. Both behaviors are fail-closed; no false success follows. State
the precedence accurately, or change it in a later wrapper revision if callers need 99 to
identify every incomplete-evidence outcome. This review does not require changing the child
exit preservation policy.

### M-04: non-0/1 rehearsal values can produce malformed invocation JSON

Location: invoke.sh:36,43,88-94.

Any value other than the string 1 selects retained mode, but REHEARSAL is interpolated as an
unquoted JSON value in claim/start records. For example REHEARSAL=yes selects retained mode
and writes `"rehearsal":yes`, which is invalid JSON; the start grep only checks a substring.
The prescribed retained invocation uses the default 0 and the rehearsals use 1, so the bound
normal paths are unaffected. Validate the flag as exactly 0/1 before any record creation,
or serialize a normalized value. Until then, retain the documented default mode and do not
inherit an arbitrary flag value. This path was inspected statically and was not launched.

## Fresh verification and limits

- All 29 original packet files (26 manifest members plus three identity wrappers) match
  published Git blobs at 6cae4f8. The helper pin is:
  a20e760a7e97eb5e37432b81e0dc3e3048bd582299c7e938fc83c8d319d00b14.
- Plan copies in r001, r002 and the execution checkout are byte-identical, 12,365 bytes,
  SHA-256 c1a6af606cc80841d61b5824913c8a1b6c896988ae4c578127c1dfc08b4f8982. The full shuffled
  1,081-hand order was independently reproduced with Python 3.14.6 standard-library code.
  All three absolute prerequisite files match their bound hashes and frozen constants.
- Source HEAD and origin adopted branch are 1c706744; tree is
  3d2fe79d2af20125e322dd4a668335e789810863. Checkout status is only `?? plans/`; .venv metadata
  identifies CPython 3.14.6. No authorization.md or invocations directory exists in r002.
- Rehearsal raw/LF stdout, attributed row, start/end hashes and 59-to-60 row counts reconcile.
  The capture records completed, cleanup verified and evidence complete. Independently
  rebuilding teacher JSON from the ordered captured rows yields 241,587 bytes, SHA-256
  c3ffab403eb7e939857cc31b0f21b255cefdffd8b0d26d078b703c1fe956b3e3. There are 545 raises,
  536 checks and zero exact action-value ties. Captured peak is 786.9140625 MiB.
- Fresh six-case helper execution used only synthetic files in
  D:/Pontius/tmp/solve-plan-r002-review-20260910/helper-fixtures under Python 3.14.6 -I -B.
  All six exits and row-presence outcomes matched. No solver/project module was imported.
  Bash -n of invoke.sh passed. Read-only ls-remote returned the expected adopted commit.
- The first independent verification utility stopped on an incorrect assumption that the
  retained artifact observation contains artifact_base64. It contains the digest and size;
  I corrected the utility to compare those against the independently rebuilt teacher.
  The corrected full utility passed. No packet/source bytes were changed to make it pass.

Verification details are retained in checks/review-01-verification.json. The deleted snapshot
and its original runtimes/teacher files were not available for inspection; reconstruction and
capture consistency are not a second poker evaluator or a fresh retained outcome. No failure
injection beyond the supplied six helper cases, new rehearsal, full test suite, retained solve,
export or agreement was executed. No source edit, commit or push was performed.

## Operator-dependent boundaries and next gate

The claim protects callers sharing this packet's claim path; it is not a global lock over all
possible scripts/checkouts. Do not delete an abandoned claim, edit the journal, launch another
writer in this checkout or treat a second authorization file as permission to reuse it. Any
interrupted/ambiguous attempt requires controller disposition while its artifacts remain.
The operator owns the authorization file's truthful content, stable source/helper/plan bytes,
ordinary command environment, and selection of a genuinely disposable rehearsal checkout.
The script does not authenticate arbitrary filesystem writers or guarantee final records
after forced termination/power loss. Absence remains absence; a surviving claim prevents retry.

Technical review recommendation: proceed to the controller's explicit one-shot authorization
decision for this r002 binding. This report is a disclosed follow-up, not the cold pass named
in the template. If that template's cold requirement is applied literally to this FIX round,
this report alone does not satisfy it. No invocation is authorized by the CLEAN verdict.
