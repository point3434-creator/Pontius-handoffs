# Repeat only inside the private review snapshot; Python 3.14.6.
$env:TEMP = 'D:/Pontius/tmp/eval-runner-cold01-20260910/test-temp'
$env:TMP = $env:TEMP
$env:PYTHONPATH = 'D:/Pontius/tmp/eval-runner-cold01-20260910/snapshot;D:/Pontius/tmp/eval-runner-cold01-20260910/snapshot/src;D:/Pontius/tmp/eval-runner-cold01-20260910/snapshot/tests;D:/Pontius/.venv/Lib/site-packages'
$env:PONTIUS_GIT = 'C:/Program Files/Git/cmd/git.exe'
Set-Location -LiteralPath 'D:/Pontius/tmp/eval-runner-cold01-20260910/snapshot'
& 'C:/Users/point/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B -P -W error::ResourceWarning -c 'import sys, unittest; print(sys.version, flush=True); suite=unittest.defaultTestLoader.loadTestsFromNames(["test_retained_eval_run.EvidenceTests", "test_retained_eval_run.RunnerTests", "test_eval_completion_tool.CompletionAdmissionTests"]); result=unittest.TextTestRunner(verbosity=2).run(suite); sys.exit(not result.wasSuccessful())'
# The original diagnostic used the identical reproduction.py content via stdin.
Get-Content -Raw -LiteralPath 'D:/Pontius/tmp/eval-runner-cold01-20260910/late-signal-reproduction.py' | & 'C:/Users/point/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B -P -W error::ResourceWarning -
