# Cold review 01: v0a-eval-panel-impl/r002

Reviewer: Codex, independent cold pass 01. Issued 2026-09-09.
Defect verdict: CLEAN. Design verdict: SOUND.
Scope: Tier C, Stage 0 / Stage 0b specification review of both complete documents.
No Critical or Important finding survives frozen-source and arithmetic verification.
This verdict approves the specification at this boundary, not implemented behavior.

Candidate: b13709ffddbf3000e019641fd123239a24f2cd75
Manifest: 98df5d549736200115732bc2a49f8cc1d3e9ec5e61c7083d710b8af87b1f0822
Base: 46f45298a405b967976413a4b8e45e7837602316
Tree: a29d1db3f4c03b8d9c19edb02cfa93af4b0fb7e7
Ref: refs/heads/review/v0a-eval-panel-impl/r002

In this report, brief/design locations mean the candidate's
`docs/architecture/v0a-eval-panel-impl-r001/{brief,design}.md`.
All source locations mean frozen Base blobs, never mutable source files.

## Independence and identity

The handoff was the first packet input. I read the candidate, pinned authority,
parent specification, README and workflow amendment before recording my independent
inventory. I did not read sibling reports, task/program ledgers or chat history.
I then opened coverage.md and the two explicitly deferred dispositions. Author
check files were not used as evidence for this verdict.

The preserved pre-deferred inventory is eval-impl-r002-review-01-inventory.md:
SHA-256 5c31f6cee88bd352f949947938f787550d5a046f1c097448de33659f64eb9f1e.
It records ten invariant groups and their related paths and falsifiers.

Independent Git checks established the exact ref, single parent and tree above.
The complete no-renames diff consists of the two added specification documents.
Stored-blob hashes, sorted as complete digest-first LF rows, reproduce the packet
manifest byte-for-byte and its declared SHA-256. Both blobs satisfy LF-only,
no BOM, no trailing whitespace and at most 100 columns. Their SHA-256 values are:

- brief.md: e100b0e77bb05ceafafa557553ccacae5952627c8becdb1d3d726228d97e7128
- design.md: 6c69179ba114dfe83c9ef27121c7819e34ebda5cd0f7057265e1e5aa789c43d6

All 34 dependency Git pins resolve against Base. Workflow bytes equal the Base
workflow blob. The workflow, controller-rulings and dependencies file hashes match
the handoff. After inventory recording, the coverage and both disposition hashes
also matched their handoff pins. No identity depends on a worktree reconstruction.

## Numerical acceptance: the deferred Important gap is closed in the specification

Design 3, lines 82-134, specifies the real APIs: construct one singleton game,
force each hero action through expected_utilities with an explicit CALL villain
policy, and separately call best_response for its value and selected map.
BASE evaluation.py:15-87 normalizes policy distributions and evaluates all branches;
missing entries are uniform. Its best_response at 257-280 returns a selected map
and a fresh expected_utilities result, not a per-action table. The design neither
invents such a table nor relies on the uniform fallback.

BASE river.py:203-229 sums exactly 990 distinct unit raw weights and divides each
by their exactly representable total. The continuation at 288-307 converts kernel
integer net returns to floats. The replayed s=4 root gives CHECK returns -2/0/+2
and bet/CALL returns -4/0/+4: the two live seats have committed two each, and
bet/CALL commits their last two each. Kernel settle at no_limit_betting.py:696-750
uses integer payouts minus contributions. No odd chip arises for these equal
contributions. Zero-probability fold branches and probability-one policy arithmetic
remain exact; only normalized chance weights and their accumulation need a bound.

The expected_utilities chance loop uses explicit += for its 990 terms. With
D=2^53, the candidate bound 4*(u+(1+u)*gamma_989) simplifies to 3960/(D-989).
Independent native BigInteger arithmetic verified that this is less than 2^-40,
that 4*gamma_1000 is also less than 2^-40, and that 2*2^-40 < 1/990.
This proof is about the stated binary64/domain assumptions. It does not depend on
Python's built-in sum behavior for the best-response action argmax.

