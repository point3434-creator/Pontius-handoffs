# Tier A metadata review: v0a-driver-seal/r001

Issued 2026-09-04 by independent Codex metadata reviewer.

Verdict: CLEAN. Specification: PASS. Engineering quality: PASS. Design: SOUND.
Findings: zero Critical, Important or Minor. No required correction remains.

## Binding and scope

- Candidate: d45de2bb4522851723667f65f4450c7155833d9a.
- Manifest: b04f8e29d8e4522aefb5ecc8878e6f40f074b91b0bd58208dcc286f48e820e1d.
- Base: af90155ebd970d0be6fe26969b121bd213a7f1f2.
- Tree: 3f1440fcec994239ed7598f391a9a325350dd4ab.
- Ref: refs/heads/review/v0a-driver-seal/r001.
- Reviewed source: bdd96aa24286ba1ebcc11bfdbe7d3480fa3f4ad2.
- Source manifest: b085c3cba799a6563b5a9b9ba8a6b274b1f7d013079ea32cae769118c69d0c9f.

This independent, bounded NEW-SURFACE pass reviews ADR-0488 and generated STATUS,
authenticates the cited source packet, and verifies preservation of its three
reviewed files. Inputs were the handoff and identity files, frozen CLAUDE.md,
workflow Tier A/checklist, ADR-0487/0488, STATUS, the existing status tests and
generator API, and the explicitly permitted issued source reviews and receipts.
Those source reviews are authenticated records, not substitutes for this metadata
review. No implementer transcript or other metadata review was consulted.

## Evidence and assessment

Independent diff-tree with rename detection disabled, cat-file blob reads and
whole-row byte sorting reproduce both manifest files and their SHA-256 values.
The candidate has exactly four additions and one modification (STATUS.md).
Exactly three additions are byte-identical to the reviewed source candidate:

| Path | SHA-256 |
| --- | --- |
| docs/architecture/v0a-rehearsal-driver-r001.md | 2397045c2ea71070a3d65df908da84618de6c7f5550b01f4da811cdc044c6e57 |
| tools/v0a_rehearsal_driver.py | 4c91cad6b0e3ce296de656f4193b346967feca9bb769941ecb24c2903c9f16f3 |
| tests/test_v0a_rehearsal_driver.py | 89dd22ba2700b347b4745c60d099415e17b960988506eba5ab7f70e5b14fed57 |

The remaining two paths are ADR-0488 and STATUS.md, with frozen SHA-256 values
f13f5dffc8c967cc8af972f1fb61488a3c61659e5e2ba488631177260e9e5421 and
99570cc2a10952ef5c095a0f2c7151124ae283dec6608a7c7ccfb434117155c6 respectively.
Parent and tree identities match candidate.json. Checkout bytes equal all five
blobs, with LF-only, no BOM and no trailing whitespace. No unrelated tree change.

ADR-0488 accurately records the source commit, tree, manifest and three blob pins.
Recomputed hashes authenticate Review A as
5974af6da5cb1dc8fc910fbb1211a77ebce29495ee9ae9a2063ea5f1fd2b178d and Review B as
3d4b2ba8e5507446d618515e2ea5216a844a0851a4a9ad1cb27d7eba478e601d.
Both issued records state CLEAN / Spec PASS / Quality PASS / SOUND, zero findings,
independent cold inputs and 3.11-first then 3.14 verification. Their recorded
harness and environment failures are retained and accurately qualified by the ADR.

Post-review results.json hashes reproduce
d3e1cc60971e89cf49a14df815dfadbe608a52d2afc042513e190f82395451c0 (3.11) and
94291a198dc0a815490591331c3e4fe590827c73a557eb8fd9daa587b2d33e7d (3.14).
Each has five zero-exit commands; corresponding logs show 12 driver, 45 hand replay,
53 trace, 62 replay and 22 contract-fault tests, totaling 194, all OK without skips.
These are authenticated prior driver-regression results, not new metadata runs.

The authority boundary is explicit and consistent with ADR-0487: this is a proposed
driver-only adoption, inactive until controller approval and the separately
authorized ceremonial commit. Conditional accepted-status metadata does not assert
that a working document, review ref or STATUS activates the seal. The active-next
and blocker text preserve approval before integration and separate authorization
before execution. Library identity, source payload identity and eventual driver
decision identity remain distinct. No rehearsal, operating budget, population,
one-shot authority or scientific result is claimed; inherited parked lanes and the
Windows fixture caveat remain open. The driver behavior summary agrees with the
permitted issued source reviews; source implementation was not re-audited.

SOUND: this small adoption record binds existing reviewed bytes and bounded
receipts, states its conditional effect, and leaves subsequent execution authority
to its separate decision. No new mechanism or assurance layer is introduced.

## Fresh metadata checks

Exclusive scratch: D:/Pontius/tmp/v0a-driver-seal-review.
Fresh snapshot: scratch/snapshot. Clone and checkout both exited zero:

```text
C:/Program Files/Git/cmd/git.exe -c core.autocrlf=false clone --no-hardlinks --no-checkout D:/Pontius D:/Pontius/tmp/v0a-driver-seal-review/snapshot
C:/Program Files/Git/cmd/git.exe -C D:/Pontius/tmp/v0a-driver-seal-review/snapshot -c core.autocrlf=false checkout --detach d45de2bb4522851723667f65f4450c7155833d9a
```

Normal-user escalation was used initially for clone and both interpreter runs.
Every Python command used -B -P, snapshot cwd, snapshot/src PYTHONPATH,
PYTHONNOUSERSITE=1, scrubbed PYTHON/GIT_/PONTIUS_ variables, absolute PONTIUS_GIT,
and exclusive D-local TEMP/TMP/TMPDIR. No dependencies or trust settings changed.
The small retained scratch/verify_metadata.py reconstructs identity, authenticates
the four cited receipts, and compares render_status(snapshot).encode('utf-8')
directly with frozen STATUS bytes. It also proves the generator import origin.

| Interpreter, executed in this order | Commands and result |
| --- | --- |
| D:/Pontius-tools/py311/Scripts/python.exe, CPython 3.11.15 | -B -P scratch/verify_metadata.py: exit 0; -B -P tests/test_status_generation.py -v: exit 0, 12 tests OK, 0.210s |
| D:/Pontius/.venv/Scripts/python.exe, CPython 3.14.6 | -B -P scratch/verify_metadata.py: exit 0; -B -P tests/test_status_generation.py -v: exit 0, 12 tests OK, 0.216s |

Both fresh generations match STATUS byte-for-byte. Existing tests cover freshness,
ADR-chain integrity, controller metadata validation, retained revocations and
front-door visibility/refusal. Final snapshot Git status is clean. No reviewer
command failed or required a retry. The packet's earlier proposed-status generation
failure remains recorded as a generator refusal, not a product pass.

This review neither reruns the driver/core audit nor invokes any host or rehearsal.
No source edit, fix, suite expansion, dependency install, commit, push, delegation,
owner, lifecycle or retained evidence operation occurred. Controller approval and
the separately authorized integration commit remain outstanding.
