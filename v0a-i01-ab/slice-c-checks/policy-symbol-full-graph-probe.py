import sys,runpy,json
from pathlib import Path
assert sys.executable==r"D:\Pontius-tools\py311\Scripts\python.exe"
assert sys.version_info[:3]==(3,11,15) and sys.flags.safe_path and sys.dont_write_bytecode
print(json.dumps(dict(executable=sys.executable,version=sys.version)),flush=True)
c=runpy.run_path("tools/check_stabilization_boundaries.py")
cases={
 "absolute_symbol":"from pontius.holdem_cards import SixSeatHoldemDeal\n",
 "relative_symbol":"from ..holdem_cards import SixSeatHoldemDeal as Deal\n",
 "qualified_symbol":"import pontius.holdem_cards as cards\nDeal = cards.SixSeatHoldemDeal\n",
 "star_symbol":"from pontius.holdem_cards import *\n",
 "host_relative":"from . import replay\n",
 "host_package":"from pontius.v0a import replay as host\n",
 "valid_visible":"from ..holdem_cards import OneSeatCardState\n",
}
sources={p.as_posix():p.read_bytes() for p in Path('src/pontius').rglob('*.py')}
results=[]
for name,text in cases.items():
 try:c['enforce_v0a_import_policy']({**sources,'src/pontius/v0a/runtime.py':text.encode()})
 except c['BoundaryError'] as e:results.append(dict(case=name,accepted=False,reason=str(e)))
 else:results.append(dict(case=name,accepted=True))
print(json.dumps(results,indent=2))
