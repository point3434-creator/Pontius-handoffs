# Initial independent inventory — review 02, Codex

Recorded 2026-09-09 before reading coverage.md or any checks/ file.
Candidate 9fce4bfba3acf1c34938aa47f37f9743e5011cea; base d8d291cc1f813ce798f2d3a990b2a8bf2297e124.
Manifest d05fd7b821fec534044eeb80acdf23a4fe09767373a67e4cde20bc5ba1bed088.

## Invariants and expected observations

1. Every changed Git fixture launch resolves one absolute executable from PONTIUS_GIT under a scrubbed environment. Check all three call sites and upstream execution.git; ordinary development fallback must not override a supplied path.
2. Each successful workload cleanup certificate implies the native worker/descendants are gone, all registered stream users stopped, and stdin/stdout/stderr are closed. Inspect completion, early budget expiry, failed input/HEAD validation, grant failure, failed assignment, failed thread start/resume, worker error and interruption paths.
3. Join stream users after native termination and before close; no buffered close against a living registered user. Close failures must be retained, deny cleanup success, and not prevent attempts on remaining eligible streams. Exceptional termination/join failures must fail closed.
4. Completed status also requires no retained errors and all selected rows. Late stderr, worker exit codes, event draining, grant counts, nonce matching, input hash/HEAD rechecks and budget checks retain their meaning.
5. Tests observe real subprocess pipe.closed and process exit independently of the certificate. Real Job termination must remain in place. Error injection must not replace closure semantics or erase diagnostics; cleanup added by tests must happen after assertions.
6. Focused receipts must bind to candidate source and locked CPython 3.14.6, -B -P, absent PATH with PONTIUS_GIT, strict ResourceWarning and unraisable warning handling. RED must expose the pre-fix behavior. Broad verification remains a subsequent gate, not a claim inferred from focused success.
7. Frozen identity must be internally exact: parent/ref/tree, exactly the three scoped changed files, raw blob SHA-256 values, whole-row lexicographic LF manifest, dependency pins and supplied input/receipt hashes.

## Related paths and seams

- tools/v0a_blueprint_workload.py: supervise, worker, load_inputs/input_path, main and report status consumer.
- tools/v0a_table_host.py: Job creation, assign, resume, active, terminate, close; native process ownership.
- tools/v0a_table_session.py: nested session/host process ownership and inherited source admission.
- src/pontius/execution.py: absolute Git resolution, begin_run/child_context and finish_run output/journal boundary.
- tests/test_blueprint_workload_session.py: SourceBoundaryTests Git setup/add; PersistentWorkerTests observer and success/refusal/budget/assignment/late-error/nonce tests.
- tests/test_legal_river_quotient_fixed_width_device_preflight.py: Git check-attr launch and unchanged fixture expectations; reflow equivalence.
- src/pontius/legal_river_quotient_fixed_width_device_preflight.py and *_result.py plus durable_evidence_journal.py: relevant fixture source/artifact consumers.
- tools/v0a_blueprint_workload_population.py, *_measure.py, *_report.py: worker measurement and legacy/current report consumers.
- tests/test_pontius.py, tests/cases.json, tests/fixtures/blueprint_workload/control.json, pyproject.toml, uv.lock, .gitattributes: suite registration, isolation and lock/text conventions.

Potential gaps to compare later: actual pre-close failure rather than post-close error; a live reader after join timeout; partial startup; interrupted/worker-error path; downstream handling of false cleanup certification. Missing execution alone is not a defect.

No coverage file, check receipt, implementer transcript or sibling review read at this point. No project/test execution or live source edit performed. Worktree status had pre-existing STATUS.md and execution_journal.jsonl modifications; these are excluded from the frozen review and preserved.
