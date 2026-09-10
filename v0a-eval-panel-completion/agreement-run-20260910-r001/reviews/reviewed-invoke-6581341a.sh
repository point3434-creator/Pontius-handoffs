#!/usr/bin/env bash
# Retained full-pool host agreement on the adopted source (design step 7, third of three).
#
# Derived from the export wrapper. Two deliberate changes, each answering a finding the
# export round's reviews produced:
#
#   1. The required launch environment is checked BEFORE the claim (exit 79). The export
#      wrapper expands SystemRoot/SYSTEMROOT, TEMP and TMP under `set -u` below the claim,
#      so a shell lacking any of them consumes the one-shot claim and starts no child. That
#      was graded Advisory there because reopening a frozen wrapper for it was not worth the
#      cost; this is a new wrapper, so the check costs nothing and the hazard is removed.
#   2. The producer input digests are verified against the PLAN rather than against a second
#      set of constants in this script (exit 80). The export wrapper pinned each input digest
#      twice, in the plan and in the wrapper, which is a drift hazard with no benefit: the
#      plan digest is already pinned here, so the plan is the single source of truth for what
#      the inputs must be.
#
# Retained mode (default): the checkout and packet are fixed constants; any AGREEMENT_ROOT or
# REHEARSAL_PK in the environment is refused, including an empty one; authorization.md must
# exist; the launch is claimed atomically (mkdir of invocations/claim.d) so one authorization
# can never start two agreement runs, and a claim survives interruption: a second caller is
# refused with exit 97 and the controller decides what an abandoned claim means.
#
# Rehearsal mode (REHEARSAL=1): requires an explicit AGREEMENT_ROOT that is a DETACHED,
# disposable worktree different from the retained checkout; records go under
# <packet>/rehearsal/ (or REHEARSAL_PK/rehearsal/ for fault-path checks). A rehearsal is not
# evidence and feeds nothing. REHEARSAL, when set at all, must be exactly 0 or 1.
#
# Exit status, in this precedence:
#   1. any nonzero status from the agreement child is returned unchanged, whether or not the
#      evidence is complete; the end record still states which evidence is missing;
#   2. otherwise, a child that exited 0 whose captures, digests, retained-file listing or
#      journal attribution are incomplete yields 99 (EVIDENCE INCOMPLETE);
#   3. otherwise 0.
# No path reports success with incomplete evidence. A refusal before successful claim
# acquisition creates no new claim and starts no child; an existing claim remains consumed.
# After acquisition, every failure leaves that claim consumed and the script never removes
# it; only the controller can resolve an abandoned or ambiguous claim. Journal attribution
# attaches exactly one new matching row and never substitutes an older row.
set -u -o pipefail
ADOPTED=1c7067448106cfa2aca3d57be879842d72293c61
RETAINED_ROOT=D:/Pontius-worktrees/eval-panel-agreement-20260910
PK=D:/Pontius-handoffs/v0a-eval-panel-completion/agreement-run-20260910-r001
GITEXE="C:/Program Files/Git/cmd/git.exe"
PLAN_SHA=525944ae6185ec683bb09dcd15727e665d9c9b2911048bd8bec210580ff60b01
ATTRIBUTE="$PK/journal_attribution.py"
ATTRIBUTE_SHA=a20e760a7e97eb5e37432b81e0dc3e3048bd582299c7e938fc83c8d319d00b14
INPUT_GUARD="$PK/verify_plan_inputs.py"
INPUT_GUARD_SHA=3e85adaed78e56657c447161c172a7d3ef3ca67c32c10691593e4e5cef023d5c
PREREQ=D:/Pontius-worktrees/eval-panel-prerequisite-20260909/experiments/results/runs
CAP="$PREREQ/a89932e7730e47b8b26b3dafad4f0c41/result.json"
CAP_SHA=29f532a900289c3e7b274646a7fc7332ff1a0aa9e6d74c332319668783d89e53
PRE="$PREREQ/7ce5ab4fb1304abfa592e780d675d9b7/result.json"
PRE_SHA=8a17325eaa07e0f8774dcb7bc2050a3ae233cf47bebfc63a6b59574031fb742f
DEC=D:/Pontius-handoffs/v0a-eval-panel-completion/prerequisite-run-20260909/resource-decision.md
DEC_SHA=037a0de1b8605dc182cdc99ef0ef146e8c5ab08f73d984e4497e5a7a94afe2cf
# Only an UNSET variable takes the default; an explicitly empty value is rejected below.
REHEARSAL="${REHEARSAL-0}"
now() { date -u +%Y-%m-%dT%H:%M:%SZ; }
sha() { sha256sum "$1" | cut -d' ' -f1; }
canon() { ( cd "$1" && pwd -P ); }
stop() { echo "PRECONDITION $2"; exit "$1"; }

