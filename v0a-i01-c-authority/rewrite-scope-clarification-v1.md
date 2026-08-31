# C replacement: comprehension scope clarification

2026-08-31. Append-only design clarification, no code or test change. This
qualifies rewrite-design-v1.md SHA701552c177840e4c5c0dd9c5985776256af5b31e7e997067dd662638a67c3ca8
and rewrite-state-model-proposal-v1.md; their issued bytes remain unchanged.

In the admitted comprehension syntax, the implicit comprehension has its own
frame. Its local name targets bind there. Free-name lookup skips the class
namespace and continues through the enclosing nonclass lexical/module rules;
it does not skip the comprehension's own local bindings. The outermost first
iterable is evaluated in the actual surrounding context, which may be a class
frame. Later iterables, filters and the body use the comprehension frame. A
member/subscript target writes its resolved destination, not an invented local
cell. Deferred execution retains these distinctions.

The earlier phrase "use the enclosing nonclass scope" must not be implemented
as binding comprehension-local names in an enclosing frame or skipping their
own locals. Existing scope classification and unsupported-syntax refusals remain
binding; this clarification grants no additional Python precision. R1's minimal
cases do not establish the later full comprehension contract. The implementation
plan must carry this rule before those paths are migrated.

The bounded rereview verified the frozen H commit135470ade797dbe2001208a7b6ff3fd4dbb6c5fd
and design manifest51cf85d387ac0b64c59603cd04fc758dcfa936cac839d016673b02fe9f7a6267,
found the six earlier design concerns addressed, and identified this wording
clarification. That is design evidence, not an implementation CLEAN verdict.
