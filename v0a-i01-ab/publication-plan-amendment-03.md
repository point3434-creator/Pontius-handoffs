# Publication integration test adaptation

The first combined r006/publication check ran181 tests. Five trace assertions/errors
came from the earlier host order: no_start fail_at1 now gates header work before
runtime dispatch; a prefailed host witness likewise never dispatches; create-new
refusal occurs at first flush rather than after a complete hand. These are intended
publication changes. Parser source is unchanged and the dynamic825 clock schedules
already preserve honest prefixes.

Adapt no-start injection to the observed real dispatch boundary, not a new hardcoded
read index. Keep both prefailed-host no-row and prefailed-runtime null-timing causes.
Expect first-write refusal to retain one accepted action with a failed terminal.
Add a real closing-publication clock failure control: valid prepublication terminal
and failed external receipt must remain distinct. Observation-only profiler hooks
may arm the actual source; no ledger/writer helper doubles or parser weakening.
Rerun all focused suites on actual3.11 then3.14 and retain initial failure receipt.
