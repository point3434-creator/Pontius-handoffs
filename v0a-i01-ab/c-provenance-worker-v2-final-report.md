# C provenance integration correction: worker release v2

Released two files from `D:\Pontius-worktrees\codex-v0a-i01-c-provenance` against r008 `00db06624ab25f10cd181badccf92c87a78f17ee`. No further edits pending.
This is an engineering handoff, not a cold review or full-corpus acceptance claim.

## Changes and preserved contracts

Callable/class/module/receiver identity is orthogonal metadata: legacy qualified values,
callable summaries, protected returns and exception transfer remain intact. Proof is met
separately at merges; captured defaults merge by parameter without choosing an arbitrary
branch. Ordinary failed lookup retains the existing exception/census path. Exact harmless
local callables retain their non-sensitive disposition; missing source snapshots are not
turned into invented completed calls.

Source-point arguments, defaults and callee capture remain preserved. Parameters in the
production proof path overwrite unrelated seeds; explicit inputs to the legacy resolver
without a helper registry retain its original contract. Source-point nonlocal captures
survive initialization, and declarations alone do not imply namespace mutation.

Known module exports and standard unittest skip/skipIf/skipUnless class decoration regain
proof through their bindings. Deferred unrelated bodies and immutable code reads do not
poison a module. Actual source-ordered member changes invalidate owner/member identity;
imported initialization changes bind to the resolved owner/member. Unknown reachable
initialization effects and unproved owner escapes produce typed refusals. Existing fresh
unrelated namespaces and protected external-module mutation semantics remain unchanged.

All 178 pre-existing class methods in the test file are AST-identical to r008;
none was removed or weakened. Only the new annotation/deletion controls were clarified:
proved non-completion may have zero helper rows without an invented unresolved blocker.
The opposing caught-NameError tests require exactly the handler's subprocess projection.
The checks execute only pure return projections of new sensitive fixtures, never their
subprocess bodies. Metered binding traversal is iterative and keeps the existing limits.

## Evidence

Existing RED: root's `abc-checks/provenance-inventory-precheck01-311.txt`, 99 tests,
39 failures and 5 errors on released d94a8e8c source. New precision RED before source edits:
`c-provenance-v2-red01-311-receipt.json`, 2 methods /8 failures /0 errors. The imported
initialization control then exposed one required residual in
`c-provenance-v2-red02-311-receipt.json` (2 methods /1 failure /0 errors); its unrelated
member positive stayed clean. The additional local default-replacement control already
refused and is coverage evidence rather than an invented product RED.

Final commands (the append-only runner derives and passes every method name from the AST):

```powershell
& 'D:\Pontius-tools\py311\Scripts\python.exe' -B -P 'D:\Pontius-handoffs\v0a-i01-ab\c-provenance-worker-v2-run-all.py' v2-green01 311
& 'D:\Pontius-tools\py311\Scripts\python.exe' -B -P 'D:\Pontius-handoffs\v0a-i01-ab\c-provenance-worker-v2-run-all.py' v2-green01 314
```

| Slot | Result | Duration | Receipt |
| --- | --- | --- | --- |
| actual3.11.15, first | 36/36;0 failures/errors/skips;exit0 | 9.841s | c-provenance-v2-green01-311-receipt.json |
| actual3.14.6 | 36/36;0 failures/errors/skips;exit0 | 18.345s | c-provenance-v2-green01-314-receipt.json |

Both receipts contain identical source overlay hashes, full explicit target names,
interpreter/origin assertions, fresh r008 D-local snapshots, -B/-P, scrubbed environments,
snapshot cwd/src PYTHONPATH, D-local TEMP/TMP and absolute PONTIUS_GIT. Intermediate
v2-probe01 through v2-probe07 receipts are retained, including failures and the initial
misplaced delete hook and recursive-visitor error; final evidence supersedes no file.

## Scope and remaining verification

Git status contains only the two owned paths; diff --check exits0. Source/test bytes are
LF with no BOM. Main, A/B, other C, generated pair, expectations, sealed baseline and
capabilities, Git refs, ledgers and review reports were not changed by this worker.
Root also supplied `abc-provenance-v2-existing-test-preservation.json` independently.

No general Python object heap or dynamic descriptor inference is claimed. Unknown/stacked
decorators, ambiguous callable identity, reflective mutation and owner escapes without a
finite read-only proof remain conservatively refused. Known helpers that forward an owner,
store it, or invoke an unproved owner method can therefore gain explicit blockers. Initial
member mutation attribution is conservative across captured modules for the same resolved
owner; unrelated member spellings and deferred bodies do not invalidate other owners.

Root owns full combined generation, helper-edge/capability-row census preservation and
full affected suites before freeze. No corpus count is refreshed or claimed here, and these
focused runs authorize no guarded profile, GPU/capability execution, approval, source freeze,
commit or publication.

## Released identity

- generator SHA256 `a57f76e38bd8e8494ab16fb878e2887854d3f59844fb1e78bd3d50c54f0b4341`
- test SHA256 `af929697b3f6c8ddad823ff16bef63936f5b924cdf16992d8bc93679368ca961`
- patch SHA256 `f68c183270ba41645f2285b0982f862e405f6be51d5acfb0f0540a597486105f`
- patch: `c-provenance-worker-v2-final-owned.patch`
- machine-readable validation: `c-provenance-worker-v2-final-validation.json`
