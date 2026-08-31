# R2-E1 frozen input engineering review

Verdict: SOUND for the bounded input design. No material source/Model/envelope issue found. This is an engineering input review, not runtime evidence or cold acceptance. The candidate, sensitive sources, harmless Models, analyzer, tests and harness were not imported or executed.

Frozen pair: H ed837198d2c83757bfb74d962af244c33f0aeae6; rewrite-r2-e1-inputs-v1-manifest.sha256 SHA-256 a45941376da823672808050182e151f22520167d6cb24a8a9947e7b2a6c4f45e. All four manifest entries were independently rehashed and the manifest was read from the exact frozen Git commit:

- cases 59b8457a2323634d883fb2c9b0ff82a1e60cd980c5f2a4b50e627c8ca32cdb9b
- scope/spec 4fcb92ed30a86be1664d9b1981e5e8dc8c47d5d76eaab7b08dc09db74abc9f11
- source/Model map171f76c7532ae5ef24e279892110b9afdcbb56660951d8c85d9bfd31270f68fb
- exact source differences a879d595fe18fd76abf7640464d37da983579061a471ea6b23df1a2fb694c76c

The preparation input is rewrite-r2-e1-finding-preparation-v2.md SHA-256 effe5454d347cf2a42dbc90e913a2f2be0e5adb31acf91c2495c58b9877dc50c. Candidate source7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d remains held and was not read as executable code in this review.

## Model and source correspondence

- Every sensitive source has exactly one ReviewTests.test_static, one ValueError() call, and the adopted sink. The source constructor and local __builtins__ assignment ASTs equal their harmless _body counterparts after removing Model-only event/return nodes and the sensitive sink.
- The sink statement is byte-exact and AST-exact across all four cases and to identity-scale-n8-s4-d0-normal. The source path, stable ID, item universe, inventory document, serialized inventory bytes and derive_design_review invocation envelope are exact adopted data. No ambient ladder, helper wrapper or selector input was retained.
- E01 constructs the FunctionType function with a fresh standard builtin dictionary. ValueError is resolved from that captured dictionary, producing constructor/launch/fixed.
- E02 constructs the function while the globals dictionary contains the exact empty builtin dictionary. Its code first records constructor, then fails at ValueError before launch. The expected NameError.name is ValueError.
- E03 performs the same empty-context function construction and only then deletes _context["__builtins__"]. FunctionType already owns the empty captured builtin dictionary, so deletion tests creation-time history rather than current globals-key visibility. The expected result remains NameError/ValueError before launch.
- E04 assigns a local variable spelled __builtins__ inside _body, while FunctionType construction uses the standard builtin context. The local spelling has no authority over the function's builtin environment, so the clean constructor/launch/fixed result is the appropriate control.
- Harmless Model sources contain no imports or sensitive sink. Their only intended live subject is _body executed through the externally supplied FunctionType under explicit globals. Model objects/results are not analyzer inputs.

This pairing is faithful to the exact proof question: the two bad cases differ in current module-key visibility after sharing the same empty context at function creation, while the two controls distinguish standard context and local spelling. It does not claim to model unittest setup, imports or subprocess behavior; those are deliberately outside the harmless projection.

## Fixed expectations and public adjudication

Case order E01 through E04, source/oracle hashes, expected traces/results/exceptions, and2clean/2refuse classifications are internally consistent. All four retain required argv [["-m","fixed"]] as the fixed sink identity. Clean cases require that row and no blocker. Refusal cases require an explicit blocker but do not demand no row, matching the fail-closed contract.

The public envelope’s canonical SHA, embedded inventory-bytes SHA and decoded inventory object reconcile independently. The frozen identity case is described only as the donor of sink/envelope bytes, never as prior GREEN evidence. E01/E04 must establish clean behavior in this new run.

## Required harness checks and limits

The executable successor should preserve these input facts rather than infer them from labels:

1. Construct _STANDARD_BUILTINS as a fresh ordinary dictionary and _FUNCTION_TYPE as the intended actual type.
2. Before Model invocation, prove _function.__globals__ is the constructed _context and _function.__builtins__ is the selected _builtin_context. For E03, separately prove the globals key is absent after deletion while the function still owns the original empty dictionary.
3. Catch outside the modeled function and retain exact exception type and NameError.name; expected NameError is completed oracle evidence, not analyzer/infrastructure failure.
4. Reconcile raw public receipt, blockers, expanded rows and argv with each exact frozen case. Do not execute sensitive source.
5. Keep actual3.11.15 first, no development replay after RED; a later repaired source needs a new GREEN owner and matching floor-to-development pins.

Runtime behavior, candidate RED, public analyzer result and harness custody remain unverified. The forthcoming harness successor still needs its own exact-diff review. This input review authorizes neither execution nor repair.
