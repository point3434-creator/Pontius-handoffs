"""Verify a completion plan's bound inputs against their files, before any claim is taken.

Usage: verify_plan_inputs.py <plan.json>

The plan is the single source of truth for what the producer inputs must be: the wrapper
already pins the plan's own digest, so re-pinning each input digest in the wrapper as well
would only create a drift hazard. This checks, for every member of the plan's `inputs`
object, that the bound path is absolute, exists as a regular file, and hashes to the bound
digest. It reads nothing else and writes nothing.

Prints one line per input and exits 0 only when every one of them verifies.
Exit 2: the plan cannot be read or has no usable `inputs` object.
Exit 3: at least one bound input is missing, unreadable or has the wrong digest.
"""
import hashlib
import json
import pathlib
import sys

HEX = set('0123456789abcdef')


def main(argv):
    if len(argv) != 2:
        print('usage: verify_plan_inputs.py <plan.json>')
        return 2
    try:
        plan = json.loads(pathlib.Path(argv[1]).read_bytes())
    except (OSError, ValueError) as error:
        print('PLAN-UNREADABLE %s' % type(error).__name__)
        return 2
    inputs = plan.get('inputs')
    if type(inputs) is not dict or not inputs:
        print('PLAN-NO-INPUTS')
        return 2
    failed = False
    for name in sorted(inputs):
        item = inputs[name]
        if (type(item) is not dict or set(item) != {'path', 'sha256'}
                or type(item['path']) is not str or type(item['sha256']) is not str
                or len(item['sha256']) != 64 or not set(item['sha256']) <= HEX):
            print('MALFORMED %s' % name)
            failed = True
            continue
        path = pathlib.Path(item['path'])
        if not path.is_absolute():
            print('NOT-ABSOLUTE %s' % name)
            failed = True
            continue
        if not path.is_file():
            print('MISSING %s %s' % (name, item['path']))
            failed = True
            continue
        try:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError as error:
            print('UNREADABLE %s %s' % (name, type(error).__name__))
            failed = True
            continue
        if digest != item['sha256']:
            print('DIGEST %s expected %s observed %s' % (name, item['sha256'], digest))
            failed = True
            continue
        print('BOUND %s %s' % (name, digest))
    return 3 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
