# Slice C plan — admission, boundary policy, and the CI gate

Author: Claude. Date: 2026-08-30. Status: plan only; **no source edited**.
Written while `v0a-i01-impl/r002` is under cold review, from read-only
inspection of the sealed tooling. Nothing here is started until r002's
verdict lands, because slice C touches shared generated files and must not
be in flight against an unsettled candidate.

## Why slice C is not optional

The stabilization boundary gate rejects the v0a package today. In
`tools/check_stabilization_boundaries.py`, `enforce_legacy_edges` walks
modules present now but absent from the frozen baseline and raises for each:

```
if added != "pontius.evidence" and not added.startswith("pontius.evidence."):
    violations.append(f"new source module lacks stabilization classification: {added}")
```

`pontius.v0a`, `pontius.v0a.model`, `.clock`, `.runtime`, `.trace`, and
`.replay` all land in that set. The baseline scan covers `src/pontius/**.py`,
so there is no path by which the package is simply invisible to the gate.
This is the controller's Stage-0 finding P1 on the brief, and ADR-0485's
change boundary authorizes exactly the narrow fix: classify v0a with its own
policy, and never regenerate
`docs/architecture/dependency-baseline.toml` to absorb it.

## The five changes

**1. Declare the origins.** Add a `V0A_ORIGIN_PATHS` frozenset beside the
existing `EVIDENCE_ORIGIN_PATHS` and `ORCHESTRATION_ORIGIN_PATHS`, listing
the six `src/pontius/v0a/*.py` files explicitly. No wildcard: an
undeclared new v0a file must fail the gate exactly as an undeclared
evidence file does.

**2. Extend origin classification.** `enforce_origin_classification`
currently inspects only `src/pontius/evidence/` and `tools/`. Add the
symmetric clause for `src/pontius/v0a/`, so an unclassified v0a path is
rejected by name.

**3. Permit the classified modules, narrowly.** Extend the
`enforce_legacy_edges` new-module allowance to accept `pontius.v0a` and
`pontius.v0a.*` alongside the evidence namespace. Every other new top-level
module stays rejected — the flat root remains read-only sediment.

**4. Add a v0a import policy.** A new `enforce_v0a_import_policy` mirroring
the evidence one, encoding ADR-0485's allowlist exactly:

| Origin | May import |
| --- | --- |
| any `pontius.v0a.*` | stdlib; `pontius.v0a` siblings; `action_clock`, `preparation_bank`, `legal_decision_spine_v2`, `no_limit_betting`, `holdem_cards`, `immutable_blueprint` |
| `pontius.v0a.replay` only | additionally `pontius.river` and the complete-deal type |

The current candidate satisfies this: `clock` is stdlib-only, `trace` imports
only its sibling `model`, and `replay` is the sole user of `river`. The
policy also enforces ADR-0485's structural rule that `model`, `clock`, and
`runtime` may not import `replay` — the isolation that keeps the complete
deal away from policy selection. `enforce_no_new_or_expanded_scc` needs no
change: the sealed modules never import v0a, so no cycle appears.

**5. Prove the baseline is untouched.** A test asserting the baseline blob is
byte-for-byte the pinned `5fe6ee47f3380b65887b528efef05b72c8e6ac0a`, so a
future round cannot quietly regenerate it to make a violation disappear.

## Test admission — the part that historically hurts

Four new test files must be declared in `STABILIZATION_TEST_FILES` in
`tools/generate_test_inventory.py`, then `tests/test-inventory.json` and
`tests/test-profiles.toml` regenerated through the authorized writer:

- `tests/test_v0a_hand_replay.py`
- `tests/test_v0a_trace.py`
- `tests/test_v0a_replay.py`
- `tests/test_v0a_contract_faults.py`

Boundary tests for the new policy go in `tests/test_v0a_boundaries.py` — a
fifth new file, also declared — rather than editing the already-declared
`tests/test_stabilization_boundaries.py`, keeping this round's diff additive.

The census expectations in `tests/test_inventory_and_profiles.py` will then
need an honest refresh. This is the machinery that has bitten this project
before: several expectations are line-bound, so inserting entries shifts
them, and the f-string census anchors to `JoinedStr` start lines for
version stability across 3.11 and 3.12+. The refresh must be mechanical and
declared — never a silent digest update, which ADR-0481's kill criteria name
explicitly.

## CI

Add the four (soon five) clone-safe v0a suites to `.github/workflows/ci.yml`
as a direct gate, per ADR-0484's continuous-integration growth rule. No
existing hard gate is demoted, and nothing v0a needs is archive- or
device-dependent, so no environment gating is required. CI remains an
early-warning layer, not the acceptance procedure.

## Sequence

1. RED: boundary gate fails on the unclassified package; baseline byte-pin
   test passes; admission gate rejects the undeclared test files.
2. Apply changes 1–5, then the admission declaration and regeneration.
3. Refresh census expectations mechanically; record what shifted and why.
4. GREEN: boundary check exits 0, baseline blob unchanged, inventory
   regeneration reproducible, all v0a suites plus
   `tests/test_inventory_and_profiles.py` pass from disposable snapshots on
   CPython 3.11 and 3.14.
5. Freeze as the next round with scope limited to paths whose digests differ
   from r002.

## Risks

- **Census churn.** The regeneration may shift line-bound expectations in a
  large generated file. Mitigation: regenerate, diff, and explain every
  changed expectation in the self-report rather than accepting the new bytes
  as self-justifying.
- **Baseline temptation.** If the gate still complains after classification,
  the wrong fix is regenerating the baseline. The byte-pin test exists to
  make that failure loud.
- **Scope creep into the flat root.** Nothing in slice C may add or modify a
  top-level `src/pontius/*.py` module.
