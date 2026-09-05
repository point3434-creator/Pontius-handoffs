# Focused metadata checks: v0a-blueprint-artifact-open/r001

Candidate: `964ae18a64eccc595526525536d0e53e02293b83`.
Manifest SHA-256: `a6daf28c7bba5d7c531b39d31ea4f2e09c292339996a73baec0edb5bd523da1b`.

Only metadata tests ran. No codec, poker runtime, rehearsal, operating,
scientific or research payload was executed.

## Results, in order

1. Fresh LF/no-hardlinks build snapshot from base, exact five-file overlay:
   `D:/Pontius/tmp/v0a-blueprint-artifact-open-r001/build-snapshot`.
   Floor slot: `D:/Pontius-tools/py311/Scripts/python.exe`, CPython 3.11.15.
   Unchanged `-m pontius.status_generation`: exit 0; new STATUS output
   mechanically formatted to LF, then frozen without semantic hand edits.
   `-m pontius.status_generation --check`: exit 0, STATUS.md is current.
   `-m unittest discover -s tests -p test_status_generation.py`:
   exit 0, 12 tests in 0.255s, OK.
2. Fresh LF/no-hardlinks clone checked out at the frozen candidate:
   `D:/Pontius/tmp/v0a-blueprint-artifact-open-r001/focused-314-snapshot`.
   Project slot: `D:/Pontius/.venv/Scripts/python.exe`, CPython 3.14.6.
   `-m pontius.status_generation --check`: exit 0, STATUS.md is current.
   Same 12-test command: exit 0, 12 tests in 0.221s, OK.

Each Python invocation uses -B -P, snapshot-root cwd, snapshot/src PYTHONPATH,
PYTHONNOUSERSITE=1, absolute PONTIUS_GIT, and a cleared child environment with
only Windows launch essentials, explicit temp paths and Python encoding knobs.
Identity checks asserted CPython version, safe path, no bytecode, and that
status_generation was imported from that snapshot.

## Diagnostic exceptions, not product failures

The first controller helper grouped command arguments incorrectly and launched
-m without its module. Child stderr identified the problem. Argument arrays
were preserved explicitly and rechecked; no repository source was changed.
An initial post-freeze path-comparison expression had a PowerShell precedence
error; direct diff-tree inspection and a corrected parenthesized comparison
confirmed the exact five expected paths without rebuilding or changing the ref.

The sandbox blocked the documented 3.14 executable. The same command succeeded
with approved escalation. A trailing Git cleanliness check in that escalated
shell encountered the clone owner's safe-directory check; it was not a Python
failure. Cleanliness is checked separately under the creating sandbox identity.
No interpreter or dependency was replaced or installed.

Post-CLEAN acceptance will repeat this bounded metadata population from fresh
candidate snapshots, floor first. These focused checks are not adoption.
