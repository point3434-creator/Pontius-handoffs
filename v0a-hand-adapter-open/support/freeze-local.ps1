$Round = 'r001'
$ErrorActionPreference = 'Stop'
$taskRoot = 'D:\Pontius\tmp\v0a-hand-adapter-open-r001'
$work = Join-Path $taskRoot 'authoring'
$packet = Join-Path $taskRoot "packets\$Round"
$stage = $work
if (Test-Path -LiteralPath $packet) { throw 'Round packet exists; do not overwrite' }
$base = '7a387e995e3b37232d2379332927247a4d49c64e'
$gitExe = 'C:\Program Files\Git\cmd\git.exe'
$allowed = @('docs/architecture/v0a-hand-adapter-r002/brief.md','docs/architecture/v0a-hand-adapter-r002/design.md','docs/architecture/v0a-hand-adapter-r002/source-opening-draft.md','docs/decisions/ADR-0493-open-the-one-hand-file-adapter-source-round.md','STATUS.md')
function Invoke-GitRaw([string[]]$GitArgs) {
    $start = [Diagnostics.ProcessStartInfo]::new()
    $start.FileName = $gitExe
    $start.UseShellExecute = $false
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    foreach ($arg in (@('--no-replace-objects','-c',"safe.directory=$($work.Replace('\','/'))",'-C',$work) + $GitArgs)) { $start.ArgumentList.Add($arg) }
    $proc = [Diagnostics.Process]::Start($start)
    $buffer = [IO.MemoryStream]::new()
    $stderr = $proc.StandardError.ReadToEndAsync()
    $proc.StandardOutput.BaseStream.CopyTo($buffer)
    $proc.WaitForExit()
    if ($proc.ExitCode -ne 0) { throw "Git failed: $($stderr.Result)" }
    return ,$buffer.ToArray()
}
function Invoke-GitText([string[]]$GitArgs) { [Text.Encoding]::UTF8.GetString((Invoke-GitRaw $GitArgs)).TrimEnd("`r","`n") }
if ((Invoke-GitText @('rev-parse','HEAD')) -ne '7a387e995e3b37232d2379332927247a4d49c64e') { throw 'Authoring base changed' }
if (Invoke-GitText @('diff','--cached','--name-only')) { throw 'Authoring index changed' }
$changed = @((Invoke-GitText @('diff','--name-only')) -split "`n") + @((Invoke-GitText @('ls-files','--others','--exclude-standard')) -split "`n")
$changed = @($changed | Where-Object { $_ })
if ($changed.Count -ne 5 -or @($changed | Where-Object { $_ -notin $allowed }).Count) { throw 'Authoring scope differs' }
foreach ($path in $allowed) {
    $bytes = [IO.File]::ReadAllBytes((Join-Path $stage $path))
    if ($bytes[-1] -ne 10 -or $bytes[-2] -eq 10 -or $bytes -contains 13) { throw "EOF/LF check failed: $path" }
    $content = [Text.UTF8Encoding]::new($false,$true).GetString($bytes)
    if ($content.StartsWith([char]0xFEFF) -or $content -match '(?m)[ \t]+$') { throw "BOM/trailing whitespace: $path" }
    if ($path -like 'docs/architecture/*') {
        $reviewed = Invoke-GitRaw @('cat-file','blob',"02e24f143b8df4b2f03e8a94c58ab57905a8b2b6:$path")
        if ([Convert]::ToBase64String($bytes) -cne [Convert]::ToBase64String($reviewed)) { throw "Reviewed copy differs: $path" }
    }
    if ($path -ne 'STATUS.md' -and @($content.Split([char]10) | Where-Object { $_.Length -gt 100 }).Count) { throw "Line width: $path" }
}
$generated = [IO.File]::ReadAllText((Join-Path $taskRoot 'snapshots/generate-311/STATUS.md')).Replace("`r`n","`n")
if ([IO.File]::ReadAllText((Join-Path $stage 'STATUS.md')) -cne $generated) { throw 'STATUS is not the normalized generator output' }
$savedIndex = [Environment]::GetEnvironmentVariable('GIT_INDEX_FILE')
$index = Join-Path $taskRoot ("freeze-" + [guid]::NewGuid().ToString('N') + '.idx')
$ref = "refs/heads/review/v0a-hand-adapter-open/$Round"
try {
    $env:GIT_INDEX_FILE = $index
    Invoke-GitText @('read-tree',$base) | Out-Null
    Invoke-GitText (@("--work-tree=$stage",'-c','core.autocrlf=false','add','--') + $allowed) | Out-Null
    Invoke-GitText @('diff','--cached','--check',$base) | Out-Null
    $tree = Invoke-GitText @('write-tree')
    $newPaths = @((Invoke-GitText @('diff','--no-renames','--name-only',$base,$tree)) -split "`n")
    if ($newPaths.Count -ne 5 -or @($newPaths | Where-Object { $_ -notin $allowed }).Count) { throw 'Frozen scope differs' }
    $commit = Invoke-GitText @('commit-tree',$tree,'-p',$base,'-m',"Review candidate v0a-hand-adapter-open/$Round (frozen, not a decision commit)")
} finally {
    if ($null -eq $savedIndex) { Remove-Item Env:GIT_INDEX_FILE -ErrorAction SilentlyContinue } else { $env:GIT_INDEX_FILE = $savedIndex }
    if (Test-Path -LiteralPath $index) { Remove-Item -LiteralPath $index -Force }
}
Invoke-GitText @('update-ref',$ref,$commit,('0'*40)) | Out-Null
$fields = (Invoke-GitText @('diff-tree','-r','-z','--no-renames','--no-commit-id','--name-status',$base,$commit)).Split([char]0)
$rows = [Collections.Generic.List[string]]::new()
New-Item -ItemType Directory -Path $packet | Out-Null
for ($i=0; $i+1 -lt $fields.Length; $i+=2) {
    if (-not $fields[$i]) { break }
    $path = $fields[$i+1]
    if ($fields[$i] -eq 'D') { throw 'Deletion outside source opening' }
    $bytes = Invoke-GitRaw @('cat-file','blob',"${commit}:$path")
    $digest = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant()
    $rows.Add("$digest  $path`n")
    $destination = Join-Path $packet "files\$path"
    New-Item -ItemType Directory -Force (Split-Path -Parent $destination) | Out-Null
    [IO.File]::WriteAllBytes($destination,$bytes)
}
$rows.Sort([StringComparer]::Ordinal)
$manifest = [Text.Encoding]::UTF8.GetBytes(($rows -join ''))
[IO.File]::WriteAllBytes((Join-Path $packet 'manifest.sha256'),$manifest)
$manifestHash = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($manifest)).ToLowerInvariant()
$identity = [ordered]@{schema_version='pontius-handoff-candidate-v1';task_id='v0a-hand-adapter-open';round=$Round;ref=$ref;commit=$commit;base=$base;tree=$tree;manifest_sha256=$manifestHash;date=(Get-Date -Format 'yyyy-MM-dd')}
[IO.File]::WriteAllText((Join-Path $packet 'candidate.json'),(($identity | ConvertTo-Json) -replace "`r`n","`n")+"`n",[Text.UTF8Encoding]::new($false))
$diff = Invoke-GitRaw @('diff','--no-ext-diff','--no-renames','-U10',$base,$commit)
[IO.File]::WriteAllBytes((Join-Path $packet 'review.diff'),$diff)
$sourceDiff = $diff
[IO.File]::WriteAllBytes((Join-Path $packet 'source.diff'),$sourceDiff)
$identity | ConvertTo-Json
'Local review snapshot only. No remote publication, primary index/HEAD change, decision commit or adoption.'
