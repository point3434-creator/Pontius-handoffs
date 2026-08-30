# Cold A observations and receipt map — r006

Pair: c74b80628a89938ca585ef3240b5c267a7174d0f /
2078d59a4a112bf29a2bd9faca9a2ca070bbd1028a940f2eeb617c9e1c31555f

Independent scope inventory was written before reading handoff.md. The three-path
r005 delta matches the declared scope. Candidate parent/tree and ten blob manifest
rows match candidate.json. Checkout CRLF was only normalized for comparison in
memory. No checked-out bytes were normalized. Initial and final snapshot status
were clean. No other reviewer's findings were consulted.

Focused execution order: release CPython 3.11.15, then development CPython 3.14.6.
Each run asserts executable, implementation, full version, -B/-P flags, snapshot
cwd and PYTHONPATH before payload import. Child environments contain only
SystemRoot, WINDIR, TEMP, TMP, PYTHONPATH, PYTHONDONTWRITEBYTECODE,
PYTHONNOUSERSITE, and absolute PONTIUS_GIT; no ambient PATH or Git overrides.

| Check | 3.11.15 | 3.14.6 | Evidence |
| --- | --- | --- | --- |
| Frozen identity | exit 0 | exit 0 | cold-a-py*-manifest-v1.txt |
| Replay suite | 41 pass | 41 pass | cold-a-py*-test_v0a_replay-v1.txt |
| Hand suite | 35 pass | 35 pass | cold-a-py*-test_v0a_hand_replay-v1.txt |
| Trace suite | 25 pass | 25 pass | cold-a-py*-test_v0a_trace-v1.txt |
| Fault suite | 22 pass | 22 pass | cold-a-py*-test_v0a_contract_faults-v1.txt |
| Owner protocol | regression confirmed, exit 0 | same, exit 0 | cold-a-py*-owned-protocol-v1.txt |

The owner-protocol diagnostic observes real production execution, replacing no
runtime, owner, evaluator, mailbox or ledger. A single deterministic fault is
raised when the second production showdown evaluator is called, inside the new
settlement owner. Opposing cases differ only in exception message behavior:

| Candidate | Body error | Result |
| --- | --- | --- |
| r005 exact blobs in memory | ordinary ValueError | failed receipt, settlement_mismatch |
| r005 exact blobs in memory | ValueError with fallible argument stringification | same failed receipt; no formatting attempt |
| r006 snapshot | ordinary ValueError | failed receipt, settlement_mismatch |
| r006 snapshot | ValueError with fallible argument stringification | RuntimeError escapes at runtime.py:416; four deliveries remain, no receipt |

The r005 module bytes come directly from absolute Git cat-file of
`a8582e6d6b53b55415dab79c4a54e252d00b74ad` and execute in a separate in-memory
package; unchanged clock/model/trace/__init__ blobs are checked for equality.
No baseline file is written. This is bounded counterfactual diagnostic evidence,
not an r005 snapshot acceptance run. The candidate runs its actual snapshot files.

New tests show ordinary body faults, direct-witness faults, and returned mismatches
around cleanup. The independent formatting case is absent. The AST check only
forbids two private attribute names; it cannot establish general exception safety
of the owner's own transfer operation. This limitation is material only through
R6-A01's direct changed-line reproduction, not an additional finding.

Scope exclusions: cold-a-host-boundaries-v1.py and its two captures preserve an
earlier category inventory. Two clean fixture controls pass; ordinary terminal
serialization and owned settlement-evaluation faults return typed receipts. Faults
in earlier decision/failure serialization or first showdown evaluation escape;
a malformed scripted raise amount True raises TypeError during event construction
after the first real delivery without any injected fault. These callers are
unchanged by r006. They are deferred observations, expressly excluded from the FIX
verdict and not claims of a changed-path regression. No broad follow-up was run.

The authoritative verdict is reviews/review-01-codex-a.md. Required behavior and
advisory engineering direction are distinguished there. Raw captures were converted
to UTF-8 LF before their first issuance/hash and never rewritten. The receipt index
lists every cold-A check file as issued before the index itself.
