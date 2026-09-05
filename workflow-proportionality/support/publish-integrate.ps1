$ErrorActionPreference = 'Stop'
$gitExe = 'C:\Program Files\Git\cmd\git.exe'
$primary = 'D:\Pontius'
$handoffs = 'D:\Pontius-handoffs'
$taskRoot = 'D:\Pontius\tmp\workflow-proportionality-r001'
$stage = Join-Path $taskRoot 'publication-staging'
$work = Join-Path $taskRoot 'authoring'
$packet = Join-Path $taskRoot 'packets\r001'
$base = '53773cb9e7489d8cfa32b4e0ceadea37c5980023'
$candidate = '922398389870ba9dc378eb096363de3b1bb3731c'
$tree = '68c961452a7adad21beddf85b4e2486b30664769'
$handBase = '90cc0bad585b3944cebc38e871f89570032df2fe'
$archive = 'refs/heads/archive/workflow-proportionality/r001'
$hooks = Join-Path $taskRoot 'authorized-empty-hooks'
if (Test-Path -LiteralPath $hooks) { throw 'Execution already started; inspect before resuming' }

function GitRaw([string]$repo,[string[]]$arguments) {
    $info = [Diagnostics.ProcessStartInfo]::new()
    $info.FileName = $gitExe
    $info.UseShellExecute = $false
    $info.RedirectStandardOutput = $true
    $info.RedirectStandardError = $true
    foreach ($key in @($info.Environment.Keys)) {
        if ($key.StartsWith('GIT_',[StringComparison]::OrdinalIgnoreCase)) {
            $info.Environment.Remove($key) | Out-Null
        }
    }
    $prefix = @('-c',"safe.directory=$($repo.Replace('\','/'))",'-c',
        "safe.directory=$($work.Replace('\','/'))",'-c',
        "safe.directory=$($work.Replace('\','/'))/.git",'-c',
        "safe.directory=$($primary.Replace('\','/'))/.git",'-c',
        'core.autocrlf=false','-c',"core.hooksPath=$hooks",'-C',$repo)
    foreach ($arg in ($prefix + $arguments)) { $info.ArgumentList.Add($arg) }
    $process = [Diagnostics.Process]::Start($info)
    $bytes = [IO.MemoryStream]::new()
    $errorText = $process.StandardError.ReadToEndAsync()
    $process.StandardOutput.BaseStream.CopyTo($bytes)
    $process.WaitForExit()
    if ($process.ExitCode -ne 0) { throw "Git $($arguments[0]) failed: $($errorText.Result)" }
    return ,$bytes.ToArray()
}
function GitText([string]$repo,[string[]]$arguments) {
    [Text.Encoding]::UTF8.GetString((GitRaw $repo $arguments)).TrimEnd("`r","`n")
}
function Require([bool]$condition,[string]$message) { if (-not $condition) { throw $message } }
function RemoteHead([string]$repo,[string]$ref) {
    $rows = GitText $repo @('ls-remote','origin',$ref)
    if (-not $rows) { return '' }
    Require (-not $rows.Contains("`n")) 'Ambiguous remote ref'
    ($rows -split "`t")[0]
}
function Digest([byte[]]$bytes) {
    [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant()
}
function CheckReceipts([string]$prefix) {
    foreach ($slot in @('311','314')) {
        foreach ($name in @('status','tests')) {
            $records = @(Get-Content -Raw -LiteralPath "$taskRoot\run-records\$prefix-$name-$slot.json" | ConvertFrom-Json)
            Require ($records.Count -eq 2 -and @($records | Where-Object {$_.exit_code -ne 0}).Count -eq 0) 'Checks missing or failed'
            $version = if ($slot -eq '311') { '3.11.15 ' } else { '3.14.6 ' }
            Require ($records[0].stdout.StartsWith($version)) 'Wrong interpreter'
            if ($name -eq 'tests') {
                Require ($records[-1].stderr -match 'Ran 12 tests in' -and $records[-1].stderr.TrimEnd().EndsWith('OK')) 'Test result mismatch'
            } else { Require ($records[-1].stdout.TrimEnd() -eq 'STATUS.md is current') 'Status mismatch' }
            foreach ($path in $sourcePaths) {
                Require ((Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $records[-1].snapshot $path)).Hash -eq (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $packet "files\$path")).Hash) 'Snapshot drift'
            }
        }
    }
}

