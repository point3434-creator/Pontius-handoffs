# Export r001: finalizer documentation corrections

Codex, 2026-09-10. Post-review addendum; outside the original 47-member freeze.
This corrects two documentation findings without changing source, plan, wrapper, helper,
input bindings, resource proposal, captures or original review bytes. It grants no authority.

## M-01: usable, fully bound approval wording

The suggested sentence and explanatory instructions at authorization-request.md:48-52
are superseded by authorization-template.txt. That file contains one physical line with
the complete absolute identity path, exact original manifest digest, this addendum's digest,
source commit and proposed worker envelope. Its final newline is not a path break.
The template is proposed wording only; authorization.md remains absent.

The original authorization request is a manifest member. Embedding its own manifest digest
inside that member would create a circular hash dependency. The corrected template is a
post-freeze authorization aid, and is hashed in the separate finalization manifest.
The long line is intentional to support exact verbatim copying; no Markdown line wrap
is inserted into any path or digest.

## M-02: identify which contention path this rehearsal exercised

The export rehearsal observed one completed caller, one caller returning 97, one stdout
pathname and one new journal row. Its loser stopped at the pre-existing-record check with
"an invocation was already started (claim.d exists)". This demonstrates serialization
after the claim exists. It did not exercise two callers reaching claim mkdir together.
Read coverage.md's claim-at-most-once row and the race receipts with this qualification.

The concurrent-acquisition evidence is inherited, and is identified separately:
../solve-run-20260910-r004/checks/race-caller-b.txt records PRECONDITIONS ok followed by
mkdir failing with File exists and the claim-refused message. The claim-creation block,
from mkdir -p "$OUT" up to START=$(now), is byte-identical in both wrappers. The block
digest and both capture digests are retained in finalization/evidence.json. This supports
the unchanged primitive; it is not a fresh concurrent-acquisition experiment for export.
The export's nine gate controls test its acceptance assertions, not scheduling at mkdir.

## Review status and limits

Claude's review remains NOT CLEAN: zero Critical, zero Important, two Minor findings.
Both findings are accepted and addressed by this addendum and the separate template.
These corrections have not received another independent review. No CLEAN verdict is issued.

The report is an independent reciprocal review, not a cold pass. The reviewer disclosed
authoring the preceding solve packets and campaign note in the same session. I accept it
as independent review evidence but do not count it as satisfying the handoff's cold-context
requirement. Only the controller can waive that requirement for this invocation.
No additional reviewer is dispatched under the one-reviewer policy.

No export is authorized by accepting findings or by the operationally-sound assessment.
The controller still decides review sufficiency, the proposed 600 s / 2048 MiB worker
envelope and the single retained invocation. Parent memory is outside that Job bound.
No retained export, commit or push has occurred in this finalization task.
