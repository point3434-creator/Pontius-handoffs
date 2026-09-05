param([Parameter(Mandatory=$true)][ValidateSet('311','314')][string]$Slot)
$ErrorActionPreference = 'Stop'
$taskRoot = 'D:\Pontius\tmp\v0a-hand-adapter-open-r001'
$candidate = '36c31477d87028aeec31339d28ccc089ffcaa31d'
$overlay = Join-Path $taskRoot 'packets/r001/files'
$runner = Join-Path $taskRoot 'run-snapshot.ps1'
& $runner -RunName post-clean-status -Slot $Slot -Candidate $candidate -Overlay $overlay -PythonArgs @('-m','pontius.status_generation','--check')
& $runner -RunName post-clean-tests -Slot $Slot -Candidate $candidate -Overlay $overlay -PythonArgs @('tests/test_status_generation.py')
