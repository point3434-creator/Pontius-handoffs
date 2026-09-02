# v0a-i01-freeze-tools-design/r001 disposition

Status: **NOT CLEAN — REJECTED FOR IMPLEMENTATION**.

Candidate commit: `ad8fbcc1ae5a9e3c3b61ae93d5ae5c0b3e4d289e`
Manifest SHA-256: `862d245f838f4b7459b6ce2aae19eede3b77a4861575722817db12d63af7b689`
Immutable initial handoff commit: `852c10645924aa9602f0d31c5d37806e0a9ec6df`
Review-output publication commit: `4c541dd4a61490725e7e689e4b2dc170c91a7608`
Round kind: NEW-SURFACE. Tier C. Documentation-only design review.

## Required verdicts

- `codex-a`: defect `NOT CLEAN`; design `WRONG SHAPE`; report SHA-256
  `79d9d814c24f56060b9fb672ff4da8e71702f82c644fb3ae94d186e95f0b1671`.
- `codex-b`: defect `NOT CLEAN`; design `STRAINED`; report SHA-256
  `d9f871de0b25c837520aeb4b254b09ef6c2e317012fbe935381a6187a82542a2`.

The design-verdict disagreement is preserved. Both reviewers agree that no
implementation may begin. The coordinator applies the stricter architectural
boundary from `WRONG SHAPE` while retaining the four-role decomposition that the
`STRAINED` review found salvageable.

The non-gate state-machine audit is retained at SHA-256
`ee00d34b17f463ad9b35ced5c6eb6ca84a808ddf84b34ca221cb89f01855fee3`.
The complete coordinator consolidation is retained at SHA-256
`2905924143ef610e0a4299ec879204d798c7a756991dea8f37c780db4b5191fa`.
Neither advisory artifact changes the two formal verdicts.

## Binding correction classes

The successor is a FIX round and must close all eleven classes in
`checks/consolidation.md`:

1. freeze complete per-role capability and dispatch grammars, with no network or
   main vocabulary reachable from builder-loaded code;
2. bind every executed shared and role-specific source through review,
   authorization, runtime origin, receipt, and final revalidation;
3. replace post-execution runtime discovery with a pre-execution source, import,
   native-image, namespace, and runtime-data boundary;
4. define every raw commit byte, including identity, time, parents, message, and
   final LF, without ambient Git identity or clock input;
5. remove persistent credential-store mutation from query, publish, timeout,
   rejection, cancellation, and recovery routes;
6. define canonical review-output semantics and the exact population relation
   among two reviewers, bundle reports, role attestations, receipts, manifests,
   and issuer ledger lines;
7. rehearse a real atomic mutation and lost-ack schedule over a separately
   authorized HTTPS target of the production server/transport class;
8. preserve concurrent handoff-main and packet ancestry and use a main-specific
   state algebra for predecessor/result descendants and protected conflicts;
9. close post-retirement replay so spent publication authority can never appear
   virgin again;
10. assign the complete fresh-repository adoption transition without granting
    network authority to the offline builder or local-ref authority to the
    publisher; and
11. define and transactionally classify the complete local authority tuple.

The successor also wraps the two overlength URL lines, binds calibration
provenance for every wall/output cap, adds the forced-Job residue and
main-descendant schedules, and supplies an invariant-to-public-test coverage map.

## Successor shape

Issue a new `v0a-i01-freeze-tools-design/r002` candidate. Do not patch the frozen
r001 ref, packet, findings, or ledger. Rewrite the central design, workflow
amendment, and runtime appendix; retain from the Git appendix only mechanisms
that remain valid after the role, credential, object, main-graph, and rehearsal
corrections. Regenerate the brief from those stronger invariants.

The r002 handoff must carry a structured coverage claim that maps every formal
and advisory class to the changed frozen sections and falsifying criterion. A
reviewer records its own invariant/seam inventory before reading that claim.

No authority utility, test, pinned runtime, candidate artifact, C harness,
Model, controller, analyzer, remote candidate transition, or evidence payload
may execute on r001 authority. No production source or ceremonial integration is
authorized by this disposition. The r001 review ref remains preserved; no
retirement action is taken.
