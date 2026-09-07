# Retained acceptance environment diagnosis

Source candidate remains 4d567797e4b3945ea3ff6c75613c56c05bc0b75a,
manifest 7d273ea40ca8b3c251ad029a8ab8ca423312703661b3c14a3bf01a375fece58b.

The first floor acceptance attempt passed commands 1-21 and stopped at command 22.
Original run-records/002g22-311.json retains 36 passes and one failure in the
unchanged test_child_launch_flags_environment_and_binary_capture_are_real.
Its exact string assertion compared the caller's PONTIUS_GIT using forward slashes
with the child's native Windows Path spelling using backslashes. Both paths name
the same absolute, regular executable. Source admission and child launch normalize
the supplied absolute path; the test expects the parent already uses that form.

Against unchanged baseline fc99ab1a02649b82ba3bc21e5db79cb9c6e25829, fresh
single-test diagnostic egit01-311 reproduces that exact failure. Changing only the
runner's absolute Git literal to native Windows spelling makes the same unchanged
baseline test pass in new diagnostic egit02-311. Neither candidate source nor any
test assertion changed. run-snapshot-before-native-git.ps1 retains the old runner.

The full affected 37-test suite is repeated under 002h22-311 in a new exact-candidate
snapshot. Only if it passes may acceptance continue at command 23. Earlier passing
receipts remain valid named checks against the same source candidate. All 26 floor
commands must pass before the current interpreter run. Its complete run uses the
canonical native spelling. The final summary indexes every selected receipt plus
the original failure and both baseline diagnostics; no failure is overwritten or
relabeled. This is execution-environment correction, not a source FIX or a weakened
acceptance population. The source candidate and both review bindings remain exact.
