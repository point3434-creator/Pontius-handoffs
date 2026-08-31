import importlib.util, json, sys, textwrap
from hashlib import sha256
from pathlib import Path

generator_path=Path.cwd()/'tools/generate_test_inventory.py'
spec=importlib.util.spec_from_file_location('codex_a_generator',generator_path)
generator=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=generator
spec.loader.exec_module(generator)
sid='tests/test_cold.py::ColdTests::test_case'
assignment={'profile_name':'current','payload_id':'current:tests/test_cold.py','expectation':{'kind':'pass'}}
inventory={'schema_version':'pontius-test-inventory-v1','baseline_commit':'1'*40,
 'baseline_discovery':{'test_file_count':1,'stable_id_count':1,'stable_ids_sha256':sha256((sid+'\n').encode()).hexdigest()},
 'discovery':{'test_file_count':1,'stable_id_count':1,'stable_ids_sha256':sha256((sid+'\n').encode()).hexdigest()},
 'entries':[{'stable_id':sid,'relative_path':'tests/test_cold.py','case_name':'ColdTests','method_name':'test_case','assignment':assignment,'baseline_assignment':assignment}]}

def source(body,sensitive):
    imports='import unittest\n'
    statement='return "fixed"'
    if sensitive:
        imports+='import subprocess, sys\n'
        statement='subprocess.run([sys.executable, "-m", "fixed"], cwd=".", env={**__import__("os").environ, "SAFE":"1"}, timeout=5, check=False)'
    return imports+'class ColdTests(unittest.TestCase):\n    @staticmethod\n    def _launch():\n        '+statement+'\n    def test_case(self):\n'+textwrap.indent(body,'        ')+'\n'

CASES=[
 ('baseline','return self._launch()'),
 ('late-cell-forward','owner = None\ndef mutate():\n    owner._launch = None\ndef forward(callback):\n    callback()\nowner = ColdTests\nforward(mutate)\nreturn self._launch()'),
 ('late-cell-return','owner = None\ndef mutate():\n    owner._launch = None\ndef forward(callback):\n    return callback\nsaved = forward(mutate)\nowner = ColdTests\nsaved()\nreturn self._launch()'),
 ('late-cell-protocol','owner = None\nclass Value:\n    def __call__(self):\n        owner._launch = None\nowner = ColdTests\nValue()()\nreturn self._launch()'),
 ('late-cell-builtin','owner = None\ndef mutate(_):\n    owner._launch = None\nowner = ColdTests\nlist(map(mutate,[0]))\nreturn self._launch()'),
 ('readonly-member-dormant-mutator','class Value:\n    def dangerous(self):\n        ColdTests._launch = None\n    def read(self):\n        return 1\nValue().read()\nreturn self._launch()'),
 ('readonly-class-member-dormant-call','class Value:\n    def __call__(self):\n        ColdTests._launch = None\n    @staticmethod\n    def read():\n        return 1\nValue.read()\nreturn self._launch()'),
 ('literal-attribute-dormant-call','class Value:\n    def __call__(self):\n        ColdTests._launch = None\n    answer = 1\nvalue = Value()\nunused = value.answer\nreturn self._launch()'),
 ('dict-callback-storage','def mutate(owner=ColdTests):\n    owner._launch = None\nbox = {}\nbox["callback"] = mutate\nreturn self._launch()'),
 ('dict-callback-call','def mutate(owner=ColdTests):\n    owner._launch = None\nbox = {}\nbox["callback"] = mutate\nbox["callback"]()\nreturn self._launch()'),
 ('dict-callback-pop','def mutate(owner=ColdTests):\n    owner._launch = None\nbox = {"callback": mutate}\ncallback = box.pop("callback")\ncallback()\nreturn self._launch()'),
 ('list-pop-call','def mutate(owner=ColdTests):\n    owner._launch = None\nbox = []\nbox.append(mutate)\ncallback = box.pop()\ncallback()\nreturn self._launch()'),
 ('captured-original-alias','saved = self._launch\nColdTests._launch = None\nreturn saved()'),
 ('class-method-default-previous-function','class Value:\n    def read():\n        return 1\n    def __call__(self, callback=read):\n        callback()\nValue()()\nreturn self._launch()'),
 ('class-method-default-mutator','class Value:\n    def mutate():\n        ColdTests._launch = None\n    def __call__(self, callback=mutate):\n        callback()\nValue()()\nreturn self._launch()'),
 ('caught-failed-lookup','def mutate(owner=ColdTests):\n    owner._launch = None\ntry:\n    absent(mutate())\nexcept NameError:\n    pass\nreturn self._launch()'),
]
results=[]
for name,body in CASES:
    harmless=source(body,False)
    assert 'subprocess' not in harmless and 'pontius' not in harmless
    namespace={}
    try:
        exec(compile(harmless,'<codex-a-harmless-'+name+'>','exec',dont_inherit=True),namespace)
        actual=namespace['ColdTests']().test_case()
    except Exception as exc:actual=type(exc).__name__
    sensitive=source(body,True).encode()
    try:
        review=generator.derive_design_review(baseline_commit='1'*40,baseline_root_tree_oid='2'*40,
            inventory_document=inventory,inventory_document_bytes=(json.dumps(inventory,sort_keys=True,separators=(',',':'))+'\n').encode(),
            sources={'tests/test_cold.py':sensitive},item_universe=(('stable_id',sid),))
        row={'name':name,'oracle':actual,'source_sha256':sha256(sensitive).hexdigest(),
             'blockers':review['unresolved_dynamic_blockers'],
             'argv':[r['argv'] for r in review['receipt']['expanded_rows'] if r['capability_kind']=='subprocess']}
    except Exception as exc:row={'name':name,'oracle':actual,'analyzer_exception':type(exc).__name__,'message':str(exc)}
    print(json.dumps(row),flush=True);results.append(row)
print(json.dumps({'case_count':len(results),'probe_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}))
