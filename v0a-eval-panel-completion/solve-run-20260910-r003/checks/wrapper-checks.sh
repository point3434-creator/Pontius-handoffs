#!/usr/bin/env bash
# Fault-path checks for invoke.sh. Every case ASSERTS its observables (exit code plus a
# stated condition) and the runner exits nonzero if any case fails, so a silent regression
# cannot pass as evidence (review 01 M-02).
#
# SNAPSHOT   a detached disposable worktree at the adopted commit, used for the refusal
#            cases and for the race whose winner becomes the packet's rehearsal.
# SNAPSHOT_B a second detached disposable worktree whose venv is deliberately broken, used
#            once for the child-failure precedence case; it is never the packet rehearsal.
#
# Cases: C1-C7, C10-C12 must refuse BEFORE any launch; C8 exercises the attribution helper
# on isolated synthetic journals; C13 launches a failing child and asserts that its nonzero
# status is returned rather than 99; C9 races two callers and asserts exactly one launch.
set -u
PK=D:/Pontius-handoffs/v0a-eval-panel-completion/solve-run-20260910-r003
SNAP="${SNAPSHOT:?set SNAPSHOT to the detached disposable worktree}"
SNAPB="${SNAPSHOT_B:?set SNAPSHOT_B to the second detached disposable worktree}"
SCR=D:/Pontius/tmp/solve-r003-checks
RETAINED=D:/Pontius-worktrees/eval-panel-solve-20260910
BRANCHED=D:/Pontius-worktrees/codex-eval-panel-completion-adopted
PY="$SNAP/.venv/Scripts/python.exe"
OUTF="$PK/checks/wrapper-checks.jsonl"
FAILED=0
rm -rf "$SCR"; mkdir -p "$SCR/captures"; : > "$OUTF"
now() { date -u +%Y-%m-%dT%H:%M:%SZ; }
assert() { # case expected_exit actual_exit condition_name condition_expected condition_actual
  local ok=true
  [ "$2" = "$3" ] || ok=false
  [ "$5" = "$6" ] || ok=false
  [ "$ok" = true ] || FAILED=$((FAILED + 1))
  printf '{"case":"%s","expected_exit":%s,"actual_exit":%s,"condition":"%s","condition_expected":"%s","condition_actual":"%s","pass":%s,"utc":"%s"}\n' \
    "$1" "$2" "$3" "$4" "$5" "$6" "$ok" "$(now)" >> "$OUTF"
  echo "$1 exit $3 (want $2); $4 = $6 (want $5); pass=$ok"
}
launched() { # a launch leaves solve-stdout.json somewhere under the given directory
  if [ -n "$(find "$1" -name solve-stdout.json 2>/dev/null)" ]; then echo launched; else echo no-launch; fi
}

# --- refusals before any launch ----------------------------------------------------------
refuse() { # case env-assignments... -- expected_exit  (runs the wrapper, asserts no launch)
  local name=$1 expected=$2 pkdir=$3; shift 3
  mkdir -p "$pkdir"
  env "$@" bash "$PK/invoke.sh" > "$SCR/captures/$name.txt" 2>&1; local rc=$?
  assert "$name" "$expected" "$rc" launch no-launch "$(launched "$pkdir")"
  cp "$SCR/captures/$name.txt" "$PK/checks/refusal-$name.txt"
}
refuse C1-retained-override-refused 88 "$PK/invocations" SOLVE_ROOT="$SNAP"
refuse C2-retained-no-authorization 89 "$PK/invocations"
refuse C3-rehearsal-no-root 87 "$SCR/c3" REHEARSAL=1 REHEARSAL_PK="$SCR/c3"
refuse C4-rehearsal-root-is-retained 86 "$SCR/c4" REHEARSAL=1 SOLVE_ROOT="$RETAINED" REHEARSAL_PK="$SCR/c4"
refuse C5-rehearsal-root-not-detached 85 "$SCR/c5" REHEARSAL=1 SOLVE_ROOT="$BRANCHED" REHEARSAL_PK="$SCR/c5"
mkdir -p "$SCR/c6/rehearsal/claim.d"
refuse C6-prior-claim 97 "$SCR/c6" REHEARSAL=1 SOLVE_ROOT="$SNAP" REHEARSAL_PK="$SCR/c6"
mkdir -p "$SCR/c7"; : > "$SCR/c7/rehearsal"
refuse C7-record-dir-unwritable 83 "$SCR/c7" REHEARSAL=1 SOLVE_ROOT="$SNAP" REHEARSAL_PK="$SCR/c7"
refuse C10-rehearsal-value-two 84 "$SCR/c10" REHEARSAL=2 SOLVE_ROOT="$SNAP" REHEARSAL_PK="$SCR/c10"
refuse C11-rehearsal-value-word 84 "$SCR/c11" REHEARSAL=yes SOLVE_ROOT="$SNAP" REHEARSAL_PK="$SCR/c11"

