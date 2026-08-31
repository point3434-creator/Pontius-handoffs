# Indexed-storage controller v4: bounded engineering review

Reviewer: Codex authority_cost_audit. Read-only controller/embedded-wrapper
inspection and static AST/hash checks. No prototype import, oracle expectation
implementation inspection, config creation, payload dispatch or W mutation.
This reviewer authored the prototype and is not a cold-review participant.

Final controller SHA7192e46cd855d767c96a06ba81ffaa97c97604e12042fad5e06e299f10a5e44c.
Initially reviewed v3 SHA06b0ae9be2ea962b94b838171d4df3692f02f63119b65e404270b18883ee44bb.
Embedded wrapper remains byte-exact SHA
f55429bf5d3f404b5d9705957694b05c33b25b8c36b33433fcc8f166fb66ff2d.
No blocking defect remains in the bounded v4 review; executable behavior is
unverified and root retains dispatch authority.

## Pre-execution findings closed in v4

1. v3 replaced the current completion identity check with dictionary/list
   equality against ok=True, which also accepts integer1/float1.0. The floor
   replay had the same Boolean-width gap; its inherited exit==0 accepted
   False/0.0. v4 retains exact stream shape/order AND requires completion ok
   is True on both routes; floor exit must be exact int0. It additionally
   requires floor payload_started/result_ok is True. These changes satisfy the
   repository's exact Boolean/integer evidence distinction at those fields.
2. Coordinator identified an oracle spec-path mismatch before any execution.
   v3 copied indexed_spec.md; v4 copies the expected full
   indexed-storage-extension-spec-v1.md basename. File population remains13
   own payloads; no oracle/case/expectation change is made by this delta.
   This reviewer verified the controller-side correction, not oracle bodies.

The v4-from-v3 diff contains only these main() corrections. Independent AST
comparison finds the wrapper and every other declaration unchanged.

## Custody and dispatch checks

Root must supply an exact config SHA. Config binds this controller, disposition,
prototype, accounting map, both successor/extension oracles, fixed cases and
spec. The old34 pack/oracle pins remain literal; cursor16/28 and indexed16/31
populations are fixed. Every input is a regular non-reparse file beneath T,
nine payload input paths must differ, and original bytes/W watch are checked
before preparation and after the child. Accounting must identify this prototype.

Each invocation creates a fresh UUID D-local clone/detach at r010, validates
clean initial status and1761 tracked files, and copies13 own payload files
plus five floor-evidence files for dev. Manifest populations are1774/1779.
The manifest excludes itself but its independent SHA is passed and rechecked.
The isolated stdlib child uses actual slot executable, -S -B -P, scrubbed env,
snapshot/src PYTHONPATH, absolute Git and explicit seed0/1/17. Identity and
manifest verification precede prototype/oracle imports; Pontius is resolved
read-only to snapshot/src and remains unimported.

Dev requires a same-seed successful actual3.11.15 receipt with identical config,
control, all source/accounting/oracle/case/spec/disposition/W input hashes.
It rehashes the old snapshot/manifest and saved floor receipt/setup/stdout/
stderr/log. Raw control records must equal retained streams in exact order:
identity, storage, cursor, indexed, completed. Setup must match the receipt,
manifest, input hashes and config; actual floor executable/version/env/seed/
prototype/accounting identities are checked. Every phase is revalidated for
its exact case/run counts, successful completion, no failures and matching
source/accounting fitness. A summary-only assertion is insufficient.

The current child is validated against the same exact ordered stream and phase
populations; indexed accounting_complete/fitness_passed must be actual True.
No success can be issued from an incomplete/failed phase or nonzero exit.

## Failure retention and remaining limits

Output paths are create-exclusive and never reused. Once initial streams are
reserved, preflight/payload/result failures reach explicit failure receipts,
raw stdout/stderr/log, partial control records, real return codes and custody
results. Post-run checks cover every tracked/overlay byte, manifest, HEAD,
exact permitted untracked path set and all retained originals/W watch.
Git and the direct child have60-second timeouts; child timeout triggers kill.

Advisory limits, not newly observed payload failures:
- Initial stream reservation precedes try/finally. An I/O error during that
  reservation can leave partial empty files without a finished receipt; no
  payload has started then.
- The watchdog is for the direct child. Kill/reap can consume another timeout,
  and no strict60-second total-controller or process-tree bound is claimed.
- The unchanged wrapper continues its other predeclared phases after a phase
  failure and ultimately reports failure. It is not a first-phase-failure
  immediate-stop wrapper; root should preserve that distinction in dispatch.
- Current control parsing ignores non-JSON stdout lines; raw floor replay is
  stricter. Frozen oracles should emit JSON records. Unexpected chatter can
  therefore fail dev replay even if the floor control retained success.
- This review did not validate oracle assertions or prototype semantics/costs,
  and creates no evidence that any of the93 planned runs passed.

No source, config, oracle or payload was executed or changed by this review.
