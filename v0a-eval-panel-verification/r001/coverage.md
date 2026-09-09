# Deferred FIX coverage: workload verification correction

Category: all three pipes created by the workload supervisor and all bare Git
fixture launches implicated by the failed broad run. Inventory method: trace
Popen allocation, Job assignment, thread targets, terminal cleanup, certificate
construction and the two test modules' subprocess argument lists.

| Surface | Invariant and observation | Falsifier |
| --- | --- | --- |
| Fixture Git | Three calls use an absolute executable with PATH absent | WinError 2 or relative argv |
| stdin | Sender stops before pipe release | Open real pipe on return |
| stdout | Receiver stops before pipe release | Open real pipe on return |
| stderr | Drain completes before status; pipe released | Lost late error or open pipe |
| Completion | Native worker exited and all pipes closed | Surviving worker or open pipe |
| Input refusal | Zero grant, native cleanup and closed pipes | Grant or leaked pipe |
| Budget/startup | Existing budget status with closed pipes | Leaked pipe or changed status |
| Expired check | Zero grant, budget status with closed pipes | Grant or leaked pipe |
| Assignment fault | Real suspended worker killed and pipes closed | Surviving worker or open pipe |
| Close fault | Real close occurs, raised error is retained, certificate false | Success certificate |
| Downstream gate | Existing eval-panel suites remain enforced | Any failing registered case |

The observer delegates to real Popen and selects the suspended worker by its
creation flag. It retains the actual pipe objects. Tests independently inspect
process.poll() and every stream.closed value before their own cleanup runs.
The close-fault schedule replaces only stdout.close on that real instance;
it performs the saved real close and then raises. This models an ambiguous
release report, not a frequency claim about the OS. Its independent outcomes
are all pipes closed, error retained, status failed and cleanup unverified.
No fake sets ownership or cleanup success. Existing Job, worker, Git and grant
boundaries execute in the isolated snapshots. Existing late-stderr scheduling
remains an inherited trigger; it does not replace the new pipe observations.

Final RED has identical test assertions to GREEN and unchanged parent production.
Seven workload tests fail on actual open pipes; the device fixture suite passes.
Earlier exploratory RED receipts include a test teardown error from attempting
the injected close twice; that harness error was corrected before final RED.
The first RED established six native-path leaks without that injected schedule.
All receipts remain available, with final-red as the valid comparison authority.

Limits: this bounded correction does not redesign early Job acquisition,
termination failure, failed joins, or signal delivery. Those exceptional paths
cannot assert verified cleanup here. The all-thread guard deliberately avoids
closing a buffered stream while a live thread may own its lock. No deterministic
live-reader-stall test is added; this safety branch is checked statically and
does not establish OS cleanup after a termination failure. No optional CUDA or
SciPy dependency is installed beyond the locked dev group. Correctness tests
cannot establish throughput, full-pool cost, or retained experimental results.

Hygiene: the two changed files containing inherited lines over 100 columns were
reflowed to meet the current changed-file gate. The device test reflow is AST
identical to final-red and changes no existing assertion. Worker path-string
reflow preserves its exact value. The production delta is 17 additions, 3 deletions;
only these three authorized source/test paths differ from the parent.
