# v0a consolidation r004 coverage claim

Deferred FIX input: reviewers first record their own invariant and related-path
inventory from the requirements and frozen source, then open this claim.

The invariant is narrow: attempted baseline helper bindings with fewer retained
positional parameters than defaults yield a reason-bearing review blocker,
without an exact row from that invocation. The new contract replaces exact
descriptor inference; it does not broaden the known-unsound analyzer's claims.

Discovery: trace the real r007 TerminalAdmissionTests.host_case invocation into
_bind_helper_arguments and enumerate all call sites of that function. There are
two consumers in _review_body: local helpers and registered/cross-file helpers.
The registered path formerly skipped unresolved non-sensitive helpers; the local
path performs a sensitivity filter before its ordinary body analysis. The new
refusal is handled before those filters. Existing None outcomes retain baseline
semantics. A valid local function normally does not trigger receiver removal;
handling the typed result there keeps the consumer contract explicit without
claiming every local-helper flow is analyzed.

The retained public regression exercises a defaulted static helper through an
instance, with a subprocess sink and with a plain return, plus a nested local
wrapper reaching the sensitive helper. It requires no expanded capability rows,
the stated blocker, and rejection of capability approval. It uses source bytes
as analyzer input and launches none of their illustrative subprocesses. The
existing helper-registry regression retains supported classmethod behavior.

RED was recorded against unchanged r003 production bytes: sensitive cases
returned exact rows and the plain helper lacked the required blocker. This is
the newly approved contract replacing the former positive inference requirement.
After withdrawing the descriptor extension, the same three cases fail against
the baseline with the original strict-zip alignment exception. GREEN follows
the narrow typed-refusal correction. Raw logs are in
D:/Pontius/tmp/v0a-consolidation-r004-work/red-r003-311/,
red-baseline-311/, and green-binding-311/.

The real ordinary writer completed on the 3.11 floor. The public review export
reported 141 existing exact rows with unchanged capability-population digest
d303a26e373f0b173a4283dcede5735fdae6b849fdb0cb0ffcddec9017e8012a,
zero v0a rows, and seven alignment blockers on real host_case call sites. Both
profile capability digests are zero. The export is under
D:/Pontius/tmp/v0a-consolidation-r004-work/census-311-temp-child/scratch/.

Limits: existing dynamic arguments, aliasing, skipped non-sensitive closures,
descriptor rebinding, and other baseline false negatives are not repaired.
The correction does not assert whole-Python analysis completeness. The nested
case covers propagation from an analyzed wrapper, not discovery of all wrappers.
Broader and independent review results belong in separate receipts/reports.

Falsifiers: an attempted inconsistent alignment crashes, is silently skipped,
produces an exact row from that invocation, or permits approval with its blocker;
a new false exact result outside the corrected shape; inability to register the
unchanged r007 core; modified imported bytes; nonzero granted capability digests;
or a changed sealed kernel/dependency baseline. No source-seal claim follows
from the focused tests or this coverage statement.
