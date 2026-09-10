#!/usr/bin/env bash
# Fault-path checks for invoke.sh. Cases C1-C7 must refuse BEFORE any launch; C8 exercises
# the journal attribution helper on synthetic journals; C9 races two callers in rehearsal
# mode against the disposable snapshot: exactly one may claim and run, the other must exit
# 97 without launching. The winner's records are the packet's official rehearsal.
# Output: checks/wrapper-checks.jsonl (one row per case) and per-case captures.
set -u
PK=D:/Pontius-handoffs/v0a-eval-panel-completion/solve-run-20260910-r002
SNAP="${SNAPSHOT:?set SNAPSHOT to the detached disposable worktree}"
SCR=D:/Pontius/tmp/solve-r002-checks
RETAINED=D:/Pontius-worktrees/eval-panel-solve-20260910
BRANCHED=D:/Pontius-worktrees/codex-eval-panel-completion-adopted
PY="$SNAP/.venv/Scripts/python.exe"
OUTF="$PK/checks/wrapper-checks.jsonl"
rm -rf "$SCR"; mkdir -p "$SCR/captures"; : > "$OUTF"
now() { date -u +%Y-%m-%dT%H:%M:%SZ; }
record() { # case expected actual note
  printf '{"case":"%s","expected_exit":%s,"actual_exit":%s,"pass":%s,"note":"%s","utc":"%s"}\n' \
    "$1" "$2" "$3" "$([ "$2" = "$3" ] && echo true || echo false)" "$4" "$(now)" >> "$OUTF"
  echo "$1 expected $2 actual $3 :: $4"
}
launched() { # a launch leaves solve-stdout.json somewhere under the given dir
  [ -n "$(find "$1" -name solve-stdout.json 2>/dev/null)" ] && echo launched || echo no-launch
}

# C1 retained mode refuses root overrides (before looking at authorization)
mkdir -p "$SCR/c1"
SOLVE_ROOT="$SNAP" bash "$PK/invoke.sh" > "$SCR/captures/c1.txt" 2>&1; rc=$?
record C1-retained-override-refused 88 "$rc" "$(head -n1 "$SCR/captures/c1.txt"); $(launched "$PK/invocations")"
# C2 retained mode without authorization.md
bash "$PK/invoke.sh" > "$SCR/captures/c2.txt" 2>&1; rc=$?
record C2-retained-no-authorization 89 "$rc" "$(head -n1 "$SCR/captures/c2.txt"); $(launched "$PK/invocations")"
# C3 rehearsal without an explicit root
REHEARSAL=1 REHEARSAL_PK="$SCR/c3" bash "$PK/invoke.sh" > "$SCR/captures/c3.txt" 2>&1; rc=$?
record C3-rehearsal-no-root 87 "$rc" "$(head -n1 "$SCR/captures/c3.txt"); $(launched "$SCR/c3")"
# C4 rehearsal root equal to the retained checkout
REHEARSAL=1 SOLVE_ROOT="$RETAINED" REHEARSAL_PK="$SCR/c4" bash "$PK/invoke.sh" > "$SCR/captures/c4.txt" 2>&1; rc=$?
record C4-rehearsal-root-is-retained 86 "$rc" "$(head -n1 "$SCR/captures/c4.txt"); $(launched "$SCR/c4")"
# C5 rehearsal root on a branch (not detached)
REHEARSAL=1 SOLVE_ROOT="$BRANCHED" REHEARSAL_PK="$SCR/c5" bash "$PK/invoke.sh" > "$SCR/captures/c5.txt" 2>&1; rc=$?
record C5-rehearsal-root-not-detached 85 "$rc" "$(head -n1 "$SCR/captures/c5.txt"); $(launched "$SCR/c5")"
# C6 a prior claim exists
mkdir -p "$SCR/c6/rehearsal/claim.d"
REHEARSAL=1 SOLVE_ROOT="$SNAP" REHEARSAL_PK="$SCR/c6" bash "$PK/invoke.sh" > "$SCR/captures/c6.txt" 2>&1; rc=$?
record C6-prior-claim 97 "$rc" "$(head -n1 "$SCR/captures/c6.txt"); $(launched "$SCR/c6")"
# C7 the record directory cannot be created (a file occupies its path)
mkdir -p "$SCR/c7"; : > "$SCR/c7/rehearsal"
REHEARSAL=1 SOLVE_ROOT="$SNAP" REHEARSAL_PK="$SCR/c7" bash "$PK/invoke.sh" > "$SCR/captures/c7.txt" 2>&1; rc=$?
record C7-record-dir-unwritable 83 "$rc" "$(head -n1 "$SCR/captures/c7.txt"); $(launched "$SCR/c7")"

