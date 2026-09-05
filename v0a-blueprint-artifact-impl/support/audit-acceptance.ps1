param([switch]$AllowFailures)
$ErrorActionPreference = 'Stop'
$taskRoot = 'D:\Pontius\tmp\v0a-blueprint-artifact-impl-r001'
$packetFiles = Join-Path $taskRoot 'packets\r002\files'
$frozenFiles = @(Get-ChildItem -LiteralPath $packetFiles -Recurse -File)
if ($frozenFiles.Count -ne 12) { throw 'Frozen population mismatch' }
$results = foreach ($slot in @('311','314')) {
    $summary = @(Get-Content -Raw -LiteralPath (Join-Path $taskRoot "broad-r002-$slot.json") | ConvertFrom-Json)
    if ($summary.Count -ne 19) { throw "Wrong command count: $slot" }
    $expectedSequence = 1
    foreach ($row in $summary) {
        if ($row.sequence -ne $expectedSequence -or $row.slot -ne $slot) { throw 'Sequence/slot mismatch' }
        if (-not $AllowFailures -and ($row.exit_code -ne 0 -or $row.failure)) {
            throw "Unresolved command $slot/$expectedSequence"
        }
        $records = @(Get-Content -Raw -LiteralPath $row.receipt | ConvertFrom-Json)
        if ($records.Count -ne 2 -or $records[0].exit_code -ne 0) {
            throw 'Identity or payload failure'
        }
        $payload = $records[-1]
        if ($payload.exit_code -ne $row.exit_code) { throw 'Exit-code mismatch' }
        if (($payload.argv[2..($payload.argv.Count-1)] -join [char]0) -cne ($row.command -join [char]0)) {
            throw 'Receipt command mismatch'
        }
        if ($payload.argv[0] -cne '-B' -or $payload.argv[1] -cne '-P') { throw 'Startup flags mismatch' }
        foreach ($file in $frozenFiles) {
            $relative = [IO.Path]::GetRelativePath($packetFiles,$file.FullName)
            $snapshotFile = Join-Path $payload.snapshot $relative
            if ((Get-FileHash -LiteralPath $file.FullName).Hash -cne (Get-FileHash -LiteralPath $snapshotFile).Hash) {
                throw "Post-run frozen-byte mismatch $slot/$expectedSequence/$relative"
            }
        }
        $counts = [regex]::Matches($payload.stderr,'Ran (\d+) tests? in')
        $skips = [regex]::Matches($payload.stderr,'OK \(skipped=(\d+)\)')
        [ordered]@{
            slot=$slot; sequence=$expectedSequence; command=$row.command
            exit_code=$payload.exit_code
            tests=if($counts.Count){[int]$counts[-1].Groups[1].Value}else{$null}
            skipped=if($skips.Count){[int]$skips[-1].Groups[1].Value}else{0}
            frozen_files_matched=12
            receipt=$row.receipt
            receipt_sha256=(Get-FileHash -LiteralPath $row.receipt -Algorithm SHA256).Hash.ToLowerInvariant()
        }
        $expectedSequence++
    }
}
$results | ConvertTo-Json -Depth 6
