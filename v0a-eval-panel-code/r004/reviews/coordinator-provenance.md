# Coordinator provenance note - r004 cold reviews

Date: 2026-09-09. Issuer: Codex coordinator.
Candidate: 0bc19bcaad5c6660468094772216cac2dc27a651
Manifest: 70ca4c76bc8bdefe8ffaab72fa8de5b7d24d49697157436d78a3e1c025a370c3
Review publication: fb7f8de19afb61f8315d0f7786f981499ae6c4a9

The controller's request for two more cold reviews authorized review of the newest
frozen packet, r004. Both agents received only that packet path plus administrative
review/output instructions, without conversation history or sibling findings.

## Utility interpreter deviation

The controller's Python policy is 3.14 only. After the reports were issued, the
coordinator checked the standalone utility interpreter versions with each reviewer.

- Review 01 used Python 3.11.15 for standard-library byte audits and artifact checks:
  C:/Users/point/AppData/Roaming/uv/python/cpython-3.11.15-windows-x86_64-none/python.exe
- Review 02 used Python 3.12.14 for isolated standard-library hashing, JSON/data,
  hygiene and artifact-staging checks:
  C:/Users/point/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe

Both versions were confirmed afterward using Windows executable VersionInfo metadata,
without invoking Python again. This utility execution did not follow the controller's
3.14-only policy. Neither reviewer imported or executed project code, tests or owners.
Their original reports remain unchanged; this note supplies the omitted exact versions.

The coordinator independently reverified with PowerShell/.NET: candidate ref, parent,
tree, all seven raw-blob manifest rows, the exact manifest digest, all 34 BASE dependency
pins, the four supplied receipt hashes, and all delivered review/inventory/ledger hashes.
Publication also checked LF/no BOM/no trailing whitespace/100-column hygiene and remote
commit identity. This verification does not retroactively change the utility versions
used by the cold reviewers or constitute a new cold review.

The supplied candidate execution receipt remains CPython 3.14.6: 27 cases, zero skipped,
exit 0, ResourceWarning treated as error, source_verified true. No new project execution
was performed by the coordinator. Both original NOT CLEAN / STRAINED verdicts and their
concrete frozen-source findings remain published, with this process deviation disclosed.
