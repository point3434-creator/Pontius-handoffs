param([string]$Interpreter,[string]$Version,[string]$Label)
$ErrorActionPreference = 'Stop'
$coldAInfo = [System.Diagnostics.ProcessStartInfo]::new()
$coldAInfo.FileName = $Interpreter
$coldAInfo.WorkingDirectory = 'D:\pontius-snapshots\v0a-r005-cold-a-96aa34d9536845ddaddc4b1dfbb9615e\harness'
$coldAInfo.UseShellExecute = $false
$coldAInfo.CreateNoWindow = $true
$coldAInfo.RedirectStandardOutput = $true
$coldAInfo.RedirectStandardError = $true
$coldAInfo.Environment.Clear()
foreach ($coldAName in @('SYSTEMROOT','WINDIR','TEMP','TMP')) { $coldAInfo.Environment[$coldAName] = [Environment]::GetEnvironmentVariable($coldAName) }
$coldAInfo.Environment['PYTHONPATH'] = 'D:\pontius-snapshots\v0a-r005-cold-a-96aa34d9536845ddaddc4b1dfbb9615e\harness\src'
$coldAInfo.Environment['PONTIUS_GIT'] = 'C:\Program Files\Git\cmd\git.exe'
$coldAInfo.Environment['PYTHONIOENCODING'] = 'utf-8'
$coldAInfo.Environment['PYTHONUTF8'] = '1'
foreach ($coldAArg in @('-B','-P','D:\Pontius-handoffs\v0a-i01-impl\r005\checks\cold-a-verify-v2.py',$Interpreter,$Version)) { $coldAInfo.ArgumentList.Add($coldAArg) }
$coldAProcess = [System.Diagnostics.Process]::Start($coldAInfo)
$coldAStdout = $coldAProcess.StandardOutput.ReadToEndAsync()
$coldAStderr = $coldAProcess.StandardError.ReadToEndAsync()
$coldAProcess.WaitForExit()
$coldAOutput = "Interpreter: $Interpreter`nVersion slot: $Version`nExit: $($coldAProcess.ExitCode)`nstdout:`n$($coldAStdout.Result)`nstderr:`n$($coldAStderr.Result)"
Write-Output $coldAOutput
$coldALog = "D:\Pontius-handoffs\v0a-i01-impl\r005\checks\cold-a-launch-$Label.txt"
if (Test-Path -LiteralPath $coldALog) { throw 'Create-only launcher log exists' }
[System.IO.File]::WriteAllText($coldALog, $coldAOutput.Replace("`r`n", "`n") + "`n", [System.Text.UTF8Encoding]::new($false))
if ($coldAProcess.ExitCode -ne 0) { throw "Cold A diagnostic exit $($coldAProcess.ExitCode)" }
