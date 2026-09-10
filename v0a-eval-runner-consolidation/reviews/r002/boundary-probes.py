import contextlib
import io
import json
import signal
from unittest.mock import patch
import test_retained_eval_run as tests

runner = tests.RUNNER
rows = []
for number in (signal.SIGINT, signal.SIGBREAK):
    for child_failed in (False, True):
        for boundary in ('deferred-evidence', 'stop-transition', 'fsync-written', 'summary-print'):
            case = tests.RunnerTests()
            case.setUp()
            try:
                if child_failed:
                    case.plan['scenario'] = 'child-failed'
                    case.refresh()
                handlers = {n: signal.getsignal(n) for n in (signal.SIGINT, signal.SIGBREAK)}
                original_write = runner.write_new
                original_inventory = runner.inventory
                original_defer = runner.defer_interrupts
                original_fsync = runner.os.fsync
                original_print = print
                captured = {}
                def evidence(directory):
                    result = original_inventory(directory)
                    signal.raise_signal(number)
                    return result
                @contextlib.contextmanager
                def transition():
                    with original_defer() as (received, stop):
                        def injected_stop():
                            stop()
                            signal.raise_signal(number)
                        yield received, injected_stop
                def fsync(fd):
                    original_fsync(fd)
                    captured['written'] = (case.records/'outcome.json').read_bytes().decode()
                    signal.raise_signal(number)
                def writer(path, raw):
                    if path.name == 'outcome.json':
                        with patch.object(runner.os, 'fsync', fsync):
                            return original_write(path, raw)
                    return original_write(path, raw)
                def summary(*args, **kwargs):
                    if args and isinstance(args[0], str) and args[0].startswith('{"state":'):
                        signal.raise_signal(number)
                    return original_print(*args, **kwargs)
                hook = {'deferred-evidence': patch.object(runner, 'inventory', evidence),
                        'stop-transition': patch.object(runner, 'defer_interrupts', transition),
                        'fsync-written': patch.object(runner, 'write_new', writer),
                        'summary-print': patch('builtins.print', summary)}[boundary]
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), hook:
                    status = case.invoke()
                assert status == (7 if child_failed else 99), (boundary, status)
                assert all(signal.getsignal(n) == h for n,h in handlers.items())
                assert (case.records/'claim.d').is_dir()
                assert (case.root/'launch-count').read_bytes() == b'launch\n'
                if boundary == 'deferred-evidence':
                    outcome = case.outcome()
                    assert outcome['signals'] == [number], outcome
                    assert outcome['state'] == 'incomplete' and outcome['evidence_complete'] is False
                else:
                    assert 'FINALIZATION INTERRUPTED' in stderr.getvalue()
                if boundary == 'fsync-written':
                    outcome = json.loads(captured['written'])
                    assert outcome['evidence_complete'] is True
                    assert outcome['exit'] == (7 if child_failed else 0)
                    assert (case.records/'outcome.json').read_text() == captured['written']
                with contextlib.redirect_stderr(stderr):
                    assert case.invoke() == 97
                rows.append(dict(signal=int(number), child_exit=7 if child_failed else 0,
                                 boundary=boundary, invocation_exit=status,
                                 outcome=json.loads(captured['written']) if captured else None,
                                 diagnostic=stderr.getvalue().strip(), passed=True))
            finally:
                case.doCleanups()
print(json.dumps(dict(probes=rows, passed=len(rows)), sort_keys=True, indent=2))