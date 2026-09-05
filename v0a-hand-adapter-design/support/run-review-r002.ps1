param([Parameter(Mandatory=$true)][ValidateSet('a','b')][string]$Seat)
$ErrorActionPreference = 'Stop'
$taskRoot = 'D:\Pontius\tmp\v0a-hand-adapter-design-r001'
$reviewRoot = Join-Path $taskRoot "review-r002-$Seat"
if (Test-Path -LiteralPath $reviewRoot) { throw 'Review directory already exists' }
New-Item -ItemType Directory -Path $reviewRoot | Out-Null
$focus = if ($Seat -eq 'a') {
    'Extra attention: literal-card mapping, input admission, full-deal separation, reader semantics and declared ground truth.'
} else {
    'Extra attention: source/import and raw-input identity, final acceptance/refusal paths, registration scope and proportionality.'
}
$prompt = @"
You are independent fresh design reviewer $Seat for v0a-hand-adapter-design/r002.
Read D:/Pontius/tmp/v0a-hand-adapter-design-r001/packets/r002/handoff.md and follow it.
Candidate 1c2fde7bdb9359436f9c2ff260e324a08439752b; base 7a387e995e3b37232d2379332927247a4d49c64e;
manifest f2c8c9f8c292585623b06a7f623e6b31f6202199f66c82afd78d765bfcab1b1a.
Object repository: D:/Pontius/tmp/v0a-hand-adapter-design-r001/authoring.
Review all three frozen documents and compatibility with actual base contracts/source. $focus
This is a FIX: independently inventory the invariant and affected paths BEFORE reading
the deferred coverage claim. The exact prior finding and allowed inputs are in handoff.md.
Independently recompute raw Git identity, registration pins and hygiene.
Git executable C:/Program Files/Git/cmd/git.exe; command-local safe.directory for this
exact clone is allowed if needed, never global configuration.
No source/index/HEAD/ref edits, project imports, tests, hand/owner invocations, installs,
network calls, subagents, current sibling reports or controller transcripts. Design review
only, not executed acceptance of unimplemented code. All files are read-only to you.
Return the complete concise attributed review as your FINAL answer; --output-last-message
retains your original issued bytes directly. First line must be your attributed one-line
verdict with task, commit and manifest. Include Spec/Quality PASS or FAIL, C/I/M counts,
CLEAN or unresolved corrections, Design SOUND/STRAINED/WRONG SHAPE, findings and limits.
Require concrete failure scenarios or contradictions for substantive findings. Distinguish
required outcomes from optional implementation advice. Harmless preferences are observations.
Keep the report roughly two pages without sacrificing a material finding. Do not write files.
"@
$start = [Diagnostics.ProcessStartInfo]::new()
$start.FileName = 'C:\Users\point\AppData\Local\OpenAI\Codex\bin\1e3e57cdf0634c02\codex.exe'
$start.WorkingDirectory = Join-Path $taskRoot 'authoring'
$start.UseShellExecute = $false
$start.RedirectStandardInput = $true
$start.RedirectStandardOutput = $true
$start.RedirectStandardError = $true
$argv = @('exec','--ephemeral','--ignore-user-config','--sandbox','read-only',
    '-c','windows.sandbox="elevated"','--disable','multi_agent','--model','gpt-5.6-sol',
    '-c','model_reasoning_effort="high"','--json','--output-last-message',
    (Join-Path $reviewRoot 'review.md'),'-')
foreach ($arg in $argv) { $start.ArgumentList.Add($arg) }
$process = [Diagnostics.Process]::Start($start)
$process.StandardInput.Write($prompt)
$process.StandardInput.Close()
$stdout = $process.StandardOutput.ReadToEndAsync()
$stderr = $process.StandardError.ReadToEndAsync()
$process.WaitForExit()
[IO.File]::WriteAllText((Join-Path $reviewRoot 'session.jsonl'),$stdout.Result,[Text.UTF8Encoding]::new($false))
[IO.File]::WriteAllText((Join-Path $reviewRoot 'session.stderr.txt'),$stderr.Result,[Text.UTF8Encoding]::new($false))
$result = [ordered]@{seat=$Seat;exit_code=$process.ExitCode;argv=$argv;report=(Join-Path $reviewRoot 'review.md')}
[IO.File]::WriteAllText((Join-Path $reviewRoot 'delivery.json'),($result | ConvertTo-Json -Depth 5) + "`n",[Text.UTF8Encoding]::new($false))
$result | ConvertTo-Json -Depth 5
if ($process.ExitCode -ne 0) { throw "Reviewer delivery failed; stderr retained: $($stderr.Result)" }
