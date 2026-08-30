param([ValidateSet('311','314')][string]$Slot)
$ErrorActionPreference = 'Stop'
$checkRoot = 'D:/Pontius-handoffs/v0a-i01-impl/r004/checks'
$snapshot = 'D:/pontius-snapshots/v0a-r004-cold-a-4ea61c5d8d494d66a1951cf78a019ee3/harness'
$interpreter = if ($Slot -eq '311') {'D:/Pontius-tools/py311/Scripts/python.exe'} else {'D:/Pontius/.venv/Scripts/python.exe'}
$start = [System.Diagnostics.ProcessStartInfo]::new()
$start.FileName = $interpreter
$start.WorkingDirectory = $snapshot
$start.UseShellExecute = $false
$start.CreateNoWindow = $true
$start.RedirectStandardOutput = $true
$start.RedirectStandardError = $true
$start.ArgumentList.Add('-B')
$start.ArgumentList.Add('-P')
$start.ArgumentList.Add($checkRoot + '/cold-a-record-preservation.py')
$start.ArgumentList.Add($Slot)
$start.Environment.Clear()
$start.Environment['SYSTEMROOT'] = 'C:/Windows'
$start.Environment['WINDIR'] = 'C:/Windows'
$start.Environment['TEMP'] = $checkRoot
$start.Environment['TMP'] = $checkRoot
$start.Environment['PATH'] = 'C:/Windows/System32'
$start.Environment['PYTHONPATH'] = $snapshot + '/src'
$start.Environment['PONTIUS_GIT'] = 'C:/Program Files/Git/cmd/git.exe'
$start.Environment['PYTHONNOUSERSITE'] = '1'
$start.Environment['PYTHONDONTWRITEBYTECODE'] = '1'
$process = [System.Diagnostics.Process]::new()
$process.StartInfo = $start
$watch = [System.Diagnostics.Stopwatch]::StartNew()
if (-not $process.Start()) { throw 'process start failed' }
$outTask = $process.StandardOutput.ReadToEndAsync()
$errTask = $process.StandardError.ReadToEndAsync()
$process.WaitForExit()
$out = $outTask.GetAwaiter().GetResult()
$err = $errTask.GetAwaiter().GetResult()
$watch.Stop()
$logPath = $checkRoot + '/cold-a-record-preservation-' + $Slot + '.log'
$log = $out + $err + "`nEXIT_CODE=" + $process.ExitCode + "`nELAPSED_SECONDS=" + $watch.Elapsed.TotalSeconds + "`n"
$bytes = [System.Text.UTF8Encoding]::new($false).GetBytes($log.Replace("`r`n", "`n"))
$stream = [System.IO.File]::Open($logPath,[System.IO.FileMode]::CreateNew,[System.IO.FileAccess]::Write,[System.IO.FileShare]::None)
try { $stream.Write($bytes,0,$bytes.Length) } finally { $stream.Dispose() }
Write-Output $log
Write-Output ('LOG_SHA256=' + (Get-FileHash -LiteralPath $logPath -Algorithm SHA256).Hash)
exit $process.ExitCode
