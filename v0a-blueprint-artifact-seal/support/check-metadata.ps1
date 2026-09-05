param([Parameter(Mandatory=$true)][ValidateSet('311','314')][string]$Slot)
$ErrorActionPreference = 'Stop'
$taskRoot = 'D:\Pontius\tmp\v0a-blueprint-artifact-seal-r001'
$candidate = '12df7106b2fca3b25ed4f57115ba9a31e70b6815'
$overlay = Join-Path $taskRoot 'packets\r002\files'
& (Join-Path $taskRoot 'run-snapshot.ps1') -RunName 'acceptance-r002-status' `
    -Slot $Slot -Candidate $candidate -Overlay $overlay `
    -PythonArgs @('-m','pontius.status_generation','--check')
& (Join-Path $taskRoot 'run-snapshot.ps1') -RunName 'acceptance-r002-tests' `
    -Slot $Slot -Candidate $candidate -Overlay $overlay `
    -PythonArgs @('tests/test_status_generation.py')
