# Storage prototype: independent oracle plan and release v2

Engineering author: codex/cold_review_a. Scope is the bounded T-only storage prototype accepted by coordinator-storage-disposition-v1.md SHAa5eaf456fa762b23ec3ccd23b46ee49cd52cb140410e42c98c3fdd514091d793. This is not a cold review, production integration, authority-model rewrite, or acceptance run. I read only the disposition, declared API/clarification, and my own oracle artifacts; I did not inspect the prototype implementation.

The coordinator selected prototype v2 SHA22cc3966435fd4e6e0cecbcbb242275e72d34b36c835b4e960c7c712613822ff. API inputs are engineer-storage-api-v1.md SHAffb03bce78dc3ed21a31515e4dc6fdf10cb1a5a9171997badbbfd5093f62a32d and engineer-storage-api-clarification-v1.md SHAa0269be3603c5f631a5c1fb8437f0f5791c2028601c711a6b8efb23f4a866116. The oracle adapter was authored only after that API was declared.

## Frozen scope and counts

The immutable v2 pack contains28 cases and336 explicit operations: all20 v1 compatibility schedules are structurally unchanged, plus the coordinator-requested8-point cost grid. Maximum scheduled operations per case is25. Keys are exact ordinary strings decoded from JSON; there is no custom hash/equality subclass probe. Largest cost-grid root is64 names. The two failure cases each have3 bounded fault/retry trials, so each child plans28 baseline runs plus6 fresh fault replays =34 runs. No unbounded fuzzing or generated runtime loop is part of the operation language.

Six serial children cover actual3.11.15 then3.14.6, with per-child PYTHONHASHSEED0,1,17. That is204 scheduled baseline/fault runs overall. This is a plan, not execution evidence. No payload has run at issuance. Execution is held for the coordinator's pinned control/configuration review.

## Independent reference semantics

The reference uses only ordinary built-in dictionaries. New/set/overwrite/delete operations use ordinary dict operations; forks copy a dict. No expected output comes from a prototype field or method. Values are shared immutable symbolic tokens. Reusing a value label supplies the same token object; a merged alternative token explicitly records ordered input alternatives and missingness. The pure merge law returns the identical token if every input supplies that token; otherwise it returns a deterministic merged token. This makes callback input order and stored-value identity observable without production authority objects or owners.

Reference empty joins produce an empty dict; singleton joins copy the input and preserve its order. For two or more states the reference literally evaluates:

    names = set().union(*(state.values.keys() for state in states))
    for name in names:
        result[name] = merge(name, tuple(state.values.get(name, MISSING) for state in states))

Every predecessor result is an ordinary dict in its own previously computed legacy order. Thus nested merge order, deletion/reinsertion and metadata-only new order recipes are compared against the actual legacy algorithm within that child. No hash-dependent order literal is frozen in the pack. The child records its requested hash seed and hash(alpha) as diagnostics; expected order is recomputed using that child's builtin set/dict behavior on every reference join.

The no_work flag is explicit test metadata, not a production classifier. Raw/default set clears it even for the same token. The reference records which names must invoke a callback: any missing/different input or pending input. Actual callbacks must receive the exact per-name input tuple in input-state order, preserving token/MISSING identities. Every required changed/pending name must be called; unchanged certified values may be shared. The pure callback invocation order across distinct names is not asserted, as explicitly clarified by the storage API. This freedom does not authorize reordering production transfers, cell writes or source-point effects.

Exact ordered_items tuples, key order, values by identity, lengths, get/default identity, missing-delete KeyError, retained-version results and previously returned immutable tuples are checked. No AVL node, version ancestry, certificate field or cache field is inspected.

## Compatibility schedules

- empty-singleton-and-missing: empty versions/forks, zero/singleton joins, repeated empty reads, missing get and missing deletion.
- overwrite-retains-position: existing-key overwrite, identical raw overwrite and retained old versions.
- delete-reinsert-appends: middle/first deletion and reinsertion, historical versions and missing deletion.
- retained-sibling-forks: independent sibling changes, retained intermediate snapshot and later join.
- same-content-order-only-merge: unrelated roots with identical values and different insertion histories, then two merges without value changes.
- order-only-merge-then-edit: new merge order followed by overwrite, append and delete/reinsert.
- raw-identical-set-clears-metadata: identical token installed pending, required callback, then another unchanged join.
- metadata-only-distinct-versions: pending/certified versions with identical values, preserving callback obligation and order.
- unrelated-disjoint-roots: both input orders, missing alternatives, repeated reads and get.
- unrelated-equal-overlap: overlapping roots with identical shared tokens, then a three-input join.
- unrelated-different-overlap: different overlapping values, opposite input orders and a later merge of merged results.
- unrelated-construction-order-history:17-key roots built in different orders and terminal read after nested joins.
- terminal-after-linear-merges: four nested merges with overwrite/deletion/reinsertion/addition; no prototype ordered read before the terminal read.
- terminal-after-balanced-merges: multiple sibling branches and balanced merges before terminal realization.
- terminal-overlap-reinsertion-history: retained merge snapshot, deletion/reinsertion and successive order recipes.
- retained-growth-ascending, retained-growth-descending, retained-growth-zigzag:17 bounded insertions, retained intermediate versions and final delete/reinsert/join.
- failed-order-linear-history and failed-order-balanced-history: pristine realization calibration plus first/middle/last bounded interruption and retry on the same version.

