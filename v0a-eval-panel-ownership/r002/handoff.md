# Cold review: v0a-eval-panel-ownership/r002

Candidate: d8d291cc1f813ce798f2d3a990b2a8bf2297e124
Manifest: 86a583d27d71c251f89f507b4761318433218f0450be649fb768c83b3d8c6926
Base: 72954e1331c9b191d927c1c4b82f277bcd322a4c
Tree: 2b542a78b5a96963a154ed1da6408834eea3e3e8
Ref: refs/heads/review/v0a-eval-panel-ownership/r002
Tier C. FIX. Codex drafts/finalizes; Claude reviews independently.

Scope: cleanup lifetime, observations, publication and their combined sample consumers.
Only tools/v0a_eval_panel.py and tests/test_eval_panel_tool.py differ from BASE.
This is a separate contract candidate required by r004's second-residual disposition.
Review the whole affected contract and its consumers, not only the latest example.
The bridge and all sealed source remain unchanged. Design steps 4-7 remain outside scope.
The governing brief/design are at f647a7989394f084875a040b20c41891168163ed under
docs/architecture/v0a-eval-panel-impl-r001/ and its referenced parent design.

Record your independent invariant/related-path inventory before opening coverage.md,
checks/, inputs/*disposition.md or inputs/repair-plan.md. These are deferred FIX
inputs, not a substitute for independent discovery. Do not read implementer transcripts,
prior-round review files, or sibling reviewer outputs.
Deferred coverage SHA-256: 5d0c4c730b7fd65f0276d63d78a845d8002442a037c363f415542db5dde9e4f5

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
This packet may be reviewed from local refs. Public publication requires the controller's
explicit approval; no reviewer may commit, push, run hooks or publish network writes.

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
- inputs/ownership-disposition.md
  61d6f5617c06a0b7f7102197562d0045f6e278e8a670d494feac8bdb1083aa27
- inputs/prior-disposition.md
  f9e3c1a1303ac67494e40e9ed0b5ea2b7cb26d0d665ac11232c10a356aed9ac3
- inputs/repair-plan.md
  463cd0b4eb413a3df8d72b5000eddaa7295a3a16071b359ee9bf15661f2db9f8
- inputs/workflow.md
  c71e3963ff726e06158878bcc10dd7dd761b32597af1c8ed39e21ebf60b58a37
- checks/focused-journal.jsonl
  3548aa8120d138fd52b6b68f38369230048f4d259ff1fb449c296343f20ee445
- checks/focused-receipt.json
  7f5eee55c419fbea0e3184a8c9019db379959744712ee888925e8ec0ac0adc9d
- checks/focused-stderr.txt
  e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- checks/focused-stdout.txt
  101b6a28bc2d42c2e9dea64c2a431b4d2785a4ef530e1b8427f61f31e8461ec2
- checks/lint.json
  87d1c2cadf6d27d2c44f63bbe04dbc8b15c9a9c7c1a46f45f0057ae3ee92be92
- checks/locator-diagnostic-journal.jsonl
  e7f0454b0bdf12ff55a173791964146d97805eaf57629de2ddf09bb315089b27
- checks/locator-diagnostic-receipt.json
  ce865ecb076d220496406660249f529714bbaaa249b460f57733eeb57629e2e3
- checks/locator-diagnostic-stderr.txt
  e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- checks/locator-diagnostic-stdout.txt
  14c6db161d274cd72a1b6f97eaa3b3fa18870cd4c316148451056879bf4bfc96
- checks/red-journal.jsonl
  8a2868a825b433195582e9324e88f0fc8cc5a4581d479ae14192a954a40ef79e
- checks/red-receipt.json
  439258252b506bed8c7e7051244cc52b829ed382bab7d6fffec5d00118fe5c62
- checks/red-stderr.txt
  e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- checks/red-stdout.txt
  400430681d75ae18d20149d7c40b4f31567dd7e17eda568569fcf05efb1da3bd
