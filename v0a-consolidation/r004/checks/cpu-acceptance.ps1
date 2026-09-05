param(
    [Parameter(Mandatory = $true)][string]$Python,
    [Parameter(Mandatory = $true)][ValidateSet('311', '314')][string]$Slot
)
$ErrorActionPreference = 'Stop'
$gitExecutable = 'C:\Program Files\Git\cmd\git.exe'
$packet = 'D:\Pontius\tmp\v0a-consolidation-r001-r004-frozen'
$source = 'D:\Pontius-worktrees\v0a-consolidation-r001'
$identity = Get-Content -Raw (Join-Path $packet 'candidate.json') | ConvertFrom-Json
if ($identity.commit -ne 'fe1e2fc68675c6c92a1263450b455011b5987207') {
    throw 'Unexpected candidate'
}
$stamp = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
$evidence = "D:\Pontius\tmp\v0a-r004-cpu-acceptance-$Slot-$stamp"
$snapshot = Join-Path $evidence 'snapshot'
$scratch = Join-Path $evidence 'scratch'
$utf8 = [System.Text.UTF8Encoding]::new($false)
New-Item -ItemType Directory -Path $evidence, $scratch | Out-Null
& $gitExecutable clone --quiet --no-hardlinks --no-checkout (Join-Path $packet 'repo') $snapshot
if ($LASTEXITCODE -ne 0) { throw 'Snapshot clone failed' }
& $gitExecutable -C $snapshot -c core.autocrlf=false checkout --quiet --detach $identity.commit
if ($LASTEXITCODE -ne 0) { throw 'Snapshot checkout failed' }
$before = Get-Content -Raw 'D:\Pontius\tmp\v0a-consolidation-r004-work\source-sha256.json' |
    ConvertFrom-Json -AsHashtable
