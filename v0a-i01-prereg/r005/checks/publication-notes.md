# Coordination publication notes

The evidence candidate's `git diff --check` passes. The coordination repository's
initial staged check reports one Markdown hard break (two trailing spaces) in the
already issued r004 review-02-codex-b.md, line 5. Its attributed review bytes and
hash are preserved under the append-only rule; the coordinator does not rewrite
an issued verdict for formatting. This is not a defect in the frozen source or
manifest. Non-review packet files pass the staged whitespace check.

The private handoff origin and post-commit push hook were installed by the controller's
Claude session and verified locally. Git HTTPS credential-manager access succeeds;
GitHub CLI authentication is not required for this publication. Packet-repository
commits are routine coordination publication under workflow rule 6, separate from
any ceremonial evidence-repository commit or experiment authorization.