The acceptance rule reconstructs each exact integer numerator independently from
its finite dyadic reference interval, then requires equality with production's
corresponding total. A false production tie cannot supply its own oracle. At a
validated tie, production/export must CHECK while either legal reference label
may pass. At unequal reconstructed totals, both the production maximizer and
reference action must agree exactly. A wrong non-tie action cannot pass merely
because its floating value is close. Nonfinite values and malformed maps fail.

Independent rational illustrations with R=-2^-55, 0 and +2^-55 accepted only
J=0 and rejected adjacent J=-1,+1 under this bound. These are arithmetic-only
controls; they do not identify a legal board/hero hand or exercise either Python
evaluator. The general lattice separation also excludes overlapping adjacent
integer intervals, including both signs of a nonzero gap.

Design 3, lines 136-148, correctly retains the all-zero control, discriminating
cancellation and false-tie fixtures, and an actual singleton check for the first
nonzero-return exact tie found during a completed H census. An incomplete census
cannot assert absence. Both supported-interpreter executions remain future checks.
The earlier gap is therefore closed as an acceptance specification; no previously
observed poker failure or measured frequency is claimed.

## Full-candidate contract assessment

- Capacity and membership: brief 1/4 and design 2/4 require public root replay,
  exact decoded key/action equality, the complement of H, monotone nested prefixes,
  fixed-width source identity and final solved-wire remeasurement. BASE codec.py
  admits and sorts exact keys, then emits compact deterministic ASCII JSON plus LF;
  CHECK/null is three bytes longer than raise/2. The cap is enforced on actual
  bytes by Session.prepare:214 and host OwnedInput:118-140. The text does not turn
  the historical 883 count into a universal limit or invent an overflow beyond 1081.
- Root and key: BASE tests/test_legal_river_continuation.py:29-56 supplies the public
  prefix pattern; no_limit_betting.py:392-422 bounds the s=4 bet to raise_to(2).
  Immutable key from_state:49-114 includes all public history and board order.
  The candidate explicitly covers altered stacks/prefixes and reversed board input.
  Existing s=6 fixtures are source references, not claimed executed s=4 evidence.
- Cost and phase stops: brief 2/3 and design 3/6 separately account for reference
  construction, both forced calls, best response and comparison. Cached ranker calls
  in river.py:164-178 make cold/warm and ordering disclosures necessary; these are
  required. Finite launch limits, preserved partial observations and a later measured
  decision prevent preflight from silently becoming a full-pool solve.
- Witnesses: design 4 requires actual finite-bank census and a seeded witness for
  every h in H, preserving all twelve cards. BASE deal_for_hand:58-65 restricts
  each seed to indices 0-15. Collision-only board rejection and first accepted
  witness selection are compatible with that API. Sizing assumptions do not certify
  completeness; test subsets, synthetic CHECK/off-pool controls and Slice B sampling
  are explicitly distinguished. Missing witnesses cannot silently shrink H.
- Outcome and failure: design 5 reads hands[*].result, which is the actual wrapper
  created at Session.play_hand:258-260. Session run/cleanup paths retain launch,
  transport, process-exit, rendering and cleanup failures before completion. Host
  WireConsumer:817-913 checks event failure, terminal settlement and final closure.
  Adapter run_session:218-307 can fail after action or hand publication. The design
  excludes such attempts before interpreting any river record, including missing,
  malformed or truncated captures. Exactly-one-river applies only to agreement;
  a completed prefix-diverged baseline keeps separate chip eligibility.
- Reason and provider independence: trace.py:216-252 puts delivery status on failure
  payloads, not v1 DecisionRecord. Runtime:363 uses no provider for blueprint-v1;
  host:795-815 validates v1 records without independently recomputing their lookup.
  PreparedBlueprint.action_for and BlueprintProvider.propose are actual distinct
  boundaries. Design 4/5 requires both, and independently reconciles the retained
  table_hit/passive_default reason so an identical CHECK action cannot hide a miss.
- Ownership: design 6:270-277 addresses the actual cwd precondition. Session.prepare
  admits Path.cwd(); Admission caches its host module; Source uses inherited context;
  execution.begin_run:37-44 rejects a different root. Normal preparation still loads
  each session schedule/artifact. execution.finish_run:122-170 returns for inherited
  contexts and otherwise writes the retained result and one journal append through
  status_generation.py:28-35. The existing source and writer paths can support the
  stated parent/worker split without editing host/session code.

