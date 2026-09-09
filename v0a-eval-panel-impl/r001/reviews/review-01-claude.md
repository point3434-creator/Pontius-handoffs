# Cold review 01 — Claude — v0a-eval-panel-impl/r001

Reviewer: Claude, independent cold reviewer 01. Issued: 2026-09-08.
Round: NEW-SURFACE, Tier C Stage 0 / Stage 0b specification review.

**Defect verdict: NOT CLEAN — one Important finding.**
**Design verdict: SOUND.** The phase order (capacity, then per-hand cost, then
bridge completion within the same Slice A budget) is the right shape and follows
the accepted lane design without reopening it. The finding below is a bounded
correction to one acceptance predicate, not a shape problem.

## Binding identity

- Candidate `e39d3b93695bfc601d051e8e71f334eef4d10d19`; ref
  `refs/heads/review/v0a-eval-panel-impl/r001`; on origin.
- Sole parent = BASE `46f45298a405b967976413a4b8e45e7837602316` (the ceremonial
  adoption commit); tree `353e9626ee00ecf1c45b17b04d748d4990d99b8e`.
- `diff-tree --no-renames` against BASE: exactly the two added documents.
- Manifest recomputed from raw `git cat-file blob` bytes, whole-row byte sort,
  LF rows: `4f16c97f50734f06cc6bcd5286a87d355aaf4f8589f8796de1e33a8c5b47c405`,
  rows byte-identical to the packet's `manifest.sha256`.
- Pinned inputs hash as stated: workflow `c71e3963…` (byte-identical to the
  BASE blob `503fd170…`), controller rulings `2649ae25…` (byte-identical to
  the r003 copy), parent disposition `218fdf7b…`, dependencies `ce6c5a91…`.
- The parent specification blobs at BASE equal candidate `18b7527a`'s.
- Candidate text: 174 and 266 lines; LF-only (zero CR bytes); no BOM; no
  trailing whitespace; no line over 100 columns. The author receipt is accurate.

I read `handoff.md` first, then the candidate blobs and pinned inputs, and
recorded my inventory at `D:/Pontius/tmp/impl-r001-review-claude-inventory.md`
before opening `checks/author-verification.json`. I read no other reviewer's
output, no task ledger, and no implementer transcript. No runtime, solver, host,
test, fetch, commit, or edit was executed for this review; all source claims
below were checked by static reading of frozen blobs at BASE.

Candidate locations refer to `docs/architecture/v0a-eval-panel-impl-r001/`
at the candidate commit; source locations refer to BASE blobs.

## Important finding

### I-01 — The singleton reference's action comparison cannot survive an exact production tie

Severity: **Important**. Confidence: high on the mechanism; the realized
frequency on a given board is not established here.

Candidate locations: `design.md` §3, "Compare its selected action exactly;
compare reported values with a declared floating-accumulation allowance …
A numerical disagreement is investigated and recorded, never converted into an
action tie", and the §3 falsifiers "disagreement with the singleton reference;
wrong tie action"; `brief.md` criterion 2, "check actions and values"; criterion
3, "a reference disagreement … stops the phase".

Frozen evidence:

- Production T1 is specified as exact integer totals with CHECK on exact
  equality (`design.md` §3). That part is sound.
- The reference is `evaluation.best_response` on the sealed singleton game.
  Its chance weights are floats: `river.py:203-229` normalizes each deal to
  `weight / total`, i.e. `1/990`, not exactly representable. `evaluation.py:187-273`
  accumulates `sum(reach * continuation_value(...))` in floating point over the
  990 deals in sorted-deal order and selects `max(entry.actions, key=...)`,
  which returns the first action — CHECK, per `legal_river_continuation.py:44-66`
  — only on an *exact* float tie.

Concrete failing scenario: a hero hand `h` whose 990 compatible villains split
into `w` wins, `l` losses and `t` ties with `w = l > 0`. Production totals are
`2(w − l) = 0` for CHECK and `4(w − l) = 0` for the bet: an exact tie, action
CHECK. The reference computes two float sums of `±2/990` and `±4/990` terms
whose partial sums are rounded at each step; neither is guaranteed to cancel to
exactly `0.0`, and whichever action carries the larger residual — of order
`1e-16` — wins `max`. If that is `raise_to(2)`, the candidate's "compare its
selected action exactly" reports an action disagreement, criterion 2 fails,
criterion 3's stop fires, and the stop rule spends a bounded-correction round
on a non-defect. The candidate's own tie clause forbids the opposite error
(turning a value disagreement into a tie) but does not address this one. The
royal-spade `2c 3d` control does not exercise it: every term there is exactly
`0.0`, so both float sums are exactly zero. A non-degenerate tie hand is the
case that matters, and the specification has no rule for it.

Smallest correction: state the comparison rule for the tie case. When
production totals are exactly equal, the reference passes if
`|V_ref(CHECK) − V_ref(raise_to(2))| ≤ allowance`, whatever action it selected,
and the case is recorded as a tie; otherwise require exact action equality and
value agreement within the allowance. Derive the allowance from the reference's
own accumulation (990 terms of magnitude ≤ `4/990`). Add a non-degenerate
tie to the reference sample when one exists in `H`, and say so if none does.
No sealed change is needed; `evaluation.py` stays as it is.

## Advisory observations, not blocking

- **A-01 Worker working directory.** `Session.prepare`
  (`tools/v0a_table_session.py:198-201`) admits `Path.cwd()`, and
  `begin_run(inherited=…)` (`execution.py:37-44`) raises "child run root differs
  from parent" if that differs from the parent context's root. The design's
  inherited-context mechanism (§6) therefore requires the worker's current
  directory to be the run root before each `Session.prepare`. State it.
