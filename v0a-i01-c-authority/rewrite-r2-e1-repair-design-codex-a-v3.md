# R2-E1 builtin authority repair design, codex A v3

Engineering design only; no source change, candidate import, analyzer execution, Model execution, or fixture is authored here. Author: codex/cold_review_a, an engineering participant and the E1 input/harness author, not a cold reviewer.

V1 SHA-256 `2e4eba3bd4af7fdcebbdf58de28997be90398ec76421fb0d1d8d3e05483bfd11` and v2 SHA-256 `98b8c09445425ed03d98c6293684c87c4ec94ddb126b3e996e590de17cae3fd1` remain immutable and are superseded. V2 correctly modeled creation-time builtin provenance but incompletely limited its consumers to six explicit Name fallbacks. Admitted `ClassDef` also consumes captured `__build_class__`, and admitted `Import`/`ImportFrom` consume captured `__import__` without ordinary global-name lookup. Planned checkpoint-3 `range` and `sum` are additional explicit fallback producers, and its `GeneratorExp` is another function-like authority carrier.

Bound source: H `beff8193e9d5ce7316f5006fccc77ffcb5ca5695`; source manifest `ef3561cb462fcbd31dda7d3774ea34d00c575b7549dc1cc804ad9f92e11c582b`; `rewrite-r2-checkpoint2-source-v1.py` SHA-256 `7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d`. Bound canonical census: `rewrite-r2-e1-canonical-write-census-v1.md` SHA-256 `5640242a28caa83b61c08f1c2ac699823fcae53d38ce74b63dd4c579033e6efb`.

Retained root-verified RED evidence is `coordinator-r2-e1-red-verification-v1.json` SHA-256 `6d17bd8218f008e54d90fbadffc47feb57f5e0c1b2522021d8fc1c6841b2ded2`, binding receipt `2040b896281e161f5fee285bc7c62506a867a1dc168feadc96f89ddd4fd4bd00`. E01/E04 are clean; E02/E03 are wrong-clean. No evidence is rerun here.

## Single authority representation

Add one required immutable positive field, `builtin_fallback_proved: bool`, to every `_CFunction` and executing `_CFrame`. It means that the function-like object captured the ordinary builtin environment at its actual creation point. A function record owns the historical fact; its invocation frame is only the execution projection. Never recompute it from the caller or current module at invocation.

Use one creation helper:

`created_proof(state, executing_frame) = false` if the current module namespace has a `__builtins__` member; otherwise it inherits `executing_frame.builtin_fallback_proved`.

Presence is unproved regardless of the modeled value. There is no custom-builtins interpreter. Absence is not universal proof: code executing in a function that already captured an unproved environment cannot launder it by deleting the module key. The initial module frame is proved true because the public analyzer starts module execution in its ordinary builtin environment.

The proof is consulted in two ways:

1. An explicit unqualified Name first uses the ordinary lexical/class/module route. Only an absent module name may enter the centralized explicit-builtin fallback table, which then requires the frame proof.
2. An opcode-level builtin consumer such as class construction or import uses a separate central frame-proof gate. It does not consult a module/global binding with the same spelling, because `LOAD_BUILD_CLASS` and import opcodes use the captured builtin environment directly.

This is one semantic truth. Module membership participates only when a new function-like record captures its environment. Reached consumers read only the executing frame projection.

## Complete builtin consumer inventory for the admitted scope

### Explicit absent-module Name fallbacks

The current table contains exactly six names:

- canonical exception types: `ValueError`, `TypeError`, `KeyError`, `IndexError`;
- canonical symbol producers: `staticmethod`, `__import__`.

Checkpoint 3 must extend this same classified table with canonical `range` and `sum`; it may not introduce direct spelling checks or independent proof. A real lexical, class, or module binding wins before the table. Unproved reached fallback calls `_c_fail`; dormant definitions are not refused merely for retaining false provenance. Every future explicit builtin producer must be added to this table and its source/value producer inventoried.

### Implicit builtin consumers

- Every admitted `ClassDef` consumes captured `__build_class__` at the class statement's `LOAD_BUILD_CLASS` point.
- Every admitted `Import` alias consumes captured `__import__` once for that alias.
- Every admitted nonrelative, nonstar `ImportFrom` statement consumes captured `__import__` once before any imported-name binding.

These consumers require the frame proof even if the module has an explicit member named `__build_class__` or `__import__`. Under an unproved frame, conservatively refuse; do not interpret a custom map or execute a hook.

No other admitted operation reads a builtin-environment name implicitly. Canonical literal/container construction, identity, native range cursor iteration, generator resume, member/subscript access, method binding, and exception matching use their proved records/protocol boundaries rather than a name from `f_builtins`. Their existing proof/refusal rules remain. If a future admitted operation does consult a builtin-environment name, it must extend this inventory before implementation.

### Function-like authority carriers

