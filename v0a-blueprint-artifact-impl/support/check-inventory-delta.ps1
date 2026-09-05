param([string]$CandidateRoot = 'D:\Pontius\tmp\v0a-blueprint-artifact-impl-r001\authoring')
$ErrorActionPreference = 'Stop'
$baseRoot = 'D:\Pontius'
$before = Get-Content -Raw (Join-Path $baseRoot 'tests/test-inventory.json') | ConvertFrom-Json -Depth 100
$after = Get-Content -Raw (Join-Path $CandidateRoot 'tests/test-inventory.json') | ConvertFrom-Json -Depth 100
$oldRows = @{}
$newRows = @{}
foreach ($row in $before.entries) { $oldRows[$row.stable_id] = $row }
foreach ($row in $after.entries) {
    if ($newRows.ContainsKey($row.stable_id)) { throw 'Duplicate generated stable ID' }
    $newRows[$row.stable_id] = $row
}
$changed = @()
foreach ($key in $oldRows.Keys) {
    if (-not $newRows.ContainsKey($key)) { throw "Removed old ID: $key" }
    if (($oldRows[$key] | ConvertTo-Json -Depth 100 -Compress) -cne ($newRows[$key] | ConvertTo-Json -Depth 100 -Compress)) { $changed += $key }
}
if ($changed.Count) { throw "Old rows changed: $($changed -join ', ')" }
if (($before.baseline_discovery | ConvertTo-Json -Depth 100 -Compress) -cne ($after.baseline_discovery | ConvertTo-Json -Depth 100 -Compress)) { throw 'Historical baseline discovery changed' }
$introduced = @($newRows.Keys | Where-Object { -not $oldRows.ContainsKey($_) })
$allowed = @('tests/test_v0a_rehearsal_driver.py','tests/test_blueprint_artifact.py','tests/test_blueprint_artifact_boundary.py')
foreach ($key in $introduced) {
    $row = $newRows[$key]
    if ($row.relative_path -notin $allowed -or $row.assignment.profile_name -ne 'current') { throw "Unapproved new row: $key" }
}
$profiles = Get-Content -Raw (Join-Path $CandidateRoot 'tests/test-profiles.toml')
foreach ($binding in @('spec_capabilities_sha256','capability_bindings_sha256')) {
    $matches = [regex]::Matches($profiles,"(?m)^$binding = `"([0-9a-f]+)`"\r?$")
    if ($matches.Count -ne 1 -or $matches[0].Groups[1].Value -cne ('0'*64)) { throw "Nonzero or absent capability binding: $binding" }
}
[ordered]@{
    old_rows_preserved=$oldRows.Count
    new_row_count=$introduced.Count
    new_rows_by_file=@($introduced | ForEach-Object { $newRows[$_].relative_path } | Group-Object | ForEach-Object { [ordered]@{path=$_.Name;count=$_.Count} })
    historical_baseline_unchanged=$true
    capability_bindings_zero=$true
    before_discovery=$before.discovery
    after_discovery=$after.discovery
} | ConvertTo-Json -Depth 8
