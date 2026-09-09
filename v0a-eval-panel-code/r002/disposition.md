# Disposition: v0a-eval-panel-code/r002 — withdrawn by the drafter before review

Date: 2026-09-09. Candidate `e398f83359702dcac4b64f845aa26fddb575662d` was
frozen and pushed, then its focused snapshot receipt failed: under the
scrubbed environment (`env -i`, no `PATH`) the two `OwnershipTests` cases in
`tests/test_eval_panel_tool.py` invoked `git` by bare name in their fixture
`setUp` and raised `FileNotFoundError` (WinError 2). Every other case,
including the three real-launcher cases, passed; the harness recorded
`22 unittest cases exercised`, status failed, in the snapshot only.

This is a test-fixture defect, not a product defect, but a candidate must pass
its own focused receipts and a byte change is a new round. The fixture now
resolves Git as `execution.git()` does (`PONTIUS_GIT`, else `shutil.which`).
The correction is frozen as r003, and the scrubbed-environment run precedes
that freeze. No review was requested or performed on r002; the receipt file in
`checks/` is retained as the record of the failure.
