# Coordinator note — cold reviews 01 and 02 of v0a-eval-panel-completion/r003

Coordinator: Claude, 2026-09-09. Candidate `7ca821802c949b047becf6599d603b3b63d51fa7`
(ref `review/v0a-eval-panel-completion/r003`), parent `430ad75d`, manifest `1f48c97a…`.
FIX round for the parent finalizer's promoted Important (raw-frame admission).

## Dispatch

Same procedure as r002 (coordinator's memory index parked; the controller ran the
prepared script from a fresh Claude Code session; probe stage first). **Probe: `NONE`.**
Two cold reviewers (01 bottom-up, 02 top-down), a prosecutor and a completeness critic
ran in exclusive scratch directories; the coordinator copied exact bytes and re-verified
every digest after copying. The index was restored afterwards.

This round's prompts stated the standard the r002 finalizer applied — host-equivalence of
admission: any bytes the unchanged host would refuse that the classifier credits is a
defect regardless of the credited values — verbatim to reviewers, prosecutor and critic,
and the prosecutor attacked the raw bytes first (separators, CR, BOM, encoding, frame size,
depth, trailing bytes, empty frames) with a "would the unchanged host accept these bytes?"
column per attack.

Copied files and SHA-256:

- `reviews/review-01-claude.md`
  `31bac62fdcdaefc677ff34b8f90335b6011574e74c55e393568aca2c72467c71`
- `checks/inventory-01-claude.md`
  `71c08a4d849c78d59032c51422fb6860cb448394a9bdccbd433a313a6e873fb3`
- `reviews/review-02-claude.md`
  `f9b2aa5bb1d843c15d5fd0f64a18721011c7155c52a3611570301e5a22233585`
- `checks/inventory-02-claude.md`
  `be34b6dffdee17eb9bb426aedf689e4d9d7c0b45bd43cf6278c5a0b87e7acd85`
- `reviews/prosecutor-claude.md` (not a cold pass; adversarial by construction)
  `ea24f80118eece64650f2f21ec4e251c90049ace4f4d244acdcb8e8404a44cca`
- `checks/inventory-prosecutor-claude.md`
  `d3cd01f78c187394a8f394ca78489379980203b67f27f233f29ec875ef455b5e`
- `reviews/completeness-critique.md` (not a cold pass; saw all three inventories)
  `52ca74b327049837b0dbe6982ddae658153b6907207a677726492622267eaf3c`

## Verdicts

**Review 01: CLEAN / SOUND. Review 02: CLEAN / SOUND.** Both confirm the raw-frame
boundary now transcribes the host predicate for predicate — `decode_frame` mirrors the
host's `decode_json` (size 16,384, depth 8, 640-digit ints, CR/BOM rules) and `frames_for`
mirrors `read_stream` (physical LF framing, 2,097,152-byte stream cap) — closing the
parent's promoted finding at the byte level. Each raised one Minor of the same kind (below)
and advisories (strategy not bound to protocol version, carried; `summarize.complete`
tolerating `unsupported`, carried; the admission oracle being a transcription that can
drift from the host; coverage limits of the new tests; host predicates the classifier
cannot mirror from a session envelope, stated as limits).

## The prosecutor's four contested Importants — for the finalizer

The prosecutor attacked **118 members** and, applying the stated standard at the
*parsed-content* level, raised four Important candidates:

- P-01: an unknown or relabelled v1 `selection_reason` (e.g. `"table_hit "`) is
  host-refused but receives chip and agreement eligibility (denied `hit` only at the
  agreement gate).
- P-02: v1 `state_before_sha256` / `state_after_sha256` / `visible_cards_sha256` /
  `blueprint_sha256` / `action_index` / `street_action_index` mismatches that the host
  refuses with `state_mismatch` are re-derived only at the agreement level; chips are
  credited first.
- P-03: v2 records pass the public validator plus identity and delivery checks but skip
  every host state/legality rule and receive chip credit with no diagnostic.
- P-04: the host's 65,536-byte stderr capture cap is not mirrored; an oversized stderr
  with `capture_truncated: false` is admitted.

