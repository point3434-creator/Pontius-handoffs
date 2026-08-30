param([Parameter(Mandatory=$true)][string]$Python, [Parameter(Mandatory=$true)][string]$Script, [Parameter(Mandatory=$true)][string]$Label, [string]$ExpectedVersion='3.11.15')
$ErrorActionPreference='Stop'
$snapshot='D:\Pontius-review-snapshots\v0a-i01-ab-r004-cold-b-8b743e9f'
$checks='D:\Pontius-handoffs\v0a-i01-ab\r004\checks'
$receipt=Join-Path $checks ($Label+'.json')
if(Test-Path -LiteralPath $receipt){throw 'Receipt already exists'}
$info=[System.Diagnostics.ProcessStartInfo]::new()
$info.FileName=$Python
$info.Arguments='-B -P "'+$Script+'"'
$info.WorkingDirectory=$snapshot
$info.UseShellExecute=$false
$info.CreateNoWindow=$true
$info.RedirectStandardOutput=$true
$info.RedirectStandardError=$true
$info.EnvironmentVariables.Clear()
foreach($name in @('SystemRoot','WINDIR','TEMP','TMP','COMSPEC')){
 $value=[Environment]::GetEnvironmentVariable($name)
 if($null -ne $value){$info.EnvironmentVariables[$name]=$value}
}
$info.EnvironmentVariables['PATH']=''
$info.EnvironmentVariables['PYTHONPATH']=Join-Path $snapshot 'src'
$info.EnvironmentVariables['PONTIUS_GIT']='C:\Program Files\Git\cmd\git.exe'
$info.EnvironmentVariables['COLD_B_EXPECTED_VERSION']=$ExpectedVersion
$start=[DateTime]::UtcNow.ToString('o')
$process=[System.Diagnostics.Process]::new()
$process.StartInfo=$info
if(-not $process.Start()){throw 'Python did not start'}
$outTask=$process.StandardOutput.ReadToEndAsync()
$errTask=$process.StandardError.ReadToEndAsync()
$process.WaitForExit()
$stdout=$outTask.Result
$stderr=$errTask.Result
$record=[ordered]@{label=$Label;start_utc=$start;end_utc=[DateTime]::UtcNow.ToString('o');executable=$Python;arguments=$info.Arguments;cwd=$snapshot;environment=[ordered]@{};script_sha256=(Get-FileHash -LiteralPath $Script -Algorithm SHA256).Hash.ToLowerInvariant();exit_code=$process.ExitCode;stdout=$stdout;stderr=$stderr}
foreach($name in $info.EnvironmentVariables.Keys){$record.environment[$name]=$info.EnvironmentVariables[$name]}
[IO.File]::WriteAllText($receipt,($record|ConvertTo-Json -Depth 12)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output $stdout
if($stderr){Write-Output $stderr}
Write-Output ('EXIT '+$process.ExitCode+' RECEIPT '+$receipt)
exit $process.ExitCode
