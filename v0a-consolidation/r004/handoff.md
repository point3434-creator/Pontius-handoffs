# v0a consolidation r004 independent cold-review handoff

Adversarial read-only review. Round FIX, Tier C. Finalizer: current Codex
implementation session. This is an unpublished local review snapshot, not a
decision commit, source seal, integration, or experiment authorization.

- Frozen repository: D:/Pontius/tmp/v0a-consolidation-r001-r004-frozen/repo
- Ref: refs/heads/review/v0a-consolidation/r004
- Commit: fe1e2fc68675c6c92a1263450b455011b5987207
- Base: bb959371eec17e76ab46ee6e42f1bac49c26d54a
- Tree: 27fa787e80f504f17233c29961d9df545f8eb7dd
- Manifest: 6eb5ec280b6a8051e88d7659920ef74b46ea682a06dc80f688ed951d75f3f221

candidate.json, manifest.sha256 and file-identities.json are in the packet
directory containing repo/. Independently recompute identity from Git blobs,
not checkout bytes, using whole-row digest-first ordinal sorting. The frozen
repository is read-only: never change its files, HEAD, index, refs or config.
Use your own disposable clone for execution or mutation.

## Requirements and permitted inputs

Read candidate CLAUDE.md, docs/workflow.md checklist v1, the increment-one
brief, ADR-0485 and ADR-0486. The controller-approved replacement requirements
are D:/Pontius/tmp/v0a-consolidation-r004-requirements.md, SHA-256
962e70309bdee53edfb54f266c1cd14c2cf6ed17452e81b1b2c4479e3f38f4c9.
That document replaces the former exact-descriptor-inference exception; do not
apply that withdrawn positive-inference obligation to this candidate.

Named slices: exact identity and regression checks of ten r007 core imports;
reduced registration, boundary and CI correctness; and the narrow alignment
refusal with propagation and zero capability grants. Do not reopen the entire
accepted r007 core design or the known-unsound parked analyzer repair. A new
false exact result introduced by this change remains in scope. The ten core
blobs are from ddea6efbeb55cb8b71da1ebd5a359a0c2c901cf1, available read-only
in D:/Pontius at review/v0a-i01-ab/r007 if absent from the clone.

FIX deferred input: D:/Pontius/tmp/v0a-consolidation-r004-coverage.md, SHA-256
cd4116d5f6f0e0a99f71935145d1a1017b25a18f6a09d8154369964709b1fec4.
First write your initial invariant and related-path inventory from requirements
and frozen source. Then read that coverage claim, compare the inventories and
challenge its boundaries. Do not read implementer conversations, previous
reviews, sibling review output, or narrative reports. No need to wait for the
implementer's optional test receipts to begin your own source-based checks.

## Execution and output

Use CPython 3.11.15 at D:/Pontius-tools/py311/Scripts/python.exe first, then
3.14.6 at D:/Pontius/.venv/Scripts/python.exe. Use -B -P, snapshot cwd,
PYTHONPATH=<snapshot>/src, scrub PYTHON/GIT_/PONTIUS_ environment, absolute
PONTIUS_GIT=C:/Program Files/Git/cmd/git.exe, and D:-local TEMP/TMP/TMPDIR.
Narrow normal-Windows-identity escalation may be needed for clone/native
handle checks. No global trust changes, dependency installs, broad profiles,
experiments or GPU runs. Keep tests/probes/reports inside your assigned scratch
directory, not the source or frozen repositories. Do not spawn subagents.

Relevant checks are the four v0a suites, tests/test_inventory_and_profiles.py,
tests/test_stabilization_boundaries.py, generator --check and the public
boundary command. Choose additional probes independently and in proportion to
the narrow corrected contract. Reviewers are independent and mutually blind.

Issue review.md in your assigned directory, bound to commit and manifest, with
Spec/Quality verdicts, Critical/Important/Minor counts, and the required design
verdict SOUND/STRAINED/WRONG SHAPE. Blocking findings require concrete input,
wrong observable result, unmet requirement, source location and verification
criterion. Separate advice from required corrections. Include strengths,
coverage and unverified limits. No fixes or adoption authorization.
