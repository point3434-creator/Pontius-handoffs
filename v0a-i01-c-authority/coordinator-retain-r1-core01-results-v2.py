"""Retain verified Gate A results and append navigation; no payload execution."""
import hashlib
import json
from pathlib import Path
import subprocess

P = Path(r'D:\Pontius')
H = Path(r'D:\Pontius-handoffs')
T = H / 'v0a-i01-c-authority'
C = T / 'tests-checks'
GIT = r'C:\Program Files\Git\cmd\git.exe'
HEAD = '43dd0551efbc462263c9839ed19593c53e28eed6'
SOURCE = 'c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f'
h = lambda raw: hashlib.sha256(raw).hexdigest()
def git(*args):
    return subprocess.run([GIT, '-c', 'core.fsmonitor=false', '-C', str(H), *args],
                          check=True, capture_output=True, timeout=60,
                          creationflags=subprocess.CREATE_NO_WINDOW).stdout
def create(path, raw):
    with path.open('xb') as stream:
        stream.write(raw)
def pinned(path, pin):
    raw = path.read_bytes()
    assert h(raw) == pin, str(path)
    return raw
assert git('rev-parse', 'HEAD').decode().strip() == HEAD
assert not git('diff', '--cached', '--name-only', '-z')
pins = {}
receipts = {}
verified = {}
known = {
    '311': ('9a59c48f5bc83452c30588237aa1ca93ce024885a7c8b3b451ec581622f2bd1f',
            '2011a4151ed3db5ea8fef6463b6f9e1b024fbe5885414e9120003d7e8112c930'),
    '314': ('543a15a932aaddd6caeb2fed870bd95dfbaf84352e1e1c2e0c17b16acc8ee82a',
            '618755f700fb59049d1ba8794e7512b117e72f05bb4957954b7ae7e53ebb96cc'),
}
for slot, (rp, vp) in known.items():
    rpath = C / f'rewrite-r1-gate-a-r1-core01-{slot}-receipt.json'
    vpath = T / f'coordinator-rewrite-r1-r1-core01-{slot}-verification-v1.json'
    r = json.loads(pinned(rpath, rp))
    v = json.loads(pinned(vpath, vp))
    assert r['success'] and r['completed'] and r['integrity_ok'] and r['semantic_ok'] and r['accounting_ok']
    assert r['exit'] == 0 and r['generator_sha256'] == SOURCE
    assert v['completed'] and v['integrity_ok'] and v['accounting_ok'] and not v['semantic_failures']
    assert v['source_sha256'] == SOURCE and v['receipt_sha256'] == rp
    assert r['summary']['case_count'] == 6 and r['summary']['projections'] == 8
    expected_files = 1770 if slot == '311' else 1775  # Dev adds five pinned floor evidence files.
    assert r['before'] == r['after'] and len(r['before']) == expected_files
    assert v['snapshot_files_rehashed'] == expected_files
    assert r['input_hashes_before'] == r['input_hashes_after']
    pins[str(rpath.relative_to(T)).replace('\\', '/')] = rp
    pins[vpath.name] = vp
    for record in r['outputs'].values():
        path = Path(record['path'])
        assert path.parent == C
        pinned(path, record['sha256'])
        pins['tests-checks/' + path.name] = record['sha256']
    receipts[slot], verified[slot] = r, v
assert verified['311']['cases'] == verified['314']['cases']
rows = verified['311']['cases']
assert all(row['passed'] and row['budget_epochs'] == 4 for row in rows)
assert max(row['maximum_epoch_work'] for row in rows) == 6692
nav = {}
for name, backup in [('CURRENT.md', 'coordinator-navigation-v19-before-v20.md'),
                     ('rewrite-r1-progress.md', 'coordinator-rewrite-r1-progress-v4-before-v5.md')]:
    raw = (T / name).read_bytes()
    assert git('cat-file', 'blob', HEAD + ':v0a-i01-c-authority/' + name) == raw
    assert not (T / backup).exists()
    nav[name] = (raw, backup)
