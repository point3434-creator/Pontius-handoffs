$Seat = 'metadata'
$ErrorActionPreference = 'Stop'
$taskRoot = 'D:\Pontius\tmp\v0a-hand-adapter-open-r001'
$reviewRoot = Join-Path $taskRoot "review-r001-$Seat"
if (Test-Path -LiteralPath $reviewRoot) { throw 'Review directory already exists' }
New-Item -ItemType Directory -Path $reviewRoot | Out-Null
$prompt = @"
You are the fresh independent Tier A light metadata reviewer for v0a-hand-adapter-open/r001.
Read D:/Pontius/tmp/v0a-hand-adapter-open-r001/packets/r001/handoff.md and follow it.
Candidate 36c31477d87028aeec31339d28ccc089ffcaa31d; base 7a387e995e3b37232d2379332927247a4d49c64e;
manifest 83814f33a6f7f64b99da7bedfaaa81e61712c083d8f0ecf55a79f0f9a22f142c.
Object repository: D:/Pontius/tmp/v0a-hand-adapter-open-r001/authoring.
Review faithful incorporation of an already independently reviewed design into exactly five
metadata paths, following ADR-0490. Recompute raw identities and confirm no additional authority.
No broader redesign or code review is requested. The accepted design reviews are allowed anchor
evidence; do not read controller transcripts or unlisted reviews. No edits, project imports,
tests, hands, owners, installs, network or agents. All your inputs are read-only.
Return the complete attributed review as your FINAL answer; --output-last-message retains
the original issued bytes directly. Start with an attributed one-line task/commit/manifest
verdict, Spec/Quality PASS or FAIL, C/I/M counts, CLEAN or corrections, and Design assessment.
Include evidence and limitations. About one or two pages is proportionate.
"@
$start = [Diagnostics.ProcessStartInfo]::new()
$start.FileName = 'C:\Users\point\AppData\Local\OpenAI\Codex\bin\1e3e57cdf0634c02\codex.exe'
$start.WorkingDirectory = Join-Path $taskRoot 'authoring'
$start.UseShellExecute = $false
$start.CreateNoWindow = $true
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
