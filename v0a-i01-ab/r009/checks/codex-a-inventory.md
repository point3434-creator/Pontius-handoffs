# Reviewer A independent pre-coverage inventory

Frozen target: 8d240db477b8c141e6142e055dbfbedc75c6a2f8.
Integration manifest: 4f91aa7ce728c3eff6a7ad30a7c131985d5b86b615875df978d30ac39386aa51.
This inventory was authored from the permitted initial packet, pinned controller
workflow, frozen requirements, and source/tests. Deferred coverage.md has not
been opened. It is a discovery inventory, not a proof or verdict.

## Identity and scope established

The independent runner reconstructed whole-row-sorted SHA-256 rows from the
candidate's Git blobs relative to parent d1ed3cbda6107d61ea8e77133871720af04970cd.
All 17 rows exactly equal manifest.sha256, including LF bytes. Candidate ref,
HEAD, parent, input pins and checked-out manifest bytes were checked. Fresh clone:
D:/pontius-snapshots/cold-r009-a-56b2a4a4e9d546edb90aedb516039e8b/harness.
Raw results: codex-a-identity.json.

FIX comparison 00db06624ab25f10cd181badccf92c87a78f17ee has exactly three changed
paths: tools/generate_test_inventory.py, tests/test_inventory_and_profiles.py,
and tests/test-inventory.json. tests/test-profiles.toml is permitted but unchanged.
The six v0a modules plus four non-boundary suites are byte-identical as blobs to
r007 source ddea6efbeb55cb8b71da1ebd5a359a0c2c901cf1. Remaining C paths are carried
integration source, not newly introduced helper-fix behavior.

## Requirement -> paths -> evidence plan

1. Exact six origin files and trusted-component import separation: __init__,
clock, model, replay, runtime, trace under src/pontius/v0a. Boundary enforcement
in tools/check_stabilization_boundaries.py and tests/test_v0a_boundaries.py must
accept permitted stdlib/visible-state siblings and reject undeclared v0a origins,
host import from non-host code, river outside replay, and complete-deal access
outside replay. Discover absolute/relative imports, aliases, wildcard imports,
qualified/deferred uses, initializer behavior and malformed syntax. Static
policy reads plus focused boundary suite; comments/strings are positive controls.

2. Preserve baseline bytes, legacy outgoing edges and SCC policy: frozen
checker and docs/architecture/dependency-baseline.toml; pinned baseline blob
5fe6ee47f3380b65887b528efef05b72c8e6ac0a. No sealed kernel appears in the changed
manifest. Verify exact pin and actual boundary acceptance, not just synthetic
inputs. Do not regenerate baseline.

3. Callable selection is source-point object identity, not a spelling: generator
_SourceOrderedResolver snapshots/_evaluate, _HelperProvenance, helper seeds,
registry exports, _resolved_helper and _review_body dispatch. Current name/alias,
original receiver, descriptor kind and captured bound receiver must identify
one callable. Reassignment must lose the name's proof while retained alias or
bound method keeps the original object. Callable evaluation precedes argument
evaluation. Probe captured callees when argument evaluation mutates/rebinds the
lookup owner; reject unstable replacement/decorated/unknown members.

4. Every Python binding scope respects its source order: module/imported module,
class, method, lexical locals, closure/nonlocal/global, parameters, comprehensions,
for/with/except targets (including exception cleanup), match/walrus/destructuring,
annotations and deletion. Future local binding produces unbound-local behavior;
an absent snapshot alone cannot prove a call dead. An actually failed lookup
must retain its exact exception successor with no helper-body rows. Probe caught
lookup failure and later reachable sensitive calls. Actually dead/deferred bodies
must not be expanded simply because their source exists.

5. Descriptor/default/argument semantics: _helper_descriptor_kind,
_helper_receiver_kinds, _helper_member_value, _bind_helper_arguments and the
effective-input binder must agree on ordinary bound/unbound methods, staticmethod,
classmethod, positional-only and keyword-only parameters, default alignment,
required/duplicate/unexpected/extra arguments. Receiver parameter spelling has no
authority. Legal all-default static and defaulted receivers cannot crash or shift
values; dynamic/unsupported argument shapes may explicitly refuse, never approve
a literal sink with guessed bindings. Preserve direct unittest-entry preflight.

6. Effects follow effective inputs, not explicit syntax alone: _apply_helper_call_effects,
_registered_helper_environment/defaults, _helper_effect_shape,
_helper_namespace_store and identity invalidation. Explicit args, omitted defaults,
implicit bound receivers, class receivers, captured local defaults, closure cells,
module globals and imported owner exports can carry helper authority. Definition
creation captures defaults before later rebinding; closure names resolve later.
Registered module default uncertainty must refuse. Attribute/delete/setattr,
reflection, rebinding, escaped/container-held references and helper-forwarding
must either retain the correct owner mutation or refuse. Name rebinding must not
invalidate the prior object retained elsewhere. Probe positive irrelevant-object
mutation and explicit/default override controls, plus reached mutation before
exception, failed argument binding, and an exception before a would-be mutation.

7. Analysis remains finite and nonexecuting: global analysis budget and helper
recursion limits cover new registry, default, effect and recursive traversals.
Unknown provenance, recursive/unsupported shapes and registered generator
consumption refuse explicitly. Creating an unconsumed generator does not execute
its body. Never execute synthetic subprocess/CuPy fixture bodies to obtain an
oracle; inspect as bytes and use harmless independent return/event projections
only where those projections are needed. No capability grant is derived here.

8. Generated corpus: tests/test-inventory.json and tests/test-profiles.toml must be
ordinary deterministic generator outputs. Existing assignments remain identical;
the five v0a suites are registered. Only mechanically affected census expectations
change. Inspect current checked-in inventory/profile tests and run generator
--check on both actual slots, before/after manifest hashes unchanged. No new
baseline, capability approval or digest grant paths may enter the manifest.

9. CI addition: .github/workflows/ci.yml must retain prior hard gates and add five
CPU-only clone-safe v0a suite commands with !cancelled() reachability after earlier
failures. No continue-on-error on the added suites. Inspect main-to-candidate diff.

10. A/B preservation contracts: typed event/value admission, immutable policy
inputs, independent legal/settlement verifier, outer authoritative clock through
host acknowledgement/publication, failure cause ownership/order and retained
known deliveries. Blob equality is the primary preservation check; bounded
existing suites can confirm lawful A/B still passes C admission. Do not redesign
or introduce new A/B scope.

## Verification boundaries and remaining uncertainty

Run actual CPython 3.11.15 first, then 3.14.6, with full executable/version checks
before Pontius import, -B -P, snapshot cwd/src PYTHONPATH, scrubbed environment,
validated absolute Git and D-local temporary directory. Use selected affected
DesignReviewTests, focused boundary and A/B preservation suites if needed, and
independent adversarial probes through derive_design_review. No whole CI wall,
guarded broad profile, GPU/install, lifecycle, source-seal or rehearsal execution.
All static probe inputs must remain data. Source is frozen; report any correction
without editing it. Initial inventory intentionally leaves untested outcomes open.

The generator has several collaborating representations of one call (source
values/provenance, descriptor binder, effective-input effect resolver, body review,
exception successors). Their agreement on one source-ordered call is an explicit
review risk. Coverage must show public receipt/blocker behavior and independent
expected execution, not only internal bookkeeping or a list of syntax cases.
