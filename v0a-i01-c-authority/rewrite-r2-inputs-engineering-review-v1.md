# R2 identity-input engineering review v1

Reviewer: codex/mapping_compatibility, 2026-08-31. New-input review only; I did not author these four cases. I participated in the R2 design, so this is engineering review, not a final cold pass. No source, Model, builder, analyzer or test payload ran.

**Design verdict: SOUND. Input verdict: one Important closure defect; not ready to dispatch from this population.** The identity premise and independent Model shape fit the bounded contract. The defect is a missing referenced envelope, not a reason to redesign the cases or weaken their expectations.

## Frozen identity

Findings bind to H `aa75536cad0ae54b76b02f9351cd7bc789d7f443`, tree `3e1fe8610d95999681ed3ef30b2f3caa1aa679f4`, parent `90a1632ffce0ebff767a1103c3739b48c0546643`, and `rewrite-r2-inputs-v1-manifest.sha256` SHA256 `96d1b71a3a08b73d2cf1bb09d3ac06473253b6291addf2fbefc541e3bbe3b41f`.

Independently read all six input blobs from that commit and reproduced their manifest hashes, whole-row byte sorting and LF bytes; working copies matched those blobs. The commit adds those six inputs plus the manifest/release metadata. The release pin set matches the six manifest entries.

| Reviewed new input | SHA256 |
| --- | --- |
| tests-checks/rewrite-r2-identity-cases-v1.json | 4834971b9d63aa182c1207959721b6bb65f742a106541d96975945060134d9ea |
| tests-checks/rewrite-r2-identity-population-v1.json | 30295f39daafcf265103cd78f3de50393c9111633ca3d5f8515e3f77c9a1197a |
| tests-checks/rewrite-r2-identity-source-model-differences-v1.diff | d132ded3312b936a5510a4c498f39c06d3a4a6259903cd8ddef0269211e110a6 |
| tests-checks/rewrite-r2-identity-coverage-v1.json | 05e24952ff5672554012bfb784215d76e44f7d95b2f3dbd1e3c0f8672d13ec38 |
| tests-checks/rewrite-r2-identity-inputs-handoff-v1.md | 354c38c26be50e1992a155ffd9505f8fecc23fdeb67482e4cb70853e0046effb |

The sixth manifest input is my separately authored plan addendum `1a1a6bc7f8ef4c56a72735670ff0bb65e883f3aa559abec7b4fec01af6991998`: hashed for closure, not independently reviewed by me here. The adopted premise is `bdf3b13684d50318c48ddbe3af1682b6e298136e21af3d1ef76ffe7a3f52e6b4`.

## Independent inventory recorded before coverage inspection

I first enumerated: frozen-blob/manifest closure; exactly four reversible source/Model substitutions; one open selector read with no public domain injection; three singleton identity decisions/four disjoint regions; preserved ambient/work/raise/handler/sink behavior; independently harmless Models and reasoned witnesses; unchanged six Gate A plus two original depth descriptors/builders/envelopes; unchanged classifications/caps/owners; and static claims separated from future actual mechanism evidence. Only afterward did I open the input coverage document.

## Important R2-I1: two unchanged cases reference a deleted envelope

Location: `tests-checks/rewrite-r2-identity-population-v1.json`, lines 339 and 381, versus the `envelopes` table beginning at 728.

Both `hidden-cell-joined-dormant` and `hidden-cell-joined-reached` correctly retain their original `envelope_ref: "name_environment_public"`. The new table contains only `identity_name_environment_public`, `original_design_review`, and `storage_composition_public`. Consequently these two references do not resolve. Ten other case references resolve.

Concrete failure: a controller following the population's declared envelope references cannot construct either hidden-cell public attempt; it must fail lookup or invent an undeclared fallback. Redirecting them to the new identity envelope would also risk substituting Model(region) for their original projection contract. Thus equality of the eight copied descriptor records does not establish a closed twelve-case population.

Required correction: issue a population-only successor adding the exact original `name_environment_public` entry alongside the identity entry. Keep all eight original descriptors and both existing envelopes unchanged; do not rename their references or reuse the identity Model constructor. The required original entry's canonical JSON SHA256 is `9c27bf22e70df68f996ef0d91b8763ef7e7467f148067be45aab500c92dc6b14`, using the population's stated no-final-newline canonical encoding.

