param([Parameter(Mandatory=$true)][string]$Label, [string]$GeneratorSource)
$ErrorActionPreference='Stop'
if ($Label -notmatch '^[a-z0-9-]+$') { throw 'invalid label' }
$taskRoot='D:\Pontius-handoffs\v0a-i01-ab'
$workRoot='D:\Pontius-worktrees\codex-v0a-i01-c-integration'
$publicationRoot='D:\Pontius-worktrees\codex-v0a-i01-publication-v3'
$git='C:\Program Files\Git\cmd\git.exe'
$base='52bd941e9fa1fb90ff6d2d14df2286e2ee4f4ec8'
$utf8=[Text.UTF8Encoding]::new($false)
$container=Join-Path 'D:\pontius-snapshots' ('c-binding-'+$Label+'-'+[guid]::NewGuid().ToString('N'))
$snapshot=Join-Path $container 'harness'
$temp=Join-Path $container 'temp'
[IO.Directory]::CreateDirectory($temp) | Out-Null
& $git -c core.autocrlf=false clone --quiet --no-hardlinks --no-checkout 'D:\Pontius' $snapshot
if ($LASTEXITCODE -ne 0) { throw 'clone failed' }
& $git -C $snapshot -c core.autocrlf=false checkout --quiet --detach $base
if ($LASTEXITCODE -ne 0) { throw 'checkout failed' }
$overlays=@{}
$publication=@('src/pontius/v0a/runtime.py','src/pontius/v0a/replay.py','src/pontius/v0a/trace.py','tests/test_v0a_replay.py','tests/test_v0a_trace.py')
$cfiles=@('.github/workflows/ci.yml','tools/check_stabilization_boundaries.py','tools/generate_test_inventory.py','tests/test_v0a_boundaries.py','tests/test_inventory_and_profiles.py','tests/test-inventory.json','tests/test-profiles.toml')
foreach ($relative in $publication) {
    Copy-Item -LiteralPath (Join-Path $publicationRoot $relative) -Destination (Join-Path $snapshot $relative)
    $overlays[$relative]=(Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $snapshot $relative)).Hash.ToLowerInvariant()
}
foreach ($relative in $cfiles) {
    $source=Join-Path $workRoot $relative
    if ($GeneratorSource -and $relative -eq 'tools/generate_test_inventory.py') {
        $source=$GeneratorSource
    }
    Copy-Item -LiteralPath $source -Destination (Join-Path $snapshot $relative)
    $overlays[$relative]=(Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $snapshot $relative)).Hash.ToLowerInvariant()
}
$environment=@{
    SYSTEMROOT='C:\windows'; WINDIR='C:\windows'; COMSPEC='C:\windows\system32\cmd.exe';
    PATH='C:\windows\System32'; TEMP=$temp; TMP=$temp; PYTHONPATH=(Join-Path $snapshot 'src');
    PONTIUS_GIT=$git; GIT_CONFIG_NOSYSTEM='1'; GIT_CONFIG_GLOBAL='NUL'
}
$targets=@(
    'DesignReviewTests.test_descriptor_defaults_preserve_real_python_argument_binding',
    'DesignReviewTests.test_receiver_descriptor_not_parameter_spelling_controls_binding',
    'DesignReviewTests.test_unknown_receiver_context_blocks_and_lexical_capture_is_preserved',
    'DesignReviewTests.test_invalid_static_helper_arguments_remain_blocked',
    'DesignReviewTests.test_unproven_helper_descriptor_provenance_remains_blocked',
    'DesignReviewTests.test_helper_registry_and_argument_binding_fail_closed',
    'DesignReviewTests.test_registered_probe_and_cross_file_helpers_are_exactly_resolved',
    'DesignReviewTests.test_source_order_bounds_exception_environments_and_decorators_are_exact',
    'DesignReviewTests.test_round4_decorator_definition_point_red_contracts_are_independent'
)
$metadata=@{ snapshot=$snapshot; temporary=$temp; base=$base; overlay_sha256=$overlays; environment=$environment; targets=$targets }
[IO.File]::WriteAllText((Join-Path $taskRoot ('c-binding-'+$Label+'-snapshot.json')),($metadata | ConvertTo-Json -Depth 6)+"`n",$utf8)
$interpreters=@(
    @('311','D:\Pontius-tools\py311\Scripts\python.exe','3.11.15'),
    @('314','D:\Pontius\.venv\Scripts\python.exe','3.14.6')
)
$receipts=@()
foreach ($slot in $interpreters) {
    $info=[Diagnostics.ProcessStartInfo]::new()
    $info.FileName=$slot[1]
    $info.Arguments='-B -P "'+(Join-Path $taskRoot 'c-binding-payload.py')+'" '+$slot[2]+' "'+$slot[1]+'" '+($targets -join ' ')
    $info.WorkingDirectory=$snapshot
    $info.UseShellExecute=$false
    $info.CreateNoWindow=$true
    $info.RedirectStandardOutput=$true
    $info.RedirectStandardError=$true
    $info.EnvironmentVariables.Clear()
    foreach ($key in $environment.Keys) { $info.EnvironmentVariables[$key]=$environment[$key] }
    $process=[Diagnostics.Process]::new()
    $process.StartInfo=$info
    $started=[DateTime]::UtcNow
    if (-not $process.Start()) { throw 'child start failed' }
    $outRead=$process.StandardOutput.ReadToEndAsync()
    $errRead=$process.StandardError.ReadToEndAsync()
    $process.WaitForExit()
    $stdout=$outRead.GetAwaiter().GetResult()
    $stderr=$errRead.GetAwaiter().GetResult()
    $stem='c-binding-'+$Label+'-'+$slot[0]
    [IO.File]::WriteAllText((Join-Path $taskRoot ($stem+'.txt')),$stdout+"`n"+$stderr,$utf8)
    $receipt=@{ command=$info.FileName+' '+$info.Arguments; cwd=$snapshot; exit_code=$process.ExitCode; started_utc=$started.ToString('o'); completed_utc=[DateTime]::UtcNow.ToString('o'); output_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $taskRoot ($stem+'.txt'))).Hash.ToLowerInvariant() }
    $receipts += $receipt
    Write-Output ($stem+': exit '+$process.ExitCode)
    Write-Output $stderr
}
[IO.File]::WriteAllText((Join-Path $taskRoot ('c-binding-'+$Label+'-receipts.json')),($receipts | ConvertTo-Json -Depth 5)+"`n",$utf8)
