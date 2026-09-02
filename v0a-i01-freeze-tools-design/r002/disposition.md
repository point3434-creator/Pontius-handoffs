# v0a-i01-freeze-tools-design/r002 disposition

Status: **NOT CLEAN — REJECTED FOR IMPLEMENTATION**.

Candidate commit: `48e590327c0a4bfd7ea5019e6770e1d582182b08`
Manifest SHA-256: `010e96031f60afd8badc07ebb4dd97ab8db4102527be0eb42ee56c2d65e7c984`
Immutable initial handoff commit: `14c1f5629024973b96f71c64a04f17ce9d7e01e2`
Review-output publication commit: `de0b9de1beb053e2ec2e51561fbac0126747ace6`
Round kind: FIX. Tier C. Documentation-only design review.

## Required verdicts

- `codex-a`: defect `NOT CLEAN`; design `WRONG SHAPE`; report SHA-256
  `f8a65509d64be686b1f06ffbb59af1b8f364508e683fb0036910540ae27fe675`.
- `codex-b`: defect `NOT CLEAN`; design `STRAINED`; report SHA-256
  `6a5a3f466044b060204cbcfcce95a5c5ba9b65b3a90b92e38916f192988d1f76`.

The design-verdict disagreement is preserved. Both reviewers agree that no
implementation may begin. The coordinator applies the stricter replacement
boundary from `WRONG SHAPE` while retaining the four-role utility decomposition
that both reviews found materially stronger than r001.

The complete coordinator consolidation is retained at SHA-256
`4544f644e42b76c1622dd9a10b7f7ccb3223dbf9e204672aba097b5da9de2f51`.
It is a non-verdict and does not alter either formal report.

## Finding dispositions

- `codex-a` finding 1: **ACCEPTED / BLOCKING**. It is the same defect as
  `codex-b` CB-01 and is consolidated once as C1. The actual packet report and
  issuer-line contract cannot produce the candidate's typed receipt,
  series-state, packet-publication, ordinal, report-prefix, and line grammar.
- `codex-a` finding 2: **ACCEPTED / BLOCKING** as C2. The 16,396-line FIX adds
  unsliced prospective Stage 0b authority surface beyond the r001 correction
  scope and violates the adopted named-slice rule.
- `codex-b` CB-01: **ACCEPTED / BLOCKING**, merged with `codex-a` finding 1 as
  C1. No coordinator rewrite or synthetic reviewer attestation is permitted.
- `codex-b` CB-02: **ACCEPTED / BLOCKING** as C3. Accepted
  `FINALIZE_REVIEWS` and `PUBLISH_DISPOSITION` mutations are expressly absent
  from the real-HTTPS campaign, so their operation-specific public paths are
  not falsified before acceptance.

There are three distinct Important correction classes and no Critical finding.
No formal finding is rejected or downgraded.

## Residual and shape decision

C1 is the first residual of r001 canonical-review-provenance correction class
6. C3 is the first residual of r001 real-HTTPS-rehearsal correction class 7.
The adopted second-residual stop rule is not yet triggered for either contract;
a repeat of either in its next FIX would trigger that stop. C2 is independently
a scope and reviewability violation.

The structural cause is the combination of the reusable authority utility, the
current pre-utility bootstrap adapter, and future Stage 0b automation in one
candidate. Prospective typed artifacts drifted from the actual rule-6 writer,
and selected campaign rows drifted from the complete accepted-operation set.
Another whole-surface prose patch would retain those equality hazards.

## Binding successor direction

Any r003 candidate must be a narrower FIX that:

1. gives the current bootstrap exactly one packet-to-reviewer output grammar,
   with every required preimage available before report freeze and no
   coordinator synthesis of issuer bytes;
2. removes the prospective Stage 0b convergence, activation, publication,
   disposition, and build-authority system into a later, separate NEW-SURFACE
   task rooted in an accepted utility;
3. maps every retained FIX member to an r001 formal or advisory requirement and
   declares named, nonoverlapping review slices if it remains above roughly
   3,000 changed lines; and
4. provides real-HTTPS, case-qualified public-boundary families for
   `FINALIZE_REVIEWS` and `PUBLISH_DISPOSITION`, or removes those operations
   from the accepted bundle and narrows every affected claim.

The successor coverage claim must include consolidation gates C1 through C3
and their falsifying criteria. R002 bytes, reports, ledger lines, packet inputs,
candidate ref, and manifest remain immutable. A successor requires a new ref,
candidate identity, packet, and two fresh cold reviews.

No authority utility, pinned runtime, candidate artifact, test, rehearsal,
controller, analyzer, retained evidence, production source, ceremonial
integration, implementation authorization, or implementation-start publication
may execute on r002 authority. The r002 review ref remains preserved; no
retirement action is taken.
