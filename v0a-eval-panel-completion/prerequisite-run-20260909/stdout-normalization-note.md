# Stdout capture normalization note

The four `*-stdout.json` captures were written by Python's `print` on Windows and
contain CRLF. `invocation-log.jsonl` and `rehearsal/receipt.json` record the SHA-256 of
those raw captured bytes. Git normalizes them to LF on commit, so the committed blobs
hash differently. Both digests are listed here; the evidence of record is each run's
`result.json` in the checkout (LF, bound by its journal row), which is unaffected.

| File | raw (CRLF) SHA-256 as recorded | LF-normalized SHA-256 (committed content) |
|---|---|---|
| `invocations/capacity-stdout.json` | `026a1a53ce076e9145313ef317bb5eb09a4d96a9b57ceec3a26579638f329017` | `29f532a900289c3e7b274646a7fc7332ff1a0aa9e6d74c332319668783d89e53` |
| `invocations/preflight-stdout.json` | `bb30ab891d3a8718696b95ae90b4fa142dbaa7a91da3561b7b6990960481db53` | `8a17325eaa07e0f8774dcb7bc2050a3ae233cf47bebfc63a6b59574031fb742f` |
| `rehearsal/capacity-stdout.json` | `fcd4d71eec4dcb689795295c292d9840f606f7626b047c91a3a90fded5a7a451` | `5dee2e8dc7851e2ea72c2ffa68497e6cf3dba1ff2bfe77c67b41a5280d3ad6b0` |
| `rehearsal/preflight-stdout.json` | `9a034c9ea687a327de13a6ae63be9293c3549fbea883c4a2576f9282fdb499e9` | `36b072872a6ea90e11a79887b130fc95606e07b648544bbda3c787f1526e2e1b` |

Recorded 2026-09-09 after handoffs commit cd47175; the captures themselves are unchanged.
