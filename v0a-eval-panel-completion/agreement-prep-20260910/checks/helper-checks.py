"""Executed checks for the two helpers the agreement wrapper calls before and after launch.

These run now, during preparation, because neither helper depends on the bindings that are
filled at freeze. The wrapper-level suite (modes, environment guard, claim, race, exit tail)
runs against the filled wrapper at freeze time and is not part of this receipt.

journal_attribution.py is carried unchanged from the solve and export packets. The four
refusal families named as unexercised by the export round's cold review are covered here:
an unparsable row, an absent or non-string `output`, a missing output file, and a
`runtimes_sha256` that does not match the sibling runtimes.json. The last matters most,
because finish_run always writes runtimes_sha256 when an output directory is set, so a real
retained row carries it while only the passing side had ever been exercised.

verify_plan_inputs.py is new: it replaces the export wrapper's duplicated input constants
with a check against the plan itself.

Usage: helper-checks.py <packet> <out.json>
Every case asserts an exit code and a stated condition; the runner exits nonzero if any
case fails, and it opens with a negative control proving the gate records failures.
"""
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile

assert sys.version_info[:3] == (3, 14, 6)
PK = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])
PY = sys.executable
ATTRIBUTE = PK / 'journal_attribution.py'
GUARD = PK / 'verify_plan_inputs.py'
SOURCE = '1c7067448106cfa2aca3d57be879842d72293c61'
rows = []


def check(case, expected, actual, condition, want, got):
    ok = expected == actual and want == got
    rows.append(dict(case=case, expected=str(expected), actual=str(actual),
                     condition=condition, condition_expected=str(want),
                     condition_actual=str(got), passed=ok))
    print('%-38s exit %-4s (want %-4s) %s = %s (want %s) %s'
          % (case, actual, expected, condition, got, want, 'ok' if ok else 'FAIL'))


def run(script, *args):
    done = subprocess.run([PY, '-I', '-B', str(script), *[str(a) for a in args]],
                          text=True, capture_output=True, timeout=30)
    return done.returncode, done.stdout


# S0 negative control: the gate must record a mismatch as a failure.
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    check('S0-deliberate-mismatch', 1, 2, 'condition', 'want', 'got')
recorded = rows[-1]['passed'] is False
rows.pop()
check('S0-gate-records-failures', 0, 0, 'mismatch-recorded', True, recorded)

