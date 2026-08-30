# Cold review A — v0a-i01-impl/r006

**Specification: FAIL — R2-03 remains open. Engineering: STRAINED.**
One Important finding survives independent verification. This verdict covers only
the FIX R2-03 change and does not reopen deferred work.

- Ref: `refs/heads/review/v0a-i01-impl/r006`
- Commit: `c74b80628a89938ca585ef3240b5c267a7174d0f`
- Manifest: `2078d59a4a112bf29a2bd9faca9a2ca070bbd1028a940f2eeb617c9e1c31555f`
- Comparison: r005 `a8582e6d6b53b55415dab79c4a54e252d00b74ad`

## R6-A01 — Important: rendering a caught exception escapes the new owner

High confidence; bounded adversarial trigger. At `runtime.py:416`, the new
`owned_bookkeeping` records the body cause, then executes
`OperationFailed(str(error))`. Exception arguments need not have a safe `__str__`.
If rendering raises, that second exception bypasses the owner's handler and
`replay.py:526`, which catches only `OperationFailed`. The identical conversion
also appears in `owned_publication` at `runtime.py:429`.

Reproduction uses the real `ReplayHost.run`, immutable blueprint, mailbox, ledgers,
and settlement path. A deterministic execution hook raises
`ValueError(message_object)` at the second real showdown-evaluation call, inside
owned settlement. `message_object.__str__` raises `RuntimeError`. Four actions
have already been accepted. r006 records `settlement_mismatch` internally but
lets `RuntimeError` escape and returns no `ReplayOutcome` or completion receipt.
This violates R2-03 containment and retained typed cause reporting.

Opposing controls: the same r006 path contains an ordinary `ValueError`; exact
r005 runtime/replay blobs contain both message variants without rendering them.
The r005 comparison loads immutable blobs in memory with verified unchanged
siblings; it is a controlled diagnostic, not a separate r005 acceptance run.
Both exact required interpreters reproduce the result.

**Required behavior:** transfer a recorded failure to the host without executing
fallible exception rendering; return the failed receipt with the first cause and
retain delivered actions. Later real failures must remain typed and ordered.
**Advisory implementation direction:** keep the original exception as the chained
cause and construct the transfer signal without calling its `str` or `repr`.
Apply the same safety rule to both owners. No particular replacement architecture
is mandated.

## Evidence and limits

The initial independent inventory preceded handoff claims. Blob-based identity,
no-renames whole-row sorting, normalized checkout equality, and clean final
snapshot were verified. Exact CPython 3.11.15 ran first, then 3.14.6, under `-B -P`,
asserted identity before payload imports, exact snapshot `PYTHONPATH`, scrubbed
environments, and absolute Git. All four focused suites pass: **123 tests per
interpreter**. Those green suites do not cover the failing exception-message path.

Direct receipts: `checks/cold-a-py311-owned-protocol-v1.txt` (SHA-256
`0cf9c1203a5a62c4db2038fb471d447c8e9d06de5b1a61a2f219ceb850d77b5b`) and
`checks/cold-a-py314-owned-protocol-v1.txt` (SHA-256
`6d94a2d7a80b78308ac513cdda59bba2dbf218c8dacab9d9609e0882b55bc7a0`).
The script, command/environment captures, scope exclusions, and complete receipt
index are in `checks/cold-a-*`.

The ownership-before-cleanup approach is coherent, but its transfer step still
executes unowned fallible work, duplicated across two wrappers: **STRAINED**.
Unchanged event/trace/pre-settlement observations are explicitly deferred and do
not contribute to this verdict. No source/test/configuration edits, installs,
broad/GPU suites, experiments, integration, or commits were performed.
