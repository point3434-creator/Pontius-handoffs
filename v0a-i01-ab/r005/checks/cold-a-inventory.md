# Cold A initial invariant/path inventory — v0a-i01-ab/r005

Recorded before reading deferred coverage.md. Reviewer: Codex cold A.
Candidate 6cdf7b00dac653a9a295bbb86cdc3b5782317491; base c6adbcaa048988361d2388970eaca772711b797b; manifest 83798245d9feac931479478e81c850ac4de277a2903a7523f5745320738cd21f.

Permitted inputs used: handoff/candidate/manifest, current CLAUDE.md/workflow.md, frozen ADR0485 and ADR0484 plus the named increment-one brief, frozen trace/replay source and test symbol inventory, and prior disposition required outcomes. No coverage claim, implementer transcript/plan/self-report or current peer review has been opened.

| Invariant/risk | Public observable check | Related paths and limits |
| --- | --- | --- |
| Frozen identity and scope | Recompute sorted manifest from stored blobs; parent/tree/ref exact; no sealed dependency diff | git diff-tree/cat-file; no checkout hashing as candidate identity |
| Canonical byte trust boundary | Every malformed variant refuses with TraceInvalidError; UTF8/LF/canonical JSON, duplicate/unknown/missing keys, nonfinite and nesting checked | parse_trace; exact header/event/decision/failure/terminal keys; action/timing/preparation/settlement nested fields |
| Exact primitive domains | Reject bool-as-int, out-of-range seats/cards/indices, wrong enums/foreign digests; retain valid schema controls | validators; source_commit and rank-domain handling; private pair ordering versus chance semantics |
| Binding and ordering | Header/hand/policy identities, exact row/event/action indices, terminal uniqueness and counts; recomputed digests cannot legalize malformed content | parse_trace plus verify_successful_trace; failure-event references and decision/failure timing/action pair consistency |
| Timing truthfulness | Completed exact subtraction/partition/deadline flags; interrupted null finals and known flags; failure precedence, interrupted count, monotonic responses | _validate_timing and parse_trace cross-record pass; recognize work cutoff cannot be inferred solely from emission time |
| Explicit accepting boundary | Parser does not claim legal/host success; failed prefixes cannot earn VerifiedTrace | ParsedTrace versus VerifiedTrace; host publication/finalization not proved by trace-only checking |
| Independent expected authority | Raw trace bound to caller-provided exact immutable fixture/policy/source/config/mode/clock; reject substitution or behavior-bearing subtypes | _owned_expected_fixture, verify_successful_trace, _admit_blueprint; no rerunning host/runtime or caller hooks as oracle |
| Legal event/decision replay | Replay current actor, legal action, action indices, state/card hashes, next reveal, full chance outcome, showdown ranks and complete schedule | _replay_parsed_success using sealed betting/card/policy interfaces; table hit, passive, repeated street, fold and showdown controls |
| Complete settlement | Independent chip-depth payout, eligibility/order/final stacks/conservation; explicit (0,1,2,15,15,5) folded 0/1/2/5 tie at 3/4 gives one 38 pot and 19/19 | chip_depth_settlement; real ReplayHost trace accepted by independent checker where legal; production pot assembly never an expected-value oracle |
| Fail closed without invalidating real controls | Both A/B controls; rejected input, accepted late/interrupted responses parse consistently but never pass accepting checker | focused trace/replay suites plus own raw-byte/rebound probes |

Tests will run only from a fresh detached D-local snapshot, on actual 3.11.15 first and 3.14.6 second, -B -P, exact snapshot/src PYTHONPATH, scrubbed environment, absolute Git. No production/test edits, installs, GPU, broad suites, owner invocation, integration, or publication/accounting/Slice C repair. Initial source inspection supports these paths; field and real-path probes will establish results rather than assuming tests or helper structure prove them.
