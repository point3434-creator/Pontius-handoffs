param([Parameter(Mandatory=$true)][string]$Version, [Parameter(Mandatory=$true)][string]$Python, [Parameter(Mandatory=$true)][string]$Label)
$ErrorActionPreference = 'Stop'
$reviewSnapshot = 'D:\Pontius-review-codex-a-r006-6c3f4d'
$reviewChecks = 'D:\Pontius-handoffs\v0a-i01-ab\r006\checks'
$reviewTemp = Join-Path $reviewSnapshot 'codex-a-temp'
[void][System.IO.Directory]::CreateDirectory($reviewTemp)
$info = [System.Diagnostics.ProcessStartInfo]::new()
$info.FileName = $Python
$info.WorkingDirectory = $reviewSnapshot
$info.UseShellExecute = $false
$info.RedirectStandardOutput = $true
$info.RedirectStandardError = $true
$info.CreateNoWindow = $true
$info.Environment.Clear()
foreach ($key in @('SystemRoot', 'WINDIR', 'COMSPEC')) { $info.Environment[$key] = [Environment]::GetEnvironmentVariable($key) }
$info.Environment['TEMP'] = $reviewTemp
$info.Environment['TMP'] = $reviewTemp
$info.Environment['PYTHONPATH'] = Join-Path $reviewSnapshot 'src'
$info.Environment['PYTHONNOUSERSITE'] = '1'
$info.Environment['PYTHONDONTWRITEBYTECODE'] = '1'
$info.Environment['PONTIUS_GIT'] = 'C:\Program Files\Git\cmd\git.exe'
foreach ($arg in @('-B', '-P', (Join-Path $reviewChecks 'codex-a-checks-v2.py'), $Version, $Python)) { $info.ArgumentList.Add($arg) }
$process = [System.Diagnostics.Process]::new()
$process.StartInfo = $info
[void]$process.Start()
$outTask = $process.StandardOutput.ReadToEndAsync()
$errTask = $process.StandardError.ReadToEndAsync()
$process.WaitForExit()
$stdout = $outTask.Result
$stderr = $errTask.Result
$receiptPath = Join-Path $reviewChecks ('codex-a-' + $Label + '.json')
if (Test-Path -LiteralPath $receiptPath) { throw 'receipt already exists' }
$receipt = @{ python=$Python; version=$Version; cwd=$reviewSnapshot; argv=@('-B','-P',(Join-Path $reviewChecks 'codex-a-checks-v2.py'),$Version,$Python); exit=$process.ExitCode; stdout=$stdout; stderr=$stderr } | ConvertTo-Json -Depth 6
[IO.File]::WriteAllText($receiptPath, $receipt.Replace("`r`n", "`n") + "`n", [Text.UTF8Encoding]::new($false))
Write-Output $receipt
exit $process.ExitCode
