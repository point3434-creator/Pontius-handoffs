# r010 builder engineering validation

Owned output: freeze-and-build-r010.py.
SHA256 ae6c5a845a5571018a869cd0a253e39e84fe75619653f08861347b7d49e0c325.
The wrapper has not been executed. No r010 packet/ref, source change, test run,
main commit or broad gate was created by this subtask.

Static parse and in-memory compile passed under CPython 3.11.15 at
D:/Pontius-tools/py311/Scripts/python.exe, then CPython 3.14.6 at
D:/Pontius/.venv/Scripts/python.exe, using -I -S -B -P. Neither imported Pontius
or executed the compiled module. Source is LF-only, BOM-free, no trailing
whitespace, maximum 100 columns. All 12 fixed helper/payload pins match the
current files. Final census/stability schema and retained owner-probe output
shapes were inspected read-only. The first sandboxed 3.14 launch was denied;
the scoped read-only retry completed successfully. No failed execution was
counted as validation.

Run the builder with actual floor Python and -I -S -B -P. The first positional
argument is validate or freeze. validate performs the complete read-only
preflight and prints its input pins; freeze repeats it and then invokes the
pinned create-only freeze-scoped-round.py. Required named parameters:

- --metadata: absolute final snapshot metadata path.
- --metadata-sha256: literal SHA256 of that file.
- --focused-label: common prefix for the 311/314 focused summaries.
- --owner-label: prefix for the two old independent receipts per slot.
- --callback-label: prefix for the four v5 independent receipts per slot.
- --census and --census-sha256: absolute final census path and literal digest.
- --stability and --stability-sha256: absolute stability path and literal digest.
- --coverage and --coverage-sha256: absolute final coverage draft and literal digest.
- --requirements-sha256: pin abc-r010-requirements-draft.md at task root.
- --protocol-sha256: pin abc-r010-protocol-interpretation.md at task root.

Owner and callback labels may be identical; their artifact name suffixes differ.
The coordinator supplied focused label abc-provenance-v4-focused01 and both
independent labels abc-provenance-v4-independent-green01. Final metadata digest
is b57b5bd719873f0fc9e606dfb5e1089342653425b55ae1b582197400096ef1b3.
Census and stability use the coordinator's final 311-03/stability03 files. The
coverage and document pins must be computed only after the coordinator closes
their drafts; this subtask does not freeze those mutable drafts.

Preflight validates 30 exact receipts/logs: nine focused targets and six
independent payloads per slot. It reparses unittest counts and all 49 independent
case outcomes, verifies commands, pre-import identities, environment, metadata,
unchanged 17-path source and current helper pins. Counts in the self-report are
derived, never copied from r009. It checks 13 preserved Git blobs, four-path FIX
scope, main/work HEAD and raw index hashes, controller documents, baseline,
prior inventory assignments, exact capability rows, final census corpus and
stability pins. After freeze it independently reconstructs the full 17-row
main-based Git-blob manifest and verifies frozen bytes equal executed source.

Limits: artifact modification times corroborate floor-before-dev within each
runner family; existing receipts have no signed execution-time chain. This is
host-controlled engineering evidence, not a hostile-filesystem security claim.
The freeze helper pushes the candidate before packet completion, as in earlier
rounds; a later failure is retained and never rolled back or overwritten. The
post-freeze remote read uses absolute host Git with its credential configuration,
not the scrubbed test environment. Static validation does not demonstrate the
entire preflight or publication path; the coordinator must inspect and run
validate once all final evidence exists, then deliberately select freeze.

The generated handoff preserves independent inventory before deferred coverage,
two fresh mutually blind reviews, the finite 17-target wall only after both
CLEAN verdicts, and exact candidate controller approval before Claude finalizes.
No acceptance readiness file or wall invocation is created by this builder.
