# Independent cold review B: v0a-i01-impl/r003

Verdict: **NOT CLEAN**. Two Important findings survive direct reproduction.
Specification: FAIL. Engineering correctness: FAIL for the two contracts below.
Confidence: high. Reviewer: Codex B. Date: 2026-08-30. Finalizer: Claude.

## Identity and scope

- Ref: `refs/heads/review/v0a-i01-impl/r003`
- Commit: `47d08d8c1556d776358e15811e3e98b859fd6a8b`
- Manifest SHA-256:
  `cc255e28680f71fe15de78f26bb8f99a337c1c79e12bf3bdf382a8aa74e7844a`
- Base: `b357d333fc2393b7fc7dcf31f30c86616208c817`
- Tree: `35a6667ca3785e750324b3c93103a8994a6d7d6a`
- FIX round, slice 1 only: R2-01, R2-02, R2-03, R2-07, R2-08.

All source locations below refer to that frozen commit, not current working files.
Inputs were the current CLAUDE.md and docs/workflow.md, frozen ADR-0485 and
`docs/briefs/v0a-increment-1-brief.md`, and this round's handoff, candidate, and
manifest. No chats, self-report files, prior reviews/dispositions, or another
reviewer's findings were consulted. Only the handoff's explicit contracts were
used as requirements; its evidence claims were not accepted as proof.

I independently recomputed all ten changed-path rows from `git cat-file blob`,
with rename detection disabled and whole-row byte sorting. The resulting row
bytes equal `manifest.sha256` exactly, and its digest equals the binding above.
The candidate ref still resolved to the bound commit after diagnostics. The
assigned disposable clone remained Git-clean; no source, test, or config changed.

## B1 - Important / high severity: accepted subclasses can still falsify policy authority

Contract: R2-01, immutable policy authority. **Residual against this handoff.**
Confidence: high; reproduced on both supported interpreter slots.

Frozen locations:

- `src/pontius/v0a/runtime.py:177-184` admits subclasses using `isinstance`.
- `src/pontius/v0a/runtime.py:90-96` calls only `action_for` non-virtually.
- `src/pontius/v0a/runtime.py:462-468` binds the source's dynamically reported digest.
- `src/pontius/v0a/runtime.py:844-881` accepts that same reported selection digest.
- Existing dependency `src/pontius/immutable_blueprint.py:345-346,360-374`
  computes `self.digest` through `self.canonical_bytes()` while reading `self.entries`.

Reproduction: derive Fixture A's first exact legal decision key using its public
betting state and controlled private cards. Construct an
`ImmutableBlueprintActionSource` subclass whose inherited `entries` contains that
key mapped to legal `raise_to(6)`. Override **only** `canonical_bytes()` to return
an honest empty source's canonical bytes. Pass it to real `HandRuntime` and real
`ActionMailbox`, then dispatch the real `HandStartedEvent`. No monkeypatch,
introspection, private mutation, or substituted selection helper is used.

Observed outcome: `status='decided'`, `selected_action=raise_to(6)`,
`selection_reason='table_hit'`, and one real mailbox acceptance. The emitted record's
blueprint digest equals the honest empty table's digest:

`fa84d6dfca78af45e18a50d1f9745ebb4224b20d69eda1f8e85eeead397ae4a9`

The sealed base implementation's canonical bytes for the actual entries hash to:

`0aeceef3967fe8afa22ad6f6770331afff5159fd20cc950aba3fba37f917ad24`

The supposedly bound empty policy would call, not produce this table hit and raise.
Bypassing the `action_for` override leaves the identity dependency overridable, so
an admitted policy can emit another table's action under the bound digest. This is
the exact false-authority contract; it does not demand a sandbox against malicious
Python introspection.

Smallest correction: require the exact sealed concrete source at admission and at
selection, or construct and bind an exact validated immutable source whose data and
canonical identity cannot dispatch through subclass overrides. Protect the complete
identity dependency, not only `action_for`. Do not edit the sealed dependency or add
a second full-table hash per decision. Add a public-boundary regression for this
canonical-identity override as well as the existing action override probe.

