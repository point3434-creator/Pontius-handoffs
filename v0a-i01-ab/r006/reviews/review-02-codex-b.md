# Independent cold review B - v0a-i01-ab/r006

Defect verdict: CLEAN. Specification: PASS. Engineering quality: PASS for the
bounded T-01/T-02 correction. No required correction remains.
Design verdict: SOUND within this scope.
Reviewer: Codex B, independent cold Tier-C pass, 2026-08-30.

## Bound identity and independence

- Candidate: 52bd941e9fa1fb90ff6d2d14df2286e2ee4f4ec8.
- Manifest: 7e1575b18c7a9cf0c74bd956a54e899aad670349d198d7863ae1f67463583d7a.
- Base: 6cdf7b00dac653a9a295bbb86cdc3b5782317491.
- Tree: 8f5e35e5c266d8a8fa4c63e96550a4e9ef894216.
- Frozen ref: refs/heads/review/v0a-i01-ab/r006.

The manifest was independently recomputed from frozen Git blobs using disabled
rename detection and whole-row sorting, and matched manifest.sha256 byte for byte.
Only src/pontius/v0a/trace.py and tests/test_v0a_trace.py differ from the base.
No sealed source or independent accepting checker/oracle changed in this round.

I began with the handoff and permitted inputs. The independent invariant/path
inventory was written before opening coverage.md: checks/codex-b-inventory.md,
SHA256 ecf8bb1bc117d21cd7f1928dbbd8dad76f064d25b2af17beec15fa7133a69658.
Deferred coverage independently hashes to
8316fc9dc13bac5b66142f73ffc992b537f009736bde77694eb9eec7b0a6ee46.
No implementer plan/report/transcript, sibling check, or peer review was read.

## Findings and required outcomes

No material in-scope defect or blocking coverage gap was found. No source change
is requested. Required T-01/T-02 outcomes are supported by these observations:

| Contract | Fresh evidence | Result |
| --- | --- | --- |
| Interrupted/unknown outcomes cannot claim completion, pass or complete accounting | Existing nine-outcome/eight-flag matrix and null-timing unknown control; independent six-outcome/eight-flag matrix | PASS |
| Failed/incomplete settlement is null; failed primary cause survives | Real accepted interruption, rejection, ambiguity, no-start and late controls; independently rebound settlement and primary mutations | PASS |
| Complete accounting has both category totals; incomplete accounting preserves available categories | Existing five-variant totals matrix; independent 40-case totals matrix | PASS |
| Counts, accepted decision/failure pairs, timing, digest and canonical wire contracts remain strict | Full 48-method trace suite and 15 independent count mutations | PASS |
| Honest failed prefixes and source/adapter compounds remain inspectable | Real source/body and prefailed-witness controls; 471 observed A/rejected-input clock schedules; independent 216 B all-in clock schedules | PASS |
| Exact event values and ascending private pair | All common/event-specific constructor negatives; three existing event-value methods; independent complete finite distinct-pair ordering domain | PASS |
| Public card order remains reveal order | Existing width/order positives and six independent unsorted flop permutations | PASS |
| Successful replay remains successful at the separate accepting boundary | Independently supplied source/configuration/policy expectations for real fixture A and side-pot/all-in fixture B | PASS |

The independent checks use real ReplayHost, ActionMailbox, runtime and witness
paths. Fault adapters exercise actual acceptance before losing acknowledgement or
breaking the source; they do not replace the ownership boundary with a helper
shape. Mutation expectations follow ADR0485 and the r005 required outcomes.
Both semantic and prefix digests are calculated with independent json/hashlib code,
without the production projection, digest or terminal-consistency helpers.

A separate untouched base snapshot admitted six invalid categories on both Python
versions: interrupted completion flags, failed settlement, missing complete total,
erased primary, replaced primary, and descending private cards. These expected
base defects establish regression sensitivity; the candidate rejects the same
categories in the focused and independent checks.

## Design assessment and advisory guidance

SOUND: wire admission now reconstructs only four known pure event value types,
with exact raw-key checks and nested HandAction admission. Constructor invariants
provide one source for primitive event domains. Stream position, minimum stack
context and rank comparability remain explicit reader checks. The bounded terminal
helper runs after exact values, counts and accepted-delivery pairs are admitted,
and applies implications independently of the passed flag. This addresses the
schema duplication and success-only placement described in the permitted r005
requirements without replacing the legal checker.

