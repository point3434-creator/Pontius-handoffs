$ErrorActionPreference = 'Stop'
$repo = 'D:/Pontius/tmp/v0a-blueprint-artifact-seal-r001/authoring'
$packet = 'D:/Pontius/tmp/v0a-blueprint-artifact-seal-r001/packets/r002'
$candidate = '12df7106b2fca3b25ed4f57115ba9a31e70b6815'
$prior = '5ba903fcb4ea4b5e4559baa6846fed99730d020b'
$combined = 'c7de23de276c50463d831f3983fede82a5400ce8'
$base = 'c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98'
$git = 'C:/Program Files/Git/cmd/git.exe'
function GitBytes([string]$arguments) {
    $p = New-Object System.Diagnostics.Process
    $p.StartInfo.FileName = $git
    $p.StartInfo.Arguments = '-C "' + $repo + '" ' + $arguments
    $p.StartInfo.UseShellExecute = $false
    $p.StartInfo.CreateNoWindow = $true
    $p.StartInfo.RedirectStandardOutput = $true
    $p.StartInfo.RedirectStandardError = $true
    if (-not $p.Start()) { throw 'Git failed to start' }
    $err = $p.StandardError.ReadToEndAsync()
    $stream = New-Object System.IO.MemoryStream
    $p.StandardOutput.BaseStream.CopyTo($stream)
    $p.WaitForExit()
    if ($p.ExitCode -ne 0) { throw $err.Result }
    $bytes = $stream.ToArray()
    $stream.Dispose()
    $p.Dispose()
    return ,$bytes
}
function Hash([byte[]]$bytes) {
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-', '').ToLowerInvariant() }
    finally { $sha.Dispose() }
}
function GitText([string]$arguments) {
    return [Text.Encoding]::UTF8.GetString((GitBytes $arguments))
}
function Assert([bool]$condition, [string]$label) {
    if (-not $condition) { throw "FAIL: $label" }
    "PASS: $label"
}
$identity = (GitText "show -s --format=%H%n%P%n%T $candidate").Trim().Split("`n")
Assert ($identity[0] -eq $candidate -and $identity[1] -eq $base -and
    $identity[2] -eq 'f3acfba65b32e0890bb86f0af9c087f55e75e50d') 'candidate sole parent and tree'
Assert ((GitText 'rev-parse refs/heads/review/v0a-blueprint-artifact-seal/r002').Trim() -eq $candidate) 'r002 ref'
$paths = (GitText "diff-tree -r --no-renames --no-commit-id --name-only $base $candidate").Trim().Split("`n")
Assert ($paths.Count -eq 14) '14-path base delta'
$rows = New-Object 'System.Collections.Generic.List[string]'
$sourceCount = 0
foreach ($path in $paths) {
    $blob = GitBytes "cat-file blob ${candidate}:$path"
    $digest = Hash $blob
    $rows.Add("$digest  $path`n")
    Assert ($digest -eq (Hash ([IO.File]::ReadAllBytes("$packet/files/$path")))) "raw packet equality: $path"
    if ($path -ne 'STATUS.md' -and $path -notlike 'docs/decisions/*') {
        Assert ($digest -eq (Hash (GitBytes "cat-file blob ${combined}:$path"))) "combined payload equality: $path"
        $sourceCount++
    }
    $text = [Text.Encoding]::UTF8.GetString($blob)
    Assert (-not $text.Contains("`r") -and -not $text.StartsWith([string][char]0xfeff, [StringComparison]::Ordinal) -and
        -not [regex]::IsMatch($text, '[ \t]+(?=\n|$)')) "LF/BOM/trailing whitespace: $path"
}
Assert ($sourceCount -eq 12) '12 original payload paths'
$rows.Sort([StringComparer]::Ordinal)
$manifest = [Text.Encoding]::UTF8.GetBytes([string]::Concat($rows))
$manifestHash = Hash $manifest
Assert ($manifestHash -eq 'c09f4bcc313e987764597f49ef703e8794e76e7be725dc52a642850803a5bb1c') 'recomputed manifest digest'
Assert ($manifestHash -eq (Hash ([IO.File]::ReadAllBytes("$packet/manifest.sha256")))) 'raw manifest file equality'
Assert ((GitText "diff-tree -r --no-renames --no-commit-id --name-only $prior $candidate").Trim() -eq 'STATUS.md') 'complete correction delta is STATUS alone'
$oldStatus = GitBytes "cat-file blob ${prior}:STATUS.md"
$newStatus = GitBytes "cat-file blob ${candidate}:STATUS.md"
$oldText = [Text.Encoding]::UTF8.GetString($oldStatus)
$newText = [Text.Encoding]::UTF8.GetString($newStatus)
Assert ($oldText.Replace("`r`n", "`n") -ceq $newText) 'entire STATUS change is CRLF-to-LF'
$oldCR = @($oldStatus | Where-Object { $_ -eq 13 }).Count
$oldLF = @($oldStatus | Where-Object { $_ -eq 10 }).Count
$newCR = @($newStatus | Where-Object { $_ -eq 13 }).Count
$newLF = @($newStatus | Where-Object { $_ -eq 10 }).Count
Assert ($oldCR -eq 88 -and $oldLF -eq 88 -and $newCR -eq 0 -and $newLF -eq 88) 'exact 88 CR removals'
"STATUS old bytes=$($oldStatus.Length) new bytes=$($newStatus.Length) oldSHA=$(Hash $oldStatus) newSHA=$(Hash $newStatus)"
foreach ($path in @('docs/decisions/ADR-0491-source-seal-the-portable-blueprint-artifact.md',
    'src/pontius/status_generation.py', 'tests/test_status_generation.py')) {
    Assert ((Hash (GitBytes "cat-file blob ${prior}:$path")) -eq
        (Hash (GitBytes "cat-file blob ${candidate}:$path"))) "unchanged versus r001: $path"
}
foreach ($path in @('src/pontius/status_generation.py', 'tests/test_status_generation.py')) {
    Assert ((Hash (GitBytes "cat-file blob ${base}:$path")) -eq
        (Hash (GitBytes "cat-file blob ${candidate}:$path"))) "unchanged versus base: $path"
}
& $git -C $repo diff --check $base $candidate
Assert ($LASTEXITCODE -eq 0) 'base/candidate diff --check'
& $git -C $repo diff --check $prior $candidate
Assert ($LASTEXITCODE -eq 0) 'r001/r002 diff --check'
