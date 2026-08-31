import sys,json,importlib.util
from pathlib import Path
exe,version=sys.argv[1:]
assert Path(sys.executable).resolve()==Path(exe).resolve()
assert ".".join(map(str,sys.version_info[:3]))==version and sys.flags.safe_path and sys.dont_write_bytecode
print(json.dumps({"identity_before_import":{"executable":sys.executable,"version":sys.version}}),flush=True)
s=importlib.util.spec_from_file_location("closure_escape_tests",Path.cwd()/"tests/test_inventory_and_profiles.py")
m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
t=m.DesignReviewTests();t.setUp();results=[]
for name,expr in [("map-consumed","list(map(mutate, [None]))"),("sorted-key","sorted([0], key=mutate)")]:
 for channel,definition in [
  ("local-cell","owner = ReviewTests\ndef mutate(_):\n    owner._launch = None"),
  ("global-owner","def mutate(_):\n    ReviewTests._launch = None"),
  ("receiver-cell","def mutate(_):\n    self._launch = None"),
  ("default-owner","def mutate(_, owner=ReviewTests):\n    owner._launch = None"),
  ("readonly","owner = ReviewTests\ndef mutate(_):\n    return 1"),
 ]:
  body=definition+"\n"+expr+"\nreturn self._launch()"
  actual,review=t._provenance_case(body)
  rows=[r for r in review["receipt"]["expanded_rows"] if r["capability_kind"]=="subprocess"]
  blockers=review["unresolved_dynamic_blockers"]
  bad=channel!="readonly"
  results.append({"case":name+"/"+channel,"projection":actual if isinstance(actual,str) else actual.__name__,"expected_mutation":bad,"blockers":blockers,"process_rows":rows,"unsafe":bad and not blockers and bool(rows)})
print(json.dumps({"results":results},indent=2))
raise SystemExit(1 if any(r["unsafe"] for r in results) else 0)
