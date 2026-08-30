param([string]$Python, [string]$Version, [string]$Script, [string]$Label)
$ErrorActionPreference = 'Stop'
$snapshot = 'D:\Pontius-review-snapshots\codex-b-v0a-i01-ab-r005-base-c5e378a6'
$checks = 'D:\Pontius-handoffs\v0a-i01-ab\r006\checks'
$outPath = Join-Path $checks ($Label + '.stdout.txt')
$errPath = Join-Path $checks ($Label + '.stderr.txt')
$receiptPath = Join-Path $checks ($Label + '.json')
if ((Test-Path -LiteralPath $outPath) -or (Test-Path -LiteralPath $errPath) -or (Test-Path -LiteralPath $receiptPath)) { throw 'Receipt paths already exist' }
$taskTemp = Join-Path $snapshot 'codex-b-temp'
New-Item -ItemType Directory -Path $taskTemp -Force | Out-Null
$info = New-Object Diagnostics.ProcessStartInfo
$info.FileName = $Python
$info.Arguments = '-B -P "' + $Script + '" "' + $Python + '" "' + $Version + '"'
$info.WorkingDirectory = $snapshot
$info.UseShellExecute = $false
$info.CreateNoWindow = $true
$info.RedirectStandardOutput = $true
$info.RedirectStandardError = $true
$info.EnvironmentVariables.Clear()
$info.EnvironmentVariables['SYSTEMROOT'] = 'C:\WINDOWS'
$info.EnvironmentVariables['WINDIR'] = 'C:\WINDOWS'
$info.EnvironmentVariables['COMSPEC'] = 'C:\WINDOWS\system32\cmd.exe'
$info.EnvironmentVariables['TEMP'] = $taskTemp
$info.EnvironmentVariables['TMP'] = $taskTemp
$info.EnvironmentVariables['PYTHONPATH'] = Join-Path $snapshot 'src'
$info.EnvironmentVariables['PYTHONNOUSERSITE'] = '1'
$info.EnvironmentVariables['PONTIUS_GIT'] = 'C:\Program Files\Git\cmd\git.exe'
$process = New-Object Diagnostics.Process
$process.StartInfo = $info
$started = [DateTime]::UtcNow.ToString('o')
if (-not $process.Start()) { throw 'Failed to launch Python' }
$stdoutTask = $process.StandardOutput.ReadToEndAsync()
$stderrTask = $process.StandardError.ReadToEndAsync()
$process.WaitForExit()
$stdout = $stdoutTask.Result
$stderr = $stderrTask.Result
$exitCode = $process.ExitCode
$utf8 = New-Object Text.UTF8Encoding($false)
[IO.File]::WriteAllText($outPath, $stdout, $utf8)
[IO.File]::WriteAllText($errPath, $stderr, $utf8)
$receipt = [ordered]@{ command = ($info.FileName + ' ' + $info.Arguments); cwd = $snapshot; started_utc = $started; ended_utc = [DateTime]::UtcNow.ToString('o'); exit_code = $exitCode; environment = [ordered]@{}; stdout_sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $outPath).Hash.ToLowerInvariant(); stderr_sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $errPath).Hash.ToLowerInvariant() }
foreach ($key in $info.EnvironmentVariables.Keys) { $receipt.environment[$key] = $info.EnvironmentVariables[$key] }
[IO.File]::WriteAllText($receiptPath, (($receipt | ConvertTo-Json -Depth 5).Replace("`r`n", "`n") + "`n"), $utf8)
Write-Output $stdout
Write-Output $stderr
Write-Output ('exit=' + $exitCode)
if ($exitCode -ne 0) { throw 'Check failed; inspect receipt' }
