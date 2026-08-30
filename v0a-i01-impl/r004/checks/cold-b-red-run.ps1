param([Parameter(Mandatory=$true)][string]$Exe,[Parameter(Mandatory=$true)][string]$Version,[Parameter(Mandatory=$true)][string]$Label,[switch]$WithProbes)
$ErrorActionPreference='Stop'
$snapshot='D:\pontius-snapshots\v0a-r004-cold-b-b7262e41033a459ea8aa6bfd0ecdd54f\harness'
$checks='D:\Pontius-handoffs\v0a-i01-impl\r004\checks'
$temp=Join-Path $checks ('cold-b-temp-'+$Label)
if (Test-Path -LiteralPath $temp) { throw 'create-only temp exists' }
[System.IO.Directory]::CreateDirectory($temp) | Out-Null
$targets=@('identity')
if($WithProbes){$targets+=Join-Path $checks 'cold-b-order-red.py'}
$records=@()
foreach($target in $targets){
    $psi=[System.Diagnostics.ProcessStartInfo]::new()
    $psi.FileName=$Exe
    $psi.WorkingDirectory=$snapshot
    $psi.UseShellExecute=$false
    $psi.CreateNoWindow=$true
    $psi.RedirectStandardOutput=$true
    $psi.RedirectStandardError=$true
    $psi.Environment.Clear()
    foreach($key in @('SystemRoot','WINDIR','COMSPEC','SystemDrive')) { if([Environment]::GetEnvironmentVariable($key)){$psi.Environment[$key]=[Environment]::GetEnvironmentVariable($key)} }
    $psi.Environment['TEMP']=$temp
    $psi.Environment['TMP']=$temp
    $psi.Environment['PYTHONPATH']=Join-Path $snapshot 'src'
    $psi.Environment['PONTIUS_GIT']='C:\Program Files\Git\cmd\git.exe'
    $psi.Environment['PYTHONDONTWRITEBYTECODE']='1'
    $psi.Environment['PYTHONSAFEPATH']='1'
    $psi.Environment['PYTHONHASHSEED']='0'
    foreach($arg in @('-B','-P',(Join-Path $checks 'cold-b-bootstrap.py'),$Exe,$Version,$snapshot,$target)){$psi.ArgumentList.Add($arg)}
    $process=[System.Diagnostics.Process]::new()
    $process.StartInfo=$psi
    $timer=[System.Diagnostics.Stopwatch]::StartNew()
    if(-not $process.Start()){throw 'child did not start'}
    $stdout=$process.StandardOutput.ReadToEndAsync()
    $stderr=$process.StandardError.ReadToEndAsync()
    $process.WaitForExit()
    $timer.Stop()
    $record=[ordered]@{target=$target;exe=$Exe;expected_version=$Version;arguments=@($psi.ArgumentList);cwd=$snapshot;exit_code=$process.ExitCode;seconds=$timer.Elapsed.TotalSeconds;stdout=$stdout.Result;stderr=$stderr.Result}
    $records+=$record
    $record | ConvertTo-Json -Depth 5 -Compress
    if($process.ExitCode -ne 0){break}
}
$output=Join-Path $checks ('cold-b-'+$Label+'-receipts.json')
$bytes=[System.Text.UTF8Encoding]::new($false).GetBytes(($records | ConvertTo-Json -Depth 8)+"`n")
$stream=[System.IO.File]::Open($output,[System.IO.FileMode]::CreateNew,[System.IO.FileAccess]::Write)
try{$stream.Write($bytes,0,$bytes.Length)}finally{$stream.Dispose()}
if($records[-1].exit_code -ne 0){throw 'payload failed; see immutable receipt'}


