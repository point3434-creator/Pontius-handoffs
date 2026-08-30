param([string]$Snapshot,[string]$Slot,[string]$Commit,[string]$Mode,[string]$Name)
$ErrorActionPreference = 'Stop'
$exe = if ($Slot -eq '311') { 'D:\Pontius-tools\py311\Scripts\python.exe' } else { 'D:\Pontius\.venv\Scripts\python.exe' }
$version = if ($Slot -eq '311') { '3.11.15' } else { '3.14.6' }
$checks = 'D:\Pontius-handoffs\v0a-i01-ab\r003\checks'
$receipt = Join-Path $checks ('cold-b-' + $Slot + '-' + $Name + '.json')
if (Test-Path -LiteralPath $receipt) { throw 'Refusing to overwrite receipt' }
$psi = [Diagnostics.ProcessStartInfo]::new()
$psi.FileName = $exe
$psi.UseShellExecute = $false
$psi.CreateNoWindow = $true
$psi.WorkingDirectory = $Snapshot
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.Environment.Clear()
foreach ($key in @('SystemRoot','WINDIR','COMSPEC','TEMP','TMP')) {
  $value = [Environment]::GetEnvironmentVariable($key)
  if ($value) { $psi.Environment[$key] = $value }
}
$psi.Environment['PYTHONPATH'] = Join-Path $Snapshot 'src'
$psi.Environment['PONTIUS_GIT'] = 'C:\Program Files\Git\cmd\git.exe'
$psi.Environment['PYTHONNOUSERSITE'] = '1'
$psi.Environment['PYTHONDONTWRITEBYTECODE'] = '1'
foreach ($arg in @('-B','-P',(Join-Path $checks 'cold-b-probe-v2.py'),$Snapshot,$version,$Commit,$Mode,$receipt)) {
  $psi.ArgumentList.Add($arg)
}
$process = [Diagnostics.Process]::new()
$process.StartInfo = $psi
if (-not $process.Start()) { throw 'Payload did not start' }
$outTask = $process.StandardOutput.ReadToEndAsync()
$errTask = $process.StandardError.ReadToEndAsync()
$process.WaitForExit()
$outTask.Result
$errTask.Result
'exit=' + $process.ExitCode
