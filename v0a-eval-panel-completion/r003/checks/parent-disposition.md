# Completion r002 finalizer disposition

Finalizer: Codex, 2026-09-09 (America/New_York).
Defect verdict: NOT CLEAN. Design verdict: STRAINED at raw-frame admission.
Candidate: 430ad75de79cec13d66ff3dc4981dd3770a371b7.
Manifest: 6e36bb41bcab8c47aed1fc87066e40cde857bee24e2f08bfdc5cb80d28604cd5.
Parent: 449a2a3c1fa1f5a7f5f04adca32e499faaf81e13.
Published review commit: b850cafd6291121af8fd5cb69552a3b2dfef6620.

## Identity and review qualification

Independently verified the ref, sole parent, tree, three-path raw-blob manifest,
35 supporting pins, 51 dependency pins and all eight published review/inventory/
coordinator artifacts against Git objects at b850caf. Exact hashes are in
checks/finalizer-audit.json. The candidate source was not changed.

Accept both reports as independent cold substantive passes. The probe and both
disclosures report no inherited candidate findings, lane verdicts or memory
content. Ordinary status/ref names provide identity context, not substantive
priming. Review 01 hashed coverage bytes before its inventory without displaying
the contents; no claim was read. Review 02 authored an extra scratch hash utility,
contrary to the two-output instruction. Record that process deviation; it does
not introduce review contamination or make the substantive analysis non-cold.
Future dispatch should keep utilities outside the two-deliverable assertion.

The prosecutor and critic are supporting analyses, not additional cold passes.
Their source-backed observations remain useful. Their universal no-credit claim
is contradicted by the executed framing counterexample below. All issued reports
remain unchanged. Cold independence does not establish correctness by itself.

## I-01 Important - host-invalid framing still receives successful credit

Locations: src/pontius/eval_agreement.py:149-154 (decode and splitlines), 312
(chip eligibility), 357 (hit), 374-378 (completed/hit summary).
Authorities: tools/v0a_table_host.py:52-90 (decode_json) and 530-535 (LF framing).
Requirement: inputs/accepted-design.md:227-230, inputs/completion-brief.md:55-56,
and brief.md:10-12 exclude malformed frames/protocol before chip or hit credit.

Promote review 01 F-01 / review 02 F02-02 / prosecutor C3 to one Important
enforcement finding. The prosecutor correctly observes that the normalized
proper-line form could receive the same credit. That is not the required
predicate: the retained byte stream itself must be admissible. The claim that
these divergences fail closed is false.

Executed reproduction, before any production edit:

- Interpreter CPython 3.14.6, -I -B -W error::ResourceWarning; frozen source
  430ad75d verified by begin_run. Utility source is pinned separately.
- Reused the existing actual CHECK-host capture in r001's diagnostic receipt;
  no new host process was launched. The original raw stream passes the unchanged
  host decoder on LF-delimited frames and classify returns hit, chips=-2.
- Mutated only captured stream bytes and re-encoded base64: (1) LF -> CRLF;
  (2) first LF -> record separator U+001E; (3) first LF -> U+2028;
  (4) pad the ready frame with 16,384 spaces so it exceeds the host frame limit.
- All four are rejected by the unchanged host decode_json with protocol_invalid.
  All four return classification=hit, chip_eligible=True, agreement_eligible=True,
  causes=[]; summarize reports completed=1, hits=1, complete=True.
- The diagnostic completed with exit 0 because its assertions establish the
  defect. This is a failing-contract reproduction, not a GREEN acceptance run.
  Result SHA-256:
  4d9f5bc4b3121c5849f3b3b61f2ab6243e5f131e1c001c27bda137a74ff8a437.

Three adversarial checks:

1. Reachability: classify is the declared retained-envelope admission boundary,
   and the existing correctness tests mutate actual captures at that boundary.
   The producer need not naturally emit a malformed frame for this contract to
   apply. That is the same scope used to uphold the missing-member cases in r001.
