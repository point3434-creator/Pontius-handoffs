param([ValidateSet('r001','r002')][string]$Round = 'r001')
$ErrorActionPreference = 'Stop'
$taskRoot = 'D:\Pontius\tmp\workflow-proportionality-r001'
$work = Join-Path $taskRoot 'authoring'
$packet = Join-Path $taskRoot "packets\$Round"
if (Test-Path -LiteralPath $packet) { throw 'Round packet exists; do not overwrite' }
$base = '53773cb9e7489d8cfa32b4e0ceadea37c5980023'
$gitExe = 'C:\Program Files\Git\cmd\git.exe'
$allowed = @('CLAUDE.md','docs/workflow.md','docs/decisions/ADR-0492-adopt-proportionate-engineering-review.md','STATUS.md')
function Invoke-GitRaw([string[]]$GitArgs) {
    $start = [Diagnostics.ProcessStartInfo]::new()
    $start.FileName = $gitExe
    $start.UseShellExecute = $false
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    foreach ($arg in (@('-c',"safe.directory=$($work.Replace('\','/'))",'-C',$work) + $GitArgs)) { $start.ArgumentList.Add($arg) }
    $proc = [Diagnostics.Process]::Start($start)
    $buffer = [IO.MemoryStream]::new()
    $stderr = $proc.StandardError.ReadToEndAsync()
    $proc.StandardOutput.BaseStream.CopyTo($buffer)
    $proc.WaitForExit()
    if ($proc.ExitCode -ne 0) { throw "Git failed: $($stderr.Result)" }
    return ,$buffer.ToArray()
}
function Invoke-GitText([string[]]$GitArgs) { [Text.Encoding]::UTF8.GetString((Invoke-GitRaw $GitArgs)).TrimEnd("`r","`n") }
if ((Invoke-GitText @('rev-parse','HEAD')) -ne '53773cb9e7489d8cfa32b4e0ceadea37c5980023') { throw 'Authoring base changed' }
$changed = @((Invoke-GitText @('diff','--name-only',$base)) -split "`n") + @((Invoke-GitText @('ls-files','--others','--exclude-standard')) -split "`n")
foreach ($path in $changed) { if ($path -and $path -notin $allowed) { throw "Out-of-scope path: $path" } }
foreach ($path in $allowed) { if (-not (Test-Path -LiteralPath (Join-Path $work $path) -PathType Leaf)) { throw "Required path missing: $path" } }
$savedIndex = [Environment]::GetEnvironmentVariable('GIT_INDEX_FILE')
$index = Join-Path $taskRoot ("freeze-" + [guid]::NewGuid().ToString('N') + '.idx')
$ref = "refs/heads/review/workflow-proportionality/$Round"
try {
    $env:GIT_INDEX_FILE = $index
    Invoke-GitText @('read-tree',$base) | Out-Null
    Invoke-GitText (@('-c','core.autocrlf=false','add','--') + $allowed) | Out-Null
    $tree = Invoke-GitText @('write-tree')
    $commit = Invoke-GitText @('commit-tree',$tree,'-p',$base,'-m',"Review candidate workflow-proportionality/$Round (frozen, not a decision commit)")
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
$identity = [ordered]@{schema_version='pontius-handoff-candidate-v1';task_id='workflow-proportionality';round=$Round;ref=$ref;commit=$commit;base=$base;tree=$tree;manifest_sha256=$manifestHash;date=(Get-Date -Format 'yyyy-MM-dd')}
[IO.File]::WriteAllText((Join-Path $packet 'candidate.json'),(($identity | ConvertTo-Json) -replace "`r`n","`n")+"`n",[Text.UTF8Encoding]::new($false))
$diff = Invoke-GitRaw @('diff','--no-ext-diff','--no-renames','-U10',$base,$commit)
[IO.File]::WriteAllBytes((Join-Path $packet 'review.diff'),$diff)
$sourceDiff = $diff
[IO.File]::WriteAllBytes((Join-Path $packet 'source.diff'),$sourceDiff)
$identity | ConvertTo-Json
'Local review snapshot only. No remote publication, primary index/HEAD change, decision commit or adoption.'

