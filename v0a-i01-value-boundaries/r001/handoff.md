# v0a value-boundary audit r001
Kind: NEW-SURFACE audit of additional contracts; no implementation changes.
Tier C review depth. Coordinator: Codex. No implementation finalizer assigned.
Candidate: 47d08d8c1556d776358e15811e3e98b859fd6a8b
Ref: refs/heads/review/v0a-i01-value-boundaries/r001 (local, unpushed; alias of implementation r003 bytes).
Manifest SHA-256: cc255e28680f71fe15de78f26bb8f99a337c1c79e12bf3bdf382a8aa74e7844a
Base: b357d333fc2393b7fc7dcf31f30c86616208c817
Tree: 35a6667ca3785e750324b3c93103a8994a6d7d6a

User asks whether the reported __post_init__-skip pattern affects other frozen
v0a values: mailbox receipts, events and spine tickets. Treat that as a
hypothesis. The latest available frozen implementation is r003; no claim
about a future submission or unavailable seed audit is permitted.

Scope: construction validation and admission of frozen values at v0a event,
action/envelope/receipt, and V2 spine-ticket boundaries. Read necessary sealed
dependencies to follow these paths; do not edit them. Inventory record/fixture
values but do not reopen the separate trace-reader/publication/accounting lanes.

Count a material issue only with a supported concrete path and observable
contract breach. Ordinary subclass construction and overriding __post_init__
are in scope. Arbitrary object.__new__, object.__setattr__, private-state
tampering, monkeypatching and a malicious mailbox simply lying about delivery
are not proof of this mechanism. Distinguish internally produced values from
externally admitted ones and harmless representability from broken admission.

Contracts: frozen ADR-0485 and docs/briefs/v0a-increment-1-brief.md, especially
exact field types, validated immutable values, malformed-event typed refusal,
delivery identity and preservation, and unchanged legal-spine contracts.
Process: committed docs/workflow.md at d1ed3cb; current CLAUDE.md supplies
approved permanent Python3.11 tooling. The concurrent mandatory-design-verdict
proposal in mutable workflow.md is not this audit's adopted instruction.

Run diagnostic payloads only in assigned fresh disposable D-local snapshots,
-B -P, snapshot cwd, exact snapshot/src PYTHONPATH, scrubbed environment,
absolute PONTIUS_GIT. Assert and record absolute sys.executable, CPython and
full sys.version before imports. Floor first: D:/Pontius-tools/py311/Scripts/python.exe
(3.11.15), then D:/Pontius/.venv/Scripts/python.exe (3.14.6). No GPU, broad suites,
source/test changes, experiments, installs or implementation commits.

Independent passes use the same frozen pair and no other reviewer's findings.
Keep probe scripts and receipts under checks/, attributed reports under reviews/.
Each reviewer writes one own task-ledger verdict with an exclusive append slot.
Coordinator consolidates by contract, gives concrete engineering techniques
and a patch/refactor/replacement assessment supported by evidence. This audit
does not amend the r003 slice-1 verdict or classify new findings as residuals.