Require ((GitText $primary @('remote','get-url','origin')) -eq 'https://github.com/point3434-creator/Pontius.git') 'Wrong primary origin'
Require ((GitText $handoffs @('remote','get-url','origin')) -eq 'https://github.com/point3434-creator/Pontius-handoffs.git') 'Wrong handoff origin'
Require ((GitText $primary @('rev-parse','HEAD')) -eq $base) 'Primary base changed'
Require ((GitText $primary @('branch','--show-current')) -eq 'master') 'Primary branch changed'
Require (-not (GitText $primary @('status','--porcelain','--untracked-files=no'))) 'Primary dirty'
Require ((RemoteHead $primary 'refs/heads/master') -eq $base) 'Primary remote moved'
Require ((GitText $handoffs @('rev-parse','HEAD')) -eq $handBase) 'Handoff base changed'
Require ((GitText $handoffs @('branch','--show-current')) -eq 'main') 'Handoff branch changed'
Require (-not (GitText $handoffs @('status','--porcelain','--untracked-files=no'))) 'Handoff dirty'
Require ((RemoteHead $handoffs 'refs/heads/main') -eq $handBase) 'Handoff remote moved'
Require ((GitText $work @('rev-parse',"$candidate`^{tree}")) -eq $tree) 'Candidate tree changed'
Require ((GitText $work @('rev-parse',"$candidate^")) -eq $base) 'Candidate parent changed'
Require ((GitText $work @('rev-parse','refs/heads/review/workflow-proportionality/r001')) -eq $candidate) 'Review ref changed'
Require ((Get-FileHash -Algorithm SHA256 -LiteralPath "$packet\manifest.sha256").Hash.ToLowerInvariant() -eq '9c45e5069a7b0e7276e9a1e63e3b809bfc2c696a26c04f32336cb36ac8411589') 'Manifest changed'
$sourcePaths = @('CLAUDE.md','STATUS.md','docs/decisions/ADR-0492-adopt-proportionate-engineering-review.md','docs/workflow.md')
$actualSource = @((GitText $work @('diff','--no-renames','--name-only',$base,$candidate)) -split "`n")
Require (@(Compare-Object ($sourcePaths | Sort-Object) ($actualSource | Sort-Object)).Count -eq 0) 'Wrong source population'
foreach ($path in $sourcePaths) {
    $raw = GitRaw $work @('cat-file','blob',"${candidate}:$path")
    Require ((Digest $raw) -eq (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $packet "files\$path")).Hash.ToLowerInvariant()) "Packet drift: $path"
}
foreach ($path in @((GitText $work @('diff','--name-only','--diff-filter=A',$base,$candidate)) -split "`n")) {
    Require (-not (Test-Path -LiteralPath (Join-Path $primary $path))) "Primary new-file collision: $path"
}
CheckReceipts 'authorized'
$priorPrimaryStatus = Digest (GitRaw $primary @('status','--porcelain=v1','-z','--untracked-files=normal'))
Require (-not (Test-Path -LiteralPath (Join-Path $handoffs 'workflow-proportionality'))) 'Publication task collision'
$publicationFiles = @(Get-ChildItem -LiteralPath $stage -Recurse -File)
Require ($publicationFiles.Count -gt 10) 'Publication set absent'
foreach ($file in $publicationFiles) {
    Require (-not ($file.Attributes -band [IO.FileAttributes]::ReparsePoint)) 'Reparse publication input'
    $relative = [IO.Path]::GetRelativePath($stage,$file.FullName).Replace('\','/')
    Require ($relative.StartsWith('workflow-proportionality/') -or $relative -in @('.gitattributes','INDEX.md','progress.md')) 'Publication scope mismatch'
}
$existingArchive = RemoteHead $primary $archive
Require (-not $existingArchive -or $existingArchive -eq $candidate) 'Remote archive collision'
New-Item -ItemType Directory -Path $hooks | Out-Null

GitText $primary @('fetch','--no-tags',$work,"${candidate}:$archive") | Out-Null
Require ((GitText $primary @('rev-parse',$archive)) -eq $candidate) 'Local archive mismatch'
GitText $primary @('push','origin',"${archive}:$archive") | Out-Null
Require ((RemoteHead $primary $archive) -eq $candidate) 'Archive push unconfirmed'
'Candidate archive published and verified'

$publishedPaths = @()
foreach ($file in $publicationFiles) {
    $relative = [IO.Path]::GetRelativePath($stage,$file.FullName).Replace('\','/')
    $destination = Join-Path $handoffs $relative
    New-Item -ItemType Directory -Path (Split-Path $destination) -Force | Out-Null
    Copy-Item -LiteralPath $file.FullName -Destination $destination
    $publishedPaths += $relative
}
GitText $handoffs @('add','--','.gitattributes','INDEX.md','progress.md','workflow-proportionality') | Out-Null
$actual = @((GitText $handoffs @('diff','--cached','--name-only')) -split "`n")
Require (@(Compare-Object ($publishedPaths | Sort-Object) ($actual | Sort-Object)).Count -eq 0) 'Publication index scope mismatch'
foreach ($path in $publishedPaths) {
    Require ((Digest (GitRaw $handoffs @('cat-file','blob',":$path"))) -eq (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $stage $path)).Hash.ToLowerInvariant()) "Publication normalization: $path"
}
GitText $handoffs @('diff','--cached','--check','--','.gitattributes','INDEX.md','progress.md','workflow-proportionality/publication-map.md') | Out-Null
GitText $handoffs @('commit','-m','Publish proportionate workflow review packet') | Out-Null
$publicationCommit = GitText $handoffs @('rev-parse','HEAD')
Require ((GitText $handoffs @('rev-parse','HEAD^')) -eq $handBase) 'Publication parent mismatch'
GitText $handoffs @('push','origin','HEAD:refs/heads/main') | Out-Null
Require ((RemoteHead $handoffs 'refs/heads/main') -eq $publicationCommit) 'Publication push unconfirmed'
"Publication confirmed: $publicationCommit; $($publishedPaths.Count) files"

Require ((GitText $primary @('rev-parse','HEAD')) -eq $base) 'Primary moved before integration'
Require (-not (GitText $primary @('status','--porcelain','--untracked-files=no'))) 'Primary changed before integration'
foreach ($path in $sourcePaths) {
    $destination = Join-Path $primary $path
    New-Item -ItemType Directory -Path (Split-Path $destination) -Force | Out-Null
    Copy-Item -LiteralPath (Join-Path $packet "files\$path") -Destination $destination
}
GitText $primary (@('add','--') + $sourcePaths) | Out-Null
Require ((GitText $primary @('write-tree')) -eq $tree) 'Staged tree does not equal authorized tree'
GitText $primary @('diff','--cached','--check') | Out-Null
GitText $primary @('commit','-m','Adopt proportionate engineering review','-m',
    "Controller-authorized candidate $candidate; exact tree $tree. Published handoff $publicationCommit. Prospective ADR-0492 only; no operating or research authority.") | Out-Null
$decision = GitText $primary @('rev-parse','HEAD')
Require ((GitText $primary @('rev-parse','HEAD^')) -eq $base) 'Decision parent mismatch'
Require ((GitText $primary @('rev-parse','HEAD^{tree}')) -eq $tree) 'Decision tree mismatch'
$result = [ordered]@{publication_commit=$publicationCommit;published_files=$publishedPaths.Count;decision_commit=$decision;base=$base;tree=$tree;candidate=$candidate;paths=$sourcePaths;archive=$archive;operating_authority=$false;primary_pushed=$false;prior_status_sha256=$priorPrimaryStatus}
[IO.File]::WriteAllText((Join-Path $taskRoot 'integration-result.json'),($result | ConvertTo-Json -Depth 5) + "`n",[Text.UTF8Encoding]::new($false))
"Decision created locally: $decision; verifying actual commit before push"

GitText $work @('fetch','--no-tags',$primary,"${decision}:refs/heads/verification/workflow-proportionality-adoption") | Out-Null
foreach ($slot in @('311','314')) {
    & (Join-Path $taskRoot 'run-snapshot.ps1') -RunName 'postcommit-status' -Slot $slot -Candidate $decision -Overlay (Join-Path $packet 'files') -PythonArgs @('-m','pontius.status_generation','--check')
    & (Join-Path $taskRoot 'run-snapshot.ps1') -RunName 'postcommit-tests' -Slot $slot -Candidate $decision -Overlay (Join-Path $packet 'files') -PythonArgs @('tests/test_status_generation.py')
}
CheckReceipts 'postcommit'
Require ((GitText $primary @('rev-parse','HEAD')) -eq $decision) 'Primary changed during checks'
Require (-not (GitText $primary @('status','--porcelain','--untracked-files=no'))) 'Primary tracked state changed'
Require ((Digest (GitRaw $primary @('status','--porcelain=v1','-z','--untracked-files=normal'))) -eq $priorPrimaryStatus) 'Primary untracked population changed'
Require ((RemoteHead $primary 'refs/heads/master') -eq $base) 'Primary remote moved during checks'
GitText $primary @('push','origin','master:refs/heads/master') | Out-Null
Require ((RemoteHead $primary 'refs/heads/master') -eq $decision) 'Decision push unconfirmed'
Require (-not (GitText $handoffs @('status','--porcelain','--untracked-files=no'))) 'Handoff tracked state changed'
$result.primary_pushed = $true
$result.postcommit_checks = '311 then 314; status current and 12 tests each; all raw blobs match'
$result.final_status_sha256 = Digest (GitRaw $primary @('status','--porcelain=v1','-z','--untracked-files=normal'))
[IO.File]::WriteAllText((Join-Path $taskRoot 'integration-result.json'),($result | ConvertTo-Json -Depth 5) + "`n",[Text.UTF8Encoding]::new($false))
$result | ConvertTo-Json -Depth 5
