"""Independent data-only helper review probes; pure projections never launch a child."""
import hashlib, importlib.util, json, sys, textwrap
from pathlib import Path
ROOT=Path.cwd()
spec=importlib.util.spec_from_file_location('cold_a_inventory', ROOT/'tools/generate_test_inventory.py')
g=importlib.util.module_from_spec(spec); sys.modules[spec.name]=g; spec.loader.exec_module(g)
PATH='tests/test_review.py'
IDS=[PATH+'::ReviewTests::test_denied',PATH+'::ReviewTests::test_static']
assignment={'profile_name':'current','payload_id':'current:'+PATH,'expectation':{'kind':'pass'}}
entries=[{'stable_id':i,'relative_path':PATH,'case_name':'ReviewTests','method_name':i.rsplit('::',1)[1],'assignment':assignment.copy(),'baseline_assignment':assignment.copy()} for i in IDS]
discovery={'test_file_count':1,'stable_id_count':2,'stable_ids_sha256':hashlib.sha256(''.join(i+'\n' for i in IDS).encode()).hexdigest()}
inv={'schema_version':'pontius-test-inventory-v1','baseline_commit':'1'*40,'baseline_discovery':discovery.copy(),'discovery':discovery.copy(),'entries':entries}
invbytes=json.dumps(inv,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()+b'\n'
universe=(('stable_id',IDS[0]),('stable_id',IDS[1]),('fixture','fixture:'+PATH),('fixture','fixture:'+PATH+'::ReviewTests'),('probe','probe:gpu-availability'))
sink='subprocess.run([sys.executable, "-m", module], cwd=".", env={**__import__("os").environ, "SAFE":"1"}, timeout=5, check=False)'
def source(body,extra='',tail=''):
    return 'import subprocess, sys, unittest\nclass ReviewTests(unittest.TestCase):\n    @staticmethod\n    def _launch(ignored=None, module="fixed"):\n        '+sink+'\n'+extra+'    def test_static(self):\n'+textwrap.indent(body,'        ')+'\n    def test_denied(self): pass\n'+tail
cases=[]
for shape in ('callback-default','callback-keyword','explicit-callback','forwarded-owner','direct-mutation'):
    for seed in ('none','read','tail','receiver'):
        owner='self' if seed=='receiver' else 'ReviewTests'
        if shape=='callback-default':
            body='def mutate(owner='+owner+'):\n    owner._launch=None\ndef invoke(callback=mutate):\n    callback()\ninvoke()'
        elif shape=='callback-keyword':
            body='def mutate(owner='+owner+'):\n    owner._launch=None\ndef invoke(*, callback=mutate):\n    callback()\ninvoke()'
        elif shape=='explicit-callback':
            body='def mutate(owner='+owner+'):\n    owner._launch=None\ndef invoke(callback):\n    callback()\ninvoke(mutate)'
        elif shape=='forwarded-owner':
            body='def mutate(owner):\n    owner._launch=None\ndef forward(owners=('+owner+',)):\n    mutate(owners[0])\nforward()'
        else:
            body='def mutate(owner='+owner+'):\n    owner._launch=None\nmutate()'
        if seed=='read': body='unused=ReviewTests\n'+body
        body+='\n'+('ReviewTests' if seed=='tail' else 'self')+'._launch()'
        cases.append((shape+'-'+seed,body,True,''))
results=[]
for label,body,blocked,extra in cases:
    text=source(body,extra)
    pure=text.replace(sink,'events.append(module)')
    assert 'subprocess.run(' not in pure
    ns={'events':[]}; exec(compile(pure,'<pure-'+label+'>','exec'),ns)
    error=None
    try: ns['ReviewTests']('test_static').test_static()
    except Exception as exc: error=type(exc).__name__
    review=g.derive_design_review(baseline_commit='1'*40,baseline_root_tree_oid='2'*40,inventory_document=inv,inventory_document_bytes=invbytes,sources={PATH:text.encode(),'tools/test_child.py':b'def _run_gpu_probe(): return None\n'},item_universe=universe)
    rows=[r['argv'] for r in review['receipt']['expanded_rows'] if r['capability_kind']=='subprocess']
    reasons=[b['reason'] for b in review['unresolved_dynamic_blockers']]
    result={'case':label,'source_sha256':hashlib.sha256(text.encode()).hexdigest(),'pure_events':ns['events'],'pure_error':error,'rows':rows,'blockers':reasons,'passed':bool(reasons)}
    assert error=='TypeError' and not ns['events'], 'bad independent oracle'
    results.append(result); print(json.dumps(result),flush=True)
print(json.dumps({'cases':len(results),'refused':sum(r['passed'] for r in results),'false_clean':[r['case'] for r in results if not r['passed']]}),flush=True)
sys.exit(0 if all(r['passed'] for r in results) else 1)
