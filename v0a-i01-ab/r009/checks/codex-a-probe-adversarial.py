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
cases=[
('saved-class-alias-after-global-rebind', 'global ReviewTests\nold=ReviewTests\nReviewTests=None\nold._launch()',False,''),
('saved-local-default-callback', 'def mutate(owner=ReviewTests):\n    owner._launch=None\ndef invoke(callback=mutate):\n    callback()\ninvoke()\nself._launch()',True,''),
('kwonly-default-callback', 'def mutate(owner=ReviewTests):\n    owner._launch=None\ndef invoke(*, callback=mutate):\n    callback()\ninvoke()\nself._launch()',True,''),
('local-default-evaluation-is-eager', 'def mutate(owner=ReviewTests):\n    owner._launch=None\ndef never(value=mutate()):\n    pass\nself._launch()',True,''),
('local-default-raise-skips-definition', 'def abort():\n    raise ValueError()\ntry:\n    def never(value=abort()):\n        self._launch(module="dead")\nexcept ValueError:\n    self._launch(module="caught")',False,''),
('finally-return-mutation', 'def mutate(owner=ReviewTests):\n    try:\n        return 1\n    finally:\n        owner._launch=None\nmutate()\nself._launch()',True,''),
('finally-overrides-exception', 'def mutate(owner=ReviewTests):\n    try:\n        raise ValueError()\n    finally:\n        owner._launch=None\ntry:\n    mutate()\nexcept ValueError:\n    pass\nself._launch()',True,''),
('unused-finally-after-return', 'def leave(owner=ReviewTests):\n    return 1\n    owner._launch=None\nleave()\nself._launch()',False,''),
('invalid-call-no-effect', 'def mutate(owner=ReviewTests, /):\n    owner._launch=None\ntry:\n    mutate(owner=self)\nexcept TypeError:\n    self._launch(module="binding-handler")',False,''),
('argument-effect-before-invalid-bind', 'def mutate(owner=ReviewTests):\n    owner._launch=None\ndef target():\n    pass\ntry:\n    target(mutate())\nexcept TypeError:\n    pass\nself._launch()',True,''),
('dictionary-held-default', 'def mutate(owners={"key":ReviewTests}):\n    owners["key"]._launch=None\nmutate()\nself._launch()',True,''),
('forwarded-dictionary-owner', 'def mutate(owner):\n    owner._launch=None\ndef forward(owners=(ReviewTests,)):\n    mutate(owners[0])\nforward()\nself._launch()',True,''),
('captured-callable-default-mutation', 'def mutate(fn=self._launch):\n    fn.__defaults__=(None,"changed")\nmutate()\nself._launch()',True,''),
('captured-receiver-forwarding', 'saved=self._mutate\nold=self\nself=None\nsaved()\nold._launch()',True,'    def _mutate(receiver):\n        def nested(owner=receiver):\n            owner._launch=None\n        nested()\n'),
('class-receiver-forwarding', 'saved=self._mutate\nself=None\nsaved()\nReviewTests._launch()',True,'    @classmethod\n    def _mutate(receiver):\n        def nested(owner=receiver):\n            owner._launch=None\n        nested()\n'),
('closure-rebind-preserves-old-owner', 'owner=ReviewTests\nold=owner\ndef mutate():\n    nonlocal owner\n    owner=None\nmutate()\nold._launch()',False,''),
('closure-rebind-before-read', 'owner=ReviewTests\ndef read():\n    if owner is not None:\n        owner._launch=None\nowner=None\nread()\nself._launch()',False,''),
('ordered-args-walrus', 'module="one"\nself._launch(module=module, ignored=(module:="two"))',False,''),
('caught-failed-lookup-retains-successor', 'ReviewTests: object\ntry:\n    ReviewTests._launch(module="dead")\nexcept UnboundLocalError:\n    self._launch(module="caught")',False,''),
('kwargs-mutator', 'def mutate(**kwargs):\n    kwargs["owner"]._launch=None\nmutate(owner=ReviewTests)\nself._launch()',True,''),
('varargs-mutator', 'def mutate(*owners):\n    owners[0]._launch=None\nmutate(ReviewTests)\nself._launch()',True,''),
('starred-mutator', 'def mutate(owner):\n    owner._launch=None\nmutate(*(ReviewTests,))\nself._launch()',True,''),
('double-star-mutator', 'def mutate(*,owner):\n    owner._launch=None\nmutate(**{"owner":ReviewTests})\nself._launch()',True,''),
('unconsumed-registered-generator', 'self._mutate()\nself._launch()',False,'    @classmethod\n    def _mutate(owner):\n        owner._launch=None\n        yield None\n'),
('consumed-registered-generator', 'list(self._mutate())\nself._launch()',True,'    @classmethod\n    def _mutate(owner):\n        owner._launch=None\n        yield None\n'),
('callee-captured-before-local-rebind', 'def first(ignored=None):\n    self._launch(module="first")\ndef second():\n    self._launch(module="second")\nfirst(ignored=(first:=second))',False,''),
('nested-default-before-later-cell', 'module="first"\ndef launch(module=module):\n    self._launch(module=module)\nmodule="second"\nlaunch()',False,''),
('parameter-explicit-override-default', 'def mutate(owner=ReviewTests):\n    if owner is not None:\n        owner._launch=None\nmutate(None)\nself._launch()',False,''),
('unrelated-member-through-default', 'def mutate(owner=ReviewTests):\n    owner.other=None\nmutate()\nself._launch()',False,''),
]
results=[]
for label,body,blocked,extra in cases:
    text=source(body,extra)
    # Only execute a distinct harmless event projection; the sensitive text is data.
    pure=text.replace(sink,'events.append(module)')
    assert 'subprocess.run(' not in pure and 'cupy' not in pure
    ns={'events':[]}; exec(compile(pure,'<pure-'+label+'>','exec'),ns)
    case=ns['ReviewTests']('test_static')
    error=None
    try: case.test_static()
    except Exception as exc: error=type(exc).__name__
    actual=list(ns['events'])
    review=g.derive_design_review(baseline_commit='1'*40,baseline_root_tree_oid='2'*40,inventory_document=inv,inventory_document_bytes=invbytes,sources={PATH:text.encode(),'tools/test_child.py':b'def _run_gpu_probe(): return None\n'},item_universe=universe)
    rows=[r['argv'] for r in review['receipt']['expanded_rows'] if r['capability_kind']=='subprocess']
    reasons=[b['reason'] for b in review['unresolved_dynamic_blockers']]
    passed=bool(reasons) if blocked else not reasons and rows==[['-m',item] for item in actual] and error is None
    result={'case':label,'pure_events':actual,'pure_error':error,'must_refuse':blocked,'rows':rows,'blockers':reasons,'passed':passed}
    results.append(result); print(json.dumps(result),flush=True)
print(json.dumps({'cases':len(results),'passed':sum(r['passed'] for r in results),'failed':[r['case'] for r in results if not r['passed']]}),flush=True)
sys.exit(0 if all(r['passed'] for r in results) else 1)
