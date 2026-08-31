import hashlib,json
from pathlib import Path
root=Path(r'D:\Pontius-handoffs\v0a-i01-ab\r009\checks')
for slot in ('311','314'):
    path=root/('codex-a-forwarding-'+slot+'.txt')
    rows=[json.loads(line) for line in path.read_text().splitlines()[1:]]
    assert rows[-1]['false_clean']==['callback-default-none','callback-keyword-none','explicit-callback-none','forwarded-owner-none']
    print(slot, json.dumps(rows[-1]), hashlib.sha256(path.read_bytes()).hexdigest())
for name in ('codex-a-helper-contracts-311.txt','codex-a-helper-contracts-314.txt','codex-a-generator-check-311.txt','codex-a-generator-check-314.txt','codex-a-inventory.md','codex-a-probe-forwarding.py'):
    print(hashlib.sha256((root/name).read_bytes()).hexdigest(),name)
