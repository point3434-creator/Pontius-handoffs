# Initial invariant and related-path inventory: review 01, Codex

Recorded before opening coverage.md, checks/, or prior disposition.
This is an independent initial inventory, not an exhaustive-proof claim.

Candidate: 0bc19bcaad5c6660468094772216cac2dc27a651
Manifest: 70ca4c76bc8bdefe8ffaab72fa8de5b7d24d49697157436d78a3e1c025a370c3
Base: f647a7989394f084875a040b20c41891168163ed
Tree: 45c76c9c8f2d7fbfa4b00e4e5b8b8cffc538b4fc
Scope: design steps 1-3, seven frozen changed paths; review-only.

## Discovery method

Read the handoff, pinned workflow/rulings/dependency inventory, BASE implementation
brief/design and parent lane design, and the candidate's complete two production modules.
Followed producer-consumer calls and every acquisition, state update, exception, cleanup,
and publication boundary. No candidate code, tests, owners, or retained run was executed.
Read-only Git resolves the ref to the stated commit, sole parent and tree. Raw cat-file
bytes independently reproduce the seven whole-row-byte-sorted LF manifest rows and digest.
All 34 dependency blob IDs reproduce from raw BASE blobs with Git blob framing.
Initial input digests match the handoff. Deferred input contents remain unopened.

## Requirement -> paths -> observable behavior -> evidence to inspect

1. Plan admission and phase isolation -> parse_plan, finite, validate_plan, worker, main;
   both plan fixtures, runtime policy, execution.begin_run/child_context.
   Missing, malformed, nonfinite, wrong-runtime, changed-root or unknown-phase plans refuse
   before work; only capacity/preflight can run; no implicit full-pool continuation.
   Inspect refusal cases, launch arguments/environment, actual source identity receipts.
2. Sample identity and coverage -> sample_identity, declared_sample, validate_plan,
   run_plan, preflight_hand, drain, full_pool_estimate; card parser, hero/villain ranges.
   Every sample is a compatible unique canonical board/hand; declared-full binds the
   declared board, four hands and royal control; emitted names and estimate lookup agree.
   Challenge aliases, duplicate cards/hands, board overlap, wrong types, control/development
   placement, incomplete samples, and repeated/partial stage or completion events.
3. Replayed root and capacity -> replay_root, require_declared_root, root_key,
   strength_blind_permutation, capacity_probe; betting kernel, card view, key and codec.
   Real replay produces the declared root; exact universe/permutation membership; wire
   capacity brackets the in-domain nested prefix and retains actual boundary encodings.
   Inspect independent key, size, decode, empty/all-fit and order controls.
4. Per-hand teacher/reference -> hand_totals, build_reference, forced_value,
   reference_best_response, lattice_integer, validate_reference; river ranker, settlement,
   LegalHeadsUpRiverContinuation, evaluation.expected_utilities/best_response.
   Exactly 990 compatible villains, real integer settlement, explicit CALL villain,
   singleton hero, separate forced values, bounded exact lattice reconstruction before
   action/tie classification. Inspect real singleton sample and arithmetic negative controls.
5. Measurement and stopping -> measure, cache_state, preflight_hand, run_plan, worker;
   supervisor wall/memory limits and result estimate.
   Separate stage costs and cache state, preserve completed stages on kill/disagreement,
   label estimates, and never infer complete coverage from a prefix or subset.
6. Native ownership and cleanup -> supervise plus host.Job/Popen/threads/streams.
   Track acquisition before probes; suspended unassigned process must die; every release
   follows earlier release failure/interruption, including Popen failure and final job close.
   Trace terminate, kill, wait, join, stream close, final drain, verification and job close.
   A failed cleanup cannot certify success; bounded cleanup must still reach the report.
   Inspect independent process-death observations and injected failure scope, not just flags.
7. Observation retention -> receive, receive_errors, drain, hands, caller-owned report,
   main exception/finally, execution.finish_run and status_generation consumers.
   Successfully drained stage observations survive every unwind and preserve their causes;
   missing/repeated records cannot become completed work or an unsupported cost estimate.
   Inspect real worker protocol, failure after completed stages, and one-run journal tests.
8. Boundary publication -> retain_boundaries, base64 decoding, staging write, replace,
   artifact metadata binding, pending deletion, retry/finally; finish_run/result writer.
   A failed/interrupted write retains recoverable bytes; completed artifacts are bound;
   partial files remain distinguishable; retry after complete does not lose metadata.
9. Scope, authority, evidence -> tests/cases.json, test harness, frozen direct dependencies,
   runtime receipts, workflow/rulings, line census and retained-output consumers.
   Only the seven paths change. Tests exercise real claimed boundaries in disposable
   snapshots under 3.14.6, -B -P, scrubbed environment and absolute PONTIUS_GIT.
   No execution/measurement/integration authority follows from a cold verdict. Count the
   whole slice against the pinned 3,000-production ceiling and 1,200/600 working figure.

## Initial limits

Test implementations and deferred receipts/coverage have not yet been inspected. Native
failure reachability, independent test oracles, actual exercised schedules, one-run
integration evidence and source/receipt agreement remain open. Later host agreement,
provider coverage, final teacher export and Slice B belong to later authorized checkpoints.
The 34 direct pins are a semantic inventory, not a transitive closure.
