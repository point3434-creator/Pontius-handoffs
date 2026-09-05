# Independent Tier C implementation review A

Reviewer: Codex review A (fresh context)

Candidate: `refs/heads/review/v0a-blueprint-artifact-impl/r001`

Commit: `6fb7f840d31d946e6b5dcb45faf82939dafd46ec`

Base: `c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98`

Tree: `6f8e17c12da42ad901c90bc764fc39958cca5854`

Manifest SHA-256: `26b8fb178aecaf3dccf038ee2e108dc4ce913f7f07baff10cff5efbe11011aee`

## Verdict

- Specification: **FAIL**
- Engineering quality: **FAIL**
- Findings (Critical / Important / Minor): **0 / 2 / 0**
- Defect verdict: **REQUIRED CORRECTIONS**
- Design verdict: **SOUND**. The codec's shared closed-schema admission path,
  exact-value reconstruction, and deterministic full-key encoding fit the
  adopted contract. The two findings are bounded gate/test defects rather than
  evidence that the codec boundary needs redesign.

## Findings

### Important 1 — The public source gate admits an undeclared colliding module

Severity: Important. Confidence: High; reproduced through the real public gate.

Locations: `tools/check_stabilization_boundaries.py:57`, `:172`, `:213`, and
`:226`; missing negative coverage in
`tests/test_blueprint_artifact_boundary.py:66`.

The adopted source opening permits exactly
`src/pontius/blueprint_artifact/__init__.py` and
`src/pontius/blueprint_artifact/codec.py`, and requires other origins in that
family to be rejected. `enforce_origin_classification` checks only paths below
`src/pontius/blueprint_artifact/`. It therefore does not classify the sibling
top-level path `src/pontius/blueprint_artifact.py`. At the graph layer,
`enforce_legacy_edges` explicitly treats the resulting module name
`pontius.blueprint_artifact` as classified, and the import-policy function also
treats that name as in-family.

Concrete state and wrong outcome: starting from the frozen candidate, the
review probe created
`src/pontius/blueprint_artifact.py` containing only a docstring and called
`CHECKER.check_repository(snapshot_root)`. The call returned normally. Receipt
`run-records/review-a-gate-collision-311.json` records CPython 3.11.15,
`-B -P`, the frozen packet overlay, exit 0, and:

```text
DEFECT REPRODUCED: public gate accepted undeclared src/pontius/blueprint_artifact.py
```

This is not only a theoretical namespace oddity: the public gate fails its
minimal exact-population promise, so an unapproved source file at the family
import name can cross the registration boundary without review.

Required correction: make the public gate reject every source path representing
the blueprint-artifact family unless it is one of the two exact authorized
paths, including the colliding top-level module, and add a real-public-gate
negative for this exact path. Verification must run the corrected negative
through `check_repository`, not only through an in-memory helper.

Engineering guidance (advisory): derive the permitted module/path pairs from
the exact path constant and reject any family-like module name whose path does
not match that mapping. This prevents path-spelling aliases from falling
between the path classifier and graph classifier.

### Important 2 — The registered codec tests do not implement the adopted independent acceptance map

Severity: Important. Confidence: High; directly established by the complete
225-line test source and focused reviewer probes.

Locations: `tests/test_blueprint_artifact.py:65-86`, `:87-124`, and `:126-150`.

The adopted design requires a field-exhaustive independent expected source for
the nonempty-history/postflop case, every action label through the artifact
action boundary, missing and unknown members at every object level, and numeric
closure for the nested key/history/action integer families through both public
operations. The registered suite does not supply those controls:

- The raise fixture is compared to a separately constructed full source, but it
  has empty history. The history fixture is checked only for source ID,
  street/board, the four history-kind strings, and the last row's suffix. Its
  complete 17-field key, full history rows, and entry action are not compared to
  a separately constructed expected source.
- Only the `raise` entry action is independently asserted. `fold` and `check`
  appear in a permutation/self-consistency path without an independent action
  oracle, and `call` is never decoded as an entry action (the runtime miss's
  passive call does not exercise `_action`).
