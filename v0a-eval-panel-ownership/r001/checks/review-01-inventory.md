# Independent initial inventory: eval-panel ownership r001

Reviewer: Codex, independent cold pass 01.
Candidate: 182d14e213c6f0b7d7578e429f81d051a9e59707
Manifest: 438d192a26e39b216cca33099c79f6f607de8e2ec1ca1749d44a50434bc7f6f6
Base: 0bc19bcaad5c6660468094772216cac2dc27a651

Recorded before coverage.md, checks/, prior-disposition.md or repair-plan.md were opened.
Inputs so far: handoff, candidate, manifest, authorization, controller rulings,
dependencies, workflow, frozen implementation brief/design, changed source/tests,
and frozen Job/execution consumers. No other conversations or reviewer outputs were read.

Scope is cleanup, caller-owned observations and boundary publication. The sample-role
contract is a separate dependent candidate, not an unaddressed finding in this scope.
Bridge internals, poker semantics, design steps 4-7 and measurements are outside this review.

Discovery: inspect the complete changed tool and test diff, then follow each owned resource,
mutable observation and published filename to its acquirer, release, writer and consumer.

| Invariant or risk | Related paths | Evidence to inspect |
| --- | --- | --- |
| Every acquired job reaches release | supervise; Job init/close | Acquisition ordering |
| Suspended child cannot escape | Popen, assign, resume, kill | Assignment failure tests |
| Cleanup stays bounded | joins; stream closer | Real pipe backpressure |
| Cleanup truth includes last release | verify; cleanup_verified | Post-close failure |
| Interrupt preserves failure state | defer_interrupts; main | Signal schedules |
| Completed events are caller-owned | receive; queue; drain | Unwind after cleanup |
| Partial hand remains explicit | stages; missing_stages | Budget tests |
| Every final boundary has identity | retain_boundaries; result | Rename then interruption |
| Failed publication preserves bytes | base64; partial files | Write/rename failures |
| One result/journal owner | main; finish_run; append_run | Real disposable run |
| Failure identity remains checkable | plan; final report | Failure result contents |
| Exact candidate and pins | ref, parent, tree, manifest | Git bytes and .NET hashes |

Initial challenges to carry into deferred comparison:

- Job acquisition precedes both the cleanup try/finally and the interrupt deferral.
  Inspect whether interruption after acquisition leaves an unreleased native handle.
- Boundary reconciliation itself performs fallible reads and mutable bookkeeping. Check that
  pending publication identity keeps any actual final filename attributable on interruption.
- SIGINT deferral ends before main's publication and finish_run. Check retained outcome
  guarantees and distinguish ordinary single-interrupt schedules from repeated interruptions.
- Cleanup can report a pending daemon closer; determine whether false certification is
  prevented and whether pending ownership is explicitly retained.
- Follow result bytes to journal output_sha256 and status rendering; green exit alone is weak.

This inventory records questions, not findings. No candidate code or tests were executed.
