import hashlib,json,pathlib,re,subprocess,sys
assert sys.version_info[:3]==(3,11,15),sys.version
checks=pathlib.Path(r'D:\Pontius-handoffs\v0a-i01-ab\r008\checks');packet=checks.parent
info=json.loads((checks/'codex-a-02-identity.json').read_text(encoding='utf-8'));root=pathlib.Path(info['snapshot']);env=info['scrubbed_environment'];env['PYTHONPATH']=str(root/'src')
results=[]
for version in ('3.11.15','3.14.6'):
 count=0
 for label in ('boundaries','inventory','legacy-boundaries','hand','trace','replay','faults','generator-check','boundary-cli'):
  path=checks/f'codex-a-06-{version}-{label}.log';text=path.read_text(encoding='utf-8');footer=json.loads(text.splitlines()[-1]);assert footer['exit']==0,(version,label,footer)
  match=re.search(r'^Ran (\d+) tests',text,re.M)
  if match:count+=int(match[1])
  results.append(dict(version=version,label=label,test_count=int(match[1]) if match else None,exit=0,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),seconds=footer['elapsed_seconds']))
 assert count==340,count
 for label in ('11-binding-confirmation','16-integration-probes-v2'):
  path=checks/f'codex-a-{label}-{version}.log';lines=path.read_text(encoding='utf-8').splitlines();assert json.loads(lines[-1])['exit']==0
  data=[]
  for line in lines:
   try:data.append(json.loads(line))
   except json.JSONDecodeError:pass
  if label=='11-binding-confirmation':
   confirmations=[x for x in data if 'confirmed_case' in x]
   assert len(confirmations)==12 and sum(bool(x['unexpected_approval']) for x in confirmations)==10
  else:assert len([x for x in data if 'boundary_case' in x])==9
  results.append(dict(version=version,label=label,exit=0,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
for row in (packet/'manifest.sha256').read_text(encoding='utf-8').splitlines():
 digest,path=row.split('  ',1);assert hashlib.sha256((root/path).read_bytes()).hexdigest()==digest,path
status=subprocess.run([info['git'],'-C',str(root),'status','--porcelain','--untracked-files=all'],cwd=root,env=env,capture_output=True,check=True);assert status.stdout==b'',status.stdout
assert hashlib.sha256((packet/'manifest.sha256').read_bytes()).hexdigest()==info['manifest_sha256']
assert hashlib.sha256((packet/'coverage.md').read_bytes()).hexdigest()=='737dcecf689cc962a5e382509fa14689c04420c79c53ac574998a741c13376a8'
summary={'candidate':info['candidate'],'manifest_sha256':info['manifest_sha256'],'snapshot_final_clean':True,'all17_physical_source_hashes_match_manifest':True,'initial_inventory_sha256':hashlib.sha256((checks/'codex-a-03-initial-inventory.md').read_bytes()).hexdigest(),'checks':results,'binding_confirmations_per_slot':{'invalid_approved':10,'lawful_controls':2},'reviewer_harness_correction':'First integration-probe receipt failed only at a comparison decoded with the CPython 3.11 Windows default codepage. The append-only v2 uses explicit UTF-8; exact raw CI insertion comparison and all integration controls pass.'}
with (checks/'codex-a-17-final-verification.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(summary,f,indent=2);f.write('\n')
print(json.dumps(summary,indent=2))