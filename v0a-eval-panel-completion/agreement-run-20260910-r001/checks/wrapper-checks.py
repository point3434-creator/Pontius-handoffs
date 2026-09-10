"""Wrapper-level checks for the frozen agreement invoke.sh. No project phase is launched.

Every case here refuses before any launch, or executes an exact source slice of the frozen
wrapper with local fixtures. The two-caller race and the end-to-end path are covered
separately by the wrapper-driven rehearsal, whose records are in rehearsal/.

Each case asserts an exit code and a stated condition, and the runner exits nonzero if any
case fails. It opens with a negative control proving the gate records failures.

Usage: wrapper-checks.py <packet> <out.json>
"""
import hashlib
import io
import contextlib
import json
import os
import pathlib
import subprocess
import sys
import tempfile

assert sys.version_info[:3] == (3, 14, 6)
PK = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])
BASH = 'C:/Program Files/Git/bin/bash.exe'
WRAPPER = (PK / 'invoke.sh').read_text(encoding='utf-8')
RETAINED = 'D:/Pontius-worktrees/eval-panel-agreement-20260910'
BRANCHED = 'D:/Pontius-worktrees/eval-panel-export-20260910'  # a real worktree on a branch
rows = []

# A base environment that satisfies the pre-claim environment guard, so that the mode and
# root cases reach the predicate they are actually testing.
BASE = {k: os.environ[k] for k in ('SystemRoot', 'TEMP', 'TMP') if k in os.environ}
BASE.setdefault('SystemRoot', os.environ.get('SYSTEMROOT', 'C:/Windows'))


def check(case, expected, actual, condition, want, got):
    ok = str(expected) == str(actual) and str(want) == str(got)
    rows.append(dict(case=case, expected=str(expected), actual=str(actual), condition=condition,
                     condition_expected=str(want), condition_actual=str(got), passed=ok))
    print('%-36s exit %-4s (want %-4s) %s = %s (want %s) %s'
          % (case, actual, expected, condition, got, want, 'ok' if ok else 'FAIL'))


def shell(code, env):
    return subprocess.run([BASH, '--noprofile', '--norc', '-s'], input=code, text=True,
                          capture_output=True, env=env, timeout=60)


def launched():
    """A launch would create the retained record directory or a phase capture anywhere."""
    if (PK / 'invocations').exists():
        return 'launched'
    return 'no-launch'


# ---- S0: the gate itself must record a mismatch -----------------------------------------
with contextlib.redirect_stdout(io.StringIO()):
    check('S0-deliberate-mismatch', 1, 2, 'condition', 'want', 'got')
recorded = rows[-1]['passed'] is False
rows.pop()
check('S0-gate-records-failures', 0, 0, 'mismatch-recorded', True, recorded)

# ---- the pre-claim environment guard, exit 79 -------------------------------------------
# This is the obligation the export round recorded as an Advisory: the launch line expands
# these under `set -u` below the claim, so a shell lacking one consumed the claim and
# started nothing. Here they are checked before anything is claimed.
for name, missing in (('systemroot', ('SystemRoot', 'SYSTEMROOT')), ('temp', ('TEMP',)),
                      ('tmp', ('TMP',))):
    env = dict(BASE, AGREEMENT_ROOT='REFUSE-BEFORE-CHECKOUT-ACCESS', REHEARSAL='1')
    for key in missing:
        env.pop(key, None)
    result = shell(WRAPPER, env)
    check('env-missing-' + name, 79, result.returncode, 'launch', 'no-launch', launched())

# ---- mode guard, exit 84, and the unset/empty distinction --------------------------------
for value, expected in [(None, 88), ('0', 88), ('1', 87), ('', 84), ('2', 84), ('yes', 84),
                        ('00', 84), (' 0', 84), ('0\n', 84)]:
    env = dict(BASE)
    if value is not None:
        env['REHEARSAL'] = value
    if value != '1':
        env['AGREEMENT_ROOT'] = 'REFUSE-BEFORE-CHECKOUT-ACCESS'
    result = shell(WRAPPER, env)
    check('mode-' + repr(value), expected, result.returncode, 'launch', 'no-launch', launched())

# ---- retained mode refuses any set override, even empty, exit 88 -------------------------
for key in ('AGREEMENT_ROOT', 'REHEARSAL_PK'):
    result = shell(WRAPPER, dict(BASE, **{key: ''}))
    check('empty-override-' + key, 88, result.returncode, 'launch', 'no-launch', launched())