- `FunctionDef`/`AsyncFunctionDef` records capture the creation helper result after admitted decorator/default effects and before `_CFunction` allocation.
- A class-body function-like frame captures at class-body function creation, before base-expression effects; methods later created while executing the class body independently use the then-current state and that class frame proof.
- Checkpoint-3 `GeneratorExp` must capture the same proof at its actual function-like creation point, before evaluation of the eager outermost iterable, retain it on the canonical generator/function-like record, and project it to every resumed implicit frame. Later module changes or the resuming caller cannot alter it.
- Any later function-like record follows the same capture/project rule. No live function-like body may execute with a defaulted or recomputed authority.

## Exact source-order gates

### Ordinary functions

In `_c_construct_function` at source line 10695, keep header validation and admitted decorator/default evaluation. For every normal successor at 10736, compute the proof from `prior.state` and the current frame immediately before allocating the `_CFunction` at 10768. Captures/defaults and the proof belong to the same successor. Invocation in `_c_call`/`_c_invoke` copies the selected record's proof into the local `_CFrame`; entry, helper, bound method, recursion, and historical calls share this site.

### Class statements

The current `_c_construct_class` at 10776 begins base evaluation at 10783 and has no `__build_class__` gate. For an otherwise admitted header:

1. Read the current frame proof at the `LOAD_BUILD_CLASS` point before `_c_eval_many(node.bases)`. If false, return the existing conservative refusal without evaluating any base, class body, class-name binding, or later effect.
2. From that same pre-base state and executing frame, compute and retain the class-body creation proof. This timing matters: base effects occur after class-body function creation and must not retroactively change its captured builtins.
3. Evaluate bases using the existing ordered outcomes. Construct each class frame at 10806 with the retained pre-base proof. Method/function definitions reached in the body still compute their own proof from the post-base/current body state.

Unsupported class decorators, keywords, type parameters, or inheritance retain their existing refusal boundary; this design grants no new header precision. The implicit gate is required for the already-admitted path and must precede its base/body effects.

### Import statements

The current branch at 10565 directly constructs a symbol and writes its alias. Add the implicit proof gate at each real import operation:

- For `Import`, gate each alias on each normal predecessor before creating the qualified symbol or calling `_c_store_name` for that alias. Earlier aliases remain ordered effects if a later alias refuses.
- For an admitted `ImportFrom`, gate once for the statement before creating or binding any imported alias; a multi-name from-import performs one implicit import call. Relative and star forms keep their existing unsupported refusal and gain no execution claim.

A failed gate has no alias/binding effect. It uses the captured frame proof, not current module membership and not ordinary `_c_read_name("__import__")`.

### Initial and deferred frames

The sole initial module `_CFrame` at 11389 supplies true. The class and ordinary-call frame constructors supply their computed/recorded value. Checkpoint 3 must add the generator implicit-frame constructor to this exact constructor census and source-order proof. No default is permitted on the field.

## State, history, and joins

`_CFunction`/future generator records remain immutable objects in the canonical object table, so aliases, members, containers, returns, forks, snapshots, recursive observations, and later calls retain the proof automatically. `_c_join` retains ordered outcomes rather than merging object records; distinct creation successors keep distinct proof-bearing refs. A later module deletion/rebinding changes no prior record.

The creation helper reads the exact successor state. Module ordinary/chained assignment, exact destructuring, name deletion, supported import alias, and supported definition stores named `__builtins__` therefore participate through the existing namespace writer. Function-local and class-local spellings do not change module membership. Existing refusal remains for reflection, relative/star import, unsupported targets, and unproved declared writes. No new namespace field, monotonic poison bit, or parallel builtin-authority map is needed.

## Required behavior

- E01: method proof true; explicit `ValueError` fallback remains admitted.
- E02: module key present during class/method creation; method proof false; reached fallback refuses.
- E03: false method proof survives later deletion and refuses.
- E04: local spelling changes no module authority; method proof remains true.
- An unproved body that never reaches an explicit or implicit builtin consumer is not blanket-refused.
- A proved currently executing module frame may still perform an import or `LOAD_BUILD_CLASS` after assigning the module key, because those opcodes use its already-captured environment. Functions/class bodies created while the key is present are nevertheless unproved.
- A real explicit binding of `ValueError`, `__import__`, `range`, or another table spelling follows ordinary binding semantics; it does not prove the corresponding implicit opcode consumer.

## Minimum prospective coverage beyond E01-E04

The exact T01-T03 source forms in `rewrite-r2-e1-repair-design-v2-coverage-addendum-codex-a-v2.md` SHA-256 `b3da849d0ccedc2d675a98fa7d07a5ed90c3de3a204af961cef4e24b0bd824ec` remain the minimum creation-rule matrix:

- T01: set empty; define `ReviewTests.test_static` false with a synchronously created/called inner function containing `ValueError()` then launch; delete the key after the class. Required refusal.
- T02: define the class/method true with the same inner function; set the empty key after the class. Required refusal.
- T03: set empty then delete before the class; define the method with direct `ValueError()` then launch. Required clean exact launch.

