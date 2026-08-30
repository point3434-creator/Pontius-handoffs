# Final integration base

The final combined candidate starts at current source HEAD d1ed3cbda6107d61ea8e77133871720af04970cd.
Ten A/B source/test files are copied from exact frozen r007 Git blobs; their hashes
are recorded in abc-integration-base.json and must remain identical after reviews.
The seven C paths are layered only after its binding correction is stable, then
ordinary inventory/profile generation and mechanical census refresh run on that
combined corpus. No capabilities or baseline pin change.

This preserves the current committed workflow. The older A/B snapshot ancestry
also differs in docs/workflow.md; that old workflow is deliberately not replayed.
The primary checkout's separate uncommitted CLAUDE.md/workflow edits remain untouched.
Final candidate manifest covers all17 integration paths relative to current HEAD.
Review names two slices: unchanged A/B preservation against its accepted pair and
new C/code-generation behavior. Both cold passes precede permitted broader gates.
No integration commit is authorized by these preparations; Claude is finalizer and
controller authorization remains candidate-specific. Review refs are retained or
archived under packet retirement rules rather than assumed reachable by byte copying.
