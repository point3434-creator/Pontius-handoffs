import sys,json,runpy
from hashlib import sha256
assert sys.executable==r"D:\Pontius-tools\py311\Scripts\python.exe" and sys.version_info[:3]==(3,11,15)
assert sys.flags.safe_path and sys.dont_write_bytecode
print(json.dumps(dict(executable=sys.executable,version=sys.version)),flush=True)
from pontius.v0a.replay import FIXTURE_A,PROTOCOL_ID,ReplayHost
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.v0a.trace import parse_trace,canonical_json
clock=iter(range(1000,10**8,1000))
raw=ReplayHost(FIXTURE_A,run_id=PROTOCOL_ID+'-correctness-numeric-range',blueprint=ImmutableBlueprintActionSource('policy'),clock=lambda:next(clock)).run().trace
parse_trace(raw)
rows=[json.loads(row) for row in raw.splitlines()]
row=next(row for row in rows if row['record_type']=='decision')
t=row['timing'];elapsed=10**400
t.update(elapsed_ns=elapsed,emission_observed_ns=t['wall_start_ns']+elapsed,last_valid_observation_ns=t['wall_start_ns']+elapsed,response_compute_seconds=0.0,response_uninstrumented_seconds=0.0,work_cutoff_crossed=True,deadline_crossed=True)
prefix=b''.join((canonical_json(r)+'\n').encode() for r in rows[:-1]);rows[-1]['trace_prefix_sha256']=sha256(prefix).hexdigest()
raw=prefix+(canonical_json(rows[-1])+'\n').encode()
try:parse_trace(raw)
except BaseException as e:print(json.dumps(dict(refusal_type=type(e).__name__,message=str(e))))
else:print('unexpected acceptance')