Two additional unsafe cases are necessary because T01-T03 could pass while implicit opcode consumers still bypass the authority:

1. **Implicit class witness.** Import `os`, `subprocess`, `sys`, and `unittest` before the override. Set module `__builtins__ = {}`, define `ReviewTests.test_static`, then delete the key after the class. The method executes `class Local: pass` and then the launch using module-imported `os.environ`, with no `ValueError` and no explicit `__import__`. Required explicit refusal. Its harmless Model creates the method body under empty builtins, deletes the globals key, and observes failure at real nested class construction (normally `NameError` for `__build_class__`) with no launch marker.
2. **Implicit import witness.** Import only `subprocess`, `sys`, and `unittest` before the override. Set module `__builtins__ = {}`, define `ReviewTests.test_static`, then delete the key after the class. The method executes `import os as launch_os` and then the launch using `launch_os.environ`, with no `ValueError` and no explicit `__import__`. Required explicit refusal. Its harmless Model creates the body under empty builtins, deletes the globals key, and observes real import failure (normally `ImportError` because `__import__` is unavailable) with no launch marker.

The two witnesses are separate so one implicit refusal cannot mask the other. A separate `ImportFrom` runtime case is not required for this minimum if the static proof establishes its distinct once-per-statement gate and shared authority helper; if implementation duplicates rather than shares the path, each branch requires independent static closure. Sensitive source remains AST-only; Models use no process/file operation. Inputs and harnesses require separate authorization.

## Work-accounting obligations

Use only the original `_AnalysisBudget`; do not change caps, reserves, epochs, or exceptions.

- Creation helper: retain the existing namespace/object read, charge the `__builtins__` membership probe, and on absence charge the executing-frame proof read. Presence returns false without interpreting the value.
- Each retained proof field is one charged record field/reference-sized scalar: `_CFunction`, each `_CFrame`, and the future generator/function-like record/frame. Update every aggregate constructor charge and exact constructor census.
- Explicit fallback: charge the classified immutable-table lookup for every absent module name, the matched frame-proof read, and the actual kind branch. Existing value/object/refusal work remains separately charged. Checkpoint-3 `range`/`sum` branches add their own record/call work.
- Implicit class gate: charge the frame-proof read/branch before any base work. Computing the class-body proof separately charges its namespace membership and possible inherited-frame read. Carrying the scalar through base successors must charge any actual tuple/record/reference storage if implementation allocates it.
- Implicit imports: charge each real frame-proof read/branch at the frequencies above. Existing alias-loop visits, atom construction, and binding work are unchanged and may not be relabeled as gate cost.
- Every helper call, comparison, allocation, installed reference, outcome, issue, and trace added by the implementation remains explicitly accounted. A false gate must not charge skipped base/body/import-binding work.

R2 cumulative raw `SequenceMatcher(autojunk=False)` accounting is 360 added+deleted lines before this fix against the separate 1500-line ceiling. Report exact successor delta and cumulative count. R1 binder bytes/normalization, five original caps, protected16, original expectations, and 1761-file base remain exact.

## Static closure before any dispatch

- Exactly one ordinary `_CFunction` producer and every `_CFrame` constructor supply the required proof; no default/recomputation exists.
- The current explicit table contains exactly the six current producers, and checkpoint 3 extends the same table with `range` and `sum` before those producers exist.
- No `_CExceptionType`, `staticmethod`, explicit `__import__`, range, or sum producer bypasses the explicit gate.
- Every admitted `ClassDef` reaches the frame-proof gate before base/body effects; class-body proof is computed pre-base and methods compute from their reached body state.
- Every admitted `Import` alias and `ImportFrom` statement reaches the implicit gate before symbol/binding effects, with the exact frequencies above.
- Explicit module names cannot satisfy an implicit gate; implicit consumers do not call `_c_read_name`.
- Function, class-body, and future generator creation use the same helper; calls/resumes project the retained record proof.
- Local/class `__builtins__` remain nonmodule routes; supported module writers/deletes are covered; no custom map or blanket reserved-name ban appears.
- All new operations have source-site accounting; false gates have no skipped-work charges.
- Binder, protected16, caps, raw line count, source/census/watch, existing case bytes, and public envelopes pass their retained static checks.

## Design verdict

Recommend this v3 design. Immutable function-like provenance plus a projected frame field remains the smallest sound history representation. Category completeness additionally requires central implicit gates for `LOAD_BUILD_CLASS` and import opcodes, correct pre-base class-body capture timing, and checkpoint-3 integration for `range`, `sum`, and generator frames. The five prospective cases are the minimum nonmasked coverage: T01-T03 for creation truth, one nested-class consumer, and one import consumer. This preserves dormant precision, later-deletion history, source-order effects, and the no-custom-builtins limit without a second authority engine.
