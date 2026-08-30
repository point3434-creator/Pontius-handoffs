# Additional coordinator verification: v0a-i01-impl/r003

Reviewer: Codex /root, 2026-08-30. This pass is not cold.
Verdict: NOT CLEAN. C-01 confirms the residual R2-03 host failure contract.

## Binding and scope

- Candidate: 47d08d8c1556d776358e15811e3e98b859fd6a8b
- Ref: refs/heads/review/v0a-i01-impl/r003
- Manifest SHA-256:
  cc255e28680f71fe15de78f26bb8f99a337c1c79e12bf3bdf382a8aa74e7844a
- Base: b357d333fc2393b7fc7dcf31f30c86616208c817
- Tree: 35a6667ca3785e750324b3c93103a8994a6d7d6a

This FIX round covers R2-01, R2-02, R2-03, R2-07 and R2-08 only.
The coordinator read historical findings for residual accounting and received
the cold reviewers' observations. This report makes no independence claim.
It records the coordinator's own fresh executions; the disposition separately
reconciles both attributed cold reviews. No source or test was changed.

## C-01 - Important: closure faults erase the required typed failure

Frozen runtime.py catches at lines 288, 298, 321, 331 and 364 set dead-clock
and incomplete-accounting state but discard the exception's typed cause.
The final host receipt at replay.py:571-585 receives no corresponding primary
or secondary code. ADR-0485:269-280 requires primary cause retention and an
ordered collection of later typed failures.

Run each ordinary fixture through the real ReplayHost, immutable blueprint,
runtime and ActionMailbox. Starting with an integer clock advancing 1,000ns
per observation, fault each observation separately using a source exception,
an invalid boolean sample, or a reversed sample. The source exception and
invalid sample enter the real clock_invalid path; reversal enters
clock_reversed. No production runtime, ledger or host implementation is replaced.

| Fixture | Baseline observations | Fault schedules | Missing-cause positions |
| --- | --- | --- | --- |
| A | 138 | 413 | 134, 135, 136, 137, 138 |
| B | 72 | 215 | 68, 69, 70, 71, 72 |

Reversal begins at observation 2 because it requires a previous accepted
sample. Thus the coordinator ran 628 fault schedules per interpreter,
1,256 total, in addition to successful baselines and settlement controls.
Each interpreter reproduces 30 cause-loss cases: five positions per fixture
under three fault kinds. These positions are bookkeeping entry/exit,
publication entry/exit and finalization.

Every affected receipt returns passed=false and accounting_complete=false,
but failure_reason=null and secondary_failures=(). The full sweeps show no
escaping ordinary exception, false success, or lost accepted-decision record.
Those are real improvements; they do not fulfill the separate cause-retention
requirement. This finding concerns host closure, not deferred duration
accounting or trace publication design.

Smallest correction: preserve typed runtime closure failures as values that
the host consumes in occurrence order. Retain the first cause, append later
causes, keep current failed-witness guards, and never obtain a replacement
clock observation. The next regression should assert cause fields as well
as unsuccessful/incomplete status at all five lifecycle seams.

Evidence: checks/codex_scope1_probes.py and the observations in
checks/codex-py311-scope1.txt / checks/codex-py314-scope1.txt.
A diagnostic exit of zero means its reproduction assertions held, not CLEAN.

## Supporting checks

The four existing focused suites pass on actual CPython 3.11.15 first, then
3.14.6: 35 hand replay, 25 trace, 25 replay host and 22 contract faults,
107 per interpreter. See checks/codex-py311-verification.json and
checks/codex-py314-verification.json and their raw suite logs.

For R2-07, two additional controls call the real settlement method before
changing only its returned final stacks or only a pot's eligible seats.
The independent oracle remains unchanged. Both yield settlement_mismatch.
Normal fixture baselines succeed. These controls establish rejection of the
r002 mismatch examples; they do not claim a defect in the sealed game kernel.

R2-08 receives further supporting evidence from unchanged known-delivery
counts and records across all 628 fault schedules on each interpreter.
Cold reports provide the additional real late-acknowledgement control.

## Execution provenance and limits

checks/codex_verify_r003.py independently verifies candidate ref, base, tree,
ten changed blob hashes and the whole-row-sorted LF manifest before creating
disposable clones. Focused-suite snapshots:

- D:/pontius-snapshots/v0a-i01-r003-59e5f7bbb8d7441d9d3f501900991e54/harness
- D:/pontius-snapshots/v0a-i01-r003-f7c260aed2044b2280e1cedd64516064/harness

After focused checks, each snapshot was assigned exclusively to one cold
reviewer. The coordinator's further matrix uses separate fresh clones:

- D:/pontius-snapshots/r003-coordinator-631d80f5f0db433d89b8a07252fb3739/harness
- D:/pontius-snapshots/r003-coordinator-24345e8a5a4744fe84770515c2fbdb1b/harness

checks/codex_run_scope1.py creates those clones and records child execution
receipts. Each child uses absolute Python, -B -P, snapshot cwd and PYTHONPATH,
a scrubbed environment and absolute PONTIUS_GIT. Exact executable,
implementation and full version are asserted before payload imports.
The real release slot is D:/Pontius-tools/py311/Scripts/python.exe;
development is D:/Pontius/.venv/Scripts/python.exe. Required NumPy comes from
the unchanged package baseline; CuPy and Torch remain absent.

Source snapshots are Git-clean after all coordinator payloads; blob/file
hashes agree with the candidate. Diff whitespace checks pass. No broad suite,
GPU work, historical owner, integration, evidence commit or ref retirement
was attempted. Deferred contracts R2-04/05/06/09/10 were not adjudicated.
