import ast, hashlib, importlib.util, json, pathlib, sys, textwrap
root=pathlib.Path.cwd()
path=root/'tools'/'generate_test_inventory.py'
spec=importlib.util.spec_from_file_location('codex_a_inventory',path)
g=importlib.util.module_from_spec(spec);sys.modules[spec.name]=g;spec.loader.exec_module(g)
assert pathlib.Path(g.__file__).resolve()==path.resolve()
ids=['tests/test_review.py::ReviewTests::test_denied','tests/test_review.py::ReviewTests::test_static']
assignment={'profile_name':'current','payload_id':'current:tests/test_review.py','expectation':{'kind':'pass'}}
entries=[dict(stable_id=i,relative_path='tests/test_review.py',case_name='ReviewTests',method_name=i.split('::')[-1],assignment=assignment,baseline_assignment=assignment) for i in ids]
discovery={'test_file_count':1,'stable_id_count':2,'stable_ids_sha256':hashlib.sha256(('\n'.join(sorted(ids))+'\n').encode()).hexdigest()}
inventory={'schema_version':'pontius-test-inventory-v1','baseline_commit':'1'*40,'baseline_discovery':discovery,'discovery':discovery,'entries':entries}
inventory_bytes=(json.dumps(inventory,sort_keys=True,separators=(',',':'))+'\n').encode()
universe=[('stable_id',i) for i in ids]+[('fixture','fixture:tests/test_review.py'),('fixture','fixture:tests/test_review.py::ReviewTests'),('probe','probe:gpu-availability')]
def source(helper,entry,receiver='self',prefix=''):
 return 'import subprocess, sys, unittest\n'+prefix+'class ReviewTests(unittest.TestCase):\n'+textwrap.indent(helper,'    ')+'\n'+f'    def test_static({receiver}):\n'+textwrap.indent(entry,'        ')+'\n    def test_denied(self): pass\n'
def review(text):
 return g.derive_design_review(baseline_commit='1'*40,baseline_root_tree_oid='2'*40,inventory_document=inventory,inventory_document_bytes=inventory_bytes,sources={'tests/test_review.py':text.encode(),'tools/test_child.py':b'def _run_gpu_probe():\n    return None\n'},item_universe=universe)
def helper(decorator='',params='self, module="alpha", /, *, timeout=7',value='module'):
 return (decorator+'\n' if decorator else '')+f'def _launch({params}):\n    subprocess.run([sys.executable, "-m", {value}], cwd=".", env={{**__import__("os").environ, "SAFE":"1"}}, timeout=7, check=False)'
fixed=helper(params='self=None',value='"fixed"')
cases=[
 ('ordinary-posonly-default',helper(),'self._launch()',False,'alpha'),
 ('ordinary-posonly-explicit',helper(),'self._launch("beta")',False,'beta'),
 ('ordinary-posonly-keyword-invalid',helper(),'self._launch(module="beta")',True,None),
 ('staticmethod-kwonly-default',helper('@staticmethod','*, module="alpha"'),'self._launch()',False,'alpha'),
 ('staticmethod-kwonly-explicit',helper('@staticmethod','*, module="alpha"'),'ReviewTests._launch(module="beta")',False,'beta'),
 ('staticmethod-noargs-fixed',helper('@staticmethod','',value='"fixed"'),'self._launch()',False,'fixed'),
 ('classmethod-all-defaults',helper('@classmethod','cls=None, module="alpha"'),'ReviewTests._launch()',False,'alpha'),
 ('classmethod-duplicate-receiver',helper('@classmethod','cls=None, module="alpha"'),'self._launch(cls=None)',True,None),
 ('ordinary-no-positional-receiver',helper(params='*, module="alpha"'),'self._launch()',True,None),
 ('ordinary-all-default',helper(params='self=None, module="alpha"'),'self._launch()',False,'alpha'),
 ('unbound-explicit',helper(params='self, module="alpha"'),'ReviewTests._launch(None, "beta")',False,'beta'),
 ('fixed-invalid-extra',fixed,'self._launch("bad", "extra")',True,None),
 ('fixed-reassigned-receiver',fixed,'self = None\nself._launch()',True,None),
 ('fixed-comp-shadow',fixed,'[self._launch() for self in [None]]',True,None),
 ('fixed-comp-outer-opposing',fixed,'[self._launch() for unused in [None]]',False,'fixed'),
 ('fixed-for-shadow',fixed,'for self in [None]:\n    self._launch()',True,None),
 ('fixed-classname-shadow',helper('@staticmethod','',value='"fixed"'),'ReviewTests = None\nReviewTests._launch()',True,None),
 ('fixed-classname-argument',helper('@staticmethod','',value='"fixed"')+'\ndef _caller(self, ReviewTests=None):\n    ReviewTests._launch()','self._caller()',True,None),
 ('fixed-context-static',helper('@staticmethod','self=None',value='"fixed"')+'\n@staticmethod\ndef _caller(self=None):\n    self._launch()','self._caller()',True,None),
 ('fixed-unknown-decorator',helper('@property','self',value='"fixed"'),'self._launch()',True,None),
]
results=[]
for label,h,e,blocked,argv in cases:
 raw=source(h,e)
 try:
  result=review(raw)
  blockers=result['unresolved_dynamic_blockers'];rows=[r for r in result['receipt']['expanded_rows'] if r['capability_kind']=='subprocess']
  actual=[r['argv'] for r in rows]
  ok=bool(blockers) if blocked else not blockers and actual==[['-m',argv]]
  row={'case':label,'expected_blocked':blocked,'expected_argv':argv,'passed':ok,'actual_argv':actual,'blockers':blockers,'source':raw}
 except Exception as error:
  row={'case':label,'passed':False,'error':repr(error),'source':raw}
 results.append(row)
 print(json.dumps(row),flush=True)
print(json.dumps({'total':len(results),'passing':sum(x['passed'] for x in results),'failures':[x['case'] for x in results if not x['passed']]}),flush=True)