Advisory only: retain the explicit compatibility treatment for earlier source
clock failures. The existing wire cannot determine every hidden source/body order;
first failure-row equality would reject demonstrated honest compound paths. If a
future contract requires trace-only proof of cause chronology, use a separately
versioned ordered cause record with real compound-schedule evidence. That future
change is neither required here nor permission to expand this round.

## Execution receipts

All Python payloads ran from fresh D-local disposable snapshots, never the primary
checkout. Every launch asserted the exact executable/version, -B and -P, snapshot
cwd, snapshot/src PYTHONPATH, and absolute regular/non-reparse Git. Launch
environments were cleared then populated with only SYSTEMROOT, WINDIR, COMSPEC,
TEMP, TMP, PYTHONPATH, PYTHONNOUSERSITE and PONTIUS_GIT. TEMP/TMP stayed in the
snapshot. No Git PATH lookup or global safe.directory setting was used.

Candidate snapshot:
D:/Pontius-review-snapshots/codex-b-v0a-i01-ab-r006-2fddbb63.
Base sensitivity snapshot:
D:/Pontius-review-snapshots/codex-b-v0a-i01-ab-r005-base-c5e378a6.

Actual floor D:/Pontius-tools/py311/Scripts/python.exe, CPython 3.11.15, ran first;
D:/Pontius/.venv/Scripts/python.exe, CPython 3.14.6, ran second for each check class.
The preserved package initialization adds its normal CUDA DLL environment entries
in the 3.14 process after import; both launch environments were scrubbed. No GPU
work, optional-dependency installation or device test was performed.

| Driver under checks/ | Python 3.11.15 | Python 3.14.6 | Receipt prefixes |
| --- | --- | --- | --- |
| codex-b-identity.py | exit 0 | included in later drivers, exit 0 | codex-b-identity-311; focused/adversary/static |
| codex-b-focused.py | 48 trace + 3 event-value methods, zero skips/failures/errors | same | codex-b-focused-311 / 314 |
| codex-b-adversary.py | 3,052 cases, PASS | 3,052 cases, PASS | codex-b-adversary-311 / 314 |
| codex-b-baseline-sensitivity.py | six expected old defects reproduced | same | codex-b-baseline-311 / 314 |
| codex-b-static.py | exit 0 | exit 0 | codex-b-static-311 / 314 |

Each prefix has .json command/environment/exit/time/output-hash receipts and exact
.stdout.txt/.stderr.txt logs. codex-b-run.ps1 and codex-b-baseline-run.ps1 retain
launch construction. The .json receipts contain the complete absolute commands;
all invoke the asserted Python with -B -P and the absolute driver path.

The independent 3,052 cases per interpreter comprise 2 successful legal controls,
6 honest outcome controls, 48 flag combinations, 15 count corruptions, 15 reason/
settlement corruptions, 40 accounting combinations, 2,652 ascending/descending
private-pair cases, 52 duplicate pairs, 6 board permutations, and 216 all-in clock
faults. The latter covers 72 observed B source reads with invalid, reversed and
raised faults and asserts that each source stops at the injected read.

Static checks parsed both changed files, passed git diff --check, confirmed LF/no
BOM/no trailing whitespace, and found all 514 added lines at most 100 columns.
Four existing long source lines and three existing long test lines are byte
identical to the base. The candidate snapshot remained Git-clean after execution.
The unprovided tests/test_v0a_model.py inventory possibility was resolved by the
three actual EventValueContractTests methods in test_v0a_hand_replay.py.

## Coverage comparison and limits

The deferred claim matches the independently recorded category/path inventory.
Its core evidence is public behavior, not merely constructor/helper presence. I
confirmed its explicit boundaries and extended fault coverage to fixture B plus
the finite private-card ordering domain. No broader exhaustive-closure claim is
made: the clock sweeps cover observed paths, not every future callback schedule,
and structurally accepted altered card/board values are not claimed as legal
fixture replays.

Parsing does not prove legal replay, source sealing, measured actual work, terminal
publication, final host receipt success, or trustworthy hidden chronology. The
unchanged legal checker and oracle were used only as preservation controls.
The known premature-script/null-reason ReplayHost producer issue is explicitly
excluded by the handoff and remains separately owned; this verdict does not close
publication/accounting or slice C. No broad suite, lifecycle/capability invocation,
source edit, evidence-repository commit, merge or push was performed.
