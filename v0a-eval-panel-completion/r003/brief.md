# Completion r003 raw-frame admission FIX

Tier C. Codex drafts/finalizes; Claude receives the frozen packet for cold review.
Explicit controller reauthorization is in inputs/r003-authorization.md.
Base 430ad75de79cec13d66ff3dc4981dd3770a371b7. Scope is exactly
src/pontius/eval_agreement.py and tests/test_eval_protocol.py. All other source
and test registration are unchanged. Python 3.14.6 is the only runtime.

The governing completion/accepted design remains in inputs/. Relevant outcome:
host-invalid raw physical framing/JSON cannot receive chip or agreement credit.
Use frozen host read_stream/decode_json as the framing and JSON oracle, and the
existing decoded-record/model/codec and kernel contracts at their later stages.
The classifier's existing finite-number restriction remains in force. Valid
v1 CHECK hits, off-pool defaults, reason-only disagreements, and actual completed
v2 baseline divergence retain their previous outcomes and settled chips.

Scope includes physical LF framing, retained stdout/frame byte bounds, CR/BOM,
JSON depth and integer token limits, duplicates, decoding and parser failures.
No changed host/session/codec, solver/export arithmetic, timing or ownership
contract, generalized protocol framework or retained measurement is authorized.
The whole-slice production ceiling remains 3000 lines. Working figures remain
disclosed in checks; do not silently turn them into new authority gates.

Two qualifying cold passes precede broad snapshot verification. An unresolved
material residual returns to the controller; no implicit fourth round. Exact
adoption commit and every retained phase still need their own authorizations.
