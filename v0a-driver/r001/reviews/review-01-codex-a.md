# Cold review A: v0a-driver/r001

Issued 2026-09-04. NEW-SURFACE, Tier C. Independent Codex reviewer A.

**Defect verdict: CLEAN. Specification: PASS. Engineering quality: PASS.
Design verdict: SOUND.** No Critical, Important, or Minor findings; no required
correction. This is a bounded driver review, not adoption or execution authority.

## Binding and cold scope

- Candidate: `bdd96aa24286ba1ebcc11bfdbe7d3480fa3f4ad2`.
- Base/seal: `af90155ebd970d0be6fe26969b121bd213a7f1f2`.
- Candidate tree: `957abe2f662395f9a00603a369444719b249ecc1`.
- Manifest SHA-256: `b085c3cba799a6563b5a9b9ba8a6b274b1f7d013079ea32cae769118c69d0c9f`.
- Handoff SHA-256: `68d9c0bdcc5bb83773801c64444a582dd02e054e4d2a4852778223224c5f1626`.
- Exclusive scratch: `D:/Pontius/tmp/v0a-driver-cold-a`.
- Snapshot: `D:/Pontius/tmp/v0a-driver-cold-a/snapshot`.

I read the handoff, candidate JSON, manifest, brief, frozen CLAUDE.md and
workflow/checklist v1, ADR-0485/0487, all three added files, and the relevant
sealed host/reader interfaces. I did not read another review, progress file,
implementer narrative, build report, or prior test receipts. No delegation.

Independent `git diff-tree --no-renames`, frozen `git cat-file blob`, and
whole-row byte sorting recomputed the manifest exactly. The delta contains
exactly three additions, no inherited modification/deletion/type change:

| File | Lines | Frozen SHA-256 |
| --- | ---: | --- |
| tools/v0a_rehearsal_driver.py | 174 | 4c91cad6b0e3ce296de656f4193b346967feca9bb769941ecb24c2903c9f16f3 |
| tests/test_v0a_rehearsal_driver.py | 172 | 89dd22ba2700b347b4745c60d099415e17b960988506eba5ab7f70e5b14fed57 |
| docs/architecture/v0a-rehearsal-driver-r001.md | 61 | 2397045c2ea71070a3d65df908da84618de6c7f5550b01f4da811cdc044c6e57 |

Checkout equality to these blobs, clean Git status, LF/no BOM/no trailing
whitespace and the 100-column ceiling passed before and after the runs. The
driver/test size budgets pass.

## Requirement and evidence matrix

| Requirement or risk | Evidence and conclusion |
| --- | --- |
| Explicit fixture/mode/run identity and root admission | Full CLI suite checks both controls, forbidden authorized mode, rehearsal-mode/correctness-ID mismatch, unsafe suffixes, missing/wrong root, existing trace. Invalid paths stop before host execution. PASS. |
| Pre-import source provenance | Read lines 54-109; pinned Git archive, exact package-set/byte comparison, bindings digest, reparse checks, no preloaded pontius, required -B/-P. Changed source/native extension tests and independent bytecode/startup/preloaded controls refuse. PASS within declared trusted-startup/no-concurrent-writer scope. |
| Actual manifest and separate payload identity | Independently built whole-row manifest from LF-pinned sealed archive plus frozen bindings/overlay blobs; real control-B receipt and trace header match c08b8ca1b495b887cdcc7a27fb0c7ee5caa45590b664cf999c44b3d797e17499 on both interpreters. Preserved payload identity remains separately reported. PASS. |
| Sealed host/publication and real clock | Full suite executes both actual CLI controls using sealed ReplayHost.run and native Windows writer; source inspection confirms fixed trace.jsonl, empty blueprint, supplied mode and default clock with monotonic_ns declaration. PASS. |
| Host completion plus saved-byte replay | Read lines 112-170 against actual host receipt and verifier interfaces. Tests reject failed/incomplete host receipts, readback corruption and malformed independently replayed content. Independent probes reject wrong expected manifest, requested ID, host receipt ID and integer 1 in either boolean success field. PASS. |
| Retention and no root reuse | Existing-trace test preserves sentinel bytes; independent real published trace is byte-identical after reattempt is refused at ROOT before host. No driver cleanup/retry path. PASS. |
| Scope and documentation | Three-file additive adapter, no CLI identity/schedule override, no new owner/journal or library changes; usage accurately describes trusted assumptions and non-evidentiary status. PASS. |

