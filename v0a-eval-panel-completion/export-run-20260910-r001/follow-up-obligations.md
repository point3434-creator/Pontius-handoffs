# Required follow-up at the next legitimate wrapper revision

Origin: cold review 02 A1 and finalization review 03 A-03. Accepted by Codex, 2026-09-10.
This is a design obligation for the next wrapper revision, including an agreement wrapper
derived from this one. It does not reopen or modify the current export freeze.

Move validation/resolution of SystemRoot or its SYSTEMROOT fallback, TEMP and TMP above
successful claim acquisition. Missing required environment must cause an explicit refusal
before any claim, claim/start record or child launch. Preserve the successful environment
and fallback behavior of the current launch line. Document the chosen refusal code and the
distinction between an unset value, an empty value and an unusable temporary directory.

Before freezing that revision, verify missing primary/fallback combinations, a valid
fallback, missing TEMP/TMP and the intended treatment of empty values. Refusal cases must
assert that no new claim or launch exists, not merely inspect exit status. A positive case
must preserve the child environment. The next drafter must explicitly disposition this
obligation rather than silently carrying the post-claim expansion forward.

Current residual: invoke.sh expands the variables after acquiring its claim. In a malformed
or deliberately stripped environment, set -u can terminate before launching the child and
leave the claim consumed. Previous successful Windows/Git-Bash invocations establish that
their observed environments supplied the variables; they do not prove absence impossible.
For this invocation, finalizer-addendum-02.md's environment prerequisites remain in force.
No claim of a runtime fix or new test coverage is made here.
