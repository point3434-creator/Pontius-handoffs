$ErrorActionPreference = 'Stop'
$taskRoot = 'D:\Pontius\tmp\v0a-hand-adapter-open-r001'
$primary = 'D:\Pontius'
$work = Join-Path $taskRoot 'authoring'
$packet = Join-Path $taskRoot 'packets\r001'
$gitExe = 'C:\Program Files\Git\cmd\git.exe'
$base = '7a387e995e3b37232d2379332927247a4d49c64e'
$candidate = '36c31477d87028aeec31339d28ccc089ffcaa31d'
$tree = '67d0e61c2cce8cba2c6e2ff759c24f432d50ac04'
$manifest = '83814f33a6f7f64b99da7bedfaaa81e61712c083d8f0ecf55a79f0f9a22f142c'
$hooks = Join-Path $taskRoot 'primary-explicit-push-hooks'
$paths = @('STATUS.md','docs/decisions/ADR-0493-open-the-one-hand-file-adapter-source-round.md','docs/architecture/v0a-hand-adapter-r002/brief.md','docs/architecture/v0a-hand-adapter-r002/design.md','docs/architecture/v0a-hand-adapter-r002/source-opening-draft.md')
if (Test-Path -LiteralPath $hooks) { throw 'Primary integration already started; inspect before resuming' }
function Require([bool]$ok,[string]$message) { if (-not $ok) { throw $message } }
function Digest([byte[]]$bytes) { [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant() }
function GitRaw([string]$repo,[string[]]$arguments) {
    $info = [Diagnostics.ProcessStartInfo]::new()
    $info.FileName = $gitExe
    $info.UseShellExecute = $false
    $info.RedirectStandardOutput = $true
    $info.RedirectStandardError = $true
    foreach ($key in @($info.Environment.Keys)) {
        if ($key.StartsWith('GIT_',[StringComparison]::OrdinalIgnoreCase)) { $info.Environment.Remove($key) | Out-Null }
    }
    $prefix = @('--no-replace-objects','-c',"safe.directory=$($repo.Replace('\','/'))",'-c',"safe.directory=$($primary.Replace('\','/'))/.git",'-c','core.autocrlf=false','-c',"core.hooksPath=$hooks",'-C',$repo)
    foreach ($arg in ($prefix + $arguments)) { $info.ArgumentList.Add($arg) }
    $process = [Diagnostics.Process]::Start($info)
    $buffer = [IO.MemoryStream]::new()
    $stderr = $process.StandardError.ReadToEndAsync()
    $process.StandardOutput.BaseStream.CopyTo($buffer)
    $process.WaitForExit()
    if ($process.ExitCode -ne 0) { throw "Git $($arguments[0]) failed: $($stderr.Result)" }
    return ,$buffer.ToArray()
}
function GitText([string]$repo,[string[]]$arguments) { [Text.Encoding]::UTF8.GetString((GitRaw $repo $arguments)).TrimEnd("`r","`n") }
function RemoteMaster {
    $rows = GitText $primary @('ls-remote','origin','refs/heads/master')
    Require ($rows -and -not $rows.Contains("`n")) 'Primary remote absent or ambiguous'
    ($rows -split "`t")[0]
}
function CheckReceipts([string]$phase) {
    foreach ($slot in @('311','314')) {
        foreach ($check in @('status','tests')) {
            $records = @(Get-Content -Raw -LiteralPath "$taskRoot\run-records\$phase-$check-$slot.json" | ConvertFrom-Json)
            Require ($records.Count -eq 2 -and @($records | Where-Object { $_.exit_code -ne 0 }).Count -eq 0) 'Metadata acceptance failed/missing'
            $version = if ($slot -eq '311') { '3.11.15 ' } else { '3.14.6 ' }
            Require ($records[0].stdout.StartsWith($version)) 'Wrong interpreter'
            if ($check -eq 'tests') {
                Require ($records[-1].stderr -match 'Ran 12 tests in' -and $records[-1].stderr.TrimEnd().EndsWith('OK')) 'Test count/status mismatch'
            } else { Require ($records[-1].stdout.TrimEnd() -eq 'STATUS.md is current') 'Generated status mismatch' }
            foreach ($path in $paths) {
                Require ((Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $records[-1].snapshot $path)).Hash -eq (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $packet "files\$path")).Hash) 'Verified snapshot drift'
            }
        }
    }
}
Require ((GitText $primary @('remote','get-url','origin')) -eq 'https://github.com/point3434-creator/Pontius.git') 'Wrong primary origin'
Require ((GitText $primary @('rev-parse','HEAD')) -eq $base) 'Primary base changed'
Require ((GitText $primary @('branch','--show-current')) -eq 'master') 'Primary branch changed'
Require (-not (GitText $primary @('status','--porcelain','--untracked-files=no'))) 'Primary tracked/index dirty'
Require ((RemoteMaster) -eq $base) 'Primary remote changed'
Require ((GitText $work @('rev-parse',"${candidate}^{tree}")) -eq $tree) 'Candidate tree changed'
Require ((GitText $work @('rev-parse',"${candidate}^")) -eq $base) 'Candidate parent changed'
Require ((Get-FileHash -Algorithm SHA256 -LiteralPath "$packet\manifest.sha256").Hash.ToLowerInvariant() -eq $manifest) 'Manifest changed'
Require ((Get-FileHash -Algorithm SHA256 -LiteralPath "$packet\reviews\review-01-codex-metadata.md").Hash.ToLowerInvariant() -eq '02ff5989576b5fdb4fcb8c13b5d781ba0cbe9aaa195d2885ab20c2d44597bcf2') 'Issued review changed'
$actual = @((GitText $work @('diff','--no-renames','--name-only',$base,$candidate)) -split "`n")
Require (@(Compare-Object ($paths | Sort-Object) ($actual | Sort-Object)).Count -eq 0) 'Candidate scope changed'
foreach ($path in $paths) {
    Require ((Digest (GitRaw $work @('cat-file','blob',"${candidate}:$path"))) -eq (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $packet "files\$path")).Hash.ToLowerInvariant()) 'Candidate raw bytes changed'
}
foreach ($path in @((GitText $work @('diff','--name-only','--diff-filter=A',$base,$candidate)) -split "`n")) {
    Require (-not (Test-Path -LiteralPath (Join-Path $primary $path))) "New-path collision: $path"
}
CheckReceipts 'authorized'
$priorStatus = Digest (GitRaw $primary @('status','--porcelain=v1','-z','--untracked-files=normal'))
New-Item -ItemType Directory -Path $hooks | Out-Null
foreach ($path in $paths) {
    $to = Join-Path $primary $path
    New-Item -ItemType Directory -Force (Split-Path -Parent $to) | Out-Null
    Copy-Item -LiteralPath (Join-Path $packet "files\$path") -Destination $to
}
GitText $primary (@('add','--') + $paths) | Out-Null
Require ((GitText $primary @('write-tree')) -eq $tree) 'Staged tree differs from authorization'
GitText $primary @('diff','--cached','--check') | Out-Null
GitText $primary @('commit','-m','Open the one-hand file adapter source round','-m',"Controller-authorized candidate $candidate; exact reviewed tree $tree; manifest $manifest. ADR-0493 source opening only. Separate archive/handoff publication remains pending explicit transfer approval.") | Out-Null
$decision = GitText $primary @('rev-parse','HEAD')
Require ((GitText $primary @('rev-parse','HEAD^')) -eq $base) 'Decision parent mismatch'
Require ((GitText $primary @('rev-parse','HEAD^{tree}')) -eq $tree) 'Decision tree mismatch'
$result = [ordered]@{decision_commit=$decision;candidate=$candidate;base=$base;tree=$tree;manifest_sha256=$manifest;paths=$paths;primary_pushed=$false;handoff_publication='pending explicit transfer approval';operating_authority=$false;prior_status_sha256=$priorStatus}
$resultPath = Join-Path $taskRoot 'primary-integration-result.json'
[IO.File]::WriteAllText($resultPath,($result | ConvertTo-Json -Depth 5)+"`n",[Text.UTF8Encoding]::new($false))
"Decision created locally: $decision; verifying exact commit before explicit push"
GitText $work @('fetch','--no-tags',$primary,"${decision}:refs/heads/verification/v0a-hand-adapter-open-adoption") | Out-Null
foreach ($slot in @('311','314')) {
    & (Join-Path $taskRoot 'run-snapshot.ps1') -RunName primary-postcommit-status -Slot $slot -Candidate $decision -Overlay (Join-Path $packet 'files') -PythonArgs @('-m','pontius.status_generation','--check')
    & (Join-Path $taskRoot 'run-snapshot.ps1') -RunName primary-postcommit-tests -Slot $slot -Candidate $decision -Overlay (Join-Path $packet 'files') -PythonArgs @('tests/test_status_generation.py')
}
CheckReceipts 'primary-postcommit'
Require ((GitText $primary @('rev-parse','HEAD')) -eq $decision) 'Primary moved during verification'
Require (-not (GitText $primary @('status','--porcelain','--untracked-files=no'))) 'Primary tracked state changed'
Require ((Digest (GitRaw $primary @('status','--porcelain=v1','-z','--untracked-files=normal'))) -eq $priorStatus) 'Pre-existing untracked population changed'
Require ((RemoteMaster) -eq $base) 'Primary remote moved during verification'
GitText $primary @('push','origin','master:refs/heads/master') | Out-Null
Require ((RemoteMaster) -eq $decision) 'Primary push unconfirmed'
$result.primary_pushed = $true
$result.postcommit_checks = 'CPython 3.11.15 then 3.14.6; status current; 12 tests each; exact reviewed tree'
$result.final_status_sha256 = Digest (GitRaw $primary @('status','--porcelain=v1','-z','--untracked-files=normal'))
[IO.File]::WriteAllText($resultPath,($result | ConvertTo-Json -Depth 5)+"`n",[Text.UTF8Encoding]::new($false))
$result | ConvertTo-Json -Depth 5
