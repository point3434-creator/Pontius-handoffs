# v0a driver r001 - bounded build brief and design

Approved scope: a thin CLI over the ADR-0487 sealed host and independent reader.
Base: af90155ebd970d0be6fe26969b121bd213a7f1f2. Tier C (identity and publication).
Implementation files: tools/v0a_rehearsal_driver.py, tests/test_v0a_rehearsal_driver.py,
and docs/architecture/v0a-rehearsal-driver-r001.md, all new. No existing byte changes.
No registration/CI edits: those are sealed; direct focused invocation is explicit.
Budget: one build session, at most 300 driver lines and 300 test lines; one review
round and one bounded correction before returning to the controller. No commit/push.

## Mechanism and acceptance

1. CLI selects exactly control-A or control-B, explicit mode correctness/rehearsal,
   explicit run ID and existing local run root. Root basename must equal run ID;
   run ID must match protocol + mode + a safe nonempty unique suffix. No authorized
   mode. Output is fixed trace.jsonl directly inside the root, create-new through
   the sealed Windows TraceWriter; no overwrite, retry, new owner or journal.
2. Source preflight before importing pontius or writing anything: pinned bindings
   JSON SHA-256; hash every src/pontius/**/*.py against the actual seal Git tree
   using explicit absolute PONTIUS_GIT; reject missing/extra/changed sources and
   bytecode caches. Require -B -P, isolated declared source root, and no preloaded
   pontius module. Put that verified src at the front of sys.path. Read Git blobs
   in one archive operation, not one subprocess per file. The source root may be
   an LF-pinned detached clone with this additive tools/tests/docs overlay.
   This is preflight identity under a no-concurrent-writer assumption, not a
   hostile-process filesystem lock or a Python sandbox.
3. Trace header uses actual seal af90155... and a computed whole-row-sorted
   manifest over actual sealed package files, bindings JSON, driver, tests and
   usage document. The preserved r004 payload manifest is reported separately:
   6eb5ec280b6a8051e88d7659920ef74b46ea682a06dc80f688ed951d75f3f221.
   CLI cannot override identities, blueprint or schedule. Empty reference blueprint
   source_id v0a-empty-reference and the two existing fixtures only.
4. Invoke ReplayHost.run(destination='trace.jsonl', run_root=root), real default
   monotonic clock, mode as supplied. Correctness subprocess tests use correctness
   IDs even with a real clock; no rehearsal invocation during this build.
5. Success requires host receipt passed and accounting_complete; read persisted
   bytes, match receipt digest and in-memory trace, then independent verifier with
   separately expected bindings, mode and monotonic_ns; compare verified run ID.
   Print a compact JSON non-evidentiary receipt. Failure returns nonzero, prints
   typed refusal, retains any created trace, never rewrites or cleans it up.
6. Focused tests: both controls via real CLI/Windows publication; invalid identity,
   wrong root, missing root, wrong source, existing trace, and injected corruption
   at readback/host failure. Fault doubles only for corruption/failure seam, not
   ownership claims. Existing v0a four suites remain unchanged and run as neighbors.

Ground truth: ADR-0485/0487, fixed fixtures' independent chip-depth settlement and
sealed verify_successful_trace; no new completeness proof or strength oracle.
Dependency: only the next separately authorized non-evidentiary rehearsal waits.
Other lanes remain parked by controller direction, not by a new technical dependency.
Stop: any sealed-core modification, new ownership framework, or exceeded budget
requires controller direction. Adoption requires separate cold code reviews and
authorization; development GREEN alone does not authorize execution.
Coverage: fixed CLI options, source mismatch and result acceptance boundaries;
not arbitrary inputs, hostile concurrent mutation or complete Python import proof.
Alternative rejected: rewriting writer/reader or adding lifecycle framework repeats
already sealed mechanisms. Hash labels alone are insufficient, hence byte preflight.
Biggest risks: false provenance from ambient imports; marking failed publication as
success; root reuse; confusing correctness output with operational evidence.
