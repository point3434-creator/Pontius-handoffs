# Cold A review — v0a-i01-ab/r004

Reviewer: Codex cold A, 2026-08-30. Tier C, independent FIX review.

- Candidate: `c6adbcaa048988361d2388970eaca772711b797b`
- Ref: `refs/heads/review/v0a-i01-ab/r004`
- Base: `30df7bce8da51715e6f1d7576892dd689421c516`
- Tree: `1b6edef1e943483e0a83ec33f1bcc61348ada166`
- Manifest SHA-256: `a810c89b7342fb1bcb4f1498fdcf53cd11a589b70424c7da48f6619a45da67cb`

## Required findings and verdict

**CLEAN for V-01/V-02/V-03. No required behavioral correction remains in this scope.**
Specification verdict: PASS. Engineering-quality verdict: PASS for the bounded admission change,
with the nonblocking formatting advice below. This is one cold pass, not the Tier-C aggregate,
broad-suite authorization, release acceptance, source seal, or commit authority.

No Critical or Important finding was demonstrated. All invalid inputs tested through real
dispatch/mailbox boundaries were refused without the prohibited effects. Genuine delivery followed
by invalid acknowledgement remained unknown and was never retried.

## Required design verdict

**SOUND.** A closed exact-type graph is rebuilt at each actual ingress before it is consumed.
This prevents an ordinary subclass from transferring its methods or skipped constructor checks
into the runtime-owned values. The four dispatch paths share one admission point inside the
measured transition. Mailbox validation and receipt preparation precede insertion; acknowledgement
validation precedes identity equality. State-dependent showdown admission checks live-seat presence
and a homogeneous comparable rank domain before terminal advancement/completion.

This is a bounded repair of the demonstrated trust-boundary mechanism. It does not rewrite or
modify sealed kernels/spine. The permitted evidence does not justify a redesign.

## Independence and identity

The initial inventory was written before opening coverage.md:
`checks/cold-a-inventory.md`, SHA-256
`f0cdf3c7b8cb0af8495586ae15ccc94582c04c44b015be04502f05d68569cefb`.
Inputs were the handoff/identity, current CLAUDE.md and workflow, frozen source/tests,
ADR-0485, ADR-0484 and brief, and the required outcomes in
value-boundaries/r001/disposition.md. No implementer plan, transcript, self-report, or current
peer report was read.

The coverage file hash independently matched
`1a6b52be5295fdcca59b9c112dea56210945ec6c6cb919833f9c57a076adae58`.
Its seven-record discovery matches the independently traced four event ingresses, nested
HandAction, ActionEnvelope, and DeliveryReceipt. The claim's immutable ranks, live masks,
mixed rank domains, safe metadata, poisoned-key controls, and real forwarded acknowledgements
were exercised independently. Its finite-input limitation is appropriate; this report does
not claim arbitrary Python object forging or monkeypatch resistance. I did not independently
rerun the coverage file's historical RED command or adopt its numerical claims as evidence.

Both final runs recomputed the manifest from `git cat-file blob <commit>:<path>`, using
whole-row sorting and LF rows, and compared the exact result with manifest.sha256. Candidate,
parent, and tree also matched. Only model.py, runtime.py, and test_v0a_hand_replay.py differ.
The clone's three checked-out files were additionally byte-equal to those blobs.

## Requirement-to-evidence map

| Contract | Fresh real-boundary evidence | Result |
| --- | --- | --- |
| V-01 complete event admission | All four event variants: ordinary skipped-validator subclasses, wrong schema, bool/float index aliases, mutable identifier; exact outer opponent event with six nested action variants | Typed invalid_event, unchanged public betting state and mailbox, no completion; unadmitted event index null |
| V-01 showdown completion | Actual legal showdown, mutable/empty vectors, invalid tuple members, mixed int/tuple ranks, missing live ranks and extra folded ranks | Invalid ranks refused before terminal advancement/completion; settlement unavailable after rejection |
| V-01 valid rank preservation | Six controls: int and tuple ranks with six live seats, folded seats, and preflop all-ins | Expected payouts 12 chips or 4 chips to seat 2; repeated settlement identical |
| V-01 metadata and timing | Hostile attribute access on fresh/dead/complete/clock-first branches; invalid input then genuine abort-boundary clock fault | No unadmitted attribute access; null metadata; first cause invalid_event then clock_invalid in occurrence order |
| V-02 atomic mailbox admission | Ten malformed envelope variants and exact outer envelope with invalid nested action; valid same-key delivery follows every refusal | Empty mailbox after refusal; valid integer key accepted once; duplicate refused; public accepted copy does not alter mailbox |
| V-03 receipt exactness | Eight genuine forward-then-invalid-ack schedules, including bool/float aliases, subclass, wrong exact ID/index, missing and hostile acknowledgement | One attempted/actual delivery, zero acknowledged count, delivery_ambiguous/unknown, null claimed delivered action; subsequent dispatch does not retry |
| Known delivery preservation | Genuine forwarding with exact valid receipt, including clock failure immediately after acceptance | Known count one, actual delivery retained; post-acceptance clock failure retains decision/action with accepted status |
| Existing behavior | All four frozen focused v0a suites, including policy authority/refusal, clock/cause, side-pot/all-in and settlement comparisons | 137 tests passed per interpreter |

