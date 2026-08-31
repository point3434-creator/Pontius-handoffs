# R2 baseline verifier v1: bounded engineering review

Reviewer: codex/r010_cold_a.
Design verdict: SOUND for the bounded data-only approach.
Release disposition: v1 is blocked by the two source-proved verifier defects below. This is not a production finding or a runtime result.

Frozen pair: H 06e6adf1366d6b47efdb904fb957044510dcb85b; rewrite-r2-harness-review-v1-manifest.sha256 SHA-256 5bf6ffd55ecb6794dddfd5a00c5b6912b7a8b9be13e5bd308e369d75db23af06.
Reviewed tool: coordinator-verify-rewrite-r2-baseline-v1.py SHA-256 22def22c092c8c8b499303974691b2b877bc45c75a2665d23618764cb7edbad9.
I independently read the manifest and all four entries as Git blobs at that commit and matched their local raw bytes/hashes.

Comparison: c00f7375a7be68daff773b4d8c6413467aa2e6be harness, manifest a2e7a238c4b87b46d6e48dad9106b13c39012fb674a4c0373b54873510815b5d; probe 0c1d7065b21e7d45a002b2e83e3ada9e29a22e3129e9168378370f231500c5bb; control bb68e24c1d01b4b04eb499274c6d714c329ea8eab56cfb3a11f4394b92d5d2a9; population v2 8ab800c1361ca53f4f294bd32e308ecb7061e031b60d32dc74d7fdf52cc5ce3b. The source remains strictly c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f.

Important BV-1 — wrong frozen population gate key, line 119

The verifier indexes pop['gates']['B']; the pinned successor population contains A and B_identity. Every otherwise valid run reaching this line raises KeyError before case replay. Use the actual B_identity key and retain the original file as the unexecuted predecessor. This is verifier/schema consumption, not a change to the population or its expectations.

Important BV-2 — runtime-copy/original-input links are incomplete, lines 69–93 and 123–139

SOURCE is checked in receipt/identity metadata, while actual snapshot files are rehashed only against receipt.before. The verifier does not independently require the actual generator and retained-source.py bytes to equal SOURCE. Similarly, it verifies original probe/control/plan/map files against the frozen harness but does not equate their snapshot copies with those verified originals.

The three snapshot pack hashes are checked against receipt.pack_sha256, without linking them to the pinned population's pack identities. Selected record/source/Model bytes are not rehashed against the population descriptors; the printed source/Model hash fields are compared instead. These checks establish self-consistency but leave the tool's claimed exact runtime-input closure dependent on earlier controller validation.

Required bounded correction: an explicit map from all sixteen copied runtime payload files to their rehashed original inputs, a separate run.json configuration/context check, SOURCE equality for actual tools/generate_test_inventory.py and retained-source.py, population-to-pack hash links, and selected canonical-record/source/Model hash checks. This closes the evidence chain without importing the controller or duplicating all its semantic predicates. No tampering or runtime probe was executed to demonstrate this source-level gap.

Other bounded conclusions

- The tool imports only stdlib modules. Its sole subprocess site is the fixed-argument-list Git wrapper at line 32, used for show, ls-tree, rev-parse and status. There is no eval, exec, compile, importlib payload loader, candidate import, Model execution or harness invocation. Its only intended new artifact is the final create-only JSON verification report.
- The three pack keys and depth/non-depth record layouts otherwise correspond to the frozen harness. The two original depth regexes remain exact. The 1778-file floor shape is consistent with 1761 tracked files plus seventeen payload files, with manifest.json separately hashed.
- Requested-unit arithmetic retains initial work separately, checks all epochs and exceptional requests, and applies the 196608 reserve to requested_units. It does not alter a budget or production cap.
- It distinguishes twelve-attempt/twenty-four-projection observation from ten-receipt/two-depth completion and from success. Semantic, analyzer, reserve and mechanism failures remain RED; mere observation does not imply success. A baseline-only verifier must remain source-bound; a future GREEN adapter needs separate reviewed verification rather than silent widening.
- This is expressly a supplement to frozen controller replay. It does not independently derive every mechanism predicate or reproduce every exact-type/schema guard. Its output must not be presented as replacing that replay. Generic harness-ref/manifest arguments can accommodate a separately frozen lifecycle-only successor with the same schema; no unpublished successor was reviewed here.

No other concrete schema-key/field mismatch was found in this bounded pass. Root has acknowledged both corrections and owns the create-only successor. R2-H1 lifecycle closure remains the separate harness-author task.

No verifier, candidate, harness, test module, Model or sensitive fixture payload was imported or executed. Only own stdlib AST/hash/data inspection and read-only Git blob comparisons were used. No tool/source/test/population or existing artifact was edited; this review is the sole create-only output. No dispatch or implementation GO is granted.
