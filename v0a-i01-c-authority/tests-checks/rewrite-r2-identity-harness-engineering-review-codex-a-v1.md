# R2 identity harness v1: bounded engineering review, codex A

Reviewer: codex/r010_cold_a
Design verdict: SOUND
Disposition: no blocker found in the assigned envelope, projector, population-loader, budget-preservation and result-replay scope. Root owns dispatch and the full custody review; the separate scalar-observer review remains independent. This is a static harness review, not implementation acceptance, runtime fitness evidence or a final cold review. I authored the prospective identity input pack and its population correction; their substantive expectations were not re-adjudicated here.

Frozen pair independently verified:
- H commit c00f7375a7be68daff773b4d8c6413467aa2e6be.
- rewrite-r2-identity-harness-v1-manifest.sha256: a2e7a238c4b87b46d6e48dad9106b13c39012fb674a4c0373b54873510815b5d.
- All ten manifest entries plus the manifest were read as Git blobs at that commit and matched local raw bytes and declared hashes.

Principal reviewed pins:
- Probe: 0c1d7065b21e7d45a002b2e83e3ada9e29a22e3129e9168378370f231500c5bb.
- Control: bb68e24c1d01b4b04eb499274c6d714c329ea8eab56cfb3a11f4394b92d5d2a9.
- Handoff: 2ea590ccf7594e5cff1d05556e9431e02e20737a90b9f7fb2d5396b5fda00216.
- Projector proof: 53e3a8bc69caed43acd0034dd9a40923d0547d942323a471efa537a9e7bb0e80.
- Observer map: a685562866deec86553d8ca06b458269f06e3f015418401325e7c4d43c1a232b.
- Plan: d4e3b07268e291863d90b35711485d1679f6ce826d01e3429604fdc375ae0182.
- Exact supported source: c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f.
- Population v2: 8ab800c1361ca53f4f294bd32e308ecb7061e031b60d32dc74d7fdf52cc5ce3b.

1. Envelope and original-code preservation

An independently authored stdlib AST/raw comparison verified thirteen definitions byte-for-byte and AST-for-AST against retained rewrite-r2-probe-v1.py (abc1a22b76691ab8881e5301f532fad32171183abb11221debc93e7428e48310): public_verdict, storage_oracle, storage_public_review, public_review, project_oracles, budget_context, budget_origin, budget_phase, BudgetObserver, validate_budget_metrics, helper65_source, generator70_source and prepare_depth_case. The original name-environment public_review AST and project_oracles raw segment also match their original probe. Both released predecessor diffs reproduce exactly.

The source receives only its frozen source bytes and existing public envelope. No region/scalar domain is supplied to derive_design_review. Source fixtures are parsed/analyzed, not used as runtime oracles. The two depth cases retain original c467 test-module identity, original builder bytes and exact helper/deferred-depth regexes. prepare_depth_case calls the original setUp, obtains that case's freshly loaded generator and verifies its source/caps. main calls the original _review with its normal include_probe default; it does not execute either large multi-subtest method. Each depth case's budget and mechanism observers bind that active generator module, not the unrelated first import.

2. Three-pack selection and separate Model projector

Probe lines 164–227 hash-bind population v2 and all three complete packs, validate pack schemas/exact integer counts, source/Model hashes and selected canonical record hashes, resolve envelope references, and return the frozen Gate B order. Lines 602–626 recheck all eight original descriptors and their original resolved envelopes against the retained early population. I independently confirmed all twelve references resolve and those eight comparisons hold. The new four identity descriptors remain tied to their coverage source/Model pins.

The fixed selection is four storage cases, two hidden-cell cases, two depth cases and four identity cases. It yields twelve public analyses and 4+4+0+16 = twenty-four Model projections; no old scalar-equality scale case is substituted. Classifications remain six clean, three refuse, one permitted-refusal and two exact-depth errors.

The new projector at lines 629–660 selects only oracle_source, parses the pinned harmless Model, disallows imports, and supplies the limited builtin set needed by those Models. Every projection gets a fresh namespace and Model(region); exactly true/false/none/other strings are required. Trace/result/ambient/work outputs and unreachable events are compared with the unchanged witness data. Its segment hash f3299d47ef623a54e1cedee1b6ce810a74f32f7a3deb3d07fa8daf531a29ddfd and all four source/Model pairs independently match the issued projector proof. This is a static transport/safety check, not execution of those Models or a second review of their substantive premise.

3. Original budget ownership, charges and reserve

BudgetObserver and its reconciliation are unchanged. Successful original initialization creates each observed epoch; consume records the supplied units before delegating once and rethrows the original exception. The exceptional request is included. The observer retains scalar accounting, not budget objects. Validation checks initial_work + requested_units = last_observed_work, completion/exception partitions, origin/phase sums and the exact original work-cap refusal.

The held consume source segment independently matches d910a8af42711e5130b93af9e55b8917dbd8b48433e29e1ab3cd51df63b7af5c; the child checks it before candidate import. Per-epoch reserve uses requested_units > 196608 only after execution, retaining initial and final observed work separately. No budget is reset, split, refunded or capped by the observer. Inclusive mechanism span counts remain overlapping diagnostics and cannot be added as disjoint original-work totals.

4. Replay and complete RED

Six predicate definitions are independently raw/AST-identical between probe and controller: load_cases, public_verdict, validate_budget_metrics, reserve_violations, validate_identity_inputs and validate_mechanism. Control lines 523–700 require fourteen complete LF JSON records in exact identity/twelve-case/summary order. They recompute Model, public/depth, accounting, reserve and mechanism results, enforce exact integer result counts/caps and reconcile the child exit code.

Observation completion is deliberately distinct from semantic/depth completion and success. A full baseline attempt may have observation_complete=true while completed=false because R1 lacks the required generator-depth result, or mechanism_ok=false because future R2 roles are unavailable. The controller retains that RED without converting it into a setup failure merely for lacking the new result. None of those states makes success true. Development replay still requires a matching successful floor across all gates; this baseline-only adapter cannot stand in for a future source adapter.

Missing/truncated output, unexpected exit or timeout cannot pass the replay predicate. The controller initializes failure status, retains raw/partial output, and requires completed, integrity, semantic, accounting, reserve, mechanism/restoration and integer exit zero for success. Observation_complete alone is not a claim of complete accounting or admission.

Limits and standing

Actual interpreter/bootstrap predicates bind floor CPython 3.11.15 and child slots 3.11.15/3.14.6; source identity is explicitly restricted to c8fc. Root must still inspect/approve dispatch. This review does not claim that the observer will finish within the 60-second watchdog or that either slot will satisfy semantic, depth, mechanism or reserve gates. Runtime overhead is not original charged work.

Static checks used only own stdlib AST/hash/data scripts, including all sixteen declared static-input raw pins. No candidate, test module, builder, Model, probe, controller or verifier-generated function was imported or executed. No existing artifact/source/test/population was edited. This create-only review is the only output.
