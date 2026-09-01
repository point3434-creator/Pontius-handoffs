# R2-E1 repair design v3 closure review

Read-only engineering closure. I did not edit/import the candidate or inputs, run the analyzer or Models, or execute a payload.

## Bound pair

- Governing design: `rewrite-r2-e1-repair-design-codex-a-v3.md` SHA-256 `eaeb65d775857c229c509b430bf3eeb187bc058e79e27cda2a1b4a17cab74845`.
- Frozen source: H `beff8193e9d5ce7316f5006fccc77ffcb5ca5695`, manifest `ef3561cb462fcbd31dda7d3774ea34d00c575b7549dc1cc804ad9f92e11c582b`, source SHA-256 `7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d`.
- Prior v2 finding review: `rewrite-r2-e1-repair-design-engineering-review-v1.md` SHA-256 `feb6f5531865438a1786cee1a5899cb2a12af522372847d12fa169d9d83a8e26`.
- Canonical write census: SHA-256 `5640242a28caa83b61c08f1c2ac699823fcae53d38ce74b63dd4c579033e6efb`.
- Creation-matrix addendum: SHA-256 `b3da849d0ccedc2d675a98fa7d07a5ed90c3de3a204af961cef4e24b0bd824ec`.

## Verdict: SOUND design closure; no remaining Important issue

V3 closes both Important findings from the v2 review without widening the custom-builtins contract or adding a second authority truth.

1. It moves the class body's captured proof to the actual function-creation point before base-expression evaluation. It separately gates the current frame's `__build_class__` authority before bases/body, then carries the pre-base scalar through every admitted base successor into the class frame. Methods created later in the class body correctly compute from their then-current state and the class-frame proof.
2. It distinguishes the six current explicit absent-module Name producers from implicit opcode consumers. Every admitted `ClassDef` uses the pre-base frame gate; each `Import` alias gates before its symbol/store; an admitted multi-name `ImportFrom` gates once before any imported-name binding. Explicit module spellings do not satisfy an implicit gate. Relative/star and other unsupported forms retain their existing refusal boundary.

The current admitted implicit builtin census is complete: only `ClassDef` (`__build_class__`) and `Import`/`ImportFrom` (`__import__`) read a name from the executing frame's builtin environment without an ordinary AST `Name` route. Function/async-function definition is a creation-time authority capture, not an immediate consumer. Current literals/containers, identity, native protocols, member/subscript access, call dispatch, `If`, `Try`, `Raise`, assignment and deletion add no other `f_builtins` name lookup. Unsupported syntax gains no precision.

The representation and construction census remain coherent: one immutable `_CFunction` field owns history; the module frame supplies true; ordinary invocation projects the selected record; the class frame receives the pre-base proof. There is no default or caller/current-module recomputation. Existing object references preserve the field through aliases, bound methods, containers, snapshots, forks and ordered outcome joins. The v3 charge rules include retained fields, creation membership/proof reads, explicit-table work, pre-base class gate/carry work, and the exact per-operation import frequency; skipped work is not charged after a false gate.

## Coverage disposition

E01-E04 remain necessary but do not establish nested creation. V3 correctly requires five separately authorized pre-fix cases:

- T01 false frame plus absent key at nested creation: refusal, detects deletion laundering.
- T02 true frame plus present key: refusal, detects blind frame-bit copying.
- T03 true module/class frame plus absent key after a prior set/delete: exact clean launch, rejects monotonic poisoning.
- Nested class under an unproved method with module-imported `os`: refusal before the following launch, isolating `LOAD_BUILD_CLASS` without an explicit `__import__` mask.
- Local `import os as launch_os` under an unproved method: refusal before alias/sink effects, isolating implicit `__import__`.

These are nonredundant. A separate `ImportFrom` behavioral case is not required for the minimum only if static source review proves the distinct once-per-statement path shares the same gate and has the stated ordering. The five cases are prospective, not executed evidence; source implementation must remain held until their immutable inputs and pre-fix results are accepted under the coordinator's process.

## Checkpoint 3 forward contract

V3 also closes the forward authority seam without implementing it early. `GeneratorExp` is a function-like owner: capture the same proof before the eager outermost iterable, retain it on the generator/function-like record, and project it on every resume. Module mutation or the resuming caller cannot recompute it, and dormant creation does not execute the body. Planned explicit `range` and `sum` producers must extend the same classified explicit-name table and proof gate. Native range cursor iteration and resume mechanics themselves are not implicit builtin-name lookups. Checkpoint 3 must add every generator record/frame constructor to the required-field and charge census.

## Remaining limits

This closure is design evidence only. It does not establish fixture correctness, pre-fix RED results, implementation correctness, work-cap fitness, or interpreter parity. Future admitted syntax must be audited before being described as covered by the current consumer inventory. Within the frozen E1 and planned checkpoint-3 scope, v3 is ready for the separately controlled input/RED stage; no further design correction is required.
