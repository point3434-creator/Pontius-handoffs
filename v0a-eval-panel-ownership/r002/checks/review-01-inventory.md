# Independent inventory: eval-ownership-r002-review-01

Reviewer: Codex; cold review; 2026-09-09.
Candidate: d8d291cc1f813ce798f2d3a990b2a8bf2297e124
Manifest: 86a583d27d71c251f89f507b4761318433218f0450be649fb768c83b3d8c6926
Base: 72954e1331c9b191d927c1c4b82f277bcd322a4c

Recorded before opening coverage.md, checks/, dispositions or repair-plan.md.
Inputs so far: handoff, candidate identity, manifest rows, governing workflow,
authorization/rulings, dependencies.json, frozen brief/design, and frozen source/tests.
No prior reviews, implementer transcripts, sibling outputs, Python or project execution.

## Independent protected invariants and related paths

1. Each acquired native job/process/stream and started I/O thread must acquire an owner
   before an interrupt or failure can abandon it. Suspended and assigned process states
   must both terminate; native Job.close consumes its handle once. Inspect supervise
   335-495, defer_interrupts 297-313, close_stream 316-332, host Job 326-446.
2. All releases must be attempted despite preceding failure; cleanup certification is
   derived only after last release and handler restoration from verified resource state.
   Interrupt and cleanup failures must remain observable. Inspect acquisition 403-421,
   release 440-480, certificate 481-493, and main exception/retention 612-620.
3. Observations belong to the report as soon as received; worker failure, budget expiry,
   interruption, thread failure and drain failure cannot erase completed stages. Inspect
   worker 219-294, receive/send/drain 355-401, loop 422-439 and final drain 477.
4. Admission, execution, completion and estimation share board/hand/role identity.
   Exact sample membership and all required stages with validated comparison precede
   success/estimation. Inspect ScheduledHand/AdmittedPlan 52-71, validate_plan 111-186,
   run_plan 252-279, drain 373-401, complete_sample 539-553, estimate 556-573.
5. Measured capacity bytes remain recoverable until actual publication is bound by path,
   byte length and SHA-256. Interrupted writes and successful-then-interrupted rename
   must preserve pending bytes or a final identity. Inspect retain_boundaries 498-536
   and its main consumer 604-620; include interrupts during reconciliation itself.
6. Exactly one parent result and journal row records success/failure, after owner cleanup;
   children inherit context. Inspect main 576-622, execution.begin_run/child_context/
   finish_run and status_generation.append_run/read_runs/render_status. Check whether
   finalization receives a stable report or any surviving producer can still mutate it.
7. Reports cannot promote missing observations or failed comparison to completed work;
   partial measurements cannot imply full-pool feasibility. Capacity and preflight are
   separate phases. Inspect completion predicate, warm repeat and estimate consumers.
8. Scope/identity: exactly two changed files against the stated immediate base, unchanged
   bridge/sealed source, exact whole-row-sorted LF manifest, all packet pins, and direct
   dependency blob pins evaluated at their original base f647a798..., not r002's parent.

## Discovery and evidence plan

Read the complete frozen tool and changed test module, not only the 17-line source diff.
Search frozen src/tools and suite registry for ownership fields and consumers. Read the
actual native Job and execution writer/status consumer. Enumerate acquisitions, transfers,
release attempts, interrupt boundaries, worker event kinds and report mutations. Inspect
real-boundary tests and identify which effects remain native and which triggers are injected.
Then compare this inventory to deferred coverage and receipts, verifying identities with
read-only Git plus PowerShell/.NET raw bytes. Receipts are supplied evidence, not my runs.

Potential boundary questions to resolve: handler lifetime through report finalization;
interrupts while reconciling renamed files; I/O/closer threads after timeout; report ownership
through JSON copy and result/journal writes; exact schedule completion and warm-repeat handling.
Missing tests alone are not product findings. A material finding needs a concrete admissible
state transition, frozen locations, violated invariant and required correction/verification.
