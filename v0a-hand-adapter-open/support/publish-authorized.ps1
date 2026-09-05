$ErrorActionPreference = 'Stop'
$gitExe = 'C:\Program Files\Git\cmd\git.exe'
$primary = 'D:\Pontius'
$handoffs = 'D:\Pontius-handoffs'
$taskRoot = 'D:\Pontius\tmp\v0a-hand-adapter-open-r001'
$stage = Join-Path $taskRoot 'publication-staging'
$work = Join-Path $taskRoot 'authoring'
$packet = Join-Path $taskRoot 'packets\r001'
$base = '7a387e995e3b37232d2379332927247a4d49c64e'
$decision = 'abe559511a72086791ca53cd3dfec24e49ec280b'
$candidate = '36c31477d87028aeec31339d28ccc089ffcaa31d'
$tree = '67d0e61c2cce8cba2c6e2ff759c24f432d50ac04'
$handBase = '9384549401ca37de909bd2160e647fb86d389dcc'
$archive = 'refs/heads/archive/v0a-hand-adapter-open/r001'
$hooks = Join-Path $taskRoot 'publication-authorized-hooks'
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
    $prefix = @('--no-replace-objects','-c',"safe.directory=$($repo.Replace('\','/'))",'-c',
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
Require ((GitText $primary @('rev-parse','HEAD')) -eq $decision) 'Adopted primary changed'
Require ((GitText $primary @('branch','--show-current')) -eq 'master') 'Primary branch changed'
Require (-not (GitText $primary @('status','--porcelain','--untracked-files=no'))) 'Primary dirty'
Require ((RemoteHead $primary 'refs/heads/master') -eq $decision) 'Adopted primary remote changed'
Require ((GitText $handoffs @('rev-parse','HEAD')) -eq $handBase) 'Handoff base changed'
Require ((GitText $handoffs @('branch','--show-current')) -eq 'main') 'Handoff branch changed'
Require (-not (GitText $handoffs @('status','--porcelain','--untracked-files=no'))) 'Handoff dirty'
Require ((RemoteHead $handoffs 'refs/heads/main') -eq $handBase) 'Handoff remote moved'
Require ((GitText $work @('rev-parse',"$candidate`^{tree}")) -eq $tree) 'Candidate tree changed'
Require ((GitText $work @('rev-parse',"$candidate^")) -eq $base) 'Candidate parent changed'
Require ((GitText $work @('rev-parse','refs/heads/review/v0a-hand-adapter-open/r001')) -eq $candidate) 'Review ref changed'
Require ((Get-FileHash -Algorithm SHA256 -LiteralPath "$packet\manifest.sha256").Hash.ToLowerInvariant() -eq '83814f33a6f7f64b99da7bedfaaa81e61712c083d8f0ecf55a79f0f9a22f142c') 'Manifest changed'
$sourcePaths = @('STATUS.md','docs/decisions/ADR-0493-open-the-one-hand-file-adapter-source-round.md','docs/architecture/v0a-hand-adapter-r002/brief.md','docs/architecture/v0a-hand-adapter-r002/design.md','docs/architecture/v0a-hand-adapter-r002/source-opening-draft.md')
$actualSource = @((GitText $work @('diff','--no-renames','--name-only',$base,$candidate)) -split "`n")
Require (@(Compare-Object ($sourcePaths | Sort-Object) ($actualSource | Sort-Object)).Count -eq 0) 'Wrong source population'
foreach ($path in $sourcePaths) {
    $raw = GitRaw $work @('cat-file','blob',"${candidate}:$path")
    Require ((Digest $raw) -eq (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $packet "files\$path")).Hash.ToLowerInvariant()) "Packet drift: $path"
}
CheckReceipts 'primary-postcommit'
$priorPrimaryStatus = Digest (GitRaw $primary @('status','--porcelain=v1','-z','--untracked-files=normal'))
Require (-not (Test-Path -LiteralPath (Join-Path $handoffs 'v0a-hand-adapter-open'))) 'Opening publication collision'
Require (-not (Test-Path -LiteralPath (Join-Path $handoffs 'v0a-hand-adapter-design'))) 'Design publication collision'
$priorHandoffStatus = Digest (GitRaw $handoffs @('status','--porcelain=v1','-z','--untracked-files=normal'))
Require ((Get-FileHash -Algorithm SHA256 -LiteralPath "$packet\reviews\review-01-codex-metadata.md").Hash.ToLowerInvariant() -eq '02ff5989576b5fdb4fcb8c13b5d781ba0cbe9aaa195d2885ab20c2d44597bcf2') 'Issued review changed'
$publicationFiles = @(Get-ChildItem -LiteralPath $stage -Recurse -File)
Require ($publicationFiles.Count -gt 10) 'Publication set absent'
foreach ($file in $publicationFiles) {
    Require (-not ($file.Attributes -band [IO.FileAttributes]::ReparsePoint)) 'Reparse publication input'
    $relative = [IO.Path]::GetRelativePath($stage,$file.FullName).Replace('\','/')
    Require ($relative.StartsWith('v0a-hand-adapter-open/') -or $relative.StartsWith('v0a-hand-adapter-design/') -or $relative -in @('.gitattributes','INDEX.md','progress.md')) 'Publication scope mismatch'
}
$archiveSpecs = @(
    @{commit='21474e3d5b105c1709205df1eb5543417abb5a0a'; task='v0a-hand-adapter-design'; round='r001'; manifest='ce327c6982338c148d26d4d73cad978ad05b49596520449337d2cc9cb9be0bc9'},
    @{commit='1c2fde7bdb9359436f9c2ff260e324a08439752b'; task='v0a-hand-adapter-design'; round='r002'; manifest='f2c8c9f8c292585623b06a7f623e6b31f6202199f66c82afd78d765bfcab1b1a'},
    @{commit='02e24f143b8df4b2f03e8a94c58ab57905a8b2b6'; task='v0a-hand-adapter-design'; round='r003'; manifest='f730799182d3f3eda2d9efa273048b2eaf28ceeb4274ea7525df95426ca679b1'},
    @{commit=$candidate; task='v0a-hand-adapter-open'; round='r001'; manifest='83814f33a6f7f64b99da7bedfaaa81e61712c083d8f0ecf55a79f0f9a22f142c'}
)
foreach ($spec in $archiveSpecs) {
    $ref = "refs/heads/archive/$($spec.task)/$($spec.round)"
    $existing = RemoteHead $primary $ref
    Require (-not $existing -or $existing -eq $spec.commit) "Archive collision: $ref"
    $publishedPacket = Join-Path $stage "$($spec.task)/$($spec.round)"
    $id = Get-Content -Raw -LiteralPath (Join-Path $publishedPacket 'candidate.json') | ConvertFrom-Json
    Require ($id.commit -eq $spec.commit -and $id.base -eq $base -and $id.manifest_sha256 -eq $spec.manifest) 'Archive identity drift'
    Require ((GitText $work @('rev-parse',"$($spec.commit)^{tree}")) -eq $id.tree) 'Archive tree drift'
    $archivePaths = @((GitText $work @('diff','--no-renames','--name-only',$base,$spec.commit)) -split "`n")
    $expectedCount = if ($spec.task -eq 'v0a-hand-adapter-design') { 3 } else { 5 }
    Require ($archivePaths.Count -eq $expectedCount) 'Archive scope count drift'
    $rows = [Collections.Generic.List[string]]::new()
    foreach ($path in $archivePaths) {
        $bytes = GitRaw $work @('cat-file','blob',"$($spec.commit):$path")
        Require ((Digest $bytes) -eq (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $publishedPacket "files/$path")).Hash.ToLowerInvariant()) 'Archive raw file drift'
        $rows.Add("$(Digest $bytes)  $path`n")
    }
    $rows.Sort([StringComparer]::Ordinal)
    $manifestBytes = [Text.Encoding]::UTF8.GetBytes(($rows -join ''))
    Require ((Digest $manifestBytes) -eq $spec.manifest) 'Archive manifest mismatch'
    Require ((Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $publishedPacket 'manifest.sha256')).Hash.ToLowerInvariant() -eq $spec.manifest) 'Archive manifest file drift'
}
New-Item -ItemType Directory -Path $hooks | Out-Null
foreach ($spec in $archiveSpecs) {
    $ref = "refs/heads/archive/$($spec.task)/$($spec.round)"
    GitText $primary @('fetch','--no-tags',$work,"$($spec.commit):$ref") | Out-Null
    Require ((GitText $primary @('rev-parse',$ref)) -eq $spec.commit) 'Local archive mismatch'
    GitText $primary @('push','origin',"${ref}:$ref") | Out-Null
    Require ((RemoteHead $primary $ref) -eq $spec.commit) 'Archive push unconfirmed'
    "Archive published and verified: $ref"
}

