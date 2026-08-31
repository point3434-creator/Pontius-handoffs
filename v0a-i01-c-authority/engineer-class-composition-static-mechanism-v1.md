# Class composition: static mechanism leads and frozen extension v1

Engineering authoring/static inspection only. Not a cold review, production fix,
runtime mechanism finding, or permission to execute. Root inspects exact bytes
before either finite control scope. W was not edited; no payload was executed.

Pinned evidence and inputs
- Retained v19, engineer-generator-v19.py:
  3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1
- W remains v20:
  e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679
- Original four-case pack, unchanged:
  faa0026181653881737e15af0effe6e670fbad3ad20e684c1d019851dd0dd709
- Root's retained floor receipt:
  tests-checks/storage-composition-storage-composition-v19-01-311-receipt.json
  210890c5e24e2eb227a99fba0c5a859c131c53d77fa4cf41e6069d56275e001f
- Its log shows both shared-list checks pass and both original class checks
  fail their frozen requirements, with correct independent harmless traces.
  Unsafe class receives no blocker and an outer subprocess row; safe class
  receives helper-namespace blockers and no row.
- Root also reported the same two failures on 3.14, receipt SHA:
  c094edd7cc9cebf3c684644f03a590e4ba22393f58ba9cbfbff51351ec6b849d
  This note does not claim independent execution of either receipt.

All source line numbers below refer to retained v19.

1. Normal class adoption versus later review entry: unconfirmed causal lead
- _statements forks class_values at 23000 and clears only its bindings at 23003.
  At normal body completion 23026 adopts only class_values.authority.
- Helper completion 18463 also adopts authority, but 18468-18472 additionally
  raw-projects caller bound names from the adopted cells; class completion has
  no corresponding outer-name refresh.
- _call_environment 14437-14454 hydrates a callable's captures from live cells.
  Normal ast.Name evaluation 18594-18597 instead reads the projected name map.
- _snapshot_call 16140-16147 freezes the caller map before live helper effects;
  the call path invokes snapshot then effects at 19205/19212.
- Recursive local-helper body review constructs its entry from filtered
  source_flow.values_by_call at 25325-25329. Same-object inherited entries
  preserve that projection; this path does not call capture hydration.
- Therefore updated cells and stale projected names can be offered to different
  analysis stages. This is a coherence lead, not proof that one refresh fixes
  the observed public failures. The instrumented original-pair scope will show
  projected owner, bound cells, callable captures, call snapshots and recursive
  entries without assuming which stage determines the final result.
- Preserve the outer module='outer' projection and outer bindings. Adopting all
  class-local names would leak module='inner' and would be a different defect.

2. Protected-owner rebinding guard: separate earlier mechanism
- _assign 20764-20770 records a rebound nonlocal/global name during active
  helper effects, and emits a blocker if its previous value contains helper
  identity. This can happen inside change(None), before read() is reached.
- Helper completion 18475-18481 then replaces the rebound caller name projection
  with an unresolved value. This is distinct from refreshing a cell projection.
- The original safe log's class-call line 17 already has binding-change/effects
  blockers, followed by reader/mutation blockers. A class-end projection change
  alone must not be assumed to remove these earlier effects.
- The original safe case, its independent trace, and required-clean expectation
  remain frozen. This inspection does not reinterpret or weaken that contract,
  declare the guard correct, or authorize changing its scope.
- Scalar armed cases avoid this protected-owner rebind trigger while retaining
  a captured cell, a nested setter, class-body execution and a later reader.

3. Class-body exceptional flow: separate source-level seam
- ClassDef at 22171-22179 is delegated to _flow_expression_statement.
  That wrapper catches _ExpressionDoesNotComplete and returns its collected
  raised successors at 21619-21630.
- The class body itself iterates items at 23005 and calls _statements on each
  individual item at 23020; it does not use _flow_statements for the whole body.
- _statements handling of explicit ast.Raise at 22539-22542 only evaluates the
  exception/cause and returns the current map. The surrounding class-item loop
  can then continue to a later body item. This differs from _flow_statement_value
  21672-21740, which constructs a real raise successor.
