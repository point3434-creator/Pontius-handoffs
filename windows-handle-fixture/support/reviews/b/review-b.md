# Tier C cold implementation review B — windows-handle-fixture/r001

Candidate: `76309774b551a874b8f9c677bc59e51299cee0e4`

Base: `5e56e4454f7b8ccb360d3e36245abc33318349bb`

Tree: `f7d2451c20e417967864718b3d000a3eb60387e9`

Manifest SHA-256:
`755c34175c060a4f0ef55616c9e52e336989645763cb16c0fd5a26293a7a37a6`

Deferred coverage SHA-256:
`6c5ea08ff78251c40714f3d651fa9f2720d6a995ed4de99dadd5e0f1f281bb8e`

Receipt SHA-256:
`306274a2b5aa0fdeae88a7ec1fa1ec845b71427580191091f0e08d0836f3918c`

## Verdict

- Specification: **PASS**
- Engineering quality: **FAIL**
- C/I/M: **0/0/1**
- Defect verdict: **NOT CLEAN**
- Design verdict: **SOUND**

The controlled test-boundary token table is an appropriate bounded shape for
the controller's explicit rule-8 exception. It leaves the writer, cleanup
owners, native resources, namespace transitions, and raw native oracles real.
The sole finding is ordinary exactness debt and does not indicate a structural
defect.

## Finding

### Minor — five added lines violate the repository's 100-column limit

Confidence: high.

The frozen `tests/test_inventory_and_profiles.py` blob has five newly added
lines longer than 100 columns:

- line 21184: 107 columns
- line 21337: 104 columns
- line 21338: 103 columns
- line 21382: 101 columns
- line 21424: 106 columns

This violates `docs/workflow.md` checklist item 10 and the repository's stated
100-column style. It is non-behavioral, but it is a required correction and
therefore prevents a CLEAN verdict.

Required correction: wrap those five statements without changing behavior,
then regenerate only the mechanically consequent string-decoy expectation and
checked-in inventory bytes required by the source change.

Verification criterion: the successor frozen diff has no newly added line over
100 columns, remains LF-only/BOM-free/trailing-whitespace-free, preserves the
164-nonblank-line adapter within its 200-line budget, and reruns the affected
inventory/focused controls under the normal correction protocol.

## Specification evidence

### Frozen identity and scope

The ref resolves to the stated commit; its parent and tree match the handoff.
An independent blob-based recomputation produced exactly these rows:

```text
0b07a2ac105e6fce052f923322836b94a36a14d9c174b5d2cc085c7baa29664f  tests/test-inventory.json
3fc1ee4390383ec8a5eb389563fb6ef039ab349a9a2117c78b2b2c87b289a992  tests/test_inventory_and_profiles.py
```

Whole-row byte sorting and LF serialization recomputed manifest SHA-256
`755c34175c060a4f0ef55616c9e52e336989645763cb16c0fd5a26293a7a37a6`.
Only those two declared paths differ from the base; codec, analyzer, writer,
and secure-filesystem production bytes are unchanged.

### Blind inventory versus deferred coverage

Before opening `coverage.md`, I recorded the governing invariant, the four
replaced allocation loops, the 14 positive role/family cases, all translated
handle-bearing APIs, the CRT ownership-transfer exception, and the required
raw native oracle/teardown properties. The record is
`reviews/b/initial-inventory.md`, SHA-256
`a297601a35ad354f8eb4690742cd5d59c966a5c136d2a1a56a15d9072f530bcd`.

The deferred claim matches that inventory: five final3 roles, six round7
families, three round9 families, and four former `range(4096)` allocation
loops. A frozen-source search confirms those four handle-reuse loops are gone;
the remaining unrelated `range(4096)` is an analysis-cardinality fixture.
No affected member or materially distinct handle-bearing call was omitted.

The coverage claim refers to a retained native-only same-token RED observation
that is not itself a candidate test. I did not use that external claim as pass
evidence. The candidate's deterministic setup, real native controls, raw
oracles, mutation checks, and fresh executions independently establish the
requested behavior.

### API forwarding and CRT transfer

`CreateFileW` tokenizes only calls with `FILE_FLAG_BACKUP_SEMANTICS`; the
ordinary no-follow path read remains a native handle and transfers directly to
`msvcrt.open_osfhandle`. The checked-in control read exact replacement bytes
through `read_regular_snapshot` and exited with no adapter-owned handle.