Evidence: `checks/cold-b-contract-probe.py`, `canonical_subclass` output in both
`checks/cold-b-contract-probe-311.jsonl` and `checks/cold-b-contract-probe-314.jsonl`.

## B2 - Important / medium severity: late clock faults lose the typed primary cause

Contract: R2-03, host failure closure and truthful result/cause retention.
**Residual against this handoff.** Confidence: high; reproduced on both slots.

Frozen locations:

- `src/pontius/v0a/runtime.py:286-300`: bookkeeping catches erase the fault type.
- `src/pontius/v0a/runtime.py:319-333`: publication catches do the same.
- `src/pontius/v0a/runtime.py:358-367`: finalization preserves only incomplete state.
- `src/pontius/v0a/replay.py:496-522,571-585`: no clock cause reaches the host's
  primary/secondary failure collection.
- Governing ADR-0485:269-279 and 402-441 require typed failure, ordered later
  failures, and retention of the first cause throughout host completion.

Reproduction: run the real `ReplayHost(FIXTURE_A, ...)` with the real mailbox and
independent oracle. The deterministic witness returns `read_number * 1_000_000`
until one specified read raises `ValueError`. The fault-free lifecycle makes 138
observations. Fault each observation independently, with a fresh host for each.

The five final positions are:

| Read | Real operation | Returned receipt |
| --- | --- | --- |
| 134 | Settlement bookkeeping opens | Failed, no typed cause |
| 135 | Settlement bookkeeping closes | Failed, no typed cause |
| 136 | Terminal publication interval opens | Failed, no typed cause |
| 137 | Terminal publication interval closes | Failed, no typed cause |
| 138 | Outer finalization | Failed, no typed cause |

Each returns `passed=false`, `accounting_complete=false`, `failure_reason=null`,
`secondary_failures=()`, and no failure records. Returning a reversed sample at each
of these same positions also discards `clock_reversed`. No later source observation
is made, so the refusal to drive the failed witness works; the lost cause is the
remaining defect. This report does not re-raise deferred trace/publication design
or accounting-total defects.

Cause ordering also fails concretely: inject the fault at bookkeeping open (134)
and use the explicitly admitted oracle seam to return different final stacks.
The host executes the later verification and reports `settlement_mismatch` as primary;
the earlier `clock_invalid` is absent. With the mismatch first and the clock fault
at publication open (136), the mismatch stays primary but the later clock fault is
missing from secondary failures.

Consequence: the host correctly refuses success but cannot identify the first
failure, distinguish an invalid clock from a reversal, or retain later clock faults.
This violates the typed host closure contract even when a completed terminal row
already exists. It also permits a later diagnostic result to become the apparent
first cause.

Smallest correction: retain the first typed runtime accounting fault as a public
failure value, communicate it to the host at each lifecycle boundary, and append
subsequent typed faults without replacing the primary. Keep the current dead-clock
and no-success guards. Verify bookkeeping entry/exit, publication entry/exit, and
finalization under invalid/reversed clocks, including an earlier and a later
independent failure; require typed causes as well as `passed=false`.

Evidence: the complete 138-position `clock_fault_sweep` and five `late_reverse`
records in `checks/cold-b-contract-probe-{311,314}.jsonl`; `clock_before_mismatch`
and `clock_after_mismatch` in `checks/cold-b-boundary-probe-{311,314}.jsonl`.

## Contract coverage and opposing evidence

| Contract | Evidence | Result |
| --- | --- | --- |
| R2-01 | Existing delegates rejected; canonical-subclass public reproduction | FAIL: B1 |
| R2-02 | Boundary, ready cutoff, postaccept interrupted flags; existing suite | PASS in scope |
| R2-03 | All 138 fault positions reject success and do not escape; late causes lost | FAIL: B2 |
| R2-07 | Both fixtures; conserving final-stack-only and eligibility-only mismatches | PASS in scope |
| R2-08 | Real late acceptance; mailbox/runtime/terminal counts across full sweep | PASS in scope |

