# v0a-i01-seal/r001: independent metadata review

Round NEW-SURFACE, Tier A mechanical seal metadata. Finalizer: current Codex
coordinator. No new runtime or gate behavior is in this review. Review only
the three metadata files and their identity/claim integration with r004.

- Frozen repository: D:/Pontius/tmp/v0a-i01-seal-r001-frozen/repo.
- Ref: refs/heads/review/v0a-i01-seal/r001.
- Commit: 95d9435c79b01303a5d809e567569a0cfb1ac096.
- Base: bb959371eec17e76ab46ee6e42f1bac49c26d54a.
- Tree: e5e31225d3f8e1fa6b73e5c81051af94bd3d1a1b.
- Manifest: d347a0589a1a27c2b37cea80f6c97815eac6bc596cc93827ccb921f081f6c79d.

The full base diff is 20 files. Exactly 17 must match source candidate
fe1e2fc68675c6c92a1263450b455011b5987207, manifest
6eb5ec280b6a8051e88d7659920ef74b46ea682a06dc80f688ed951d75f3f221.
Exactly three files may differ from r004: new ADR-0487, new
docs/architecture/v0a-increment-1-source-bindings.json, and generated STATUS.
The frozen source must remain read-only; clone it separately for any execution.

Read requirements.md in this packet, candidate CLAUDE.md and workflow checklist,
ADR-0485/0486, and the controller-ruling-001.md in
D:/Pontius-handoffs/v0a-consolidation/r004/. That ruling approves the bounded
CPU acceptance and retained inherited fixture caveat and requests this
library-only source-seal record, not a decision commit or rehearsal.

Independently recompute the blob-derived whole-row manifest. Verify source
preservation, the copied JSON identity/contents against r004, source/dependency
and fixture/reader bindings, generated STATUS, exact cited review/check hashes,
the library-versus-argv boundary, and the absence of added operational authority.
Previously issued r004 reports are documentary evidence to check, not a fresh
review of core correctness. Do not read implementation conversations, older
fix narratives, or unrelated parked-lane source. Do not reopen the analyzer or
the complete r007 design; a false metadata claim remains in scope.

The JSON is byte-exact copied materialization, not a new runtime parser or
executable authorization format. Its long API-signature line and the required
single-line ADR front-door metadata/generated STATUS should not be rewrapped
in a way that changes identity or breaks the existing metadata parser.

For checks use a fresh D:-local clone, 3.11.15 first then 3.14.6, -B -P,
snapshot cwd/PYTHONPATH, scrubbed environment, absolute PONTIUS_GIT, D:-local
temporary paths. Existing status checks and the status suite suffice for the
changed generator consumer; choose other read-only checks proportionately.
No full 526-test rerun, guarded profile, dependency installation, experiment,
rehearsal, process termination, source edit, or commit is authorized.

Issue one attributed review under your assigned scratch directory, bound to
the exact commit and manifest, with Spec/Quality and SOUND/STRAINED/WRONG SHAPE
verdicts and C/I/M counts. State whether metadata is ready for the specific
commit-authorization request, without granting that authorization. If CLEAN,
also write your own short ledger-entry.md with the same identity/verdict and
issue date for byte-exact publication; do not write another reviewer's verdict.
Do not spawn subagents.
