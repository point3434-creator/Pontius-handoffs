"""In-memory compatibility check on retained input bytes, not a retained phase run."""
from pathlib import Path
from hashlib import sha256
import json
import sys
import time
from pontius.blueprint_artifact.codec import decode_blueprint, encode_blueprint
from pontius.eval_bridge import validate_membership

wire_path, teacher_path, output_path = map(Path, sys.argv[1:])
wire, teacher = wire_path.read_bytes(), teacher_path.read_bytes()
assert sha256(wire).hexdigest() == '666021c448c622caf235b304128d17de02823c12966c66510f5a1ec483814d17'
assert sha256(teacher).hexdigest() == 'c3ffab403eb7e939857cc31b0f21b255cefdffd8b0d26d078b703c1fe956b3e3'
source = decode_blueprint(wire)
assert encode_blueprint(source) == wire
start = time.perf_counter()
result = validate_membership(teacher, wire)
elapsed = time.perf_counter() - start
record = dict(wire_sha256=sha256(wire).hexdigest(), wire_bytes=len(wire),
              teacher_sha256=sha256(teacher).hexdigest(), source_digest=source.digest,
              canonical_sha256=sha256(source.canonical_bytes()).hexdigest(),
              diagnostic_membership_seconds=elapsed, result=result)
output_path.write_text(json.dumps(record, sort_keys=True, indent=2) + '\n', newline='\n')
print(json.dumps({k: v for k, v in record.items() if k != 'result'}))
print(json.dumps({k: v for k, v in result.items() if k != 'rows'}))
