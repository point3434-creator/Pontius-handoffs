$ErrorActionPreference = 'Stop'
$taskRoot = 'D:\Pontius\tmp\v0a-blueprint-artifact-seal-r001'
$stage = Join-Path $taskRoot 'publication-staging'
if (Test-Path -LiteralPath $stage) { throw 'Publication staging already exists' }
New-Item -ItemType Directory -Path $stage | Out-Null
$tasks = @(
    @('v0a-blueprint-artifact-impl','D:\Pontius\tmp\v0a-blueprint-artifact-impl-r001'),
    @('windows-handle-fixture','D:\Pontius\tmp\windows-handle-fixture-r001'),
    @('v0a-blueprint-artifact-seal',$taskRoot)
)
foreach ($task in $tasks) {
    $name,$source = $task
    foreach ($round in @('r001','r002')) {
        $from = Join-Path $source "packets\$round"
        $to = Join-Path $stage "$name\$round"
        New-Item -ItemType Directory -Path $to -Force | Out-Null
        Get-ChildItem -LiteralPath $from -File -Recurse | ForEach-Object {
            if ($_.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse input' }
            $relative = [IO.Path]::GetRelativePath($from,$_.FullName)
            $destination = Join-Path $to $relative
            New-Item -ItemType Directory -Path (Split-Path $destination) -Force | Out-Null
            Copy-Item -LiteralPath $_.FullName -Destination $destination
        }
    }
    $support = Join-Path $stage "$name\support"
    New-Item -ItemType Directory -Path $support -Force | Out-Null
    Get-ChildItem -LiteralPath $source -File | Where-Object {
        $_.Extension -in @('.md','.json','.py','.ps1','.sha256')
    } | ForEach-Object { Copy-Item -LiteralPath $_.FullName -Destination $support }
    foreach ($sub in @('reviews','review','review-r002','run-records')) {
        $from = Join-Path $source $sub
        if (-not (Test-Path -LiteralPath $from)) { continue }
        Get-ChildItem -LiteralPath $from -File -Recurse | ForEach-Object {
            if ($_.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse input' }
            $relative = [IO.Path]::GetRelativePath($from,$_.FullName)
            $destination = Join-Path $support "$sub\$relative"
            New-Item -ItemType Directory -Path (Split-Path $destination) -Force | Out-Null
            Copy-Item -LiteralPath $_.FullName -Destination $destination
        }
    }
}
foreach ($path in @('.gitattributes','INDEX.md','progress.md')) {
    Copy-Item -LiteralPath (Join-Path 'D:\Pontius-handoffs' $path) -Destination $stage
}
$files = @(Get-ChildItem -LiteralPath $stage -Recurse -File)
if (@($files | Where-Object {$_.Length -gt 50000000}).Count) { throw 'Unexpected large file' }
"Staged $($files.Count) files; $((($files | Measure-Object Length -Sum).Sum)) bytes"