- Root, entry, and key object membership receive examples, but the action object
  has no missing-member or unknown-member control. A bad action label and a
  duplicate member are different schema failures and do not cover these cases.
- The 640-digit boundary is tested only through `last_full_raise_size`; the
  registered suite has no corresponding key-vector, history-record, or action
  integer-family controls, and no independently constructed accepted exact graph
  at the upper boundary. The over-bound exact-source case also covers only that
  one key scalar.

Directly demonstrated missing acceptance contract: review probe
`probe_codec_edges.py` had to add the absent action-object membership cases,
independently assert all four entry actions, exercise history nullable/label
failures, and traverse upper and over-limit values in a key vector, history
record, action, and independently constructed exact source. Its corrected
minimum-digit snapshot run passed, which is useful evidence that the current
implementation handles these samples; it does not turn unregistered reviewer
code into the durable, independently-oracled acceptance suite required by the
adopted design.

Concrete regression exposure: a future change that maps a decoded `call` entry
to another non-raise action, admits an action object with an extra member, or
drops the integer ceiling from history/action fields can leave every current
registered assertion green. Those are explicit schema and identity contracts,
not advisory coverage preferences.

Required correction: within the existing 300-line combined test budget, add
durable independent controls for the complete history fixture graph and action,
all four entry-action labels, action-object missing/unknown members, and the
key-vector/history/action numeric families at and immediately beyond the bound
through decode and exact-source encode. Expected values must be stated
independently rather than inferred through round-trip or entry-order equality.
Consolidating tables/helpers is an implementation choice, not an additional
acceptance requirement.

## Strengths

- Frozen-source inspection found a coherent single admission pipeline for both
  public operations. Exact outer records, tuples, enum values, strings,
  integers, booleans, nullable fields, card constraints, semantic duplicate
  keys, and existing constructors are applied before a source or bytes result is
  returned.
- Deterministic encoding sorts by full key canonical bytes, emits sorted compact
  ASCII JSON plus one LF, and preserves the separate unchanged policy digest.
- The real `HandRuntime` hit/miss/illegal-hit assertions and complete
  `ReplayHost` settlement/independent-reader assertion use production paths,
  not a policy helper double. The expected payout and final stacks are stated
  independently.
- Numeric and Unicode handling is symmetric in the implementation; the codec
  does not alter the process-wide integer setting and has no former one-MiB
  capacity cap. The corrected reviewer edge probe passed under the minimum
  decimal setting.
- The driver allowance is origin-specific and limited to the three authorized
  internal targets. Generated registration adds exactly the two codec suites and
  unchanged 12-test driver suite. Existing payloads are unchanged and the
  capability-binding digest remains all zeroes.
- Scope and numeric budgets are respected: 12 approved changed paths, 281/300
  source lines, 299/300 new test lines, 1,699/8,192 fixture bytes, and 96/100
  manual registration added-plus-removed lines.

## Requirement-to-evidence map

| Requirement or risk | Best evidence reviewed | Result |
| --- | --- | --- |
| Frozen commit/tree/blob/manifest identity | Independent Git-object recomputation of all 12 rows and packet copies | PASS |
| Exact opened paths and registration delta | Frozen diff, base blob pins, structural generated-output comparison, real gate falsifier | **FAIL**: colliding top-level module admitted |
| Complete closed JSON/exact-object graph | Full codec source inspection, registered suite, focused edge probe | Behavior sampled PASS; **acceptance contract FAIL** |
| Canonical bytes and policy identity | Literal canonical raise fixture, full-source comparison, source inspection, four-slot suite | PASS for exercised cases |
| Runtime hit, miss, illegal hit/no delivery | Real `HandRuntime` registered test; four-slot suite | PASS |
| Complete replay and independent expected reader | Real `ReplayHost`, settlement values, `verify_successful_trace` with separately constructed policy | PASS |
| Numeric/Unicode closure and no artificial byte cap | Four-slot normal/minimum-digit suite plus corrected nested edge probe | PASS for observed behavior; durable numeric-family coverage incomplete |
| Real public boundary positives/negatives | Existing two-slot boundary receipts plus fresh colliding-path probe | **FAIL** |
| Driver registration and zero grants | Structural inventory/TOML comparison and two-slot writer-check receipts | PASS; no analyzer-soundness claim |
| Budgets and hygiene | Frozen numstat, direct file counts, fixture sizes, `git diff --check` | PASS |

