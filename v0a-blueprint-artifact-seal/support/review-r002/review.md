# Independent Tier A metadata correction review

Issued 2026-09-05 by Codex reviewer `/root/seal_metadata_correction_review`.
Task: `v0a-blueprint-artifact-seal/r002`, FIX.
Candidate: `12df7106b2fca3b25ed4f57115ba9a31e70b6815`.
Base and sole parent: `c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98`.
Tree: `f3acfba65b32e0890bb86f0af9c087f55e75e50d`.
Manifest SHA-256:
`c09f4bcc313e987764597f49ef703e8794e76e7be725dc52a642850803a5bb1c`.
Ref: `refs/heads/review/v0a-blueprint-artifact-seal/r002`.
Prior candidate: `5ba903fcb4ea4b5e4559baa6846fed99730d020b`.

Defect verdict: CLEAN. Spec PASS. Quality PASS. C/I/M: 0/0/0.
No required correction remains within this metadata correction review.
Design verdict: SOUND. Exact source incorporation, unchanged decision text and
a bounded raw-byte serialization correction fit the contract. There is no new
implementation, authority mechanism or recurring design residual to redesign.
This is a metadata verdict, not a new Tier C source verdict or acceptance run.

## Binding correction closed

Prior review `review/review.md` required M01: preserve r001 and remove precisely
the STATUS CRLF serialization defect in a new frozen candidate, retaining every
other blob and the unchanged generator. That issued report was read completely.

Fresh raw-object checks establish:

- The complete r001/r002 changed-path set is `STATUS.md` alone.
- Old STATUS: 23,548 bytes, 88 CR and 88 LF;
  SHA-256 `c05ef95363f3db0c9ff72fcf56932987b3cafc5ecd45a63495e293141d8e5045`.
- New STATUS: 23,460 bytes, zero CR and 88 LF;
  SHA-256 `2932b3fbf79346f7c80162de73360de9fc0ea3b4371e25b4c84a3ac73b325df2`.
- Replacing CRLF with LF in the complete old content equals the complete new
  content exactly. All 88 removed bytes are carriage returns.
- Both base-to-r002 and r001-to-r002 `git diff --check` exit zero.
- All 14 frozen changed files have zero CR bytes, no UTF-8 BOM and no trailing
  spaces or tabs. Generated historical STATUS ledger row widths are unchanged.
- ADR-0491, `src/pontius/status_generation.py` and its test module equal r001;
  the renderer and its test also equal the integration base.

The unchanged renderer returns LF-joined text, while its CLI uses text output
with platform newline translation. Its `--check` reads text with universal
newline handling. Raw byte inspection is therefore necessary for M01 closure;
a text freshness check alone would not distinguish the rejected serialization.
No generator edit is needed or included in this correction.

## Independent discovery and deferred coverage

`independent-inventory.md` was written before opening coverage.md or the prior
review report. It enumerates the incorporation invariant, raw correction site,
all related metadata/source identity sites and the separate execution gate.
Its initial git comparison independently identified STATUS alone and an empty
end-of-line-whitespace-insensitive diff.

The subsequently opened coverage file has the handoff-bound SHA-256
`95641a4ce97fbc3b88fabc7113c92ff53dc711b9310c44eef49d1efbc43f4a1d`.
Its category and falsifier agree with the independent inventory. Exact content
comparison, complete changed-path enumeration and raw hashing verify its claim
that only 88 CR bytes were removed. No missed correction member was found.
The claim properly keeps both interpreter metadata gates pending and does not
treat universal-newline equality as raw hygiene evidence.

## Incorporation, identity and authority

Read-only absolute Git and .NET raw-byte checks independently resolved the
candidate's sole parent, tree and ref, the 14-path base delta, every raw packet
copy and the manifest. SHA-256 rows were reconstructed from frozen Git blobs,
whole-row ordinal-sorted and joined with LF. Their bytes reproduce the packet
manifest and the exact bound digest above.

All 12 original payload blobs equal combined source
`c7de23de276c50463d831f3983fede82a5400ce8`. Its sole parent is codec
`5e56e4454f7b8ccb360d3e36245abc33318349bb`; their trees match ADR-0491.
Codec-to-combined changes only inventory and its test module. Combined-to-r002
changes only STATUS and adds ADR-0491. Runtime, driver, earlier ADRs and other
source bytes are consequently preserved by object identity.

I read both handoffs, primary CLAUDE.md completely, relevant Tier A/FIX,
manifest, cold-review and Stage 5 workflow rules, ADR-0490, ADR-0491, both codec
amendment authorizations, the fixture brief and both design addenda, and the
prior acceptance record. The code-verification skill kept this pass limited to
identity, faithful incorporation, the correction and the evidence's limits.

The unchanged ADR confines adoption to the exact source payload, two existing
codec extensions and separately approved fixture exception. The real writer,
native resources, independent native observations and erroneous-replay controls
remain required for the finite 14-schedule fixture scope. No general helper
waiver or workflow amendment is introduced. Its source seal activates only at
the separately authorized decision commit. Draft metadata and passing checks
do not activate it. No operating, research, rehearsal, policy-search or new-lane
authority is added. Analyzer repair remains parked with zero grants, historical
failures retain their standing, and ADR-0307 remains the runtime contract.

## Prior evidence remains identified, not recertified

All ten ADR-bound raw-file digests match: two amendment inputs, four issued
source reports, acceptance.md, acceptance-evidence.sha256 and both source
manifests. The four report identities and verdict sections name their correct
source candidates and CLEAN, Spec PASS, Quality PASS, C/I/M 0/0/0, Design SOUND.
All 43 rows in acceptance-evidence.sha256 also match their raw target hashes.

The unchanged acceptance record names the 38 prior commands: 19 on 3.11.15,
then 19 on 3.14.6; per slot 495 methods, 494 passing and one POSIX-only skip,
plus three consistency commands. Both inventory runs name 91 methods. It
preserves failures, environment limitations, unavailable Ruff and local-only
standing. This correction does not claim hosted CI, strategy or timing proof.
The prior r001 review's detailed receipt/snapshot audit remains prior evidence.
I did not repeat that behavioral review or execute its broad source population.

## Fresh checks and remaining gate

Reviewer-owned `check-raw.ps1` runs the raw Git/.NET identity, manifest, packet,
payload, hygiene, exact correction and diff checks above. Final execution
exited zero with all assertions passing. Supporting read-only commands hashed
the ten bound files and 43 acceptance targets and inspected report identities.

An initial reviewer-script BOM predicate used culture-sensitive StartsWith and
incorrectly matched an ignorable BOM character against BOM-free content. The
predicate was changed to ordinal comparison; direct byte/text diagnostics
confirmed the issue was in the reviewer check. One diagnostic had a PowerShell
pipeline parse error before execution. Neither was a candidate test failure,
and no source was changed to obtain the final passing audit.

The separate post-CLEAN gate remains required: unchanged
`-m pontius.status_generation --check` and `tests/test_status_generation.py`
(12 tests) on 3.11.15 first, then 3.14.6, against this exact candidate and frozen
r002 overlay in fresh isolated D-local snapshots. The handoff assigns these
executions to the controller. This CLEAN review permits that ordered next gate;
it does not claim the new metadata's executable acceptance has already passed.
Exact per-commit authorization remains required after that gate.

Only reviewer-owned inventory, audit script and issued reports were written.
No source, candidate, packet, ledger or ref was edited; no dependency installed;
no commit, publication, push, subagent or operating/research run occurred.
