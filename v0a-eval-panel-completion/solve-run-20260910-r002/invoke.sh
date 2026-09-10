#!/usr/bin/env bash
# Retained full-pool T1 solve on the adopted source (design step 7, first of three phases).
#
# Retained mode (default): the checkout and packet are fixed constants; any SOLVE_ROOT or
# REHEARSAL_PK in the environment is refused; authorization.md must exist; the launch is
# claimed atomically (mkdir of invocations/claim.d) so one authorization can never start
# two solves, and a claim survives interruption: a second caller is refused with exit 97
# and the controller decides what an abandoned claim means. Nothing is retried.
#
# Rehearsal mode (REHEARSAL=1): requires an explicit SOLVE_ROOT that is a DETACHED,
# disposable worktree different from the retained checkout; records go under
# <packet>/rehearsal/ (or REHEARSAL_PK/rehearsal/ for fault-path checks). A rehearsal is
# not evidence and feeds nothing.
#
# Every required record write is checked. A failed write before the launch stops without a
# launch (the claim, if already taken, stays on disk). A failed write after the launch, or
# a journal row that cannot be attributed to this attempt, makes the wrapper exit 99
# (EVIDENCE INCOMPLETE) even when the child exited 0. The journal row is attached only when
# exactly one new row appeared and it binds this checkout's result file; an absent, extra or
# mismatching row is recorded as such and never replaced by an older row.
set -u -o pipefail
ADOPTED=1c7067448106cfa2aca3d57be879842d72293c61
RETAINED_ROOT=D:/Pontius-worktrees/eval-panel-solve-20260910
PK=D:/Pontius-handoffs/v0a-eval-panel-completion/solve-run-20260910-r002
GITEXE="C:/Program Files/Git/cmd/git.exe"
PLAN_SHA=c1a6af606cc80841d61b5824913c8a1b6c896988ae4c578127c1dfc08b4f8982
ATTRIBUTE="$PK/journal_attribution.py"
ATTRIBUTE_SHA=a20e760a7e97eb5e37432b81e0dc3e3048bd582299c7e938fc83c8d319d00b14
PREREQ=D:/Pontius-worktrees/eval-panel-prerequisite-20260909/experiments/results/runs
CAP="$PREREQ/a89932e7730e47b8b26b3dafad4f0c41/result.json"
CAP_SHA=29f532a900289c3e7b274646a7fc7332ff1a0aa9e6d74c332319668783d89e53
PRE="$PREREQ/7ce5ab4fb1304abfa592e780d675d9b7/result.json"
PRE_SHA=8a17325eaa07e0f8774dcb7bc2050a3ae233cf47bebfc63a6b59574031fb742f
DEC=D:/Pontius-handoffs/v0a-eval-panel-completion/prerequisite-run-20260909/resource-decision.md
DEC_SHA=037a0de1b8605dc182cdc99ef0ef146e8c5ab08f73d984e4497e5a7a94afe2cf
REHEARSAL="${REHEARSAL:-0}"
now() { date -u +%Y-%m-%dT%H:%M:%SZ; }
sha() { sha256sum "$1" | cut -d' ' -f1; }
canon() { ( cd "$1" && pwd -P ); }
stop() { echo "PRECONDITION $2"; exit "$1"; }

# --- mode and roots ----------------------------------------------------------------------
if [ "$REHEARSAL" != 1 ]; then
  [ -z "${SOLVE_ROOT:-}" ] && [ -z "${REHEARSAL_PK:-}" ] \
    || stop 88 "root or packet overrides are refused in retained mode"
  ROOT="$RETAINED_ROOT"; OUT="$PK/invocations"
  [ -f "$PK/authorization.md" ] || stop 89 "authorization.md missing"
else
  [ -n "${SOLVE_ROOT:-}" ] || stop 87 "rehearsal requires an explicit SOLVE_ROOT"
  ROOT="$SOLVE_ROOT"; OUT="${REHEARSAL_PK:-$PK}/rehearsal"
  [ -d "$ROOT" ] || stop 90 "checkout missing"
  [ "$(canon "$ROOT")" != "$(canon "$RETAINED_ROOT")" ] \
    || stop 86 "rehearsal root is the retained checkout"
  "$GITEXE" -C "$ROOT" symbolic-ref -q HEAD > /dev/null \
    && stop 85 "rehearsal root must be a detached disposable worktree"
fi
LOG="$OUT/invocation-log.jsonl"

# --- preconditions: minimal predicates, each its own exit code ------------------------
[ -d "$ROOT" ] || stop 90 "checkout missing"
cd "$ROOT" || stop 90 "checkout missing"
[ "$("$GITEXE" rev-parse HEAD)" = "$ADOPTED" ] || stop 91 "HEAD != adopted"
[ "$(sha plans/solve.json)" = "$PLAN_SHA" ] || stop 92 "plan hash"
{ [ "$(sha "$CAP")" = "$CAP_SHA" ] && [ "$(sha "$PRE")" = "$PRE_SHA" ] \
  && [ "$(sha "$DEC")" = "$DEC_SHA" ]; } \
  || stop 93 "prerequisite bytes differ from the bound digests"
[ "$(sha "$ATTRIBUTE")" = "$ATTRIBUTE_SHA" ] || stop 82 "journal_attribution.py hash"
PY="$ROOT/.venv/Scripts/python.exe"
"$PY" -I -B -c "import sys; assert sys.version_info[:3] == (3, 14, 6)" || stop 94 "python"
# No run directory beyond those tracked in the adopted tree (the tree tracks old runs).
TRACKED_RUNS=$("$GITEXE" ls-tree -r --name-only HEAD experiments/results/runs \
  | sed "s#^experiments/results/runs/##; s#/.*##" | sort -u)
