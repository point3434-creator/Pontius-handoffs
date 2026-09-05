param([Parameter(Mandatory=$true)][ValidateSet('a','b')][string]$Seat)
$ErrorActionPreference = 'Stop'
$taskRoot = 'D:\Pontius\tmp\workflow-proportionality-r001'
$reviewRoot = Join-Path $taskRoot "review-$Seat"
if (Test-Path -LiteralPath $reviewRoot) { throw 'Review directory already exists' }
New-Item -ItemType Directory -Path $reviewRoot | Out-Null
$focus = if ($Seat -eq 'a') {
    'Extra attention: mechanical eligibility, cumulative anchors, independent review and immutable identity.'
} else {
    'Extra attention: controlled-trigger admissibility, independent outcomes, negative controls and risk-tier understatement.'
}
$prompt = @"
You are independent fresh reviewer $Seat of a four-file prospective workflow amendment.
Read D:/Pontius/tmp/workflow-proportionality-r001/packets/r001/handoff.md and its brief.md.
Candidate 922398389870ba9dc378eb096363de3b1bb3731c; base 53773cb9e7489d8cfa32b4e0ceadea37c5980023;
manifest 9c45e5069a7b0e7276e9a1e63e3b809bfc2c696a26c04f32336cb36ac8411589.
Object repository: D:/Pontius/tmp/workflow-proportionality-r001/authoring.
Governing review protocol comes from the BASE; the proposed rules cannot self-apply.
Review all three changes and all four changed files. $focus
Independently recompute raw Git identity and hygiene. Git executable is C:/Program Files/Git/cmd/git.exe;
use command-local safe.directory for the exact authoring repo if required, never global configuration.
No source/index/HEAD/ref edits, subagents, sibling reviews, controller transcripts, network calls,
publication, commit, push or test execution. Controller runs metadata acceptance after both reviews.
This launcher overrides handoff output instructions only: you are filesystem read-only. Return the
complete concise review as your FINAL answer; --output-last-message saves your issued bytes directly.
Include a one-line attributed verdict, exact commit/manifest, Spec/Quality PASS or FAIL, C/I/M counts,
CLEAN or required corrections, Design SOUND/STRAINED/WRONG SHAPE, findings and verification limits.
Require concrete failure scenarios for substantive findings. Harmless preferences are observations.
Do not alter files to issue your review. Do not spawn reviewers. Keep a clean report to roughly two pages.
"@
$start = [Diagnostics.ProcessStartInfo]::new()
$start.FileName = 'C:\Users\point\AppData\Local\OpenAI\Codex\bin\1e3e57cdf0634c02\codex.exe'
$start.WorkingDirectory = Join-Path $taskRoot 'authoring'
$start.UseShellExecute = $false
$start.RedirectStandardInput = $true
$start.RedirectStandardOutput = $true
$start.RedirectStandardError = $true
$argv = @('exec','--ephemeral','--ignore-user-config','--sandbox','read-only',
    '--disable','multi_agent','--model','gpt-5.6-sol','-c','model_reasoning_effort="high"',
    '--json','--output-last-message',(Join-Path $reviewRoot 'review.md'),'-')
foreach ($arg in $argv) { $start.ArgumentList.Add($arg) }
$process = [Diagnostics.Process]::Start($start)
$process.StandardInput.Write($prompt)
$process.StandardInput.Close()
$stdout = $process.StandardOutput.ReadToEndAsync()
$stderr = $process.StandardError.ReadToEndAsync()
$process.WaitForExit()
[IO.File]::WriteAllText((Join-Path $reviewRoot 'session.jsonl'),$stdout.Result,[Text.UTF8Encoding]::new($false))
[IO.File]::WriteAllText((Join-Path $reviewRoot 'session.stderr.txt'),$stderr.Result,[Text.UTF8Encoding]::new($false))
[ordered]@{seat=$Seat;exit_code=$process.ExitCode;argv=$argv;report=(Join-Path $reviewRoot 'review.md')} | ConvertTo-Json
if ($process.ExitCode -ne 0) { throw "Reviewer execution failed; retained stderr: $($stderr.Result)" }
