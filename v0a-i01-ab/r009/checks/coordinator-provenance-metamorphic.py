import sys,json,importlib.util
from pathlib import Path
exe,version=sys.argv[1:]
assert Path(sys.executable).resolve()==Path(exe).resolve()
assert ".".join(map(str,sys.version_info[:3]))==version and sys.flags.safe_path and sys.dont_write_bytecode
print(json.dumps({"identity_before_import":{"executable":sys.executable,"version":sys.version}}),flush=True)
s=importlib.util.spec_from_file_location("closure_escape_tests",Path.cwd()/"tests/test_inventory_and_profiles.py")
m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
t=m.DesignReviewTests();t.setUp();results=[]
for name,anchor,final in [
 ("self-only","","self._launch()"),
 ("inert-class-name","unused = ReviewTests\n","self._launch()"),
 ("class-tail","","ReviewTests._launch()"),
]:
 source=anchor+"def mutate(_, owner=ReviewTests):\n    owner._launch=None\nlist(map(mutate, [None]))\nreturn "+final
 actual,review=t._provenance_case(source)
 results.append({"case":name,"projection":actual.__name__ if isinstance(actual,type) else actual,"blockers":review["unresolved_dynamic_blockers"],"process_rows":review["receipt"]["expanded_rows"]})
print(json.dumps({"results":results},indent=2))
raise SystemExit(1 if any(not r["blockers"] and r["process_rows"] for r in results) else 0)