ONDISK_RUNS=$(ls experiments/results/runs 2>/dev/null | sort -u)
[ "$TRACKED_RUNS" = "$ONDISK_RUNS" ] || stop 95 "untracked run directories present"
[ -z "$("$GITEXE" status --short -- src tools tests pyproject.toml uv.lock .gitattributes .github)" ] \
  || stop 96 "source scope dirty"
for f in claim.d invocation-log.jsonl solve-stdout.json solve-stderr.txt \
         solve-journal-row.jsonl retained-files.txt; do
  [ ! -e "$OUT/$f" ] || stop 97 "an invocation was already started ($f exists)"
done
ROWS_BEFORE=$(wc -l < execution_journal.jsonl) || stop 81 "journal unreadable"
echo "PRECONDITIONS ok at $(now); journal rows before: $ROWS_BEFORE"

# --- exclusive claim, then checked start record --------------------------------------
mkdir -p "$OUT" || stop 83 "cannot create the record directory"
mkdir "$OUT/claim.d" || stop 97 "claim refused: another caller already claimed this launch"
START=$(now)
printf '{"claimed_utc":"%s","pid":%s,"root":"%s","rehearsal":%s}\n' "$START" "$$" "$ROOT" \
  "$REHEARSAL" > "$OUT/claim.d/claim.json" \
  || { echo "RECORD claim record failed; claim held; no launch"; exit 98; }
printf '{"phase":"solve","event":"start","utc":"%s","plan_sha256":"%s","reviewed_commit":"%s","rehearsal":%s,"journal_rows_before":%s}\n' \
  "$START" "$PLAN_SHA" "$ADOPTED" "$REHEARSAL" "$ROWS_BEFORE" >> "$LOG" \
  || { echo "RECORD start record failed; claim held; no launch"; exit 98; }
grep -q '"event":"start"' "$LOG" || { echo "RECORD start record unreadable; claim held; no launch"; exit 98; }

# --- exactly one launch -------------------------------------------------------------------
set -o noclobber
t0=$(date +%s)
env -i SystemRoot="${SystemRoot:-$SYSTEMROOT}" TEMP="$TEMP" TMP="$TMP" PONTIUS_GIT="$GITEXE" \
  PYTHONDONTWRITEBYTECODE=1 \
  "$PY" -B -P -W error::ResourceWarning "$ROOT/tools/v0a_eval_panel.py" run \
  --reviewed-commit "$ADOPTED" --plan "$ROOT/plans/solve.json" \
  > "$OUT/solve-stdout.json" 2> "$OUT/solve-stderr.txt"
rc=$?
set +o noclobber
wall=$(( $(date +%s) - t0 ))
echo "PHASE solve exit=$rc wall=${wall}s"

# --- evidence: every write checked; journal row attributed, never assumed ---------------
EVIDENCE=complete
[ -f "$OUT/solve-stdout.json" ] && [ -f "$OUT/solve-stderr.txt" ] || EVIDENCE=incomplete
ROWS_AFTER=$(wc -l < execution_journal.jsonl) || { ROWS_AFTER=unreadable; EVIDENCE=incomplete; }
"$PY" -I -B "$ATTRIBUTE" execution_journal.jsonl "$ROWS_BEFORE" "$ADOPTED" "$ROOT" \
  "$OUT/solve-journal-row.jsonl" > "$OUT/journal-attribution.txt"
ATTR_RC=$?
JOURNAL_ROW=$(head -n 1 "$OUT/journal-attribution.txt" | cut -d' ' -f1)
[ "$ATTR_RC" -eq 0 ] && [ "$JOURNAL_ROW" = BOUND ] || EVIDENCE=incomplete
STDOUT_SHA=$(sha "$OUT/solve-stdout.json") || { STDOUT_SHA=unavailable; EVIDENCE=incomplete; }
STDERR_SHA=$(sha "$OUT/solve-stderr.txt") || { STDERR_SHA=unavailable; EVIDENCE=incomplete; }
if [ "$JOURNAL_ROW" = BOUND ]; then
  ROW_SHA=$(sha "$OUT/solve-journal-row.jsonl") || { ROW_SHA=unavailable; EVIDENCE=incomplete; }
else
  ROW_SHA=absent
fi
(
  for d in experiments/results/runs/*/; do
    name=$(basename "$d"); echo "$TRACKED_RUNS" | grep -qx "$name" && continue
    for f in "$d"*; do
      h=$(sha "$f") || exit 1; n=$(wc -c < "$f") || exit 1
      printf '%s  %s  %s\n' "$h" "$n" "$f" || exit 1
    done
  done
) > "$OUT/retained-files.txt" || EVIDENCE=incomplete
printf '{"phase":"solve","event":"end","utc":"%s","exit":%s,"wall_seconds":%s,"journal_rows_before":%s,"journal_rows_after":"%s","journal_row":"%s","journal_row_sha256":"%s","stdout_sha256":"%s","stderr_sha256":"%s","evidence":"%s"}\n' \
  "$(now)" "$rc" "$wall" "$ROWS_BEFORE" "$ROWS_AFTER" "$JOURNAL_ROW" "$ROW_SHA" "$STDOUT_SHA" \
  "$STDERR_SHA" "$EVIDENCE" >> "$LOG" || { echo "RECORD end record failed"; EVIDENCE=incomplete; }
echo "JOURNAL $(cat "$OUT/journal-attribution.txt")"
echo "RETAINED files:"; cat "$OUT/retained-files.txt"
echo "DONE at $(now): solve exit $rc, evidence $EVIDENCE (rehearsal=$REHEARSAL)"
[ "$rc" -eq 0 ] || exit "$rc"
[ "$EVIDENCE" = complete ] || { echo "EVIDENCE INCOMPLETE"; exit 99; }
exit 0
