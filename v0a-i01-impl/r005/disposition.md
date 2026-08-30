# v0a-i01-impl/r005 disposition

Coordinator: Codex /root, 2026-08-30. Finalizer: Claude.
Verdict: NOT CLEAN. Design: STRAINED. Two Important mechanisms of the same
R2-03 host-cause contract remain; no implementation integration.

Candidate: a8582e6d6b53b55415dab79c4a54e252d00b74ad
Manifest SHA-256: e9b0baf12e258d66a92169d38137cbf2f42317158b6515ac377f745bbc52093a
Ref: refs/heads/review/v0a-i01-impl/r005
Base: b357d333fc2393b7fc7dcf31f30c86616208c817
Tree: 5d373871b27bed5ef026150b816d684a588b75c3

The ten blob identities and full manifest verify. Only runtime.py, replay.py
and test_v0a_replay.py changed from r004. Two cold reviewers independently
recorded their initial inventories before reading the author's coverage claim.
The coordinator performed additional checks; it does not claim a third cold pass.

## R5-01: body failure can be overtaken by its cleanup failure

Important / Medium, high confidence. Attribution: cold A R5-A01, cold B R5-B01,
and independent coordinator R5-C01. Frozen replay.py:496-532 and runtime.py:341-350.

A public oracle callback raises ValueError/ZeroDivisionError. During unwind,
the real bookkeeping exit observes a clock fault. Expected primary
settlement_mismatch then secondary clock_invalid/reversed; actual order is
reversed. Both faults actually occur. The body error is journalled by an except
outside the context only after cleanup has journalled its own error.

Required: classify and retain the initiating body cause before cleanup executes;
retain genuine later causes exactly once, in order. ADR-0485:269-280 and :437-441
already bind this. No ADR amendment or category-ranking rule is needed.

## R5-02: real clock failure in host work can disappear

Important / Medium, high confidence. Attribution: independently cold A R5-A02
and cold B R5-B02, then coordinator reproduction R5-C02.
Frozen replay.py:524-526, with runtime.py:344-348.

Pass a real public MonotonicWitness as the host clock and use that same witness
inside the public oracle callback. A real source exception, invalid value or
reversal raises the typed clock error there. Cleanup sees the dead witness and
correctly suppresses its own synthetic refusal, but the host typed catch assumes
the original cause was already recorded. The failed receipt has no primary
and no secondary code. Expected exactly the original clock_invalid/reversed.

Required: exception type or witness death must not stand in for proof that this
occurrence was retained. Assign original-cause ownership at the actual body
boundary, without duplication, type loss or another source sample.
The default oracle does not sample a clock; this is the supported public
injection path used to challenge the new branch, not a claim about the ordinary
no-fault default execution.

## Progress and evidence

Both previous r004 mechanisms are now corrected: the first real writer refusal
stays primary, and rejected-event abort retains its later typed clock cause.
All 119 focused tests pass per actual interpreter: 35 hand replay, 25 trace,
37 replay and 22 contract-fault tests.

Coordinator repeated 628 single-clock-fault schedules over A/B, 56 wrong-turn
faults plus a control, and six real writer schedules. New host-body diagnostics
provide 24 ordinary-exception/exit-fault ordering counterexamples, and six real
shared-witness fault counterexamples, per interpreter. The no-fault/opposing
controls pass; accepted action and decision counts survive. Counts overlap
between reviewers and are not summed as unique coverage.

Cold A ran 30 selected existing tests and nine diagnostic schedules per slot;
cold B ran all 37 replay tests and fourteen observation cases per slot.
Both also checked complete delivered-record preservation on their acknowledged
delivery fault controls. Coordinator receipts primarily check delivery counts;
these are not presented as complete-value comparison evidence.

All three passes used actual CPython3.11.15 first, then3.14.6, in fresh
disposable snapshots, with pre-import identity assertions, -B -P, exact snapshot
cwd/src PYTHONPATH, scrubbed environments and absolute Git. Snapshots stayed
clean. See checks/ receipts and the reports for exact commands/hashes.

The initial coordinator unwind probe includes deliberately raised clock-shaped
exceptions with provisional expected settlement typing; that subset is expressly
excluded from adjudication. The separate real-witness probe establishes R5-02.
Diagnostic exit zero means capture completed, never candidate acceptance.
Initial reviewer-harness errors are retained with corrected new-version probes;
they are not counted as product failures.

## Reconciled design and scope

All issued design verdicts are STRAINED. Keep the append-only journal: its
representation fixes the old merge/cursor/ranking problem. Complete ownership
at host operation boundaries before exceptional unwind. A bounded correction
of that flow is proportionate; evidence does not justify rewriting the hand,
solver, sealed ledgers or spine.

Cold B labels R5-B01 High, whereas cold A and coordinator use Important/Medium.
This disposition retains Important/Medium: the reproduced impact is incorrect
failure identity/order, with failed receipts, delivered actions and no-resample
guards intact. Both assessments block acceptance of this contract; the original
severity assessment remains unchanged in B's report.

The coverage work was useful. Its remaining boundary was too narrow: ledger
closing calls and clock-only projections cannot establish host body ownership
or ordering across clock and settlement causes. The next test model should
cross returned mismatch versus raised error, ledger versus direct witness origin,
and entry/body/exit/finalization, proving actual fault occurrence and exact
first/rest. Structural discovery and the ledger conservation observer remain
supporting checks. Required behavior is binding; the suggested representation
and test organization are advisory.

The prior root-cause note is present and r005 correctly isolated R2-03.
This is the third residual of that one contract, not two new contracts. Preserve
isolation; explain the newly demonstrated host-body/origin gap in the next
handoff or an append-only supplement to the existing root-cause history. Do not
reset evidence or reopen closed/deferred contracts.

Cold B's unchanged malformed destination, malformed fixture, and injected
builder-exception observations are retained as non-counted scope notes.
They do not add gates to this FIX. Policy authority R3-01, deferred
R2-04/05/06/09/10 and the separate value audit retain their existing dispositions.
The prospective coverage-guidance/r002 update is not imposed retroactively
as a coverage.md requirement on r005.

## Issued records

- reviews/review-01-codex-a.md
  SHA-256 d3b54f0c740bd5cb09393c9cbd4680f56a5f4ebba1745817eb21d446f493b01c
- reviews/review-02-codex-b.md
  SHA-256 7c70f0f33ef510d5ed8a99145a1940c4e806c0a7d865e1b564e4c15ee83cfc5a
- reviews/review-03-codex-coordinator.md
  SHA-256 a3cb809433cc5a1fc0750445e11eb5eac5b47c019d347f8b1ce2dd69046c243a

Each issuer appends its own bound task verdict under a serialized slot. This is
the single program disposition. Routine packet commit/push publishes review
records only. Source integration, broad/GPU suites, experiments, installations,
performance claims and increment acceptance are not authorized by this review.
Claude retains finalization when a successor clears review and applicable gates.
