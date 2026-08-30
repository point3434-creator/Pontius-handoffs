param([string]$Exe,[string]$Version,[string]$Payload,[string]$Receipt)
$ErrorActionPreference='Stop'
$coldSnapshot='D:\pontius-snapshots\v0a-r005-cold-b-e6ac13a682804562a53621e8fab883e1\harness'
$coldPsi=[Diagnostics.ProcessStartInfo]::new()
$coldPsi.FileName=$Exe
$coldPsi.Arguments='-B -P "'+$Payload+'" "'+$Exe+'" "'+$Version+'"'
$coldPsi.WorkingDirectory=$coldSnapshot
$coldPsi.UseShellExecute=$false
$coldPsi.CreateNoWindow=$true
$coldPsi.RedirectStandardOutput=$true
$coldPsi.RedirectStandardError=$true
$coldPsi.EnvironmentVariables.Clear()
foreach ($coldKey in @('SystemRoot','WINDIR','TEMP','TMP','COMSPEC')) {
  $coldValue=[Environment]::GetEnvironmentVariable($coldKey)
  if ($null -ne $coldValue) {$coldPsi.EnvironmentVariables[$coldKey]=$coldValue}
}
$coldPsi.EnvironmentVariables['PYTHONPATH']=$coldSnapshot+'\src'
$coldPsi.EnvironmentVariables['PONTIUS_GIT']='C:\Program Files\Git\cmd\git.exe'
$coldPsi.EnvironmentVariables['PYTHONIOENCODING']='utf-8'
$coldPsi.EnvironmentVariables['PYTHONUTF8']='1'
$coldProcess=[Diagnostics.Process]::new()
$coldProcess.StartInfo=$coldPsi
[void]$coldProcess.Start()
$coldOutTask=$coldProcess.StandardOutput.ReadToEndAsync()
$coldErrTask=$coldProcess.StandardError.ReadToEndAsync()
$coldProcess.WaitForExit()
$coldOut=$coldOutTask.Result
$coldErr=$coldErrTask.Result
$coldRecord=[ordered]@{executable=$Exe;version=$Version;arguments=$coldPsi.Arguments;cwd=$coldSnapshot;environment=[ordered]@{};exit_code=$coldProcess.ExitCode;stdout=$coldOut;stderr=$coldErr}
foreach ($coldKey in $coldPsi.EnvironmentVariables.Keys) {$coldRecord.environment[$coldKey]=$coldPsi.EnvironmentVariables[$coldKey]}
$coldJson=($coldRecord | ConvertTo-Json -Depth 6).Replace("`r`n","`n")+"`n"
$coldBytes=[Text.UTF8Encoding]::new($false).GetBytes($coldJson)
$coldStream=[IO.File]::Open($Receipt,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {$coldStream.Write($coldBytes,0,$coldBytes.Length)} finally {$coldStream.Dispose()}
Write-Output $coldOut
if ($coldErr) {Write-Output $coldErr}
Write-Output ('PAYLOAD_EXIT='+$coldProcess.ExitCode)
if ($coldProcess.ExitCode -ne 0) {exit $coldProcess.ExitCode}
