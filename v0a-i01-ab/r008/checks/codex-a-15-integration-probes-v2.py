# Revision 2: fix reviewer harness default-codepage decoding; original failure retained.
import hashlib,importlib.util,json,os,pathlib,shutil,subprocess,sys,tempfile
root=pathlib.Path.cwd(); git=os.environ['PONTIUS_GIT'];base='d1ed3cbda6107d61ea8e77133871720af04970cd'
def blob(ref,path): return subprocess.run([git,'-C',str(root),'cat-file','blob',ref+':'+path],capture_output=True,check=True,env=dict(os.environ)).stdout
before=json.loads(blob(base,'tests/test-inventory.json'));after=json.loads((root/'tests/test-inventory.json').read_bytes())
a={x['stable_id']:x for x in before['entries']};b={x['stable_id']:x for x in after['entries']}
assert all(b[k]==v for k,v in a.items())
added=sorted(set(b)-set(a));assert len(added)==205
newpaths=sorted({b[k]['relative_path'] for k in added});assert newpaths==['tests/test_inventory_and_profiles.py','tests/test_v0a_boundaries.py','tests/test_v0a_contract_faults.py','tests/test_v0a_hand_replay.py','tests/test_v0a_replay.py','tests/test_v0a_trace.py']
assert all(b[k]['assignment']['profile_name']=='current' for k in added)
oldci=blob(base,'.github/workflows/ci.yml').decode();newci=(root/'.github/workflows/ci.yml').read_text(encoding="utf-8")
start=newci.index('      # v0a increment one,');end=newci.index('      - name: Ruff report',start)
assert newci[:start]+newci[end:]==oldci
addition=newci[start:end];assert addition.count('if: ${{ !cancelled() }}')==5 and 'continue-on-error' not in addition
for name in ('boundaries','hand_replay','trace','replay','contract_faults'):assert f'tests\\test_v0a_{name}.py' in addition
print(json.dumps({'inventory_old_entries':len(a),'new_entries':len(b),'added_entries':len(added),'all_existing_entries_byte_value_equal':True,'addition_paths':newpaths,'all_additions_current':True,'ci_exact_additive_insertion':True,'ci_new_hard_gates':5}),flush=True)
path=root/'tools/check_stabilization_boundaries.py';spec=importlib.util.spec_from_file_location('codex_a_boundaries',path);c=importlib.util.module_from_spec(spec);sys.modules[spec.name]=c;spec.loader.exec_module(c)
assert pathlib.Path(c.__file__).resolve()==path.resolve()
with tempfile.TemporaryDirectory(prefix='codex-a-boundary-controls-') as folder:
 copy=pathlib.Path(folder)
 for directory in ('src','tools'):shutil.copytree(root/directory,copy/directory)
 baseline=copy/c.BASELINE_RELATIVE_PATH;baseline.parent.mkdir(parents=True);baseline.write_bytes((root/c.BASELINE_RELATIVE_PATH).read_bytes())
 def probe(label,changes,blocked,reason=None):
  originals={}
  try:
   for rel,value in changes.items():
    target=copy/rel;originals[rel]=target.read_bytes() if target.exists() else None;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(value)
   refusal=None
   try:c.check_repository(copy)
   except c.BoundaryError as error:refusal=str(error)
   assert bool(refusal)==blocked,(label,refusal)
   if reason:assert reason in refusal,(label,refusal)
   print(json.dumps({'boundary_case':label,'blocked':bool(refusal),'reason':refusal}),flush=True)
  finally:
   for rel,value in originals.items():
    target=copy/rel
    if value is None:target.unlink()
    else:target.write_bytes(value)
 probe('clean-real-source',{},False)
 probe('visible-state-relative-alias',{'src/pontius/v0a/runtime.py':b'from ..holdem_cards import OneSeatCardState as State\n'},False)
 probe('foreign-river-relative-alias',{'src/pontius/v0a/runtime.py':b'from .. import river as evaluator\n'},True,'forbidden v0a import')
 probe('deferred-complete-attribute',{'src/pontius/v0a/trace.py':b'from .. import holdem_cards as h\ndef deferred():\n    return h.SixSeatHoldemDeal\n'},True,'complete-deal')
 probe('initializer-host-relative',{'src/pontius/v0a/__init__.py':b'from . import replay as host\n'},True,'explicit-deal host')
 probe('unknown-origin',{'src/pontius/v0a/unregistered.py':b'value = 1\n'},True,'unclassified stabilization origin')
 probe('new-scc',{'src/pontius/v0a/model.py':b'from . import clock\n','src/pontius/v0a/clock.py':b'from . import model\n'},True,'new or expanded internal SCC')
 probe('legacy-edge-drift',{'src/pontius/action_clock.py':(copy/'src/pontius/action_clock.py').read_bytes()+b'\nimport pontius.v0a.runtime\n'},True,'legacy outgoing edges changed')
 probe('malformed-source',{'src/pontius/v0a/model.py':b'def malformed(:\n'},True,'cannot be derived')