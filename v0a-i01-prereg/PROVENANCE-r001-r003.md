# Provenance: recovered rounds r001–r003

Recovered 2026-09-08 from `D:\Pontius-worktrees\v0a-increment-1-preregistration-review`,
an unregistered directory under the worktrees root — not a git worktree, and not
referenced by any commit. Before this recovery the packet began at r004; the
r001–r003 review evidence existed in exactly one place on one disk.

**Nothing here was rewritten.** Every file is a byte-identical copy of its
source, verified by SHA-256 after placement (58 files, 0 mismatches). Only
filenames and directory placement changed, to match the r004/r005 packet shape.

## Identity checks performed at recovery

Each round's `manifest.sha256` hashes to the `manifest_sha256` its own
`candidate.json` records — the same relation r004 satisfies:

| Round | `manifest_sha256` in candidate.json | `sha256(manifest.sha256)` |
|---|---|---|
| r001 | `4b01560395285a30fb65530fb776598d076c4a7bc687eed89d32e650c18dbdc0` | matches |
| r002 | `da3c4ad5290a49f9d6e600b61e3190047ca6221394a4fc4ad06e40af727d799c` | matches |
| r003 | `f5e5d7a3071518e139e8bdffdbe0f813a510ae80c477fdd9a88fb537be4d6fff` | matches |

Each recorded candidate commit resolves to its archive ref, which is present on
`origin`:

| Round | Candidate commit | Archive ref |
|---|---|---|
| r001 | `073f0c5b8e6ad4f8d6e10dd9118b722186968ddf` | `archive/v0a-i01-prereg/r001` |
| r002 | `119411fda2376d61d9ff310bada71f25aa64de70` | `archive/v0a-i01-prereg/r002` |
| r003 | `953b8703ef93fe261a6857b57bca196b2b8ded9b` | `archive/v0a-i01-prereg/r003` |

All three share base `ca0b2e41bbf5d9fc1649de20379299331de6591a`.

## Two things that differ from r004/r005 — deliberately left alone

**Older candidate schema.** These `candidate.json` files carry
`base` / `ref` / `candidate` / `tree` / `manifest_sha256` / `paths` /
`remote_publication`. They predate `pontius-handoff-candidate-v1`, which uses
`schema_version` / `task_id` / `round` / `ref` / `commit` / `base` / `tree` /
`manifest_sha256` / `date`, and they name the older flat refs
(`refs/heads/review/v0a-increment-1-prereg-r1`) rather than
`review/v0a-i01-prereg/r001`. Migrating the fields would alter evidence bytes,
so the originals stand as written.

**`"remote_publication": "not_performed"`** is recorded in all three. That was
true when written. The archive refs are on `origin` now; this note does not
retroactively change what those files claim.

## Filename mapping

Round files, for `N` in 1–3 mapping to `r00N`:

| Source | Placed |
|---|---|
| `rN-candidate.json` | `r00N/candidate.json` |
| `rN-manifest.txt` | `r00N/manifest.sha256` |
| `rN-review-a.md` | `r00N/reviews/review-01-a.md` |
| `rN-review-b.md` | `r00N/reviews/review-02-b.md` |
| `rN-py311-{0,1,2}.txt`, `rN-py311-verification.json` | `r00N/checks/` (names unchanged) |
| `rN-py314-{0,1,2}.txt`, `rN-py314-verification.json` | `r00N/checks/` (names unchanged) |

Round-specific:

| Source | Placed |
|---|---|
| `r1-counterexamples.md` | `r001/counterexamples.md` |
| `r2-handoff.md` | `r002/handoff.md` |
| `r2-review-disposition.md` | `r002/disposition.md` |
| `r2-review-claude.md` | `r002/reviews/review-03-claude.md` |
| `r2-acceptance-*` (8 files) | `r002/checks/` (names unchanged) |
| `r3-link-counterexample.md` | `r003/link-counterexample.md` |

Cross-round:

| Source | Placed |
|---|---|
| `preregistration-report.md` | packet root |
| `progress.md` | `scripts/recovered-progress.md` (differs from the packet's own `progress.md`; both kept) |
| `freeze_candidate.py`, `freeze_candidate_r3.py`, `freeze_r004.py`, `publish_r005.py`, `run_coderabbit_r2.py`, `verify_r2_identity.py`, `verify_snapshot.py` | `scripts/` |

`scripts/verify_snapshot.py` is **not** the same file as
`r004/checks/verify_snapshot.py`; the digests differ, so both are retained.

**Reviewer attribution.** The sources are named `review-a` / `review-b` with no
reviewer identity in the filename. r004 uses `review-01-codex-a.md` /
`review-02-codex-b.md`. The recovered files were placed as `review-01-a.md` /
`review-02-b.md` rather than asserting an attribution the bytes do not carry.
`r2-review-claude.md` names its reviewer and kept it.

## Not copied

`uv-cache/` (~43 MB) and `venv311/` — reconstructible build caches, no evidence
value. They remain in the source directory, which is otherwise now fully
represented here.
