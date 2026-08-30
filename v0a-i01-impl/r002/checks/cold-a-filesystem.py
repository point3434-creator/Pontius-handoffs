import json, os, sys
from pathlib import Path
snapshot=Path(r'D:\Pontius-review-cold-a-r002')
assert os.path.normcase(sys.executable)==os.path.normcase(r'D:\Pontius\.venv\Scripts\python.exe')
assert sys.implementation.name=='cpython' and sys.version_info[:3]==(3,14,6)
assert Path.cwd()==snapshot and os.environ['PYTHONPATH']==str(snapshot/'src')
assert os.environ['PONTIUS_GIT']==r'C:\Program Files\Git\cmd\git.exe'
assert sys.flags.safe_path and sys.dont_write_bytecode
identity={'executable':sys.executable,'implementation':sys.implementation.name,
          'version':sys.version,'cwd':str(Path.cwd()),'PYTHONPATH':os.environ['PYTHONPATH'],
          'PONTIUS_GIT':os.environ['PONTIUS_GIT']}
print(json.dumps({'before_payload_import':identity}),flush=True)
from pontius.v0a.trace import write_trace
root=snapshot/'cold-a-filesystem'
alias=root/'alias'
assert alias.is_junction()
result={'identity':identity,'alias_is_junction':alias.is_junction(),
        'supplied_destination':str(alias/'through-link.jsonl')}
try:
    digest=write_trace(b'cold-a-link-probe\n',alias/'through-link.jsonl',run_root=root)
    result.update(accepted=True,digest=digest,
                  actual_destination=str(root/'real'/'through-link.jsonl'),
                  actual_bytes=(root/'real'/'through-link.jsonl').read_bytes().decode())
except Exception as error:
    result.update(accepted=False,exception=type(error).__name__,message=str(error))
output=Path(r'D:\Pontius-handoffs\v0a-i01-impl\r002\checks\cold-a-filesystem.json')
with output.open('x',encoding='utf-8',newline='\n') as handle:
    json.dump(result,handle,indent=2); handle.write('\n')
print(json.dumps(result,indent=2))