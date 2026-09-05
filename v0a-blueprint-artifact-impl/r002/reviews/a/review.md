# Independent Tier C FIX review A — portable blueprint artifact r002

Reviewer: Codex review A, fresh independent FIX review

Candidate: `refs/heads/review/v0a-blueprint-artifact-impl/r002`

Commit: `5e56e4454f7b8ccb360d3e36245abc33318349bb`

Base: `c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98`

Tree: `dc18ed133504fe6c7677b494bcefba311cc73704`

Manifest SHA-256: `6d5e14a64466f8aaa874d4bdf62ada439703eb74911a7b4dc4445c14b2af13b5`

Rejected r001 commit: `6fb7f840d31d946e6b5dcb45faf82939dafd46ec`

## Verdict

- Specification: **PASS**
- Engineering quality: **PASS**
- Findings (Critical / Important / Minor): **0 / 0 / 0**
- Defect verdict: **CLEAN**
- Design verdict: **SOUND**. The bounded correction preserves the small shared
  admission traversal and exact public source gate. Local checked slot reads and
  one missing family-path predicate close the demonstrated defects without
  broad exception handling, schema duplication, runtime coupling, or analyzer
  expansion. The consolidated acceptance suite remains contract-oriented and
  fits the adopted fixed budget.

No required correction survives verification.

## Binding correction requirements and disposition

### Prior A Important 1 / B B02 — undeclared flat family module: CLOSED

The frozen checker now treats `src/pontius/blueprint_artifact.py` as an
unclassified family origin in addition to checking descendants of
`src/pontius/blueprint_artifact/`. The change is one exact predicate; the two
approved package paths remain unchanged. It does not widen the family exemption
or alter graph/SCC/analyzer behavior.

The registered negative physically adds the flat module in a disposable
snapshot and invokes `CHECKER.check_repository(ROOT)`. My fresh floor boundary
run passed all four tests through that public gate. The same test also retained
the real-gate negatives for an unlisted package descendant, a forbidden codec
import, and a legacy source importing the codec. Driver positives and negatives
remain part of the same public suite. The standalone checker also passed on the
unmodified frozen r002 snapshot.

Regression sensitivity is direct: permitted old-production receipt
`correction-boundary-red-r001-311.json` (SHA-256
`849b3cba459a475dfdb77a38cec79c9e0837fe3cbf4f35d7baf0d212dc8680f4`)
runs the expanded test against r001 and fails because `check_repository` does
not raise for the flat path. This is a behavioral RED, not a filename claim.

### Prior B B01 — missing exact-record slots escape typed refusal: CLOSED

After every exact-class check, source, entry, key, and action field reads now go
through `_slot`. It catches only `AttributeError` and raises a fixed,
path-qualified `BlueprintArtifactError`. Foreign subclasses are still rejected
before traversal, and the codec does not catch `BaseException` or interpolate an
untrusted value.

The registered suite covers an uninitialized exact source; a valid entry followed
by an uninitialized exact entry; and entries containing uninitialized exact key
and action records, while retaining malformed populated graphs and the foreign
hook trap. My minimum-digit public encoder probe independently confirmed all four
typed paths and their useful locations (`source.source_id`, `entries[1].key`,
`entries[0].key.street`, and `entries[0].action.kind`) and confirmed the foreign
hook remained untouched.

Regression sensitivity is direct: permitted old-production receipt
`correction-codec-red-r001-311.json` (SHA-256
`623d90c80188f5ecba7fa81826393965e939a0cc0db1fbffd90f865d234d45bb`)
runs the expanded registered suite against r001 and records the leaked
`AttributeError`. The same frozen r002 suite passes.

### Prior A Important 2 — missing durable independent acceptance: CLOSED

The complete history fixture now compares to a separately constructed exact
source containing all 17 key fields, all four complete eight-field history rows,
the astral source ID, and the CHECK entry action. A separate table decodes each
artifact action label (`fold`, `check`, `call`, `raise`) and compares it with an
independently constructed `BettingAction`. Action objects now have both missing-
member and unknown-member negatives.

Four independently constructed numeric route families cover a key scalar, key
vector member, history chip field, and action amount. Each uses independently
authored raw max/overflow tokens, compares decoded output with an exact expected
graph at `10**640 - 1`, traverses policy digest plus encode/decode closure, and
requires typed exporter refusal at `10**640`. Both longer raw-token spellings are
refused. This is durable registered coverage, not a reviewer-only probe.

