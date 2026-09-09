# Admitted sample contract coverage

Invariant 1: declared-full means exactly four development hands on the declared
development board and one royal-board control, with those roles preserved. Equal
unlabeled membership is insufficient. Enumerate every role movement while holding
board/hand identities fixed, including empty development and main-board rebinding.
The new negative test moves one hand, all four hands, then every identity into controls
with a different main board. All three subcases fail against the rejected admission
and pass after the correction. Existing malformed, duplicate, colliding and nonfinite
plan cases continue to exercise the same admission entry point.

Invariant 2: the admitted schedule is the authority for execution and reconciliation.
Discovery follows parse -> admission -> supervisor serialization -> worker admission
-> stage emission -> result reconciliation -> estimator. AdmittedPlan contains an
immutable wire snapshot and tuple of role/board/hand units. Worker execution iterates
those units directly; its process boundary validates the serialized snapshot again.
Neither worker labels nor estimator requirements are rebuilt from separate raw lists.
The full phase also binds the main board explicitly when development membership is empty.

Invariant 3: successful full preflight requires each admitted unit exactly once, all
stages present, completion observed and comparison passed. The royal control is included
in this requirement. No missing, extra, duplicate or failed unit can supply an estimate.
Discovery follows actual retained records into complete_sample and both its consumers:
supervisor completion and full_pool_estimate. Existing estimator tests now supply the
complete literal full sample and challenge omitted/failed control and development rows.

Invariant 4: a valid declared-full execution produces exactly the literal identities
the estimator needs, independently of the implementation's required-set constructor.
The new integration executes the real five-hand worker through main, source admission,
native containment, result publication and journal recording in a disposable clone.
It asserts AdAs, KdKh, 8dTd and 3c4d on 2c/7d/9h/Js/Qc as development, and 2c3d on
the declared royal board as control, complete comparisons, and a four-hand estimate.
The estimator's costs use only development-role records after full reconciliation.

RED beb069455a6d3ce20f202c0b4398683548631a33: 33 cases, zero skipped, exit 1.
Exactly three assertion failures are the role-movement subcases; no unittest errors.
The real full-worker integration and all existing ownership checks pass on RED.
GREEN 72954e1331c9b191d927c1c4b82f277bcd322a4c: 33 cases, zero skipped, exit 0.
Both frozen receipts identify CPython 3.14.6 and source_verified true. Execution used
the scrubbed environment, ResourceWarning-as-error and each snapshot's locked dev venv.

This candidate depends on ownership/r001 at its exact parent 182d14e. That parent's
later cleanup-certificate review is handled in a separate ownership/r002 continuation;
this packet does not claim the combined source is ready for adoption. The sample
contract itself is the independent scope here. The final combined candidate must be
reviewed before integration. Neither candidate changes the numerical bridge.

Limits: supplied tests establish schedule and reporting correctness, not runtime cost
estimates suitable for a retained measurement, poker strength or full-pool performance.
This phase's sample is fixed; these changes do not implement design steps 4-7.
