# Freeze r009 only after both exact-source focused legs pass.
from pathlib import Path
import hashlib,json,subprocess,sys
R=Path(r'D:\Pontius-handoffs\v0a-i01-ab');W=Path(r'D:\Pontius-worktrees\codex-v0a-i01-abc');M=Path(r'D:\Pontius');G=r'C:\Program Files\Git\cmd\git.exe'
sha=lambda b:hashlib.sha256(b).hexdigest()
def need(condition,why):
 if not condition:raise RuntimeError(why)
def write(path,data):
 if isinstance(data,str):data=data.encode('utf-8')
 with path.open('xb') as stream:stream.write(data)
def js(value):return json.dumps(value,indent=2)+'\n'
def git(*args):return subprocess.check_output([G,'--no-optional-locks','-C',str(W),*args])
need(sys.version_info[:3]==(3,11,15) and sys.flags.isolated and not sys.flags.optimize,'control runtime')
meta=R/'abc-provenance-v3-focused02-snapshot-v2.json';msha='ae61377fb9a1555cf10e40b0b0e14bcec9e9ba83ca1123242f3f14247e42a02b'
need(sha(meta.read_bytes())==msha,'metadata digest');setup=json.loads(meta.read_text());hashes=setup['source_sha256']
need(all(sha((W/p).read_bytes())==h for p,h in hashes.items()),'work source drift')
receipts=[];sums={}
for slot in ('311','314'):
 sp=R/('abc-provenance-v3-focused02-'+slot+'-summary.json');summary=json.loads(sp.read_text())
 need(summary['source_sha256']==hashes and summary['metadata_sha256']==msha,'summary source')
 need(len(summary['results'])==9 and all(row['exit']==0 for row in summary['results']),'focused leg not green')
 need(sum(row['tests'] or 0 for row in summary['results'])==354,'test count differs')
 need(sum('skipped=1' in row['summary'] for row in summary['results'])==1,'skip count differs')
 sums[slot]={'path':str(sp),'sha256':sha(sp.read_bytes()),'tests':354,'skips':1}
 for row in summary['results']:
  rp=Path(row['receipt']);raw=rp.read_bytes();r=json.loads(raw)
  need(sha(raw)==row['receipt_sha256'],'receipt SHA')
  need(r['exit']==0 and r['before_sha256']==r['after_sha256']==hashes,'receipt source')
  need(sha(Path(r['log']).read_bytes())==r['sha256'],'log drift')
  receipts.append({'path':str(rp),'sha256':sha(raw),'log':r['log'],'log_sha256':r['sha256']})
 for name in ('owner','effective-input'):
  rp=R/('abc-provenance-v3-final02-'+name+'-'+slot+'-receipt.json');raw=rp.read_bytes();r=json.loads(raw)
  need(r['exit']==0 and r['before_sha256']==r['after_sha256']==hashes and r['metadata_sha256']==msha,'independent source')
  lp=rp.with_name(rp.name.replace('-receipt.json','.txt'));need(sha(lp.read_bytes())==r['log_sha256'],'independent log')
  receipts.append({'path':str(rp),'sha256':sha(raw),'log':str(lp),'log_sha256':r['log_sha256']})
