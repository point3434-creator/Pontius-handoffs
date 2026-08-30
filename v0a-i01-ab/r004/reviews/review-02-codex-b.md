# Cold B review: v0a-i01-ab/r004

Reviewer: Codex /root/ab_r004_cold_b. Date: 2026-08-30.
Tier C FIX; V-01/V-02/V-03 value admission only.

**Defect verdict: CLEAN.** No required correction remains in this review's scope.
**Design verdict: SOUND.** The bounded ingress shape fits the three contracts.
Specification: PASS for the named required outcomes under the tested schedules.
Engineering quality: PASS with one nonblocking formatting note below.
This is one independent cold pass, not release or experiment authorization.

## Candidate identity and independence

- Ref: refs/heads/review/v0a-i01-ab/r004
- Commit: c6adbcaa048988361d2388970eaca772711b797b
- Base: 30df7bce8da51715e6f1d7576892dd689421c516
- Tree: 1b6edef1e943483e0a83ec33f1bcc61348ada166
- Manifest SHA-256: a810c89b7342fb1bcb4f1498fdcf53cd11a589b70424c7da48f6619a45da67cb

I independently recomputed SHA-256 for all changed frozen blobs, sorted complete
manifest rows by row bytes, and verified both the resulting digest and the packet
manifest file bytes. Only model.py, runtime.py and test_v0a_hand_replay.py differ
from the base. Snapshot file bytes for those paths equal the blobs.

Permitted inputs only: handoff/candidate/manifest, frozen source and tests,
ADR-0485 and ADR-0484 brief, current CLAUDE.md/workflow.md, and required outcomes in
v0a-i01-value-boundaries/r001/disposition.md. No implementer narrative, self-report,
current peer report or current peer findings were read. The coverage claim was
opened only after the independent inventory was written:

checks/cold-b-inventory-before-coverage.md
SHA-256 ba1386402f335bc3dbc32986dcdfce0400d92a46818a793b9bd63bb2004fa496.

Coverage.md SHA-256 independently verified as
1a6b52be5295fdcca59b9c112dea56210945ec6c6cb919833f9c57a076adae58.

## Required findings

None. I found no reproducible material requirement violation and no blocking
coverage gap within the declared contracts. The following are observations and
opposing controls, not an inference from constructors or helper doubles alone.

| Contract | Fresh direct evidence | Result |
| --- | --- | --- |
| V-01 exact immutable event graph | 24 outer-subclass cases across all four variants; wrong schema, bool/float/negative indices and malformed IDs; four exact outer opponent events with invalid or subclassed nested HandAction | Typed invalid_event, null unadmitted event index, identical public betting state/history and mailbox contents, no completion or extra action |
| V-01 ordinary semantic input | Exact start whose stacks cannot cover blinds; exact wrong actor/street/hand/index; known-card overlap after a legal completed preflop round | Typed failure before state or mailbox effects; safe admitted integer metadata retained |
| V-01 showdown | Legally reached river completion with all six live and with one fold; mutable/empty vectors, empty/bool/float ranks, exact mixed int/tuple ranks and bad live-seat masks | Refused before terminal transition/completion; no new delivery; mutable rejected vector could not supply settlement |
| V-01 valid settlement | Eight independent equal-contribution controls: int, tuple, differing tuple lengths and ties, each with/without a folded seat | Exact expected 12-chip/10-chip payouts; repeat-stable settlement; 600 total chips conserved; four controlled deliveries retained |
| V-01 timing/metadata | Real outer boundary with deterministic clock; first-read, boundary-read and cleanup clock faults; hostile metadata object on fresh/dead/complete/clock branches | Ordinary invalid input charged the measured 1ms boundary; invalid_event precedes cleanup clock_invalid; clock-first cases retain clock priority; zero metadata callbacks |
| V-02 mailbox | Ten malformed outer envelope schedules plus two exact-outer/nested-action schedules, followed by valid same-key delivery | No bad insertion/key poisoning; subsequent valid key accepted once; exact receipt returned; duplicate refused without replacement |
| V-03 acknowledgement | Eight malformed/nonmatching receipt schedules after Forward actually calls real ActionMailbox.deliver; exact valid receipt opposing control | One physical acceptance and one committed controlled action remain; unknown delivery_ambiguous, acknowledged count zero and no retry; valid exact receipt yields known count one |
| Known-delivery preservation | Genuine acceptance followed by a closing clock fault | Accepted status/count and full decision record remain known; clock failure does not erase delivery |
| Existing behavior | Frozen affected test_v0a_hand_replay.py, including policy admission/refusal, clocks, fold terminal, repeated actions and settlement controls | 45 tests PASS on each interpreter |

All 80 direct observation records are identical across the two interpreters.
The probe asserts complete state equality for rejection and separately records
history length, delivery counts and chip conservation. Receipt schedules also
observe the actual committed state history and real mailbox contents. Positive
settlement expectations come from the simple contribution schedules, not from
calling production settlement as its own oracle.

## Coverage and design assessment

