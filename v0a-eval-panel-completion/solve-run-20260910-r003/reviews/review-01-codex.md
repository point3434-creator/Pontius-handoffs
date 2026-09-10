# Independent cold review 01 — Codex

**Verdict: NOT CLEAN. Findings: 0 Critical, 0 Important, 3 Minor.**

**Specification verdict:** the concrete solve plan, source/prerequisite bindings, controller
resource envelope and four earlier operational properties conform. The literal mode and
claim-consumption promises, and the assertion claim for race check C9, remain inaccurate.
**Engineering-quality verdict:** operationally SOUND for the bound retained solve in the
intended modes under exclusive operator ownership; the regression-check gate needs correction.
No material reachable launch-safety failure was established for that supported invocation.
This report authorizes no invocation or publication.

Packet: `D:/Pontius-handoffs/v0a-eval-panel-completion/solve-run-20260910-r003/`.
Unqualified file citations below are relative to that packet. Behavioral source citations
refer exclusively to Git blobs at `1c7067448106cfa2aca3d57be879842d72293c61`.

**Independence and immutable inventory.** CONTEXT_PROBE_NONE was stated before opening any
packet or source: no memory summary, project history, candidate verdict or finding was
injected. I was the sole reviewer; no delegation, other agent, or reviewer contact occurred.

Inventory: `D:/Pontius/tmp/solve-r003-cold-20260910/reviewer-01/inventory-01-codex-cold.md`.
SHA-256: `276514b46eda6bc6e60b74d7212cafb543e9f70d2095aa10307e2846c0911106`.
It was written and hashed after steps 1–3, before opening any step-4 check/rehearsal input.
Its final hash equals the original seal; it has never been revised. Checks/rehearsal, then
authorization/campaign, then deferred predecessors, then governing documents followed.

**M-01 — Minor: C9 does not assert its advertised caller-status outcome.**

Location: `checks/wrapper-checks.sh:127–131`, assertion implementation `:26–33`;
claim: `authorization-request.md:59–67`; obligation: `handoff.md:81–84` (acceptance 4).

C9 computes RACE from RA/RB, but supplies it only inside the condition-name string.
`assert C9-race-one-claim 0 0 "launches($RACE)" 1 "$LAUNCHES"` compares literal 0 to 0
and one capture pathname to the expected 1. It never compares RACE with
`one-winner-one-refusal`. The failure accumulator and final nonzero exit work only for
comparisons actually supplied to assert.

Concrete reachable counterexample: the winner claims and creates stdout, then its child
fails or evidence becomes incomplete; the other caller returns 97. RA=1, RB=97 and one
stdout path still produce pass=true and no failure increment. The recorded C13 boundary
already demonstrates that a claimed launch can fail this way. A hypothetical regression
allowing two callers to reuse one pathname likewise cannot be detected by counting that
pathname alone. An independent stdlib model of the exact assertion confirms that (0,97),
(1,97), and (0,0) all pass when LAUNCHES=1; no race or script was executed in this review.

Consequence: the suite can report success without the claimed successful-winner/refused-loser
outcome. This does not invalidate the present captures: caller A records completed/BOUND;
caller B records claim refusal, and jsonl records the expected statuses. Assert both the
status pair and the capture condition. The actual atomic claim remains sound.

**M-02 — Minor: an explicitly empty REHEARSAL bypasses the literal 0/1 guard.**

Location: `invoke.sh:43,50–58`; promises: `identity.json:124`,
`authorization-request.md:30`; obligation: `handoff.md:76–77` (acceptance 2).

`${REHEARSAL:-0}` replaces both an unset variable and an explicitly empty string with 0
before the case statement. A caller supplying REHEARSAL="", with no root overrides and
otherwise satisfied authorization/preconditions, reaches the retained launch. It does not
receive the promised exit 84 for a value other than 0 or 1. The guard is positioned before
the branch, but after this normalization. C10/C11 cover 2 and yes, not empty.

Consequence: an empty configuration value silently chooses retained mode. This is a narrow
input-contract defect, not an authorization bypass: authorization, fixed roots and the
claim still apply, and the normalized records remain valid JSON. Preserve unset-default
behavior while rejecting explicitly empty input, or explicitly document empty as another
default and adjust the acceptance claim. This path was traced statically, not launched.

**M-03 — Minor: the blanket claim-consumption promise includes pre-claim refusals.**

Location: `invoke.sh:24–25,50–99`; repeated in `identity.json:141` and
`authorization-request.md:36–37`; obligation: `handoff.md:72–75` (acceptance 1).

The documents say every failing path leaves the claim consumed. For example, a fresh
retained invocation with authorization present but a wrong plan digest exits 92 at line 74,
before claim.d is created at line 99. Nothing in that path consumes the claim. After the
plan is restored to the already-bound bytes, the wrapper can be called again and claim.
Missing authorization, invalid mode and other preconditions have the same pre-claim scope.

