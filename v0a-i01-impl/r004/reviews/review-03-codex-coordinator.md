# r004 coordinator review

Reviewer: Codex /root, 2026-08-30. Additional verification, not a cold pass.
Defect verdict: NOT CLEAN — one Important residual of R3-02.
Design verdict: STRAINED at receipt projection; retain the corrected runtime
cause collection and replace the category-based projection with chronological
first/rest semantics. No whole-host rewrite is justified by this evidence.

Candidate: 0207430a37e1e5b31c8da8da7aa57da1bc5c88ee
Ref: refs/heads/review/v0a-i01-impl/r004
Manifest SHA-256: ab28f8dfbe412849c2db2a015b7c40f0549d733a61f6e19295de02dccede06ef
Base: b357d333fc2393b7fc7dcf31f30c86616208c817
Tree: c5cf6cc281d2800727029737fd4ee05bd20ebbd3

FIX scope: R3-02 host typed causes and their occurrence order only. Policy and
deferred R2-04/05/06/09/10 remain excluded. The separate value-boundary audit
does not add requirements to this candidate.

## C-01 — Important: primary selection discards the first reporting cause

Confidence: high; deterministic on both required interpreters.
Frozen location: src/pontius/v0a/replay.py:432-448 (split), :595-607 (write
failure collection followed by publication exit/finalization and final split).
Requirement: frozen ADR-0485:269-280, especially later ordered secondary codes,
retention of the primary typed cause, and host success requiring publication
and finalization.

The host collects actual causes in order, then split() removes every
TRACE_WRITE_FAILED from eligibility for primary. That changes chronology into
an undocumented category priority. A successful hand is not successful host
completion: publication itself is a required host operation.

Real production path: ReplayHost(FIXTURE_A) with the normal immutable policy
and a monotone public clock, asking the real writer to write README.md under
the snapshot run root. That file already exists; the real create-new writer
refuses without modifying it. No writer double or private mutation is used.

Observed receipts:

| Schedule | Actual receipt | Required first/later causes |
| --- | --- | --- |
| Existing destination only | passed=false; primary=null; secondary=[trace_write_failed] | primary=trace_write_failed; secondary=[] |
| Earlier clock fault at observation 134, 135 or 136, then existing destination | primary=clock_invalid; secondary=[trace_write_failed] | Same; opposing controls pass |
| Existing destination, then clock fault at publication exit (137) | primary=clock_invalid; secondary=[trace_write_failed] | primary=trace_write_failed; secondary=[clock_invalid] |
| Existing destination, then clock fault at finalization (138) | primary=clock_invalid; secondary=[trace_write_failed] | primary=trace_write_failed; secondary=[clock_invalid] |

All schedules retain four accepted actions and four decision records. Failed
clocks are not resampled; the writer leaves the snapshot clean. The issue is
receipt meaning and chronology, not lost delivery or false success.

The handoff explicitly requests judgment on keeping even a lone trace failure
secondary. That interpretation is not supported by the frozen contract:
secondary_failures describes later codes and preserves a reporting failure
without replacing an existing first cause. When no earlier cause exists, a
write failure is the first host failure. A subsequent clock failure cannot
become first merely because it is not a reporting code.

Required outcome: failure_reason is the first observed typed host failure,
regardless of its category; secondary_failures contains exactly the subsequent
causes in order. Success has no causes. Preserve known delivery and no-resample.

Advisory correction: keep the runtime's exception-derived typed retention and
host drain-before-note mechanism. Make receipt projection a single first/rest
operation on the ordered collection, with no enum-specific priority. This
removes the special case instead of adding another flush or precedence branch.

Verification must include no faults, each single cause including real trace
refusal, both clock/write orders, mismatch/clock order controls, and repeated
code occurrences without deduplication. Test the public final receipt from the
real host; a helper-only ordering test is supplementary.

## Verified improvements

Both required interpreter slots pass the four existing focused suites:
35 hand replay + 25 trace + 31 replay + 22 contract faults = 113 per slot.

The coordinator also enumerated all observations of fixtures A and B:
138 and 72 normal clock reads respectively. Invalid values and raising sources
cover observations 1..N; reversals cover 2..N, because a reversal needs a prior
accepted sample. This is 628 fault schedules per interpreter, plus two normal
controls. Every fault returns a non-null primary, forbids success, preserves
accepted-action/decision counts and never calls the underlying clock after
its failing observation. No exception escapes this matrix.

The five swallowed clock seams from r003 are therefore closed by the inspected
mechanism and these schedules. This evidence does not erase C-01: the matrix
alone does not combine a real write failure with the later clock observations.

The RuntimeError branch marks accounting incomplete without inventing a code.
No legitimate first-fault path for that branch was established. A fabricated
private-ledger state is not used to claim an additional defect.

## Design and scope judgment

STRAINED is local to the current split between an ordered cause collection and
a category-sensitive receipt projection. The collection already holds the
needed truth; discarding it at the last step invites this recurrence. Removing
that projection exception is a bounded simplification with low transition risk,
not a reason to replace the runtime, ledger or host architecture. Preserve the
five catch sites, existing clock-death guards, real delivery and sealed APIs.

The explicit ADR wording is sufficient; no requirement amendment is necessary
to fix this candidate. If different host semantics are desired, they require
a separate contract decision rather than silently changing this fix round.

## Evidence and limits

checks/coordinator-probe.py and checks/coordinator-run.py retain commands and
observations. checks/coordinator-311-receipt.json and coordinator-314-receipt.json
record log hashes, snapshot, command arrays, environments and exits.
Probe logs include six real writer-refusal schedules: one write-only plus the
five closure positions. They are the six real_trace_refusal rows in each log.

Execution was actual CPython 3.11.15 first, then 3.14.6; -B -P, fresh disposable
snapshot cwd, src PYTHONPATH, scrubbed environment and absolute PONTIUS_GIT.
Exact executable, full version and implementation were asserted before imports,
including for existing test payloads. Source stayed Git-clean before/after.
Manifest and ten frozen blobs verify; only runtime, replay and replay tests
differ from r003. No production/test/config edits, broad suites, GPU runs,
experiments or acceptance/performance claims.
