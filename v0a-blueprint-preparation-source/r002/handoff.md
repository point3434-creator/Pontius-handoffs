# Mechanical verification: v0a-blueprint-preparation-source/r002

This is the qualified mechanical route in docs/workflow.md Stage 4, not a new
cold substantive review. Coordinator /root is the finalizer. Inspect only the
cumulative correction, eligibility, related consumers and retained prior reports;
do not repeat the already completed whole-source audit or execute any test/poker/
profiling/owner/lifecycle work. All source and packet inspection is read-only.

Corrected candidate: `666cb43b097707a54733a51cd7930d55920a5af7`; parent/adopted base: `c9a8aa95a1c8f65bcfb15288cbc5e4492314e457`;
tree: `2515fe2cf7259b611f60e5b2582e846422cb0247`; full 24-blob manifest: `4ac5089861356eb3bfe25f8d4c2b45aff3c9b39b4306a51a66ea3f5d01fa4012`.
Fixed substantive anchor: `d3717e7153bc2acad43672e954fbd53bcdd51fe7`;
anchor manifest: `5405d27ea6a72de5fbfb0f0cced81f9b34b71178e7914f85f2fb44c4fe0a42b1`.
Both formal refs and exact nine-field candidate records are in these local packets.
Verify raw blobs and complete sorted manifests independently through native Git.

Both Tier C substantive passes on the anchor completed. Read these issued reports
verbatim; prior findings are permitted inputs for this mechanical verification:
- `D:\Pontius-handoffs\v0a-blueprint-preparation-source\r001\reviews\review-001-codex-a.md`
  SHA-256 08ef2835d4f8aba10a8d1f66ee3b1142b0bd0c399f4f75d1380558a12ae4e8e2.
  Verdict NOT CLEAN / SOUND; sole required finding is Minor CI comment encoding.
- `D:\Pontius-handoffs\v0a-blueprint-preparation-source\r001\reviews\review-002-codex-b.md`
  SHA-256 2810966dae3d823503319de75927cb6d61482ec4eaf7d3333b45831ead56c664.
  Verdict CLEAN / SOUND; same comment issue is advisory. No behavioral finding.
These reports remain unchanged; do not turn A's original verdict into CLEAN.

The complete cumulative delta from the fixed anchor is three byte-span restorations
in .github/workflows/ci.yml comments at lines 3, 30 and 90: UTF-8 mojibake is replaced
by the original B U+2014 bytes. Each resulting whole line must equal B. All other
file bytes, including the intended CI blocks, are identical to the anchor.
Read CLAUDE.md, the Stage 4 mechanical rule, and ADR-0513/source-contract.md as needed
to confirm authority. There is no behavior, normative text, gate, clock, ID, expected
outcome, source-position line, analyzer population or generated-data change.
Verify this claim rather than assuming AST equality is enough: inspect YAML comment
placement, exact cumulative raw diff, line maps and relevant CI/census consumers.

Return eligibility verdict ELIGIBLE/INELIGIBLE and correction verdict CLEAN/NOT CLEAN,
bound to both complete commit/manifest pairs. Include the exact delta, verification
performed, closure of the sole required finding, any remaining issue, and design
verdict SOUND/STRAINED/WRONG SHAPE. If a substantive concern appears, stop this route
and identify it. No implementation, new source scope or decision/push authority is
granted. Broad exact-candidate gates on 3.11 then3.14 follow successful closure.
End with an attributable single ledger line preserving both anchor and corrected
identities and your mechanical eligibility/correction/design verdicts.
