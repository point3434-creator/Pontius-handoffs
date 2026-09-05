$ErrorActionPreference = 'Stop'
$taskRoot = 'D:\Pontius\tmp\workflow-proportionality-r001'
$stage = Join-Path $taskRoot 'publication-staging'
if (Test-Path -LiteralPath $stage) { throw 'Publication staging exists' }
$destinationRoot = Join-Path $stage 'workflow-proportionality'
function Copy-TreeFiles([string]$from,[string]$to) {
    foreach ($file in (Get-ChildItem -LiteralPath $from -Recurse -File)) {
        if ($file.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse input' }
        $relative = [IO.Path]::GetRelativePath($from,$file.FullName)
        $destination = Join-Path $to $relative
        New-Item -ItemType Directory -Path (Split-Path $destination) -Force | Out-Null
        Copy-Item -LiteralPath $file.FullName -Destination $destination
    }
}
Copy-TreeFiles (Join-Path $taskRoot 'packets\r001') (Join-Path $destinationRoot 'r001')
$support = Join-Path $destinationRoot 'support'
New-Item -ItemType Directory -Path $support -Force | Out-Null
Get-ChildItem -LiteralPath $taskRoot -File | Where-Object {
    $_.Extension -in @('.md','.json','.jsonl','.txt','.py','.ps1','.sha256')
} | ForEach-Object { Copy-Item -LiteralPath $_.FullName -Destination $support }
foreach ($sub in @('review-a','review-b','review-a-v2','review-b-v2','review-probe-v2','run-records')) {
    Copy-TreeFiles (Join-Path $taskRoot $sub) (Join-Path $support $sub)
}
$reviews = Join-Path $destinationRoot 'r001\reviews'
New-Item -ItemType Directory -Path $reviews -Force | Out-Null
$verdictBytes = [Collections.Generic.List[byte]]::new()
foreach ($seat in @('a','b')) {
    $from = Join-Path $taskRoot "review-$seat-v2\review.md"
    Copy-Item -LiteralPath $from -Destination (Join-Path $reviews "review-$seat.md")
    $bytes = [IO.File]::ReadAllBytes($from)
    $end = [Array]::IndexOf($bytes,[byte]10)
    if ($end -lt 0) { throw 'Issued verdict line missing LF' }
    $verdictBytes.AddRange([byte[]]$bytes[0..$end])
}
# Mechanical transport of the issuers' exact first-line verdict bytes; no new verdict.
[IO.File]::WriteAllBytes((Join-Path $destinationRoot 'progress.md'),$verdictBytes.ToArray())
foreach ($path in @('.gitattributes','INDEX.md','progress.md')) {
    Copy-Item -LiteralPath (Join-Path 'D:\Pontius-handoffs' $path) -Destination $stage
}
$files = @(Get-ChildItem -LiteralPath $stage -Recurse -File)
if (@($files | Where-Object {$_.Length -gt 50000000}).Count) { throw 'Unexpected large input' }
"Staged $($files.Count) files; $(($files | Measure-Object Length -Sum).Sum) bytes"
