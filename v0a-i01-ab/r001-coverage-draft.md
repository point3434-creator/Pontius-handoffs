# r001 coverage planning — failure ownership

Draft recorded before implementation; frozen coverage.md will record executed
cases and subsequent discovery. This narrative is deferred cold-review input.

Invariant: the receipt retains every genuine typed failure once, in occurrence
order, and an in-scope failure cannot escape the host's completion result.
Category: source observation, interval entry/body/exit/finalization and transport
through every exception adapter, including the host's optional publication wrapper.
Discovery: enumerate all Clock* catches, classify/record/closure calls, contextmanager
definitions/usages and public oracle/writer/clock ingress across clock/runtime/replay;
cross-check r006 independent inventories and immutable handover.
Related paths: dispatch admission/transition abort; decision open/ready/emit/close;
bookkeeping and publication; finalization; direct body witness reads; source errors
with arbitrary rendering/metadata; raw body errors and writer path conversion.

Planned controls: source faults at entry/body/exit, dead-witness refusal after entry,
independent same-code body fault after entry, body failure followed by new cleanup
fault, ordinary and fallible error rendering/metadata/traceback, both fixtures,
settlement and actual writer admission. Compare complete receipt cause sequence
to actual independently observed source/body faults; preserve deliveries/records.
Existing full observation and rejected-input sweeps remain opposing controls.
Exclusions: unsupported nested intervals, fabricated/foreign OperationFailed marker
contracts, arbitrary private-state mutation, unrelated policy/value/trace contracts.
Falsifier: lost/invented/reordered cause or host escape on a supported schedule.
