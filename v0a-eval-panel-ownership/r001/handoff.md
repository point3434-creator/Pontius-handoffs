# Cold review: v0a-eval-panel-ownership/r001

Candidate: 182d14e213c6f0b7d7578e429f81d051a9e59707
Manifest: 438d192a26e39b216cca33099c79f6f607de8e2ec1ca1749d44a50434bc7f6f6
Base: 0bc19bcaad5c6660468094772216cac2dc27a651
Tree: 81f2e97805bcaf9e93a05b98ecc4277e1c2dd32c
Ref: refs/heads/review/v0a-eval-panel-ownership/r001
Tier C. FIX. Codex drafts/finalizes; Claude reviews independently.

Scope: cleanup, caller-owned observations and boundary publication.
Only tools/v0a_eval_panel.py and tests/test_eval_panel_tool.py differ from BASE.
This is a separate contract candidate required by r004's second-residual disposition.
Review the whole affected contract and its consumers, not only the latest example.
The bridge and all sealed source remain unchanged. Design steps 4-7 remain outside scope.
The governing brief/design are at f647a7989394f084875a040b20c41891168163ed under
docs/architecture/v0a-eval-panel-impl-r001/ and its referenced parent design.

Record your independent invariant/related-path inventory before opening coverage.md,
checks/, inputs/prior-disposition.md or inputs/repair-plan.md. These are deferred FIX
inputs, not a substitute for independent discovery. Do not read implementer transcripts,
prior-round review files, or sibling reviewer outputs.
Deferred coverage SHA-256: b13e8d56c170978438417086636b66e81539df1d8030ff878daf9cb23e214a1d

Verify ref, parent, tree, scope, exact whole-row-sorted LF manifest and pinned bytes
from Git objects. dependencies.json pins refer to its stated original base, not this
candidate's immediate parent; check that provenance explicitly.
No candidate execution, tests, owners or source changes are requested from reviewers.
Use the supplied focused RED/GREEN receipts; both executed in disposable snapshots with
their own locked dev environments, CPython 3.14.6, -B -P, ResourceWarning-as-error,
scrubbed environment and absolute PONTIUS_GIT. All utility Python must also be 3.14.
PowerShell/.NET is available for byte verification. Tests are correctness evidence,
not authorized capacity/preflight measurement or evidence of poker strength.

CLEAN requires no surviving material finding. Give SOUND, STRAINED or WRONG SHAPE
separately. Each Important/Critical finding needs exact frozen locations, a concrete
counterexample, violated invariant, and required correction and verification outcome.
Missing coverage alone does not prove a product defect. Compare the independent
inventory with deferred coverage before issuing the verdict.
Publish attributed reviews/review-NN-REVIEWER.md and one original task-ledger line.
Issued files and frozen inputs are immutable; corrections are appended records.

## Pinned inputs and receipts

- inputs/authorization.md
  b88a16216550509adb3b0e30b55370c580024a8116ee1bd583112d884634a7f7
- inputs/controller-rulings-addendum-2.md
  0b708f7619c25167a51d55f8af00baa3cedc3e8a85e0a80511c18bd178e93dfa
- inputs/controller-rulings-addendum.md
  d3a15c896463449913fa0852b51f654ac7688b6c6941b57652a745244e040a6c
- inputs/controller-rulings.md
  9652b870dfb214af764addb3de276c776d51015d7e55b75b98d0bb519711f3bc
- inputs/dependencies.json
  ab0933726111415870200d4b14358012826da35fd2f083890cf7d8b0165f50b2
- inputs/prior-disposition.md
  f9e3c1a1303ac67494e40e9ed0b5ea2b7cb26d0d665ac11232c10a356aed9ac3
- inputs/repair-plan.md
  463cd0b4eb413a3df8d72b5000eddaa7295a3a16071b359ee9bf15661f2db9f8
- inputs/workflow.md
  c71e3963ff726e06158878bcc10dd7dd761b32597af1c8ed39e21ebf60b58a37
- checks/focused-journal.jsonl
  962dc0ee0ad8f619ba93bb8781dd5a367506d0c25d2cba81cf8ee25238629f18
- checks/focused-receipt.json
  e9e21be64be990b5f0e2254ebeae39452ed498029f13693c71f4da914b2c58b2
- checks/focused-stderr.txt
  e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- checks/focused-stdout.txt
  5627395b92ea358e6e9433191648126745a72d58e3edf541c3e898a1d9afeba7
- checks/red-journal.jsonl
  be242df62565754c2a498016b6867301cac5378f35fca1ccdfa4aee4d36c111e
- checks/red-receipt.json
  05fcd8216e1357b2b58ec3484c8830306bfe304dca0b9f3269723a53be143845
- checks/red-stderr.txt
  e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- checks/red-stdout.txt
  2a6e79ff7a9200a082a6dfb8901550e286601a05bbb12bd714a52959d594fde5