Consequence: an operator cannot infer consumed-claim state from every nonzero wrapper exit
as the prose suggests. There is no demonstrated duplicate solve: these refusals precede the
solve launch, and post-claim failures preserve the claim. State that every failure after
successful claim acquisition leaves it consumed, distinguishing precondition refusal from
a claimed attempt. The corrected child-status precedence itself is accurate.

**Complete acceptance and closure/evidence matrix.** Inventory identifiers refer to the
immutable predicates, not predecessor verdicts.

| Question | Independent evidence and conclusion |
| --- | --- |
| 1. Exit contract (I04–I06) | `invoke.sh:154–156` returns nonzero child status first, then 99 for zero child plus incomplete evidence, else 0. Header/identity/authorization agree on that precedence. M-03 remains in the blanket claim wording. No successful exit with incomplete required evidence was found through the supported producer/caller. An unwritable end record cannot itself persist its failure; line 149 still forces incomplete/nonzero. |
| 2. REHEARSAL guard (I03) | Nonempty invalid values stop at 84 before branching. Empty input is the M-02 exception. Intended default/0/1 paths preserve the roots and authorization boundary. |
| 3. Four earlier Important properties (I03–I06) | CLOSED independently: atomic mkdir at 99 before launch 112; fixed retained roots and nonempty overrides refused at 54–58; separate detached rehearsal root at 60–66; claim/start writes checked at 101–107 and evidence writes at 123–155; helper checks one new line and matching result bytes at 24–60, with no older-row substitution. This closure depends on the ownership boundary below. |
| 4. Honest checks (I08) | General assert/failure propagation works; recorded 18 comparisons pass. C9 is incomplete (M-01). C12 is explicitly a one-line LOG-target mutant; reconstructing its bytes in memory gives `d829047e38ae56bf76f6837d5c2739806d7583d847ed854deabd0f232ba03f57`, matching the diff/identity. Capture shows start append refused, exit 98/no launch. C13 shows child 1, ABSENT, unchanged 59 rows, incomplete evidence and nonzero precedence; limits below. |
| 5. Rehearsal consistency (I09) | PASS for reproducible capture assertions: 1081 teacher-hand observations + artifact + summary; 545 raises/536 checks; zero exact ties; ordered full pool; matching raw/LF/result/row hashes and reconstructed teacher. Receipt marks evidence=false. The carried campaign note's 19-second figure is historical; this r003 receipt/log records 16 seconds. |
| 6. Residual risk (I04–I07,I10) | Exclusive checkout/journal ownership, authentic authorization, preservation of consumed records, immutable launch inputs and retention/mirroring remain operator duties. A per-packet claim is not a global lock or supervisor. |
| 7. Forbidden claims (I02,I07,I10) | PASS: solve alone is requested; no teacher-strength or retained host-agreement proof, export/agreement authorization, or envelope change. `brief.md:90–91,110–112,141–144`; `design.md:10–27,142–168,307–315`; resource decision `:10–22`. |

**Identity and actual boundaries.** All 33 manifest members match raw bytes; whole-row
byte sorting and LF termination match. Manifest SHA-256 is
`9e98d06dd4d605a236a5def7663cb7a65b793e83922fb5a6d1e9a9e1c7fee05d`, matching candidate.json.
HEAD and read-only remote adopted ref both equal the source commit; tree is
`3d2fe79d2af20125e322dd4a668335e789810863`. Checkout branch is `claude/eval-panel-solve`;
status is only `?? plans/`; seven on-disk run directories equal the frozen tracked census.
Identity-only hashing of 892 source-scope checkout files found zero canonical differences
from frozen blobs; 870 raw newline differences explain the distinct frozen raw aggregate.
The checkout aggregate matches `bac14bea3e9a4e4c8c120556311447262d7775de54e39ef121c02bb2c59eb204`.
Worktree bytes were used only for identity hashing, never behavioral review.

The plan copies are byte-identical: 12,365 bytes, SHA-256
`c1a6af606cc80841d61b5824913c8a1b6c896988ae4c578127c1dfc08b4f8982`.
Independent card enumeration and CPython seeded shuffle reproduce all 1,081 names, universe
and permutation digests. All three prerequisite files match both plan bindings and frozen
PREREQUISITES; capacity/preflight completion predicates hold. The helper pin matches.
Exact schema, board, stack/prefix, runtime, empty solve inputs and 600 s/2048 MiB conform to
entry `validate_plan:131–196` and completion `validate:97–146`; project validators were not run.

