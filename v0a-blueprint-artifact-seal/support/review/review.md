# Independent Tier A integration metadata review

Issued 2026-09-05 by Codex reviewer `/root/seal_metadata_review`.

Task: `v0a-blueprint-artifact-seal/r001`.
Candidate: `5ba903fcb4ea4b5e4559baa6846fed99730d020b`.
Base: `c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98`.
Tree: `f8f325e33b8b27cade462702762f1987f8ecf8c8`.
Manifest SHA-256:
`36497fb40160365060601255b41fa432171294e968a8df25fcf7d94422f89732`.
Ref: `refs/heads/review/v0a-blueprint-artifact-seal/r001`.

Defect verdict: REQUIRED CORRECTION; not CLEAN.
Spec FAIL. Quality FAIL. Critical/Important/Minor: 0/0/1.
Design verdict: SOUND. Exact incorporation with a separate metadata review and
post-CLEAN status checks fits this integration. The defect is generated-file
packaging hygiene; it does not require source or governance redesign.

## Required correction

M01: Frozen STATUS.md has CRLF line endings (Minor, high confidence).

Location: candidate `STATUS.md`, beginning at line 1 and throughout all 88 lines.
The raw Git blob contains 23,548 bytes, 88 CR bytes and 88 LF bytes; it is BOM-free.
SHA-256: `c05ef95363f3db0c9ff72fcf56932987b3cafc5ecd45a63495e293141d8e5045`.
`git diff --check <base> <candidate>` exits 2 and reports trailing whitespace on
the STATUS lines. This violates CLAUDE.md rule 7 and workflow checklist item 10,
which require LF-only changed governance files. Freezing this candidate would
retain nonconforming generated governance bytes and cannot receive CLEAN.

Required outcome: preserve r001, mechanically generate the same STATUS document
with LF-only, BOM-free bytes in the next frozen metadata candidate, and retain
every other candidate blob unchanged. Verify the raw STATUS difference is only
the 88 CR removals, independently recompute the new manifest, and require the
frozen diff check to pass. After a CLEAN review of the corrected candidate, run
the unchanged status check and 12-test suite on 3.11.15 then 3.14.6 using the
specified isolated snapshots. This is not permission to change the generator.

The controller reported this suspected issue during review. I independently
reproduced it from the immutable Git blob and the frozen diff; the finding is
not based solely on that report. I did not inspect or rely on corrected mutable
authoring bytes. No additional required correction was found.

## Independently established identity and scope

Using absolute `C:/Program Files/Git/cmd/git.exe` against the named object repo,
read-only Git commands resolved the candidate's exact ref, sole parent and tree.
The codec object is `5e56e4454f7b8ccb360d3e36245abc33318349bb`, with sole parent
equal to the integration base and tree `dc18ed133504fe6c7677b494bcefba311cc73704`.
The combined fixture object is `c7de23de276c50463d831f3983fede82a5400ce8`, with
sole parent equal to that codec object and tree
`014ee05a5014181bd63471247e5ee09607bb2346`.

Base-to-integration `diff-tree --no-renames` contains exactly the 14 manifest
paths: the declared 12 payload paths plus ADR-0491 and STATUS. Raw SHA-256 of
each candidate blob matches its packet copy. Whole-row ordinal sorting of the
digest/two-space/path/LF rows reproduces the packet manifest and bound digest.
Every one of the 12 payload blobs equals the combined fixture candidate.
Combined-to-integration has only STATUS modified and ADR-0491 added.
Codec-to-combined has only inventory and its test module modified. Consequently
runtime, driver, prior ADR and other source bytes are preserved by identity.
ADR-0491 is LF-only and BOM-free (8,486 bytes, 154 LF, zero CR).

## Documentary incorporation and authority

I read the packet handoff, primary CLAUDE.md completely, relevant workflow
Tier A/cold-review/Stage 5/checklist rules, ADR-0490, frozen ADR-0491 and STATUS,
both codec amendment authorizations, fixture brief and both design addenda,
the four issued final implementation reviews, and fixture acceptance record.
I used the code-verification skill for bounded evidence and verdict separation.

