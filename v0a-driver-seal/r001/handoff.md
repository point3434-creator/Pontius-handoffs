# Tier A metadata review - v0a-driver-seal/r001

NEW-SURFACE metadata only. Finalizer: root implementer. No source implementation review.
Candidate d45de2bb4522851723667f65f4450c7155833d9a,
manifest b04f8e29d8e4522aefb5ecc8878e6f40f074b91b0bd58208dcc286f48e820e1d,
ref refs/heads/review/v0a-driver-seal/r001, source repo D:/Pontius,
base af90155ebd970d0be6fe26969b121bd213a7f1f2.

Scope: the new ADR-0488 and generated STATUS.md. Three other files in this five-file
tree must be byte-identical to reviewed source candidate
bdd96aa24286ba1ebcc11bfdbe7d3480fa3f4ad2 (manifest
b085c3cba799a6563b5a9b9ba8a6b274b1f7d013079ea32cae769118c69d0c9f).
This is the small adoption record authorized for preparation, not an approved
integration or rehearsal. Budget one lightweight metadata pass, no broad audit.

Acceptance: independently reconstruct frozen five-file manifest from Git blobs;
confirm payload preservation and no unrelated change; verify ADR identities and
counts against D:/Pontius-handoffs/v0a-driver/r001/{candidate.json,manifest.sha256,
reviews/review-01-codex-a.md,reviews/review-02-codex-b.md,checks/post-review-311/,
checks/post-review-314/}; verify correct authority/claim boundaries; regenerate
STATUS and run existing tests/test_status_generation.py on CPython 3.11.15 first
then 3.14.6 in exclusive disposable D-local clone(s) with LF checkout and -B -P.
Use the existing generator, no generator edits. Root's generated status used its
render_status API encoded directly as UTF-8 to preserve LF output on Windows.

Read frozen CLAUDE.md, applicable workflow Tier A/checklist and ADR-0487 for governing
requirements. The conditional accepted-status wording follows ADR-0487; draft seal
activation still requires explicit controller approval and the ceremonial commit.
The status generator rejects a proposed-status front-door record; that initial
generation failure is retained in checks, not hidden or treated as a product failure.

Use normal-user escalation initially for clones/interpreter to avoid Windows launcher
and ownership limitations. Python slots D:/Pontius-tools/py311/Scripts/python.exe and
D:/Pontius/.venv/Scripts/python.exe; absolute PONTIUS_GIT C:/Program Files/Git/cmd/git.exe;
scrub PYTHON/GIT_/PONTIUS_, set PYTHONNOUSERSITE=1 and snapshot/src PYTHONPATH, snapshot
cwd and exclusive D-local TEMP/TMP/TMPDIR. No dependencies or global trust config edits.

Issue reviews/review-01-codex.md and your own progress.md in this packet with exact
identity pair, Spec/Quality verdict, SOUND/STRAINED/WRONG SHAPE and any concrete required
correction. No fixes, source edits, rehearsal, broad suites, commits, pushes, extra
agents or implementer-transcript reading. The two issued code reviews are permitted
as primary evidence being authenticated, not as substitutes for this metadata review.
