# C provenance integration correction — Stage 0

The first combined corpus and full inventory precheck exposed regressions in the
released d94a8e8c generator. Evidence: abc-provenance-corpus-regression01.json,
99 tests /39 failures /5 errors on actual3.11.15; source and logs remain retained.
No census expectation was changed and no new candidate was frozen. This is an
engineering correction within the existing two-file scope, not a cold verdict.

Root adopts the implementer's read-only diagnosis and the independent precision
check. The repair category is integration of callable proof with existing abstract
values and source-ordered exception semantics. Existing contract assertions remain
unchanged. The proof must not replace or weaken existing value/return information.

Required bounded design:
1. Carry callable/class/receiver/module proof as orthogonal metadata. Preserve
   existing FlowValue kinds, qualified values, callable summaries, protected return
   values, attribute storage semantics and exception transfer. Merge proof separately:
   loss of helper identity must not erase otherwise exact underlying value semantics.
2. Keep callee capture and evaluated-argument/default binding, but do not snapshot an
   ordinary failed call as though its body completed. Preserve existing independent
   census and exception-successor accounting.
3. Clarify the earlier blanket failed-lookup obligation: a proved NameError/TypeError
   or other exact non-completion has no helper-body execution and retains its actual
   handler successor. It needs no invented unresolved blocker. Unknown provenance
   still requires a blocker; mere absence from a snapshot is not a new proof. New
   tests may be refined to accept proved non-execution plus exact handler rows. They
   must continue rejecting stale helper-body rows. This clarifies Stage0 in light of
   the existing independently projected exception contracts, not a weakened gate.
4. Restore supported module-qualified exports and exact standard unittest skip,
   skipIf and skipUnless class decoration using proven imports/identities. Unknown
   decorators remain refused. Do not import the wider discovery decorator allowlist.
5. Attribute member/namespace invalidation to the owner and relevant executed effects.
   A deferred unrelated body, immutable code-object inspection, or an unrelated
   same-spelled member store is not evidence that this member changed. Actual writes,
   unresolved mutable namespace escapes, code/default replacement and opaque owner
   escapes (including containers) remain explicit refusals. Do not silence a genuinely
   lost identity merely because the original helper body looked pure.
6. A global/nonlocal declaration alone is not mutation. Attribute actual writes and
   unproved effects without discarding read-only captures or exception successors.
7. Preserve unchanged finite per-module/item limits; no raised cap, silent truncation,
   generic object heap or Python interpreter implementation.

RED is already established for existing contracts by the99-test snapshot. Add small
public positive/negative discriminators for stable module exports, exact skip versus
unknown decorators, unrelated same-name store versus actual owner mutation, and
read-only code inspection versus replacement, before the corresponding new edits.
The seven new category methods plus all previously failing DesignReview methods and
all nine earlier preservation methods form the next focused floor matrix. Confirm
identical bytes on3.14, then root repeats full corpus generation/census and full suites.
Any unexpected capability-row or helper-edge loss requires explanation before an
expectation refresh. No approval/baseline/GPU/guarded-profile/lifecycle or finalization
authority changes. All ten A/B and the other C paths remain outside worker ownership.