# ---- retained mode requires authorization.md, exit 89 ------------------------------------
assert not (PK / 'authorization.md').exists(), 'authorization must be absent during checks'
result = shell(WRAPPER, dict(BASE))
check('no-authorization', 89, result.returncode, 'launch', 'no-launch', launched())

# ---- rehearsal root separation, exits 86 and 85 ------------------------------------------
result = shell(WRAPPER, dict(BASE, REHEARSAL='1', AGREEMENT_ROOT=RETAINED))
check('rehearsal-root-is-retained', 86, result.returncode, 'launch', 'no-launch', launched())
result = shell(WRAPPER, dict(BASE, REHEARSAL='1', AGREEMENT_ROOT=BRANCHED))
check('rehearsal-root-not-detached', 85, result.returncode, 'launch', 'no-launch', launched())

# ---- the plan-input guard as an exact source slice, exit 80 ------------------------------
# The wrapper delegates to verify_plan_inputs.py, so the slice is one line; running it with
# the real helper and a local plan proves the wrapper's branch, not a reimplementation.
start = '# --- producer input digests, read from the plan (before claim acquisition) ---'
guard_line = [l for l in WRAPPER.splitlines() if l.startswith('"$PY" -I -B "$INPUT_GUARD"')]
assert len(guard_line) == 1, 'guard line not found'
guard = guard_line[0] + '\n'
setup = 'set -u -o pipefail\nstop() { echo "PRECONDITION $2"; exit "$1"; }\n'
with tempfile.TemporaryDirectory(prefix='agreement-wrapper-') as tmp:
    root = pathlib.Path(tmp)
    (root / 'plans').mkdir()
    good = root / 'teacher.json'
    good.write_bytes(b'teacher-bytes\n')
    digest = hashlib.sha256(good.read_bytes()).hexdigest()

    def slice_case(name, sha, expected):
        (root / 'plans/agreement.json').write_bytes(
            json.dumps(dict(inputs=dict(teacher=dict(path=good.as_posix(), sha256=sha)))
                       ).encode() + b'\n')
        env = dict(BASE, PY=sys.executable, INPUT_GUARD=str(PK / 'verify_plan_inputs.py'))
        done = subprocess.run([BASH, '--noprofile', '--norc', '-s'], input=setup + guard,
                              text=True, capture_output=True, env=env, cwd=root, timeout=60)
        check('input-guard-' + name, expected, done.returncode, 'launch', 'no-launch',
              launched())

    slice_case('bound', digest, 0)
    slice_case('wrong-digest', '0' * 64, 80)

# ---- retained file inventory as an exact source slice ------------------------------------
# Regression guard. The agreement phase writes a host-inputs/ subdirectory into its run
# directory, which solve and export never did. The first wrapper-driven rehearsal failed
# here: the collector globbed the run directory and handed sha256sum a directory, so a
# completed phase with a bound journal row was recorded as incomplete evidence and exited 99.
inventory = WRAPPER[WRAPPER.index('# --- retained file inventory'):
                    WRAPPER.index('# --- end retained file inventory')]
