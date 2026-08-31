# C replacement: design review disposition v1

Engineering only. The reviewed draft was SHA18ff3c1d6b228474a321d93f8be4498c717f5af2244be62855cfb5e50ec24acb.
Its exact bytes are retained as rewrite-design-reviewed-draft-v0.md after an exact
inverse of the recorded later edit reproduced that hash. The reviewer read a
mutable draft; this is not a frozen implementation review or a cold pass. Do not
apply its report to later bytes as though it reviewed them.

The coordinator accepts all six design findings. rewrite-design-v1.md addresses:
1. Executable-entry inventory: resolver, call snapshots, helper-return/prepass,
   unittest preflight and recursive review bridges. Binder rules can remain;
   executable live-value transport cannot.
2. Full call observation: selected callee/receiver, argument/default references,
   call-entry state version, and result/effects. A default selects a reference,
   not frozen mutable contents; closure reads remain live until invocation.
3. R1 includes required minimal successor/state-result pairing and exceptions.
   R2 extends control/deferred behavior; it cannot supply a missing R1 obligation.
4. Explicit class shadow/fallback, lexical destinations, outermost comprehension
   iterable versus implicit body scope, and state-owned current members.
5. Typed retention/element/capture/deferred edges and reached outcome issues,
   without confusing container traversal with executing a contained generator.
6. The early test uses the entire public path and all actual budget scopes;
   required name enumeration is separate from avoidable value reconstruction.

The state proposal and cost v1/v2 are adopted as design input subject to the
coordinator design. Root adopts the196608 Gate B reserve before any replacement
result, while retaining the262144 production cap. Gate A uses the cap and records
headroom. This is a continuation choice, not empirically established sufficiency.
No representation-specific prototype interface is added to product requirements.

Replacement implementation, detailed operation accounting, controller review and
payload execution have not occurred. Category/coverage planning and a concrete R1
implementation plan precede production edits. All failed candidates, tests,
expectations and held diagnostics remain intact. Existing engineering sessions
cannot count as the future two mutually blind cold reviewers.
