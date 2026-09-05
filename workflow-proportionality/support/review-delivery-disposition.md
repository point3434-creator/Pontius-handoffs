# Review delivery preflight and correction

The controller authorized using the existing OpenAI sign-in for two read-only
cold reviews. The first launch used --ignore-user-config and --sandbox read-only
but omitted the user's configured Windows sandbox backend. Both sessions exited
normally but reported that their read-only commands had been rejected by policy.
They did not inspect the candidate. Their reports remain unedited:

- review-a/review.md: 1a250da70039eb261a76b744e7e8d5a12175ad18318f15f169768fa61265008d
- review-b/review.md: 59a1f84f646a530cbbca3a29ae4b4072738f35a49f7c5fc1e807719eec9d2dd3

Controller disposition: INCONCLUSIVE environment failures, not completed cold
passes, amendment defects or amendment design verdicts. The reports' Critical
and WRONG SHAPE labels describe inability to inspect, not an observed policy
failure. Their asserted packet-root access cause was not established by the
actual command-denial logs and is not adopted as an independent finding.

Read-only configuration inspection found the existing setting
windows.sandbox = "elevated". The launch had ignored it. The only permission-related
change in run-review-v2.ps1 explicitly selects that existing backend; read-only
filesystem permissions and disabled delegation remain. No global setting, trust
rule, sign-in secret, filesystem ACL or source file was edited by the controller.
The CLI's normal native sandbox machinery supplies its execution isolation.

A one-command preflight in review-probe-v2 read the first five handoff lines and
resolved candidate 922398389870ba9dc378eb096363de3b1bb3731c successfully. This tests
review access only. It is neither a substantive review nor acceptance evidence.
The corrected launch creates fresh review-a-v2 and review-b-v2 sessions with no
prior session history or sibling report inputs, reviewing the unchanged r001
commit and manifest. Candidate scope and review scope are unchanged.

References used for launcher diagnostics: installed CLI help and the official
Windows sandbox documentation at
https://learn.chatgpt.com/docs/windows/windows-sandbox.
No permissive or full-access fallback was used.
