# Portable blueprint artifact adopted

2026-09-05. The controller's exact publication, commit and push authorization
was executed. This is a new disposition; earlier issued records remain unchanged.

- Decision: ADR-0491, Source-seal the portable blueprint artifact.
- Decision commit: 53773cb9e7489d8cfa32b4e0ceadea37c5980023.
- Sole parent: c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98.
- Tree: f3acfba65b32e0890bb86f0af9c087f55e75e50d.
- Reviewed integration candidate: 12df7106b2fca3b25ed4f57115ba9a31e70b6815.
- Manifest: c09f4bcc313e987764597f49ef703e8794e76e7be725dc52a642850803a5bb1c.
- Initial handoff publication: 9c87d0fa995f6a0401ea4b1efef7ae612cc0c9b3,
  459 files, byte-verified against their staged originals.

The 14-path decision tree equals the reviewed integration tree exactly. Its
12 source/registration/CI paths preserve the accepted combined codec r002 and
fixture r002 bytes. Only ADR-0491 and generated STATUS accompany that payload.
Primary master and remote master were confirmed at the decision commit.
Primary tracked working tree and index remain clean; unrelated untracked work
was preserved. No force push or global Git configuration change occurred.

Six immutable candidate archive refs were published to Pontius and verified:
archive/v0a-blueprint-artifact-impl/r001 and r002;
archive/windows-handle-fixture/r001 and r002;
archive/v0a-blueprint-artifact-seal/r001 and r002.
Local review refs and all evidence remain retained; no cleanup was performed.
Packets and coordination records were published to private Pontius-handoffs.
No experiment result, journal, lifecycle directory or working clone was moved.

Fresh authorized precommit checks passed on CPython 3.11.15 first, then3.14.6:
the unchanged status --check and full 12-test status suite on each slot.
After commit/push, the same metadata population passed against fresh snapshots
of actual commit 53773cb: 12 tests in 1.198s on3.11 and 1.204s on3.14, no skips,
failures or errors, all preflights and command exits zero. All 14 files in
each of the four postcommit snapshots matched the frozen packet after execution.
Runs used -B -P, snapshot-root cwd/src, scrubbed child environments, exact
interpreter/module preflights and absolute Git. Raw receipts are
run-records/postcommit-{status,tests}-{311,314}.json under the local task root.

An initial native fetch into the sandbox-owned clone refused Git ownership
before any payload executed. The verified clone was then named in a command-local
safe.directory setting; no global trust or source change was made. This was an
environment setup refusal, not a failing candidate test or a hidden test retry.

The earlier 38-command source acceptance and independent code/metadata reviews
retain their exact scope and standing. These final metadata checks do not assert
a new broad-suite or hosted-CI pass. The source seal is now active, but it confers
no operating, research, rehearsal, policy-search or parked-lane authority.
Workflow-rule adjustments remain separate. No strategic-improvement result is
claimed. The next bounded source task remains to be selected separately.