$publishedPaths = @()
foreach ($file in $publicationFiles) {
    $relative = [IO.Path]::GetRelativePath($stage,$file.FullName).Replace('\','/')
    $destination = Join-Path $handoffs $relative
    New-Item -ItemType Directory -Path (Split-Path $destination) -Force | Out-Null
    Copy-Item -LiteralPath $file.FullName -Destination $destination
    $publishedPaths += $relative
}
GitText $handoffs @('add','--','.gitattributes','INDEX.md','progress.md','v0a-hand-adapter-open','v0a-hand-adapter-design') | Out-Null
$actual = @((GitText $handoffs @('diff','--cached','--name-only')) -split "`n")
Require (@(Compare-Object ($publishedPaths | Sort-Object) ($actual | Sort-Object)).Count -eq 0) 'Publication index scope mismatch'
foreach ($path in $publishedPaths) {
    Require ((Digest (GitRaw $handoffs @('cat-file','blob',":$path"))) -eq (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $stage $path)).Hash.ToLowerInvariant()) "Publication normalization: $path"
}
GitText $handoffs @('diff','--cached','--check','--','.gitattributes','INDEX.md','progress.md','v0a-hand-adapter-design/publication-map.md') | Out-Null
GitText $handoffs @('commit','-m','Publish retained hand-adapter design and opening packets') | Out-Null
$publicationCommit = GitText $handoffs @('rev-parse','HEAD')
Require ((GitText $handoffs @('rev-parse','HEAD^')) -eq $handBase) 'Publication parent mismatch'
GitText $handoffs @('push','origin','HEAD:refs/heads/main') | Out-Null
Require ((RemoteHead $handoffs 'refs/heads/main') -eq $publicationCommit) 'Publication push unconfirmed'
"Publication confirmed: $publicationCommit; $($publishedPaths.Count) files"

