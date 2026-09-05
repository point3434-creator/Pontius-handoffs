"""Read-only source-seal preparation; never constructs or runs a ReplayHost."""

import dataclasses
import hashlib
import inspect
import json
from pathlib import Path
import sys

from pontius.v0a import model, replay, trace


root = Path.cwd().resolve()
assert (root / "src/pontius/v0a/replay.py").resolve() == Path(replay.__file__).resolve()
fixtures = []
for fixture in replay.FIXTURES:
    deal = fixture.deal()
    fixtures.append({
        "declaration": dataclasses.asdict(fixture),
        "materialized_deal": dataclasses.asdict(deal),
        "suit_permutation": fixture.permutation,
        "deal_sha256": deal.digest,
        "configuration_sha256": fixture.configuration_sha256(),
    })
origins = []
for name, module in sorted(sys.modules.items()):
    if name == "pontius" or name.startswith("pontius."):
        path = Path(module.__file__).resolve()
        relative = path.relative_to(root).as_posix()
        raw = path.read_bytes()
        origins.append({"module": name, "path": relative, "bytes": len(raw),
                        "sha256": hashlib.sha256(raw).hexdigest()})
assert not any(name == "cupy" or name.startswith("cupy.") for name in sys.modules)
result = {
    "scope": "materialized source bindings only; no host run, seal or rehearsal",
    "protocol_id": replay.PROTOCOL_ID,
    "event_schema": model.EVENT_SCHEMA_VERSION,
    "trace_schema": trace.TRACE_SCHEMA_VERSION,
    "host_api": "pontius.v0a.replay.ReplayHost.run",
    "host_signature": str(inspect.signature(replay.ReplayHost.run)),
    "reader_api": "pontius.v0a.replay.verify_successful_trace",
    "reader_signature": str(inspect.signature(replay.verify_successful_trace)),
    "fixtures": fixtures,
    "observed_import_origins": origins,
    "origin_limit": "Observed import closure, not arbitrary future dynamic reachability.",
}
sys.stdout.buffer.write((json.dumps(result, indent=2, sort_keys=True) + "\n").encode("ascii"))
