# Terminal plan Stage0 clarification — compatible primary causes

2026-08-30. Independent NON-COLD Stage0 reviewer ab_r005_cold_a: SOUND with this
required clarification, reproduced on actual3.11.15 and3.14.6. Primary consistency
is compatibility, not unconditional first-row equality. Source/body order is partly
outside the current trace's fields; do not invent chronology to make a stricter rule.

Default terminal primary equals first failure.code. For interrupted failures allow
an earlier terminal clock_invalid/clock_reversed before a later adapter outcome.
Also allow terminal clock_reversed with first failure clock_invalid and null timing:
an already-failed reversed witness can have no runtime start. Do not permit arbitrary
replacement nonclock causes. With no failure row preserve host-only terminal causes;
never require a fabricated row. Failure reason still cannot be erased on a failed hand.

Real opposing controls required: accepted delivery then caught source reversal then
acknowledgement (terminal reversed, row invalid); actual source fault then mailbox
exception (terminal originalclock, row delivery_ambiguous); failed reversed witness
before runtime start (rowinvalid/nulltiming); rejected input before cleanup (event_order
stays first); both source-before-settlement-error and settlement-error-before-source
with no failure rows. Review probe and both receipts are under stage0-checks with
cold-a-terminal-causes-v2.py. Its then-reject labels actually observed UNKNOWN and must
not be claimed as rejected-delivery evidence. Add separate genuine nondelivery control.

Shared exact event constructors and unconditional terminal helper otherwise SOUND.
Preserve all-outcome flag matrix, complete-accounting totals, settlement/cause mutations,
all event negative variants, private ascending pair and unsorted reveal-order positives.
The current schema can test compatible reasons, not independently reconstruct every
hidden source/body ordering. Record this limit explicitly in the frozen handoff.
