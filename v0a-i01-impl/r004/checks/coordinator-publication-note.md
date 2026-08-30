# Publication verification clarification

The structured cr_aware_remaining_warnings array in
coordinator-publication-verification.json correctly lists THREE retained
extra EOF-blank-line warnings:

- cold-b-probe-run.ps1
- cold-b-red-run.ps1
- coordinator-publication-check.py

Its warning_disposition prose says Two; that count is a coordinator prose error.
Three is correct. This append-only clarification preserves the original receipt.
All three are diagnostic inputs, not frozen candidate production files. Their
issued bytes remain unchanged. Governance whitespace passed; default full-capture
whitespace did not, as recorded, because raw CRLF was intentionally preserved.
Frozen candidate identity, executable observations and byte-level staged-file
verification all passed. No broader whitespace PASS is claimed.
