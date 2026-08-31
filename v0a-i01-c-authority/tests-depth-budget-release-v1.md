# Two-case floor diagnostic controller: v1 release

Engineering infrastructure for root review, not execution authorization or a
cold/product verdict. No new controller, probe, candidate, Python parse/import,
or fixture payload was executed by this author.

Frozen controller: T/tests-depth-budget-control-v1.py
SHA256 9df274065efc48c9bd31d208c0ac0a3d13bc6217bf3fee762ef06cf7d7a2e407
(28586 bytes, UTF-8 without BOM, LF).
T is D:/Pontius-handoffs/v0a-i01-c-authority.

Read-only predecessor:
T/engineer-chain32-budget-control-v1.py
SHA256 425aa5a008dae30fff32a6e9e1fe1c04be6b714c1e6aa5ef5785159e7a8ce2df.
The successor keeps its single-case fresh-snapshot pattern but binds explicit
retained input hashes, complete identity/custody, process status and diagnostic
completion. The predecessor and all other issued artifacts remain unchanged.

Only helper1050 and generator70 are selectable. There is no dev slot, suite,
matrix, public24, generator-write, owner, GPU, broad-wall or arbitrary command
mode. Root must inspect the final probe and candidate before dispatch.

Required CLI

Use actual D:/Pontius-tools/py311/Scripts/python.exe with -I -S -B -P, followed
by this controller and:
--label NAME
--case helper1050|generator70
--source-path ABSOLUTE_RETAINED_T_PYTHON_FILE
--source-sha FULL_ROOT_APPROVED_SOURCE_SHA256
--probe-sha FULL_FINAL_PROBE_SHA256
--control-sha 9df274065efc48c9bd31d208c0ac0a3d13bc6217bf3fee762ef06cf7d7a2e407
--watch-sha FULL_SEPARATE_ROOT_APPROVED_W_SOURCE_SHA256

The fixed probe path is T/engineer-depth-budget-probe-v1.py. Its final source
and SHA are still pending from the cost author at this release. The control
does not select, invent, approve, or obtain that hash itself. Root must bind
the final reviewed file explicitly. The candidate is always copied from the
retained T path; W/tools/generate_test_inventory.py is separately hash-watched
before/after and never used as the candidate. W's expected hash need not equal
the candidate hash.

Every invocation creates a new UUID directory under D:/pontius-snapshots.
It checks detached r01029c02f6fbd5eb0b7ddc9e816ef28f570b9839358,
a clean initial checkout, and exactly1761 unique tracked paths equal to the
commit tree's path set. All tracked raw hashes are retained. Original source
must be29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692;
original tests must bec46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf.
Only the candidate generator is overlaid; tests remain unchanged.

Before any repository import, the child validates actual3.11.15/executable,
-B -P, no optimization/user-site, snapshot cwd, exact scrubbed environment,
snapshot/src PYTHONPATH, D-local TEMP/TMP, complete1765-file pre-import manifest
(1761tracked+probe/control/wrapper/job), and source/test/probe/control pins.
The final before/after map additionally includes the manifest itself:
1766 files. Git is the absolute validated C:/Program Files/Git/cmd/git.exe
with the established config/hooks/template/attributes restrictions. No
interpreter, dependency, repository fixture or owner is installed/executed
outside the selected diagnostic protocol.

The probe receives --case CASE. Its agreed completion record is
depth_budget_diagnostic_complete, containing case, completed:true,
caps_unchanged:true, original_methods_restored:true, source_sha256 and
tests_sha256. Optional depth_budget_failure records are retained verbatim.
The controller requires exactly one matching completion, one actual identity,
no bootstrap/malformed-JSON error, child exit0 and intact custody to report
diagnostic_completed:true. This means observation and restoration completed;
it never labels the selected candidate or fixture as passing.

Controller lines274 onward validate completion; lines322 onward create and
verify the disposable snapshot; lines454 onward launch only the one child.
Its owned PID and stream paths are printed immediately. The direct process
has a60-second watchdog. Timeout kills/waits for that process, records
actual returncode separately, and returns logical124 with retained partial
stdout/stderr and case identity. No descendant-tree termination is claimed.
Each setup/integrity Git call also has a60-second limit; controller total wall
time is not one global60-second deadline. Root must serialize launches.

Create-only files under T/tests-checks are
depth-budget-LABEL-CASE-311-{setup.json,receipt.json}, .stdout.txt,
.stderr.txt and .txt. Raw streams are retained; the convenience log is LF
normalized. Inputs, all tracked/payload files, HEAD/status and untracked
population are checked after completion or failure. Timeout and partial/invalid
evidence cannot pass. A nonzero probe exit propagates; infrastructure/custody
failure returns2. Results/receipts survive ordinary child/bootstrap failure
and post-child validation failure. Snapshots/logs are not deleted, retried or
repurposed for another case.

Fixture constraints

Helper1050 original test lines4926-4959 builds1050 module helpers, ending in a
subprocess call represented only as source bytes. It requires InventoryError
matching analysis.*(?:depth|budget); it does not require one exact depth message.
Generator70 original lines14528-14557 constructs a70-generator consumption chain
and requires exactly analysis deferred generator depth exceeds64. The original
32-chain assertion requires no capability rows and a nonempty blocker. No cap,
message, expectation or assertion change is authorized.

The probe author agreed to preserve the original _review envelope at1977-1995,
including tools/test_child.py and the existing inventory/universe. Reduced
one-file synthetic review, direct sensitive fixture execution, or extra depth
cases are outside this controller's scope. Review of that final probe remains
a required independent root gate.

Authoring validation is read-only PowerShell hashing and source inspection.
No Python parser or controller self-test ran. The final probe, root source
review and an eventual dispatch receipt remain necessary evidence.