The R2-02 probes retain `cutoff=true, deadline=true` after a boundary-established
16-second observation and after an accepted action's final timing fails. The
ready-cutoff-only case retains `cutoff=true, deadline=null`; unknown is not false.
The R2-07 stack probe moves one chip between final stacks without changing their
sum, so conservation alone cannot satisfy it. Both it and the eligibility-only
probe return `settlement_mismatch`. The R2-08 delayed real acknowledgement yields
one actual acceptance, one runtime acceptance, and terminal `decision_count=1`
while correctly failing with `action_deadline_exceeded`.

The coordinator's objective fresh-clone focused logs were inspected independently:
35 hand-replay + 25 trace + 25 replay + 22 contract-fault tests = 107 passing tests
per interpreter, all eight suite exits zero. Receipts are
`checks/codex-py311-verification.json` and `checks/codex-py314-verification.json`;
raw logs are the corresponding `codex-py311-*.txt` and `codex-py314-*.txt` files.
Those green tests do not cover the canonical identity override. The late host-fault
test checks `passed=false` but does not require a typed cause at its final positions.

## Execution and limits

Diagnostic commands, in this order, all exited zero:

1. `D:/Pontius-tools/py311/Scripts/python.exe -B -P`
   `D:/Pontius-handoffs/v0a-i01-impl/r003/checks/cold-b-contract-probe.py 311`
2. `D:/Pontius/.venv/Scripts/python.exe -B -P`
   `D:/Pontius-handoffs/v0a-i01-impl/r003/checks/cold-b-contract-probe.py 314`
3. `D:/Pontius-tools/py311/Scripts/python.exe -B -P`
   `D:/Pontius-handoffs/v0a-i01-impl/r003/checks/cold-b-boundary-probe.py 311`
4. `D:/Pontius/.venv/Scripts/python.exe -B -P`
   `D:/Pontius-handoffs/v0a-i01-impl/r003/checks/cold-b-boundary-probe.py 314`

Snapshot cwd:
`D:/pontius-snapshots/v0a-i01-r003-f7c260aed2044b2280e1cedd64516064/harness`

PYTHONPATH was that snapshot's `src` directory. Each child received a cleared
environment with only COMSPEC, NUMBER_OF_PROCESSORS, SYSTEMROOT, TEMP, TMP, WINDIR,
PYTHONPATH, and absolute `PONTIUS_GIT=C:/Program Files/Git/cmd/git.exe`.
Each script recorded and asserted the exact executable, CPython implementation,
full version, version tuple, cwd, and PYTHONPATH before importing payload modules.
The actual versions were CPython 3.11.15 and 3.14.6, not labels inferred from paths.
Imports resolved to the assigned snapshot; CuPy and Torch remained absent. Payload
execution never ran in the primary checkout. Snapshot ownership required the
approved external-root execution context; no Git safety configuration was changed.

Script SHA-256 values:

- `cold-b-contract-probe.py`:
  `692a0d3417d7e7a8f47d64b894b2aa3fb9bccbb6cf3242d56a37c4b0f746059b`
- `cold-b-boundary-probe.py`:
  `4f66752b86915f1f41085b3e8f15c827a8ad0883dcc7ddf61181dbfb8e80dc1a`

Largest remaining unknown: arbitrary combinations of failures beyond the bounded
schedules above; no exhaustive claim is made. Cheapest falsifying experiments are
the supplied deterministic public-boundary probes. Kill criterion: either admitted
policy substitution or lost typed host cause remains sufficient for NOT CLEAN.

Recommendation: reject this slice until B1 and B2 are closed in appropriately
scoped new immutable candidates. The coordinator applies historical residual counts
under the current workflow; this blind review does not infer those counts. No broad
suites, owners, GPU work, commits, or fixes were performed. Deferred slices 2 and 3,
admission/CI surface, and unchanged storage/trace defects were not re-raised.
