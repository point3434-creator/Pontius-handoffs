# Cold review 02: v0a-eval-panel-impl/r001

Reviewer: Codex, independent reviewer 02. Issued 2026-09-08.
Defect verdict: CLEAN. No Critical or Important finding survives verification.
Design verdict: SOUND.

Candidate: e39d3b93695bfc601d051e8e71f334eef4d10d19.
Manifest SHA-256:
4f16c97f50734f06cc6bcd5286a87d355aaf4f8589f8796de1e33a8c5b47c405
BASE: 46f45298a405b967976413a4b8e45e7837602316.
Tree: 353e9626ee00ecf1c45b17b04d748d4990d99b8e.
Ref: refs/heads/review/v0a-eval-panel-impl/r001.

This verdict covers the entire frozen brief and design at Stage 0/0b, Tier C.
It establishes specification consistency under static inspection, not an implemented
or measured bridge. No execution, integration or ceremonial commit is authorized.

## Independence and identity

I read handoff.md first. I read the complete candidate, BASE requirements/workflow
and relevant frozen source before saving my initial invariant/related-path inventory.
Only after saving and format-checking that inventory did I open parent-disposition.md
and checks/author-verification.json. I read no existing review, task ledger,
implementer conversation, coordinator notes or sibling-agent material.

Initial inventory SHA-256:
8d3074e2e6874cc2a26ca947c5e27b22dea3ebaf9c2b0dc2ab6db83154bbd99a

Native Git and PowerShell/.NET raw-byte inspection independently established:

- Ref resolves to the stated candidate; its parent and tree equal the stated values.
- The complete diff adds only the two target Markdown documents. No source changed.
- Raw Git blob hashes produce these whole-row, ordinal-byte-sorted manifest rows:

  design.md: 0bcd669e3af5db21387a84f80437da48b9722b47f4e007ea951322275fe78648
  brief.md: edffd325a4c998381baa74a25d7a3367577014fb945ff3323277766abff6d62a

- Reconstructed manifest bytes equal packet manifest.sha256, including LF rows;
  the digest equals the identity above. Both candidate blobs pass LF/no-BOM,
  no-trailing-whitespace and <=100-column checks.
- All four pinned input SHA-256 values match handoff.md. Pinned workflow bytes
  match BASE docs/workflow.md. All 34 dependency Git blob pins match BASE.
- Both parent specification blobs at BASE equal candidate
  18b7527a3989f7d38830a7881c976385fe9bc4de byte for byte.

The author-check claims were corroborated by these independent operations rather
than accepted as receipts. The supplied inventory accurately labels itself direct;
I made no transitive-closure claim or inference from another review's verdict.

## Requirement and source assessment

All candidate locations below are in
docs/architecture/v0a-eval-panel-impl-r001/design.md unless stated otherwise.
Source locations refer to BASE; those source blobs are unchanged in the candidate.

1. Early measurements and retained scope: lines 17-27 and 218-240 separate the
   first source checkpoint from bridge completion and require preflight to exit.
   The brief retains the combined 600 production/400 test line limit and two-round
   Slice A budget. The measured decision cannot automatically launch full solving.
   Two future code freezes do not receive two fresh budgets. This is coherent with
   workflow Stage 0/0b and the requirement to return for further round authority.

2. Capacity: lines 29-64 fix a 67-character ASCII source_id, exact replayed keys,
   a strength-blind permutation and conservative CHECK/null prefix. The codec's
   _admit and encode_blueprint serialize distinct entries deterministically with
   compact JSON plus LF. Action kind lengths are equal; null versus 2 contributes
   exactly three bytes. Added rows have positive size regardless of serialization
   order. The stated boundary and final remeasurement therefore support the precise
   conservative-prefix claim, including all-fit and one-row-failure cases. They do
   not claim maximum solved-policy capacity or an out-of-domain overflow point.

3. Per-hand teacher: lines 68-109 use integer kernel settlement and fixed CALL.
   no_limit_betting.py:392 establishes minimum and maximum raise-to 2 at the
   declared root. After that all-in bet there is no second hero decision; the
   continuation's legal-action ordering puts CHECK first at the root. Combinatorial
   counts are C(47,2)=1081 and C(45,2)=990. Kernel settle at line 696 returns integer
   net chips. The royal-spade board ties all legal private hands: pots 4 and 8 split
   equally between the two contributors, leaving zero net returns for both actions.

   evaluation.policy_distribution defaults absent keys to uniform, so the explicit
   CALL rows at lines 82-89 are essential. best_response weights each hero state by
   chance/opponent reach and maximizes in legal-action order. The singleton game
   bounds the continuation's repeated dict(game.deals) construction to 990 deals.
   Production integer totals and a separately declared reference floating allowance
   are appropriately distinct; an action disagreement remains a stop, not a tie
   invented with epsilon. Shared ranker/kernel assumptions remain an explicit limit.

4. Cost and interruption: lines 91-109 distinguish production from reference
   construction/evaluation, cold from warm, CPU from elapsed time, and job peaks from
   allocations. river.py caches five/seven-card ranks, making those distinctions
   consequential. The finite worker/resource boundary can preserve completed
   observations without promoting interrupted preflight to success. No feasibility
   number or elapsed-time upper bound is asserted before the measurement.

