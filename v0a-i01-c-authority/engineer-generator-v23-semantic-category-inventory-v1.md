# Semantic v23: bounded implementation inventory

Engineering authoring only; not cold review, not a runtime result. The candidate
was produced from exact retained v22. W remains exact v20. No source fixture,
Model, oracle, public analyzer, candidate module, test or payload was executed.

Candidate SHA256: 53a17d52196bd83a540ebf4892d3687f3efbe9633d1539fa834ea0a27f0db499
v22 SHA256: 61a0ce3bc3ea59bc09a7b14d45da843fb3c3a8614feb4c913132b67028916da3
Disposition SHA256: d5b1d838a1d5bbbf591dff8974c7c8d7fb8e0a033477573b9c8143d92d1dd72a

The companion static JSON is the exact node/method boundary, AST/source pins,
runtime flags and W watch. Every preexisting top-level node outside its nine
allowed changed nodes remains byte/AST exact. The complete v22 name-store
region, all 27 named primitives, certificate/mutation bodies and budget/caps
remain exact. The two cell-method bodies are exact; only key annotations
change. The ordinary comprehension body is checked against its old AST after
removing the two optional first-iterator substitutions (defaults None/False).
The only local token allocation remains ExecutionState's local_names boundary;
class comprehension targets use that same real lexical activation boundary.

| Category | Shared implementation | Frozen evidence / remaining gate |
|---|---|---|
| Store/Del-only and forwarded captures | Scope-aware binding/capture visitors, retained callable_scope, callable-record-only incoming bindings | Original scalar/class cases; C01–C06, C09; runtime rerun pending |
| Ordinary global reads versus lexical proof | Plain-int placeholders keep ordinary read projection; explicit global barriers cannot inherit caller-local proof; no blanket refusal for ordinary global capture | Existing authority/public packs remain required; no new global clean claim |
| Precise nonlocal writes and deletes | One destination predicate under call snapshot, Name write/delete guards and callee binding construction; proved writes never enter rebound poisoning | Original protected-owner pair plus scalar polarities, C09/C10; runtime pending |
| Missing/alternative evidence | Per-record proof validation before record union; missing retained lexical cells refuse; scope conflict/missing evidence is not restored from surviving tuples | Existing authority families required; no fabricated ID witness |
| Current contents, stable ownership | Class frame keeps enclosing binding identities; current successor cells supply contents; helper adoption and class exits refresh raw projection | Change-then-define C05/C06 and forwarded factory C03/C04 |
| All outward class exits | One flow driver uses successor kinds, stops on no normal path, retains raise tag/explicit/exclusions, projects each outward state through namespace exit | Existing explicit-Raise scalar schedules and C01/C02 known call-raise |
| Compound/nested frames | Resolver frame lives across If/Try/handlers/finally and nests/restores in finally; reached immediate method authorities remain retained | C07/C08; further nested-class/compound coverage remains a runtime obligation |
| Class-local shadow/fallback | Own immutable scope sets; raw unbound mask; actual stores/deletes/imports/definitions/handler/pattern bindings use shared guard | Fixed N01–N08; no value-identity heuristic |
| Repeated projected absence | Class projection join normalizes unbound/maybe-unbound for locals and eligible free bindings and retains helper obligations; binding-plan cell writes remain owed | Deletion/maybe-bound/repeated-join schedules not yet all executed |
| Direct declarations | Nonlocal routes only proved enclosing lexical cells; reached unrepresented nonlocal and class module writes/deletes explicitly refuse, including raised exits | N05 required refusal, N06 permitted; N07/N08 required conservative refusal |
| Historical recursive review | ReviewFlow retains the actual callable alongside its historical state; recursive local body review uses shared capture hydration | C11 entry-without-row RED must become an actual supported row; no private ID/count oracle |
| Eager implicit scopes | First iterable executes in class; targets/body use an enclosing nonclass activation over current cells; normal/raised effects use shared namespace projection | Independent Q01–Q04 frozen after design; no candidate run |
| Deferred class generators | Creation still evaluates only the first iterable; a retained marker refuses reached nonempty/changed-iterator consumption because no persistent lexical view is represented | Q05/Q06; no widened deferred precision promise |
| Eager callable metadata | Defaults/decorators remain evaluated in current class context; synthetic annotation/construction projections explicitly capture that context, while real bodies skip class locals | Existing definition-time and descriptor coverage remains required |
| Prepass and other contracts | Helper-disabled direct dormant method shortcut remains; normal nonclass comprehension body stays equivalent; attribute/subscript/reflection guards unchanged | Old public24/design53/matrix/coordinatorjoin/weakwrite/lexical/A19/B18 remain required unchanged |

The old 8 class cases plus shared-list pair remain unchanged and separate from
the 12-case extension and 8 Name witnesses. The 12-case classifications remain
6 clean / 5 refuse / 1 permitted refusal. The Name witnesses remain 2 clean /
5 refuse / 1 permitted refusal. B18 still requires its additional excluded
case; nothing here changes or substitutes a frozen scope.

The implementation does not recover correlations already merged by helper
normal/exception completion, promise descriptors/metaclasses/TryStar or
unsupported AugAssign, or add defining-module global-write precision. A known
always-raising helper stays within existing exception precision. Deferred class
generator consumption intentionally remains conservative. Generic downstream
nonclass join precision is not broadened by the class-specific presence merge.

Remaining verification: root source inspection, all frozen semantic packs on
fresh floor-first snapshots, independent comprehension witnesses, the old
authority/regression packs, cost fitness and eventual cold review. This artifact
claims only static construction/preservation. It makes no GREEN, corpus-fitness,
storage-fitness, merge or integration claim.