Verification: every case's envelope_ref resolves; the restored entry equals the original population entry; all eight original descriptor canonical hashes still match; the four identity records still use their distinct envelope. This is a source-proved input defect, not an executed analyzer failure. No files were repaired.

## Remaining static checks

All checks below passed independently against frozen new bytes and pinned originals:

- Exactly four approved identity-prefixed records exist, with four Model projections each. Source inverse removes only one selector latch and restores the three original equality predicates; all four inverse source strings equal their predecessors byte-for-byte. Model inverse additionally removes its new constructor and equals each original Model byte-for-byte. Independently regenerated unified differences equal the issued diff exactly.
- Each sensitive test has exactly one self.choice load, one selector assignment and three Is comparisons, with True/False/None in order and else as the complement. No constructor or Model region/domain assignment appears in sensitive source. Normal latches follow ambient/work initialization; exceptional latches are inside the original try immediately before the ladder.
- N8/N64 ambient assignments and D0/D2 work paths are exact. D2 branches retain (1,-1)/ValueError, (2,-2)/TypeError, (3,-3)/KeyError and (4,-4)/IndexError; the four-type handler and common launch remain. Source/Model test ASTs agree after removing only event/output projections and preserving empty branch/handler Pass nodes.
- Models have no imports or sensitive calls. Direct calls are restricted to exact-string validation, fresh object creation and the four builtin exceptions; attribute calls are event append and the harmless launch. The constructor accepts true/false/none/other strings, creates object() only for other, and rejects invalid values. Fresh per-projection namespaces and nonserialization of the selector remain explicit future-wrapper requirements, not demonstrated runtime properties.
- Independently derived all sixteen expected projections: D0 branch:i then sink with work(0,0); D2 branch:i, raise:Type, handled, sink with the corresponding signed pair. Every ambient projection is 0 through N-1. Changing only region back to predecessor choice reproduces every old witness. The Model result "fixed" remains a launch-projection label, not a claim about a real subprocess return object.
- Recomputed all new record/source/Model/expected-data hashes and predecessor pins. The original name-environment and storage-composition packs remain unchanged. All eleven separately pinned original dependency files match their retained raw hashes; these are explicit original raw dependencies, not a claim that every such file is present in this H tree.
- All eight original descriptors are exactly equal to the original population, including source/Model hashes, classifications, original builders and error assertions. Gate A itself, all five caps and the budget-scope object are exact. Counts remain twelve public attempts and twenty-four Model projections: six clean, three refuse, one permitted-refusal, two exact-depth assertions.
- Independently rehashed the original r010 test-module blob: `c46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf`, 1,265,190 bytes. Verified 28 pinned source spans covering builders/assertions/setup/public dependencies, and AST correspondence of the retained helper65 and generator70 builders without calling them. Both exact depth strings remain. The complete original depth envelope, fixture/probe universe, child source dependency and default include_probe behavior are unchanged.
- The identity envelope preserves original API, inventory/stable identity, source path and original public_review reference. Its serialized inventory hashes and decodes to the declared document. Reading the pinned public_review body confirms only source/inventory inputs are passed to derive_design_review: no Model selector/domain fact is supplied.

## Coverage and limits

The coverage claim accurately records zero exercised cases/projections and separately requires actual one-analysis decisions, four alternatives/join and D2 write/raise/handler paths. Static AST correspondence and equal argv cannot establish those observations or cost headroom. The inherited hidden-cell pair still permits/refuses unsupported precision; it is not independent proof of joined-cell execution.

The coverage/handoff claim of a preserved full population is incomplete specifically because R2-I1 omits the referenced original envelope. No other required correction was found in this bounded input review. Twelve other affected scale siblings remain explicitly outside this prospective correction; no whole-family acceptance is implied.

Static work used actual CPython 3.11.15 with -I -S -B -P for stdlib JSON/AST/hash comparisons, absolute Git blob reads and plain source inspection. Two initial Git reads stopped at the sandbox-account ownership guard; subsequent explicitly scoped owner-context reads succeeded without changing Git configuration. No candidate/test module was imported, no builder or Model was called, and no payload or controller ran.

A corrected input successor still needs root review/freeze and the separately reviewed exact controller before baseline or candidate execution. This review grants neither production source GO nor runtime readiness.