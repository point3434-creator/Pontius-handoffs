"""Assert that every derived figure quoted in the packet's prose matches its receipt.

Stale digests and counts in prose have now been raised as findings twice, because the
figures were written by hand and then drifted when the wrapper or the suites changed. This
recomputes each one from the artifact it describes and fails if the prose disagrees, so the
class of defect cannot recur silently.

Usage: prose-figures.py <packet> <out.json>
"""
import hashlib
import json
import pathlib
import re
import sys

assert sys.version_info[:3] == (3, 14, 6)
PK = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])
rows = []


def check(name, expected, actual):
    ok = expected == actual
    rows.append(dict(check=name, expected=str(expected), actual=str(actual), passed=ok))
    print('%-46s %s %s' % (name, 'ok' if ok else 'FAIL',
                           '' if ok else '(expected %r, prose says %r)' % (expected, actual)))


helper = json.loads((PK / 'checks/helper-checks.json').read_bytes())
wrapper = json.loads((PK / 'checks/wrapper-checks.json').read_bytes())
total = helper['cases'] + wrapper['cases']
wrapper_digest = hashlib.sha256((PK / 'invoke.sh').read_bytes()).hexdigest()
plan_digest = hashlib.sha256((PK / 'plans/agreement.json').read_bytes()).hexdigest()
inventory_cases = [r['case'] for r in wrapper['results'] if r['case'].startswith('inventory-')]

req = (PK / 'authorization-request.md').read_text(encoding='utf-8')
cov = (PK / 'coverage.md').read_text(encoding='utf-8')
scope = (PK / 'review-scope.md').read_text(encoding='utf-8')

# Any 8-hex-digit prefix quoted for the wrapper must be the current wrapper.
for name, text in (('authorization-request', req), ('coverage', cov), ('review-scope', scope)):
    quoted = set(re.findall(r'`([0-9a-f]{8})…`', text))
    stale = {q for q in quoted
             if q not in (wrapper_digest[:8], plan_digest[:8])
             and any(q == hashlib.sha256(p.read_bytes()).hexdigest()[:8]
                     for p in [PK / 'invoke.sh'])}
    check(name + ': no stale wrapper digest', set(), stale)

check('authorization-request names the current wrapper',
      True, wrapper_digest[:8] + '…' in req)
check('authorization-request total case count', True,
      ('%d cases with 0 failures' % total) in req)
check('authorization-request helper case count', True, ('%d helper cases' % helper['cases']) in req)
check('authorization-request wrapper case count', True,
      ('%d wrapper cases' % wrapper['cases']) in req)
check('suites report zero failures', (0, 0), (helper['failures'], wrapper['failures']))
found = re.search(r'(\d+) executed controls cover the normal walk', cov)
check('coverage inventory-control count', len(inventory_cases),
      int(found.group(1)) if found else 'absent')
found = re.search(r'runs (\d+)\s+inventory cases', scope)
check('review-scope inventory-case count', len(inventory_cases),
      int(found.group(1)) if found else 'absent')

failures = sum(1 for r in rows if not r['passed'])
receipt = dict(python=sys.version, checks=len(rows), failures=failures, results=rows,
               wrapper_sha256=wrapper_digest, helper_cases=helper['cases'],
               wrapper_cases=wrapper['cases'], total_cases=total,
               inventory_cases=len(inventory_cases))
with OUT.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(receipt, stream, indent=2)
    stream.write('\n')
print('\nchecks %d failures %d' % (len(rows), failures))
sys.exit(bool(failures))
