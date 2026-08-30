# Terminal T-01/T-02 structured coverage claim

Implementer claim for coordinator freeze; not a cold-review verdict. Only trace.py
and test_v0a_trace.py differ from r005 commit 6cdf7b00dac653a9a295bbb86cdc3b5782317491.
Final file identities and receipt hashes: terminal-checks/terminal-final-hashes.json.

| Category/invariant | Enumerated paths and controls | Evidence | Residual limit |
| --- | --- | --- | --- |
| T-01 all-outcome terminal flags | Success, delivered late/completed failure, accepted interrupted, accepted then unknown acknowledgement, real rejected nondelivery, no-start, event-order rejection, invalid input, host-only settlement. All eight flag tuples each, explicit allowed sets | TerminalAdmissionTests.test_all_flag_combinations_for_real_outcome_variants; 72 cases | Ordinary failed/no-start flags cannot reconstruct missing chronology; no added implication beyond the plan |
| Interrupted/unknown forces incomplete failure/accounting | Real interrupted/unknown/rejected controls; independently rebound unknown with null timing and zero interrupted count | test_real_outcome_controls_preserve_delivery_timing_and_terminal_fields; test_unknown_delivery_forces_flags_even_without_a_started_timing_record | Unknown count is never evidence of nondelivery |
| Failed/incomplete settlement null; failed reason retained | Rebound real failed variants with success settlement, erased reason, unrelated nonclock replacement | test_failed_settlement_and_erased_or_replaced_primary_are_refused | Host-only rows have no earlier record proving another primary |
| Complete category totals | Five failure variants, every null/present pair with accounting true and false | test_accounting_complete_requires_both_category_totals_on_failed_hands | Does not establish host measured work from trace-only values |
| Primary compatibility | Six actual source-before-ack/exception/rejection paths, invalid and reversed source; real zero-acceptance rejection; both prefailed witnesses; opposing source/settlement-body order; event_order before cleanup | test_source_cause_survives_later_real_adapter_outcomes; test_prefailed_witness_and_opposing_host_only_source_body_causes; sweep controls | Current fields cannot independently reconstruct hidden source/body ordering; compatible clock primary is deliberately preserved |
| Honest fault prefixes | All 138 normal A and 19 rejected-input observed source reads, bool-invalid/reversed/raised source faults, 471 schedules; 12 input-first cleanup controls | test_every_observed_normal_and_rejected_input_clock_read_preserves_prefixes | First reversed-source read is negative/invalid because no earlier witness exists. Not exhaustive over future paths |
| Host-only final writer failure | Existing destination through real writer, retained bytes unchanged, failed host receipt and valid pre-publication terminal | test_real_host_write_failure_keeps_prepublication_trace_inspectable | Trace terminal cannot attest later publication completion |
| T-02 common event schema | Four pure known constructors; exact common wire field negative domains, nested HandAction keys/types, constructor errors typed | EventConstructorAdmissionTests + retained TraceSchemaRegressionTests | Object subclasses cannot survive JSON as distinct primitive types; no executable deserialization |
| Event-specific domains | Start seats/stacks/blinds/cards including descending, duplicates, bool, range; four action variants; all reveal widths; rank scalar/tuple/null domains | Five EventConstructorAdmissionTests methods | Stack >= big blind, stream position and comparable rank domain remain reader context; legal state remains accepting replay scope |
| Positive event preservation | Ascending pair, stack equal to big blind, unsorted public reveal sequence, signed strengths, unequal rank-tuple lengths, all-null structural ranks | Same five methods and retained successes | Structurally valid mutations are not claimed as legally valid successful hands |

Independent digest rebinding is the test's json/sha256 projection; no production
semantic helper or new terminal helper supplies expectations. Real ActionMailbox,
MonotonicWitness, runtime dispatch, ReplayHost and writer paths execute. The invalid
host input generator changes only the external input presented to real dispatch.

RED02: 14 methods with73 intended missing-refusal failures against unchanged r005
production. RED01 additionally had one unsupported category-availability assertion,
corrected before production edits; both retained. Final fresh snapshot suites on
actual3.11.15 first and3.14.6 second:45 hand-replay +48 trace +53 replay +22 faults =
168 each, all exit0. Exact commands/logs/environment in green04-final-311 and
green05-final-314 receipts. No source/replay/ownership acceptance beyond this scope.

Coordinator-reported producer contradiction (proper script-prefix exhaustion with
failed/null reason) remains refused by this parser and is fixed in the separate
coordinator-owned replay change. No reader weakening or cross-scope repair here.
