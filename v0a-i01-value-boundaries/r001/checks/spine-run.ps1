param([Parameter(Mandatory=$true)][string]$Interpreter,[Parameter(Mandatory=$true)][string]$Version,[Parameter(Mandatory=$true)][string]$Receipt)
$ErrorActionPreference = 'Stop'
$packet = 'D:\Pontius-handoffs\v0a-i01-value-boundaries\r001'
$root = 'D:\pontius-snapshots\v0a-values-spine-621bb1725663439baa809b694e3a2f07\harness'
$probe = Join-Path $packet 'checks\spine-boundary-probe.py'
$info = [System.Diagnostics.ProcessStartInfo]::new()
$info.FileName = $Interpreter
$info.WorkingDirectory = $root
$info.UseShellExecute = $false
$info.CreateNoWindow = $true
$info.RedirectStandardOutput = $true
$info.RedirectStandardError = $true
$info.Environment.Clear()
foreach ($entry in @{
    SystemRoot = 'C:\Windows'; WINDIR = 'C:\Windows'
    TEMP = 'C:\Users\point\AppData\Local\Temp'; TMP = 'C:\Users\point\AppData\Local\Temp'
    PYTHONPATH = ($root + '\src'); PYTHONDONTWRITEBYTECODE = '1'; PYTHONNOUSERSITE = '1'; PYTHONUTF8 = '1'
    PONTIUS_GIT = 'C:/Program Files/Git/cmd/git.exe'
}.GetEnumerator()) { $info.Environment[$entry.Key] = $entry.Value }
foreach ($item in @('-B', '-P', $probe, $Interpreter, $Version)) { [void]$info.ArgumentList.Add($item) }
$receiptStream = [System.IO.File]::Open($Receipt, [System.IO.FileMode]::CreateNew, [System.IO.FileAccess]::Write)
try {
    $process = [System.Diagnostics.Process]::new()
    $process.StartInfo = $info
    [void]$process.Start()
    $stdoutTask = $process.StandardOutput.ReadToEndAsync()
    $stderrTask = $process.StandardError.ReadToEndAsync()
    $process.WaitForExit()
    $stdout = $stdoutTask.GetAwaiter().GetResult()
    $stderr = $stderrTask.GetAwaiter().GetResult()
    $text = "COMMAND=$Interpreter -B -P $probe $Interpreter $Version`nCWD=$root`nPROBE_SHA256=$((Get-FileHash -LiteralPath $probe -Algorithm SHA256).Hash.ToLowerInvariant())`nRUNNER_SHA256=$((Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant())`nSTDOUT`n$stdout`nSTDERR`n$stderr`nEXIT_CODE=$($process.ExitCode)`n"
    $text = $text.Replace("`r`n", "`n")
    $bytes = [System.Text.UTF8Encoding]::new($false).GetBytes($text)
    $receiptStream.Write($bytes, 0, $bytes.Length)
    Write-Output $text
    if ($process.ExitCode -ne 0) { throw "Diagnostic failed with exit $($process.ExitCode)" }
} finally { $receiptStream.Dispose() }