Require ((GitText $primary @('rev-parse','HEAD')) -eq $decision) 'Primary HEAD changed'
Require ((GitText $primary @('rev-parse','HEAD^{tree}')) -eq $tree) 'Adopted tree changed'
Require ((RemoteHead $primary 'refs/heads/master') -eq $decision) 'Primary remote changed'
Require ((Digest (GitRaw $primary @('status','--porcelain=v1','-z','--untracked-files=normal'))) -eq $priorPrimaryStatus) 'Primary working population changed'
Require (-not (GitText $handoffs @('status','--porcelain','--untracked-files=no'))) 'Handoff tracked state changed'
Require ((Digest (GitRaw $handoffs @('status','--porcelain=v1','-z','--untracked-files=normal'))) -eq $priorHandoffStatus) 'Existing handoff untracked population changed'
foreach ($spec in $archiveSpecs) {
    Require ((RemoteHead $primary "refs/heads/archive/$($spec.task)/$($spec.round)") -eq $spec.commit) 'Final archive confirmation failed'
}
$result = [ordered]@{
    publication_commit=$publicationCommit
    prior_handoff_commit=$handBase
    published_files=$publishedPaths.Count
    published_bytes=($publicationFiles | Measure-Object Length -Sum).Sum
    archives=$archiveSpecs
    decision_commit=$decision
    primary_tree=$tree
    primary_unchanged=$true
    remote_confirmed=$true
    original_primary_status_sha256=$priorPrimaryStatus
    original_handoff_status_sha256=$priorHandoffStatus
}
[IO.File]::WriteAllText((Join-Path $taskRoot 'transfer-result.json'),($result | ConvertTo-Json -Depth 6) + "`n",[Text.UTF8Encoding]::new($false))
$result | ConvertTo-Json -Depth 6

