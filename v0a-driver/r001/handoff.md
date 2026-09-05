# Cold review request - v0a-driver/r001

Round kind: NEW-SURFACE. Tier C. Finalizer: root implementer, not either reviewer.
Candidate: refs/heads/review/v0a-driver/r001
Commit: bdd96aa24286ba1ebcc11bfdbe7d3480fa3f4ad2
Base: af90155ebd970d0be6fe26969b121bd213a7f1f2
Manifest SHA-256: b085c3cba799a6563b5a9b9ba8a6b274b1f7d013079ea32cae769118c69d0c9f
Source repository holding the local ref: D:/Pontius
Packet: D:/Pontius-handoffs/v0a-driver/r001

## Scope and inputs

Review only the three added files listed in manifest.sha256 and their use of
sealed interfaces. Inputs: candidate.json, manifest.sha256, brief.md; frozen
CLAUDE.md, docs/workflow.md checklist v1, ADR-0485 and ADR-0487. Related sealed
source can be read to judge boundary use, but this is not a new whole-core audit.
No implementer transcript, build report, design discussion or other review may
enter cold context. No FIX coverage file is applicable to this first surface.
checks/311 and checks/314 hold raw prior commands/results; independently execute
the focused new suite before a pass, with independently chosen boundary checks.

Independently recompute the manifest from frozen Git blobs, whole-row byte sort,
LF rows; verify exactly three additions and no change to inherited source.
Use a fresh D-local no-hardlink detached clone of this exact commit, checkout
core.autocrlf=false, and an exclusive reviewer scratch root. Never test from the
primary checkout or source worktree. Run CPython 3.11.15 first at
D:/Pontius-tools/py311/Scripts/python.exe, then CPython 3.14.6 at
D:/Pontius/.venv/Scripts/python.exe, -B -P, cwd snapshot, PYTHONPATH=snapshot/src,
scrub PYTHON/GIT_/PONTIUS_ variables, set PYTHONNOUSERSITE=1, absolute PONTIUS_GIT
C:/Program Files/Git/cmd/git.exe, and D-local TEMP/TMP/TMPDIR. No installs.
Normal-user escalation is allowed for native Windows publication and 3.14 launcher
permissions. An environment refusal is not a product failure or a pass.

## Review contract

Independently assess specification and quality, naming SOUND/STRAINED/WRONG SHAPE.
Each material finding needs an exact scenario, violated requirement, consequence,
source location and the smallest required correction plus verification criterion.
Distinguish required outcomes from advice. Honor the brief's trusted-startup and
no-concurrent-writer scope without weakening its actual provenance/publication
claims. Apply the helper-double rule: acceptance-object doubles prove no native
ownership behavior. Report gaps plainly, with proportionality for this thin driver.
Every run must use a correctness identity; mode rejection checks must stop before
the host. No successful rehearsal-mode run, owner, journal, consumed identity,
GPU operation, policy training, fix, commit, push or source edit is authorized.

No delegation; the two independent review seats are already assigned. Do not read
the other review. Do not alter candidate bytes, primary tree, Git index or HEAD.
Probes may be created only in each reviewer's disposable scratch, retained there.
Write the issued review with identity pair, command/exits and findings to your
assigned reviews/review-01-codex-a.md or reviews/review-02-codex-b.md. Write your own
verdict line to a separate reviewer-specific progress file, avoiding shared writes.
Packet/ref are local pending any separately authorized remote publication.
