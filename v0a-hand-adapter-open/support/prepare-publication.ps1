$ErrorActionPreference = 'Stop'
$taskRoot = 'D:\Pontius\tmp\v0a-hand-adapter-open-r001'
$designRoot = 'D:\Pontius\tmp\v0a-hand-adapter-design-r001'
$stage = Join-Path $taskRoot 'publication-staging'
if (Test-Path -LiteralPath $stage) { throw 'Publication stage already exists' }
function Copy-TreeFiles([string]$from,[string]$to) {
    foreach ($file in (Get-ChildItem -LiteralPath $from -Recurse -File)) {
        if ($file.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse publication input' }
        $relative = [IO.Path]::GetRelativePath($from,$file.FullName)
        $destination = Join-Path $to $relative
        New-Item -ItemType Directory -Force (Split-Path -Parent $destination) | Out-Null
        Copy-Item -LiteralPath $file.FullName -Destination $destination
    }
}
foreach ($round in @('r001','r002','r003')) {
    Copy-TreeFiles (Join-Path $designRoot "packets\$round") (Join-Path $stage "v0a-hand-adapter-design\$round")
}
Copy-TreeFiles (Join-Path $taskRoot 'packets\r001') (Join-Path $stage 'v0a-hand-adapter-open\r001')
foreach ($spec in @(
    @{source=$designRoot; task='v0a-hand-adapter-design'; dirs=@('review-a','review-b','review-r003-a','review-r003-b')},
    @{source=$taskRoot; task='v0a-hand-adapter-open'; dirs=@('review-r001-metadata','run-records')}
)) {
    $support = Join-Path $stage ($spec.task + '\support')
    New-Item -ItemType Directory -Force $support | Out-Null
    Get-ChildItem -LiteralPath $spec.source -File | Where-Object { $_.Extension -in @('.md','.json','.txt','.py','.ps1','.sha256') } | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $support $_.Name)
    }
    foreach ($dir in $spec.dirs) { Copy-TreeFiles (Join-Path $spec.source $dir) (Join-Path $support $dir) }
}
$designVerdicts = [Collections.Generic.List[byte]]::new()
foreach ($round in @('r001','r003')) {
    $designVerdicts.AddRange([IO.File]::ReadAllBytes((Join-Path $designRoot "packets\$round\progress.md")))
}
[IO.File]::WriteAllBytes((Join-Path $stage 'v0a-hand-adapter-design\progress.md'), $designVerdicts.ToArray())
Copy-Item -LiteralPath (Join-Path $taskRoot 'packets\r001\progress.md') -Destination (Join-Path $stage 'v0a-hand-adapter-open\progress.md')
foreach ($path in @('.gitattributes','INDEX.md','progress.md')) {
    Copy-Item -LiteralPath (Join-Path 'D:\Pontius-handoffs' $path) -Destination (Join-Path $stage $path)
}
$files = @(Get-ChildItem -LiteralPath $stage -Recurse -File)
if (@($files | Where-Object { $_.Length -gt 50000000 }).Count) { throw 'Unexpected large publication file' }
"Staged $($files.Count) files; $(($files | Measure-Object Length -Sum).Sum) bytes; no repository mutation"
