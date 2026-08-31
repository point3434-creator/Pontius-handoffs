import hashlib, importlib.util, json, sys, textwrap
from pathlib import Path
ROOT=Path.cwd()
spec=importlib.util.spec_from_file_location('codex_b_generator',ROOT/'tools/generate_test_inventory.py')
g=importlib.util.module_from_spec(spec); sys.modules[spec.name]=g; spec.loader.exec_module(g)
ID='tests/test_review.py::ReviewTests::test_static'
def review(source):
    assignment={'profile_name':'current','payload_id':'current:tests/test_review.py','expectation':{'kind':'pass'}}
    census={'test_file_count':1,'stable_id_count':1,'stable_ids_sha256':hashlib.sha256((ID+'\n').encode()).hexdigest()}
    inv={'schema_version':'pontius-test-inventory-v1','baseline_commit':'1'*40,'baseline_discovery':census,'discovery':census,'entries':[{'stable_id':ID,'relative_path':'tests/test_review.py','case_name':'ReviewTests','method_name':'test_static','assignment':assignment,'baseline_assignment':assignment.copy()}]}
    return g.derive_design_review(baseline_commit='1'*40,baseline_root_tree_oid='2'*40,inventory_document=inv,inventory_document_bytes=(json.dumps(inv,sort_keys=True,separators=(',',':'))+'\n').encode(),sources={'tests/test_review.py':source.encode()},item_universe=(('stable_id',ID),))
def program(body,sensitive):
    pre='import unittest\n'
    if sensitive:pre+='import subprocess, sys\n'
    sink=('subprocess.run([sys.executable, "-m", module], cwd=".", env={**__import__("os").environ, "SAFE":"1"}, timeout=5, check=False)' if sensitive else 'return module')
    return pre+'class ReviewTests(unittest.TestCase):\n    @staticmethod\n    def _launch(ignored=None,module="fixed"):\n        '+sink+'\n    def test_static(self):\n'+textwrap.indent(body,'        ')+'\n\ndef external(callback):\n    callback(None)\n'
mutate='def mutate(_, owner=ReviewTests):\n    owner._launch = None\n'
cases=[
('deleted-local-default-first',mutate+'absent=0\ndel absent\ntry:\n    def callback(a=absent,b=mutate(None)):\n        pass\nexcept UnboundLocalError:\n    pass\nreturn self._launch()','fixed','safe'),
('deleted-local-decorator-first',mutate+'absent=0\ndel absent\ntry:\n    @absent\n    def callback(a=mutate(None)):\n        pass\nexcept UnboundLocalError:\n    pass\nreturn self._launch()','fixed','safe'),
('explicit-helper-raise-first',mutate+'def stop():\n    raise ValueError()\ntry:\n    def callback(a=stop(),b=mutate(None)):\n        pass\nexcept ValueError:\n    pass\nreturn self._launch()','fixed','safe'),
]
results=[]
for name,body,expected,mode in cases:
    raw=program(body,True); pure=program(body,False)
    assert 'subprocess' not in pure and 'sys.executable' not in pure
    ns={}; exec(compile(pure,'codex-b-pure-'+name,'exec',dont_inherit=True),ns)
    try: actual=ns['ReviewTests']('test_static').test_static()
    except Exception as exc:actual=type(exc).__name__
    try:
        observed=review(raw); blockers=observed['unresolved_dynamic_blockers']; rows=[x for x in observed['receipt']['expanded_rows'] if x['capability_kind']=='subprocess']; argv=[x['argv'] for x in rows]
        good=actual==expected and (bool(blockers) if mode=='block' else (not blockers and argv==[['-m','fixed']]) if mode=='safe' else True)
        result={'case':name,'oracle':actual,'expected':expected,'mode':mode,'satisfied':good,'argv':argv,'blockers':blockers,'source_sha256':hashlib.sha256(raw.encode()).hexdigest(),'source':raw,'pure_source':pure}
    except Exception as exc:result={'case':name,'oracle':actual,'satisfied':False,'analyzer_error':repr(exc),'source':raw,'pure_source':pure}
    results.append(result); print(json.dumps(result),flush=True)
print(json.dumps({'cases':len(results),'satisfied':sum(r['satisfied'] for r in results),'unsatisfied':[r['case'] for r in results if not r['satisfied']]}),flush=True)
