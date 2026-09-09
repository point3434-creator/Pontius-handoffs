# Measured report: retained capacity and preflight on beb84be5

Drafter: Claude, 2026-09-09. Both authorized invocations completed. This report
returns the measurements to the controller for the resource decision that design
step 4 requires. Estimates are labeled as estimates; nothing here is a full-pool
solve, an export, or an agreement result.

## Identity

- Source: `beb84be566aa28029284bd35c526d33cd27af369` (tree `d26c3fb1`, identical to
  reviewed `a40e29ca`). Both journal rows: `source_verified: true`,
  `source_sha256 43ee826f…`.
- Checkout: `D:/Pontius-worktrees/eval-panel-prerequisite-20260909`, branch
  `claude/eval-panel-prerequisite`; CPython 3.14.6 (`tags/v3.14.6:c63aec6`, MSC
  v.1944, 64-bit) from the locked `uv` environment.
- Plans: capacity `6ad3e205…` (blob `5040350e`), preflight `d2e5c04c…` (blob
  `6f8d92d2`); the tool's retained `plan_sha256` equals each.
- Environment: scrubbed (`SystemRoot TEMP TMP`), `PONTIUS_GIT=C:/Program
  Files/Git/cmd/git.exe`, `PYTHONDONTWRITEBYTECODE=1`, `-B -P -W
  error::ResourceWarning`, `--reviewed-commit`, no `--development`.
- Authorization: `authorization.md` (verbatim controller wording, recorded before
  launch). Invocation timeline: `invocation-log.jsonl`. One precondition stop before
  any launch is recorded in `precondition-stop-01.md`; it consumed nothing.

## Retained evidence (in the checkout; never copied into this packet)

- **capacity** — Directory: `experiments/results/runs/a89932e7730e47b8b26b3dafad4f0c41/`;
  `result.json` SHA-256: `29f532a9…` (2,789 B); Journal row: row 60, 19:09:44Z
- **preflight** — Directory: `experiments/results/runs/7ce5ab4fb1304abfa592e780d675d9b7/`;
  `result.json` SHA-256: `8a17325e…` (20,722 B); Journal row: row 61, 19:10:17Z

`runtimes.json` in both: `1b058fba…`. Boundary artifact
`capacity-boundary-1081.blueprint.json`: 1,012,625 bytes, SHA-256 `078171ff…`,
bound in the capacity result (`boundary_retention: complete`). Journal rows and
STATUS.md are committed on `claude/eval-panel-prerequisite`; run directories stay
on disk under the gitignored retained path and are mirrored. Full listing with
hashes: `invocations/retained-files.txt`. Invocation receipts (stdout, stderr,
exit, wall): `invocations/`.

## Capacity (design mechanism 4)

- Status `completed`, exit 0, 6 s wall; worker 2.1 s; probe body 1.19 s elapsed /
  1.17 s CPU (`untraced-body-v1`); peak worker Job memory 794.4 MiB;
  `cleanup_verified: true`, all twelve cleanup steps `ok`; stderr empty.
- **Capacity-selected H = 1,081 — the whole compatible hero universe fits.**
  `bytes_at_largest` 1,012,625 of the 1,048,576-byte cap (35,951 bytes headroom,
  3.4%); `all_fit: true`; no failing prefix exists in the domain
  (`bytes_at_next: null`); `one_row_failure: false`.
- Wire bytes were measured on the real codec with placeholder CHECK/null rows and
  real replayed keys, per the design. Solved rows carry the same fixed-width
  `source_id` and action encoding, so the solved artifact is expected to fit; the
  design still requires an independent recheck of the final solved bytes at export.

## Preflight (design mechanism 2, declared-full sample)

Status `completed`, exit 0, 32 s wall; worker 31.3 s; peak worker Job memory 777.3
MiB; `cleanup_verified: true`; stderr empty; `sample_complete: true`; 5/5 units
complete with all seven stages; every comparison `passed`.

- **dev `AdAs`** — Board: 2c7d9hJsQc; Production action: raise-to-2; Totals (check / bet): 1,430 /
  2,860; Class: agree; prod cold: 0.066 s; prod warm: 0.014 s; ref build: 1.50 s; forced CHECK: 0.81
  s; forced BET: 0.91 s; best resp.: 2.49 s
