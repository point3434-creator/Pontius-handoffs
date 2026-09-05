# Cold review B: v0a-driver/r001

Verdict: CLEAN. Specification: PASS. Engineering quality: PASS. Design: SOUND.
Findings: 0 Critical, 0 Important, 0 Minor. No required correction remains.

## Identity and independence

- Candidate: bdd96aa24286ba1ebcc11bfdbe7d3480fa3f4ad2.
- Manifest: b085c3cba799a6563b5a9b9ba8a6b274b1f7d013079ea32cae769118c69d0c9f.
- Base: af90155ebd970d0be6fe26969b121bd213a7f1f2.
- Tree: 957abe2f662395f9a00603a369444719b249ecc1.
- Handoff SHA-256: 68d9c0bdcc5bb83773801c64444a582dd02e054e4d2a4852778223224c5f1626.
- Brief SHA-256: e063655705946d6931ec4e9bcd1b22ffc404e51e1d1cd26ffaa0c1085ae2a7c7.

Reviewer B had no prior participation and received the pinned handoff before
inspection. Inputs were the handoff, candidate.json, manifest.sha256, brief.md,
three added candidate files, frozen CLAUDE.md and workflow checklist v1,
ADR-0485/0487, and relevant sealed ReplayHost/reader interfaces. No implementer
transcript, build report, other review, or prior command receipts were consulted.
No delegation occurred.

Independently reconstructed whole-row byte-sorted LF manifest rows from frozen
Git blobs using diff-tree with --no-renames and cat-file. Verified exact parent,
tree and candidate, exactly three additions, no inherited modifications, and
checkout equality to each added blob. Before/after verification passed on both
successful interpreter runs, including clean snapshot Git status. Added files
are LF-only, BOM-free, have no trailing whitespace and satisfy 100-column hygiene.
Driver has 174 lines, tests 172, documentation 61: both code budgets are met.

## Contract-to-evidence assessment

| Contract or risk | Evidence and result |
| --- | --- |
| Fixed controls and identities | Both controls execute the actual CLI and native publication on both slots; expected payouts are A [0,0,0,12,0,0] and B [16,10,24,30,0,0]. Invalid mode, namespace and unsafe suffix refuse. |
| Root admission and retention | Wrong/missing roots refuse, existing trace bytes remain unchanged. validate_run checks absolute local path, exact basename, each ancestor's non-reparse directory status and emptiness before the host. |
| Pre-import provenance | Sealed tree read by one Git archive invocation; complete package-file comparison rejects changed source and extra native extension in supplied tests. Independent checks reject missing startup flags, a preloaded pontius submodule, an extra .pyc, and a wrong bindings pin. |
| Actual manifest identity | Independent ls-tree enumeration and actual-file SHA-256 rows reproduce c08b8ca1b495b887cdcc7a27fb0c7ee5caa45590b664cf999c44b3d797e17499; real trace header matches on both slots. Preserved payload manifest is separately reported. |
| Sealed host boundary | main passes fixed fixture, empty reference blueprint, supplied validated mode/run ID, actual seal, computed manifest and monotonic_ns; run receives destination='trace.jsonl' and admitted root. Default host clock remains real. |
| Acceptance and readback | Actual CLI controls pass host completion, persisted/in-memory byte equality, digest equality and independent replay. Supplied negative seam checks reject incomplete host, readback corruption, and invalid replay despite matching hashes. |
| Independent expected bindings | Additional checks using a real persisted control-B outcome reject wrong manifest, wrong fixture, wrong requested ID, wrong receipt ID, wrong receipt digest and failed accounting. Every rejection preserves saved bytes. |
| Claims and size | Usage document states trusted startup/no concurrent writers, no sandbox/global identity registry, non-evidentiary stdout and separate rehearsal authorization. Thin adapter does not create a replacement ownership framework or alter sealed source. |

The shape is SOUND: a small preflight and fixed CLI selection delegate execution
and native publication to the sealed host, then make persisted-byte identity and
the independent reader necessary for success. Source validation checks bytes
before package imports under the brief's stated trust model. Receipt acceptance
does not mistake independent semantic replay for host finalization.

## Fresh commands and results