Relevant implementation locations: model.py:305-361; runtime.py:493-540, 703-744,
1020-1054, and 1130-1178. Those spans are frozen-candidate references.

The independent probe suite contains 67 unittest cases per interpreter. Its 67 cases and the
137 existing tests overlap intentionally and are not 204 unique contract categories. Source
inspection establishes the admission ordering; the probes establish observable outcomes.

## Execution evidence

Fresh disposable clone:
`D:/Pontius-review-snapshots/v0a-i01-ab-r004-cold-a`.
Created from local repository with `clone --no-checkout --no-hardlinks --local`, then detached
at the candidate with `core.autocrlf=false`. No mutable working bytes were overlaid.

Final commands, executed in this order:

```text
D:/Pontius-tools/py311/Scripts/python.exe -B -P D:/Pontius-handoffs/v0a-i01-ab/r004/checks/cold-a-runner-v3.py 3.11.15 311-v3
D:/Pontius/.venv/Scripts/python.exe -B -P D:/Pontius-handoffs/v0a-i01-ab/r004/checks/cold-a-runner-v3.py 3.14.6 314-v3
```

Both exit 0: 137 existing focused tests + 67 independent probes, no failure/error/skip.
Actual executable, CPython full version, flags and environment were asserted/printed before
payload import. Cwd was the clone; PYTHONPATH was exactly its src directory. The child environment
was cleared and populated only with SYSTEMROOT, WINDIR, TEMP, TMP, PYTHONPATH, PONTIUS_GIT,
PYTHONDONTWRITEBYTECODE and PYTHONNOUSERSITE. Temporary test output was D-local outside the clone.
PONTIUS_GIT was the regular non-reparse absolute `C:/Program Files/Git/cmd/git.exe`;
Git used a command-scoped safe.directory for the clone, never PATH lookup or global configuration.
Imported pontius module origins were asserted inside clone/src. No CuPy or Torch module loaded.

Final git status was clean before and after both runs. Fresh `git diff --check <base> <candidate>`
also exited 0. The three changed blobs are LF-only and BOM-free.

Authoritative receipts:

| File | SHA-256 |
| --- | --- |
| checks/cold-a-311-v3-receipt.json | 3d73140edd88f93d6e693666f892fdd0109ce290b8dbb0ef894ac741b6fdc54d |
| checks/cold-a-314-v3-receipt.json | deb7199235156825c8ca9b25e452e7b5a6bd9d97d12ac5d61a8fbea8f2038aa3 |
| checks/cold-a-probes-v2.py | e5e9dcc3a857dd765d4650c9a088bb47750088c37720d42b32bcce3b048aacb2 |
| checks/cold-a-runner-v3.py | 1cc173a9d3d806256be66f2905bb216173d0dd23023bc34ff4802c2bb022ed3b |

Preserved diagnostics are not hidden retries: the initial 3.11 runner verified identity/manifest
but stopped before test execution on my erroneous NumPy exclusion. NumPy is a CPU dependency;
runner v2 removed only that exclusion. Its 137 existing tests passed; 66/67 independent probes
passed. The one failed probe scheduled clock read 2, which source tracing shows belongs to
start_transition_boundary, so the observed clock_invalid priority was correct. Probe v2 schedules
read 3 and records/asserts the actual abort_transition_boundary stack. Both final runs confirm
invalid_event followed by clock_invalid. Earlier scripts, logs and the v2 receipt remain retained;
these two reviewer-harness errors are not candidate defects.

## Advisory guidance and limits

- Preserve the closed record whitelist and expand the real-ingress matrix when an input variant
  changes. Do not replace it with dynamically calling a caller object's __post_init__.
- Minor formatting advice: test_v0a_hand_replay.py:1167 is 101 columns, one column beyond the
  workflow guideline. Wrapping that assertion is a nonblocking hygiene improvement, not a
  V-01/V-02/V-03 behavioral residual.

No production source, frozen test, sealed kernel, policy authority, or existing packet input was
edited. No broad/GPU suite, dependency installation, experiment owner, source seal, integration,
commit, push, or publication occurred. Existing trace/replay tests ran only as focused preservation
controls; this review does not certify trace/publication/accounting or the separate C surface,
and counts no finding in those surfaces as a residual of this value-only FIX round.
