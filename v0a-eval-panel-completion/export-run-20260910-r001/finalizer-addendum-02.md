# Export r001: documentation corrections after cold review 02

Codex, 2026-09-10. This is the current documentation correction set, outside the original
47-member freeze. It supersedes finalizer-addendum.md's pending-cold-review status and the
earlier suggested authorization text. All earlier records remain unchanged history.
This addendum changes no source, wrapper, helper, plan, input, envelope or captured outcome.

## Review and readiness

Review 02 returned CLEAN, with SOUND specification, engineering and design judgments,
zero Critical, zero Important, four Minor findings and one Advisory. Its exact report and
sealed inventory are retained as reviews/review-02-claude.md and checks/review-02-inventory.md.
It reports CONTEXT_PROBE_NONE, no prohibited content read, no project module imports and
no predecessor review/disposition reads. Filename listings exposed no verdict content.
The finalizer verified the delivered report/inventory hashes and accepts this as the fresh
cold pass. Coldness is assessed from the delivered report and commissioning result; the
finalizer did not independently observe or replay that external session's initial context.

Review 01 remains NOT CLEAN with two Minors and disclosed non-cold context. The later
CLEAN verdict applies to the same reviewed manifest; it does not rewrite the earlier one.
Finalizer readiness is CLEAN / SOUND for the bound retained export, with the accepted
documentation corrections and limits below. The proposed invocation still requires the
controller's separate one-shot authorization and 600 s / 2048 MiB worker envelope decision.

## Approval wording (review 01 M-01)

Use authorization-template-02.txt, which supersedes authorization-template.txt and the
suggestion at authorization-request.md:48-52. It is one physical line with the complete
absolute identity path, source commit, original manifest digest, this addendum's digest
and proposed envelope. It is suggested wording only; authorization.md remains absent.
The template stays outside the reviewed manifest to avoid a self-referential digest.

## Race coverage (review 02 M1; review 01 M-02)

The export rehearsal's loser stopped at the pre-existing-record check: "an invocation was
already started (claim.d exists)". Its 0/97 pair, single capture and single new journal row
demonstrate serialization once the claim exists. They do not observe two callers passing
preconditions together and contending at atomic mkdir. The nine race-gate controls test
the assertions used to accept outcomes; they do not force the mkdir scheduling window.

The concurrent-acquisition evidence is inherited from solve r004: its race-caller-b.txt
records PRECONDITIONS ok followed by mkdir/File exists and the claim-refused message.
The exact claim-creation block is unchanged; its digest and both capture hashes are in
finalization/evidence.json. This is separately identified predecessor evidence, not a
fresh export acquisition-race receipt. No extra race or project phase was run here.

## Full pool has no off-pool complement (review 02 M2)

For declared-full on this board, H is the entire 1,081-hand compatible universe. Its
complement within that universe is empty, so brief criterion 4's complement clause holds
vacuously. All membership rows are in-pool hits; unsupported=0 does not mean an off-pool
default control passed. Criterion 8's off-pool default control is deferred to agreement's
test-only proper-subset artifact and must distinguish a default from an in-pool CHECK hit
using the retained reason. Nothing here establishes real-host agreement or strategy quality.

## Exact RED bytes now available (review 02 M3)

Accepted: the reviewed packet did not retain the whole RED wrapper. It is now reconstructed
at finalization-02/reconstructed-red-invoke.sh. Removing BOTH the four producer path/digest
constants and the producer guard block from the frozen wrapper reproduces SHA-256
8edd61520f838de99afde315a19065e3e1c5e0d08c63fa9975673af97a3a43b6, exactly the original
RED receipt's source_sha256. Removing only the guard would leave the constants and would
not reproduce it. The complete diff is retained alongside the reconstructed bytes.

This reconstruction was made after review and was not present for the reviewer. Its bytes
are identified by the original executed receipt digest; no new RED execution is claimed.
The reconstructed file is evidence material only and must not be used as the launch wrapper.

## Helper coverage limits (review 02 M4)

Accepted and explicitly documented: the six synthetic cases did not exercise the refusal
branches for an unparsable new row, absent/non-string/empty output, a missing output file,
or missing/mismatched sibling runtimes bytes when runtimes_sha256 is present. In particular,
none of those synthetic rows carried runtimes_sha256. The real rehearsal exercised the
passing runtimes binding, not its refusal. No additional synthetic tests were run here.
The unchanged refusal branches were statically reviewed as conservative failures; this
statement is not a claim of executable coverage. Exclusive adopted-producer ownership
remains an assumption, and arbitrary hostile journals are outside the helper contract.

## Required launch environment (review 02 A1)

Before authorizing/launching, the operator must ensure that SystemRoot is nonempty or
SYSTEMROOT supplies a nonempty fallback, and that TEMP and TMP are set to usable writable
temporary directories. Use the same Windows/Git-Bash and locked Python 3.14.6 setup as
rehearsed. Do not remove those variables when starting Bash --noprofile --norc.
Keep REHEARSAL unset and EXPORT_ROOT/REHEARSAL_PK unset for the retained invocation.

The frozen wrapper expands those environment variables after taking its claim. Missing
variables under set -u can therefore leave a consumed claim and start record without a
child or end record. The operator must preserve and escalate that outcome, never retry
it as if no attempt occurred. Listing the prerequisite does not add a runtime guard or
change the wrapper. Parent memory is unmeasured and remains outside the worker Job bound.

## Authority and preservation

Review completion and this disposition authorize no invocation, commit or push. Once the
controller authorizes the exact bound attempt and envelope, record that decision verbatim
before creating any claim. Source scope, frozen inputs, exclusive journal ownership,
retention/mirroring duties and the prohibition on substituting rehearsal outputs remain.
Agreement must bind the future retained export outputs, and needs its own plan and approval.
