from pathlib import Path
import json,os,subprocess,sys
packet=Path(r"D:\Pontius-handoffs\v0a-i01-value-boundaries\r001")
git=r"C:\Program Files\Git\cmd\git.exe"
snap=Path(json.loads((packet/"checks/snapshots.json").read_text())["snapshots"]["coordinator"])
slot=sys.argv[1]
python={"311":r"D:\Pontius-tools\py311\Scripts\python.exe","314":r"D:\Pontius\.venv\Scripts\python.exe"}[slot]
env={key:os.environ[key] for key in ("SYSTEMROOT","WINDIR","TEMP","TMP") if key in os.environ}
env["PYTHONPATH"]=str(snap/"src");env["PONTIUS_GIT"]=git
def gitrun(*args):return subprocess.check_output([git,"-C",str(snap),*args])
assert gitrun("rev-parse","HEAD").decode().strip()=="47d08d8c1556d776358e15811e3e98b859fd6a8b"
assert not gitrun("status","--porcelain").strip()
commands=[
    ("probe",[python,"-B","-P",str(packet/"checks/coordinator-probe.py"),str(snap),slot]),
    ("hand-replay",[python,"-B","-P","tests/test_v0a_hand_replay.py","-v"]),
    ("contract-faults",[python,"-B","-P","tests/test_v0a_contract_faults.py","-v"]),
]
results=[]
for label,argv in commands:
    done=subprocess.run(argv,cwd=snap,env=env,capture_output=True)
    log=packet/("checks/coordinator-"+slot+"-"+label+".txt")
    with log.open("xb") as f:f.write(done.stdout+done.stderr)
    results.append({"command":argv,"exit":done.returncode,"log":str(log)})
assert not gitrun("status","--porcelain").strip()
receipt={"candidate":"47d08d8c1556d776358e15811e3e98b859fd6a8b","manifest_sha256":"cc255e28680f71fe15de78f26bb8f99a337c1c79e12bf3bdf382a8aa74e7844a","slot":slot,"snapshot":str(snap),"results":results,"source_pristine":True}
with (packet/("checks/coordinator-"+slot+"-receipt.json")).open("x",encoding="utf-8",newline="\n") as f:json.dump(receipt,f,indent=2);f.write("\n")
print(json.dumps(receipt,indent=2))
if any(r["exit"] for r in results):sys.exit(1)
