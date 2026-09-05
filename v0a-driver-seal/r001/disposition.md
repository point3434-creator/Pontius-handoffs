# Driver source-seal preparation complete; authorization outstanding

Exact five-file candidate: d45de2bb4522851723667f65f4450c7155833d9a.
Manifest: b04f8e29d8e4522aefb5ecc8878e6f40f074b91b0bd58208dcc286f48e820e1d.
Tree: 3f1440fcec994239ed7598f391a9a325350dd4ab.
Required integration parent: af90155ebd970d0be6fe26969b121bd213a7f1f2.

The candidate adds ADR-0488 and regenerates STATUS, preserving exactly all three
driver files reviewed as bdd96aa24286ba1ebcc11bfdbe7d3480fa3f4ad2. The two independent
code reviews remain bound to those unchanged files. One fresh Tier A metadata
review returned CLEAN / Spec PASS / Quality PASS / SOUND, zero findings.
Review SHA-256: 2d4eb2d1be94732e91271e74f5c9300e925a7cb9cfe67f9e9716c0fc4c2d4a30.
The coordinator read the issued report and independently checked its file digest.

After review, fresh no-hardlink detached clones of this exact five-file candidate
ran six suites on CPython 3.11.15 first, then 3.14.6: status 12, driver 12, hand
replay 45, trace 53, replay 62 and contract faults 22. Total 206 passed per slot,
zero failures or skips, all six command exits zero; snapshot sources stayed clean.
Raw final receipts are retained at checks/final-311/ and checks/final-314/.
This is bounded affected-surface verification, not a full repository or hosted CI run.
No test capability, scientific-profile approval or operational authority is added.

The initial draft used a proposed-status front-door header, refused by the sealed
status generator. Only the draft header changed to ADR-0487's conditional accepted
convention; explicit inactivity until controller approval and decision commit is
preserved. The original generation refusal log remains in checks. No generator or
reviewed driver byte changed. Generated STATUS is byte-exact on both interpreters.

Remaining requested controller authorization, not yet exercised:

1. Publish only the new v0a-driver/r001 and v0a-driver-seal/r001 coordination packets
   in Pontius-handoffs, with narrowly scoped attributes if needed to preserve raw
   log bytes. Do not include unrelated handoff changes or retire old refs.
2. Approve ADR-0488's exact bounded seal/acceptance disposition and make the five-file
   decision commit titled "Source-seal the non-evidentiary v0a driver", matching this
   candidate's tree and parent, fast-forward master and push origin/master.

These actions do not authorize a rehearsal. Exact invocation binding and explicit
execution authorization remain a separate next step after the driver seal. Until
authorization, primary master/HEAD and index remain untouched, no remote is updated,
and the review refs are retained local exchange objects, not decision commits.