The claim's discovery of seven ingress records matches my independently recorded
inventory. I followed dispatch through all four handlers, complete-event refusal
metadata, mailbox preparation/insertion, acknowledgement matching, and the sealed
settlement consumer's max/equality requirement. The claim explicitly includes
live-seat masks and normally constructed mixed rank domains, so these are not
hidden constructor-only checks. My additional wrong-exact receipt identities,
null/foreign receipts, full six-seat showdown, tied payouts, and differing tuple
lengths supplied independent opposing cases. No material omitted path was found.

The shared exact-graph admission is appropriate for this closed set of values.
It refuses foreign subclasses before inspecting their fields and reconstructs
nested values using fixed exact constructors. Event admission is inside the
existing measured transition. State-dependent rank/mask validation precedes
terminal mutation, envelope and receipt preparation precede mailbox insertion,
and receipt admission precedes equality and known-delivery count. These are the
three real commit boundaries identified by the required-outcome disposition.
The change does not require a whole-runtime or sealed-spine redesign.

This review does not adopt the coverage claim's reported 137-test count as fresh
evidence: I ran the affected 45-test suite and my independent 80 observations.
I did not inspect its implementer receipts or use them to issue this verdict.

## Commands, environment and evidence

Fresh detached shared-object clone outside the packet:
D:/Pontius-review-snapshots/v0a-i01-ab-r004-cold-b-8b743e9f.
No source overlay or source/test modification. Every payload ran from that root
with -B -P, PYTHONPATH set exactly to its src, empty PATH, environment cleared
except explicit Windows prerequisites and bound settings, and absolute regular
non-reparse C:/Program Files/Git/cmd/git.exe as PONTIUS_GIT.

checks/cold-b-run.ps1 records exact executable, arguments, cwd, environment,
script hash, UTC start/end, stdout/stderr and exit code. Drivers assert actual
CPython/full version before payload imports, and verify snapshot module origins.
Actual 3.11.15 ran first; actual 3.14.6 followed only after floor checks passed.

| Receipt | Execution | Exit/result | SHA-256 |
| --- | --- | --- | --- |
| cold-b-identity-py311.json | D:/Pontius-tools/py311/Scripts/python.exe -B -P cold-b-identity.py | 0; identity/manifest/blobs/clean | 47d2b50744796d45dc67d236c7c744caa9458395321c85a3dab55a6901e16b0e |
| cold-b-probes-v2-py311.json | Same executable -B -P cold-b-probes-v2.py | 0; 80 observations PASS | b5bbef6f8f0edce29e63494293cb5988bc95923f2cd1cc06e1c8ebdcb898400b |
| cold-b-suite-py311.json | Same executable -B -P cold-b-suite.py | 0; 45 tests PASS | ea3ebee36f5e4394ab75617578d68a347b0cacf52a4c3074f2fdda331a0f5ded |
| cold-b-static-py311.json | Same executable -B -P cold-b-static.py | 0; exact diff and hygiene inspection | abf374782ba530519f1ff11c9f89f56ca244142e2a23bb06f4601c0805ea83a7 |
| cold-b-identity-py314.json | D:/Pontius/.venv/Scripts/python.exe -B -P cold-b-identity.py | 0; identity/manifest/blobs/clean | 111dbc190b6e0cf97f9c99a53b2ae9c724aab875caa0c42573711a19c74b1f74 |
| cold-b-probes-v2-py314.json | Same executable -B -P cold-b-probes-v2.py | 0; 80 observations PASS | d647bb26ca7e1fcea6d0a2d52d97454fe0c424380548fdc6936be5f3665e2906 |
| cold-b-suite-py314.json | Same executable -B -P cold-b-suite.py | 0; 45 tests PASS | d06a02f8ca2f6fbf59fc9566382bb37b7d460b427b0cf779130a07e8e7ea9750 |

All receipt filenames above are under this packet's checks directory. Driver
arguments in each receipt retain the full absolute script path. Final snapshot
status remained clean. Changed blobs are LF-only, BOM-free, and trailing-space
free; git diff --check passed. No sealed kernel/spine changed.

A first probe driver had a missing closing parenthesis and failed to parse before
any payload import. The original cold-b-probes.py and exit-1 receipt
cold-b-probes-py311.json remain retained. It is a reviewer harness error, not a
product failure. The separately named v2 driver corrected only that syntax and
then passed on both interpreters; SHA-256
fbb5910c4d2202cec3175d854f8b5936067ba74723af76ac896d0a942234a0c9.
An exploratory unsanitized shell diff failed to resolve the snapshot as a Git
repository; the scrubbed static driver subsequently produced the verified diff.
No product conclusion relies on that exploratory command.

## Advisory note and limits

Nonblocking formatting note: frozen tests/test_v0a_hand_replay.py:1167 is 101
columns, one beyond the repository's 100-column guidance. Wrapping that assertion
would restore the convention; it does not alter this admission verdict. No source
was edited. No additional design change is recommended for this bounded scope.

Finite ordinary-construction adversarial schedules do not certify arbitrary
private mutation, object forging, class monkeypatching, or unlimited hostile
memory/depth. No trace/schema/writer/publication/C fix or acceptance-replay claim
is assessed. No broad profile, GPU computation, optional dependency installation,
lifecycle owner, ceremonial commit, or release authorization was performed.