foreach ($relative in $before.Keys) {
    foreach ($root in @($source, $snapshot)) {
        $digest = (Get-FileHash -LiteralPath (Join-Path $root $relative) -Algorithm SHA256).Hash
        if ($digest -ne $before[$relative]) { throw "Candidate mismatch: $root / $relative" }
    }
}
Copy-Item -LiteralPath (Join-Path $packet 'candidate.json') -Destination $evidence
Copy-Item -LiteralPath (Join-Path $packet 'manifest.sha256') -Destination $evidence
$commands = @(
    @{ name = 'interpreter'; arguments = @('-c',
        'import sys,platform; print(sys.executable); print(platform.python_implementation()); print(sys.version); print(sys.flags)') },
    @{ name = 'status-freshness'; arguments = @('-m', 'pontius.status_generation', '--check') },
    @{ name = 'status-generation'; arguments = @('tests/test_status_generation.py') },
    @{ name = 'evidence-errors-model'; arguments = @('tests/test_evidence_errors_and_model.py') },
    @{ name = 'evidence-manifests'; arguments = @('tests/test_evidence_manifests.py') },
    @{ name = 'evidence-manifest-generation'; arguments = @('tests/test_evidence_manifest_generation.py') },
    @{ name = 'orchestration-imports'; arguments = @('tests/test_test_orchestration_import_boundary.py') },
    @{ name = 'orchestration-configuration'; arguments = @('tests/test_test_orchestration_configuration.py') },
    @{ name = 'inventory-profiles'; arguments = @('tests/test_inventory_and_profiles.py') },
    @{ name = 'boundaries'; arguments = @('tests/test_stabilization_boundaries.py') },
    @{ name = 'retained-inventory'; arguments = @('tests/test_retained_evidence_inventory.py') },
    @{ name = 'generation-check'; arguments = @('tools/generate_test_inventory.py', '--check') },
    @{ name = 'public-boundary'; arguments = @('tools/check_stabilization_boundaries.py') },
    @{ name = 'v0a-hand-replay'; arguments = @('tests/test_v0a_hand_replay.py') },
    @{ name = 'v0a-trace'; arguments = @('tests/test_v0a_trace.py') },
    @{ name = 'v0a-replay'; arguments = @('tests/test_v0a_replay.py') },
    @{ name = 'v0a-contract-faults'; arguments = @('tests/test_v0a_contract_faults.py') },
    @{ name = 'kernel-action-clock'; arguments = @('tests/test_action_clock.py') },
    @{ name = 'kernel-preparation-bank'; arguments = @('tests/test_preparation_bank.py') },
    @{ name = 'kernel-legal-spine-v2'; arguments = @('tests/test_legal_decision_spine_v2.py') },
    @{ name = 'kernel-betting'; arguments = @('tests/test_no_limit_betting.py') },
    @{ name = 'kernel-cards'; arguments = @('tests/test_holdem_cards.py') },
    @{ name = 'kernel-blueprint'; arguments = @('tests/test_immutable_blueprint.py') }
)
$results = @()
Write-Output "EVIDENCE=$evidence"
foreach ($command in $commands) {
    $start = [System.Diagnostics.ProcessStartInfo]::new()
    $start.FileName = $Python
    $start.WorkingDirectory = $snapshot
    $start.UseShellExecute = $false
    $start.CreateNoWindow = $true
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    $start.ArgumentList.Add('-B')
    $start.ArgumentList.Add('-P')
    foreach ($argument in $command.arguments) { $start.ArgumentList.Add($argument) }
    foreach ($key in @($start.Environment.Keys)) {
        if ($key -match '^(PYTHON|GIT_|PONTIUS_)') { $start.Environment.Remove($key) | Out-Null }
    }
    $start.Environment['PYTHONPATH'] = Join-Path $snapshot 'src'
    $start.Environment['PYTHONNOUSERSITE'] = '1'
    $start.Environment['PONTIUS_GIT'] = $gitExecutable
    $start.Environment['TEMP'] = $scratch
    $start.Environment['TMP'] = $scratch
    $start.Environment['TMPDIR'] = $scratch
    $timer = [System.Diagnostics.Stopwatch]::StartNew()
    Write-Output ('START ' + $command.name)
    $process = [System.Diagnostics.Process]::Start($start)
    $stdoutTask = $process.StandardOutput.ReadToEndAsync()
    $stderrTask = $process.StandardError.ReadToEndAsync()
    $process.WaitForExit()
    $stdout = $stdoutTask.GetAwaiter().GetResult()
    $stderr = $stderrTask.GetAwaiter().GetResult()
    $timer.Stop()
    [System.IO.File]::WriteAllText((Join-Path $evidence ($command.name + '.stdout.log')), $stdout, $utf8)
    [System.IO.File]::WriteAllText((Join-Path $evidence ($command.name + '.stderr.log')), $stderr, $utf8)
    $result = [ordered]@{
        name = $command.name; python = $Python; root = $snapshot
        arguments = @('-B', '-P') + $command.arguments
        exit_code = $process.ExitCode; seconds = [math]::Round($timer.Elapsed.TotalSeconds, 3)
    }
    $results += $result
    Write-Output ($result | ConvertTo-Json -Compress)
    if ($stdout) { Write-Output (($stdout -split '\r?\n' | Select-Object -Last 5) -join "`n") }
    if ($stderr) { Write-Output (($stderr -split '\r?\n' | Select-Object -Last 10) -join "`n") }
    $process.Dispose()
    $raw = ($results | ConvertTo-Json -Depth 5).Replace("`r`n", "`n") + "`n"
    [System.IO.File]::WriteAllText((Join-Path $evidence 'results.json'), $raw, $utf8)
}
foreach ($relative in $before.Keys) {
    foreach ($root in @($source, $snapshot)) {
        $digest = (Get-FileHash -LiteralPath (Join-Path $root $relative) -Algorithm SHA256).Hash
        if ($digest -ne $before[$relative]) { throw "Source drift: $root / $relative" }
    }
}
$raw = ($before | ConvertTo-Json).Replace("`r`n", "`n") + "`n"
[System.IO.File]::WriteAllText((Join-Path $evidence 'source-sha256.json'), $raw, $utf8)
Write-Output ('SOURCE_HASHES_UNCHANGED=' + $before.Count)
$failures = @($results | Where-Object { $_.exit_code -ne 0 }).Count
Write-Output ('FAILED_COMMANDS=' + $failures)
exit $failures
