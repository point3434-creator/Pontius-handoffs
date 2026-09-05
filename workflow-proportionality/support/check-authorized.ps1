param([Parameter(Mandatory=$true)][ValidateSet('311','314')][string]$Slot)
$ErrorActionPreference = 'Stop'
$taskRoot = 'D:\Pontius\tmp\workflow-proportionality-r001'
$candidate = '922398389870ba9dc378eb096363de3b1bb3731c'
$overlay = Join-Path $taskRoot 'packets\r001\files'
& (Join-Path $taskRoot 'run-snapshot.ps1') -RunName 'authorized-status' `
    -Slot $Slot -Candidate $candidate -Overlay $overlay `
    -PythonArgs @('-m','pontius.status_generation','--check')
& (Join-Path $taskRoot 'run-snapshot.ps1') -RunName 'authorized-tests' `
    -Slot $Slot -Candidate $candidate -Overlay $overlay `
    -PythonArgs @('tests/test_status_generation.py')