`NtCreateFile` translates `OBJECT_ATTRIBUTES.RootDirectory` and publishes its
native output. `NtSetInformationFile` translates both the primary handle and
embedded rename/link root for information classes 10 and 11. Close, identity,
liveness, read, write, and flush calls translate their primary handle;
`ReplaceFileW` is correctly forwarded unchanged. Function `argtypes` and
`restype` assignments are forwarded to the original ctypes functions.

My additional probe compared a failing raw and routed `CreateFileW` call and
observed the same nonzero last-error in both interpreters. It also confirmed
that a retired token reaches Windows only as invalid handle zero and preserves
`ERROR_INVALID_HANDLE`, while an unknown synthetic-range value refuses before
dispatch without changing the thread's last-error value.

### Ownership, collisions, and lifecycle

Every successful tokenized native acquisition becomes exactly one live table
entry. Publication validates the native/token range, moves ownership on reuse,
and retires a token only after a successful native close. Issued-but-retired
tokens cannot fall through as native handles. The checked-in failure control
exercised publication failure after real directory `CreateFileW` and
`NtCreateFile` acquisitions and observed both acquired native handles closed.

The positive writer schedules use real acquisition, I/O, identity,
disposition, close, rollback, and namespace work for every governed role and
family. Replacement handles are captured at reassignment, and both liveness
and full-width file identity are checked using pre-facade native functions.

### Error/refusal preservation and teardown

Native Win32 returns and last-error values are not fabricated. NTSTATUS and
I/O status blocks remain native. Closed-token and unknown-token behavior fails
closed. The checked-in teardown control verifies facade restoration, fallback
closure, leak detection after both normal and exceptional bodies, and retention
of the body exception as cause.

My additional raw-close-failure schedule left a real adapter-owned directory
handle live, forced fallback `CloseHandle` to return false, and observed:

- teardown failed rather than declaring cleanup success;
- the original `ValueError` remained the `AssertionError` cause;
- the private module's ctypes binding was restored;
- the ownership entry remained available for explicit native cleanup.

The probe then raw-closed the captured native handle, so it introduced no
resource leak.

### Independent oracle and mutation truthfulness

The native oracle captures the original `GetHandleInformation`,
`GetFileInformationByHandleEx`, and `CloseHandle` functions before installing
the facade. Assertions query the captured native HANDLE directly and compare
its recorded full-width identity; table state and routed production liveness
cannot satisfy them.

Four mutation rows deliberately replay production cleanup through the real
writer path: each of the three governed helpers through
`_WindowsGovernanceFileOwner`, plus final3 directory ownership through
`_WindowsHandleOwner`. The replay actually closes the replacement; raw native
queries observe it closed, and the helper fails with `native replacement was
closed`. These controls passed on both interpreters. The per-case positive raw
survival assertion remains present across the complete 14-case population.

## Execution evidence

All executions used unique fresh no-hardlink D:-local snapshots, overlay
`packets/r001/files`, `python -B -P`, snapshot-root cwd, scrubbed environment,
snapshot `PYTHONPATH`, and absolute regular/non-reparse
`C:\Program Files\Git\cmd\git.exe` via `PONTIUS_GIT`. The runner separately
asserted module resolution and exact interpreter identity before each payload.

- `review-b-focused-controls-311`: 4 tests, PASS in 1.474s on CPython 3.11.15.
- `review-b-focused-controls-314`: 4 tests, PASS in 2.929s on CPython 3.14.6.
- `review-b-full-inventory-311`: 91 tests attempted; one sandbox-only
  `os.link` received `WinError 5`. This run is retained as environment-limited,
  not green.
- `review-b-full-inventory-escalated-311`: 91 tests, PASS in 131.254s with the
  required hardlink permission.
- `review-b-adversarial-api-311`: PASS on CPython 3.11.15.
- `review-b-adversarial-api-314`: PASS on CPython 3.14.6.

The exact argv, stdout, stderr, snapshot, interpreter, and exit code for each
run are bound by `reviews/b/receipt.json`; that receipt also records the SHA-256
of every raw runner record.

## Quality and limits

Both changed blobs are LF-only, BOM-free, and have no trailing whitespace. The
adapter is 164 nonblank lines against the 200-line cap and parses under the
supported floor. Aside from the five E501 lines, I found no maintainability,
scope, oracle-independence, cleanup, or test-truthfulness defect.

I did not modify candidate/source/test/generated bytes, run the 19-command
broad acceptance population, or run a second full inventory suite on 3.14.
Those broad gates remain with the controller after both Tier C reviews are
CLEAN. I did not inspect implementation narratives or another implementation
reviewer's report.
