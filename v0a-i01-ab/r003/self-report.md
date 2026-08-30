# r003 self-report

Commit 30df7bce8da51715e6f1d7576892dd689421c516; manifest 21d9686c9918d9d0648fd98edf35219dfb5e0b4dc1dcfe5e4f28171b7d94e513. Typed-refusal correction only. Kernel-derived
decision shape is compared before copying arbitrary caller structure; the derived
owned value then feeds unchanged sealed lookup. Remaining admission guards normalize
RecursionError to existing typed failures. No operational depth limit added.

Actual floor-first final receipts: ../policy-refusal-checks/freeze-check-311-receipt.json
and freeze-check-314-receipt.json,132 pass each. RED23 public-field schedules on r002
raise RecursionError; new expected type passes. All commands/exits/log hashes retained.
Changed2files, diff --check clean. Tested overlays match frozen blobs; real HEAD/index
preserved. No primary/legacy/C edits, broad run, source seal or integration claim.