with tempfile.TemporaryDirectory(prefix='agreement-inventory-') as tmp:
    root = pathlib.Path(tmp)
    run = root / 'experiments/results/runs/newrun'
    (run / 'host-inputs').mkdir(parents=True)
    (run / 'result.json').write_bytes(b'result\n')
    (run / 'host-inputs/host-input.json').write_bytes(b'session\n')
    (root / 'out').mkdir()
    setup_inventory = ('set -u -o pipefail\nsha() { sha256sum "$1" | cut -d" " -f1; }\n'
                       'TRACKED_RUNS=""\nEVIDENCE=complete\n')
    def inventory_case(name, shadow):
        for stale in (root / 'out').glob('*'):
            stale.unlink()
        done = subprocess.run(
            [BASH, '--noprofile', '--norc', '-s'],
            input=setup_inventory + shadow + inventory + '\necho "EVIDENCE=$EVIDENCE"\n',
            text=True, capture_output=True, cwd=root,
            env=dict(BASE, OUT=str(root / 'out')), timeout=60)
        listing = (root / 'out/retained-files.txt').read_text().splitlines()
        names = ','.join(sorted(l.rsplit('  ', 1)[-1].rsplit('/', 1)[-1] for l in listing))
        evidence = done.stdout.strip().splitlines()[-1] if done.stdout.strip() else '(none)'
        return done.returncode, names, evidence

    code, names, evidence = inventory_case('normal', '')
    check('inventory-walks-subdirectories', 0, code, 'files listed',
          'host-input.json,result.json', names)
    check('inventory-normal-keeps-evidence', 0, code, 'evidence', 'EVIDENCE=complete', evidence)

    # I1 controls. A process substitution feeding the loop would not propagate the
    # enumeration's failure, so a run that enumerated nothing, or only part of the tree, and
    # then failed could still be recorded as complete evidence. Each control shadows find.
    # The run directory itself may be absent: a phase that retained nothing must not be
    # recorded as complete evidence just because the loop had nothing to walk.
    code, names, evidence = inventory_case('no-new-run-directory', 'TRACKED_RUNS="newrun"\n')
    check('inventory-no-new-run-directory', 0, code, 'evidence', 'EVIDENCE=incomplete',
          evidence)
    check('inventory-no-new-run-directory-empty', 0, code, 'files listed', '', names)

    # R2-I1. The loop's own input redirection can fail before the body runs, and a while
    # loop that executed no body command returns zero, so the seen check would mask it. The
    # here-string's backing storage could not be made to fail on this build (bash 5.3.15,
    # cygwin), so the guard is exercised against the same construct with a redirection that
    # does fail: a missing file. What is being tested is that a failed loop redirection is
    # detected rather than masked.
    redirect_probe = ('set -u -o pipefail\nseen=0\n'
                      '(\n  seen=$((seen + 1))\n'
                      '  while IFS= read -r f; do echo "body ran"; done < /nonexistent/missing'
                      ' || exit 1\n  [ "$seen" -gt 0 ] || exit 1\n) > /dev/null 2>&1\n'
                      'echo "STATUS=$?"\n')
    done = subprocess.run([BASH, '--noprofile', '--norc', '-s'], input=redirect_probe,
                          text=True, capture_output=True, env=dict(BASE), timeout=60)
    check('inventory-loop-redirection-failure-detected', 0, done.returncode, 'block status',
          'STATUS=1', done.stdout.strip())
    unguarded = redirect_probe.replace(' || exit 1\n  [ "$seen"', '\n  [ "$seen"')
    done = subprocess.run([BASH, '--noprofile', '--norc', '-s'], input=unguarded, text=True,
                          capture_output=True, env=dict(BASE), timeout=60)
    check('inventory-redirection-guard-is-load-bearing', 0, done.returncode,
          'unguarded block status', 'STATUS=0', done.stdout.strip())

    for label, shadow, want_names in (
            ('enumeration-fails', 'find() { return 1; }\n', ''),
            ('enumeration-partial-then-fails',
             'find() { printf "%s\\n" "experiments/results/runs/newrun/result.json"; return 1; }\n',
             ''),
            ('enumeration-returns-no-names', 'find() { return 0; }\n', '')):
        code, names, evidence = inventory_case(label, shadow)
        check('inventory-' + label, 0, code, 'evidence', 'EVIDENCE=incomplete', evidence)
        check('inventory-' + label + '-no-partial-output', 0, code, 'files listed',
              want_names, names)

# ---- exit precedence, the exact tail, over every child status and evidence state ---------
tail = WRAPPER[WRAPPER.index('# Precedence:'):]
for status in (0, 1, 7, 99):
    for evidence in ('complete', 'incomplete'):
        result = shell(tail, dict(BASE, rc=str(status), EVIDENCE=evidence))
        expected = status if status else (99 if evidence == 'incomplete' else 0)
        check('exit-%d-%s' % (status, evidence), expected, result.returncode,
              'incomplete-evidence-message', evidence == 'incomplete',
              'EVIDENCE INCOMPLETE' in result.stdout)

failures = sum(1 for r in rows if not r['passed'])
receipt = dict(python=sys.version, cases=len(rows), failures=failures, results=rows,
               wrapper_sha256=hashlib.sha256((PK / 'invoke.sh').read_bytes()).hexdigest(),
               slices_sha256=dict(input_guard=hashlib.sha256(guard.encode()).hexdigest(),
                                  inventory=hashlib.sha256(inventory.encode()).hexdigest(),
                                  exit_tail=hashlib.sha256(tail.encode()).hexdigest()),
               scope='wrapper refusals and source slices; the two-caller race and the '
                     'end-to-end path are covered by the wrapper-driven rehearsal',
               no_project_invocation=True)
with OUT.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(receipt, stream, indent=2)
    stream.write('\n')
print('\ncases %d failures %d' % (len(rows), failures))
sys.exit(bool(failures))
