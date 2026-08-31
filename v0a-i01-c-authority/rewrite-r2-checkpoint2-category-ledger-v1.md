# R2 checkpoint 2: category and new-work ledger

Engineering implementation checkpoint only; source held for coordinator review. No candidate import, analyzer, Model, test, or runtime acceptance run. This is not an independent cold review.

Source: `rewrite-r2-checkpoint2-source-v1.py`, SHA256 `7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d`.
All line anchors below refer to that retained source. Checkpoint delta: 242 additions + 21 deletions = 263 lines. Cumulative R2 delta from R1 c8fc: 314 additions + 46 deletions = 360 of the 1500-line ceiling.

## Authority and bounded coverage

Authorizing disposition: `rewrite-r2-source-checkpoint2-disposition-v1.md` SHA256 `5c0e09c4bdda13848f78827ef139a0776859ec4eaf59fd3da76a003fed340b5b`. The implementation follows the retained R2 plan and normative addendum: explicit proved builtin exceptions, bounded Try/Except and exact unary minus; no generators or deferred-depth changes.

| Category | Implemented boundary and limits |
| --- | --- |
| Builtin class proof | `_c_read_name` 9961–9968 is the sole `_CExceptionType` constructor. Real lexical/module bindings win before the module-fallback proof for ValueError, TypeError, KeyError, IndexError. Import/qualified symbols with matching text are not proof. Missing unmodeled names retain refusal. |
| Class identity and aliasing | Class proof is a distinct immutable value, not a newly allocated object reference. Repeated lookup cannot produce falsely unequal object IDs. `_c_identity_compare` remains exact checkpoint1 bytes and conservatively returns BooleanUnknown for this new alternative; key/dataclass equality never proves runtime identity. Aliases retain the proof value. |
| Instance construction | `_c_invoke` 10877–10882 admits only empty calls on exact class proof. Each `_CException` receives a fresh canonical object ID using existing allocation/store APIs. Construction returns normally; mere construction does not raise. Other arguments remain refused after ordinary operand evaluation. |
| Catchable producer | `_c_raise_known` 10419–10430 requires a current canonical exception record. Explicit Raise is its sole caller, at 10606. It retains the exact exception reference, tag, origin, explicit flag, state, and trace; it adds no unconditional issue debt. Class-form Raise, bare Raise, cause, custom exceptions and unproved values refuse. |
| Current handler proof | `_c_exception_matches` 10433–10454 admits exact proved classes or a current native tuple whose every element is an exact proved class. It scans after an earlier match; a later invalid/unproved member refuses. Nested tuples refuse. Only the four distinct exact tags match; no implicit superclass hierarchy is added. |
| Handler source order | `_c_match_known_handlers` 10465–10517 evaluates reached handler expressions against the raised successor's current state. Lookup effects/abrupt outcomes are retained. Matched handler execution uses that state, not the pre-try state. Sibling handlers cannot catch a newly raised handler result. |
| Handler consumption | `_c_handle_known_exception` 10457–10462 clears only the consumed active exception metadata by starting a normal outcome, retaining issues and trace. Any new raise/refusal/return from the handler is retained. Binding an exception name and bare handlers are outside this checkpoint and refuse. |
| Try and else | `_c_try` 10520–10541 routes normal body results to else, known raises to handlers, and all other controls unchanged. Else exceptions are not caught by those same body handlers. Finally refuses before body execution; TryStar remains unsupported. |
| Negative literal | `_c_eval` 10380–10396 admits unary minus on an exact literal int/float only, excluding bool and user protocols. It evaluates the operand once and retains abrupt outcomes. |
| Escaping evidence | `_c_review_outcomes` 11079–11095 turns only active escaping known raises into terminal blockers at their immutable origin. Missing active proof metadata raises InventoryError. Historical call summaries are never scanned as terminal exception debt. |
| Existing core | No changes to state ownership, forks/snapshots/joins, cell/object writes, lexical facts, function/class construction, binder, caps/budget, sink/native writer, or public entry policy. New metadata increases actual outcome/call costs; no discount or new budget epoch. |

The coordinator's upstream check of CPython 3.11.15 confirms flat tuple validation before matching: [CHECK_EXC_MATCH and check_except_type_valid](https://raw.githubusercontent.com/python/cpython/v3.11.15/Python/ceval.c), lines 3689–3699 and 7169–7190. This checkpoint's own source inspection verifies the complete-member condition described above; no CPython or fixture reproduction was run.

## All six legacy diagnostic producers remain uncatchable

Their call ASTs remain byte/AST-equivalent to checkpoint1. Central `_c_fail` 9919–9928 now always produces `control="refused"`, an unsupported issue, and no active exception metadata; old diagnostic keyword text grants no catchability.

| Current source site | Existing diagnostic category | R2 disposition |
| --- | --- | --- |
| `_c_read_name` 9972 | Unbound/missing name, including unmodeled builtin uncertainty | Refused; not a promoted NameError/UnboundLocalError proof. |
| `_c_read_element` 10020 | Sequence index bounds | Refused; implicit IndexError promotion deferred. |
| `_c_delete` 10134 | Unbound cell deletion | Refused; implicit deletion exception promotion deferred. |
| `_c_delete` 10140 | Missing namespace deletion | Refused; no handler recovery from legacy tag. |
| `_c_invoke` 10909 | Unproved/noncallable selection | Refused; literal diagnostic TypeError does not authorize recovery. |
| `_c_invoke` 10925 | Unsupported or invalid helper binding | Refused; binder uncertainty is not a proved TypeError. |

