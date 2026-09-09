# Cold review: v0a-eval-panel-sample/r001

Candidate: 72954e1331c9b191d927c1c4b82f277bcd322a4c
Manifest: d79035495a278fa8ee3fb1a6adc6fc1838938900ab7c19bbdd434264faf63510
Base: 182d14e213c6f0b7d7578e429f81d051a9e59707
Tree: 73797f3b554f68c3ced59cc295b0e41f1507b8bb
Ref: refs/heads/review/v0a-eval-panel-sample/r001
Tier C. FIX. Codex drafts/finalizes; Claude reviews independently.

Scope: role-bearing admission, worker execution, complete-sample reconciliation and estimation.
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
Deferred coverage SHA-256: 9b481d761c8eaa73bfe9e26447e9cc54ddbe046a6fe99727d994a9685958129d

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
  288a82907ed5d3ac6ca51dd078696417abfb4b331496a62c0e9cf2c6d71e5d67
- checks/focused-receipt.json
  56e26f1a9b9f3f7bf0d9c20f83e3adc2ce948eb4aab61802b93254068de21260
- checks/focused-stderr.txt
  e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- checks/focused-stdout.txt
  2d3ba1b8847323fad9175f4b3cb48f8e042b352400f4d31faec5c28967168ce2
- checks/red-journal.jsonl
  a09f3a2dd17dac88f0835305803255271f0ab6cb3ce2b301c7b6adb7336743e8
- checks/red-receipt.json
  533283fe82a0d7727de5846d507318d8d286ef02a293f770e678cd7192e41cb1
- checks/red-stderr.txt
  e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- checks/red-stdout.txt
  4a2a98fa81e62c029baec7f4f1785597680114805163b5ca2be34be2815717cf
