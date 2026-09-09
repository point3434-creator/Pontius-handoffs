# Ownership contract coverage

Invariant 1: a cleanup certificate can be true only after every required release
has returned successfully and the worker, I/O threads and streams have been observed
released. A recorded failure or interruption cannot coexist with a true certificate.
Discovery: trace every native resource from Popen/Job acquisition through release,
including verification before the native Job handle is consumed and certification after.
Falsifier: a final close failure, or interrupted wait with otherwise dead resources,
leaves cleanup_verified true. The former failed on the RED snapshot through the real
worker/main/result writer and passes here; the existing wait-interruption case now
also asserts false. Release success is observed via real process poll, streams and Job.

Invariant 2: every received preflight record is attached to caller-owned observations
when it is created; later annotations and cleanup do not transfer its ownership.
Discovery: follow stdout queue -> drain -> stage object -> main -> execution.finish_run.
Falsifier: interrupt the real supervisor immediately after native Job.close, before
normal return/finalization; the real retained result loses the completed production stage.
The RED run loses that stage; the corrected run retains it and writes one journal row.
The test's trace hook controls interruption timing only; worker computation, native
release, source admission and both result writers remain real in a disposable clone.

Invariant 3: an I/O lock cannot make a stream close block the report owner indefinitely.
Discovery: join timeouts do not establish that a buffered stream lock is available.
Each close has a single daemon owner and a bounded wait. A timed-out owner is retained
by its running thread, and the run cannot certify cleanup. No ambiguous native close
is retried. The new real-pipe test fills an OS pipe with a 1 MiB write, observes close
timeout under backpressure, then drains the pipe and verifies the original closer
finishes, both I/O threads exit, the stream closes and every byte arrives unchanged.
This is additional coverage of the disposition's concern, not a new RED product claim.

Invariant 4: the intended identity of a boundary publication is registered before
write/rename; a successful or ambiguous rename is reconciled against the final file.
Pending bytes remain recoverable until the final artifact's binding is established.
Discovery: enumerate before write, partial write, before rename, after rename and
before successful binding. The new real-worker main case performs the actual rename
then raises KeyboardInterrupt. RED leaves a complete file unbound; GREEN reads its
retained path/length/hash binding and independently matches the final file's bytes.
Existing second-write failure/retry and codec round-trip tests remain green.

Console SIGINT is recorded while supervision owns resources, so ordinary console
interrupt delivery cannot unwind between release attempts. Operation-raised exceptions
and KeyboardInterrupt are recorded per attempt. The post-cleanup trace test also checks
an escaping interruption, independently of this signal handler, after actual releases.

Focused receipts: RED cf47853df2c17723a162792db6910021652d2f20 exercised 30 cases,
zero skipped, exit 1, exactly three new assertion failures and no unittest errors.
GREEN 182d14e213c6f0b7d7578e429f81d051a9e59707 exercised 31 cases, zero skipped,
exit 0; both journal rows identify their frozen source and source_verified true.
Ruff check passed for both affected files using the snapshot's installed linter.

Limits: deterministic schedules establish the contract, not OS failure frequencies.
No exhaustive simultaneous-fault proof, failed storage device guarantee, externally
killed parent recovery, or new capacity/performance measurement is claimed. A pending
close is reported as failed cleanup, not as a released resource. Source review must
still challenge queue/record ownership, terminal cleanup certification and publication
reconciliation beyond the supplied schedules. The sample-role finding is deliberately
unchanged here and belongs to the separate dependent sample candidate.
