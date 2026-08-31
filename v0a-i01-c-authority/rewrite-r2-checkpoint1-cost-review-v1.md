# R2 checkpoint 1 cost and ownership engineering review v1

Reviewer: Codex authority_cost_audit, 2026-08-31. Read-only engineering review; not a cold review, runtime result or dispatch authorization.

Frozen handoff: H c119b3f2c452982cc595b156c276d5d904bbc94b; manifest rewrite-r2-checkpoint1-v1-manifest.sha256 SHA256 a6399d62ee23b42673766e857af047feb3abdfcab914053813eccec4cb9b9b90.
Candidate rewrite-r2-checkpoint1-source-v1.py SHA256 41b4de563da886a7c674d49b25acd4332ba208906b403ec244d1a4aea856ee05.
Predecessor rewrite-r1-task5-source-v2.py SHA256 c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f.
Exact delta 481d22b66d524df872a6bd447974df3992119f11904cb49fb09bf5bfe5983108; category ledger 7a272914a7eee6d441ac138d38c275a82eec04bdc994f79a4d6eb3bed55ae56e.

## Disposition

SOUND for this bounded source checkpoint. No material defect found in the new boolean domain, conservative identity rules, branch ownership/transport or declared semantic-work accounting. Executable correctness and whole-analysis fitness remain unverified; this source review supplies no GREEN claim. Exceptions and deferred generators remain later checkpoints.

## Independent category inspection

| Requirement | Source evidence and conclusion |
|---|---|
| Proof is distinct from runtime identity | _CBooleanUnknown9091 is fieldless/frozen/slotted/eq=False. _c_identity_compare10106 does not compare proof identity or choice keys. Even the same proof object, choices, symbols and opaque values reach the uncertainty producer. _c_value_key9455 uses an opaque retained-object identity only for alternative deduplication; live retained alternatives prevent key-ID reuse during that operation. |
| Exact identity needs an actual proof | 10113–10131 compares canonical reference IDs or literal identities with at least one proved None/bool singleton. It does not equate arbitrary equal strings/numbers, interning, bool-proof keys or structural value equality. A canonical heap reference cannot denote those singleton atoms in the installed representation. IsNot inverts only an exact bool. Generic comparisons remain outside the public single-Is/IsNot route at10328. |
| Producer/consumer category is complete | Whole-file search and AST census found exactly two proof constructors: identity10135 and Not10350. Both _c_truth callers are explicit: Not10347 and If10427; each checks the proof type before Python negation/truth. Unsupported generic truth still refuses. Proofs transported in cells/defaults/containers/outcomes stay immutable references; existing strict atom/ref gates for read/call/index/decorator/base/environment/sink consumption remain conservative. The only formerly unguarded value.kind consumer, _c_value_key, now handles the proof first. _c_choice has no production caller in this checkpoint. |
| Predicate work and branch ownership | Predicate evaluation still occurs once through the original _c_eval_many path. If10433–10447 visits body then orelse, and each uncertain branch calls _c_fork on the same pre-branch prior.state. The second fork does not use the first child's result. Existing token invalidation, outer table detach and selected-bank/object-table COW routines prevent the first child's writes from mutating the parent's view. The shared arena intentionally preserves unique allocation IDs. |
| Order, control and debt survive | Entered outcomes use the child wrapper. Unchanged _c_statements runs only normal paths and carries abrupt outcomes. Unchanged _c_follow takes result.state/control and links prior issues/trace; unchanged _c_join keeps ordered distinct outcomes without a value/heap merge. Prefix work is retained separately for feasible continuations. No general repeated-predicate correlation is claimed. |
| Limits and owners remain intact | Every added consume uses current ctx.budget. All original budget/cap, storage, allocator, metadata, binder, context, outcome/call and terminal-policy nodes are unchanged. No new epoch, refund, weakened cap, old-engine fallback, fixture discriminator or Model-supplied input was introduced. |

## Charge reconciliation

The declared unit remains semantic allocation/reference/visit work, not a Python opcode or allocator census. I found no missing new charge under that established model.

- Identity helper: one reached operation; +2 for actual ID/literal-payload reads, or +1 for the reference/singleton payload branch. Exact output uses the unchanged four-unit atom constructor. Uncertainty allocates a fieldless proof for one unit. Thus the ledger's exact-reference/literal cases cost7, reference/singleton6, and opaque/choice/proof uncertainty2. No alternative traversal occurs.
- Not on the proof allocates one new fieldless proof and retains the existing truth/outcome/follow/join charges. _c_truth merely returns the already held proof after its existing operation charge.
- Proof-key construction costs4 for the id integer, two-field tuple and retained fields. Existing choice visits, key probes, insertion references and container guard remain unchanged.
- Exact If routing adds the real singleton tuple2 plus one reached branch visit, without a fork. Uncertain routing charges the pair tuple3, two visits2 and two unchanged eight-unit forks:21 before entered/body/follow/join work. The second fork/body is charged only if reached; an earlier abort does not manufacture completed alternatives.

These are local accounting facts. Four continuations also pay their real operand/body work, trace reconstruction, terminal traversal and any full table/bank COW copies. The early-refusal baseline costs cannot establish this candidate's reserve. No runtime speed or headroom claim is made.

## Fresh static evidence and limits

A separate stdlib-only AST/text/hash check, invoked through D:/Pontius-tools/py311/Scripts/python.exe -I -S -B -P, verified:

- all seven manifest file hashes and the controlling candidate/base/manifest hashes;
- exact forward and inverse application of all seven edits;
-77 added +30 deleted =107 lines using SequenceMatcher(autojunk=False);
- only seven existing top-level nodes changed and two were added; all remaining top-level AST is identical;
- two proof constructors, two truth calls, one identity-helper call and zero _c_choice calls.

The frozen Git manifest was also read directly from H and matched the listed manifest. The first read-only Git attempt encountered sandbox ownership protection; a scoped read-only escalation succeeded without changing Git configuration. No candidate, test, Model, fixture or analyzer code was imported or executed. No source or existing artifact was edited.

The later observer adapter must bind this source's actual proof return class and input-state/source-span context; the c8fc-only baseline adapter cannot be reused. Required public four-leaf execution, D2 handling, generator depth and the196608 per-original-epoch continuation condition remain obligations of the separately authorized integrated run. This review does not close them.
