$ErrorActionPreference='Stop'
$scratch='D:/Pontius/tmp/eval-runner-r002-cold01-20260910'
$python='C:/Users/point/AppData/Local/Python/pythoncore-3.14-64/python.exe'
$env:TEMP="$scratch/test-temp"
$env:TMP="$scratch/test-temp"
$env:PONTIUS_GIT='C:/Program Files/Git/cmd/git.exe'
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONPATH="$scratch/snapshot;$scratch/snapshot/src;$scratch/snapshot/tests;D:/Pontius/.venv/Lib/site-packages"
Set-Location -LiteralPath "$scratch/snapshot"
& $python -I -B -c 'import sys; print(sys.version)'
& $python -I -B -W error::ResourceWarning "$scratch/red-source/tests/test_retained_eval_run.py" RunnerTests.test_finalization_interrupt_cannot_return_success_or_replace_child_failure *> "$scratch/red-independent.log"
$redExit=$LASTEXITCODE
& $python -B -P -W error::ResourceWarning -m unittest -v test_retained_eval_run.EvidenceTests test_retained_eval_run.RunnerTests test_eval_completion_tool.CompletionAdmissionTests *> "$scratch/focused-green.log"
$greenExit=$LASTEXITCODE
& $python -B -P -W error::ResourceWarning "$scratch/boundary-probes.py" *> "$scratch/boundary-probes.log"
$probeExit=$LASTEXITCODE
@{red_exit=$redExit; focused_green_exit=$greenExit; boundary_probes_exit=$probeExit; python=$python; temp=$env:TEMP; pythonpath=$env:PYTHONPATH} | ConvertTo-Json | Set-Content -LiteralPath "$scratch/check-results.json"
Get-Content -LiteralPath "$scratch/check-results.json"
Get-Content -LiteralPath "$scratch/red-independent.log" -Tail 6
Get-Content -LiteralPath "$scratch/focused-green.log" -Tail 8
Get-Content -LiteralPath "$scratch/boundary-probes.log" -Tail 5
if($redExit -ne 1 -or $greenExit -ne 0 -or $probeExit -ne 0){exit 1}