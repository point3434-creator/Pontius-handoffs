# Independent initial closure-path inventory: coverage-guidance/r002

Reviewer: Codex. Recorded 2026-08-30 before opening coverage.md.
Candidate: 81fb6cf6491b7ae87ca2a2a3ccd0a7103c4cfed3
Manifest SHA-256: 2c9903843b765143f2f2a33c4c3e0233ff0ca9c907faae9462f12b2577e56fdc
Prior candidate: d07b11e874955121487351a20104dec5176f9cb3
Scope: FIX I1 only; a light review of frozen docs/workflow.md.

## Inputs and discovery

Read handoff.md, candidate.json, manifest.sha256, the allowed r001 review I1,
and the complete workflow blob at the candidate commit. Read frozen CLAUDE.md
and the workflow amendment for applicable authority; inspect PROJECT.md's
Evidence and dissent protocol. Mutable workflow bytes, implementation transcripts,
pending design-verdict edits, and other tasks are excluded.

Discovery method: walk Stage 1, every Stage 4 closure paragraph and bullet,
Stage 3 verdict rules, Stage 5 gates, and the request/brief templates. Search
frozen workflow and its governing documents for RED, GREEN, Each finding,
Every binding, coverage-only, CLEAN, and advisory. Compare the exact r001-to-r002
diff, which changes only the Stage 1 and Stage 4 opening paragraphs.

## Independently identified paths and invariants

1. Demonstrated behavioral failure: reproduce deterministically before fixing;
   Stage 4 requires RED against the rejected candidate before production edits,
   then integrated GREEN. Locations: workflow lines 61-65 and 191-193.
2. Missing evidence with correct behavior: establish the missing or unsound
   evidence, supply an independent behavioral check, and record its result.
   A passing result on the rejected implementation is permitted; neither an
   invented failure nor a production edit is required. Lines 193-196.
3. Unsound prior oracle or discovery: repair the evidence through an independent
   contract check; source structure alone cannot close it. Lines 193-197,
   212-238. This is separate from proving a product failure.
4. Newly exposed product defect: a coverage check that demonstrates failure
   transfers that defect to the ordinary RED/GREEN path. Lines 196-197.
5. Unresolved evidence: a check that does not establish the required contract
   cannot close a required finding or justify CLEAN. Lines 161-166, 222-238.
6. Advisory concern: no unmet acceptance requirement and concrete unverified
   failure scenario means no automatic blocking coverage finding; advice stays
   advisory. Lines 183-187 and 222-229.
7. Repeated residual or proposed replacement: the existing second-residual and
   replacement rules still apply; these must not silently mandate a production
   rewrite merely because a check was missing. Lines 239-262.
8. All paths retain the frozen identity, scope, independent review, severity,
   real-boundary evidence, isolated verification, and per-commit authorization
   rules. Closure is not acceptance or authority to integrate. Lines 13-23,
   150-166, 198-238, 264-306, 338-370, 375-410, and 431-460.

## Remaining consistency checks before verdict

Compare the author claim with all eight paths. Walk the r001 A-then-B example
with correct product behavior, the same example with a demonstrated defect,
and an inconclusive check. Check that role shorthand (lines 28-29), replacement
RED/GREEN wording (259-261), brief RED targets (426), and the cold-review
CLEAN wording (446-458) do not override the explicit coverage-only closure rule.
Check that the source diff preserves all unrelated gates.

## Identity and scope observations

Absolute Git resolved the ref to the supplied commit, with parent
 d1ed3cbda6107d61ea8e77133871720af04970cd and tree
 33dc90fc78bb8ec62f07c7afed82f6b4b2a4851e.
The parent-to-candidate changed-path set contains only docs/workflow.md.
The stored blob SHA-256 is
51ca0741ebe4ed0289525642967deabbf4c422ba830c7fd781d3ad2b1119d39b.
The reconstructed LF manifest row equals manifest.sha256 byte for byte and
hashes to the supplied manifest digest. r001-to-r002 is 10 additions and
4 deletions in that one file. diff --check exits 0. The blob has no CR, BOM,
trailing whitespace, or lines over 100 columns.

No tests, production imports, code edits, commits, or pushes were performed.
This inventory is a pre-claim record, not an issued verdict.