- A raising call may instead record a throw and propagate
  _ExpressionDoesNotComplete through the shared throw collector. Such a path
  can leave class_values before the normal 23026 adoption, with class-local
  projection/bindings carried by a recorded throw state. This route also needs
  outer-namespace discipline, but the new six cases use direct ValueError raise.
- A normal-completion-only refresh is not a complete exceptional-flow design.
  Effect-before-raise and raise-before-unreachable-effect must be distinguished.
  No runtime behavior for the six new cases is asserted by this static note.

Frozen six-case extension
tests-checks/scalar-class-composition-cases-v1.json
SHA256 50e88cedf77f902012237ccd88700c911fa8f3681c8dada380cca6c3142659ac

Every case has outer module='outer', class-local module='inner', a local setter
of captured boolean armed, and read() that writes ReviewTests._launch only when
armed is true. Source bytes are reviewed, never executed. The independently
written Model oracle replaces the subprocess with a trace/returning sink.

- normal unsafe: False -> True; trace change/read/write; TypeError; refuse.
- normal safe: True -> False; trace change/read/sink; outer; clean argv outer.
- change then raise unsafe: False -> True, raise ValueError, caught outside;
  trace change/raise/caught/read/write; TypeError; refuse.
- change then raise safe: True -> False, same known raise/catch;
  trace change/raise/caught/read/sink; outer; clean argv outer.
- raise before change unsafe: initial True, unreachable change(False);
  trace raise/caught/read/write; TypeError; refuse; change and sink unreachable.
- raise before change safe: initial False, unreachable change(True);
  trace raise/caught/read/sink; outer; clean argv outer; change/write unreachable.

This extends coverage; it does not replace the original four cases. A raising
helper call, descriptor/metaclass failure and direct nonlocal syntax in the
class body remain explicit limits of this six-case set.

Probe and control, not executed
- tests-checks/class-composition-mechanism-probe-v1.py
  SHA256 4e2e0cb1f472a6cf7f0c38bd699f4fc54c084db29e5f903305e88f1358dbe83e
- tests-checks/class-composition-mechanism-control-v1.py
  SHA256 67cf68877e9c3daffe980360cdb0ff3c41d06237374dd4aab1f7f6892562702c

The control accepts only these finite scopes:
- original-class2 selects the two class cases from the unchanged original pack.
- scalar-class6 selects exactly the six frozen extension cases.

CLI, for later root dispatch only:
  LABEL SLOT SCOPE RETAINED_V19_PATH V19_SHA --control-sha256 CONTROL_SHA
For 314 also supply --floor-receipt PATH --floor-sha256 SHA.
Control itself requires actual 3.11.15 with -I -S -B -P. Children use exact
3.11.15/3.14.6 with -B -P, scrubbed environment/Git and snapshot/src PYTHONPATH.
The matching scope's floor must have completed all oracle/analyzer work with
intact infrastructure; a recorded semantic failure remains a failure and is
allowed as comparison evidence for the second runtime.

Each invocation creates a retained D-local r010 clone, verifies all 1761 tracked
files, overlays only the exact retained v19 generator, copies both case packs,
probe and control outside the Git snapshot, and checks tracked/input/W hashes
again afterward. The 60-second watchdog is infrastructure, not an analysis cap.
Logs, setup and receipt are create-only; no snapshot is deleted or reused.

Instrumentation delegates to original _statements, _call_environment,
_apply_helper_call_effects, _snapshot_call, _assign and _review_body. It logs
before/after class and direct class-raise handling, capture hydration, helper
effects, retained call maps, assignments and recursive helper entry.

Observations use dict.get on v19's actual dict projection and direct .data
dictionaries for bindings/cells/objects. They retain primitive JSON descriptions,
not FlowValues, AST nodes, analysis budgets or caches. Emission checks the
observed state's work counter did not advance. No consume/cap behavior is
patched. Original methods are restored at ordinary probe completion.

These traces can support or reject the normal-coherence lead and expose the
earlier guard independently. They are not cold-review evidence. Root must
inspect and authorize the exact retained control/probe bytes before payload.

Static authoring validation
The six sources and six harmless oracles were parsed with ast.parse, and hashes
were derived from their UTF-8 bytes. Probe/control source was also AST-parsed
under 3.11.15. No source body or harmless oracle was executed during authoring.
