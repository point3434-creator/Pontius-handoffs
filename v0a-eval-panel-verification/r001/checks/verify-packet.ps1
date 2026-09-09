$ErrorActionPreference='Stop'
$packet='D:/Pontius-handoffs/v0a-eval-panel-verification/r001'
$candidate=Get-Content -LiteralPath ($packet+'/candidate.json') -Raw | ConvertFrom-Json
function Blob([string]$spec) {
    $start=[Diagnostics.ProcessStartInfo]::new()
    $start.FileName='C:/Program Files/Git/cmd/git.exe'
    $start.UseShellExecute=$false
    $start.CreateNoWindow=$true
    $start.RedirectStandardOutput=$true
    foreach ($arg in @('-C','D:/Pontius','cat-file','blob',$spec)) {
        $start.ArgumentList.Add($arg)
    }
    $process=[Diagnostics.Process]::Start($start)
    $memory=[IO.MemoryStream]::new()
    $process.StandardOutput.BaseStream.CopyTo($memory)
    $process.WaitForExit()
    if ($process.ExitCode) { throw 'Blob read failed' }
    $bytes=$memory.ToArray()
    $memory.Dispose()
    $process.Dispose()
    return ,$bytes
}
function Digest([byte[]]$bytes) {
    return [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($bytes)).ToLower()
}
$paths=git -C D:/Pontius diff-tree --no-renames --no-commit-id --name-only -r `
    $candidate.base $candidate.commit
if ($LASTEXITCODE) { throw 'Scope lookup failed' }
[string[]]$rows=@(foreach ($path in $paths) {
    $bytes=Blob ($candidate.commit+':'+$path)
    (Digest $bytes)+'  '+$path+"`n"
})
[Array]::Sort($rows,[StringComparer]::Ordinal)
$manifest=[Text.Encoding]::UTF8.GetBytes(($rows -join ''))
if ((Digest $manifest) -ne $candidate.manifest_sha256) { throw 'Manifest mismatch' }
if ((Digest ([IO.File]::ReadAllBytes($packet+'/manifest.sha256'))) -ne
    $candidate.manifest_sha256) { throw 'Manifest file mismatch' }
$dependencies=Get-Content -LiteralPath ($packet+'/inputs/dependencies.json') -Raw | ConvertFrom-Json
foreach ($dependency in $dependencies) {
    if ((Digest (Blob ($dependency.commit+':'+$dependency.path))) -ne $dependency.sha256) {
        throw ('Dependency mismatch '+$dependency.path)
    }
}
$result=[ordered]@{candidate=$candidate.commit;manifest_sha256=$candidate.manifest_sha256;
    changed_paths=@($paths);dependency_count=@($dependencies).Count;
    verified=$true;method='Independent PowerShell/.NET raw Git blob recomputation'}
[IO.File]::WriteAllText('D:/Pontius/tmp/eval-panel-verification/identity-verification.json',
    ($result|ConvertTo-Json -Depth 4)+"`n",[Text.UTF8Encoding]::new($false))
$result | ConvertTo-Json -Depth 4
