# Independent initial inventory (before deferred coverage)

Reviewer: Codex A. Candidate 00db06624ab25f10cd181badccf92c87a78f17ee;
manifest 1e5814b2c04a0065586d8fa73f89edc1ffb0eae4830bea8c893630172d5798f2.
Recorded from handoff, acceptance, ADR-0485/0484, revised brief, current
CLAUDE/workflow, frozen source and C diff. Coverage and prior/peer artifacts
have not been opened. Identity receipt: codex-a-02-identity.json.

## Paths

Preserve r007 blobs exactly: src/pontius/v0a/{__init__,clock,model,replay,runtime,trace}.py;
tests/test_v0a_{contract_faults,hand_replay,replay,trace}.py (ten files).
C surface: .github/workflows/ci.yml; tools/check_stabilization_boundaries.py;
tools/generate_test_inventory.py; tests/test_v0a_boundaries.py;
tests/test_inventory_and_profiles.py; tests/test-inventory.json;
tests/test-profiles.toml (seven files).
Related frozen source: tools/generate_dependency_baseline.py for module/init,
relative import and graph normalization; existing stabilization boundary tests;
inventory public design-review entry, registry, binder, flow and direct-test
preflight; immutable kernel/baseline blob references; pontius/__init__.py CPU
import behavior. No implementation narratives or earlier findings are inputs.

## Independent invariant and risk matrix

1. Blob identity: whole-row byte-sorted manifest, exact parent/base, exactly 17
paths; all ten preservation blobs equal r007; legacy baseline pin and sealed
source remain outside the diff. Evidence: raw Git blobs and manifest comparison.
2. Origin admission: only six v0a Python origins including initializer; reject
additional files or nested package members, no broad namespace escape. Distinguish
classification from graph legacy-module admission.
3. Import direction: ADR external kernels only; river and replay host isolation;
absolute/relative/aliased imports, from-package names and nested deferred imports;
initializer normalization is part of the same boundary. Full-corpus source names
must be supplied so import prefix normalization does not hide a target.
4. Complete-deal separation: direct renamed import, module attribute, bare symbol,
wildcard from holdem_cards and references nested in functions or TYPE_CHECKING
must be refused outside replay. Visible OneSeatCardState and comments/string
literals accepted. Malformed syntax/encoding must become BoundaryError.
5. Graph preservation: exact legacy edges and approved baseline/SCC identity;
new v0a cycles rejected. Real check_repository positive plus opposing controls.
6. Helper binding: Python positional/default/keyword semantics before sink
expansion; defaulted bound receiver must not shift defaults or crash; positional
only receiver must not remove a following keyword parameter; static all-default
helper has no implicit receiver. Ordinary/class/static descriptor provenance
must be proved; unknown/shadowed/aliased/stacked decorators conservatively refuse.
7. Receiver authority: parameter name alone is not identity; instance-vs-class
origin, unbound calls, reassignment, nested lexical capture and parameter shadow,
forwarded helpers, direct unittest entry and cross-file helpers need evidence.
Invalid arity/duplicates/unknown keyword/positional-only keywords remain typed
blockers even when sink argv is entirely literal. Sensitive fixture source is
never executed; expectations come from Python binding semantics/pure projections.
8. Inventory integration: exactly five new v0a suite entries; preserve every old
assignment, approvals and digest grants. Normal generator --check must reproduce
both generated files byte-for-byte. Changed census expectations reflect the
combined corpus and do not silently weaken checks.
9. CI integration: each five new suite command stays a hard gate and has an
explicit !cancelled status predicate; prior steps/gates remain byte-preserved
apart from additive insertion. Do not execute CI wall.
10. Execution evidence: genuine 3.11.15 first, then 3.14.6; fresh D-local clone(s),
-B -P, snapshot cwd/src PYTHONPATH, identity before payload import, exact module
origins, scrubbed environment and absolute validated Git. Focused C suites and
A/B integration tests only, no broad/guarded/GPU/install/lifecycle operations.

## Planned challenge cases and limits

Use source-independent table-driven helper fixtures covering descriptor and
receiver contexts, legal and invalid call shapes, with literal-sink controls;
exercise the public design-review API. Exercise real check_repository on copies
for undeclared origin/import/cycle/baseline controls. Compare generated metadata
and prior assignments structurally, not only hashes. Existing focused tests
supply deeper nested/cross-file regression coverage. Static trusted-component
separation does not prove a malicious-Python reflection sandbox, and ordinary
checks establish no source seal, experimental authority or timing result.