The shape is SOUND because a small adapter enforces startup/admission and final
acceptance while the existing host, writer and independent reader retain their
responsibilities. No parallel ownership framework or duplicated replay engine
has been introduced. The declared startup trust and absence of concurrent
writers are material assumptions, explicitly stated rather than inferred.

## Fresh commands and outcomes

Clone, exit 0:

```text
C:/Program Files/Git/cmd/git.exe -c core.autocrlf=false clone --no-hardlinks --no-checkout D:/Pontius D:/Pontius/tmp/v0a-driver-cold-a/snapshot
C:/Program Files/Git/cmd/git.exe -C D:/Pontius/tmp/v0a-driver-cold-a/snapshot -c core.autocrlf=false checkout --detach bdd96aa24286ba1ebcc11bfdbe7d3480fa3f4ad2
```

All required payload runs used normal-user escalation from the initial attempt,
snapshot cwd, `-B -P`, snapshot/src PYTHONPATH, PYTHONNOUSERSITE=1, scrubbed
PYTHON/GIT_/PONTIUS_ variables, absolute PONTIUS_GIT, and scratch D-local
TEMP/TMP/TMPDIR. The complete reproducible wrappers and probes are retained
under the exclusive scratch root. No dependency install or safe.directory edit.

| Command (PowerShell wrapper in scratch) | Interpreter | Exit and result |
| --- | --- | --- |
| run-slot.ps1 -Interpreter D:/Pontius-tools/py311/Scripts/python.exe -Slot 311 | CPython 3.11.15, MSC v.1944 AMD64 | 0; identity check, all 12 tests, identity recheck; 4.257s suite |
| run-slot.ps1 -Interpreter D:/Pontius/.venv/Scripts/python.exe -Slot 314 | CPython 3.14.6, MSC v.1944 AMD64 | 0; identity check, all 12 tests, identity recheck; 3.024s suite |
| run-falsifiers.ps1 -Interpreter D:/Pontius-tools/py311/Scripts/python.exe -Slot 311 | CPython 3.11.15 | Initial exit 1: reviewer probe error described below; corrected exit 0, all independent probes and identity recheck pass |
| run-falsifiers.ps1 -Interpreter D:/Pontius/.venv/Scripts/python.exe -Slot 314 | CPython 3.14.6 | 0; all independent probes and identity recheck pass |

The suite command in each run-slot wrapper is
`<interpreter> -B -P tests/test_v0a_rehearsal_driver.py -v`. Independent probe
commands are `<interpreter> -B -P D:/Pontius/tmp/v0a-driver-cold-a/falsifiers.py`;
the wrapper subsequently runs `check_identity.py` with the same flags.

Probe failure classification: my initial independent archive command omitted
`-c core.autocrlf=false`, producing Git archive newline conversion and a different
oracle manifest. This was a reviewer harness defect, not a candidate defect.
The diagnostic compared archive and checkout hashes; correcting that omitted
flag produced the actual header manifest on both slots. Only scratch probe
code changed. The initial trace and subsequent traces remain in scratch; no
failed command was silently relabeled. Every host invocation used a new
correctness identity. Root-reattempt and mode-rejection checks stop before host.

## Limits and disposition

Acceptance-object doubles establish rejection logic only. They do not prove
native ownership under injected close/write failures. Native happy publication
was exercised through the real CLI for both fixtures; the sealed native failure
contracts are inherited, not re-audited by this thin-driver review. Four unchanged
neighbor suites and broader acceptance remain the finalizer's gate; they were
not rerun here. This review makes no arbitrary dynamic-import proof, hostile
mutation defense, global run-ID registry, timing distribution or strength claim.

No candidate fix, source change, commit, push, successful rehearsal-mode run,
owner invocation, consumed identity, GPU operation or policy training occurred.
The existing suite's temporary source fault injection restored exact snapshot
bytes; the independent cache contaminant was removed after its rejection check.
Primary checkout/index/HEAD and frozen packet inputs were not modified.

Bounded disposition: CLEAN / Spec PASS / Quality PASS / SOUND for the identity
pair above. No required correction remains. Separate controller adoption and
execution authorization are still required by the packet and ADR-0487.
