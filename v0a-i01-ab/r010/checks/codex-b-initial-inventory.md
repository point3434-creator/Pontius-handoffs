# Independent initial review inventory (before deferred coverage)

Reviewer codex/cold_review_b; frozen target 29c02f6fbd5eb0b7ddc9e816ef28f570b9839358.
Main comparison d1ed3cbda6107d61ea8e77133871720af04970cd; repair comparison
8d240db477b8c141e6142e055dbfbedc75c6a2f8. No coverage, prior review, peer review,
implementation report, ledger or transcript has been opened.

Manifest reconstructed directly from Git blobs using no-rename diff-tree,
lowercase SHA-256, two spaces, POSIX paths, LF rows and whole-row sorting.
Result 8741fa20b1ebc7e9e9d226f463680c603c348f1332bf19c8ae12b29579f76deb;
17 rows agree byte-for-byte with the supplied manifest. Receipt:
codex-b-floor-setup.json and codex-b-floor-manifest.sha256. Ten A/B blobs match
ddea6efbeb55cb8b71da1ebd5a359a0c2c901cf1, and the three other C source blobs match
00db06624ab25f10cd181badccf92c87a78f17ee. Actual repair delta is exactly three paths.

Initial sources: hashed handoff/candidate/manifest/acceptance/protocol and pinned
CLAUDE/workflow; frozen ADR-0484, relevant ADR-0485 component and acceptance map,
revised brief; generator declaration/function index, repair diff and source-ordered
callable/effect code; inventory suite public-review construction and provenance
fixtures. This is a bounded repair review plus preservation, not renewed review
of every accepted A/B line.

| Invariant / risk | Observable requirement and intended independent check | Relevant paths / seams |
| --- | --- | --- |
| Candidate and scope integrity | Exact blob manifest, 13 preservation matches, three-path repair, unchanged baseline/kernels/capability files | Full manifest, baseline dependency TOML, unchanged sealed modules, generated pair |
| Narrow C admission | Only six v0a origins; dependency/complete-deal separation handles aliases, relative/deferred/wildcard imports; old edges and SCC unchanged | boundary checker, v0a boundary suite, six preserved v0a modules, baseline |
| Source-point identity | Callee captured before args; aliases retain original object; names can rebind without granting old authority; class/module/local/global/nonlocal/imported scope differs | generator _ReviewRegistry, _SourceOrderedResolver, _ReviewFunction, _HelperProvenance, public design-capability review |
| Effective argument binding | Positional-only/defaulted implicit receiver and static all-default signatures follow Python; invalid args do not run body; unknown binding refuses | binder, descriptor selection, captured defaults, contract suite |
| Reached effect completeness | Relevant authority may reside solely in default, closure, receiver or nested container; incidental owner reads cannot change refusal; invocation mutates/refuses the reached authority | _FlowValue, _with_callable_authority, _reachable_helper_authorities, _apply_helper_call_effects |
| Opaque call and transfer | Returning, aliasing, storing and forwarding callable authority must preserve obligations or explicitly refuse later unknown execution/escape | return projection, native containers, member/subscript lookup, external call handling |
| Definition-time order | Decorator expression, defaults, annotations and decorator application obey construction order; class methods use source-point class defaults and lexical free names | callable construction, _record_callable_construction_obligations, class statements |
| Deferred effects | Generator/coroutine construction does not execute; real consumption/escape differs from unstarted close and proved empty/dead paths | deferred local generator, async call, implicit protocols, native-unstarted coroutine |
| Exception successor | Failed lookup is proved rather than inferred from absent state; exact NameError/AttributeError/TypeError successor controls reached rows; try/finally/handler effects persist | flow successors, evaluated callable snapshots, try/raise processing |
| Fail closed and bounded | Unknown owner/provenance, mutation/escape and unsupported semantics yield explicit blockers even with literal process argv; budget remains finite and source is never executed by analyzer | analysis budget, preclassification, source-ordered flow, public review |
| Direct unittest preservation | Discovery and entry preflight remain faithful; local/cross-file helpers and lawful default/read-only/dormant cases retain correct rows without blanket blockers | discover_test_sources, build_inventory, build_design_capability_review, suite |
| Ordinary census and assignment | Five v0a suites registered; every old assignment preserved; --check succeeds with no mutations or grants | STABILIZATION_TEST_FILES, test-inventory.json, test-profiles.toml, CI |
| CI reachability | Five clone-safe CPU gates added, all existing gates remain hard and reachable after earlier failures unless canceled | .github/workflows/ci.yml |

Adversarial probe families chosen before coverage: (1) authority retained through
containers/forwarders with rebinding and source ordering; (2) construction and
closure timing with class namespaces and annotations; (3) implicit protocol,
generator/coroutine consumption versus proved nonexecution; (4) exact failed-call
exception successors. Use independently authored harmless runtime projections
only, and pass sensitive source bytes solely into the real public analyzer.
Tests will execute in fresh D-local exact-candidate clones, actual 3.11.15 first
then actual 3.14.6, full identity before Pontius imports, -B -P, snapshot cwd/src
PYTHONPATH, scrubbed env, D-local temp and validated absolute Git. No full wall,
GPU, lifecycle owner, source seal, rehearsal or dependency install is permitted.

Open limits: inspect the bounded replacement's actual propagation and tests before
claiming any family complete; supported Python subset is finite. Missing coverage
alone is not a defect. Prior implementations are code-only comparison objects.