These are static specification passes, not runtime or implementation passes.
The current tests manifest/harness is the required registration seam; source code
and test size, executed coverage, resource fit and performance remain unmeasured.

## Deferred coverage comparison and workflow checklist

The FIX claim's numerical category matches inventory groups 2-4, including unit
weights, fixed CALL, settlement, forced-action accumulation, lattice reconstruction,
argmax tie policy, cost and refusal. Its discovery chain reaches each declared
consumer of the changed rule. Inventory groups 1 and 5-10 separately covered the
complete candidate's authority, export, host, witnesses, accounting and ownership.
Thus the narrow FIX category did not replace the full-candidate review.

The deferred claim's cases and falsifiers match the recorded inventory: cancellation
of either sign, false tie, changed total, smallest gap in both directions, invalid
map/value/domain, interruption, worker root and witness completeness. Its limits
correctly call fixtures and arithmetic planned evidence. The package __init__ files
independently discovered through imports are inert at Base; this adds no missing
normative mechanism. The inventory remains a direct semantic map, not import closure.
The prior and parent dispositions supplied constraints only after independent work.

Checklist v1 assessment at this specification boundary:

1. Real contract/oracle: independent forced evaluations and real host/provider checks
   are required; fixtures are labeled and cannot certify the boundary they replace.
2-5. Subprocess, cross-boundary, imports and isolation: actual session/child APIs
   support the design; scrubbed environment, absolute PONTIUS_GIT, -B -P imports,
   disposable snapshots and real retained frames remain explicit code-stage checks.
6. Failure coverage: nullable/no-decision failures, late failures, incomplete closure,
   malformed/truncated streams and wrong record multiplicity are included.
7-8. Budgets/minimal gates: measured cost comes before adoption of resource limits;
   lattice validation admits a valid tie without relaxing wrong non-ties; capacity
   is domain-specific and witness acceptance uses the actual census.
9. Ownership: parent/context inheritance, normal preparation and no per-cell run rows
   fit existing public ownership. New worker launch/kill controls still need execution.
10-11. Exactness/identity: exact arithmetic rule and strict future evidence inputs are
   specified; fresh blob/text/pin/manifest checks passed for this frozen candidate.

## Design verdict, advisories and remaining authority

SOUND. Early capacity and bounded per-hand preflight expose the two feasibility
risks before bridge completion. The correction belongs at caller-side reference
acceptance, preserving the sealed game/evaluator and the canonical exported policy.
No larger solver, codec or lifecycle replacement is warranted by this review.

No additional corrective advisory is required. Existing obligations remain material:
execute both interpreter/domain controls, measure total reference overhead and cold
cost, freeze a finite witness bank with rationale, establish actual coverage, and
exercise real host failure boundaries. The combined 600 production/400 test-line
allowance is not verified until code exists. Brief:161-170 explicitly consumes the
two-round Slice A allowance in r001/r002; checkpoints do not reset it. Any later
candidate review requires controller reauthorization. CLEAN grants no such extension,
implementation/run authority, integration or ceremonial commit.

## Commands and evidence limits

Read-only git rev-parse, show, diff-tree, cat-file and grep operations inspected the
identified frozen blobs. PowerShell Get-FileHash checked packet hashes. A temporary
Python stdin helper used only pathlib/subprocess/hashlib/json for identity checks:
its initial interpreter start was denied in the sandbox; the required escalated
retry completed identity and dependency checks, then failed while printing Unicode
parent prose through cp1252. Missing prose was subsequently read through Git directly.
No project imports or project execution occurred in that helper.

A first native arithmetic helper failed on PowerShell's Int32-to-BigInteger comparison
coercion. The corrected explicit-BigInteger helper exited 0 and produced the exact
inequalities and three rational illustrations reported above. This was reviewer
arithmetic, not solver/test execution or an author receipt.

No fetch, runtime, solver, host, historical owner, test suite, experiment or retained
measurement was invoked. No production source, frozen packet, existing report or
mutable journal was edited. Primary status already showed STATUS.md and
execution_journal.jsonl modified; neither content was used as review evidence.
No legal non-degenerate tie witness, measured capacity, cost, host agreement rate,
resource sufficiency, test pass or poker-strength claim follows from this review.