## Outcome and completion reconstruction

The machine-readable `rewrite-r2-checkpoint2-outcome-inventory-v1.json` retains the full before/after call census and source spans. After this checkpoint there are 40 `_c_out` sites, one direct `_COutcome` constructor, four unchanged `_CContext` constructors, and one `_CCallObservation` constructor.

- `_c_out` 9901 is the sole ten-field outcome constructor. New fields are `exception_value` and `exception_origin`; active explicit/exclusion fields are now accepted and preserved rather than always reset.
- `_c_follow` 9931 carries result control/tag/reference/origin/explicit/exclusions while retaining prior/result issue and trace composition.
- `_c_call` 10819 retains nine-field completion tuples in this order: control, result, immutable state view, issues, tag, exception reference, origin, explicit, exclusions. The first four positions retain their earlier meaning. Its final outcome reconstruction forwards all active fields.
- The normal-only conversions in store completion, Return, successful class installation, and helper normal/return completion remain unchanged and are guarded by their normal/return branches. Abrupt outcomes are passed intact. `_c_eval_many`, `_c_statements` and `_c_join` are unchanged.
- All four context constructors, including helper entry, are unchanged. No deferred-depth field or generator state exists yet. There is no new nonempty exclusion-set producer in this checkpoint.
- State, result, debt and active exception metadata remain paired per ordered outcome. Handled historical raises may remain in immutable call observations but are not terminal blockers.

## New operation accounting

All charges use the existing operation context and budget. Numbers below identify newly introduced or widened work; existing called helpers charge their own allocations, visits, snapshots, copies and references separately.

| Site/work | Charge |
| --- | --- |
| Builtin fallback membership; class proof | 1 reached lookup probe; 2 for one-field proof allocation/reference. |
| Proof key in `_c_value_key` | 4: tag read, tuple allocation and two retained fields. |
| Empty exception record | 4: allocation + two retained fields + tag read, then existing object-ID/store costs. |
| `_c_out` | 11 for ten-field record; +1 only when creating its default empty exclusion set. Existing atom/trace creation remains separately charged. |
| `_c_follow` | +4 active-field reads, in addition to existing issue concatenation and trace linking. |
| `_c_call` completion item | 18 instead of 8: visit 1 + nine-field tuple 10 + append/reference 2 + five new metadata reads 5. Existing snapshot and final fact-tuple costs remain. |
| `_c_call` returned outcome | 6 instead of 2: earlier append/reference work plus four active-field reads. New `_c_out` cost is separate. Observation record remains 11. |
| Known raise | Admission 1, current object read when applicable, origin allocation/two fields + tag read 4, then outcome construction. No fabricated issue allocation. |
| Single handler proof | Dispatch 1 + tag read/comparison 2. |
| Tuple handler proof | Dispatch 1, current object read, kind check 1, then visit/proof check 2 per reached member and tag read/comparison 2 per proved member. Invalid member stops with refusal after actual reached work. |
| Handler routing | Handler visit/pending check 2; new work list 1; pending visit/form check 2; evaluated-result visit 1; tag read 1; retained active fields 5 when reconstructing. Appends pay 2, or 3 including a separately iterated result. Remaining pending extension pays 2N. Evaluator/join/outcome work is additional. |
| Handler entry | Admission 1, new normal outcome, then actual handler-body work. |
| Try | Admission 1, result list 1, body-outcome visit 1, produced-result visit/append/reference 3. Existing statement, outcome and join charges remain. |
| Raise statement | Work list 1, each evaluated outcome visit 1 and append/reference 2; evaluator/raise/follow/join charged separately. |
| Unary minus | Work list 1; outcome visit 1; exact arithmetic 1 only on admitted normal literal; append/reference 2. Atom/outcome/follow/join remain separate. |
| Terminal outcome | Control check 1 for every outcome. Escaping raise adds three active metadata reads and 20 for reason construction, two origin reads and the existing blocker/key export work. |

No table/bank ownership or copying algorithm changed. A detached dict still costs allocation + three units per entry (visit and key/value references), including full selected banks or object tables when copied. Wider metadata charges also affect ordinary nonexception calls/outcomes. Cost headroom is not established until the reviewed full12 run.

## Static checks and remaining standing

Retained checker: `rewrite-r2-checkpoint2-static-check-v1.py` SHA256 `4a5f2d351f289cfc846c8de3fbc01b7cca24e5e15ffbfb208d50278ae4dd6380`.
Result: `rewrite-r2-checkpoint2-static-v1.json` SHA256 `7a77f53394954002607d6b8cb66984e856ca051f215e5bdbd722a9f9887ce0fc`.

Exact20-edit forward/reverse reconstruction, syntax/changed-line style, 360-line R2 limit, sole proof/exception/origin producers, six unchanged legacy-tagged call sites, completion metadata shape, no historical-completion terminal scan, and protected core source segments passed. Original16 protected W paths were hashed before/after installation and again at result retention. Candidate bytes were never imported/executed. The coordinator's separate full r010/R1 static aid, source/accounting review and runtime dispatch remain its responsibility; this source-only checkpoint is not GREEN evidence.
