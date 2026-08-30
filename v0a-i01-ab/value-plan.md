# Value-admission correction plan

2026-08-30, Codex. Tier C, separate FIX V-01/V-02/V-03 from the value-boundaries
r001 disposition. Base draft: policy r002 commit2f4287f68a83fac4225a05a91daffdb3f2977a43;
freeze only after predecessor disposition. Claude keeps C. No sealed bytes change.
Scope: model.py, runtime.py, existing test_v0a_hand_replay.py (other existing test
files only if a necessary regression observer conflicts). Expected <700 changed lines.

Stage0 read-only review by ab_scope_inventory accepts three commit boundaries:
dispatch handlers, mailbox insertion, acknowledgement count. Closed exact model
admission reconstructs one owned immutable graph using seven known record types,
exact primitives/tuples, and established constructors. Subtypes and mutable leaves
reject before their hooks or effects. No caller post_init dispatch or new dependency.
Event admission happens inside the opened outer transition before game/action effects.
Unadmitted metadata is null, including dead/complete and early clock refusal paths.
Mailbox prebuilds both admitted envelope and receipt before insertion. Runtime
validates complete receipt before equality; malformed after actual delivery remains
unknown/ambiguous, no retry, no claimed acknowledged count.

Discovery method: enumerate every public record entrance, then every state/effect
assignment and error-report metadata use; recursively enumerate record fields.
Four event variants, envelope action and receipt fields are all covered. New member:
exact valid showdown ranks mixing int/tuple domains cannot be compared by settlement;
reject before completion, no coercion. Preserve all-int/all-tuple controls and live mask.

RED before production edits on frozen r002: ordinary skipped-validator event subclasses,
exact outer plus invalid nested action, schema/index aliases, mutable/empty strengths,
mixed competing ranks; malformed envelope then valid same-key delivery; real forwarding
mailbox then bool/float/subtype receipt. GREEN also demonstrates valid controls, actual
receipt ambiguity, unchanged no-retry/known actions and complete failure sequence.
Category expected outcomes derive from no-effects/immutability/delivery contracts, not
private helper bookkeeping. Source search supports discovery only. Exclude arbitrary
private forging, monkeypatching sealed classes and lying callbacks.

Floor-first fresh snapshots, four focused suites, freeze manifest and two independent
cold reviews; no broad/GPU/source seal/operational claim or ceremonial source commit.
Policy remains separate. Trace and publication remain separate subsequent candidates.