- **dev `KdKh`** — Board: 2c7d9hJsQc; Production action: raise-to-2; Totals (check / bet): 1,438 /
  2,876; Class: agree; prod cold: 0.020 s; prod warm: 0.014 s; ref build: 1.71 s; forced CHECK: 0.95
  s; forced BET: 0.93 s; best resp.: 2.53 s
- **dev `8dTd`** — Board: 2c7d9hJsQc; Production action: raise-to-2; Totals (check / bet): 1,914 /
  3,828; Class: agree; prod cold: 0.015 s; prod warm: 0.014 s; ref build: 1.69 s; forced CHECK: 0.92
  s; forced BET: 0.92 s; best resp.: 2.52 s
- **dev `3c4d`** — Board: 2c7d9hJsQc; Production action: check; Totals (check / bet): −1,962 /
  −3,924; Class: agree; prod cold: 0.015 s; prod warm: 0.014 s; ref build: 1.65 s; forced CHECK:
  0.93 s; forced BET: 0.91 s; best resp.: 3.16 s
- **control `2c3d`** — Board: TsJsQsKsAs; Production action: check; Totals (check / bet): 0 / 0;
  Class: **tie** (exact); prod cold: 0.071 s; prod warm: 0.014 s; ref build: 1.66 s; forced CHECK:
  0.93 s; forced BET: 0.93 s; best resp.: 2.48 s

Observations:
- The `J_bet = 2·J_check` identity holds on every unit (bet totals are exactly
  twice the check totals), as the design predicts for this two-action root.
- Cold/warm is real and labeled: the first development hand ran against an empty
  ranker cache (0 → 991 entries) and cost 0.066 s; later hands on the same board
  reuse it and cost 0.014–0.020 s. The royal control is cold for its own board
  (1,081 → 2,072 entries), 0.071 s. `production_warm` repeats match production.
- The sealed singleton reference costs ≈ 5.7 s per hand (build 1.5–1.7 s, two forced
  evaluations ≈ 0.9 s each, best response 2.5–3.2 s). It is sample-only by design.
- All timings carry `timing_mode: untraced-body-v1`; `traced_peak_status:
  not_collected`. Memory is the native Job peak of the whole worker process.

## Full-pool estimate (the tool's own; an estimate, not a bound)

`full_pool_estimate`: production only, 1,081 hands, sample 4, `untraced-body-v1`:
**min 15.8 s, mean 31.1 s, max 71.4 s.** Assumptions as recorded: single untraced
body invocations; the first hand cold, later hands reusing cached villain ranks;
the sealed reference excluded. The max is the cold first-hand cost × 1,081 and is
pessimistic; a full-H solve on one board warms after the first hand, so the
realistic production cost is near the min. Initialization is negligible
(< 1 ms). Neither reference nor export cost is in this number.

For calibration: the r001 development diagnostic, taken under allocation tracing,
projected 1.1–5.9 minutes for the same work. That was I-01; the retained
untraced figure is roughly 4–5× lower.

## Inputs to the resource decision

If the controller authorizes a full-pool T1 solve on the development board for the
whole capacity-selected H = 1,081:

- Production time, measured basis: ≈ 16–71 s (estimate above); a limit of 600 s
  leaves ≥ 8× headroom.
- Memory, measured basis: ≈ 0.8 GiB worker Job peak for capacity and preflight; a
  2048 MiB Job limit leaves ≈ 2.5× headroom. The solve holds one hand's
  enumeration at a time, so no growth with H is expected beyond the artifact bytes.
- Artifact: 1,012,625 wire bytes at H = 1,081 with 3.4% headroom under the cap.
- The reference over all of H is not estimated because the design makes it
  sample-only; if the controller wants the first nonzero-return exact tie recorded
  during the solve (design §3), that is a solve-time scan, not a reference over H.

The decision — the specific resource envelope and whether H = 1,081 is the pool —
is the controller's. This report supplies no authorization for the solve, export,
or agreement phases.

## Limits

One board; a fixed four-hand sample plus one control; timing on one machine at one
moment; no tie census over H; no export bytes measured; no host agreement. The
rehearsal in `rehearsal/` is not evidence and was not used for any figure above
except the calibration sentence, which cites r001.
