# C helper-binding Stage 0 clarification

This implements slice-c-plan-amendment-02.md under the root's adopted Stage 0
clarification, recorded before generator edits. The independent plan was SOUND.
Only tools/generate_test_inventory.py and tests/test_inventory_and_profiles.py
are owned. Preserve every other C and publication file.

Descriptor support is deliberately bounded: bare builtin staticmethod and
classmethod must have no module or class namespace binding or wildcard import
that makes their provenance uncertain. Qualified, aliased, dynamic and stacked
decorators are not accepted by spelling and receive conservative blockers. The
original two unrun qualified/alias positive cases become blocker cases before
source changes. This does not change a capability grant or the baseline.

Cases cover static self/class calls, ordinary bound/unbound calls, class methods
accessed through instance/class/cls, defaulted and required receivers including
positional-only, explicit and omitted arguments, keyword-only defaults, duplicate,
unknown, missing and excess arguments. Pure Python descriptor projections provide
expected module/timeout values; sensitive subprocess fixture bodies are inspected
through derive_design_review only and never executed.

The repair aligns defaults with the full declared positional signature before
receiver removal; descriptor binding is decided once, and allowed keywords derive
from the remaining parameters. No strict=False default-zip workaround, alias
resolver expansion, analyzer rewrite, generation, capability action, broad test,
source freeze, ledger write, or main-checkout change is included.

Fresh D-local snapshots overlay five publication-v3 files and seven C files on
52bd941e9fa1fb90ff6d2d14df2286e2ee4f4ec8. Run focused new and existing binding /
decorator checks with actual 3.11.15 first, then 3.14.6, -B -P, explicit origins,
scrubbed environment, D-local TEMP/cwd/src PYTHONPATH and absolute Git. Root owns
combined generation/census/freeze and final integration review.
