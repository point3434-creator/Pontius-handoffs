# R1 Task4 construction/call engineering review v1

Reviewer: codex/cold_review_a, acting as an engineering participant.
Disposition: no additional construction/call blocker found in this bounded
Task4 delta. This is source inspection of an unwired intermediate, not a
runtime pass, public-path acceptance, or cold implementation CLEAN. Task3's
open findings and the requested original helper-depth correction remain open.

## Frozen target and evidence

- H commit: c74092059ba4451d7f1983f2b737e2ea3fdbd40d.
- Task4 manifest: rewrite-r1-task4-v1-manifest.sha256,
  23d7980e9dc34ac396bd4d7426e17ceb0d5c883291afd14eef88f80735645cb2.
- Source: rewrite-r1-task4-source-v1.py,
  3511f60a62fc9588f153ba3db6b05ac228a1ce235cb23a5316000ce7ba4e550c.
- Delta: rewrite-r1-task4-from-task3-v1.diff,
  b6fe1bcd5afdac2ade9b7914c529a9cc4c63b05d8d923bad88d26bc49ee395d1.
- Prior source: 1ecbde73fcd2159aef2a96538850a93fc4ec2bfa590352bc33d95581d12ccc45.
- Prior review: rewrite-r1-task3-semantic-review-v1.md,
  623015f010c066784b13b11c35c3f17ce1918fdfa57c48fcaa917dc21ee834d1.
- Additional coordinator scope note, read separately from the frozen candidate:
  rewrite-r1-task4-coordinator-disposition-v1.md,
  c12b0455954e90e3ee4f9ecaba888079002c6374aa85615439a9e959228bea37.

Independent read-only Git cat-file inspection verified the manifest blob and
all nine listed blobs against their local immutable bytes and hashes. A
stdlib-only AST/hash inspection under actual Python3.11.15 -I -S -B -P verified
the exact unified diff, the five new helpers, and that the only changed prior
helpers are _c_scope, _c_statement and _bind_helper_arguments. All other prior
module AST is exact. Removing fourteen validated binder budget guards, six
read wrappers and the optional keyword reproduces the prior matcher AST.
No candidate, fixture, Model, source checker or test was imported/executed.
No source/test/generated/ledger bytes were changed.

## Category assessment

1. Construction and dormant bodies (10401-10522).
   Decorator expressions precede positional then keyword-only defaults;
   _c_eval_many preserves operand order and abrupt outcomes. Captured defaults
   are the returned canonical values, not later AST reevaluations. Captures
   record destinations after those construction effects. Function bodies are
   not run at construction. Async/generator bodies are retained with an
   unsupported-deferred body kind and explicitly refuse at invocation.
   Yield/YieldFrom/Await source-site collection excludes nested body scopes.
   Unsupported annotations, generic forms, decorators and class headers have
   explicit refusal paths; this review does not enlarge their admitted subset.

2. Class versus lexical ownership (10482-10522; 9781-9857).
   The new class has a separate current namespace. Its frame retains the
   enclosing nonclass frame for capture lookup, and actual body execution uses
   current successor state. Child closures capture enclosing function cells,
   not accidental class dictionary slots. Only a normal completed class body
   binds the class in the enclosing namespace; failed/refused body effects and
   traces are retained. Immediate class methods receive class attribution in
   the immutable binder descriptor; nested function bodies get their own scope.
   No new inheritance/MRO, custom descriptor or cross-module precision is
   claimed. Existing class-name routing and its declared-subset assumptions
   were checked as the construction dependency, not reopened as a new engine.

3. Call selection, binding and native receiver freshness (10560-10653).
   The existing caller evaluates and selects the callee before its operands.
   _c_invoke consumes these captured argument values; binder AST identities
   select them, and defaults select the values captured at definition time.
   Explicit proven_bound prevents spelling-based receiver inference. A fresh
   activation allocates all locals unbound, then fills receiver/parameters and
   installs only the selected function's captures; unrelated caller locals do
   not hydrate the callee. Returned refs and effects remain paired with each
   outcome. Local recursive bodies share the existing ctx.budget.
   Native append rereads the selected receiver's current record after argument
   evaluation, preserving selected receiver identity and intervening mutations.
   Unsupported call/signature forms refuse; definite fixed-signature binding
   errors and literal noncallables produce TypeError outcomes before the body.

4. Historical observation boundaries (10525-10557).
   Entry view is taken at invocation after operands have evaluated; selected
   callee, receiver, arguments and defaults are explicit captured values.
   _c_snapshot revokes the state's writable token, and later cell/object writes
   detach through the existing ownership helpers. Completed views are paired
   with control/result/issues; observations do not reconstruct executable
   inputs from names or old projections. The observation's frame is the CALLER
   evaluation frame, not a callee activation. Its completed tuple contains all
   alternatives; later emission must consume the outcome/trace topology rather
   than count each alternative as a sequential call. That row-emission code is
   not yet present here and is not approved by this finding.

## Explicit limits and carried obligations

- The six _c_binding_read wrappers initially exceeded the earlier literal
  consume-only wording, but the exact additional coordinator disposition now
  authorizes these six sites. Each wrapper returns its original pure read,
  charges immediately afterwards and precedes dependent matching action.
  Its narrow exception does not authorize delayed allocation/mutation charging.
  The only new budgeted binder caller is _c_invoke; it passes explicit boolean
  binding and the existing budget. Reached starred/expanded syntax is rejected
  upstream. Task3's expansion ordering defect is still open; the matcher itself
  does not repair it. This was a scope clarification, not a new semantic bug.

- _c_invoke's current len(helper_path)>64 branch (10601-10602) emits an ordinary
  differently worded refusal. Root already requested restoration of the
  original InventoryError text and final entry/depth convention in Task5.
  The original helper65 assertion at original test lines20418-20449 remains
  binding. No helper-depth payload ran, and no claim about exact final depth
  is made from this intermediate caller alone.

- _CFunction has no explicit defining-module owner; invocation currently creates
  its frame with the caller's frame.module (10622). Free module captures carry
  their own route, but explicit globals and uncaptured module fallback use the
  invocation frame. This is a real future ownership obligation before any
  cross-module call is admitted. R1 explicitly excludes that path; this review
  does not present it as an exercised current-path defect or demand new scope.

- The four Task3 source categories remain open: destination absence/unbound
  handling; unsupported implicit truth effects; abrupt sequencing across import
  aliases; and mapping/keyword expansion boundaries. Their original report and
  the coordinator's additional environment-expansion correction stand unchanged.
  The original nondefault exception metadata also remains a later obligation
  before handler semantics are admitted.

Public integration, row-count reconciliation, helper-depth mapping, Gate A and
all runtime/cost acceptance remain later root-owned checkpoints. This review
makes no whole-engine metering or passing-test claim.