The caller passes one immutable admitted plan into supervision. The worker is created
suspended, assigned to the memory-limited Job, then resumed (`v0a_eval_panel.py:431–449`;
`v0a_table_host.py:326–445`). Completion reconciles the full ordered census, applicable tie
reference, teacher bytes and cleanup before success; retention precedes finish_run.
The parent creates a UUID directory (`v0a_eval_panel.py:630–668`), while
`execution.py:122–162` constrains result location, writes/hashes result and runtimes, appends
through `status_generation.py:28–35`, then renders STATUS. No phase calls the next phase.

The helper alone accepts broader inputs than this producer: it does not enforce containment,
fresh UUID, phase, command, source_verified or source digest. Under the adopted producer,
the newly appended row names the newly created in-root result; no supported path was found
that substitutes an old/external result. Forged/copied journal rows and unrelated writers
are outside the disclosed ownership assumption, not demonstrated failures of this solve.

**Coverage limits and observations.** C13's runner description is consistent with the actual
import boundary: entry line 36 imports pontius.execution, which first loads
`pontius/__init__.py:14` -> `full_width_belief.py:17` -> NumPy. Missing NumPy can therefore
exit before begin_run, leaving no result or row. Captures establish the compound outcome;
the original child traceback is not a manifest member, so the specific environment fault
is supported by the runner account and source trace, not independently re-read stderr.
This is an alternative pre-owner failure trigger to the predecessor's transient Git example.

The checks do not execute every write failure, a zero-child/incomplete-evidence 99 case,
helper copy-content validation, arbitrary malformed journals, or interrupted cleanup.
C7 is a file occupying the output-directory path, not a real permission denial. C12 proves
the injected start-write boundary only, not all filesystem failures. Six C8 cases assert
return status and row existence, not exact copied bytes. These limits do not reopen the
statically checked fail-closed paths or turn 18 recorded passes into exhaustive coverage.

Recomputed production seconds min/max/mean/sum are 0.0130621/0.0668351/0.0139907/15.1239705;
worker 15.6868549 seconds; journal duration 16.0657699; peak worker Job 787.140625 MiB.
Normalized stdout is the 527,216-byte result bound by the row. Independent serialization of
captured rows gives the 241,587-byte teacher with SHA-256
`c3ffab403eb7e939857cc31b0f21b255cefdffd8b0d26d078b703c1fe956b3e3`.
This reconstructs captured policy bytes; it does not independently solve poker hands.
Deleted snapshot teacher/runtimes files and native cleanup cannot be freshly inspected.
Chain-receipt measurements remain receipt-only: its raw captures are outside allowed inputs.
Campaign planning arithmetic agrees; worker Job versus unmeasured parent memory is correctly
distinguished, and later envelopes remain undecided.

Operator ownership also includes selecting the reviewed wrapper/helper/environment, preventing
concurrent edits/direct launchers, preserving abandoned claims, and deciding any ambiguous
interruption before another authorization. File existence alone does not authenticate an
authorization. No claim or reviewed code automatically implements permanent mirroring.

**Exposure and method disclosure.** Before sealing, required handoff/identity disclosed r001
NOT CLEAN/four Important defects, r002 follow-up CLEAN/SOUND and cold NOT CLEAN/SOUND, the
exit-precedence Minor, proposed closures and producer-ownership assumption. Step-4 comments
and step-5 prose repeated finding labels/closure claims; campaign also mentions prior memory
findings. None supplied this review's verdict.

Only at step 6, after the seal and independent candidate inspection, I opened the named
predecessor review directories, their review/coordination records, r002 disposition/addendum
and r001 disposition. Exposure included r001's NOT CLEAN verdicts (5 Important/1 Minor versus
4 Important/2 Minor), manifest grading reconciliation to Minor, the four wrapper defects,
memory wording, r002's four Minor follow-up observations and its cold exit-contract finding.
Those records also relay older CLEAN/SOUND/GREEN adoption labels, prior diagnostic I-01 and
historical test assertions. They were used to identify historical issues and exposure, not
to inherit a verdict or treat prior tests as fresh evidence. Governing documents mention
accepted predecessors; resource-decision records controller envelope approval. No linked
adoption reports, older source reviews, memories or histories were followed.

No current reviews directory, unmanifested check, review inventory/verification, progress.md,
INDEX.md, other scratch, launch log or unrelated report was opened. No invocation/check
script, project test, solve, export, agreement or rehearsal was executed; no source edit,
Git mutation, publication or ledger append occurred. Only the two requested artifacts were
written. Utilities were PowerShell/.NET, the specified Git, and exclusively CPython 3.14.6
with -I -B for inline stdlib calculations. Initial interpreter access and network checks
were blocked in the sandbox; approved read-only retries succeeded. No required identity
check remains blocked. The execution-checkout venv itself was not launched or reinstalled.
