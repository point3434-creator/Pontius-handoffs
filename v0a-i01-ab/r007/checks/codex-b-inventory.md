# Cold B independent inventory (before deferred coverage)

Candidate ddea6efbeb55cb8b71da1ebd5a359a0c2c901cf1; manifest
c234b4271bd665e869689fb5d976e629703b678faeb3f55532a3615edc98b189.
Recorded 2026-08-30 before opening coverage.md. No implementation narratives,
self-report, plans or peer reviews were used. Governing instructions are current
CLAUDE.md/workflow.md; requirements are ADR-0485, the ADR-0484 brief, and the
R2-04/R2-09/R2-10 required outcomes in the named disposition.

| Invariant/risk | Changed paths and related boundaries | Independent observable criterion |
| --- | --- | --- |
| Ordinary host work is measured and cannot start after required measurement fails | replay.py ReplayHost.run: setup/new_builder, iterator construction/next, feed/retention/serialization, runout/showdown construction, settlement/oracle, semantic digest; runtime.py begin_host_accounting, _OwnedInterval, accounting | Inject delays into actual operations; totals change only in the terminal-at-entry category; required-entry failure prevents later input, writes, evaluation and success. |
| Response walls are disjoint from host bookkeeping | runtime.dispatch/_finish_boundary/_decide_inner and public ActionClockLedger | Post-delivery serializer/write delay affects preparation or post-terminal totals, never the next response; already accepted decisions survive failures. |
| Required rows publish before subsequent event acquisition | replay.feed/flush_rows; trace.TraceBuilder.take_pending; TraceWriter.append | Observe real destination after the first accepted delivery and before next acquisition; native first-write failure prevents a second delivery and retains any created prefix. |
| Terminal accounting cut and receipt are honest | semantic_sha256 -> accounting -> TraceBuilder.close -> flush/finish/cleanup -> stop interval -> finalize_accounting -> HostCompletionReceipt | Terminal totals cover all pre-cut intervals; publication is separate; publication/finalization failure rejects receipt even if completed terminal remains parseable. |
| Stable directory authority, create-new leaf and no reparse escape | TraceWriter._open, _open_native, native NtCreateFile/GetFileType/GetFileInformationByHandle/WriteFile/FlushFileBuffers/CloseHandle | Real local Windows parent replacement/rename/reparse attempts cannot redirect writes; existing leaf unchanged; root and each component held through publication. |
| Ownership precedes probes, close-once is monotonic | _NativeHandle holder registration; TraceWriter._handles/_state/_close_attempted; ReplayHost.close_stream | Native acquisition followed by failed inspection remains owned; native failure closes every held handle once; append/finish after failure cannot resume; later equal cleanup causes retained in actual order. |
| First cause survives body/cleanup/clock faults | _OwnedInterval.__exit__, runtime._retain_error/record, MonotonicWitness.failure; close_stream journal | Actual native/body fault remains primary; later cleanup/clock failures remain ordered secondaries; source clock not retried after failure. |
| Exhaustion is explicit and legal controls remain complete | ReplayHost._events, automatic runout/showdown, runtime.betting_terminal, EVENT_ORDER | Complete A/B and all-in controls pass; exhausted nonterminal fixture returns typed event_order without further acceptance, retaining prior actions. |
| Existing parser, independent legal replay and policy/clock contracts stay intact | trace.parse_trace/validators; replay.verify_successful_trace/_replay_parsed_success; runtime policy binding; model/clock; sealed dependency public APIs | Changed suites and focused controls preserve strict schemas, semantic/payout bindings, action clocks and immutable policy. Stored-blob diff must remain the five named files. |

Planned evidence: independently recompute manifest from commit blobs with no rename
detection and whole-row byte sorting; fresh D-local clone, actual 3.11.15 first,
then 3.14.6; -B -P, asserted executable/version/origins, exact snapshot cwd/src
PYTHONPATH, scrubbed environment and D-local TEMP/TMP, absolute PONTIUS_GIT.
Use only focused permitted replay/trace tests and bounded own diagnostics through
real host/native boundaries. No source/test edits, broad/GPU/install/capability
or lifecycle execution. Native unsupported/error cases will not be reported as
cross-platform success or as forced multiple-native-close evidence.