need(json.loads((R/'abc-provenance-v3-census-stability03.json').read_text())['all_asserted_census_values_stable'],'unstable census')
base='d1ed3cbda6107d61ea8e77133871720af04970cd';prior='00db06624ab25f10cd181badccf92c87a78f17ee'
subprocess.run([sys.executable,'-I','-S','-B','-P',str(R/'freeze-scoped-round.py'),str(W),base,'r009',*hashes],check=True)
P=R/'r009';candidate=json.loads((P/'candidate.json').read_text())
rows={line.split('  ',1)[1]:line.split('  ',1)[0] for line in (P/'manifest.sha256').read_text().splitlines()}
need(rows==hashes,'frozen blob/source mismatch')
delta=git('diff','--no-renames','--name-only',prior,candidate['commit']).decode().splitlines()
allowed={'tools/generate_test_inventory.py','tests/test_inventory_and_profiles.py','tests/test-inventory.json','tests/test-profiles.toml'}
need(set(delta)<=allowed,'FIX scope expansion')
write(P/'checks/focused-evidence-binding.json',js({'candidate':candidate['commit'],'manifest':candidate['manifest_sha256'],'all_17_blob_sha256':hashes,'metadata_sha256':msha,'summaries':sums,'receipts':receipts,'frozen_blob_bytes_equal_executed_source':True,'fix_delta_from':prior,'fix_changed_paths':delta,'fix_allowed_paths':sorted(allowed)}))
I=P/'inputs';I.mkdir();pins={}
expected={'CLAUDE.md':'af06aad6ec36b91a4e942d7cfc1d3560555ae60e50b023270a0807f247b32b76','docs/workflow.md':'d9de38ede87fb619b3045a60ee7fab137ae23ba3b580c0a6d6b3ca14e567a170'}
for origin,oldsha in expected.items():
 raw=(M/origin).read_bytes();need(sha(raw)==oldsha,'controller document changed')
 raw=raw.replace(b'\r\n',b'\n');dest=I/Path(origin).name;write(dest,raw)
 pins[str(dest.relative_to(P))]={'sha256':sha(raw),'origin':origin,'origin_raw_sha256':oldsha}
for source,dest in [('abc-r009-requirements-draft.md','acceptance.md'),('abc-r009-coverage-draft.md','coverage.md'),('abc-r009-protocol-interpretation.md','protocol-interpretation.md')]:
 data=(R/source).read_bytes().replace(b'\r\n',b'\n')
 if dest=='coverage.md':
  data+=b'\nFrozen evidence inputs (deferred until independent inventory):\n'
  for evidence in [P/'checks/focused-evidence-binding.json',R/'slice-c-provenance-v3-census-311-03.json',R/'abc-provenance-v3-census-stability03.json']:
   relative=str(evidence.relative_to(P)) if evidence.is_relative_to(P) else '../'+evidence.name
   data+=('- '+relative+' SHA256 '+sha(evidence.read_bytes())+'\n').encode()
 write(P/dest,data)
