# Ownership contract coverage: final combined candidate

This FIX continues the separate ownership contract. Its immediate parent is the
separately frozen sample/r001 candidate 72954e1331c9b191d927c1c4b82f277bcd322a4c.
Only Job lifetime, terminal certificate timing and their regression tests change
against that parent. Review the entire affected ownership contract and check the
combined sample consumers; the earlier ownership changes are inherited, not waived.

Invariant 1: every acquired resource has a release owner before another fallible
operation. Enumerate Job acquisition, suspended process creation, assignment, thread
start, resume, every release, signal-handler restoration and terminal certification.
The report and empty ownership state now exist first. Job acquisition happens inside
interrupt deferral and the cleanup try. A returned Job is closed even if SIGINT arrived
inside acquisition, and an interrupted acquisition stops before launching a worker.
The real-acquisition regression observes the native Job still open on RED, before its
fixture closes that otherwise leaked resource. The corrected result must report close
success and interruption, and the actual returned Job must already be released.

Invariant 2: cleanup_verified can become true only after all cleanup inputs are final:
observed dead resources, every successful release and the end of interrupt deferral.
The previous candidate stopped this lifetime at the last native close, overlooking
the handler that could still mutate cleanup outcomes. That handler is now restored
before the certificate is computed. An interrupt during the final store raises under
the original handler; the caller's original false certificate survives the unwind.
Falsifier: a retained result contains a recorded cleanup interruption and a true
certificate. The new real-worker main test injects SIGINT at the final STORE_SUBSCR
after the conjunction has already been evaluated. RED records precisely that false
claim. The test locates all compiler copies of the assignment's finally body, rather
than assuming one opcode exists; it records that the schedule actually fired.
The independent review's after-certification/before-handler-restoration window is
eliminated by ordering: certification is outside and after the deferral context.

Inherited checks also exercise final native close followed by reported failure,
interrupted wait, assignment refusal, independent releases after earlier cleanup faults,
and cleanup interruption. No failed or interrupted cleanup outcome may certify success.
The Job implementation is unchanged, and a consumed numeric handle is never retried.

Invariant 3: every drained preflight record is reachable through the caller's report
when created; later stages mutate that same object. Missing-stage annotations do not
transfer ownership. Discovery follows queue -> drain -> stage -> main -> result/journal.
The real post-native-close interruption retains the completed production stage even
when supervise never returns normally. Existing budget interruption retains partial
stages with explicit incompleteness. No successful end-of-function merge is required.

Invariant 4: a stream's buffered lock cannot block the report owner indefinitely.
Each stream has one daemon closer and a bounded wait; a pending close is a failed
cleanup outcome, never an observed release. The real OS-pipe test applies 1 MiB of
backpressure, observes timeout, then drains the pipe and checks every byte, both I/O
thread exits and stream closure. The same closer completes; no ambiguous retry occurs.

Invariant 5: intended publication identity exists before rename, and successful or
ambiguous publication is reconciled against the actual final file before its encoding
is removed. Enumerate before write, partial write, before rename, after rename and
before binding. The real rename-then-interrupt case checks final path, size and SHA-256
in the retained result against file bytes. Existing second-write failure/retry preserves
both already bound artifacts and remaining recoverable encodings. A failed reconcile
retains the intended publication metadata and bytes, rather than inventing success.

Inherited sample contract: role-bearing admission supplies the worker and estimator's
same schedule. The combined suite retains all role-movement rejections and the real
five-hand declared-full preflight, four literal development identities, royal control,
successful comparisons and four-hand estimate. No numerical bridge or sealed blob changes.

RED b6ede27a2c737f2a77344908fb3ebe8a88088f54: 35 cases, zero skipped, exit 1,
exactly the certificate and acquisition assertions fail; no unittest errors. All
other 33 cases pass. The earlier ee98f51 instruction-locator diagnostic is explicitly
not counted as a product RED. Both defects were reproduced before production edits.
GREEN d8d291cc1f813ce798f2d3a990b2a8bf2297e124: 35 cases, zero skipped, exit 0.
The GREEN receipt and its independently retained journal identify this exact candidate;
the packet carries the complete focused output and separate Ruff command/exit receipt.
All checks use disposable locked environments and CPython 3.14.6; test execution uses
-B -P, ResourceWarning-as-error, scrubbed environment and absolute PONTIUS_GIT.

Size: 959 production lines (333 unchanged bridge + 626 tool), 799 test lines (198
unchanged bridge tests + 601 tool tests), excluding the unchanged serialized fixtures.
Against rejected r004, only two files change: 486 additions and 118 deletions. This is
within the controller's up-to-3,000-line correction authorization. The former 600-line
test working figure is exceeded and remains disclosed; it is not silently redefined.

Limits: deterministic schedules establish correctness, not external failure rates.
No exhaustive simultaneous-fault proof, failed-device guarantee, externally killed
parent recovery, retained performance measurement or poker-strength claim is made.
No broad suites or ceremonial integration precede both required Tier C reviews.
