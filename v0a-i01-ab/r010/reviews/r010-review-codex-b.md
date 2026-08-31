# Independent cold review B: r010

Reviewer ID: codex/cold_review_b
Candidate commit: 29c02f6fbd5eb0b7ddc9e816ef28f570b9839358
Manifest SHA-256: 8741fa20b1ebc7e9e9d226f463680c603c348f1332bf19c8ae12b29579f76deb
Defect verdict: NOT CLEAN
Design verdict: STRAINED

One Important correctness finding remains. The ordinary focused suites pass,
but the public analyzer silently loses callable authority after mutation of a
nested native collection. The specification is not satisfied at that boundary.
No production or repository test source was changed during this review.

## Required correction

### R010-B-01 — Important, high confidence: nested list retention loses authority

Location: frozen `tools/generate_test_inventory.py:17707`, especially lines
17715-17718; related retention admission at 17721-17748 and its early return at
17766-17768. The later unknown member/subscript propagation at 17971-17980 can
only preserve obligations that survived the earlier store.

The native-list retention path updates only values directly present in the
current name-to-value mapping. An inner list reached through a list, tuple or
mapping is an existing represented collection, but its new obligations are not
written back into the enclosing abstract values. The operation is nevertheless
accepted as handled. Subsequent extraction and invocation can therefore carry
no authority, leaving the original registered helper apparently unchanged.
This also occurs when the inner object has a direct local alias: updating that
local value does not update an older nested alias retaining the same identity.

A minimal test-method body, with a static `_launch` whose declared process row
is `[-m, fixed]`, demonstrates the failure:

```python
def mutate(_, owner=ReviewTests):
    owner._launch = None
bag = [[]]
bag[0].append(mutate)
bag[0][0](None)
return self._launch()
```

The independently authored pure runtime projection substitutes `return module`
for the process sink and contains no subprocess execution. It raises `TypeError`
at the final call after `_launch` has been replaced by `None`. Passing the
sensitive source bytes to the real public `derive_design_review` instead returns
one subprocess row with `argv == ["-m", "fixed"]` and an empty unresolved-blocker
list. The analyzer has neither retained the reached effect nor refused it.
The sensitive fixture itself was never executed.

Fresh CPython 3.11.15 and 3.14.6 reproduce all seven variants: nested list,
mapping-to-list, tuple-to-list, an existing local alias also retained in a list,
`extend`, `insert`, and direct invocation of the extracted callback. The first
six use a harmless module-local forwarding function calling the callback; the
seventh calls it directly. All produce the same wrong unblocked process row.
Flat-list retention followed by invocation correctly refuses, while the same
nested storage without consumption remains lawful and returns `fixed`.

Evidence: `checks/codex-b-floor-probes-311.txt` and
`checks/codex-b-dev-probes-314.txt` contain the full sensitive source, separate
pure projection, source hashes, runtime outcomes, public rows and blockers.
`checks/codex-b-probe-assessment.json` records the seven confirmed cases and
classification, SHA-256
`736155be6613641be6d74d6efc796b5e129a9b2c8dc68df06d1e039a1577c1e5`.

This violates the acceptance requirements that forwarding/storage/escape retain
or explicitly refuse relevant callable authority, and that absence of discovered
proof never becomes proof of no effect. It also directly falsifies coverage.md's
native-storage and stale-literal-capability claims. No general heap, reflection,
metaclass or unsupported external ambient mutation is involved in this witness.
The consequence is an unsound capability-review result for ordinary represented
source. This review does not claim any capability was approved or invoked.

Required outcome: retained callable authority must remain visible through every
represented alias of these native collections. When later extraction, invocation
or escape cannot be resolved, issue an explicit blocker instead of publishing an
unblocked stale helper capability. Preserve the distinction between storage and
execution: merely retaining the callback must not run its body or invent mutation.

Required verification: add public-boundary regressions for the seven witnessed
variants and the flat/nested unconsumed controls on both supported interpreters.
Assert the harmless runtime outcome, explicit refusal for the unsafe consumed
cases, and lawful expected rows for the dormant cases. Exercise aliases formed
before and after retention and each admitted `append`/`extend`/`insert` path.
Do not satisfy this by dropping rows without blockers or by blanket-refusing all
native storage. Re-freeze changed bytes and repeat the required review sequence.

## Advisory engineering guidance and design assessment

The new separation of callable obligations from legacy abstract values is useful,
but its storage discipline remains strained. Obligations are copied into immutable
flow values and then repaired by scanning direct local bindings. The witnessed
nested-alias loss is a concrete example of the inconsistency this invites: the
same runtime object has different authority depending on its syntactic access path.
The source already has a `mutable_collection_identity`, so this is a bounded
representation problem rather than a need to interpret arbitrary Python heaps.

Consider an authority store indexed by the existing collection identity, with
explicit branch snapshots/joins and common resolution on nested reads. Alternatively,
use one bounded graph-rewrite operation that updates every reachable representation
and explicitly retains an unresolved obligation when it cannot prove completion.
Keep the existing argument binder, public API, finite work budget and nonexecution
rules. This is a limited resolver-state refactor plus alias/branch/transfer tests;
it need not extract the whole generator or touch unrelated governance machinery.
A local patch can work only if it establishes that invariant across all retained
aliases; adding one more subscript spelling to the exemption retains the cause.
These implementation choices are advisory, not additional acceptance gates.

