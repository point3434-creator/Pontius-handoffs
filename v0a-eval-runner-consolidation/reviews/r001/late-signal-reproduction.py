import json, signal, sys
from unittest.mock import patch
import test_retained_eval_run as tests
case = tests.RunnerTests()
case.setUp()
original = tests.RUNNER.write_new
observed = []
def interrupt_final(path, raw):
    if path.name == 'outcome.json':
        signal.raise_signal(signal.SIGINT)
        observed.append('SIGINT raised with runner deferred handler active before final outcome write')
    return original(path, raw)
try:
    with patch.object(tests.RUNNER, 'write_new', side_effect=interrupt_final):
        code = case.invoke()
    outcome = case.outcome()
    receipt = dict(python=sys.version, injected=observed, returned=code,
                   state=outcome['state'], evidence_complete=outcome['evidence_complete'],
                   child_exit=outcome['child_exit'], recorded_signals=outcome['signals'],
                   errors=outcome['errors'], launches=(case.root/'launch-count').read_text())
    print(json.dumps(receipt, indent=2))
finally:
    case.doCleanups()
