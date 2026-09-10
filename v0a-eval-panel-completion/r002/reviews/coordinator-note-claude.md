# Coordinator note — cold reviews 01 and 02 of v0a-eval-panel-completion/r002

Coordinator: Claude, 2026-09-09. Candidate `430ad75de79cec13d66ff3dc4981dd3770a371b7`
(ref `review/v0a-eval-panel-completion/r002-verified`), parent `449a2a3c`, manifest
`6e36bb41…`. FIX round for the parent's accepted Important (retained-protocol admission).

## How the passes were made cold this time

The r002 handoff requires probing the inherited context and using a fresh context if
prior history is injected. A probe from the coordinator's own session confirmed that its
harness injects a stale session-start snapshot of the coordinator's memory index into
every agent it spawns (the same exposure recorded in r001's coordinator addendum 02).
Therefore the reviews were NOT dispatched from that session. Instead:

1. The coordinator's memory index (`MEMORY.md`) was parked (renamed) so that no session
   had an index to inject.
2. The controller opened a new Claude Code session on `D:/Pontius` and ran the prepared
   workflow script (`D:/Pontius/tmp/eval-completion-r002-dispatch/cold-reviews-r002.js`,
   syntax-checked) with a single instruction to run it and report the result.
3. The script's first stage is a probe agent that aborts the whole run if any memory
   index, memory file, or eval-panel verdict text is present in its context. A first
   attempt aborted on the coordinator's own over-specified probe (it tripped on the
   ordinary git-status block, which names "Pontius" in commit titles); the probe was
   narrowed to memory sources and verdict text, with git status explicitly exempted, and
   the second attempt's probe returned `NONE`.
4. Reviewers 01 (bottom-up) and 02 (top-down) and a prosecutor ran concurrently, each in
   an exclusively created scratch directory under `D:/Pontius/tmp`, each receiving only
   the packet path, the handoff's rules restated, and its role; a completeness critic ran
   afterwards. The coordinator copied their exact bytes into this packet and re-verified
   every digest. The index was restored after the run.

Copied files and SHA-256:

- `reviews/review-01-claude.md`
  `5e3bb9f4290f94f5722e027de06f5e5f89a6049277f21794b3caddecfd57ebeb`
- `checks/inventory-01-claude.md`
  `af8323913bd1acc9fd77c8d987b90079292584189e8b2d7af1f00a15eefe03b6`
- `reviews/review-02-claude.md`
  `8f425227e9c7af3f3247355335c78bb8e5350423b0a69f72f6af87ec8e3ea6d0`
- `checks/inventory-02-claude.md`
  `fb8c8c8a8db96179739d39a917aa87930e4b868391276fdd285058b587a124d1`
- `reviews/prosecutor-claude.md` (not a cold pass; adversarial by construction)
  `518a51efc9413af4bba7513ed7f7db0cbec85e514abc16153eeb8880d7009d55`
- `checks/inventory-prosecutor-claude.md`
  `ab3ed87a121bc7395a17fbfbed34778685dd06d42c1f41c24c82f79cc85872ef`
- `reviews/completeness-critique.md` (not a cold pass; saw all three inventories)
  `e1549eaa24609efcd30733e46158e76aa79dcf431ef2ab071f6873a35889986c`

## Verdicts

**Review 01: CLEAN / SOUND. Review 02: CLEAN / SOUND.** Neither raised a Critical or
Important finding. Minors: universal-newline frame splitting is broader than the host's
LF-only framing (01 F-01, 02 F02-02 — fail-closed); `RecursionError` from `json.loads`
lies outside the exclusion tuple (01 F-02 — a phase crash, never credit; the host bounds
depth to 8); the declared `strategy` is not bound to the capture's protocol version
(02 F02-01, 01 F-03 — unreachable from the frozen caller, which fixes `blueprint-v1`).
Advisories: outer envelopes not exact-membership checked; caller inputs `stacks` and
`teacher_actions` trusted; `summarize.complete` tolerating `unsupported` (pre-existing,
outside the fix scope); several `r002*` refs in the review namespace (this packet names
`r002-verified` explicitly).

Both reviewers reconcile the parent's accepted finding **closed member by member, not by
example**: `ready.evidentiary is False` (164); `interrupted_response_count` exact int 0
(208); `requested_hands`/`completed_hands`/`ordinal` exact int 1 (292–297); the
`preparation_use` member set, `producer_absent`, exact empty list and exact 0 checked
before `PreparationUseRecord` is constructed (68–71); v2 records admitted only through the
public `validate_decision`, then provider/config/source-manifest/fallback-digest bound to
the ready frame with accepted delivery (56–64).

## The prosecutor (new this round)

A prosecutor agent — required to attack CLEAN by mutation regardless of the reviewers'
verdicts — enumerated **73 consumed members** across the session report, hand entry, hand
result, ready/action/event_result frames, v1 and v2 decision records, timing,
preparation_use, hand_result, session_result and settlement, and for each tried absence,
wrong JSON type, equal-but-not-it values (`False`/`0`, `1.0`/`1`, `True`/`1`), default
filling and unvalidated v2. **No material candidate survived**; every attack is listed in
`prosecutor-claude.md` §5 with the frozen line that refuses it. Its four advisories
coincide with the reviewers' Minors. Because no material claim was raised by any of the
three, the three-lens verification stage had nothing to verify.

## The critic

Given all three inventories, the critic checked nine unexamined areas (post-boundary code,
the baseline early return, v2 provider-outcome semantics, config digest binding, blinds and
button not being retained, event-count identity against the host, settlement comparison
semantics, result members with no production reader, registration and hygiene) and found
each correct; it corrected three of the prosecutor's closure claims (bytes-typed base64 is
admitted but only reachable in memory; `-0.0` passes `seconds()` as the host's own check
does; `exact_integer` type-checks the value, not the caller's expectation) — none with a
credit consequence. Its answer to the Tier C question: **no path by which missingness, a
default, a coercion or a failure becomes a hit, chip eligibility, agreement eligibility, a
completed count or a full-coverage claim.**

## Exposures, disclosed

- Probe: `NONE` — no memory index or verdict text reached any agent.
- Reviewer 02 disclosed the harness's ordinary git-status snapshot (branch, two modified
  files, five recent commit titles) and the user's email in its system context. These name
  no finding or verdict; the commit titles are the same read-only history the handoff
  permits through Git. Recorded, not treated as contamination.
- No agent opened any `reviews/` directory, other packet, ledger, index, disposition or
  readiness file outside this packet's `checks/`, other scratch directory or transcript;
  no project code ran; utility scripting used the handoff's interpreter.

## What this does and does not establish

Two independent, probe-verified cold passes, both CLEAN / SOUND, satisfy the handoff's
Tier C requirement for this round; the prosecutor and critic are supporting evidence, not
passes. Nothing here is broad-suite clearance, adoption, or authorization for the retained
solve, export or agreement invocations. The finalizer for this checkpoint is Codex.
