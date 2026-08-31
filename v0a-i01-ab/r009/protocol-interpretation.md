# r009 protocol interpretation

ADR-0485 refers to the existing three-round review circuit breaker; the current
controller workflow defines that breaker by residuals on one contract, not the
serial number of a packet. These rules operate consistently as an initial review
and up to two residual fix reviews of the same contract. A second residual stops
in-place fixing and requires the workflow's separate contract candidate/root-cause
reassessment. Packet numbers also cover distinct accepted A/B contracts and the
combined integration, so r009 does not itself establish nine attempts on one
contract. This is the first frozen FIX of the C helper-identity contract reviewed
at source r008. Internal pre-freeze engineering runs are retained evidence, not
cold-review verdicts or extra acceptance attempts.

No breaker waiver, source seal or experimental authority is granted. The four-path
FIX allowlist is generator, its inventory test, and the ordinarily generated
inventory/profile pair. The actual r008-to-r009 source delta must be recorded;
unchanged accepted A/B and remaining C are carried only for complete integration
and are compared as blobs. The manifest remains all17 paths relative to its exact
main parent. Separate governance wording cleanup must not enter this FIX manifest.

Pinned current workflow and CLAUDE copies govern reviewers, with their SHA-256s in
the handoff. Initial reviewer inputs exclude coverage contents and implementation
narratives. Inventory first, then hashed deferred coverage; reviewers do not read
peer reports. Both fresh CLEAN verdicts precede the enumerated finite CPU wall.
Claude is checkpoint finalizer; controller authorization still must identify the
final candidate after reviews and gates. No generic earlier permission transfers
to newer source bytes.
