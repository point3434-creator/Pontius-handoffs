import sys,json,hashlib
from pathlib import Path
exe,version=sys.argv[1:3]
assert Path(sys.executable).resolve()==Path(exe).resolve()
assert '.'.join(map(str,sys.version_info[:3]))==version
assert sys.flags.safe_path and sys.dont_write_bytecode
print(json.dumps({"identity_before_payload_import":{"executable":sys.executable,"version":sys.version}}),flush=True)
import pontius.v0a.runtime as runtime
from pontius.immutable_blueprint import ImmutableBlueprintActionSource
from pontius.v0a.replay import ReplayHost,FIXTURE_A,FIXTURE_B,PROTOCOL_ID
from pontius.v0a.trace import parse_trace
class Clock:
    def __init__(self):self.now=1000
    def __call__(self):
        value=self.now;self.now+=1000;return value
rows=[]
for fixture in (FIXTURE_A,FIXTURE_B):
    original=ImmutableBlueprintActionSource(source_id="policy-observer")
    admissions=[];lookups=[];identities=[]
    codes=(runtime._admit_blueprint.__code__,ImmutableBlueprintActionSource.action_for.__code__,
           ImmutableBlueprintActionSource.canonical_bytes.__code__)
    def profile(frame,event,arg):
        if event!="call":return
        if frame.f_code is codes[0]:admissions.append(id(frame.f_locals["source"]))
        elif frame.f_code is codes[1]:lookups.append(id(frame.f_locals["self"]))
        elif frame.f_code is codes[2]:identities.append(id(frame.f_locals["self"]))
    previous=sys.getprofile();sys.setprofile(profile)
    try:
        host=ReplayHost(fixture,run_id=PROTOCOL_ID+"-correctness-policy-observer",
                       blueprint=original,clock=Clock())
        result=host.run()
    finally:sys.setprofile(previous)
    assert result.receipt.passed
    assert admissions==[id(original)]
    assert len(lookups)==len(result.decisions)
    assert len(set(lookups))==1 and lookups[0]!=id(original)
    assert identities and all(value==lookups[0] for value in identities)
    parsed=parse_trace(result.trace)
    assert parsed.header["blueprint_sha256"]==original.digest
    assert all(row.blueprint_sha256==original.digest for row in result.decisions)
    rows.append(dict(fixture=fixture.name,admissions=len(admissions),sealed_lookups=len(lookups),
        source_digest_calls=len(identities),all_identity_and_lookup_calls_on_owned_source=True,
        header_and_decisions_match_supplied_exact_policy=True,delivered=len(result.decisions)))
print(json.dumps({"observations":rows}),flush=True)