5. Export and witnesses: lines 117-149 require full key-set equality and independent
   direct provider coverage. deal_for_hand preserves twelve private cards and admits
   indices 0..15. TableInput validates all private cards against the declared board.
   The finite seed bank cannot guarantee coverage mathematically, but the candidate
   explicitly refuses incomplete coverage and forbids shrinking H or adding seeds
   silently. Correctness witness selection is clearly separated from Slice B's
   collision-accepted population. Synthetic CHECK/off-pool controls retain separate
   identities when the production table cannot supply their prerequisites.

6. Outcome and agreement: lines 153-193 match the actual nested Session.play_hand
   wrapper at tools/v0a_table_session.py:233. That method records failed captures and
   cleanup before returning a completed settlement. WireConsumer.exchange/complete
   at tools/v0a_table_host.py:817/886 validate decisions, accounting, settlement,
   terminal closure and child EOF. The adapter publishes nullable event decisions
   and failures separately; v0a/trace.py:216/239 confirms that only FailureRecord
   carries delivery_status in v1. Failure-first classification covers absent river
   decisions, accepted-then-failed paths, malformed captures and missing outcomes.

   Runtime's blueprint-v1 path sets _provider=None at v0a/runtime.py:363.
   BlueprintProvider.propose emits blueprint_hit/blueprint_default, while v1 frames
   retain table_hit/passive_default. The required replayed PreparedBlueprint check
   therefore closes a real reason-verification gap without mistaking provider tests
   for runtime tests. Exactly-one-river checks stay agreement-only; completed
   prefix-diverged baseline chips survive. Scheduled attempts receive one final
   disposition, and pre-river defaults cannot inflate root hits.

7. Run ownership: lines 197-216 match Session.prepare, Admission and host.Source.
   The Admission cache shares the loaded host module; inherited PONTIUS_RUN_CONTEXT
   makes begin_run skip another source scan. Each session still prepares its own
   schedule/artifact/stacks. execution.py:122 suppresses inherited finish_run writes
   and permits the parent's output_directory under the repository. Its actual
   writer calls status_generation.append_run and render_status. The candidate
   explicitly inventories both, and does not propose per-cell seals or records.

8. Verification design: lines 187-245 require genuine successful host controls and
   real-boundary failure triggers, while labeling envelope fixtures as classifier
   evidence only. Changed-prefix zero hits, CHECK reason discrimination, off-pool
   default, reversed-board handling, exact ties and interruption are discriminating
   planned checks. tests/test_pontius.py uses tests/cases.json for the maintained
   parameterized harness and inherits run context. The specification requires
   isolated snapshots, supported runtime order and distinct measurement receipts.

## Checklist v1 and design judgment

- Items 1, 3 and 6: independent reference versus shared poker rules is disclosed;
  actual codec/provider/runtime/writer boundaries and fixture limits are explicit.
- Items 2, 4 and 5: absolute PONTIUS_GIT, scrubbed child environments, -B -P and
  disposable snapshot imports are mandatory planned checks, not present receipts.
- Items 7 and 8: measurements precede cost decisions; no universal entry count,
  arbitrary hard performance gate or river predicate on all chip outcomes appears.
- Item 9: existing process/transport owners remain intact; new worker failure and
  interruption behavior must be demonstrated at the code checkpoint.
- Items 10 and 11: candidate text and identity checks pass from raw frozen bytes.
  Exact integer/boolean validation in future evidence code remains a code-review
  obligation; this documentation candidate contains no such implementation.

Specification assessment: Pass for Stage 0/0b. Engineering design assessment: SOUND.
The narrow per-hand teacher, early measured checkpoints and separate outcome/agreement
results fit the declared contract without a new framework or sealed-interface change.
No required correction is issued. No design replacement is indicated by the permitted
evidence.

Advisory planning observation: the combined line budget is plausible but tight for
resource supervision, framing and real-boundary tests. The current specification
round plus the first code round consume the ordinary two-round allowance; bridge
completion needs the already-required explicit reauthorization. Keep both totals
visible at the measured decision. This is not a new gate or a material defect:
the candidate already preserves those constraints and requires a stop when exceeded.

## Evidence limits and command outcomes

Executed only native Git read operations (cat-file, show, rev-parse, diff-tree,
ls-tree and grep), PowerShell text selection, and .NET byte/hash/format checks.
Identity/pin/format checks completed successfully. One ancillary git rev-parse in
D:/Pontius-handoffs was refused for dubious ownership; I reported it immediately
and used the available frozen objects in D:/Pontius without changing Git settings.
Packet file reads remained available. No approval is pending.

No Python, project source tool, solver, host, historical owner, test suite or retained
experiment was executed. No source/candidate edit, fetch, commit or push occurred.
Only this attributed report, its earlier inventory and my own ledger line were staged.
Capacity, cost, finite witness coverage, actual resource containment and the final
line count remain unmeasured. The shared ranker/kernel cannot certify its own physical
poker semantics; host agreement cannot establish policy strength or general transfer.
