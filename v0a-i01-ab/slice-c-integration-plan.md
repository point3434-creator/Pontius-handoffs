# Slice C replay and bounded import-policy correction

2026-08-30, Codex coordinator. Controller requested replay of Claude's ready
Slice C into finished A/B. Claude's unfrozen worktree is implementation input,
not review evidence. Preserve that worktree and exact initial file hashes.

Replay seven paths only: .github/workflows/ci.yml,
tools/check_stabilization_boundaries.py, tools/generate_test_inventory.py,
tests/test_v0a_boundaries.py, tests/test_inventory_and_profiles.py,
tests/test-inventory.json, tests/test-profiles.toml. Final generated inventory,
profiles and census expectations must reflect the completed A/B/C contents.
Do not alter baseline, existing hard gates, capabilities or historical owners.

Discovered category: module-level import permission does not enforce a
symbol-level complete-deal exclusion. The real full-source-graph probe accepts
SixSeatHoldemDeal imported absolutely, relatively with an alias, through a
qualified module alias, and via star import in runtime. ADR0485 limits that type
to replay. The initial reduced graph also appeared to miss host imports, but
that was an incomplete probe: full graph correctly refuses both relative and
package host imports. Preserve both outputs; claim only the complete-deal gap.

Proposed narrow mechanism: supplement existing module-edge enforcement with
source AST inspection of non-host v0a modules. Refuse explicit from-import of
SixSeatHoldemDeal (including aliases), wildcard import from holdem_cards, and
references to the SixSeatHoldemDeal symbol/attribute. Resolve relative imports
from source origin instead of substring heuristics. Preserve OneSeatCardState
and all other approved kernel imports; replay retains complete-deal access.
This is a trusted-component static dependency rule, not a malicious-Python
sandbox or a claim to detect fabricated names via reflection.

Before production edits: add generated opposing tests for all non-host origins,
absolute/relative/aliased/qualified/star forms, and approved visible-state/replay
controls. Run RED against exact copied C inputs on actual3.11. Apply smallest
rule that closes this discovered category, then focused GREEN floor-first and
3.14. Root/non-cold design review precedes edits. Final integration regenerates
census through authorized writer, records every expectation delta, and freezes
for two fresh independent cold reviews. No pending approval is manufactured:
controller authorization covers this isolated engineering integration, while
final ceremonial source commit remains a later candidate-specific checkpoint.