# C12 injected start-record failure, exercised on a LABELED MUTANT of invoke.sh (the host
# filesystem offers no reliable way to deny a write to a directory this user owns). The
# mutant differs from the frozen script in exactly one line: LOG points at the claim
# directory, so the start-record append cannot succeed. Its digest and diff are retained.
MUT="$SCR/mutant-start-record-failure.sh"
sed 's@^LOG="[$]OUT/invocation-log.jsonl"$@LOG="$OUT/claim.d"  # MUTANT: unwritable start record@' \
  "$PK/invoke.sh" > "$MUT"
mkdir -p "$SCR/c12"
diff -u "$PK/invoke.sh" "$MUT" > "$PK/checks/mutant-C12.diff"
{ echo "mutant of invoke.sh; one line changed; NOT the frozen script"
  echo "frozen  sha256 $(sha256sum "$PK/invoke.sh" | cut -d' ' -f1)"
  echo "mutant  sha256 $(sha256sum "$MUT" | cut -d' ' -f1)"
  echo "changed lines  $(grep -c '^[+-][^+-]' "$PK/checks/mutant-C12.diff")"; }   > "$PK/checks/mutant-C12-identity.txt"
REHEARSAL=1 SOLVE_ROOT="$SNAP" REHEARSAL_PK="$SCR/c12" bash "$MUT"   > "$SCR/captures/C12.txt" 2>&1; RC12=$?
assert C12-start-record-failure-mutant 98 "$RC12" launch no-launch "$(launched "$SCR/c12")"
cp "$SCR/captures/C12.txt" "$PK/checks/refusal-C12-start-record-failure-mutant.txt"

# --- C8 attribution helper on isolated synthetic journals --------------------------------
mkdir -p "$SCR/c8/experiments/results/runs/aa"
printf '{"x":1}\n' > "$SCR/c8/experiments/results/runs/aa/result.json"
RSHA=$(sha256sum "$SCR/c8/experiments/results/runs/aa/result.json" | cut -d' ' -f1)
COMMIT=1c7067448106cfa2aca3d57be879842d72293c61
OLD='{"source_commit":"old","output":"experiments/results/runs/aa/result.json","output_sha256":"'$RSHA'"}'
GOOD='{"source_commit":"'$COMMIT'","output":"experiments/results/runs/aa/result.json","output_sha256":"'$RSHA'"}'
BADC='{"source_commit":"deadbeef","output":"experiments/results/runs/aa/result.json","output_sha256":"'$RSHA'"}'
BADS='{"source_commit":"'$COMMIT'","output":"experiments/results/runs/aa/result.json","output_sha256":"0000"}'
attr() { # name journal-content rows_before expected_exit expected_row_written
  printf '%b' "$2" > "$SCR/c8/journal.jsonl"; rm -f "$SCR/c8/row.jsonl"
  local out rc written
  out=$("$PY" -I -B "$PK/journal_attribution.py" "$SCR/c8/journal.jsonl" "$3" "$COMMIT" \
        "$SCR/c8" "$SCR/c8/row.jsonl"); rc=$?
  if [ -f "$SCR/c8/row.jsonl" ]; then written=yes; else written=no; fi
  assert "C8-$1" "$4" "$rc" row-written "$5" "$written"
  echo "  helper said: $out"
}
attr absent "$OLD\n" 1 3 no
attr extra "$OLD\n$GOOD\n$GOOD\n" 1 4 no
attr mismatch-commit "$OLD\n$BADC\n" 1 5 no
attr mismatch-sha "$OLD\n$BADS\n" 1 5 no
attr bound "$OLD\n$GOOD\n" 1 0 yes
attr bound-crlf "$OLD\r\n$GOOD\r\n" 1 0 yes

