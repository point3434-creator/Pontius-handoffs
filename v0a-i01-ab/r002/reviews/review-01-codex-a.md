# Independent cold A review - v0a-i01-ab/r002

Reviewer: Codex /root/ab_r002_cold_a. Issued 2026-08-30.

**Defect verdict: CLEAN for the scoped R2-01/R3-01 policy-authority correction.**
**Design verdict: SOUND.** No required authority correction remains. Two low-impact
observations below are advisory. The independent diagnostic deliberately exits 1 for
the malformed-depth observation; this is not a claim that every diagnostic passed.

## Frozen identity and independence

- Ref: refs/heads/review/v0a-i01-ab/r002
- Commit: 2f4287f68a83fac4225a05a91daffdb3f2977a43
- Manifest SHA-256: 55f7ebf8827c79a6d6c70b1bf26508d87527b8c7113d2458fb4c3dfb5fed0957
- Parent: 256bcf5b1e721c70216f4d8937166cbb9c25a7ce
- Tree: 7d1383a1a7b2cf05442e4ef4fe8a9189708b2263

I recomputed changed-file digests from stored Git blobs, sorted complete manifest
rows by digest-first bytes, and verified both the manifest file and its digest.
Exactly runtime.py, replay.py and the two stated tests differ. The six examined sealed
kernel/blueprint dependency blobs are unchanged. The LF checkout matches the four
changed blobs byte-for-byte. See ../checks/codex-a-identity.json.

Inputs were the handoff, frozen source/tests, frozen ADR-0485/ADR-0484 and brief,
current CLAUDE.md and whole workflow/checklist, and the permitted prior dispositions.
No implementer transcript, plan, self-report or other review was consulted.

My initial invariant/path inventory was written before opening coverage.md:
../checks/codex-a-initial-inventory.md, SHA-256
9d4ae1826fd29b40c05e742f224d1a8bc279cd8ddb643ea294f5e5aefd6a43a8.
The deferred coverage file verifies as
35edf1f2b309f0bc017f6831631efaead86d0cf3b8f6cf1fe9db6a753b102b12.
I did not rely on the implementation's referenced probe results or root-cause narrative.

## Findings and required outcomes

There are no Critical or Important findings and no required correction for this
policy-authority candidate. The prior delegate, outer identity hooks and nested
subtype influence are closed at the admitted policy boundary. The direct four-input
helper rejects the tested substitutions before lookup.

### A-N1 - Advisory, low impact: malformed deep context escapes the normal refusal type

Confidence: high; reproduced on both actual interpreters.
Location: src/pontius/v0a/runtime.py:88-96 and :146-157.

Starting from a real valid legal decision, build an exact tuple nested 2,000 times.
Use ordinary dataclasses.replace to place it in either decision.action_kinds or
its exact RaiseBounds.minimum_raise_to. These records have ordinary constructors
without field validators. Call public select_blueprint_action with a real empty
source, real cards and real betting state. Both calls raise RecursionError instead
of InvalidDecisionContextError: the generic copier descends before checking the
field's semantic shape, and the context handler does not catch RecursionError.
No subclass, private mutation, introspection or production monkeypatch is needed.

Exact reproduction and exception names are in ../checks/codex-a-policy-probe.py and
both v2 receipts. The diagnostic exits 1 on this explicit expectation mismatch;
all its preceding authority and behavior assertions passed.

This is a limited error-classification defect in malformed direct-helper input.
It refuses before selection, runs no caller hook, produces no action, substitutes no
policy identity, and is not reached by the runtime's sealed decision producer.
Those facts limit impact and do not support calling the original authority residual
open. It is advisory for this scope, not a required correction or input-size gate.

Advisory outcome: normalize these malformed shapes to InvalidDecisionContextError
without lookup. A field-aware shape check before descent avoids copying arbitrarily
nested content in fields permitting only enum values or an integer. Narrow
RecursionError containment is another possible local correction; neither technique
is mandated. Verify both public-helper examples and preserve honest hit/miss/illegal
controls. Do not invent an operating-size budget as a workaround.

### A-N2 - Advisory, low impact: two test lines exceed the width rule

Confidence: high; stored-blob check.
Location: tests/test_v0a_hand_replay.py:971 and :978.

