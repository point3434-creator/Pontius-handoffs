# What follows this phase

Agreement is the last of design step 7's three retained phases. When it has run, Slice A's
bridge is complete: a teacher solved for the full pool, exported to a blueprint artifact, and
reproduced through the unchanged host for every hand.

## What Slice A will and will not have established

It will have established an instrument. The exported artifact reproduces the teacher's action
through the real host for 1,081 hands on one board, one replayed prefix and one stack depth,
with the schedule reconciled and the census complete.

It will not have established anything about play. Teacher strength, equilibrium quality,
chip outcomes and transfer to other boards, budgets or stack depths are all untouched. Those
are Slice B's questions, and Slice B must draw its population from the reserved holdout seed
range, never from the witness draws selected here.

## The consolidation the controller has agreed

The launch logic is now written three times: solve, export and agreement. The controller has
agreed to consolidate it into one small tested runner with phase-specific data, after this
phase rather than before it, so that the runner is built from three worked examples.

The benefit must come from fewer duplicated rules and explicit state transitions, not from
the language change alone. Two concrete targets:

- **Collapse the duplicated pins.** Each prerequisite digest currently lives in the adopted
  tool's constants, in the plan, and in the wrapper. This packet already removed the
  equivalent duplication for the producer inputs by reading them from the plan; the same
  applies to the prerequisites.
- **Make the state machine explicit.** The wrapper progresses from unclaimed to claimed to
  launched to recorded to verified, but that progression is implicit in straight-line code
  with exit codes scattered through it, which is why each review round has found another
  wrinkle in it. One runner with named steps, the exit codes as a table, and a single
  function deciding status from recorded state would close that class of finding.

One constraint worth stating before it is written: the runner must stay independent of the
code it launches. Standard library only, no project imports, separate process. Bash gives
that for free today; a Python runner that imports project modules would let a broken source
take down the recorder, which is the one thing the wrapper exists to protect.

The published solve and export packets stay frozen. Consolidation applies to future phases,
not retroactively to executed evidence.

## Carried findings for the Slice B interface

- Retaining all 98,304 witness draws dominates memory and result size, and is redundant given
  the bank and the deterministic dealer. Changing it means changing adopted source.
- The full pool leaves the artifact with no negative space, so the default path has one
  synthetic witness rather than a population. Holding back a small number of hands would
  give a real off-pool set testable through the host.
- The parent process's live peak memory remains unmeasured for every phase; the correct
  method is to sample the process tree rather than the launched process.
- Earlier carried items stand: v2 state reconciliation, the stderr cap, the identity charset
  regex and v2 config digest binding.
