param([Parameter(Mandatory)][string]$Label, [string]$Selection='')
$ErrorActionPreference='Stop'
$stage='D:/Pontius/tmp/eval-panel-verification'
$candidate=[IO.File]::ReadAllText((Join-Path $stage ($Label+'-commit.txt'))).Trim()
$snapshot='D:/Pontius-worktrees/eval-verification-check-'+$Label
if (Test-Path -LiteralPath $snapshot) { throw 'Refuse existing snapshot' }
git -C D:/Pontius worktree add --detach $snapshot $candidate
if ($LASTEXITCODE) { throw 'Snapshot creation failed' }
& 'C:/Users/point/.local/bin/uv.exe' sync --locked --offline --group dev --project $snapshot `
  --python 'C:/Users/point/AppData/Local/Python/pythoncore-3.14-64/python.exe'
if ($LASTEXITCODE) { throw 'Snapshot environment setup failed' }
$python=Join-Path $snapshot '.venv/Scripts/python.exe'
& $python -I -B -c 'import sys; assert sys.version_info[:3] == (3,14,6); print(sys.version)'
if ($LASTEXITCODE) { throw 'Wrong test interpreter' }
$start=[Diagnostics.ProcessStartInfo]::new()
$start.FileName=$python
$start.WorkingDirectory=$snapshot
$start.UseShellExecute=$false
$start.CreateNoWindow=$true
$start.RedirectStandardOutput=$true
$start.RedirectStandardError=$true
$start.Environment.Clear()
foreach ($name in @('SystemRoot','TEMP','TMP')) { $start.Environment[$name]=[Environment]::GetEnvironmentVariable($name) }
$start.Environment['PONTIUS_GIT']='C:/Program Files/Git/cmd/git.exe'
$start.Environment['PYTHONDONTWRITEBYTECODE']='1'
foreach ($arg in @('-B','-P','-W','error::ResourceWarning','-m','pytest','-p','no:cacheprovider',
                  '-W','error::pytest.PytestUnraisableExceptionWarning',
                  '-q','-o','pythonpath=. src tests','tests/test_pontius.py')) {
    $start.ArgumentList.Add($arg)
}
if ($Selection) { $start.ArgumentList.Add('-k'); $start.ArgumentList.Add($Selection) }
$process=[Diagnostics.Process]::Start($start)
$stdout=$process.StandardOutput.ReadToEndAsync()
$stderr=$process.StandardError.ReadToEndAsync()
$process.WaitForExit()
$out=$stdout.GetAwaiter().GetResult().Replace("`r`n","`n")
$err=$stderr.GetAwaiter().GetResult().Replace("`r`n","`n")
[IO.File]::WriteAllText((Join-Path $stage ($Label+'-stdout.txt')),$out,[Text.UTF8Encoding]::new($false))
[IO.File]::WriteAllText((Join-Path $stage ($Label+'-stderr.txt')),$err,[Text.UTF8Encoding]::new($false))
$receipt=[ordered]@{candidate=$candidate; snapshot=$snapshot; python=$python;
    version='3.14.6'; exit=$process.ExitCode; environment=@('SystemRoot','TEMP','TMP',
    'PONTIUS_GIT','PYTHONDONTWRITEBYTECODE'); arguments=@($start.ArgumentList)}
[IO.File]::WriteAllText((Join-Path $stage ($Label+'-receipt.json')),($receipt|ConvertTo-Json -Depth 4)+"`n",
                       [Text.UTF8Encoding]::new($false))
$journal=Join-Path $snapshot 'execution_journal.jsonl'
if (Test-Path -LiteralPath $journal) {
    $last=(Get-Content -LiteralPath $journal -Tail 1)
    [IO.File]::WriteAllText((Join-Path $stage ($Label+'-journal.jsonl')),$last+"`n",
                           [Text.UTF8Encoding]::new($false))
}
Write-Output $out
Write-Output $err
Write-Output ('Recorded exit '+$process.ExitCode+' for '+$candidate)
$process.Dispose()
