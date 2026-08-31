# Original reviewer-receipt bytes

The issued codex-a-ledger-append-receipt.json uses CRLF. It is preserved as issued,
not normalized after the review. The handoff repository adds one exact-path
-text attribute for that receipt so both Git storage and later checkouts retain
its original bytes. The default * text=auto eol=lf rule and every manifest remain
unchanged. All other files in this publication are LF-only. This is an artifact
preservation rule, not a relaxation of the source or governance style requirement.
