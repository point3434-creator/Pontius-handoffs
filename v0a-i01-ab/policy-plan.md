# Policy-authority correction planning

2026-08-30, Codex. Next separate R2-01/R3-01 FIX candidate; exact predecessor
will be v0a-i01-ab/r001 only after its reviews settle. Draft worktree:
D:/Pontius-worktrees/codex-v0a-i01-policy. No unrelated correction is frozen here.
Existing root cause: ../v0a-i01-impl/R2-01-root-cause.md. Its second-residual history
persists. Scope reviewer ab_scope_inventory reviewed this direction, not implementation.

Required: source identity/behavior cannot substitute caller-supplied policy;
ordinary subtype identity and nested equality paths must reject before an action.
Preserve exact honest hits, misses, illegal matching entries and complete context
validation. The unchanged sealed action_for API remains the only lookup algorithm.

Chosen boundary: exact-type, recursively exact immutable graph admission, then
reconstruct an owned exact sealed source. No caller digest/equality is trusted
before validation, and the runtime never consults the caller's source thereafter.
Public select_blueprint_action admits its four inputs and delegates to the same
private four-input selection used by the runtime's already admitted policy.
No second source validation/full-table hash is added per runtime action.
The hand-start canonical digest binding remains inside the first measured dispatch;
ReplayHost obtains its header policy identity from the admitted runtime source.
Rejecting all source subclasses deliberately supersedes the earlier test which
accepted an action_for-override subclass while bypassing its override.

Discovery: source admission, key/entry/action/leaf/tuple graph, identity methods,
selection, matching-error classifier, runtime binding, host header and direct helper.
The direct helper also validates exact card/betting/decision graph and compares
decision to the kernel-derived decision with exact type equality, preventing bool
or float aliases where a dataclass lacks a constructor validator.

RED targets: digest/canonical substitution at both boundaries; ordinary nested
key equality and scalar/container/action/entry subtypes; exact legal-decision
numeric aliases. GREEN preserves existing controls and tests legal selection
through the real runtime/mailbox. No private forging is needed to establish RED.
Source copying additionally prevents retention of caller-owned dataclass objects;
private-state mutation remains outside the required threat model.

Files: runtime.py, replay.py, tests/test_v0a_hand_replay.py,
tests/test_v0a_contract_faults.py. No new module or test filename. Expected <1,000
changed lines. CPU correctness only; floor-first dual interpreter snapshots,
frozen manifest and two independent cold passes. No sealed edit, broad execution,
source seal, research owner or ceremonial integration authorization.
