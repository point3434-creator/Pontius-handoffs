# Independent initial inventory - Codex review 02

Candidate: 0bc19bcaad5c6660468094772216cac2dc27a651
Manifest: 70ca4c76bc8bdefe8ffaab72fa8de5b7d24d49697157436d78a3e1c025a370c3
Base: f647a7989394f084875a040b20c41891168163ed

Recorded before opening coverage.md, checks/, or inputs/prior-disposition.md.
Inputs so far: handoff, candidate identity, pinned workflow/rulings/dependencies,
BASE implementation brief/design, both frozen production files and the first part of
frozen tool tests. No reviewer output, prior review, or implementer conversation was read.

Identity: raw Git blobs establish the seven changed paths, parent, tree, whole-row-sorted
LF manifest and its digest. All 34 direct BASE dependency blob IDs independently match.
The packet's five nondeferred workflow/ruling/dependency hashes also match the handoff.

## Requirements and related paths to challenge

1. Admission must bind exactly one phase, runtime, canonical compatible card population,
   seed/permutation, root and finite resource envelope. Declared-full must preserve the
   development/control roles as well as card membership. A subset cannot claim full work.
   Paths: parse_plan, validate_plan, sample_identity, declared_sample, run_plan,
   preflight_hand, full_pool_estimate; plan fixtures; holdem_cards and river parsing.
2. Capacity must precede any teacher/reference solving, search the actual wire encoding,
   retain both in-domain boundaries, and distinguish a one-row failure/all-fit result.
   Paths: replay_root, root_key, capacity_probe, placeholder_artifact, real codec and key
   schema; worker capacity branch; retain_boundaries and finish_run artifact discovery.
3. Production must sum kernel integer net returns over precisely 990 compatible villains
   at the declared s=4 root. The independent reference must force both hero actions and
   an explicit CALL villain on a singleton game, then reconstruct exact lattice totals.
   Paths: hand_totals, build_reference, forced_value, reference_best_response,
   validate_reference, lattice_integer; legal_river_continuation, evaluation and betting.
4. Numerical acceptance must reject nonfinite values, false ties, wrong non-tie action,
   wrong root map and wrong totals; CHECK wins an exact production tie. Bound assumptions
   must match the only supported CPython 3.14.6 and real reference accumulation/domain.
   Paths: numeric helpers, reference tests, evaluation normalization and summation.
5. Measurement must separate cold/warm production and each reference stage, retain costs
   and cache context, and never project full-H from incomplete required records. Failures
   preserve completed stages and cannot complete preflight or automatically launch H.
   Paths: measure, cache_state, preflight_hand, run_plan, supervise.drain, estimate, main.
6. Resource ownership starts at creation, before fallible operations. Every acquired
   stream/thread/process/job must get an independent bounded cleanup attempt after failure
   or interrupt, including launch/assignment failures. Any recorded cleanup failure must
   prevent cleanup_verified, including failures after verification such as job.close.
   Paths: supervise setup, Popen, thread start, assignment, poll, cleanup attempt/verify,
   host Job implementation; stdout/stderr readers and sender threads.
7. Retained observations must already belong to the caller before any unwind can escape.
   Completed and partial hand records must survive interruptions during cleanup/final
   aggregation. Repeated events cannot replace or falsely complete a prior observation.
   Paths: supervise hands/observations, drain and final aggregation; main try/finally.
8. Boundary publication must keep recoverable bytes or an authoritative binding across
   write, partial write, rename, digest/bind, encoding deletion and retry interruptions.
   A partial file must not be confused with a completed boundary; completed retry is safe.
   Paths: retain_boundaries, file naming and os.replace, main and execution.finish_run.
9. One parent owns source admission/result/journal; the child inherits that context.
   Plans/errors/interruption do not erase source identity or prior completed measurements.
   Paths: main, worker, supervise environment/cwd; execution begin_run/child_context/
   finish_run, status_generation consumers, host admission and actual writer discovery.
10. Evidence must use actual native boundaries for resource claims; injected triggers
    need independent outcome checks. No test may spend a full pool or live owner state.
    Paths: both complete test suites, cases.json registration, test_pontius harness,
    disposable ownership fixture; later compare frozen receipts and declared exclusions.
11. Scope stays within design steps 1-3 and seven frozen paths; whole-slice lines remain
    below the controller ceiling. Claims cannot infer poker strength, host agreement,
    measured campaign feasibility, or authorization from focused correctness tests.

## Intended evidence and open questions

Read all remaining frozen tests and relevant BASE consumers, then read deferred coverage
and receipts and reconcile each inventory member with the actual exercised contract.
Challenge cleanup interruption/failure paths individually, admission relabeling as well
as duplicates, publication interruption windows, and incomplete result aggregation.
Static proof can establish a concrete counterexample; missing execution alone is not a
product defect. Project code, tests, owners, and Git mutations will not be executed.
