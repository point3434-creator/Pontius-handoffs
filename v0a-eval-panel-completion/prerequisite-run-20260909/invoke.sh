#!/usr/bin/env bash
# Retained capacity/preflight invocation on the bound source. Run once, under the
# controller's authorization recorded in authorization.md. Each phase runs exactly once;
# an interrupted or failed phase stops the sequence and its records are kept.
set -u
ADOPTED=beb84be566aa28029284bd35c526d33cd27af369
ROOT=D:/Pontius-worktrees/eval-panel-prerequisite-20260909
PK=D:/Pontius-handoffs/v0a-eval-panel-completion/prerequisite-run-20260909
GITEXE="C:/Program Files/Git/cmd/git.exe"
PY="$ROOT/.venv/Scripts/python.exe"
LOG="$PK/invocation-log.jsonl"
CAP_SHA=6ad3e205058de941a695e04a966cb966d255369b0f910cfcee25a3426636bae1
PRE_SHA=d2e5c04cf5c4ba2543aca91b6705b5593464989a331bc0400a76a966e59253c5
now() { date -u +%Y-%m-%dT%H:%M:%SZ; }
sha() { sha256sum "$1" | cut -d' ' -f1; }
mkdir -p "$PK/invocations"

# --- authorization record, written before any launch ---------------------------------
if [ ! -f "$PK/authorization.md" ]; then
  {
    echo "# Controller authorization"
    echo
    echo "Received via chat 2026-09-09; recorded at $(now) before any launch."
    echo
    echo 'Controller, verbatim: "I authorize one retained capacity invocation and, on'
    echo 'nonempty capacity success, one retained preflight invocation on'
    echo 'beb84be566aa28029284bd35c526d33cd27af369 as bound in identity.json."'
    echo
    echo "Scope: exactly what authorization-request.md requested; nothing else."
  } > "$PK/authorization.md"
fi

# --- preconditions --------------------------------------------------------------------
cd "$ROOT" || { echo "PRECONDITION checkout missing"; exit 90; }
[ "$("$GITEXE" rev-parse HEAD)" = "$ADOPTED" ] || { echo "PRECONDITION HEAD != adopted"; exit 91; }
[ "$(sha plans/capacity.json)" = "$CAP_SHA" ] || { echo "PRECONDITION capacity plan hash"; exit 92; }
[ "$(sha plans/preflight.json)" = "$PRE_SHA" ] || { echo "PRECONDITION preflight plan hash"; exit 93; }
"$PY" -I -B -c "import sys; assert sys.version_info[:3] == (3, 14, 6)" || { echo "PRECONDITION python"; exit 94; }
# Minimal predicate: no run directory beyond those tracked in the adopted tree.
TRACKED_RUNS=$("$GITEXE" ls-tree -r --name-only HEAD experiments/results/runs | sed "s#^experiments/results/runs/##; s#/.*##" | sort -u)
ONDISK_RUNS=$(ls experiments/results/runs 2>/dev/null | sort -u)
[ "$TRACKED_RUNS" = "$ONDISK_RUNS" ] || { echo "PRECONDITION untracked run directories present"; exit 95; }
[ -z "$("$GITEXE" status --short -- src tools tests pyproject.toml uv.lock .gitattributes .github)" ] \
  || { echo "PRECONDITION source scope dirty"; exit 96; }
echo "PRECONDITIONS ok at $(now); journal rows before: $(wc -l < execution_journal.jsonl)"

run_phase() {
  local ph=$1 start rc t0 wall
  start=$(now)
  printf '{"phase":"%s","event":"start","utc":"%s","plan_sha256":"%s","reviewed_commit":"%s"}\n' \
    "$ph" "$start" "$(sha "plans/$ph.json")" "$ADOPTED" >> "$LOG"
  t0=$(date +%s)
  env -i SystemRoot="${SystemRoot:-$SYSTEMROOT}" TEMP="$TEMP" TMP="$TMP" PONTIUS_GIT="$GITEXE" \
    PYTHONDONTWRITEBYTECODE=1 \
    "$PY" -B -P -W error::ResourceWarning "$ROOT/tools/v0a_eval_panel.py" run \
    --reviewed-commit "$ADOPTED" --plan "$ROOT/plans/$ph.json" \
    > "$PK/invocations/$ph-stdout.json" 2> "$PK/invocations/$ph-stderr.txt"
  rc=$?
  wall=$(( $(date +%s) - t0 ))
  tail -1 execution_journal.jsonl | sed 's/\r$//' > "$PK/invocations/$ph-journal-row.jsonl"
  printf '{"phase":"%s","event":"end","utc":"%s","exit":%s,"wall_seconds":%s,"stdout_sha256":"%s","stderr_sha256":"%s","journal_row_sha256":"%s"}\n' \
    "$ph" "$(now)" "$rc" "$wall" "$(sha "$PK/invocations/$ph-stdout.json")" \
    "$(sha "$PK/invocations/$ph-stderr.txt")" "$(sha "$PK/invocations/$ph-journal-row.jsonl")" >> "$LOG"
  echo "PHASE $ph exit=$rc wall=${wall}s stderr_bytes=$(wc -c < "$PK/invocations/$ph-stderr.txt")"
  return "$rc"
}

# --- capacity -------------------------------------------------------------------------
run_phase capacity
CAP_RC=$?
CAP_GATE=$("$PY" -I -B -c '
import json, sys
r = json.load(open(sys.argv[1]))
rows = [o for o in r.get("observations", []) if o.get("kind") == "capacity"]
ok = (r.get("status") == "completed" and r.get("cleanup_verified") is True and len(rows) == 1
      and (rows[0]["probe"].get("largest_fitting") or 0) > 0
      and rows[0].get("boundary_retention") == "complete")
print("nonempty-success" if ok else "stop")
' "$PK/invocations/capacity-stdout.json" 2>/dev/null || echo stop)
echo "CAPACITY gate: $CAP_GATE (exit $CAP_RC)"
printf '{"event":"capacity_gate","utc":"%s","decision":"%s"}\n' "$(now)" "$CAP_GATE" >> "$LOG"
if [ "$CAP_GATE" != "nonempty-success" ]; then
  echo "SEQUENCE stopped after capacity; preflight not run"
  exit 10
fi

# --- preflight (conditional) ----------------------------------------------------------
run_phase preflight
PRE_RC=$?

# --- bind retained files ---------------------------------------------------------------
{
  for d in experiments/results/runs/*/; do
    name=$(basename "$d"); echo "$TRACKED_RUNS" | grep -qx "$name" && continue
    for f in "$d"*; do printf '%s  %s  %s\n' "$(sha "$f")" "$(wc -c < "$f")" "$f"; done
  done
} > "$PK/invocations/retained-files.txt"
echo "RETAINED files:"; cat "$PK/invocations/retained-files.txt"
echo "JOURNAL rows after: $(wc -l < execution_journal.jsonl)"
echo "SEQUENCE done at $(now): capacity exit $CAP_RC, preflight exit $PRE_RC"
exit $PRE_RC