These two new lines exceed 100 columns. All four changed files are LF-only, BOM-free
and have no trailing whitespace. Reflowing the expressions would satisfy checklist
item 10; it has no policy-authority consequence and is not an acceptance blocker here.

## Authority and behavioral evidence

| Requirement / risk | Independent evidence | Result |
| --- | --- | --- |
| Delegate and outer identity/action hooks | Eleven source graph cases at both boundaries | Typed rejection, zero deliveries |
| Nested key/entry/action/tuple/int/str influence | Ordinary constructed graphs and frozen subtype/history regressions | Rejected before lookup |
| Complete legal context typing | All six integer decision fields and five RaiseBounds fields aliased | Eleven typed refusals |
| Hit, miss, other-state miss, illegal entry | Real HandRuntime.dispatch and ActionMailbox | Raise/call/call; illegal entry fails without delivery |
| One authority for header and decisions | Both real ReplayHost fixtures, sealed-method profiling | One admission, one owned source |
| No second full-table rehash per action | Actual sealed digest/action_for calls | Four actions/six digests; two actions/four digests |
| Initial binding remains measured | Add 16 seconds at first real dispatch digest | Deadline failure; elapsed 16,000,012,000 ns |
| Complete hands and hidden-card controls | Existing isolated focused suites | 131 tests per interpreter pass |
| Malformed exact graph depth | Two direct-helper cases | Advisory exception mismatch above |

The host profile observes real production methods, not replacement helpers. Every
lookup/digest object differs from the caller's original source, and all such calls
in one hand use one owned source. Header and all decision digests match the honest
policy. Only the header and initial bind add digest calls beyond one per action.
The synthetic clock perturbation proves accounting placement, not performance.
The sealed action_for algorithm is unchanged.

## Coverage comparison and design assessment

Deferred coverage names the principal paths independently found: admission, identity
dependencies, matching, illegal-entry classification, direct context graphs, initial
binding and ReplayHost header. Its finite ordinary-subtype limit is reasonable;
this evidence does not establish an arbitrary Python sandbox. Malformed depth adds
an observation but demonstrates no caller hook, identity substitution, context alias
acceptance or repeated runtime admission.

SOUND: replacing caller policy objects with one owned graph of exact validated values
fits this trust boundary and removes virtual-method/equality authority rather than
adding a check for the latest hook. Runtime decisions do not repeat source admission.
The direct-context classification issue can be handled locally; it does not justify
redesigning the complete runtime or altering sealed code. Keep the record-type
allowlist narrow and preserve real boundary tests as models change. This guidance
is advisory, not an additional acceptance gate.

## Execution receipts and limits

Fresh clone: D:/Pontius-review-ab-r002-cold-a-20260830, outside the packet repository.
All payload children used -B -P, snapshot cwd, exactly snapshot/src as PYTHONPATH,
a scrubbed environment and absolute C:/Program Files/Git/cmd/git.exe. Git was checked
as regular/non-reparse. Preflight asserted versions, flags and runtime import path.

1. D:/Pontius-tools/py311/Scripts/python.exe: actual CPython 3.11.15, first.
2. D:/Pontius/.venv/Scripts/python.exe: actual CPython 3.14.6, second.

On each interpreter: hand_replay 39, contract_faults 22, replay 45, trace 25:
**131 tests, all exit 0**. Independent diagnostic: 22 source-boundary refusals,
11 context-alias refusals, four real dispatch outcomes, two host profiles and one
measured-binding control pass. Two depth refusal-type checks mismatch; probe exit 1.

Receipts: ../checks/codex-a-py311-v2-receipt.json and
../checks/codex-a-py314-v2-receipt.json. Initial floor receipt is retained: three
correctly named suites pass; a nonexistent test_v0a_replay_host.py command exits 2.
The append-only v2 runner corrects the reviewer filename to test_v0a_replay.py.
No candidate correction or silent retry is claimed. The 3.14 preflight records the
existing initializer's CUDA-DLL environment setup; no GPU payload ran. The floor
needed no optional packages.

Final clone status is empty; ../checks/codex-a-final-verification.json binds key
receipts and probe. No source/test edits, installs, evidence-repository commits,
integration, source seal, experiment owner, broad suite, GPU suite or ref retirement
occurred. Event/mailbox/receipt admission, trace/schema/legal acceptance,
publication/accounting and slice C remain outside this verdict. Focused adjacent
tests do not expand the reviewed contract or authorize release.
