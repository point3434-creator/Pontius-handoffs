# Cold review A — v0a-i01-ab/r005

Reviewer: Codex cold A. Date: 2026-08-30.

**Defect verdict: NOT CLEAN. Design verdict: STRAINED.** The explicit accepting checker is an appropriate independent legal-replay boundary and the independently specified settlement correction passes. Strict parser admission remains incomplete on failed-terminal variants and the ordered private-card pair.

## Frozen identity and independence

- Ref: `refs/heads/review/v0a-i01-ab/r005`.
- Commit: `6cdf7b00dac653a9a295bbb86cdc3b5782317491`.
- Parent/base: `c6adbcaa048988361d2388970eaca772711b797b`.
- Tree: `89ae2190fa69c6974750ae032a7afec3ca106f18`.
- Manifest SHA-256: `83798245d9feac931479478e81c850ac4de277a2903a7523f5745320738cd21f`.

I independently recomputed all four changed-file hashes from `git cat-file blob`, with rename detection disabled and the complete LF manifest sorted by whole rows. The bytes equal `manifest.sha256`; ref/parent/tree match. `git diff --check` passes. Only trace.py, replay.py and their two focused tests change; sealed dependencies are unchanged.

The initial requirements/path inventory was written before opening coverage.md: `checks/cold-a-inventory.md`, SHA-256 `498c748c9916965919f61d326c5f33d15f7ac291cf101881abacf3abe05f2c73`. The deferred coverage hash was independently verified as `007168c11b2554994ec24b1b6c821e17636f85b75257a84258c1304ac68c53d7`. No implementer transcript, plan, self-report or current peer report was read. Permitted requirements were ADR0485, ADR0484/the named brief, the linked prior disposition and current CLAUDE.md/workflow.md. No finding below concerns the separately owned publication/accounting/Slice C correction.

## Required findings

### A1 — Important: failed-terminal consistency is skipped when passed is false

Confidence: high; reproduced on both actual interpreter slots.

Frozen locations: `src/pontius/v0a/trace.py:836-858`, `:870-876`, and especially `:910-920`. Terminal fields are individually typed, but the cross-record consistency predicate is guarded by `if terminal["passed"]`. A failed trace can therefore claim facts expressly forbidden by its own interrupted or unknown-delivery records.

Real reproduction in `checks/cold-a-probe.py`:

1. Run real ReplayHost/FIXTURE_A with an adapter that calls the real ActionMailbox.deliver, then causes the next clock observation to return an invalid boolean. One mailbox acceptance occurs. The retained trace has one interrupted decision/failure pair, `interrupted_response_count=1`, `passed=false`, `complete=false`, `accounting_complete=false` and null totals. The unmodified trace parses.
2. Change only the terminal to `complete=true`, `accounting_complete=true` and float zero totals, keeping `passed=false`. Recompute both specified digests independently. `parse_trace` accepts this contradictory trace.
3. In a separate real schedule, accept into the real mailbox and raise before acknowledgement. The host retains unknown delivery and one interrupted response. The same completeness/accounting mutation is accepted.
4. On the real interrupted prefix, separately attach the successful A settlement while leaving the hand unsuccessful/incomplete: parsing accepts. Separately replace or erase the terminal's clock-invalid primary reason while retaining the paired clock-invalid failure/decision: parsing also accepts.

The evidence is in `cold-a-311-probe.txt` and `cold-a-314-probe.txt`, cases `interrupted-claims-complete`, `unknown-claims-complete`, `interrupted-claims-settlement`, `terminal-replaces-primary`, and `terminal-erases-primary`. The zero probe exits mean the observations completed, not that these invalid traces passed review.

ADR0485:427-435 unconditionally requires an interrupted response or unknown delivery to force incomplete/failed/incomplete-accounting status. ADR0485:364 requires null settlement on unsuccessful/incomplete hands; :437-438 preserves the first cause. These are reader/record consistency obligations, not a request to measure host work or redesign publication. A consumer inspecting retained failed traces currently receives internally false completeness, settlement or cause claims from the advertised strict reader.

Required outcome: enforce the applicable failed-terminal invariants as well as the success invariants, preserving honest failure prefixes. Do not permit an interrupted/unknown prefix to claim completion or complete accounting; do not permit a failed/incomplete hand to carry settlement; retain established primary-cause consistency. GREEN must mutate real accepted-interrupted and unknown-delivery prefixes, rebind both digests, require typed refusal, and preserve the original prefixes plus normal controls. The accepting checker currently refuses these failed prefixes; this finding does **not** claim a false VerifiedTrace or host success.

### A2 — Minor: hand_started accepts descending private cards

Confidence: high; reproduced on both actual interpreter slots.

Frozen location: `src/pontius/v0a/trace.py:657-659`, calling `_validate_cards` at :627-633. The helper checks cardinality, exact card type, range and distinctness, but never the private pair's ascending order.

Start with the real successful A trace, reverse only `hand_started.private_cards`, and recompute both digests independently. `parse_trace` accepts it (`descending-private-pair-parser` in both probe logs). The same content is correctly rejected by verify_successful_trace because it differs from the independently expected deal.

ADR0485:140-141 explicitly requires an ascending private pair. The preserved `HandStartedEvent` constructor also rejects first >= second at `model.py:199-202`; the parser's claim of complete nested canonical schema admission does not match that contract.