The consolidation preserved the earlier full-key raise fixture and literal
canonical-byte oracle, semantic duplicate-key check, empty policy, malformed and
closed-schema families, Unicode/surrogate controls, above-former-one-MiB control,
file-byte portability, actual runtime hit/miss/illegal-hit behavior, complete
replay and independent reader. The removed `subTest` wrappers and formatting do
not remove executions or observable assertions; the Ellipsis deletion sentinel
is private test data and cannot collide with parsed JSON values; the class-default
test clock becomes an instance attribute on its first increment and preserves a
fresh starting value per instance.

## Independent FIX coverage assessment

The deferred claim's three categories agree with the inventory I recorded before
opening it (inventory SHA-256
`db5cded1a48aef15a5223e8ff878edbe74191eedfae6748271d96a692363585d`):

1. **Source-family exactness.** Discovery reaches both path spellings that map
   to the family, all package descendants, outgoing codec imports, incoming
   legacy imports, and the separately authorized driver origin/three edges.
2. **Typed exact-graph admission.** Discovery follows each fixed record level
   traversed by encode, distinguishes exact-but-incomplete records from foreign
   subclasses, and preserves hook avoidance and valid-first/bad-second behavior.
3. **Durable independent acceptance.** Discovery maps the adopted history/action
   and numeric families to registered public checks, while retaining the original
   runtime, replay, reader, malformed-input, Unicode, and no-byte-ceiling controls.

The related frozen definitions in `immutable_blueprint.py`,
`no_limit_betting.py`, `holdem_cards.py`, the runtime/replay/trace consumer path,
the dependency scanner, driver, and inventory/profile registrations do not expose
another member of these three correction categories. The claim correctly calls
the numeric cases representatives rather than exhaustive enumeration; shared
exact validators and source inspection support that bounded category choice.

The stated falsifiers were materially exercised: the unapproved flat family path
is refused by the real gate; missing exact slots become the common typed error;
the callback trap stays untouched; the independent history/action/numeric controls
are registered and pass; and comparison with r001 plus full source inspection
found no lost binding assertion. The exclusions for races, arbitrary resource
safety, installed-module mutation, strategy quality, and analyzer soundness are
honest and consistent with the adopted scope.

## Requirement-to-evidence map

| Requirement or risk | Fresh or primary evidence | Result |
| --- | --- | --- |
| Frozen ref, parent, tree, 12 blob rows, packet copies and manifest convention | `verify_metadata.py` recomputed Git objects, raw blob SHA-256 rows, whole-row lexical manifest bytes, packet equality and both amendment digests | PASS |
| Exact base-relative and FIX scope | Git diff: 12 authorized base paths; r001→r002 exactly codec, two codec tests, boundary checker; no driver/runtime/analyzer/fixture/generated/CI correction | PASS |
| API, closed schema, exact graph and typed whole-object refusal | Frozen codec inspection; fresh 7/7 codec runs; missing-slot/hook public probe | PASS for specified contract and exercised boundaries |
| Independent full keys, actions, canonical bytes and policy identity | Literal raise bytes/full expected source; complete independent history source; four independent action oracles; digest closure | PASS |
| Symmetric numeric and Unicode closure, no former byte cap | Fresh CPython 3.11 normal/min640 and 3.14 min640 codec suites; reviewer min640 probe; source inspection of pre-conversion/pre-format checks | PASS for declared finite controls; no capacity claim |
| Actual runtime hit/miss/illegal hit and no delivery | Registered `HandRuntime` test in each fresh codec run | PASS |
| Complete hand and independent reader | Registered `ReplayHost.run` plus payout/final-stack assertions and `verify_successful_trace` against separately built policy | PASS |
| Exact public source boundary and driver three-edge amendment | Fresh real-gate boundary suite 4/4 and standalone checker; frozen diff/import inspection | PASS |
| Registration, stable prior rows, current-only additions and zero grants | Fresh structural metadata audit; focused inventory 2/2; writer `--check`; generated JSON/TOML comparison | PASS |
| CI and full acceptance preservation | Frozen diff adds only two direct CPU codec steps; no driver step/hard-gate removal; test-source comparison maps all adopted controls | PASS |
| Budgets and exactness hygiene | Frozen bytes: source 290, tests 300, fixtures 1699 bytes, manual registration delta 97, maximum added Python width 99; LF/no BOM/no trailing whitespace; diff check | PASS |

## Fresh reviewer checks

Every test/probe below used the inspected `run-snapshot.ps1`, the exact r002
packet overlay, a fresh D-local snapshot, scrubbed child environment, absolute
`PONTIUS_GIT`, snapshot-root working directory and imports, and `-B -P`.