## Scope, independence and coverage challenge

The manifest was independently reconstructed from Git blobs, with no rename
inference, lowercase hashes, two spaces, LF endings and whole-row sorting.
All 17 rows match the supplied manifest. The candidate's parent is
`d1ed3cbda6107d61ea8e77133871720af04970cd` and its tree is
`21d7aeb7a6a5d5c6cd599e9467e838dd888c828d`.

All ten A/B paths match `ddea6efbeb55cb8b71da1ebd5a359a0c2c901cf1` byte-for-byte.
CI, boundary checker and boundary suite match
`00db06624ab25f10cd181badccf92c87a78f17ee`. The actual repair delta against
`8d240db477b8c141e6142e055dbfbedc75c6a2f8` is exactly the generator, inventory
contract suite and generated inventory. The 13 preservation paths are not a new
implementation review of every accepted A/B line.

The initial independent invariant/path inventory was saved before coverage was
opened: `checks/codex-b-initial-inventory.md`, SHA-256
`6e9212609412798c8b2adafc24a7454e56798b2229bb28a4ad575c81e6224e6f`.
The pinned current CLAUDE/workflow, acceptance/protocol and handoff hashes matched.
Deferred coverage matched SHA-256
`75513c3217e4f8bde476f6dcd7ddb214a4bd14b78161a0c980e31a39b3a3875f`.
Only permitted source comparisons and the named deferred evidence binding were
opened; no prior or peer review, implementation discussion or task ledger was read.

The coverage category is appropriate, and the added tests use meaningful pure
Python projections rather than analyzer bookkeeping as their oracle. However,
`test_callable_authority_native_storage_retains_without_invoking` at test-suite
line 21459 constructs each mutable destination as a direct local. Its surrounding
nested-container forwarding cases do not establish mutation-through-nested-alias
coverage. The seven new observations expose the missing composition, not merely
a coverage percentage gap. The finding above is the sole required correction;
this coverage discussion is not a duplicate finding.

An initial absent-global default probe was deliberately not promoted to a finding:
an absent supplied binding alone cannot prove lookup failure under the accepted
policy. Three additional controls using explicit local deletion or an explicit
helper raise all pass and preserve the lawful later capability. Empty-filter and
arithmetic-failure probes were recorded as conservative-permitted observations,
not new precision requirements.

## Fresh verification and limits

Two fresh D-local exact-candidate clones were used. The floor sequence completed
before the dev sequence began. Every payload asserted actual executable, CPython
version and flags before Pontius imports, recorded the full identity, used `-B -P`,
snapshot-root cwd, snapshot `src` PYTHONPATH, a scrubbed environment, D-local
TEMP/TMP, and validated absolute Git. Receipt checks confirm unchanged manifested
source and clean clones after each payload. Independent probes were outside the
snapshots and invoked only the real public analyzer over inspected source bytes.

| Check | 3.11.15 | 3.14.6 |
| --- | --- | --- |
| `tests/test_inventory_and_profiles.py` | 119 passed, no skips; 310.910 s | 119 passed, no skips; 296.399 s |
| `tests/test_v0a_boundaries.py` | 18 passed, no skips; 57.818 s | 18 passed, no skips; 63.998 s |
| `tools/generate_test_inventory.py --check` | Exit 0; no mutation | Exit 0; no mutation |
| Independent 19-case authority/ordering probe | Seven confirmed unsafe acceptances | Same seven unsafe acceptances |
| Three explicit failure-order controls | All pass | All pass |

The probe command's exit 0 means observations were collected; it does not mean
the semantic checks passed. The raw runner reports eight unsatisfied expectations;
seven support R010-B-01 and the absent-global expectation is excluded as explained
above. The existing suite emits expected negative-CLI diagnostics. Python 3.14
also emits a SyntaxWarning for an existing pure finally-return control; its suite
still passes. These are not unresolved infrastructure failures.

Independent integrity checks establish all 2,860 earlier complete inventory entries
are unchanged, 13 entries were added, profiles are byte-identical to the repair
reference, the baseline blob remains `5fe6ee47f3380b65887b528efef05b72c8e6ac0a`,
and analysis limit constants are unchanged. The main-based diff preserves all old
CI steps and adds five hard CPU gates guarded by `!cancelled()`.

Commands, environments, source hashes, logs, script copies and receipt digests are
bound in `checks/codex-b-evidence-index.json`, SHA-256
`2dec720d453fbb86656b31eae6e1a88ab86791e06d5ebcf9f217fb5823e88417`.
The analysis is bounded to the declared repair and preservation contract; it is
not an exhaustive Python semantic proof. No full 17-target wall, guarded profile,
GPU work, owner/lifecycle execution, source seal, rehearsal, installation, commit
or push was performed. This non-clean review does not authorize broader gates.
