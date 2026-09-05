$ErrorActionPreference = 'Stop'
$root = 'D:\Pontius-handoffs'
$taskRoot = 'D:\Pontius\tmp\workflow-proportionality-r001'
$stage = Join-Path $taskRoot 'adoption-staging'
$gitExe = 'C:\Program Files\Git\cmd\git.exe'
$integration = Get-Content -Raw -LiteralPath (Join-Path $taskRoot 'integration-result.json') | ConvertFrom-Json
if (-not $integration.primary_pushed) { throw 'Primary push not verified' }
function GitText([string]$repo,[string[]]$arguments) {
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
    $prefix = @('-c',"safe.directory=$($repo.Replace('\','/'))",'-c','core.autocrlf=false',
        '-c',"core.hooksPath=$taskRoot/authorized-empty-hooks",'-C',$repo)
    foreach ($arg in ($prefix + $arguments)) { $info.ArgumentList.Add($arg) }
    $process = [Diagnostics.Process]::Start($info)
    $stdout = $process.StandardOutput.ReadToEndAsync()
    $stderr = $process.StandardError.ReadToEndAsync()
    $process.WaitForExit()
    if ($process.ExitCode -ne 0) { throw "Git $($arguments[0]) failed: $($stderr.Result)" }
    $stdout.Result.TrimEnd("`r","`n")
}
function Require([bool]$condition,[string]$message) { if (-not $condition) { throw $message } }
function RemoteHead([string]$repo,[string]$ref) {
    $rows = GitText $repo @('ls-remote','origin',$ref)
    Require ($rows -and -not $rows.Contains("`n")) 'Remote ref absent or ambiguous'
    ($rows -split "`t")[0]
}
Require ((GitText $root @('remote','get-url','origin')) -eq 'https://github.com/point3434-creator/Pontius-handoffs.git') 'Wrong handoff origin'
Require ((GitText $root @('rev-parse','HEAD')) -eq $integration.publication_commit) 'Handoff base changed'
Require ((GitText $root @('branch','--show-current')) -eq 'main') 'Handoff branch changed'
Require (-not (GitText $root @('status','--porcelain','--untracked-files=no'))) 'Handoff dirty'
Require ((RemoteHead $root 'refs/heads/main') -eq $integration.publication_commit) 'Handoff remote moved'
Require ((GitText 'D:\Pontius' @('rev-parse','HEAD')) -eq $integration.decision_commit) 'Primary moved'
Require ((RemoteHead 'D:\Pontius' 'refs/heads/master') -eq $integration.decision_commit) 'Primary push mismatch'
$paths = @()
foreach ($file in (Get-ChildItem -LiteralPath $stage -Recurse -File)) {
    Require (-not ($file.Attributes -band [IO.FileAttributes]::ReparsePoint)) 'Reparse input'
    $relative = [IO.Path]::GetRelativePath($stage,$file.FullName).Replace('\','/')
    Require ($relative.StartsWith('workflow-proportionality/r001/') -or $relative -in @('INDEX.md','progress.md')) 'Adoption scope mismatch'
    $to = Join-Path $root $relative
    Require ($relative -in @('INDEX.md','progress.md') -or -not (Test-Path -LiteralPath $to)) 'Adoption record collision'
    $paths += $relative
}
Require ($paths.Count -eq 9) 'Unexpected adoption file population'
foreach ($path in $paths) {
    $to = Join-Path $root $path
    New-Item -ItemType Directory -Path (Split-Path $to) -Force | Out-Null
    Copy-Item -LiteralPath (Join-Path $stage $path) -Destination $to
}
GitText $root (@('add','--') + $paths) | Out-Null
$actual = (GitText $root @('diff','--cached','--name-only')) -split "`n"
Require (@(Compare-Object ($paths | Sort-Object) ($actual | Sort-Object)).Count -eq 0) 'Staged scope mismatch'
foreach ($path in $paths) {
    Require ((GitText $root @('hash-object','--no-filters',"$stage/$path")) -eq (GitText $root @('rev-parse',":$path"))) "Staged byte normalization: $path"
}
GitText $root @('diff','--cached','--check','--','INDEX.md','progress.md','workflow-proportionality/r001/adoption-result.md') | Out-Null
GitText $root @('commit','-m','Record proportionate workflow adoption') | Out-Null
$commit = GitText $root @('rev-parse','HEAD')
Require ((GitText $root @('rev-parse','HEAD^')) -eq $integration.publication_commit) 'Adoption parent mismatch'
GitText $root @('push','origin','HEAD:refs/heads/main') | Out-Null
Require ((RemoteHead $root 'refs/heads/main') -eq $commit) 'Adoption push unconfirmed'
Require (-not (GitText $root @('status','--porcelain','--untracked-files=no'))) 'Handoff not clean'
$result = [ordered]@{adoption_publication_commit=$commit;publication_commit=$integration.publication_commit;decision_commit=$integration.decision_commit;paths=$paths;remote_confirmed=$true}
[IO.File]::WriteAllText((Join-Path $taskRoot 'adoption-publication-result.json'),($result | ConvertTo-Json -Depth 5) + "`n",[Text.UTF8Encoding]::new($false))
$result | ConvertTo-Json -Depth 5