| Run / command | Result | Receipt SHA-256 |
| --- | --- | --- |
| CPython 3.11.15 codec suite, normal | 7/7 PASS, exit 0 | `ce6f6c5f6a1fc1d7c40af3f9bd3b96da6f3c643024ad77e4aa4a259fc7cd7ed4` |
| CPython 3.11.15 codec suite, `-X int_max_str_digits=640` | 7/7 PASS, exit 0 | `aff7d675a938726b2e0c49c534b0c9f55ae1d13f687a9374f0609cad4c1d21f8` |
| CPython 3.11.15 boundary suite | 4/4 PASS through real public gate, exit 0 | `c47bae6dc356502729867d471fa10f8e0a98dc730f458e1059d9a037ab2a1aa4` |
| CPython 3.11.15 standalone boundary checker | PASS, exit 0 | `f86d1b05af8a1e0e2ac47c2883a78f1447b05e7b6b08016ee499dbe5471b02d9` |
| CPython 3.11.15 two focused inventory/census methods | 2/2 PASS, exit 0 | `d734d8825e5f4e1ffed4784970af4f59b4bb2cdabaf886405f46a3d0ac4096ae` |
| CPython 3.11.15 unchanged inventory writer `--check` | PASS, exit 0 | `977856226b1a7af0edbbc2fdd42f0c839a0e86d62889b3a87bc9f76700d796f6` |
| CPython 3.11.15 min640 reviewer contract probe | Missing source/entry/key/action slots typed; hook untouched; over-limit action refused; astral digest closure preserved, exit 0 | `25521ec1c9bf52e43c1806dcba64817b1e9fc1cd3832ae687a57ff78366c739c` |
| CPython 3.14.6 codec suite, min640, exact escalated native slot | 7/7 PASS, exit 0 | `9de5ee7fc02095974053c9f393ae25b561220c97aa0f87a557f092848034abfd` |

`verify_metadata.py` (SHA-256
`a9a76aa4ed4d06b93e8a936a54101ae0a410cb33cf1202aba21a14a7ba2ac891`)
also exited 0 and reported: identity/manifest PASS, 12-path candidate and
four-path FIX scope PASS, all four numerical budgets PASS, 23 additions exactly
7 codec + 4 boundary + 12 unchanged driver tests, all 2,828 prior inventory rows
unchanged, three current payloads only, and zero capability grants.

The final reviewer contract probe SHA-256 is
`4d77671fc423a105e13c47f4c80472b63e9240c0c234a6116fed8c05e53fa4b7`.

## Failures classified and evidence limitations

- The first unprivileged 3.14 snapshot launch failed before importing candidate
  code with process exit 101, `Access is denied` (receipt SHA-256
  `48baf098c8939129a973cb539cc02649580c2c2360bb93f8cbcea4e886387048`).
  This is an environment limitation. The exact native-slot rerun with permitted
  escalation passed 7/7; there was no retry-until-green candidate change.
- Two preliminary direct metadata-probe executions stopped on reviewer-script
  assumptions: one measured historical lines instead of added Python lines; one
  expected capability boolean keys not present in the profile schema. I corrected
  only the reviewer-owned script, reran it, and obtained the final exit-0 result
  above. Neither failure executed or diagnosed candidate behavior.
- The controller's `provenance-clarification.md` says the earlier boundary GREEN
  snapshots matched 11/12 r002 files, with only the unexecuted codec test file
  differing. I do not infer whole-snapshot identity from those receipts. My fresh
  boundary run used the complete frozen r002 overlay; my fresh codec runs used the
  complete overlay; metadata independently matched all twelve packet blobs.
- Existing 3.14 boundary, focused inventory, and writer-check receipts were
  inspected as implementation evidence, but not duplicated for ceremony after
  fresh floor public-boundary/registration checks and a fresh full 3.14 min640
  codec run. The boundary correction is path logic, not interpreter-specific.
- Finite tests and source inspection do not prove all representable policies,
  hostile resource exhaustion, capacity, filesystem race safety, policy quality,
  analyzer soundness, or arbitrary installed-module mutation. No such claim is
  part of this verdict.
- The post-CLEAN broad acceptance union remains unexecuted by design and is not
  claimed here. No operating/rehearsal/scientific run, dependency installation,
  source edit, primary/authoring payload, index/ref write, commit, push, grant,
  publication, source seal, or cleanup was performed. Only reviewer-owned files
  and snapshot-run outputs were created.

This verdict is a bounded technical review of the frozen local candidate. It is
not publication, adoption, source sealing, commit authority, or operating
authority.