Each went through three-lens adversarial verification. **All four are CONTESTED (1 of 3):**
upheld under the *reachability* lens (the paths are exactly as described in the frozen
bytes) and refuted under the *contract* lens (no packet document requires host-equivalent
admission at the parsed level; the accepted design §5 deliberately routes reason relabels
and replay mismatches to the agreement gate with chips retained; a frozen test pins that
scenario as "not hit, chip-eligible"; the r001 disposition's own language preserves
"agreement-only treatment of an unknown/relabelled reason") and under the *already-handled*
lens (chips derive from the host-authoritative `applied_actions` replay bound to two
retained settlement copies, so the mismatched record cannot move them).

The coordinator's reading, offered to the finalizer rather than ruled: the r002 promotion
concerned bytes that are not a valid host *stream*; P-01–P-03 concern *content* a real
host would reject semantically while the settlement the chips derive from is real. Whether
host-equivalence extends from the parse boundary to semantic refusals is a design question
the accepted design answers with its two-stage structure — but the r002 ruling was made on
a distinction ("no new credit path") that the finalizer rejected, so the finalizer should
say explicitly which side of that line these fall on. The critic's view: P-01 sanctioned by
the brief and design §5; P-02/P-03 pre-disposed at r002 with P-03 "the stronger gap and
cheap to close"; P-04 a genuine asymmetry with no consumed bytes, Minor follow-up.

## The critic

Probe-clean, given all three inventories. It verified the byte-level parity claim
predicate by predicate, confirmed the one asymmetry (the classifier refuses non-finite
floats the host admits) cannot exclude a host-completed stream, and found two items
nobody named: **N-1 (Minor, constructed-only)** identity-label charset regexes are not
mirrored, so a consistently substituted out-of-charset session id is host-unreachable yet
can reach `hit` — no game semantics, `play()` always supplies a valid label, not in r003's
scope; **N-2 (Advisory)** the v2 `config_sha256` is a constant and therefore mirrorable,
corrected from review 01's "cannot mirror". It traced every assignment to `chip_eligible`,
`agreement_eligible`, `hit`, `summarize` and `complete()` and found no credit path beyond
the disposed P-01–P-03 class. Its recommendation: CLEAN for the r003 scope; carry N-1,
N-2, P-03 and P-04 as explicit follow-ups before the classifier becomes the Slice B
interface. It also notes `checks/review-gate.json` ("broad: Not yet run") is stale
relative to `checks/broad-gate.json`.

## Coordinator's recommendation

CLEAN / SOUND for the authorized r003 scope, with P-03 and P-04 and the critic's N-1/N-2
recorded as follow-ups for the finalizer's disposition, and one explicit ruling requested
from the finalizer on where host-equivalence stops. The finalizer for this checkpoint is
Codex; his own r003 passes exist in his scratch and are his to publish.

## Exposures and deviations, disclosed

- Probe `NONE`; the reviewers disclosed only the ordinary git-status block.
- The coordinator's critic prompt still carried r002's path list ("tests/cases.json …
  (new)") and directory prefix. The critic detected and corrected the path error from the
  bytes (cases.json is unchanged; test_eval_protocol.py is modified, not new) and wrote
  its report under an `r002`-prefixed directory name; the bytes are copied here unchanged.
  Coordinator's error, no contamination.
- The critic wrote one generator script to its session scratchpad (disclosed in its
  report); no project code was run by any agent.
- Agent count: 17 (probe, two reviewers, prosecutor, critic, and 12 verifiers — three per
  prosecutor candidate). The controller has ruled that scale unaffordable; the dispatch
  script is being changed so verification runs the contract lens first on a small model and
  escalates only survivors, with a hard cap on verifier count.

## What this does and does not establish

Two probe-verified cold passes, both CLEAN / SOUND, satisfy the handoff's Tier C
requirement for this round; prosecutor and critic are supporting evidence. Nothing here is
broad-suite clearance, adoption, or authorization for the retained solve, export or
agreement invocations.
