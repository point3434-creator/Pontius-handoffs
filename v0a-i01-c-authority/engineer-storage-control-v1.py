import hashlib,json,os,pathlib,re,stat,subprocess,sys,uuid
P=pathlib.Path
ROOT=P(r'D:\Pontius-handoffs\v0a-i01-c-authority')
WORKSPACE=P(r'D:\Pontius')
SOURCE=P(r'D:\Pontius-worktrees\codex-v0a-i01-c-authority-v1\tools\generate_test_inventory.py')
SOURCE_SHA='3d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1'
PROTOTYPE=ROOT/'engineer-storage-prototype-v2.py'
PROTOTYPE_SHA='22cc3966435fd4e6e0cecbcbb242275e72d34b36c835b4e960c7c712613822ff'
SLOTS={'311':(P(r'D:\Pontius-tools\py311\Scripts\python.exe'),'3.11.15'),'314':(P(r'D:\Pontius\.venv\Scripts\python.exe'),'3.14.6')}
def req(value,message):
    if not value:raise RuntimeError(message)
def h(raw):return hashlib.sha256(raw).hexdigest()
def validate(path):
    req(path.is_absolute() and '..' not in path.parts,'unsafe path')
    for parent in (path,*path.parents):
        info=parent.lstat()
        req(not(getattr(info,'st_file_attributes',0)&stat.FILE_ATTRIBUTE_REPARSE_POINT),'reparse '+str(parent))
    return path

def create(path,raw):
    with path.open('xb') as stream:stream.write(raw)
def create_json(path,value):create(path,(json.dumps(value,indent=2)+'\n').encode())
def local_file(relative):
    req(type(relative) is str,'file path type')
    path=ROOT/P(relative)
    req(path.is_relative_to(ROOT) and '..' not in path.parts,'outside handoff')
    return validate(path)
def input_file(entry):
    req(type(entry) is dict and set(entry)=={'path','sha256'},'input schema')
    req(re.fullmatch('[0-9a-f]{64}',entry['sha256']) is not None,'input digest')
    path=local_file(entry['path']);raw=path.read_bytes()
    req(h(raw)==entry['sha256'],'changed input '+str(path))
    return path,raw

