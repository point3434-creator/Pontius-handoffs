# Independent cold-review invariant inventory

Packet: solve-run-20260910-r003. Reviewer: sole Codex cold reviewer. Date: 2026-09-10.
CONTEXT_PROBE_NONE: before opening packet/source, no injected memory summary, prior project
history, candidate verdict or finding was present; only generic instructions/environment.

This inventory is sealed after handoff steps 1-3 and before any step-4 check/rehearsal
content, step-5 prose, or step-6 predecessor reviews/dispositions. It must never be revised.
The final review will report outcomes against these predicates, including any new findings.

Exposure already received from mandatory inputs: handoff.md describes r002 NOT CLEAN,
its child-exit-status Minor, r001/r002 finding labels and the sole-producer assumption;
identity.json describes r001 two NOT CLEAN reviews/four Important defects, r002 follow-up
CLEAN/SOUND and cold NOT CLEAN/SOUND, and claims closure of remaining Minors. These are
candidate assertions, not independent verdicts. No deferred review has been opened.

## Independent predicates and boundary map

I01 Identity: raw packet files must match the manifest, whose whole rows are byte-sorted
and LF-terminated; candidate wrapper digest must agree. Source commit/tree, remote adopted
ref, checkout HEAD/status, plan duplicate, three prerequisite hashes and helper pin must
match. Behavioral source comes exclusively from frozen Git blobs; no project code executes.
Observed before seal: HEAD 1c7067448106cfa2aca3d57be879842d72293c61;
tree 3d2fe79d2af20125e322dd4a668335e789810863; status only ?? plans/.
Remote query was blocked by network connectivity; retry read-only if permitted, otherwise
report the limitation. Complete manifest verification is deferred until after sealing so
it cannot read step-4 inputs prematurely.

I02 Admission: exact solve schema, declared-full board, stack 4 and replay prefix; runtime
3.14.6; 1081 unique compatible hands in the seeded order; empty inputs/no witness bank;
600 seconds and 2048 MiB; pinned completed capacity/preflight and decision. Entry validator
131-196 delegates completion schema to completion.validate 97-146 and recursively validates
base geometry/runtime/order before checking prerequisites and phase-specific fields.
Independent stdlib calculations already match 12365 plan bytes, c1a6af606cc80841d61b5824913c8a1b6c896988ae4c578127c1dfc08b4f8982,
checkout copy, all prerequisite hashes, universe 18953f113d65c6e25111ac9c2441942e4145051e169261fecd0ed0b9e5be41ed
and permutation 344e7eeb06d72b97313f470880b8d169c4674e83bb440de827fa6fb87d97648a.

I03 Modes/authority: exactly one selected mode; invalid REHEARSAL refused before branching;
retained roots fixed, overrides refused, authorization required; rehearsal detached and
outside retained checkout. Inspect empty/unset separately: invoke.sh:43 uses ${REHEARSAL:-0},
so an explicitly empty value becomes 0 before guard 50-53. Compare this to the literal
'exactly 0 or 1' promise. Empty override variables are also treated as absent (55).
Authorization file content is not validated (58); authorization authenticity and choosing
the reviewed bytes therefore remain operator responsibilities, not a cryptographic gate.

I04 One-shot: claim mkdir precedes the sole solve launch, remains after any post-claim
failure/interruption, and concurrent callers cannot both acquire it. Preconditions and
record errors must fail closed. Distinguish pre-claim refusals from consumed attempts:
header 24-25 says 'every failing path' consumes the claim although exits 84/88/89 etc.
precede mkdir. Decide whether the scope is clear in final authorization prose.
Claims depend on operator preservation, fixed checkout ownership, no direct alternate
launcher, and no concurrent source/plan/journal changes; a filesystem marker is not a
host-wide execution or supervisor lock.

I05 Records/exit: claim/start writes checked before launch; capture redirection, helper,
hashes, retained listing and final record errors propagate to incomplete evidence. Actual
post-launch precedence at 154-156 is nonzero child unchanged, else incomplete -> 99, else 0.
Compare all prose to that scope, including final-record failure which cannot guarantee a
persisted end record. Do not assume child rc=0 independently proves teacher strength.

I06 Actual producer attribution: wrapper captures baseline newline count then calls one
parent. eval-panel main 630-668 begins source verification, allocates UUID run directory,
writes runtimes, validates/supervises/retains artifacts, and finally calls finish_run.
execution.finish_run 122-162 writes result bytes, hashes result/runtimes and invokes
status_generation.append_run 28-35, then regenerates STATUS. Helper 24-60 accepts exactly
one added line with expected commit and matching result (+ optional runtimes), then copies
that new row; no old-row fallback. It does not constrain path containment, phase/command,
fresh UUID, source_verified or source digest independently. Determine material reachability
through this producer/caller, rather than treating arbitrary forged rows as supported input.
Parent begin_run can fail before journal creation; worker exceptions/cleanup failures must
not silently become successful evidence. Partial append/copy failures must fail nonzero.

I07 Solve completion/resources: one suspended worker assigned to memory-limited job before
resume; deadline and independent cleanup attempts. Completion requires ordered full hand
rows, first nonzero-return tie reference if present, correct artifact digest/contents and
successful cleanup. Parent retention must finish before its completed result and journal.
Trace solve 189-226 -> complete 376-436 -> retain 466-487 -> finish_run; no implicit export
or agreement. Inspect any remaining needed frozen dependency boundaries, not worktree code.

I08 Check honesty (deferred): runner must assert expected rc and substantive property,
accumulate failures and exit nonzero. Read all manifest-listed per-case captures. C12 must
be a labeled precise diff/digest mutant limited to unavailable write-denial emulation;
C13 must exercise real child failure plus failed evidence, not fabricated helper output.
Race evidence must demonstrate one launch, with limits acknowledged. Missing boundary
cases do not become proven merely from '18 cases, 0 failures'. Never execute the runner.

I09 Rehearsal (deferred): derive receipt from logs, captures, row, raw/LF-normalized hashes,
retained-file listing, observation counts, timing, resource/cleanup and tie evidence.
Deleted snapshot artifacts permit internal consistency verification only, not fresh disk
verification. Chain receipt is separate preparation evidence, never retained phase proof.

I10 Authority/claims (deferred): reconcile authorization request and campaign note with
actual contract and governing brief/design/resource decision. Cover all seven acceptance
questions, not only predecessor closure. No teacher-strength, host-agreement, export or
agreement authorization claim. Controller envelope unchanged. Name operator-dependent
one-shot/evidence properties before authorization.

## Review method and remaining sequence

Read only manifest-listed current files and identity wrappers, explicitly named governing/
deferred inputs, and frozen behavioral dependencies needed to trace named validators and
actual caller/producer boundaries. No current reviews/check inventories, ledger, memories,
other scratch, launch logs, unrelated reports, project tests or phase execution. Only this
inventory and the final review may be written in the exclusive reviewer directory.
Next: hash this file; step 4 checks then rehearsal then chain receipt; step 5 authorization
then campaign; step 6 named predecessor reviews/dispositions; step 7 frozen brief/design
and resource decision. Historical exposure must be disclosed and not adopted as verdict.
