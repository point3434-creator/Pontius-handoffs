# Campaign note: the three retained phases of design step 7

Drafter: Claude, 2026-09-10; carried unchanged from r002, which corrected the agreement
memory paragraph per reviews M-01/M-02 of solve-run-20260910. This note sequences the
retained solve, export and
agreement invocations on the adopted source `1c706744` and records what the rehearsal chain
measured about the two later phases. Only the solve is requested in this packet. Nothing
here is evidence: every number below comes from the disposable snapshot and feeds nothing.

## Why the phases are sequential

The adopted tool binds each phase to the previous phase's retained bytes. The export plan
must name the retained solve's `teacher.json` and `result.json` by absolute path and
SHA-256; the agreement plan must name the retained export's `teacher.json`,
`blueprint.json` and `result.json` the same way, plus a witness bank. Those digests exist
only after each retained run, so the three phases cannot share one authorization. Each
phase gets its own bound plan, rehearsal, one cold review and one-shot authorization.

## Phase 1 — solve (this packet)

Bound in `identity.json`; requested in `authorization-request.md`. This packet's rehearsal:
all 1,081 hands in 17 s wall at 786 MiB peak; 545 raise-to-2 and 536 CHECK rows; no exact
tie, so the tie census is complete with absence; teacher `c3ffab40…` (241,587 bytes),
the same digest the earlier rehearsals produced.

## Phase 2 — export (next packet, after the retained solve)

Plan: `phase: export`, `declared-full`, the same prerequisites, `inputs.teacher` and
`inputs.producer_result` bound to the retained solve run directory. The tool re-derives the
pool order, requires the producer to be a completed declared-full solve with
`phase_complete` true, checks that repeated export is byte-identical, validates exact key
membership and the direct provider boundary, and retains `teacher.json` (identical bytes)
and `blueprint.json`.

Rehearsal on the rehearsal teacher (`rehearsal/chain-receipt.json`, phase `export-full`):
completed, exit 0, 12.4 s wall, worker 11.6 s, peak 788 MiB; wire 1,010,990 bytes, which
is 37,586 bytes (3.6%) under the 1,048,576-byte cap and 1,635 bytes below the capacity
probe's CHECK/null placeholder size; `source_id` `t1:c3ffab40…`; membership passed with
1,081 hits, exact entries and equal key sets; `blueprint.json` SHA-256 `666021c4…`.

Envelope: the export has no recorded resource decision yet. The rehearsal used 2% of 600 s
and 38% of 2048 MiB; the export packet will propose an envelope on that measured basis and
the controller decides it, as with the solve.

## Phase 3 — agreement (after the retained export)

Plan: `phase: agreement`, `declared-full`, the same prerequisites, three bound inputs from
the retained export, and a `witness_bank` (`seed_start`, `seed_count`, ascending unique
`indices` in 0..15, a disjoint `holdout_seed_start`/`holdout_seed_count`, and a
`sizing_rationale`). The tool scans the whole bank, requires a witness for every hand in
H, then runs one real host session per hand plus three controls (off-pool, CHECK-hit,
changed-stack), 1,084 attempts in all, and reconciles the schedule.

Rehearsal on a four-hand test subset through the real host (phases `subset-solve`,
`subset-export`, `subset-agreement`): completed, exit 0; witness scan 1.56 s for 65,536
draws (48,746 collisions, 74.4%, matching the 1 - C(47,12)/C(52,12) = 0.7468 collision
rate; 16,786 unused; 4 witnesses; census complete); seven host attempts at 0.48–0.52 s
each, classified hit x4, unsupported (off-pool), hit (CHECK-hit), unsupported with zero
table hits (changed-stack); accounting 7 scheduled, 7 observed, 0 missing.

Two facts the agreement packet must settle before its plan is frozen:

1. **Bank sizing.** Per draw, a given hero hand appears with probability
   0.2532 / 1081 = 2.34e-4. For the full pool the IID union bound on any missing hand is
   1081 * (1 - 2.34e-4)^n: about 2.3e-4 at n = 65,536 draws (4,096 seeds x 16 indices),
   about 1.1e-7 at n = 98,304 (6,144 seeds), about 5e-11 at n = 131,072 (8,192 seeds).
   The rationale is a planning estimate; acceptance is the actual census, and an
   incomplete census fails the run without a retry under the same plan. The holdout range
   must be reserved for Slice B and stay disjoint; the rehearsal used a placeholder.
2. **Memory and result size grow with both the bank and H; one observation exists.** The
   four-hand rehearsal with 65,536 draws produced a 20,128,357-byte `result.json` and a
   worker Job peak of 1,560 MiB (the Job limit applies to the worker; the parent, which
   holds every drained observation before writing, is outside it and was not measured).
   The frozen code emits each draw as an observation and also retains all draws inside the
   `witness_scan` report, so the result grows with the bank; it also retains one full host
   session result per scheduled attempt, so the result and both memory owners grow with H
   as well. A single measurement cannot separate fixed runtime cost, per-draw cost and
   per-attempt cost, so no forecast for a larger bank is made here and the solve envelope
   does not transfer. The agreement envelope must come from a full-pool agreement rehearsal
   in a snapshot (about 1,084 attempts at 0.5 s, so roughly nine minutes of host time plus
   the scan), and the controller decides it. If the per-draw retention is judged unnecessary
   (the bank and the deterministic dealer already reproduce witness choice), that is a
   source change with its own review, not a plan edit.

## Determinism and cross-checks

Identical source and plan bytes give identical teacher bytes, and the tool refuses an
export whose repeated encoding differs. The retained solve's teacher digest may be compared
with the rehearsal's `c3ffab40…` as a diagnostic; the retained bytes are the identity.
The export's `source_id` is `t1:` followed by the teacher digest, so the retained
`blueprint.json` binds the retained teacher by construction.

## Not authorized by this packet

The export and agreement invocations, any second solve, any change to the adopted source,
the witness bank, any envelope for phases 2 and 3, and integration into `master`.
