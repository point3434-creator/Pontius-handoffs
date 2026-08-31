import sys,json,importlib.util
from pathlib import Path
exe,version=sys.argv[1:]
assert Path(sys.executable).resolve()==Path(exe).resolve()
assert ".".join(map(str,sys.version_info[:3]))==version
assert sys.flags.safe_path and sys.dont_write_bytecode
print(json.dumps({"identity_before_import":{"executable":sys.executable,"version":sys.version,"cwd":str(Path.cwd())}}),flush=True)
spec=importlib.util.spec_from_file_location("owner_probe_tests",Path.cwd()/"tests/test_inventory_and_profiles.py")
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
t=m.DesignReviewTests();t.setUp()
cases=[('kw-default-write', 'def mutate(*, owner=ReviewTests):\n    owner._launch = None\nmutate()\nreturn ReviewTests._launch()', '', True), ('posonly-default-write', 'def mutate(owner=ReviewTests, /):\n    owner._launch = None\nmutate()\nreturn ReviewTests._launch()', '', True), ('global-owner-write', 'def mutate():\n    ReviewTests._launch = None\nmutate()\nreturn ReviewTests._launch()', '', True), ('closure-owner-write', 'owner = ReviewTests\ndef mutate():\n    owner._launch = None\nmutate()\nreturn ReviewTests._launch()', '', True), ('closure-self-write', 'def mutate():\n    self._launch = None\nmutate()\nreturn self._launch()', '', True), ('container-default-write', 'def mutate(owners=(ReviewTests,)):\n    owners[0]._launch = None\nmutate()\nreturn ReviewTests._launch()', '', True), ('mutation-before-raise', 'def mutate(owner=ReviewTests):\n    owner._launch = None\n    raise ValueError()\ntry:\n    mutate()\nexcept ValueError:\n    return ReviewTests._launch()', '', True), ('overridden-default', 'def mutate(owner=ReviewTests):\n    if owner is not None:\n        owner._launch = None\nmutate(None)\nreturn ReviewTests._launch()', '', False), ('dormant-mutator', 'def mutate(owner=ReviewTests):\n    owner._launch = None\nreturn ReviewTests._launch()', '', False)]
results=[]
for name,body,helper,expected in cases:
    actual,review=t._provenance_case(body,helper=helper)
    blockers=review["unresolved_dynamic_blockers"]
    rows=[r for r in review["receipt"]["expanded_rows"] if r["capability_kind"]=="subprocess"]
    result={"case":name,"pure_projection":actual if isinstance(actual,str) else actual.__name__,"blockers":blockers,"process_rows":rows,"expected_blocked":expected,"matched":bool(blockers)==expected}
    results.append(result)
print(json.dumps({"results":results},indent=2))
raise SystemExit(0 if all(r["matched"] for r in results) else 1)
