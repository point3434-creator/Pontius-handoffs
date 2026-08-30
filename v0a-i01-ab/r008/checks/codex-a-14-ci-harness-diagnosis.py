import difflib,os,pathlib,subprocess
root=pathlib.Path(r'D:\Pontius-review-snapshots\codex-a-r008-b4138cf23699407a901e6c699771d00d\snapshot');git=r'C:\Program Files\Git\cmd\git.exe'
before=subprocess.run([git,'-C',str(root),'cat-file','blob','d1ed3cbda6107d61ea8e77133871720af04970cd:.github/workflows/ci.yml'],capture_output=True,check=True).stdout
after=(root/'.github/workflows/ci.yml').read_bytes()
print('before',len(before),'CR',before.count(b'\r'),'after',len(after),'CR',after.count(b'\r'))
new=after.decode();start=new.index('      # v0a increment one,');end=new.index('      - name: Ruff report',start);projected=new[:start]+new[end:]
print('exact raw projected match',projected.encode()==before)
print(''.join(difflib.unified_diff(before.decode().splitlines(keepends=True),projected.splitlines(keepends=True))))