After each case's scheduled operations, every retained version receives an ordered read. Those audits occur after the terminal operations, so they do not silently warm prototype order caches before the intended terminal materialization. Previously returned tuples are rechecked after all later edits.

## Requested cost grid and accounting

The8 new cases are cost-grid-n{8,64}-j{2,4}-d{0,2}. Each starts with N certified unchanged ambient tokens. Each of J rounds forks the current version, changes either zero or exactly two separately named entries, then joins the two successors. Only after all joins does the terminal version receive an ordered read and two repeated reads. All retained versions are audited afterward.

Public Meter.used and Meter.counts deltas are reported separately for construction, joins, terminal_order, repeated_order, retained_order_audit, lookup_audit, validation, meter initialization, and failed/retry operations where applicable. All phase units must sum exactly to meter.used. First and repeated ordered reads remain in the report; delayed materialization is not counted as free. External len/order/value assertions are a separate validation phase. No absolute timing, new asymptotic threshold, zero-copy requirement, or prototype-internal counter is asserted. The coordinator will compare finite measured costs with the ordinary-corpus requirement separately.

## Failed materialization and precise transaction boundary

Each failure schedule first builds a pristine independent version with Meter limit262144. The oracle captures used/count deltas immediately around its first ordered_items call, before any external len or validation read. Call this primitive-only cost C. Fresh independent replays build the identical version/history without prior ordered reads. They temporarily set the public limit to used_before +0, +floor(C/2), or +(C-1), respectively, preserving used/counts. Each attempted ordered_items must raise the public BudgetExceeded and retain the spent/throwing charge.

The limit is restored to262144 without resetting/refunding spent work. On the SAME failed version, the next ordered_items must produce the expected complete legacy tuple, with exactly the pristine C used-unit delta and exactly the pristine per-category public Meter.counts delta. Only that primitive call is compared; validation follows afterward. This public subsequent-cost equivalence is the cache-publication check, not merely eventual value equality. Repeated successful reads and later retained-version reads are still measured. No direct cache introspection is used.

V1 oracle/data remain immutable and unexecuted. Coordinator review caught that v1's pristine helper included an external len(version) while its injected call did not; v2 corrects that calibration boundary. V1 also used a weaker retry-cost inequality; v2 requires exact used and public-count-delta equality. These corrections occurred before any payload. The20 compatibility operation schedules are unchanged; the new8 cost cases are an explicit coordinator-requested extension.

## Release artifacts and invocation

All paths below are under D:/Pontius-handoffs/v0a-i01-c-authority/tests-checks:

- storage-oracle-cases-v2.json SHA3bd5678da334fb551c2f179906e8b4d2cf7a0b0e7a3779e0fad2fb4b4a9c548f,34304bytes.
- storage-oracle-v2.py SHA6a58ef82832d53510f7d44d58cf5a8fa3764f8be5f2c28dcb7e555a83c72cfba,16157bytes.
- Preserved storage-oracle-cases-v1.json SHAb29d540442d7069cc046118826342e195ce1ed0aac0899eff84e619520cbfc3c,21029bytes.
- Preserved storage-oracle-v1.py SHA109386a2b01fd208a302df2742c7dde2c59a8a0fca209a7ff08dd1717ca0d8c9,13443bytes.

The declared import interface is verify_storage(prototype_module, case_path). It returns a JSON-serializable summary and prints detailed per-case/cost records. Importing the module itself runs no tests. The module hash-checks the supplied case bytes and asserts28 cases/336 operations, supported actual runtime, safe-path/no-bytecode flags and one of the three explicit hash seeds. The coordinator owns the wrapper/control, earliest executable/patch identity checks, pure-stdlib fresh D-local snapshots, scrubbed environments and hash-bound source/configuration checks. Children must not use-I because it ignores PYTHONHASHSEED; the proposed child flags are-S -B -P. No host-wide environment setting is changed.

The coordinator reviewed v2 oracle/data and approved them for the forthcoming six serial children subject to control/configuration review. Source/data are now held immutable. I have performed no prototype/oracle payload execution and inspected no prototype implementation. No W/primary source, tests, generated artifacts, protected fixture body, owner, GPU, broad suite, package install, cap edit, commit, push or ledger action is involved. The public24-case authority family remains unchanged for later production integration; this storage oracle does not replace it.
