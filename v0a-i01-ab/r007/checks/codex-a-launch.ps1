param([string]$Snapshot, [string]$Python, [string]$Version, [string]$Mode, [string]$Receipt)
$ErrorActionPreference = 'Stop'
if(Test-Path -LiteralPath $Receipt){ throw 'Receipt already exists' }
$processInfo = [Diagnostics.ProcessStartInfo]::new()
$processInfo.FileName = $Python
$processInfo.UseShellExecute = $false
$processInfo.RedirectStandardOutput = $true
$processInfo.RedirectStandardError = $true
$processInfo.CreateNoWindow = $true
$processInfo.WorkingDirectory = $Snapshot
$processInfo.Environment.Clear()
$processInfo.Environment['SYSTEMROOT'] = 'C:\WINDOWS'
$processInfo.Environment['WINDIR'] = 'C:\WINDOWS'
$processInfo.Environment['TEMP'] = $Snapshot + '\codex-a-temp'
$processInfo.Environment['TMP'] = $Snapshot + '\codex-a-temp'
$processInfo.Environment['PYTHONPATH'] = $Snapshot + '\src'
$processInfo.Environment['PYTHONNOUSERSITE'] = '1'
$processInfo.Environment['PONTIUS_GIT'] = 'C:\Program Files\Git\cmd\git.exe'
foreach($argument in @('-B', '-P', 'D:\Pontius-handoffs\v0a-i01-ab\r007\checks\codex-a-run.py', $Snapshot, $Version, $Mode, $Python)){ $processInfo.ArgumentList.Add($argument) }
$process = [Diagnostics.Process]::Start($processInfo)
$outTask = $process.StandardOutput.ReadToEndAsync()
$errTask = $process.StandardError.ReadToEndAsync()
$process.WaitForExit()
$output = $outTask.Result + $errTask.Result + "`nEXIT=" + $process.ExitCode + "`n"
[IO.File]::WriteAllText($Receipt, ($output -replace "`r`n", "`n"), [Text.UTF8Encoding]::new($false))
Write-Output $output
if($process.ExitCode -ne 0){ throw 'Payload failed; receipt retained' }
