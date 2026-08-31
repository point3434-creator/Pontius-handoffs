import ast, hashlib, json, os, subprocess
from pathlib import Path
G=Path(os.environ['PONTIUS_GIT']); assert G.is_absolute() and G.is_file()
C='29c02f6fbd5eb0b7ddc9e816ef28f570b9839358'; OLD='8d240db477b8c141e6142e055dbfbedc75c6a2f8'
def blob(ref,path):return subprocess.run([str(G),'-c','core.hooksPath=NUL','-C',str(Path.cwd()),'cat-file','blob',ref+':'+path],capture_output=True,check=True).stdout
old=json.loads(blob(OLD,'tests/test-inventory.json')); now=json.loads(blob(C,'tests/test-inventory.json'))
a={x['stable_id']:x for x in old['entries']};b={x['stable_id']:x for x in now['entries']}
changed=[key for key,value in a.items() if b.get(key)!=value]; assert not changed
assert blob(OLD,'tests/test-profiles.toml')==blob(C,'tests/test-profiles.toml')
pin=subprocess.run([str(G),'-C',str(Path.cwd()),'rev-parse',C+':docs/architecture/dependency-baseline.toml'],capture_output=True,check=True,text=True).stdout.strip();assert pin=='5fe6ee47f3380b65887b528efef05b72c8e6ac0a'
oldtree=ast.parse(blob(OLD,'tools/generate_test_inventory.py'));newtree=ast.parse(blob(C,'tools/generate_test_inventory.py'))
def limits(tree):
    return {target.id:ast.dump(node.value,include_attributes=False) for node in tree.body if isinstance(node,ast.Assign) for target in node.targets if isinstance(target,ast.Name) and (target.id.startswith('MAXIMUM_') or target.id.startswith('MINIMUM_'))}
assert limits(oldtree)==limits(newtree)
print(json.dumps({'old_entries':len(a),'new_entries':len(b),'added':sorted(b.keys()-a.keys()),'old_entry_changes':changed,'profiles_identical':True,'baseline_blob':pin,'analysis_limits_identical':True},indent=2))
