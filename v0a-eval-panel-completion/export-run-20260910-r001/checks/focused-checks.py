"""Focused export wrapper checks; no project run except --rehearse, once in a snapshot.

Default checks execute guaranteed early refusals, source slices with local inputs, and
the unchanged attribution helper on synthetic journals. Slice digests bind the test seam.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

assert sys.version_info[:3] == (3, 14, 6)
PK = Path(sys.argv[1])
OUT = Path(sys.argv[2])
BASH = 'C:/Program Files/Git/bin/bash.exe'
SOURCE = '1c7067448106cfa2aca3d57be879842d72293c61'
wrapper = (PK / 'invoke.sh').read_text()
env = dict(os.environ)
for key in ('EXPORT_ROOT', 'REHEARSAL', 'REHEARSAL_PK', 'BASH_ENV', 'ENV'):
    env.pop(key, None)
rows = []


def shell(code, extra):
    return subprocess.run([BASH, '--noprofile', '--norc', '-s'], input=code,
                          text=True, capture_output=True, env=dict(env, **extra), timeout=20)


def check(name, expected, actual, **details):
    rows.append(dict(case=name, expected=expected, actual=actual,
                     passed=actual == expected, **details))


for value, expected in [(None, 88), ('0', 88), ('1', 87), ('', 84), ('2', 84),
                        ('yes', 84), ('00', 84), (' 0', 84), ('0\n', 84)]:
    extra = {} if value is None else dict(REHEARSAL=value)
    if value != '1':
        extra['EXPORT_ROOT'] = 'REFUSE-BEFORE-CHECKOUT-ACCESS'
    result = shell(wrapper, extra)
    check('mode-' + repr(value), expected, result.returncode,
          stdout=result.stdout, stderr=result.stderr)
for key in ('EXPORT_ROOT', 'REHEARSAL_PK'):
    result = shell(wrapper, {key: ''})
    check('empty-override-' + key, 88, result.returncode, stdout=result.stdout)
# Authorization is absent during preparation, so this never reaches any checkout write.
assert not (PK / 'authorization.md').exists()
result = shell(wrapper, {})
check('no-authorization', 89, result.returncode, stdout=result.stdout)
check('no-retained-records', False, (PK / 'invocations').exists())

# New pre-claim input guard: exact shell bytes, isolated absolute-path fixtures.
start, end = '# --- producer input digests', '# --- end producer input digests'
guard = wrapper.split(start, 1)[1].split('\n', 1)[1].split(end, 1)[0] if start in wrapper else ''
with tempfile.TemporaryDirectory(prefix='export-branches-') as tmp:
    root = Path(tmp)
    teacher, producer = root / 'teacher.json', root / 'result.json'
    teacher.write_bytes(b'teacher'); producer.write_bytes(b'result')
    extra = dict(TEACHER=teacher.as_posix(), PRODUCER=producer.as_posix(),
                 TEACHER_SHA=hashlib.sha256(b'teacher').hexdigest(),
                 PRODUCER_SHA=hashlib.sha256(b'result').hexdigest())
    setup = ('set -u -o pipefail\nsha() { sha256sum "$1" | cut -d" " -f1; }\n'
             'stop() { echo "$2"; exit "$1"; }\n')
    for case in ('bound', 'teacher-mismatch', 'producer-mismatch', 'teacher-missing'):
        teacher.write_bytes(b'teacher'); producer.write_bytes(b'result')
        if case == 'teacher-mismatch': teacher.write_bytes(b'wrong')
        if case == 'producer-mismatch': producer.write_bytes(b'wrong')
        if case == 'teacher-missing': teacher.unlink()
        result = shell(setup + guard, extra)
        check('producer-' + case, 0 if case == 'bound' else 80, result.returncode,
              stdout=result.stdout, stderr=result.stderr)

    # Real unchanged helper; verify exact copied bytes as well as status and classification.
    run = root / 'experiments/results/runs/new'
    run.mkdir(parents=True)
    result_file = run / 'result.json'; result_file.write_bytes(b'{}\n')
    good = dict(source_commit=SOURCE, output='experiments/results/runs/new/result.json',
                output_sha256=hashlib.sha256(result_file.read_bytes()).hexdigest())
    old = dict(good, source_commit='old')
    for name, values, code, label, crlf in [
        ('absent', [old], 3, 'ABSENT', False), ('extra', [old, good, good], 4, 'EXTRA', False),
        ('wrong-commit', [old, dict(good, source_commit='wrong')], 5, 'MISMATCH', False),
        ('wrong-digest', [old, dict(good, output_sha256='0'*64)], 5, 'MISMATCH', False),
        ('bound', [old, good], 0, 'BOUND', False),
        ('bound-crlf', [old, good], 0, 'BOUND', True)]:
        journal = root / (name + '.jsonl'); target = root / (name + '-row.jsonl')
        encoded = [json.dumps(row).encode() for row in values]
        sep = b'\r\n' if crlf else b'\n'
        journal.write_bytes(sep.join(encoded) + sep)
        result = subprocess.run([sys.executable, '-I', '-B', str(PK / 'journal_attribution.py'),
                                 str(journal), '1', SOURCE, str(root), str(target)],
                                text=True, capture_output=True, timeout=10)
        expected_bytes = encoded[-1] + b'\n' if code == 0 else None
        observed = target.read_bytes() if target.exists() else None
        check('attribution-' + name, [code, label, True],
              [result.returncode, result.stdout.split()[0], observed == expected_bytes],
              stdout=result.stdout, stderr=result.stderr)

# Execute exact exit-precedence tail for every product of child/evidence states.
tail = wrapper[wrapper.index('# Precedence:'):]
for status in (0, 1, 7, 99):
    for evidence in ('complete', 'incomplete'):
        result = shell(tail, dict(rc=str(status), EVIDENCE=evidence))
        expected = status if status else (99 if evidence == 'incomplete' else 0)
        check(f'exit-{status}-{evidence}', [expected, evidence == 'incomplete'],
              [result.returncode, 'EVIDENCE INCOMPLETE' in result.stdout])

receipt = dict(python=sys.version, cases=len(rows), failures=sum(not r['passed'] for r in rows),
               results=rows, source_sha256=hashlib.sha256((PK / 'invoke.sh').read_bytes()).hexdigest(),
               slices_sha256={k: hashlib.sha256(v.encode()).hexdigest()
                              for k, v in [('producer_guard', guard), ('exit_tail', tail)]},
               no_project_invocation=True)
with OUT.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(receipt, stream, indent=2); stream.write('\n')
print(json.dumps(dict(cases=receipt['cases'], failures=receipt['failures'],
                     failed=[r['case'] for r in rows if not r['passed']])))
sys.exit(bool(receipt['failures']))