outname = 'rewrite-r1-gate-a-core01-results-v1.md'
assert not (T / outname).exists()
table = '\n'.join(f"| {r['id']} | {'clean' if not r['blockers'] else 'explicit refusal'} | {r['maximum_epoch_work']} |" for r in rows)
document = f'''# R1 Gate A core01 results

The fixed first checkpoint passes on actual CPython3.11.15 and3.14.6 using
the same frozen source. This clears R1 Gate A only. A/B/C integration, full
original coverage, depth/generator/branch cost checks and final cold reviews
remain incomplete. No main commit or broader payload is authorized here.

## Identity and executed checks

Source {SOURCE}, H b1d15de062ac45c351f0254b358ee1e5fc35bdee,
manifest beb50fab0fe159249de1397529b78a71e2b176b8e3643ea64ccb37dbf1a1c15a.
Closure reviews and the dispatch were retained at H {HEAD},
manifest36e2dde4401f5f2aa9d8da3b7f5d386b251dda52417a48fd283327559aa9db9b.

Each slot ran six unchanged public analyses and eight unchanged independent
Model projections. Each exited0, completed every case and met all expected
classifications. Both clean controls retained their exact argv. Four original
budget stages were observed per case; all counters reconcile on both slots.
The outcomes and work counts are identical across slots.

| Fixed case | Observed result, both slots | Largest epoch work |
| --- | --- | ---: |
{table}

The class-adoption unsafe case now refuses its reached protected class write;
the safe case remains clean with exact argv [-m,outer]. These were the original
r010 baseline's two failed expectations. Shared-list dormant stays clean with
[-m,fixed]; consumed reaches the protected-write refusal. Both hidden-cell
cases refuse unproved truth at line17, before their branch/join. Their expected
refusals pass, but do not demonstrate joined-cell execution.

The maximum6692 is below the unchanged production cap262144. It is not a
physical runtime comparison, a cost-scaling result or a15-second hand result.
The original baseline's smaller counters are not a valid speed comparison to
a changed analysis and accounting implementation. Gate B's196608 continuation
criterion is a separate unexecuted experiment, not a retroactive Gate A gate.

## Custody and independent verification

- Floor receipt: tests-checks/rewrite-r1-gate-a-r1-core01-311-receipt.json,
  SHA {known['311'][0]}.
- Development receipt: tests-checks/rewrite-r1-gate-a-r1-core01-314-receipt.json,
  SHA {known['314'][0]}.
- Root floor verification SHA {known['311'][1]}.
- Root development verification SHA {known['314'][1]}.

The reviewed controller ran under actual3.11.15 -I -S -B -P and gave each child
a separate fresh D-local r010 clone/detach with only the pinned generator and
harness overlay. Children used actual configured interpreters, -B -P, snapshot
cwd, scrubbed environment, snapshot/src PYTHONPATH and hash seed0. Each emitted
identity before candidate import. The development leg was unlocked only by the
successful floor receipt with matching source/controller/Model pins.

Root independently rehashed1770 floor and1775 development snapshot files (the
latter includes five pinned floor evidence files), all original watched
inputs and every raw output; replayed the six source-bound result records,
eight projections, budget sums and exit/summary agreement; and verified the
snapshot Git base. The reports retain exact commands, environments, snapshots,
output hashes and all counters. No source, cap, expectation or original test
changed between runs. No broad or guarded/GPU suite was run.

The first result-summary writer stopped before any artifact/navigation write
because it incorrectly expected1770 files in the development snapshot too.
The independent receipt verifiers had already rehashed the actual1770/1775
files successfully. The retained v2 summary writer corrects this reporting
assumption; no receipt, source, expected result or payload was changed/rerun.

## Next boundary

R2 remains prospective. The old Gate B four-way cost sources have an open-input
comparison-premise defect, recorded without changing their original bytes or
labels. The separately frozen identity-partition proposal repairs that premise
through a source-level language guarantee. It still needs a concrete reviewed
support/measurement plan, new pinned source/Model records, preservation of the
six Gate A and two original depth cases, and a new frozen controller before use.
No blanket scalar assumption, old-engine fallback or cap increase is allowed.

The implementation remains2198 added-plus-deleted lines relative to r010,
within the first-attempt2500 limit. The named finalizer and exact-candidate
main integration authorization remain later gates. This file records a bounded
engineering result, not a new accepted research decision or release acceptance.
'''
create(T / outname, document.encode('utf-8'))
pins[outname] = h((T / outname).read_bytes())
addition = '''

## R1 Gate A completed on both interpreters

The corrected canonical source is frozen at H b1d15de062ac45c351f0254b358ee1e5fc35bdee,
manifest beb50fab0fe159249de1397529b78a71e2b176b8e3643ea64ccb37dbf1a1c15a,
source c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f.
Its two engineering source reviews closed the bounded corrections. Root then
ran the unchanged six-case/eight-Model Gate A on actual3.11.15 and3.14.6; both
passed with independent receipt/snapshot/accounting verification. The two
original class-adoption failures are corrected. See [the result record](rewrite-r1-gate-a-core01-results-v1.md).

The largest epoch is6692 under the unchanged262144 cap. Both hidden cases
refuse unproved truth before a join: no joined-cell or branch-scaling claim.
R2 planning is next; the original Gate B remains held for its recorded missing
comparison premise and a separately frozen correction. No broad suite, original
test migration, main integration, final cold acceptance or live-hand result yet.
Source remains held while the next plan is reviewed. Earlier entries describe
their historical checkpoints and are not relabeled by this addendum.
'''
for name, (raw, backup) in nav.items():
    create(T / backup, raw)
    (T / name).write_bytes(raw + addition.encode('utf-8'))
    pins[backup] = h(raw)
    pins[name] = h((T / name).read_bytes())
failed_writer = P / 'codex-retain-r1-core01-results-v1.py'
failed_raw = pinned(failed_writer, 'abea334cc7bfa7d19597e01f60f48e7b552374260be0e298d9f3f483c2cb652f')
failed_name = 'coordinator-retain-r1-core01-results-v1.py'
create(T / failed_name, failed_raw)
pins[failed_name] = h(failed_raw)
scriptname = 'coordinator-retain-r1-core01-results-v2.py'
create(T / scriptname, Path(__file__).read_bytes())
pins[scriptname] = h((T / scriptname).read_bytes())
ready = T / 'rewrite-r1-gate-a-core01-ready-v1-publication.json'
pins[ready.name] = h(ready.read_bytes())
release = {'release_id': 'rewrite-r1-gate-a-core01-results-v1', 'expected_head': HEAD,
           'title': 'Retain dual-interpreter R1 Gate A results',
           'kind': 'Verified bounded engineering results and append-only navigation', 'pins': pins}
releasepath = P / 'codex-r1-gate-a-core01-results-release-v1.json'
create(releasepath, (json.dumps(release, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'release': str(releasepath), 'pins': len(pins),
                  'results_sha256': pins[outname], 'cases_per_slot': 6, 'models_per_slot': 8,
                  'largest_epoch': 6692}))