with tempfile.TemporaryDirectory(prefix='agreement-helpers-') as tmp:
    root = pathlib.Path(tmp)

    # ---- journal_attribution.py -------------------------------------------------------
    run_dir = root / 'experiments/results/runs/new'
    run_dir.mkdir(parents=True)
    result_file = run_dir / 'result.json'
    result_file.write_bytes(b'{}\n')
    runtimes = run_dir / 'runtimes.json'
    runtimes.write_bytes(b'[]\n')
    result_sha = hashlib.sha256(result_file.read_bytes()).hexdigest()
    runtimes_sha = hashlib.sha256(runtimes.read_bytes()).hexdigest()
    good = dict(source_commit=SOURCE, output='experiments/results/runs/new/result.json',
                output_sha256=result_sha)
    old = dict(good, source_commit='old')

    def attribution(name, rows_text, expected_code, expected_label, expect_written):
        journal = root / (name + '.jsonl')
        target = root / (name + '-row.jsonl')
        if target.exists():
            target.unlink()
        journal.write_bytes(rows_text)
        code, out = run(ATTRIBUTE, journal, 1, SOURCE, root, target)
        label = out.split()[0] if out.split() else '(none)'
        written = target.exists()
        check('attribution-' + name, expected_code, code, 'label/written',
              '%s/%s' % (expected_label, expect_written), '%s/%s' % (label, written))

    def line(row):
        return json.dumps(row).encode() + b'\n'

    # the six already exercised in the predecessor packets
    attribution('absent', line(old), 3, 'ABSENT', False)
    attribution('extra', line(old) + line(good) + line(good), 4, 'EXTRA', False)
    attribution('wrong-commit', line(old) + line(dict(good, source_commit='wrong')),
                5, 'MISMATCH', False)
    attribution('wrong-digest', line(old) + line(dict(good, output_sha256='0' * 64)),
                5, 'MISMATCH', False)
    attribution('bound', line(old) + line(good), 0, 'BOUND', True)
    attribution('bound-crlf', json.dumps(old).encode() + b'\r\n' + json.dumps(good).encode()
                + b'\r\n', 0, 'BOUND', True)
    # the four families the export round's cold review named as unexercised
    attribution('unparsable-row', line(old) + b'{not json\n', 5, 'MISMATCH', False)
    attribution('output-absent', line(old) + line({k: v for k, v in good.items()
                                                   if k != 'output'}), 5, 'MISMATCH', False)
    attribution('output-not-string', line(old) + line(dict(good, output=17)),
                5, 'MISMATCH', False)
    attribution('output-file-missing',
                line(old) + line(dict(good, output='experiments/results/runs/new/gone.json')),
                5, 'MISMATCH', False)
    attribution('runtimes-mismatch',
                line(old) + line(dict(good, runtimes_sha256='0' * 64)), 5, 'MISMATCH', False)
    attribution('runtimes-bound',
                line(old) + line(dict(good, runtimes_sha256=runtimes_sha)), 0, 'BOUND', True)

    # ---- verify_plan_inputs.py ---------------------------------------------------------
    teacher = root / 'teacher.json'
    teacher.write_bytes(b'teacher-bytes\n')
    blueprint = root / 'blueprint.json'
    blueprint.write_bytes(b'blueprint-bytes\n')
    producer = root / 'producer-result.json'
    producer.write_bytes(b'producer-bytes\n')

    def bind(path):
        return dict(path=path.as_posix(),
                    sha256=hashlib.sha256(path.read_bytes()).hexdigest())

    def guard(name, inputs, expected_code, expected_token):
        # The guard reports one line per input in sorted order, so a failure on a later
        # input is preceded by BOUND lines for the earlier ones. Assert that the expected
        # token is reported and that no failing case reports every input as bound.
        plan = root / (name + '-plan.json')
        plan.write_bytes(json.dumps(dict(inputs=inputs)).encode() + b'\n')
        code, out = run(GUARD, plan)
        tokens = [l.split()[0] for l in out.splitlines() if l.split()]
        present = expected_token in tokens
        if expected_code != 0:
            present = present and not all(t == 'BOUND' for t in tokens)
        check('guard-' + name, expected_code, code, 'reports ' + expected_token, True, present)

    bound = dict(teacher=bind(teacher), blueprint=bind(blueprint),
                 producer_result=bind(producer))
    guard('all-bound', bound, 0, 'BOUND')
    guard('wrong-digest', dict(bound, teacher=dict(bind(teacher), sha256='0' * 64)),
          3, 'DIGEST')
    guard('missing-file', dict(bound, blueprint=dict(path=(root / 'gone.json').as_posix(),
                                                     sha256='0' * 64)), 3, 'MISSING')
    guard('relative-path', dict(bound, producer_result=dict(path='producer-result.json',
                                                            sha256='0' * 64)),
          3, 'NOT-ABSOLUTE')
    guard('malformed-member', dict(bound, teacher=dict(path=teacher.as_posix())),
          3, 'MALFORMED')
    guard('extra-member-key', dict(bound, teacher=dict(bind(teacher), extra=1)), 3, 'MALFORMED')
    guard('short-digest', dict(bound, teacher=dict(bind(teacher), sha256='abc')), 3, 'MALFORMED')
    guard('empty-inputs', {}, 2, 'PLAN-NO-INPUTS')
    unreadable = root / 'unreadable-plan.json'
    unreadable.write_bytes(b'{not json\n')
    code, out = run(GUARD, unreadable)
    check('guard-unreadable-plan', 2, code, 'reports PLAN-UNREADABLE', True,
          'PLAN-UNREADABLE' in out)
    code, out = run(GUARD)
    check('guard-no-argument', 2, code, 'usage-printed', True, 'usage' in out)

failures = sum(1 for r in rows if not r['passed'])
receipt = dict(python=sys.version, cases=len(rows), failures=failures, results=rows,
               journal_attribution_sha256=hashlib.sha256(ATTRIBUTE.read_bytes()).hexdigest(),
               verify_plan_inputs_sha256=hashlib.sha256(GUARD.read_bytes()).hexdigest(),
               scope='helpers only; the wrapper-level suite runs against the filled wrapper '
                     'at freeze', no_project_invocation=True)
with OUT.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(receipt, stream, indent=2)
    stream.write('\n')
print('\ncases %d failures %d' % (len(rows), failures))
sys.exit(bool(failures))
