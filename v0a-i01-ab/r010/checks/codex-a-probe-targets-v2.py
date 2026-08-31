import importlib.util, json, sys, textwrap
from hashlib import sha256
from pathlib import Path

p=Path.cwd()/'tools/generate_test_inventory.py'
spec=importlib.util.spec_from_file_location('codex_a_target_generator',p)
generator=importlib.util.module_from_spec(spec);sys.modules[spec.name]=generator
spec.loader.exec_module(generator)
sid='tests/test_cold.py::ColdTests::test_case'
assignment={'profile_name':'current','payload_id':'current:tests/test_cold.py','expectation':{'kind':'pass'}}
census={'test_file_count':1,'stable_id_count':1,'stable_ids_sha256':sha256((sid+'\n').encode()).hexdigest()}
inventory={'schema_version':'pontius-test-inventory-v1','baseline_commit':'1'*40,
 'baseline_discovery':census,'discovery':census,
 'entries':[{'stable_id':sid,'relative_path':'tests/test_cold.py','case_name':'ColdTests','method_name':'test_case','assignment':assignment,'baseline_assignment':assignment}]}
def source(body,sensitive):
    imports='import unittest\n'
    statement='return "fixed"'
    if sensitive:
        imports+='import subprocess, sys\n'
        statement='subprocess.run([sys.executable, "-m", "fixed"], cwd=".", env={**__import__("os").environ, "SAFE":"1"}, timeout=5, check=False)'
    return imports+'class ColdTests(unittest.TestCase):\n    @staticmethod\n    def _launch():\n        '+statement+'\n    def test_case(self):\n'+textwrap.indent(body,'        ')+'\n'

cases=[]
for returned in ('callback','(callback,)[0]','{"cb":callback}["cb"]'):
    for reaches in (False,True):
        body=('owner = None\ndef mutate():\n    if owner is not None:\n        owner._launch = None\n'
              'def forward(callback):\n    return '+returned+'\nsaved = forward(mutate)\n'
              +('owner = ColdTests\n' if reaches else '')+'saved()\nreturn self._launch()')
        cases.append(('late-cell-return-'+returned+'-'+str(reaches),body,reaches))
for operation in ('box.pop("cb")','box.get("cb")','box.popitem()[1]'):
    for reaches in (False,True):
        body='def mutate(owner=ColdTests):\n    owner._launch = None\nbox = {"cb":mutate}\n'
        body+='callback = '+operation+'\n'+('callback()\n' if reaches else '')+'return self._launch()'
        cases.append(('dict-extract-'+operation+'-'+str(reaches),body,reaches))
for construction in ('captured-default','called-default','decorator'):
    for reaches in (False,True):
        effect='ColdTests._launch = None' if reaches else 'return function'
        if construction=='captured-default':
            body=('class Value:\n    def mutate(function=None):\n        '+effect+'\n'
                  '    def __call__(self, callback=mutate):\n        callback()\nValue()()\n')
        elif construction=='called-default':
            body=('class Value:\n    def mutate(function=None):\n        '+effect+'\n'
                  '    def method(self, ignored=mutate()):\n        return 1\n')
        else:
            body=('class Value:\n    def mutate(function=None):\n        '+effect+'\n'
                  '    @mutate\n    def method(self):\n        return 1\n')
        cases.append(('prior-method-'+construction+'-'+str(reaches),body+'return self._launch()',reaches))
cases.append(('proved-local-lookup-before-argument',
 'def mutate(owner=ColdTests):\n    owner._launch = None\n'
 'if False:\n    absent = None\ntry:\n    absent(mutate())\n'
 'except UnboundLocalError:\n    pass\nreturn self._launch()',False))

failed=[]
for name,body,must_refuse in cases:
    harmless=source(body,False);assert 'subprocess' not in harmless and 'pontius' not in harmless
    namespace={}
    try:
        exec(compile(harmless,'<codex-a-harmless-'+name+'>','exec',dont_inherit=True),namespace)
        actual=namespace['ColdTests']().test_case()
    except Exception as exc:actual=type(exc).__name__
    assert actual==('TypeError' if must_refuse else 'fixed'),(name,'bad oracle',actual)
    sensitive=source(body,True).encode()
    review=generator.derive_design_review(baseline_commit='1'*40,baseline_root_tree_oid='2'*40,
        inventory_document=inventory,inventory_document_bytes=(json.dumps(inventory,sort_keys=True,separators=(',',':'))+'\n').encode(),
        sources={'tests/test_cold.py':sensitive},item_universe=(('stable_id',sid),))
    blockers=review['unresolved_dynamic_blockers']
    argv=[r['argv'] for r in review['receipt']['expanded_rows'] if r['capability_kind']=='subprocess']
    # Unsafe effective authority must at least refuse; supported pure controls
    # must retain exactly the unchanged one helper capability and no refusal.
    passed=bool(blockers) if must_refuse else (not blockers and argv==[['-m','fixed']])
    row={'name':name,'oracle':actual,'required_refusal':must_refuse,'passed':passed,
         'source_sha256':sha256(sensitive).hexdigest(),'source':sensitive.decode(),
         'blockers':blockers,'argv':argv}
    print(json.dumps(row),flush=True)
    if not passed:failed.append(name)
print(json.dumps({'cases':len(cases),'failures':failed,'probe_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}))
assert not failed,failed