# --- required launch environment, checked BEFORE anything is claimed --------------------
# These are expanded at the launch line below, under `set -u`. Checking them here means a
# shell that lacks one refuses without consuming the claim, rather than aborting after it.
[ -n "${SystemRoot:-${SYSTEMROOT:-}}" ] || stop 79 "SystemRoot (or SYSTEMROOT) is not set"
[ -n "${TEMP:-}" ] || stop 79 "TEMP is not set"
[ -n "${TMP:-}" ] || stop 79 "TMP is not set"

# --- mode and roots ----------------------------------------------------------------------
case "$REHEARSAL" in
  0|1) ;;
  *) stop 84 "REHEARSAL, when set, must be exactly 0 or 1 (empty is not 0)" ;;
esac
if [ "$REHEARSAL" = 0 ]; then
  [ -z "${AGREEMENT_ROOT+x}" ] && [ -z "${REHEARSAL_PK+x}" ] \
    || stop 88 "root or packet overrides are refused in retained mode"
  ROOT="$RETAINED_ROOT"; OUT="$PK/invocations"
  [ -f "$PK/authorization.md" ] || stop 89 "authorization.md missing"
else
  [ -n "${AGREEMENT_ROOT:-}" ] || stop 87 "rehearsal requires an explicit AGREEMENT_ROOT"
  ROOT="$AGREEMENT_ROOT"; OUT="${REHEARSAL_PK:-$PK}/rehearsal"
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
[ "$(sha plans/agreement.json)" = "$PLAN_SHA" ] || stop 92 "plan hash"
{ [ "$(sha "$CAP")" = "$CAP_SHA" ] && [ "$(sha "$PRE")" = "$PRE_SHA" ] \
  && [ "$(sha "$DEC")" = "$DEC_SHA" ]; } \
  || stop 93 "prerequisite bytes differ from the bound digests"
[ "$(sha "$ATTRIBUTE")" = "$ATTRIBUTE_SHA" ] || stop 82 "journal_attribution.py hash"
[ "$(sha "$INPUT_GUARD")" = "$INPUT_GUARD_SHA" ] || stop 82 "verify_plan_inputs.py hash"
PY="$ROOT/.venv/Scripts/python.exe"
"$PY" -I -B -c "import sys; assert sys.version_info[:3] == (3, 14, 6)" || stop 94 "python"
# --- producer input digests, read from the plan (before claim acquisition) --------------
"$PY" -I -B "$INPUT_GUARD" plans/agreement.json || stop 80 "plan inputs differ from their bound digests"
# --- end producer input digests ---------------------------------------------------------
# No run directory beyond those tracked in the adopted tree (the tree tracks old runs).
TRACKED_RUNS=$("$GITEXE" ls-tree -r --name-only HEAD experiments/results/runs \
  | sed "s#^experiments/results/runs/##; s#/.*##" | sort -u)
ONDISK_RUNS=$(ls experiments/results/runs 2>/dev/null | sort -u)
[ "$TRACKED_RUNS" = "$ONDISK_RUNS" ] || stop 95 "untracked run directories present"
[ -z "$("$GITEXE" status --short -- src tools tests pyproject.toml uv.lock .gitattributes .github)" ] \
  || stop 96 "source scope dirty"
for f in claim.d invocation-log.jsonl agreement-stdout.json agreement-stderr.txt \
         agreement-journal-row.jsonl retained-files.txt; do
  [ ! -e "$OUT/$f" ] || stop 97 "an invocation was already started ($f exists)"
done
ROWS_BEFORE=$(wc -l < execution_journal.jsonl) || stop 81 "journal unreadable"
echo "PRECONDITIONS ok at $(now); journal rows before: $ROWS_BEFORE"

# --- exclusive claim, then checked start record --------------------------------------
mkdir -p "$OUT" || stop 83 "cannot create the record directory"
# A refused mkdir is a refusal to claim, whether the cause is an existing claim or a denied
# directory. Both keep the launch from happening; the message states the observed cause.
mkdir "$OUT/claim.d" || stop 97 "claim refused: an existing claim or an unwritable record directory"
START=$(now)
printf '{"claimed_utc":"%s","pid":%s,"root":"%s","rehearsal":%s}\n' "$START" "$$" "$ROOT" \
  "$REHEARSAL" > "$OUT/claim.d/claim.json" \
  || { echo "RECORD claim record failed; claim held; no launch"; exit 98; }
printf '{"phase":"agreement","event":"start","utc":"%s","plan_sha256":"%s","reviewed_commit":"%s","rehearsal":%s,"journal_rows_before":%s}\n' \
  "$START" "$PLAN_SHA" "$ADOPTED" "$REHEARSAL" "$ROWS_BEFORE" >> "$LOG" \
  || { echo "RECORD start record failed; claim held; no launch"; exit 98; }