## Exact checks and evidence

Reviewer-executed checks:

1. `python -B -P reviews/a/verify_identity.py` — exit 0. Recomputed the ref,
   parent, tree, all 12 raw frozen blob SHA-256 values, digest-first sorted
   manifest bytes/digest, and equality of every packet blob copy. Both amendment
   authorization SHA-256 values also matched their handoff pins.
2. `python -B -P reviews/a/inspect_generated.py` — exit 0. All 2,828 prior
   inventory rows and all 422 prior payloads remained structurally identical;
   additions were exactly 7 codec + 4 boundary + 12 unchanged driver tests and
   three current payloads. The three test paths were the only stabilization-list
   additions; added payloads had no probes or environment additions; the
   capability digest was 64 zeroes.
3. `run-snapshot.ps1 -RunName review-a-gate-collision -Slot 311 -Overlay
   packets/r001/files ...probe_gate_collision.py` — identity check exit 0,
   probe exit 0, defect reproduced as described in Important 1.
4. `run-snapshot.ps1 -RunName review-a-codec-edges -Slot 311 -Overlay
   packets/r001/files -MinimumDigits ...probe_codec_edges.py` — identity check
   exit 0; initial probe exit 1. Classification: reviewer-probe defect, not a
   candidate defect. The probe attempted to `json.dumps(10**640)` under the
   640-digit limit. The receipt is retained.
5. Corrected `review-a-codec-edges-r002` command with the over-limit token
   injected as raw bytes — identity check and probe both exit 0 under CPython
   3.11.15, `-B -P -X int_max_str_digits=640`.
6. `git diff --check <base> <commit>` — exit 0. All six authorized base Git blob
   pins matched. Frozen numstat gave 96 manual registration lines; direct frozen
   packet counts gave the source/test/fixture budgets above.

Fresh controller-owned frozen-blob checks independently checked from their raw
receipts:

- `frozen-codec-normal-311.json`: 7/7, exit 0.
- `frozen-codec-min-311.json`: 7/7, exit 0, startup minimum 640.
- `frozen-codec-normal-314.json`: 7/7, exit 0.
- `frozen-codec-min-314.json`: 7/7, exit 0, startup minimum 640.

Permitted implementation receipts checked structurally, without treating names
as verdicts: the final boundary suite ran 4/4 with exit 0 on 3.11 and 3.14, and
the generated writer `--check` exited 0 on both slots. Those green results do
not cover the colliding path or the missing acceptance cases above.

## Limitations and deliberately unverified claims

- The broad post-CLEAN acceptance union was correctly not run. This review is
  not CLEAN, so this report does not infer broad acceptance.
- The parked capability analyzer was not executed or judged sound. Registration
  and a zero capability digest are not a safety proof or invocation grant.
- No operating, rehearsal, scientific, optional-dependency, network, or
  subprocess-owner path was run. No policy-strength, performance, capacity, or
  arbitrary-resource guarantee is claimed.
- The focused reviewer edge probe was run only on the supported floor; the
  controller's full registered codec suite supplies both-slot evidence, while
  the reproduced path-classification defect is interpreter-independent source
  logic.
- No candidate source, tests, index, refs, working tree, generated output,
  retained artifact, commit, or remote state was changed. Reviewer probe/report
  files are confined to `packets/r001/reviews/a`; transient gate mutations were
  confined to disposable snapshots and removed by the probe.