# C8 journal attribution helper on synthetic journals
mkdir -p "$SCR/c8/experiments/results/runs/aa"
printf '{"x":1}\n' > "$SCR/c8/experiments/results/runs/aa/result.json"
RSHA=$(sha256sum "$SCR/c8/experiments/results/runs/aa/result.json" | cut -d' ' -f1)
COMMIT=1c7067448106cfa2aca3d57be879842d72293c61
OLD='{"source_commit":"old","output":"experiments/results/runs/aa/result.json","output_sha256":"'$RSHA'"}'
GOOD='{"source_commit":"'$COMMIT'","output":"experiments/results/runs/aa/result.json","output_sha256":"'$RSHA'"}'
BADC='{"source_commit":"deadbeef","output":"experiments/results/runs/aa/result.json","output_sha256":"'$RSHA'"}'
BADS='{"source_commit":"'$COMMIT'","output":"experiments/results/runs/aa/result.json","output_sha256":"0000"}'
attr() { # name journal-content rows_before expected
  printf '%b' "$2" > "$SCR/c8/journal.jsonl"; rm -f "$SCR/c8/row.jsonl"
  out=$("$PY" -I -B "$PK/journal_attribution.py" "$SCR/c8/journal.jsonl" "$3" "$COMMIT" "$SCR/c8" "$SCR/c8/row.jsonl"); rc=$?
  record "C8-$1" "$4" "$rc" "$out; row-written=$([ -f "$SCR/c8/row.jsonl" ] && echo yes || echo no)"
}
attr absent "$OLD\n" 1 3
attr extra "$OLD\n$GOOD\n$GOOD\n" 1 4
attr mismatch-commit "$OLD\n$BADC\n" 1 5
attr mismatch-sha "$OLD\n$BADS\n" 1 5
attr bound "$OLD\n$GOOD\n" 1 0
attr bound-crlf "$OLD\r\n$GOOD\r\n" 1 0

# C9 two concurrent callers against the snapshot; records into the packet's rehearsal/
REHEARSAL=1 SOLVE_ROOT="$SNAP" bash "$PK/invoke.sh" > "$SCR/captures/c9-a.txt" 2>&1 & A=$!
REHEARSAL=1 SOLVE_ROOT="$SNAP" bash "$PK/invoke.sh" > "$SCR/captures/c9-b.txt" 2>&1 & B=$!
wait $A; RA=$?; wait $B; RB=$?
if [ "$RA" -eq 0 ] && [ "$RB" -eq 97 ]; then verdict=0; elif [ "$RB" -eq 0 ] && [ "$RA" -eq 97 ]; then verdict=0; else verdict=1; fi
record C9-race-one-claim 0 "$verdict" "exit A=$RA B=$RB; launches=$(find "$PK/rehearsal" -name solve-stdout.json | wc -l); claim.d=$([ -d "$PK/rehearsal/claim.d" ] && echo present || echo absent)"
cp "$SCR/captures/c9-a.txt" "$PK/checks/race-caller-a.txt"; cp "$SCR/captures/c9-b.txt" "$PK/checks/race-caller-b.txt"
for c in c1 c2 c3 c4 c5 c6 c7; do cp "$SCR/captures/$c.txt" "$PK/checks/refusal-$c.txt"; done
echo "CHECKS done at $(now); failures: $(grep -c '"pass":false' "$OUTF")"