Required outcome: reject nonascending private pairs at the public structural reader while preserving board reveal order. GREEN must reverse the real event's pair and rebind both digests so a digest mismatch cannot mask the missing schema rule. This is a bounded schema defect; it does not permit an invalid successful legal replay.

## Engineering guidance and design verdict

**STRAINED overall; the independent legal checker itself is sound in shape.** Its fresh betting/card walk, direct sealed lookup, expected chance/configuration bindings and independent payout comparison are the right separation from the producing runtime. A frozen ParsedTrace is not treated as a successful acceptance token; the checker reparses raw bytes and returns an immutable semantic summary.

The parser's long combined decode/schema/cross-record procedure makes variant coverage uneven: substantial nested-field validation was added, but the terminal cross-record block concentrates on passed=true, leaving failed variants with only per-field checks. The missing ordered pair is another gap between separately maintained schema predicates and the model contract. The initial inventory explicitly included failure/timing/terminal bindings and exact primitive domains; the deferred claim's complete admission assertion exceeds the observed coverage on those members.

Advisory technique: organize explicit variant invariants for completed success, completed failure, interrupted failure and unknown delivery, then apply cross-record identities/counts/cause rules to every relevant variant. Keep event-specific order rules distinct from generic card-array validation. A bounded trace-module refactor and table of public-boundary negative controls should be sufficient; no replacement of the independently walking verifier, production kernels or writer is warranted by this review. This technique is advisory; the behavioral outcomes above are the binding corrections.

## Requirement-to-evidence result

| Requirement | Independent evidence | Result |
| --- | --- | --- |
| Frozen scope/identity | Stored blob manifest; exact ref/parent/tree; diff check | Pass |
| Strict complete nested schema and failure consistency (R2-06) | 34 focused tests plus rebound real-trace mutations | Fail: A1/A2 |
| Distinct legal acceptance and expected inputs (R2-05) | Real A/B acceptance; rebound foreign source, illegal action, false hit, reordered decision, null timing, changed payout/count all refused | Pass for exercised cases |
| Honest failed prefixes | Real accepted-interrupted/unknown controls; every one of 138 normal A clock observations independently failed, all 138 retained trace prefixes parse per interpreter | Pass for these controls; contradictory mutations fail the admission requirement |
| Independent settlement dependency | Legal public action sequence and full real ReplayHost/checker with a shared broadway board, live tied seats3/4 | Pass: contributions (0,1,2,15,15,5), one38 pot eligible (3,4), payouts (0,0,0,19,19,0), final stacks (20,19,18,24,24,15) |
| CPU/interpreter isolation | Actual 3.11.15 first, actual 3.14.6 second; no CuPy/Torch imports in probes; asserted flags and module origins | Pass |

The tied-pot expected values are independently fixed by 38 chips shared by two tied live seats; no production side_pots/settle call supplies this expectation. Two legal policy entries create the preflop5 and flop10 contributions; the ordinary host completes the hand and its trace passes the separately walking checker.

## Execution receipts and limits

Fresh detached snapshot: `D:/Pontius-review-snapshots/cold-a-v0a-i01-ab-r005-20260830`, outside the handoff packet and primary checkout. Execution harness: `checks/cold-a-run.py`; independent probes: `checks/cold-a-probe.py`.

Each child uses `-B -P`, snapshot cwd, exact snapshot/src PYTHONPATH, a new allowlisted environment, PYTHONNOUSERSITE=1 and absolute `C:/Program Files/Git/cmd/git.exe`. Interpreter executable/full version/implementation/flags are emitted and asserted before payload import, followed by trace/replay module origins. The floor uses `D:/Pontius-tools/py311/Scripts/python.exe` (3.11.15); confirmation uses `D:/Pontius/.venv/Scripts/python.exe` (3.14.6).

| Command payload, through harness | 3.11.15 | 3.14.6 |
| --- | --- | --- |
| tests/test_v0a_trace.py | Exit0, 34 tests OK | Exit0, 34 tests OK |
| tests/test_v0a_replay.py | Exit0, 53 tests OK | Exit0, 53 tests OK |
| checks/cold-a-probe.py | Exit0; observations above | Exit0; same observations |

Receipts: `checks/cold-a-identity.json`, `cold-a-311-focused-receipt.json`, `cold-a-314-focused-receipt.json`, `cold-a-311-probes-receipt.json`, `cold-a-314-probes-receipt.json`; each execution receipt records full argv/environment/log SHA-256. Full focused logs use the corresponding `cold-a-<slot>-test_v0a_trace.txt` and `cold-a-<slot>-test_v0a_replay.txt` names. Probe logs use `cold-a-<slot>-probe.txt`.

A read-only snapshot status attempt without a per-call safe.directory setting was refused for account ownership; the repeated check with only the exact snapshot command-line setting succeeded and was clean. No global Git configuration changed. The primary retained its pre-existing CLAUDE.md/workflow.md modifications; this review did not edit source or tests.

No broad suites, dependency install, GPU run, owner execution, source seal, publication/accounting measurement, ceremonial commit, integration or ref retirement was performed or authorized. Passing finite controls is not exhaustive legal-state or timing coverage, and trace-only checking cannot prove host publication/finalization. This report is final; its issuer will append a separately serialized task-ledger verdict only after the coordinator grants the requested exclusive slot.