Exclusive scratch: D:/Pontius/tmp/v0a-driver-cold-b.
Both snapshots used `git -c core.autocrlf=false clone --no-hardlinks --no-checkout`
from D:/Pontius, followed by `git -c core.autocrlf=false checkout --detach`
at the exact candidate. Clone/checkout commands succeeded.

The retained run_slot.ps1 scrubs all PYTHON*, GIT_* and PONTIUS_* environment
variables, sets PYTHONNOUSERSITE=1, PYTHONPATH=<snapshot>/src, absolute
PONTIUS_GIT=C:/Program Files/Git/cmd/git.exe and exclusive D-local TEMP/TMP/TMPDIR.
It sets cwd to the snapshot, prints executable/implementation/full version and
flags before payload import, then invokes every Python command with -B -P.

1. Floor command:
   `run_slot.ps1 -Python D:/Pontius-tools/py311/Scripts/python.exe -Slot 311`.
   Snapshot: scratch/snapshot. CPython 3.11.15, MSC v.1944, AMD64. Exit 0.
   Identity check: PASS; `tests/test_v0a_rehearsal_driver.py -v`: 12 tests, OK,
   4.459s; `falsifiers.py`: 5 tests, OK, 0.929s; final identity check: PASS.
2. First 3.14 command in sandbox: exit 1 before interpreter identity or payload
   execution, launcher access denied. Classified as environment refusal.
3. Approved normal-user retry of that command: CPython 3.14.6 identity printed,
   then exit 1 during identity precheck, before tests. Explicit Git diagnostic
   returned exit 1 and identified dubious ownership: sandbox-owned clone versus
   normal user. No global Git trust configuration was changed.
4. Fresh no-hardlink detached normal-user clone: scratch/snapshot314, exit 0.
   Command: `run_slot.ps1 -Python D:/Pontius/.venv/Scripts/python.exe -Slot 314
   -Snapshot D:/Pontius/tmp/v0a-driver-cold-b/snapshot314` under approved normal-user
   permissions. CPython 3.14.6, MSC v.1944, AMD64. Exit 0. Identity check: PASS;
   focused suite: 12 tests, OK, 4.631s; falsifiers: 5 tests, OK, 0.984s; final
   identity check: PASS. No product-test failure was retried.

Total successful bounded verification: 24 supplied tests and 10 independent
test methods across the two slots, with additional subcases inside those methods.
No skips. This is not a broad-suite or whole-core acceptance result.

Retained independent real-host trace artifacts:

- 3.11: scratch/pontius-v0a-hand-replay-v1-correctness-coldb-real-edbf74579b1f41e695c113a37eb515ae/trace.jsonl;
  SHA-256 49fcd57f33ce8b2078beecee06990f65fb438a57e5b4bf752551805385c182d1.
- 3.14: scratch/pontius-v0a-hand-replay-v1-correctness-coldb-real-c57b2766009740a8a0d7a4e2a103607b/trace.jsonl;
  SHA-256 b830cc48e8b5fc7d999437667d6a8d0e8f782d332b7dfe9bc9600bc897aafcc9.

Here scratch means the exclusive absolute scratch directory named above.
Probe scripts verify_identity.py, falsifiers.py and run_slot.ps1 are retained there.

## Limits and scope discipline

The source-pin override and altered receipt objects exercise only source/acceptance
boundaries. They prove no native ownership, close-once or failure-transaction
property. Both actual CLI control cases and the retained extra host case exercise
real successful Windows publication. No new claim is made about sealed writer
fault schedules or the inherited Windows handle-reuse fixture caveat. That core
was not re-audited; the additive driver introduces no native owner.

The four unchanged neighboring v0a suites and broader gates were not rerun under
this bounded review assignment. Arbitrary/hostile startup, hostile concurrent
filesystem mutation, exhaustive Python import reachability, global run-ID
uniqueness and rehearsal execution are not covered or asserted.

All host executions used correctness identities. Mode rejection occurred before
host invocation. Supplied tests temporarily inject faults only in disposable
snapshots and restore bytes; independent cache injection is also removed there.
Final snapshots remain byte-identical and clean. No primary source, Git index,
HEAD, sealed file, owner, journal, consumed identity or retained result was changed.
No fixes, installs, broad sweep, GPU work, training, commits or pushes occurred.
This review does not authorize adoption, a rehearsal, or an operational invocation.