grep -q '"event":"start"' "$LOG" || { echo "RECORD start record unreadable; claim held; no launch"; exit 98; }

# --- exactly one launch -------------------------------------------------------------------
set -o noclobber
t0=$(date +%s)
env -i SystemRoot="${SystemRoot:-$SYSTEMROOT}" TEMP="$TEMP" TMP="$TMP" PONTIUS_GIT="$GITEXE" \
  PYTHONDONTWRITEBYTECODE=1 \
  "$PY" -B -P -W error::ResourceWarning "$ROOT/tools/v0a_eval_panel.py" run \
  --reviewed-commit "$ADOPTED" --plan "$ROOT/plans/agreement.json" \
  > "$OUT/agreement-stdout.json" 2> "$OUT/agreement-stderr.txt"
rc=$?
set +o noclobber
wall=$(( $(date +%s) - t0 ))
echo "PHASE agreement exit=$rc wall=${wall}s"

# --- evidence: every write checked; journal row attributed, never assumed ---------------
EVIDENCE=complete
[ -f "$OUT/agreement-stdout.json" ] && [ -f "$OUT/agreement-stderr.txt" ] || EVIDENCE=incomplete
ROWS_AFTER=$(wc -l < execution_journal.jsonl) || { ROWS_AFTER=unreadable; EVIDENCE=incomplete; }
"$PY" -I -B "$ATTRIBUTE" execution_journal.jsonl "$ROWS_BEFORE" "$ADOPTED" "$ROOT" \
  "$OUT/agreement-journal-row.jsonl" > "$OUT/journal-attribution.txt"
ATTR_RC=$?
JOURNAL_ROW=$(head -n 1 "$OUT/journal-attribution.txt" | cut -d' ' -f1)
[ "$ATTR_RC" -eq 0 ] && [ "$JOURNAL_ROW" = BOUND ] || EVIDENCE=incomplete
STDOUT_SHA=$(sha "$OUT/agreement-stdout.json") || { STDOUT_SHA=unavailable; EVIDENCE=incomplete; }
STDERR_SHA=$(sha "$OUT/agreement-stderr.txt") || { STDERR_SHA=unavailable; EVIDENCE=incomplete; }
if [ "$JOURNAL_ROW" = BOUND ]; then
  ROW_SHA=$(sha "$OUT/agreement-journal-row.jsonl") || { ROW_SHA=unavailable; EVIDENCE=incomplete; }
else
  ROW_SHA=absent
fi
# --- retained file inventory ---------------------------------------------------------
(
  for d in experiments/results/runs/*/; do
    name=$(basename "$d"); echo "$TRACKED_RUNS" | grep -qx "$name" && continue
    # A phase may leave subdirectories in its run directory: agreement writes host-inputs/
    # for the sessions it plays, which solve and export never did. List every regular file
    # below the run root, in a stable order, so the inventory is what it claims to be.
    while IFS= read -r f; do
      h=$(sha "$f") || exit 1; n=$(wc -c < "$f") || exit 1
      printf '%s  %s  %s\n' "$h" "$n" "$f" || exit 1
    done < <(find "$d" -type f | LC_ALL=C sort)
  done
) > "$OUT/retained-files.txt" || EVIDENCE=incomplete
# --- end retained file inventory -------------------------------------------------------
printf '{"phase":"agreement","event":"end","utc":"%s","exit":%s,"wall_seconds":%s,"journal_rows_before":%s,"journal_rows_after":"%s","journal_row":"%s","journal_row_sha256":"%s","stdout_sha256":"%s","stderr_sha256":"%s","evidence":"%s"}\n' \
  "$(now)" "$rc" "$wall" "$ROWS_BEFORE" "$ROWS_AFTER" "$JOURNAL_ROW" "$ROW_SHA" "$STDOUT_SHA" \
  "$STDERR_SHA" "$EVIDENCE" >> "$LOG" || { echo "RECORD end record failed"; EVIDENCE=incomplete; }
echo "JOURNAL $(cat "$OUT/journal-attribution.txt")"
echo "RETAINED files:"; cat "$OUT/retained-files.txt"
echo "DONE at $(now): agreement exit $rc, evidence $EVIDENCE (rehearsal=$REHEARSAL)"
# Precedence: the child's nonzero status first, then incomplete evidence, then success.
[ "$rc" -eq 0 ] || { [ "$EVIDENCE" = complete ] || echo "EVIDENCE INCOMPLETE"; exit "$rc"; }
[ "$EVIDENCE" = complete ] || { echo "EVIDENCE INCOMPLETE"; exit 99; }
exit 0
