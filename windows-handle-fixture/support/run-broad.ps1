param(
    [Parameter(Mandatory=$true)][ValidateSet('311','314')][string]$Slot,
    [Parameter(Mandatory=$true)][ValidatePattern('^r00[12]$')][string]$Round,
    [Parameter(Mandatory=$true)][switch]$ReviewsConfirmedClean
)
$ErrorActionPreference = 'Stop'
if (-not $ReviewsConfirmedClean) { throw 'Both independent reviews must be confirmed CLEAN first' }
$taskRoot = 'D:\Pontius\tmp\windows-handle-fixture-r001'
$overlay = Join-Path $taskRoot "packets\$Round\files"
if (-not (Test-Path -LiteralPath $overlay)) { throw 'Frozen source overlay absent' }
$commands = @()
foreach ($test in @(
    'test_blueprint_artifact','test_blueprint_artifact_boundary','test_immutable_blueprint',
    'test_status_generation','test_evidence_errors_and_model','test_evidence_manifests',
    'test_evidence_manifest_generation','test_test_orchestration_import_boundary',
    'test_test_orchestration_configuration','test_inventory_and_profiles',
    'test_stabilization_boundaries','test_retained_evidence_inventory',
    'test_v0a_hand_replay','test_v0a_trace','test_v0a_replay','test_v0a_contract_faults'
)) { $commands += ,@("tests/$test.py") }
$commands += ,@('-m','pontius.status_generation','--check')
$commands += ,@('tools/generate_test_inventory.py','--check')
$commands += ,@('tools/check_stabilization_boundaries.py')
$summary = @()
for ($i=0; $i -lt $commands.Count; $i++) {
    $name = 'broad-{0}-{1:d2}' -f $Round,($i+1)
    $failure = $null
    try {
        & (Join-Path $taskRoot 'run-snapshot.ps1') -RunName $name -Slot $Slot -Overlay $overlay -PythonArgs $commands[$i] | Out-Null
    } catch { $failure = $_.Exception.Message }
    $receipt = Join-Path $taskRoot "run-records\$name-$Slot.json"
    if (Test-Path -LiteralPath $receipt) {
        $record = @(Get-Content -Raw -LiteralPath $receipt | ConvertFrom-Json)[-1]
        $row = [ordered]@{sequence=($i+1);slot=$Slot;command=$commands[$i];exit_code=$record.exit_code;receipt=$receipt;failure=$failure}
    } else {
        $row = [ordered]@{sequence=($i+1);slot=$Slot;command=$commands[$i];exit_code=$null;receipt=$null;failure=$failure}
    }
    $summary += $row
    $row | ConvertTo-Json -Compress -Depth 4
}
$summaryPath = Join-Path $taskRoot "broad-$Round-$Slot.json"
$summary | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $summaryPath -Encoding utf8NoBOM
if (@($summary | Where-Object { $null -eq $_.exit_code -or $_.exit_code -ne 0 }).Count) { throw 'Broad population has unresolved failed/missing commands; see receipts' }