- **A-02 Witness bank size.** Criterion 6 needs a witness for every `h ∈ H`
  from a *frozen* bank scanned first-accepted-draw-wins. The controlled seat
  receives a specific hand with probability `1/1326` per dealt hand, twelve
  private cards must avoid the board (`C(47,12)/C(52,12) ≈ 0.25`), and covering
  1,081 hands is a coupon-collector problem (`≈ 1,081·(ln 1,081 + 0.58) ≈ 8,200`
  accepted draws). The bank must therefore hold on the order of `3 × 10⁴` dealt
  hands — roughly two thousand seeds at sixteen indices each — or the schedule
  is incomplete by construction. The design says an uncovered `H` cannot pass,
  which is honest; it should also say how the bank is sized so that it can.
  Dealing is cheap; the host runs are the cost, and those are one per `h`.
- **A-03 Coverage category.** Stage 0b asks for the coverage claim and its
  enumeration method stated early. The candidate expresses it as per-section
  falsifiers and defers the record to the code freeze. Acceptable for this
  round; the code freeze's coverage record should state the category
  (every path from plan to retained result, plus every exclusion) and the
  discovery method explicitly, as the r003 record did.
- **A-04 Reference villain policy.** After the hero's all-in bet the villain's
  legal actions are FOLD and CALL only (`_raise_bounds` returns `None` when the
  sole opponent has zero stack, `no_limit_betting.py:392-405`), so "CALL with
  probability one at every villain key" is well-defined and the design's
  warning against the uniform default is correct — `policy_distribution`
  (`evaluation.py:15-25`) would otherwise split FOLD/CALL evenly.

## Claims verified against frozen source

| Candidate claim | Evidence | Assessment |
|---|---|---|
| Inherited run context avoids a second source scan (§6) | `table_host.py:142-151`: `Source.__init__` calls `begin_run(…, inherited=os.environ.get(CONTEXT_ENV))`; `execution.py:37-44` returns the parsed context without filesystem work | Holds, subject to A-01 |
| Children inherit the context (criterion 9) | `table_host.py:470-475`: the scrubbed child environment sets `CONTEXT_ENV = child_context(source.context)` | Holds |
| One journal row per invocation; sessions and children write none | `execution.py:122-125`: `finish_run` returns for inherited contexts; `finish_run` is called only from `main()` in `table_host.py:997` and `table_session.py:388`, never from the `Session` class | Holds for the in-process `Session` path the design specifies |
| `output_directory` under `experiments/results/runs` (§6) | `execution.py:126-134` honors `context["output_directory"]`, writes `result.json` there, and hashes a sibling `runtimes.json`; precedent `v0a_blueprint_workload.py:400` | Holds; real API, not invented |
| Retained frames are complete framed messages (§5) | `table_host.py:512-537`: newline-delimited frames ≤ 16,384 bytes, stdout captured to 2,097,152 bytes, overflow → `truncated` and `transport_failed` | Holds |
| `Admission` caches the host module; `prepare` builds a fresh `Admission` per session (§6) | `table_session.py:44-60`, `198-201` | Holds; each `Source.__init__` is a JSON parse under inheritance |
| Placeholder rows are conservative (§2) | codec `_action` serializes `{"kind":"check","raise_to":null}` vs `{"kind":"raise","raise_to":2}`: three bytes longer | Holds |
| Wire length monotone in the nested prefix (§2) | `encode_blueprint` emits a JSON array of positive-length rows with fixed metadata; adding a row adds its bytes plus a separator | Holds |
| Boards ascending under the library encoding | `river.py:43-53`: card = rank_index·4 + suit_index; `2c 7d 9h Js Qc` = 0, 21, 30, 39, 40; `Ts Js Qs Ks As` = 35, 39, 43, 47, 51 | Holds |
| `s = 4` root: CHECK or `raise_to(2)`, one hero node | `no_limit_betting.py:392-422` (unchanged since r003 review) | Holds |
| Kernel settlement for both terminal outcomes, integer net chips (§3) | `no_limit_betting.py:696-749` `settle`/`net_returns`; pots 4 and 8 split evenly on ties | Holds |
| Per-hand production never builds the joint game; partition confined to T1 (§3) | Stated explicitly; `legal_river_continuation.py:195,241` quadratic checks remain the reason | Holds |
| r003 disposition obligations carried | `hands[*].result` (§5); agreement ≠ chip eligibility (§5, criterion 7); seed/index 0–15 (§1); inventory called direct with clock/action_clock/execution/preparation_bank/status_generation pinned (`dependencies.json`, 34 rows, all recompute) | Holds |
| Budget accounting (brief) | 600/400 lines for the whole slice; this round counted toward the two-round Slice A budget; no reset at the design→code transition | Holds and is conservative |

## Requirement assessment

Stage 0: tier and protected invariant, baseline, scope with unchanged list,
seams, size budget, ground truth with its stated weak point, dependencies, stop
and kill rules, round budget, forbidden claims — present. Stage 0b: mechanisms
with invariants and falsifiers per section, alternatives rejected with reasons,
open decisions correctly deferred to execution plans rather than invented here,
cheap-versus-permanent stated — present; coverage category implicit (A-03).
Checklist v1 items applicable to a specification round pass; execution items
remain future obligations, as the candidate says.

## Verdict basis and limits

NOT CLEAN because I-01 is a concrete, source-derived way for a correct
production computation to fail the round's own acceptance predicate. SOUND
because the phase structure, ownership, envelopes, and arithmetic are otherwise
consistent with the frozen contracts and the accepted lane design, and the
correction is one sentence of rule. Nothing here establishes implemented
correctness, measured cost, capacity, agreement, or poker strength; the
candidate claims none of those either.
