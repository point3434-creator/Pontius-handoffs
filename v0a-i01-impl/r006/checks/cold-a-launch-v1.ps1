param([Parameter(Mandatory=$true)][string]$Python, [Parameter(Mandatory=$true)][string]$Version, [Parameter(Mandatory=$true)][string]$Slot)
$ErrorActionPreference = 'Stop'
$packet = 'D:\Pontius-handoffs\v0a-i01-impl\r006\checks'
$runner = Join-Path $packet 'cold-a-runner-v1.py'
$snapshot = 'D:\pontius-snapshots\v0a-r006-cold-a-98fee7dce06d4fcca2da4475c550b928\harness'
$jobs = @(@('manifest', ''), @('suite', 'test_v0a_replay.py'), @('suite', 'test_v0a_hand_replay.py'), @('suite', 'test_v0a_trace.py'), @('suite', 'test_v0a_contract_faults.py'))
foreach ($job in $jobs) {
    $label = if ($job[0] -eq 'manifest') { 'manifest' } else { $job[1].Replace('.py','') }
    $capture = Join-Path $packet "cold-a-$Slot-$label-v1.txt"
    if (Test-Path -LiteralPath $capture) { throw "Refuse to overwrite $capture" }
    $start = [Diagnostics.ProcessStartInfo]::new()
    $start.FileName = $Python
    $start.WorkingDirectory = $snapshot
    $start.UseShellExecute = $false
    $start.CreateNoWindow = $true
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    $start.Environment.Clear()
    $start.Environment['SystemRoot'] = $env:SystemRoot
    $start.Environment['WINDIR'] = $env:WINDIR
    $start.Environment['TEMP'] = $env:TEMP
    $start.Environment['TMP'] = $env:TMP
    $start.Environment['PYTHONPATH'] = Join-Path $snapshot 'src'
    $start.Environment['PYTHONDONTWRITEBYTECODE'] = '1'
    $start.Environment['PYTHONNOUSERSITE'] = '1'
    $start.Environment['PONTIUS_GIT'] = 'C:\Program Files\Git\cmd\git.exe'
    foreach ($arg in @('-B', '-P', $runner, $Python, $Version, $job[0])) { $start.ArgumentList.Add($arg) }
    if ($job[1]) { $start.ArgumentList.Add($job[1]) }
    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $start
    [void]$process.Start()
    $stdoutTask = $process.StandardOutput.ReadToEndAsync()
    $stderrTask = $process.StandardError.ReadToEndAsync()
    $process.WaitForExit()
    $stdout = $stdoutTask.GetAwaiter().GetResult()
    $stderr = $stderrTask.GetAwaiter().GetResult()
    $text = "argv=$($start.ArgumentList -join ' | ')`nexit=$($process.ExitCode)`nstdout:`n$stdout`nstderr:`n$stderr"
    [IO.File]::WriteAllText($capture, $text.Replace("`r`n", "`n"), [Text.UTF8Encoding]::new($false))
    [pscustomobject]@{Capture=$capture; Exit=$process.ExitCode; SHA256=(Get-FileHash -LiteralPath $capture -Algorithm SHA256).Hash; Stderr=$stderr.Trim() } | ConvertTo-Json -Compress
    if ($process.ExitCode -ne 0) { throw "Failed $label on $Slot" }
}