write(P/'checks/protocol-input-pins.json',js(pins))
coverage_sha=sha((P/'coverage.md').read_bytes());acceptance_sha=sha((P/'acceptance.md').read_bytes());protocol_sha=sha((P/'protocol-interpretation.md').read_bytes())
hand=f'''# Cold review: v0a-i01-ab/r009

Round kind FIX; Tier C. Implementer Codex, original C drafter Claude;
checkpoint finalizer Claude. Candidate commit {candidate['commit']};
ref {candidate['ref']}; manifest SHA-256 {candidate['manifest_sha256']}.
Main parent {base}. Review this frozen Git snapshot plus its
blob manifest, never a mutable worktree or chat narrative.

Initial allowed inputs: this handoff, candidate.json, manifest.sha256,
acceptance.md SHA256 {acceptance_sha}, protocol-interpretation.md SHA256
{protocol_sha}, pinned inputs/CLAUDE.md and inputs/workflow.md below,
and frozen source/tests/ADR-0485/ADR-0484/revised brief. Pinned current workflow
copies govern rather than older copies inside the source candidate.
r007 source ddea6efbeb55cb8b71da1ebd5a359a0c2c901cf1 is the ten-path A/B
preservation reference. Prior integration source {prior} is the
FIX comparison only. Read code/blobs, not prior reviews, dispositions,
self-reports, status, checks, plans or implementation discussions.

The full17-path manifest is relative to main. Actual FIX delta:
{', '.join(delta)}.
No new A/B or other C behavior enters this round. Independently reconstruct
the whole-row-sorted Git-blob manifest and applicable invariant/path inventory
BEFORE opening deferred coverage.md SHA256 {coverage_sha}.
Save and hash that inventory first. Never read peer checks/reports.
Implementation self-reports and coordination notes are excluded. Raw evidence
links in coverage may be assessed after inventory.

Use fresh D-local disposable candidate clones and the isolated snapshot policy:
actual3.11.15 FIRST then3.14.6; assert fullversion/executable before Pontius
imports, -B -P, snapshot-root cwd and src PYTHONPATH, scrubbed environment,
D-local TEMP/TMP and absolute validated PONTIUS_GIT. Run focused affected tests
and independent adversarial controls only. No full CI wall before two CLEAN
verdicts, guarded broad/GPU/install/capability/source-seal/rehearsal execution.
Sensitive fixture bodies are inspected, never executed as a binding oracle.
Do not repair frozen source; a changed byte requires a new candidate.

Execution helper ../snapshot-run-abc-v2.py SHA256
62bf07eb88845dfc30c3820aeb8c899ccfbe8111d811192485e2826a5ecfc20c may be
inspected as infrastructure. A fresh clone of this exact commit is permitted.
Independent focused probes may use a separately inspected wrapper satisfying
the same policy. Write only your assigned checks/report.

Reports require defect and design verdicts, with required corrections separate
from advisory engineering guidance. Use each label exactly once:
Reviewer ID: <assigned reviewer_id>
Candidate commit: <full commit above>
Manifest SHA-256: <full manifest above>
Defect verdict: <actual verdict>
Design verdict: <actual verdict>
Request an exclusive task-ledger slot after the final report/hash. Each issuer
appends their own verdict without reading a peer report.

After both fresh CLEAN verdicts, the coordinator may run only the enumerated
current-CI12+v0a5 CPU wall under ADR-0485 on both actual slots. Exact targets:
checks/permitted-cpu-wall.json. This is not a guarded-profile grant. Controller
approval must name this candidate before Claude's main finalization/push.
'''
for path,pin in pins.items():hand+='\nPinned '+path+' SHA256 '+pin['sha256']+'; origin raw SHA256 '+pin['origin_raw_sha256']+'.\n'
write(P/'handoff.md',hand)
wall=[['module:pontius.status_generation','--check'],['tests/test_status_generation.py'],['tests/test_evidence_errors_and_model.py'],['tests/test_evidence_manifests.py'],['tests/test_evidence_manifest_generation.py'],['tests/test_test_orchestration_import_boundary.py'],['tests/test_test_orchestration_configuration.py'],['tests/test_inventory_and_profiles.py'],['tests/test_stabilization_boundaries.py'],['tests/test_retained_evidence_inventory.py'],['tools/generate_test_inventory.py','--check'],['tools/check_stabilization_boundaries.py'],['tests/test_v0a_boundaries.py'],['tests/test_v0a_hand_replay.py'],['tests/test_v0a_trace.py'],['tests/test_v0a_replay.py'],['tests/test_v0a_contract_faults.py']]
write(P/'checks/permitted-cpu-wall.json',js({'authority':'ADR-0485 finite currentCI12+v0a5 after two fresh CLEAN reviews','guarded_profile_authority':False,'targets':wall}))
write(P/'self-report.md',f'''# Combined FIX engineering evidence

Candidate {candidate['commit']}; manifest {candidate['manifest_sha256']}.
All17 frozen Git blobs equal the executed final snapshot bytes. Final focused
3.11.15 first and3.14.6 second each ran354 tests:353 pass, one existing POSIX-only
skip, no failures/errors. Both C CLI checks pass. Independent13 pure controls
pass each slot, with no stale process rows in nine mutation cases. All22
receipts/log hashes bind in checks/focused-evidence-binding.json.

The correction repairs current callable/effective-input authority and reached
namespace effects. Existing AB and remainingC bytes are preserved. Ordinary
inventory generation preserves2641 baseline entries and adds219 current entries;
2860 total. All141 capability rows/spec digest and27 helper edges are unchanged.
The895-blocker census records conservative unsupported-shape costs. Source-bound
attribution and stable rederivation are retained at task root.

Earlier engineering failures remain append-only: v1 semantic/corpus regressions,
v2 omitted-owner RED, and v3 precheck/first-focus census-only failures. No failed
observation is acceptance. Final literal correction and all previous source
edits precede this freeze; no post-freeze fixes are permitted.

No broad wall, guarded/GPU grant, source seal, rehearsal, performance/live wall
claim or ceremonial main commit follows from focused GREEN. Two fresh cold passes
are next, then the permitted wall and exact controller approval for Claude.
''')
print(json.dumps({'packet':str(P),'candidate':candidate,'coverage_sha256':coverage_sha,'acceptance_sha256':acceptance_sha,'fix_delta':delta}))
