# Review B issuer ledger

Issuer: Codex /root/evaluation_review_b. Date: 2026-09-07.
Original create-new record; independent blind review of packet r001.
Candidate 96aad82a482a0f37b13490df1bf03c1c74a860ca.
Base e043f81ecec3ac16128720b42c3312bb41a4ed67.
Tree 17140a92f66c1b10bd11f266b093a7c3076f7711.
Manifest 6f388fbcc7c7bff9d99ba69fcac5287ad9e30e72d20bc1d1e02fe76ee8a06129.

Reads: frozen handoff/candidate/manifest and all six raw packet documents; CLAUDE.md,
workflow/checklist, PROJECT evidence/dissent, architecture boundaries and ROADMAP C10;
accepted ADR-0505/0506/0507; relevant accepted host Source/Job/WireConsumer, session
Admission/report construction, seeded recipe, boundary-registration rules, inventory
registration list, provider codec declarations and existing native/session test contracts.
No other review, transcript or mapping report was read.

Commands: PowerShell Get-Content/rg for read-only source; stdlib-only Python -B -P via
D:/Pontius-tools/py311/Scripts/python.exe for native Git raw-byte SHA-1/SHA-256 analysis.
Absolute Git: C:/Program Files/Git/cmd/git.exe. Replacement objects disabled.
First Git identity attempt failed (exit 128) on sandbox dubious ownership. Repeated with
command-local safe.directory for this exact authoring repository; no Git config was written.
Next audit recomputed candidate/parent/tree/scope/manifest and six pins but exited 1 because
my regex crossed a newline in the three-tool-pin pattern. Corrected newline exclusion,
asserted nine pins, and independently verified all nine in the final audit (exit 0).
These were reviewer command faults, not target defects; no payload was invoked by either.

Raw manifest rows independently reconstructed from frozen Git blobs:
1a0cf5fcddf3f33c392b19849c2af39c8c74c871f5fcfd04006a32e2d6dce8e4  docs/architecture/v0a-evaluation-r001/design.md
2c2c064d464559b5ccc53cea3d073d5a8ad94bb0d32eeb3fe69f13a952575ee8  docs/superpowers/plans/2026-09-07-paired-local-evaluation.md
4254976215f5c4f22c66ddc5077263038f84a53ad27dc9a22cd577fc8baa9bc5  STATUS.md
47ce8747e7cc0c0a46f22fe710a9d6da63856ebb05a4f42ee19314c6cee33cdd  docs/architecture/v0a-evaluation-r001/source-contract.md
632b79d4124bf8426fd2466a7ba64f00ccbbff68489c387766cb270016c2a09a  docs/decisions/ADR-0508-open-the-paired-local-evaluation-source-round.md
6b59aae1c94780eb7ca54c2e2cc0d5a780eb7858247af89cd8912299cd8905c8  docs/architecture/v0a-evaluation-r001/brief.md

Nine B raw Git blob identities verified by hashing blob header plus raw bytes:
9cc2ae8d8e82ccc77648ade4eb79ae9c34c88a9f  tools/check_stabilization_boundaries.py
2ac1413b0f89fa848f1ee5df0814b58dcbfa15b8  tools/generate_test_inventory.py
c28445aa4b77a98cfd706672d955be4570b98a15  tests/test-inventory.json
4469bf813b2e97116667c206784a7bc212f6eef5  tests/test-profiles.toml
e71a24322878361fb2feb44437d9210cff79c89e  tests/test_inventory_and_profiles.py
3d873a2f75ff1b155bf3533583eddf971eb7790a  .github/workflows/ci.yml
2963004e38c6e66f76ae9ce3bd474063eee870fe  tools/v0a_seeded_deals.py
a5e058260fa56e29f06e38074d59dc55f420c5ee  tools/v0a_table_session.py
6ec8a162b053158203663c48e82314b10750f962  tools/v0a_table_host.py

All nine remain equal in candidate. Packet copies of the six proposal blobs are raw-exact.
The four primary source files read through checkout match B after checkout CRLF removal;
identity conclusions above use raw Git blobs, never normalized checkout hashes.
Prior disposition SHA-256: 2f9d99f1aaca32252680a80b80e9b7a0ef1ad6d51b9482af0b42d849b1382c5f.
No status tests were run by this reviewer; they remain the coordinator's later gates.
Verdicts: specification CLEAN, engineering CLEAN, overall CLEAN, design SOUND; C/I/M 0/0/0.