2. Requirement: malformed frames are explicitly excluded before chip credit.
   This is not a new demand for canonical JSON or a general stylistic preference.
   The actual host's physical framing and admission limits provide the oracle.
3. Elsewhere handled: universal splitlines and unbounded JSON parsing precede
   all schema/replay checks. Those checks see normalized records, so identical
   actions and settlements cannot detect the discarded framing violation.

Impact is invalid-observation acceptance, not a changed poker action, false win
or changed chip amount. It invalidates the stated hit/completed evidence gate.
No full-H run or full-coverage claim was executed by this diagnostic. No evidence
is offered that normal Session captures naturally become malformed this way.

## Root cause, correction scope and gates

The r001 member/default/coercion examples are closed: exact received member sets,
typed counters and v2 codec admission work as the reviewers describe. The remaining
gap is earlier: text normalization and a separate incomplete raw parser operate
before that admission stage. I fixed parsed objects without completing the byte
boundary. The decision-admission structure is sound; the overall raw-admission
contract remains strained. A whole-bridge rewrite is not justified.

Required next correction: one explicit raw-frame admission step matching the
frozen host's physical LF framing and bounded JSON contract, before schema
construction. Enumerate framing, byte size, BOM/CR, depth, numeric parsing,
duplicate/unknown keys, decoding failures and closure; distinguish existing
guards from gaps. Catch parser failures as excluded outcomes with a cause.
Preserve v1 unknown string reason disagreements, valid v1/v2 chips, actual
baseline divergence, lookup semantics and exact byte/source identities.

The companion repair-plan.md makes the bounded next candidate concrete. No
production/test edit or broad-suite invocation was made during finalization.
Completion has used r001 and r002; the frozen completion brief requires returning
to the controller after at most two rounds. Return with this disposition before
starting r003. Historical general correction/line-budget grants are preserved;
they do not silently erase the checkpoint's explicit stopping rule.

If continuation is authorized, freeze a distinct r003 with no ref retargeting;
two qualifying cold passes must precede broad verification. Exact per-commit
authorization then governs adoption. Every later retained phase still needs
its own bound plan and one-shot grant. No adoption authorization is requested
for this rejected candidate.

## Other findings and supporting claims

- Review 01 F-02: accept Minor. RecursionError escapes the exclusion return but
  fails the phase without successful credit. Include parser-depth/refusal handling
  in the same raw-admission correction because it shares that boundary.
- Review 02 F02-01 / 01 F-03: accept nonblocking strategy/protocol labeling limit.
  Frozen Slice A play fixes v1; a mismatched caller cannot manufacture a hit.
  Address before using the classifier as the Slice B policy-attribution interface.
- Review 01 F-04 / prosecutor C4: accept explicit outer-envelope and external
  identity limits. Unknown unused members do not grant credit; current worker
  binds wire/deal inputs outside this classifier. No extra source scope here.
- Review 02 F02-03: accept caller-input typing advisory. Caller stacks/teacher
  mappings are not wire objects; frozen callers supply the declared exact values.
- Review 01 F-05 / 02 F02-04: generic summarize.complete is outcome resolution,
  not primary acceptance. Unchanged worker/parent require every primary to hit.
  Preserve this distinction for the next consumer.
- Review 01 F-06: accept ref-navigation advisory. r002-verified is the only issued
  candidate for this packet. Preparatory refs remain immutable and need explicit
  archive/retirement handling at final adoption, not retargeting now.
- Critic corrections about base64 bytes inputs, -0.0 and trusted caller stacks:
  accepted as limits of the prosecutor's wording, without a new credit defect.
- The critic's other traced seams, including baseline replay separation, do not
  rebut raw framing. No further material finding is asserted from those seams.
- Focused receipt remains valid: six suites, 79 unittest cases, zero skips,
  source_verified=true. Its mutation matrix does not exercise the raw-frame gap.
  The prosecutor/critic correctly disclose static-only verification; this new
  executed result supersedes their no-credit conclusion on framing.

All new disposition and diagnostic records are local, create-only additions.
No review bytes, frozen source, sealed parser or prior ledger line was rewritten.
