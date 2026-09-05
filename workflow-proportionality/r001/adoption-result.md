# Proportionate engineering review: adoption result

Controller disposition, 2026-09-05: ADOPTED and pushed. This is the execution
receipt for the separately authorized ADR-0492 decision, not a new review.

## Exact identities

| Item | Identity |
| --- | --- |
| Decision commit | 7a387e995e3b37232d2379332927247a4d49c64e |
| Required and actual parent | 53773cb9e7489d8cfa32b4e0ceadea37c5980023 |
| Reviewed candidate | 922398389870ba9dc378eb096363de3b1bb3731c |
| Reviewed and committed tree | 68c961452a7adad21beddf85b4e2486b30664769 |
| Candidate manifest SHA-256 | 9c45e5069a7b0e7276e9a1e63e3b809bfc2c696a26c04f32336cb36ac8411589 |
| Prior packet publication | a183ccd01b77e38bc89c4bf75e65da7b40f4ca80 |
| Candidate archive | refs/heads/archive/workflow-proportionality/r001 |

The decision title is "Adopt proportionate engineering review". Its entire tree
equals the reviewed tree, not merely the four copied file hashes. Exactly
CLAUDE.md, docs/workflow.md, docs/decisions/ADR-0492-adopt-proportionate-engineering-review.md
and STATUS.md differ from its parent. All other source, tests, CI, profiles and
dependency blobs remain unchanged.

The controller's "Please do" authorizes the two actions in
../support/authorization-request.md, SHA-256
e2f8c97a4c38b990b836137ebed1c254684776595d557354c48824a146b963b6.
The record is ../support/authorization-record.md. Two completed independent
CLEAN/SOUND cold reviews and their acceptance receipt remain unchanged in this
packet. Earlier delivery failures retain their INCONCLUSIVE disposition and
are not counted as cold passes. No original issuer verdict was rewritten.

## Execution and verification

The candidate archive was pushed to the existing private Pontius origin and its
full remote identity confirmed. The unchanged review packet, reports, logs and
receipts were published as 59 exact staged files in private Pontius-handoffs;
the prior publication commit above was confirmed against remote main before
the primary integration.

Fresh precommit metadata checks passed on CPython 3.11.15 first, then 3.14.6.
The exact decision was then created locally. Four fresh snapshots of that actual
commit were checked before pushing master, with -B -P, scrubbed child environments,
exact interpreter identities and module-source paths verified:

| Slot | STATUS check | Metadata suite |
| --- | --- | --- |
| CPython 3.11.15, first | current, exit 0 | 12 tests, OK, exit 0 |
| CPython 3.14.6, second | current, exit 0 | 12 tests, OK, exit 0 |

All 16 postcommit snapshot-file comparisons matched the frozen four blobs.
The primary decision push was confirmed by querying origin refs/heads/master.
Both repositories' tracked/index states were clean. The normal porcelain
untracked population fingerprint was unchanged before and after integration:
3ad015f8e8f7e2623bca0a4e23411f5c287134aa89bb60531a935226189172c5.
No local or remote ref, snapshot, probe or user-owned file was removed. Git's
auto-push hook was suppressed only by a command-local setting so verification
could precede the explicit push; no persistent Git configuration was changed.

## Retained postcommit receipts

Paths below are relative to adoption-records/; the original bytes are retained.

| Receipt | SHA-256 |
| --- | --- |
| postcommit-status-311.json | fcb249cd8ba3f26e25a06862170c5c30ffd25e56a5f1d6c2719675ba568ef843 |
| postcommit-tests-311.json | d1e170413f611676e15bc38fe7ff38659971056a2c76e5f2093868aea5eca70c |
| postcommit-status-314.json | 40658454b1bac4f01844ab0f5f5026ae693a9dd9a33a54895e9c3095c4f36459 |
| postcommit-tests-314.json | d4efa4276a2a26cff78c21704450c60935e402825676308c7a63c69867c6d5be |
| integration-result.json | 83919bfd9b332570e8ca1adc439fa6409b9e4481a25c76bf259e8693de4ddca2 |

## Effect and limits

The three amendments now apply prospectively: qualified mechanical correction
verification, controlled failure schedules with independent outcomes, and
review tiers selected by the highest changed contract risk. Stronger task
requirements and explicit per-commit authority still bind. This amendment itself
completed the preceding protocol; it did not apply its own lighter route.

The metadata suite verifies metadata, not future human or model judgment. No
runtime, test, analyzer, CI, profile or dependency byte changed. No source task,
experiment, rehearsal, operating gate, research gate or consumed-owner invocation
was opened. The next bounded source task remains to be separately selected.