# --- C13 child-failure precedence: the child's nonzero status is returned, never 99 -------
# SNAPSHOT_B's venv is broken before this call (numpy removed), so the tool fails during
# import, before begin_run's owner can append any journal row. This is the compound path
# named in cold review 02 M-01: no new row exists, the helper reports ABSENT, the evidence
# is incomplete, and the wrapper must return the child's status (1) rather than 99.
REHEARSAL=1 SOLVE_ROOT="$SNAPB" REHEARSAL_PK="$SCR/c13" bash "$PK/invoke.sh" \
  > "$SCR/captures/C13.txt" 2>&1; RC13=$?
C13_STATE=$("$PY" -I -B -c "
import json, pathlib, sys
log = [json.loads(l) for l in pathlib.Path(sys.argv[1]).read_bytes().splitlines()]
end = [r for r in log if r.get('event') == 'end'][0]
names = pathlib.Path(sys.argv[2]).read_text().split()
found = [t for t in names if t.endswith('result.json')]
status = 'no-result'
if found:
    status = json.loads((pathlib.Path(sys.argv[3]) / found[0]).read_bytes())['status']
print('%s|%s|%s' % (end['exit'], end['journal_row'], status))
" "$SCR/c13/rehearsal/invocation-log.jsonl" "$SCR/c13/rehearsal/retained-files.txt" "$SNAPB"   2>/dev/null) || C13_STATE=unreadable
[ -n "$C13_STATE" ] || C13_STATE=unreadable
assert C13-child-failure-precedence 1 "$RC13" end-record "1|ABSENT|no-result" "$C13_STATE"
cp "$SCR/captures/C13.txt" "$PK/checks/child-failure-C13.txt"
cp "$SCR/c13/rehearsal/invocation-log.jsonl" "$PK/checks/child-failure-C13-log.jsonl"

# --- C9 two concurrent callers; the winner's records are the packet rehearsal -------------
REHEARSAL=1 SOLVE_ROOT="$SNAP" bash "$PK/invoke.sh" > "$SCR/captures/c9-a.txt" 2>&1 & A=$!
REHEARSAL=1 SOLVE_ROOT="$SNAP" bash "$PK/invoke.sh" > "$SCR/captures/c9-b.txt" 2>&1 & B=$!
wait $A; RA=$?; wait $B; RB=$?
if { [ "$RA" -eq 0 ] && [ "$RB" -eq 97 ]; } || { [ "$RB" -eq 0 ] && [ "$RA" -eq 97 ]; }; then
  RACE=one-winner-one-refusal; else RACE="A=$RA,B=$RB"; fi
LAUNCHES=$(find "$PK/rehearsal" -name solve-stdout.json | wc -l | tr -d ' ')
assert C9-race-one-claim 0 0 "launches($RACE)" 1 "$LAUNCHES"
cp "$SCR/captures/c9-a.txt" "$PK/checks/race-caller-a.txt"
cp "$SCR/captures/c9-b.txt" "$PK/checks/race-caller-b.txt"

echo "CHECKS done at $(now); cases: $(wc -l < "$OUTF"), failures: $FAILED"
exit $(( FAILED > 0 ))
