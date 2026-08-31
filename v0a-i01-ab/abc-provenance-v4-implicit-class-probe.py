import sys,json,importlib.util
from pathlib import Path
exe,version=sys.argv[1:]
assert Path(sys.executable).resolve()==Path(exe).resolve()
assert ".".join(map(str,sys.version_info[:3]))==version
assert sys.flags.safe_path and sys.dont_write_bytecode
print(json.dumps({"identity_before_import":{"executable":sys.executable,"version":sys.version}}),flush=True)
s=importlib.util.spec_from_file_location("implicit_class_tests",Path.cwd()/"tests/test_inventory_and_profiles.py")
m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
t=m.DesignReviewTests();t.setUp();results=[]
for label,body in [
 ("implicit-class-mutation","def mutate(_):\n    __class__._launch=None\nlist(map(mutate, [None]))\nreturn self._launch()"),
 ("implicit-class-readonly","def mutate(_):\n    return __class__.__name__\nlist(map(mutate, [None]))\nreturn self._launch()"),
 ("direct-implicit-class","def mutate():\n    __class__._launch=None\nmutate()\nreturn self._launch()"),
]:
 actual,review=t._provenance_case(body)
 rows=[r for r in review["receipt"]["expanded_rows"] if r["capability_kind"]=="subprocess"]
 blockers=review["unresolved_dynamic_blockers"]
 results.append({"case":label,"projection":actual if isinstance(actual,str) else actual.__name__,"blockers":blockers,"process_rows":rows})
print(json.dumps({"results":results},indent=2))
raise SystemExit(1 if any(r["projection"]=="TypeError" and not r["blockers"] and r["process_rows"] for r in results) else 0)
