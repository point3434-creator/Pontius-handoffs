# Run only after final combined snapshot generation; no source or capability writer.
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$SnapshotRoot,
    [Parameter(Mandatory = $true)][ValidateSet('3.11.15', '3.14.6')][string]$ExpectedVersion,
    [Parameter(Mandatory = $true)][string]$TempRoot,
    [Parameter(Mandatory = $true)][string]$OutputPath
)
$ErrorActionPreference = 'Stop'
function Assert-NoReparseDirectoryAncestors([string]$DirectoryPath) {
    $cDirectory = [IO.DirectoryInfo]::new($DirectoryPath)
    while ($null -ne $cDirectory) {
        $cDirectory.Refresh()
        if (-not $cDirectory.Exists) { throw 'Required directory no longer exists' }
        if (($cDirectory.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
            throw ('Reparse directory is outside this launcher scope: ' + $cDirectory.FullName)
        }
        $cDirectory = $cDirectory.Parent
    }
}
if ($PSVersionTable.PSVersion.Major -lt 7) { throw 'PowerShell 7 is required' }
foreach ($cPath in @($SnapshotRoot, $TempRoot, $OutputPath)) {
    if (-not [IO.Path]::IsPathRooted($cPath)) { throw 'All paths must be absolute' }
}
$cRoot = (Resolve-Path -LiteralPath $SnapshotRoot).Path
$cTemp = (Resolve-Path -LiteralPath $TempRoot).Path
$cOutput = [IO.Path]::GetFullPath($OutputPath)
$cOutputParent = [IO.Path]::GetDirectoryName($cOutput)
Assert-NoReparseDirectoryAncestors $cRoot
Assert-NoReparseDirectoryAncestors $cTemp
Assert-NoReparseDirectoryAncestors $cOutputParent
if ($cOutput.StartsWith($cRoot.TrimEnd('\') + '\', [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Inspection output must remain outside the source snapshot'
}
if (Test-Path -LiteralPath $cOutput) { throw 'Inspection output already exists; use a new name' }
if (-not (Test-Path -LiteralPath ([IO.Path]::GetDirectoryName($cOutput)))) {
    throw 'Output parent directory must already exist'
}
$cPython = if ($ExpectedVersion -eq '3.11.15') {
    'D:\Pontius-tools\py311\Scripts\python.exe'
} else {
    'D:\Pontius\.venv\Scripts\python.exe'
}
$cStart = [Diagnostics.ProcessStartInfo]::new()
$cStart.FileName = $cPython
$cStart.WorkingDirectory = $cRoot
$cStart.UseShellExecute = $false
$cStart.CreateNoWindow = $true
$cStart.WindowStyle = [Diagnostics.ProcessWindowStyle]::Hidden
$cStart.RedirectStandardOutput = $true
$cStart.RedirectStandardError = $true
$cStart.Environment.Clear()
foreach ($cKey in @('SYSTEMROOT', 'WINDIR', 'COMSPEC')) {
    $cValue = [Environment]::GetEnvironmentVariable($cKey)
    if ($null -ne $cValue) { $cStart.Environment[$cKey] = $cValue }
}
$cStart.Environment['PATH'] = Join-Path $cStart.Environment['SYSTEMROOT'] 'System32'
$cStart.Environment['TEMP'] = $cTemp
$cStart.Environment['TMP'] = $cTemp
$cStart.Environment['PYTHONPATH'] = Join-Path $cRoot 'src'
$cStart.Environment['PONTIUS_GIT'] = 'C:\Program Files\Git\cmd\git.exe'
$cStart.Environment['GIT_CONFIG_NOSYSTEM'] = '1'
$cStart.Environment['GIT_CONFIG_GLOBAL'] = 'NUL'
foreach ($cArgument in @(
    '-B', '-P', (Join-Path $PSScriptRoot 'slice-c-inspect-test-census.py'),
    '--snapshot', $cRoot, '--expected-version', $ExpectedVersion
)) { $cStart.ArgumentList.Add($cArgument) }
$cProcess = [Diagnostics.Process]::new()
$cProcess.StartInfo = $cStart
try {
    if (-not $cProcess.Start()) { throw 'Census process did not start' }
    $cStdoutTask = $cProcess.StandardOutput.ReadToEndAsync()
    $cStderrTask = $cProcess.StandardError.ReadToEndAsync()
    $cProcess.WaitForExit()
    $cStdout = $cStdoutTask.GetAwaiter().GetResult()
    $cStderr = $cStderrTask.GetAwaiter().GetResult()
    if ($cProcess.ExitCode -ne 0) {
        throw ('Read-only census refused, exit ' + $cProcess.ExitCode + ': ' + $cStderr)
    }
    if ($cStderr.Length -ne 0) { throw ('Unexpected census stderr: ' + $cStderr) }
    $null = ConvertFrom-Json -InputObject $cStdout
    $cBytes = [Text.UTF8Encoding]::new($false).GetBytes($cStdout.Replace("`r`n", "`n"))
    Assert-NoReparseDirectoryAncestors $cOutputParent
    $cStream = [IO.File]::Open(
        $cOutput, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None
    )
    try { $cStream.Write($cBytes, 0, $cBytes.Length) } finally { $cStream.Dispose() }
    Get-FileHash -LiteralPath $cOutput -Algorithm SHA256
} finally {
    $cProcess.Dispose()
}