req(sys.implementation.name=='cpython' and sys.version_info[:3]==(3,11,15),'control version')
req(P(sys.executable).resolve()==SLOTS['311'][0].resolve(),'control executable')
req(sys.flags.isolated and sys.flags.no_site and sys.flags.safe_path and sys.dont_write_bytecode,'control flags')
label,slot,seed,config_relative,config_sha=sys.argv[1:]
req(re.fullmatch('[a-z0-9][a-z0-9-]{0,70}',label) is not None,'label')
req(slot in SLOTS and seed in {'0','1','17'},'slot/seed')
req(re.fullmatch('[0-9a-f]{64}',config_sha) is not None,'config digest')
config_path=local_file(config_relative);config_raw=config_path.read_bytes()
req(h(config_raw)==config_sha,'config changed');config=json.loads(config_raw)
req(set(config)=={'schema','control_sha256','oracle','cases'} and config['schema']==1,'config schema')
control_path=validate(P(__file__).absolute());control_raw=control_path.read_bytes()
req(h(control_raw)==config['control_sha256'],'control changed')
req(h(validate(SOURCE).read_bytes())==SOURCE_SHA,'production source changed')
prototype_raw=validate(PROTOTYPE).read_bytes();req(h(prototype_raw)==PROTOTYPE_SHA,'prototype changed')
oracle_path,oracle_raw=input_file(config['oracle'])
cases_path,cases_raw=input_file(config['cases'])
exe,version=SLOTS[slot];validate(exe)
folder=WORKSPACE/('engineer-storage-'+uuid.uuid4().hex)
req(folder.absolute().is_relative_to(WORKSPACE.absolute()),'snapshot outside workspace')
folder.mkdir();validate(folder)
snapshot=folder/'snapshot';snapshot.mkdir();validate(snapshot)
temp=folder/'temp';temp.mkdir();validate(temp)
files={'prototype.py':prototype_raw,'oracle.py':oracle_raw,'cases'+cases_path.suffix:cases_raw,'control.py':control_raw,'config.json':config_raw}
case_name='cases'+cases_path.suffix
wrapper=r'''import sys,json,os,hashlib,importlib.util
from pathlib import Path
exe,version,seed,manifest_sha,case_name=sys.argv[1:]
assert sys.implementation.name=='cpython' and '.'.join(map(str,sys.version_info[:3]))==version
assert Path(sys.executable).resolve()==Path(exe).resolve()
assert sys.flags.safe_path and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize
assert not sys.flags.ignore_environment and os.environ.get('PYTHONHASHSEED')==seed
assert 'PYTHONPATH' not in os.environ
snapshot=Path.cwd()
manifest_raw=(snapshot/'manifest.json').read_bytes()
assert hashlib.sha256(manifest_raw).hexdigest()==manifest_sha
manifest=json.loads(manifest_raw)
for name,digest in manifest.items():
    assert hashlib.sha256((snapshot/name).read_bytes()).hexdigest()==digest
print(json.dumps({'identity_before_payload_imports':{'executable':sys.executable,'version':sys.version,'version_info':list(sys.version_info[:3]),'implementation':sys.implementation.name,'cwd':str(snapshot),'flags':str(sys.flags),'hash_seed':seed,'hash_probe':hash('pontius-storage-order-probe'),'environment':dict(os.environ),'manifest_sha256':manifest_sha}}),flush=True)
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module
    spec.loader.exec_module(module)
    return module
prototype=load('storage_prototype_under_test',snapshot/'prototype.py')
oracle=load('independent_storage_oracle',snapshot/'oracle.py')
summary=oracle.verify_storage(prototype,case_path=snapshot/case_name)
print(json.dumps({'storage_summary':summary},sort_keys=True),flush=True)
'''
files['wrapper.py']=wrapper.encode()
for name,raw in files.items():create(snapshot/name,raw)
before={name:h(raw) for name,raw in files.items()}
manifest_raw=(json.dumps(before,indent=2)+'\n').encode();create(snapshot/'manifest.json',manifest_raw)
manifest_sha=h(manifest_raw)
windows=validate(P(os.environ['SYSTEMROOT']));system=validate(windows/'System32')
environment={'SYSTEMROOT':str(windows),'WINDIR':str(windows),'COMSPEC':str(system/'cmd.exe'),'PATH':str(system),'TEMP':str(temp),'TMP':str(temp),'PYTHONNOUSERSITE':'1','PYTHONHASHSEED':seed}
command=[str(exe),'-S','-B','-P',str(snapshot/'wrapper.py'),str(exe),version,seed,manifest_sha,case_name]
checks=ROOT/'engineer-checks';checks.mkdir(exist_ok=True);validate(checks)
prefix=label+'-'+slot+'-seed'+seed
setup={'label':label,'slot':slot,'seed':seed,'snapshot':str(snapshot),'temp':str(temp),'command':command,'environment':environment,'config_sha256':config_sha,'control_sha256':h(control_raw),'prototype_sha256':PROTOTYPE_SHA,'oracle':config['oracle'],'cases':config['cases'],'production_source_sha256':SOURCE_SHA,'snapshot_manifest_sha256':manifest_sha,'before':before}
create_json(checks/(prefix+'-setup.json'),setup)
try:
    result=subprocess.run(command,cwd=snapshot,env=environment,capture_output=True,timeout=60)
    code,stdout,stderr=result.returncode,result.stdout,result.stderr
except subprocess.TimeoutExpired as error:
    code,stdout,stderr=124,error.stdout or b'',error.stderr or b''
    stderr+=b'\nCONTROL: finite storage oracle timed out after60 seconds\n'
log=checks/(prefix+'.txt');create(log,stdout+stderr)
after={name:h((snapshot/name).read_bytes()) for name in before}
manifest_after=h((snapshot/'manifest.json').read_bytes())
production_after=h(SOURCE.read_bytes())
originals_after={'prototype':h(PROTOTYPE.read_bytes()),'oracle':h(oracle_path.read_bytes()),'cases':h(cases_path.read_bytes()),'control':h(control_path.read_bytes()),'config':h(config_path.read_bytes())}
identity=None;summary=None
for line in stdout.splitlines():
    try:record=json.loads(line)
    except (ValueError,UnicodeError):continue
    if 'identity_before_payload_imports' in record:identity=record['identity_before_payload_imports']
    if 'storage_summary' in record:summary=record['storage_summary']
receipt={**setup,'exit':code,'stdout_sha256':h(stdout),'stderr_sha256':h(stderr),'log':str(log),'log_sha256':h(stdout+stderr),'after':after,'manifest_after_sha256':manifest_after,'production_source_after_sha256':production_after,'originals_after':originals_after,'identity_before_payload_imports':identity,'summary':summary}
receipt_path=checks/(prefix+'-receipt.json');create_json(receipt_path,receipt)
req(before==after and manifest_sha==manifest_after,'snapshot changed')
req(production_after==SOURCE_SHA,'production source changed during payload')
req(originals_after=={'prototype':PROTOTYPE_SHA,'oracle':config['oracle']['sha256'],'cases':config['cases']['sha256'],'control':h(control_raw),'config':config_sha},'input changed during payload')
req(identity is not None,'missing pre-import identity')
print(json.dumps({'exit':code,'receipt':str(receipt_path),'receipt_sha256':h(receipt_path.read_bytes()),'log_sha256':h(stdout+stderr),'summary':summary},indent=2))
raise SystemExit(code!=0)
