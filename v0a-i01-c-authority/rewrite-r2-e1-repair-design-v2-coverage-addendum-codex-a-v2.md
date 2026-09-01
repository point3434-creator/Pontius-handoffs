# R2-E1 repair design v2 coverage addendum, codex A v2

Engineering coverage recommendation only. No input, Model, harness, source, or expectation is authored; no payload is authorized or run. This supersedes only the prospective source shapes in v1; v1 remains immutable.

Bound design: `rewrite-r2-e1-repair-design-codex-a-v2.md` SHA-256 `98b8c09445425ed03d98c6293684c87c4ec94ddb126b3e996e590de17cae3fd1`. Bound source/census: `7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d` / `5640242a28caa83b61c08f1c2ac699823fcae53d38ce74b63dd4c579033e6efb`. Existing E1 pack remains `59b8457a2323634d883fb2c9b0ff82a1e60cd980c5f2a4b50e627c8ca32cdb9b`.

E01-E04 do not exercise nested function or class/method creation after deletion or after a present-key change. E03 proves that an already-created false method stays false after deletion; it does not prove the rule for a new nested record. E01 has no prior override. E04 is function-local and does not change module builtin authority.

The minimum prospective addition is exactly three cases. All use the existing imports, `ReviewTests(unittest.TestCase)`, `test_static`, `ValueError()` constructor, and unchanged launch statement. A nested `inner` is an ordinary zero-argument function defined and called synchronously in the method.

| ID | Exact admitted source order | Required result | Why necessary |
| --- | --- | --- | --- |
| T01 | Set module `__builtins__ = {}`; define `ReviewTests.test_static` while the key is present; in the method define and call `inner`, whose body is `ValueError()` then the launch; after the class statement delete module `__builtins__`. | Explicit refusal. | At invocation the method proof is false and the key is absent. This catches an implementation that treats absence as proved instead of inheriting the executing frame. The nested function avoids an earlier `__build_class__` refusal that could mask the proof transition. |
| T02 | Define `ReviewTests.test_static` before any override; in the method define and call the same `inner`; after the class statement set module `__builtins__ = {}`. | Explicit refusal. | At invocation the method proof is true and the key is present. This catches an implementation that copies the executing proof while ignoring the present key. |
| T03 | Set module `__builtins__ = {}` and delete it before the class statement; then define `ReviewTests.test_static` with `ValueError()` followed directly by the launch. | Clean exact launch. | The proved module frame plus absent key must give the implicit class frame and resulting method a true proof. Direct consumption in the method makes that proof observable and rejects monotonic ever-unproved namespace history. |

These statements are already in the declared R2 subset: module name assignment/deletion, ordinary class definition with the existing base, ordinary method/nested-function construction, synchronous call, constructor expression, and the existing launch. No new protocol, descriptor, custom-builtins interpretation, decorator, default, annotation, comprehension, or general class semantics is requested.

Independent harmless Models should reproduce the same creation order with real Python function/class creation and no process/file operation. T01 and T02 must observe `NameError` naming `ValueError` and no launch marker; T03 must observe constructor then launch. The sensitive sources remain AST-only and are never executed.

The cases are not redundant:

- Existing E02 covers present key plus false current frame.
- T01 covers absent key plus false current frame during new nested creation.
- T02 covers present key plus true current frame during new nested creation.
- T03 covers absent key plus true module/class frame after an earlier override and deletion.
- Existing E03 separately retains the historical false-method-after-deletion obligation.

No fourth case is needed for this creation rule. If inputs are later authorized, use a separately named three-case family with two required-refusal and one required-clean classifications. Report pre-fix results rather than assuming them; a RED does not authorize a development slot.
