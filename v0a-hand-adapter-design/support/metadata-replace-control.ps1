$ErrorActionPreference = 'Stop'
$taskRoot = 'D:\Pontius\tmp\v0a-hand-adapter-design-r001'
$probeRoot = Join-Path $taskRoot 'metadata-replace-control.git'
if (Test-Path -LiteralPath $probeRoot) { throw 'Metadata control already exists' }
$gitExe = 'C:\Program Files\Git\cmd\git.exe'
New-Item -ItemType Directory -Path $probeRoot | Out-Null
function GitText([string[]]$arguments,[string]$payload = '',[switch]$Raw) {
    $info = [Diagnostics.ProcessStartInfo]::new()
    $info.FileName = $gitExe
    $info.UseShellExecute = $false
    $info.RedirectStandardInput = $true
    $info.RedirectStandardOutput = $true
    $info.RedirectStandardError = $true
    foreach ($key in @($info.Environment.Keys)) {
        if ($key.StartsWith('GIT_',[StringComparison]::OrdinalIgnoreCase)) {
            $info.Environment.Remove($key) | Out-Null
        }
    }
    $prefix = @()
    if ($Raw) { $prefix += '--no-replace-objects' }
    $prefix += @('-c','user.name=Metadata control','-c',
        'user.email=metadata-control@example.invalid','-C',$probeRoot)
    foreach ($arg in ($prefix + $arguments)) { $info.ArgumentList.Add($arg) }
    $process = [Diagnostics.Process]::Start($info)
    $stdout = $process.StandardOutput.ReadToEndAsync()
    $stderr = $process.StandardError.ReadToEndAsync()
    $process.StandardInput.Write($payload)
    $process.StandardInput.Close()
    $process.WaitForExit()
    if ($process.ExitCode -ne 0) { throw "Git $($arguments[0]) failed: $($stderr.Result)" }
    $stdout.Result.TrimEnd("`r","`n")
}
GitText @('init','--bare','--quiet') | Out-Null
$originalBlob = GitText @('hash-object','-w','--stdin') "original bytes`n"
$replacementBlob = GitText @('hash-object','-w','--stdin') "replacement bytes`n"
$originalTree = GitText @('mktree') "100644 blob $originalBlob`tmarker.txt`n"
$replacementTree = GitText @('mktree') "100644 blob $replacementBlob`tmarker.txt`n"
$original = GitText @('commit-tree',$originalTree,'-m','Synthetic original metadata object')
$replacement = GitText @('commit-tree',$replacementTree,'-m','Synthetic replacement metadata object')
GitText @('update-ref','refs/heads/main',$original,('0'*40)) | Out-Null
GitText @('symbolic-ref','HEAD','refs/heads/main') | Out-Null
GitText @('update-ref',"refs/replace/$original",$replacement,('0'*40)) | Out-Null
$head = GitText @('rev-parse','HEAD')
$ordinary = GitText @('cat-file','blob',"${original}:marker.txt")
$raw = GitText @('cat-file','blob',"${original}:marker.txt") -Raw
if ($head -ne $original -or $ordinary -ne 'replacement bytes' -or $raw -ne 'original bytes') {
    throw 'Metadata control did not reproduce expected replacement behavior'
}
$result = [ordered]@{scope='synthetic Git objects only; no project import or execution';
    repository=$probeRoot;head=$head;original_commit=$original;replacement_commit=$replacement;
    ordinary_commit_path_read=$ordinary;no_replace_commit_path_read=$raw;
    reproduced=$true;original_objects_retained=$true}
[IO.File]::WriteAllText((Join-Path $taskRoot 'metadata-replace-control.json'),
    ($result | ConvertTo-Json -Depth 4) + "`n",[Text.UTF8Encoding]::new($false))
$result | ConvertTo-Json -Depth 4
