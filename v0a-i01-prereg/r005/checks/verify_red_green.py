"""Retain the actual rejected-packet check and corrected-packet check."""
import json
from pathlib import Path
import subprocess
import sys

checks = Path(__file__).resolve().parent
records = []
for label, packet in [('red', checks.parents[1] / 'r004'),
                      ('green', checks.parent)]:
    argv = [sys.executable, '-B', '-P', str(checks / 'verify_manifest.py'), str(packet)]
    result = subprocess.run(argv, capture_output=True, text=True)
    raw = result.stdout + result.stderr
    with (checks / ('manifest-' + label + '.txt')).open('x', encoding='utf-8', newline='\n') as log:
        log.write(raw)
    records.append(dict(label=label, argv=argv, exit=result.returncode, output=raw))
assert records[0]['exit'] != 0 and 'not lexicographically sorted' in records[0]['output']
assert records[1]['exit'] == 0
with (checks / 'manifest-red-green.json').open('x', encoding='utf-8', newline='\n') as receipt:
    json.dump(records, receipt, indent=2)
    receipt.write('\n')
print(json.dumps(dict(red_exit=records[0]['exit'], green_exit=records[1]['exit'],
                     same_source_commit=True, canonical_identity_verified=True)))
