# Workload verification correction

Tier C: the cleanup certificate and verification launch boundary are protected.
Base: d8d291cc1f813ce798f2d3a990b2a8bf2297e124, already independently reviewed.
The controller authorized this separate bounded correction on 2026-09-09.

Scope: tools/v0a_blueprint_workload.py and the two existing test modules
test_blueprint_workload_session.py and
test_legal_river_quotient_fixed_width_device_preflight.py. Budget: 200 changed
lines, two review rounds. No eval-panel arithmetic or orchestration change.

Acceptance:
1. All three fixture Git launches work with absolute PONTIUS_GIT and no PATH.
2. Workload cleanup closes all three real worker pipes after their users stop.
   A successful cleanup certificate requires dead threads and closed pipes.
   A pipe close failure is retained and cannot produce a successful certificate.
3. Existing worker statuses, grants, results and source checks remain enforced.
4. Focused tests and the registered broad harness pass in a fresh locked CPython
   3.14.6 environment under -B -P and strict resource/unraisable warnings.
   Optional dependency skips remain explicit; no suppression of leaks.

Oracle: real subprocess pipe objects, actual native worker termination, existing
Git fixture assertions, and the registered test outcomes. The test observer
delegates subprocess construction to the real implementation and inspects the
returned objects; it does not substitute OS cleanup or success bookkeeping.

Seams: fixture/Git executable, Popen/pipes, worker threads/native Job, certificate.
Only the eval-panel broad verification gate depends on this correction.
Adopt only after independent Tier C reviews and the broad gate. Return for
reauthorization after two rounds or if the bounded repair needs redesign.
No retained experiment, capacity claim, ceremonial adoption or public push is
authorized by this correction. Python 3.11 is outside current execution scope.

## Design

Git fixtures bind an absolute executable before use, with the same development
resolution convention as maintained fixtures. Scrubbed verification supplies
PONTIUS_GIT, so no PATH lookup occurs in that environment.

After worker termination, join the pipe users before releasing their streams.
If any user remains alive, retain failure instead of risking a blocking close
against that user's buffered-I/O lock. Attempt each eligible stream once;
retain individual close errors so one failure cannot prevent other releases.
Cleanup verification includes real stream closure as well as the existing Job
and thread checks. Existing exceptional termination handling remains; this
correction does not certify cleanup when termination or thread joining fails.

The category is every Popen pipe on the existing supervised workload path,
including completion, refusal, budget exhaustion and assignment failure.
Regression observations extend the native cases already exercising those paths.
Do not rely on garbage collection timing to observe leaks. Do not suppress
ResourceWarning or infer stream closure from the cleanup certificate itself.
The remaining eval-panel design and later measured runs are outside this task.
