# Evaluation panel contract repair plan

Controller authorization: fix the r004 findings, extend review rounds and allow up to
3,000 lines if necessary. Python 3.14.6 only, including utilities. No numerical bridge,
sealed module, full-pool measurement or integration changes are authorized by this work.

Rejected source: 0bc19bcaad5c6660468094772216cac2dc27a651.
Root cause and accepted findings: r004/disposition.md, published in handoff b846226.
Codex implements; Claude reviews the next checkpoint under the recorded alternation.

## Candidate 1: cleanup, observation ownership and publication

Scope: tools/v0a_eval_panel.py and tests/test_eval_panel_tool.py only.
The two prior attempts repaired sequences but left independent copies of the protected
state: a local hands map, a report list, a cached cleanup boolean and published files
without bindings. Replace those projections with explicit ownership and final outcomes.

- Attach records directly to the caller's observations on first receipt; mutate in place.
  Derive missing stages separately. An interrupt cannot require a successful return merge.
- A cleanup certificate is false until resource observations and every required cleanup
  outcome, including Job.close, are known. Failed/interrupted outcomes cannot become true.
- Preserve independent release attempts and protect the release sequence from ordinary
  SIGINT delivery between attempts. Do not retry an ambiguously released native handle.
- Do not synchronously close a stream against a still-live I/O thread after a join timeout;
  a bounded cleanup failure must remain explicit instead of hanging the record owner.
- Register artifact identity before publication and reconcile final-file presence and
  byte identity after successful or ambiguous rename. Pending bytes remain recoverable.
- Real-worker main tests use disposable source clones, the real Job/process and real
  result/journal writers. Fault injection changes timing/failure only, not successful
  resource or filesystem effects. Observe result data and files independently.

## Candidate 2: admitted sample schedule

Scope: the same two files, a separate candidate after candidate 1.
The prior fixes validated count and then an unlabeled set. Both erased the role used
downstream. Admission must produce one canonical schedule with role, board and hand.

- Validate the declared development board and role-specific required members separately.
- Use the admitted schedule directly in worker execution and estimate reconciliation.
- Reject role movement, all-controls/empty-development and rebinding the main board.
- A full run requires every scheduled record complete with all stages and successful
  comparison, including its royal control; otherwise it cannot report completed.
- Run a valid declared-full plan through the actual worker and result writer; independently
  assert four literal development identities, one royal control and a four-hand estimate.

## Execution and review order

For each candidate: write regression tests; freeze a test-only RED snapshot based on the
rejected bytes; run focused suites in a disposable snapshot with its own locked dev venv
under scrubbed environment and ResourceWarning-as-error; inspect actual failure causes;
implement the contract; freeze GREEN candidate; rerun focused suites and record receipts.
Use immutable separate refs/packets for each contract and explicit dependency identities.
Retain both RED and GREEN receipts. Review the combined final state after both candidates.
No ceremonial integration commit or broad suite precedes the applicable cold-review gate.
