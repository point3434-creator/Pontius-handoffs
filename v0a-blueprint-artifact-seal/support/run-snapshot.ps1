param(
    [Parameter(Mandatory=$true)][string]$RunName,
    [ValidateSet('311','314')][string]$Slot = '311',
    [string]$Overlay = 'D:\Pontius\tmp\v0a-blueprint-artifact-seal-r001\authoring',
    [Parameter(Mandatory=$true)][string[]]$PythonArgs,
    [switch]$MinimumDigits,
    [ValidatePattern('^[0-9a-f]{40}$')][string]$Candidate = 'c7de23de276c50463d831f3983fede82a5400ce8'
)
$ErrorActionPreference = 'Stop'
$taskRoot = 'D:\Pontius\tmp\v0a-blueprint-artifact-seal-r001'
if ($RunName -notmatch '^[a-zA-Z0-9_-]+$') { throw 'Unsafe run name' }
$snapshot = Join-Path $taskRoot "snapshots\$RunName-$Slot"
if (Test-Path -LiteralPath $snapshot) { throw "Snapshot already exists: $snapshot" }
$gitExe = 'C:\Program Files\Git\cmd\git.exe'
$pythonExe = if ($Slot -eq '311') { 'D:\Pontius-tools\py311\Scripts\python.exe' } else { 'D:\Pontius\.venv\Scripts\python.exe' }
foreach ($executable in @($gitExe,$pythonExe)) {
    $item = Get-Item -LiteralPath $executable
    if ($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Executable is not regular/non-reparse' }
}
& $gitExe -c safe.directory=D:/Pontius/tmp/v0a-blueprint-artifact-seal-r001/authoring -c safe.directory=D:/Pontius/tmp/v0a-blueprint-artifact-seal-r001/authoring/.git clone --quiet --no-hardlinks --no-checkout (Join-Path $taskRoot 'authoring') $snapshot
if ($LASTEXITCODE -ne 0) { throw 'Snapshot clone failed' }
& $gitExe -C $snapshot -c core.autocrlf=false checkout --quiet --detach $Candidate
if ($LASTEXITCODE -ne 0) { throw 'Snapshot checkout failed' }
$paths = @('docs/decisions/ADR-0491-source-seal-the-portable-blueprint-artifact.md', 'STATUS.md')
foreach ($relative in $paths) {
    $from = Join-Path $Overlay $relative
    if (Test-Path -LiteralPath $from) {
        $to = Join-Path $snapshot $relative
        New-Item -ItemType Directory -Force (Split-Path -Parent $to) | Out-Null
        Copy-Item -LiteralPath $from -Destination $to
    }
}
$runTemp = Join-Path $taskRoot "process-temp\$RunName-$Slot"
New-Item -ItemType Directory -Force $runTemp | Out-Null
$envKeep = @('SystemRoot','WINDIR','SystemDrive','COMSPEC','USERPROFILE','APPDATA','LOCALAPPDATA')
$prefix = @('-B','-P')
if ($MinimumDigits) { $prefix += @('-X','int_max_str_digits=640') }
$expectedVersion = if ($Slot -eq '311') { '(3, 11, 15)' } else { '(3, 14, 6)' }
$identity = "import sys, pathlib, pontius.immutable_blueprint as m; assert sys.implementation.name == 'cpython'; assert sys.version_info[:3] == $expectedVersion; assert sys.flags.safe_path and sys.dont_write_bytecode; assert pathlib.Path(m.__file__).resolve() == pathlib.Path('src/pontius/immutable_blueprint.py').resolve(); print(sys.version); print(m.__file__)"
$commands = @()
$commands += ,($prefix + @('-c',$identity))
$commands += ,($prefix + $PythonArgs)
$records = @()
foreach ($argv in $commands) {
    $info = [Diagnostics.ProcessStartInfo]::new()
    $info.FileName = $pythonExe
    $info.WorkingDirectory = $snapshot
    $info.UseShellExecute = $false
    $info.RedirectStandardOutput = $true
    $info.RedirectStandardError = $true
    $info.Environment.Clear()
    foreach ($key in $envKeep) { if ([Environment]::GetEnvironmentVariable($key)) { $info.Environment[$key] = [Environment]::GetEnvironmentVariable($key) } }
    $info.Environment['TEMP'] = $runTemp
    $info.Environment['TMP'] = $runTemp
    $info.Environment['PONTIUS_GIT'] = $gitExe
    $info.Environment['PYTHONPATH'] = Join-Path $snapshot 'src'
    $info.Environment['PYTHONNOUSERSITE'] = '1'
    $info.Environment['PYTHONIOENCODING'] = 'utf-8'
    foreach ($arg in $argv) { $info.ArgumentList.Add($arg) }
    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $info
    if (-not $process.Start()) { throw 'Python start failed' }
    $stdout = $process.StandardOutput.ReadToEndAsync()
    $stderr = $process.StandardError.ReadToEndAsync()
    $process.WaitForExit()
    $record = [ordered]@{ snapshot=$snapshot; interpreter=$pythonExe; argv=$argv; exit_code=$process.ExitCode; stdout=$stdout.Result; stderr=$stderr.Result }
    $records += $record
    $record | ConvertTo-Json -Depth 6
    if ($process.ExitCode -ne 0) { break }
}
$logDir = Join-Path $taskRoot 'run-records'
New-Item -ItemType Directory -Force $logDir | Out-Null
$records | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $logDir "$RunName-$Slot.json") -Encoding utf8NoBOM
if ($records[-1].exit_code -ne 0) { throw "Python refused or failed: $($records[-1].exit_code)" }