ADR-0491 carries the exact codec source identity and fixture identity. Its
driver-origin/three-import exception and unchanged driver-test registration
match the two authorization records. The separately adopted fixture exception
remains confined to numeric reuse at the Windows API boundary and its reviewed
test/inventory bytes. Real writer and cleanup execution, native resources,
independent raw-native identity/liveness observations and bad-replay controls
remain required. The stated population is the existing 14 schedules, with no
claim to cover every Windows allocation schedule or a general helper waiver.

The decision and generated front door require the separately authorized commit
for effect. A review ref, draft, generated STATUS or passing test does not
activate the seal. No operating, research or rehearsal permission, new lane,
analyzer repair or grant, policy-search authority, historical reclassification,
hosted-CI pass, strategic-improvement result or timing result is introduced.
The known-unsound analyzer remains parked, runtime/driver seals remain intact,
and budgets, authoritative population and invocation authority remain closed.
The STATUS text diff reflects ADR-0491 and the normal recent-ledger window;
research ADR-0280, runtime ADR-0307 and revoked authorities stay unchanged.

## Evidence verification

All ten ADR-bound digests checked directly against raw files match: the two
amendment inputs, four final implementation reports, acceptance.md,
acceptance-evidence.sha256, codec manifest and fixture manifest. All 43 rows of
acceptance-evidence.sha256 also match their raw targets: 38 receipts, two
summaries and three runner/audit scripts. These are prior source evidence,
not this reviewer's own implementation verdict.

Each final implementation report names the correct source candidate and reports
CLEAN, Spec PASS, Quality PASS, C/I/M 0/0/0, Design SOUND. Their finite scope,
earlier failed attempts, correction history and environment limitations remain
visible. ADR-0491 preserves those limits and does not turn prior failures into
passing evidence or claim Ruff ran when it was unavailable.

I parsed every one of the 38 broad raw receipts. Each contains successful
interpreter preflight and payload exit zero with -B -P. Preflight stdout records
3.11.15 or 3.14.6 as appropriate. Per slot, the receipts total 19 commands,
495 unittest methods and one skip, leaving 494 passing methods. Both complete
inventory runs report 91 tests. All 12 combined-payload hashes in each of the
38 retained snapshots match: 456 comparisons passed. This independently binds
the prior executed source to the source now being incorporated.

The inspected runner fixes snapshot-root cwd and PYTHONPATH, clears the child
environment, supplies absolute Git, checks interpreter/module origin, uses
fresh no-hardlink D-local snapshots and refuses reused snapshot names. The
bound broad runner has one invocation per numbered command and no retry loop.
The acceptance record identifies the one existing POSIX-only skip; no Windows
reuse coverage is represented as skipped. Source acceptance is correctly stated
as bounded local evidence, predating ADR-0491 and STATUS.

## Commands, limits and disposition

Fresh read-only PowerShell/.NET raw-byte hashing, Git metadata/diff commands,
receipt parsing and snapshot hash comparisons passed as detailed above.
The frozen `git diff --check` failed exactly as M01 records. One initial audit
command had a PowerShell variable-delimiter parse error before execution; the
corrected read-only command succeeded. That was a reviewer command error, not
a candidate test failure.

No new task payload or broad acceptance suite was executed by this reviewer.
The handoff assigns post-CLEAN metadata execution to the controller; that gate
remains pending, and cannot be spent against this non-CLEAN r001 as acceptance.
Prior source receipts do not establish freshness of the added metadata.
This review is limited to faithful incorporation, identity and authority; it
does not repeat or replace the prior Tier C implementation reviews.

Only this issued report and its attributed verdict-line are written. Candidate,
source, packets, ledgers, refs and historical evidence are not changed. No
commit, publication, push, dependency installation or agent delegation occurs.
