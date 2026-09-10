#!/usr/bin/env bash
# Retained full-pool T1 solve on the adopted source (design step 7, first of three phases).
# Runs exactly once, under the controller's authorization recorded in authorization.md.
# REHEARSAL=1 runs the same command, environment and plan bytes against a disposable
# snapshot (SOLVE_ROOT overridden) and writes its records under rehearsal/. A rehearsal
# is not evidence and feeds nothing. An interrupted or failed invocation stops here and
# keeps every record; it is never retried as if it had not happened.
set -u
ADOPTED=1c7067448106cfa2aca3d57be879842d72293c61
ROOT="${SOLVE_ROOT:-D:/Pontius-worktrees/eval-panel-solve-20260910}"
PK="${SOLVE_PK:-D:/Pontius-handoffs/v0a-eval-panel-completion/solve-run-20260910}"
GITEXE="C:/Program Files/Git/cmd/git.exe"
PY="$ROOT/.venv/Scripts/python.exe"
PLAN_SHA=c1a6af606cc80841d61b5824913c8a1b6c896988ae4c578127c1dfc08b4f8982
PREREQ=D:/Pontius-worktrees/eval-panel-prerequisite-20260909/experiments/results/runs
CAP="$PREREQ/a89932e7730e47b8b26b3dafad4f0c41/result.json"
CAP_SHA=29f532a900289c3e7b274646a7fc7332ff1a0aa9e6d74c332319668783d89e53
PRE="$PREREQ/7ce5ab4fb1304abfa592e780d675d9b7/result.json"
PRE_SHA=8a17325eaa07e0f8774dcb7bc2050a3ae233cf47bebfc63a6b59574031fb742f
DEC=D:/Pontius-handoffs/v0a-eval-panel-completion/prerequisite-run-20260909/resource-decision.md
DEC_SHA=037a0de1b8605dc182cdc99ef0ef146e8c5ab08f73d984e4497e5a7a94afe2cf
REHEARSAL="${REHEARSAL:-0}"
if [ "$REHEARSAL" = 1 ]; then OUT="$PK/rehearsal"; else OUT="$PK/invocations"; fi
LOG="$OUT/invocation-log.jsonl"
now() { date -u +%Y-%m-%dT%H:%M:%SZ; }
sha() { sha256sum "$1" | cut -d' ' -f1; }
mkdir -p "$OUT"

# --- preconditions: minimal predicates, each its own exit code ------------------------
if [ "$REHEARSAL" != 1 ]; then
  [ -f "$PK/authorization.md" ] || { echo "PRECONDITION authorization.md missing"; exit 89; }
  [ ! -s "$LOG" ] || { echo "PRECONDITION an invocation was already started"; exit 97; }
fi
cd "$ROOT" || { echo "PRECONDITION checkout missing"; exit 90; }
[ "$("$GITEXE" rev-parse HEAD)" = "$ADOPTED" ] || { echo "PRECONDITION HEAD != adopted"; exit 91; }
[ "$(sha plans/solve.json)" = "$PLAN_SHA" ] || { echo "PRECONDITION plan hash"; exit 92; }
{ [ "$(sha "$CAP")" = "$CAP_SHA" ] && [ "$(sha "$PRE")" = "$PRE_SHA" ] && [ "$(sha "$DEC")" = "$DEC_SHA" ]; } \
  || { echo "PRECONDITION prerequisite bytes differ from the bound digests"; exit 93; }
"$PY" -I -B -c "import sys; assert sys.version_info[:3] == (3, 14, 6)" || { echo "PRECONDITION python"; exit 94; }
# No run directory beyond those tracked in the adopted tree (the tree tracks old runs).
TRACKED_RUNS=$("$GITEXE" ls-tree -r --name-only HEAD experiments/results/runs | sed "s#^experiments/results/runs/##; s#/.*##" | sort -u)
ONDISK_RUNS=$(ls experiments/results/runs 2>/dev/null | sort -u)
[ "$TRACKED_RUNS" = "$ONDISK_RUNS" ] || { echo "PRECONDITION untracked run directories present"; exit 95; }
[ -z "$("$GITEXE" status --short -- src tools tests pyproject.toml uv.lock .gitattributes .github)" ] \
  || { echo "PRECONDITION source scope dirty"; exit 96; }
echo "PRECONDITIONS ok at $(now); journal rows before: $(wc -l < execution_journal.jsonl)"

# --- exactly one invocation --------------------------------------------------------------
start=$(now)
printf '{"phase":"solve","event":"start","utc":"%s","plan_sha256":"%s","reviewed_commit":"%s","rehearsal":%s}\n' \
  "$start" "$PLAN_SHA" "$ADOPTED" "$REHEARSAL" >> "$LOG"
t0=$(date +%s)
env -i SystemRoot="${SystemRoot:-$SYSTEMROOT}" TEMP="$TEMP" TMP="$TMP" PONTIUS_GIT="$GITEXE" \
  PYTHONDONTWRITEBYTECODE=1 \
  "$PY" -B -P -W error::ResourceWarning "$ROOT/tools/v0a_eval_panel.py" run \
  --reviewed-commit "$ADOPTED" --plan "$ROOT/plans/solve.json" \
  > "$OUT/solve-stdout.json" 2> "$OUT/solve-stderr.txt"
rc=$?
wall=$(( $(date +%s) - t0 ))
tail -1 execution_journal.jsonl | sed 's/\r$//' > "$OUT/solve-journal-row.jsonl"
printf '{"phase":"solve","event":"end","utc":"%s","exit":%s,"wall_seconds":%s,"stdout_sha256":"%s","stderr_sha256":"%s","journal_row_sha256":"%s"}\n' \
  "$(now)" "$rc" "$wall" "$(sha "$OUT/solve-stdout.json")" "$(sha "$OUT/solve-stderr.txt")" \
  "$(sha "$OUT/solve-journal-row.jsonl")" >> "$LOG"
echo "PHASE solve exit=$rc wall=${wall}s stderr_bytes=$(wc -c < "$OUT/solve-stderr.txt")"

# --- bind the retained files (new run directories only) ----------------------------------
{
  for d in experiments/results/runs/*/; do
    name=$(basename "$d"); echo "$TRACKED_RUNS" | grep -qx "$name" && continue
    for f in "$d"*; do printf '%s  %s  %s\n' "$(sha "$f")" "$(wc -c < "$f")" "$f"; done
  done
} > "$OUT/retained-files.txt"
echo "RETAINED files:"; cat "$OUT/retained-files.txt"
echo "JOURNAL rows after: $(wc -l < execution_journal.jsonl)"
echo "DONE at $(now): solve exit $rc (rehearsal=$REHEARSAL)"
exit $rc
