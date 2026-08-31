import ast, json, os, stat, subprocess
from hashlib import sha256
from pathlib import Path

root=Path.cwd();git=Path(os.environ['PONTIUS_GIT'])
assert git.is_absolute() and git.is_file()
for p in (git,*git.parents):assert not p.lstat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT
old='8d240db477b8c141e6142e055dbfbedc75c6a2f8'
candidate='29c02f6fbd5eb0b7ddc9e816ef28f570b9839358'
def blob(ref,path):
    return subprocess.run([str(git),'-C',str(root),'cat-file','blob',ref+':'+path],check=True,capture_output=True,env=os.environ.copy()).stdout
previous=json.loads(blob(old,'tests/test-inventory.json'))
current=json.loads(blob(candidate,'tests/test-inventory.json'))
before={row['stable_id']:row for row in previous['entries']}
after={row['stable_id']:row for row in current['entries']}
removed=sorted(before.keys()-after.keys());added=sorted(after.keys()-before.keys())
changed=sorted(key for key in before.keys()&after.keys() if before[key]!=after[key])
assert not removed and not changed and len(added)==13
assert blob(old,'tests/test-profiles.toml')==blob(candidate,'tests/test-profiles.toml')
path='tests/test_inventory_and_profiles.py'
def methods(raw):
    tree=ast.parse(raw)
    return {cls.name+'::'+node.name:ast.dump(node,include_attributes=False)
            for cls in tree.body if isinstance(cls,ast.ClassDef)
            for node in cls.body if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef))}
bm=methods(blob(old,path));am=methods(blob(candidate,path))
method_changed=sorted(k for k in bm.keys()&am.keys() if bm[k]!=am[k])
for row in (R for R in after.values() if R['relative_path'].startswith('tests/test_v0a_')):
    assert row['assignment']['profile_name']=='current'
result={'candidate':candidate,'before_entries':len(before),'after_entries':len(after),
        'removed_entries':removed,'changed_existing_entries':changed,'new_entries':added,
        'profiles_unchanged':True,'prior_class_methods':len(bm),'final_class_methods':len(am),
        'removed_methods':sorted(bm.keys()-am.keys()),'added_methods':sorted(am.keys()-bm.keys()),
        'changed_existing_method_ast':method_changed,'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(result,indent=2))
