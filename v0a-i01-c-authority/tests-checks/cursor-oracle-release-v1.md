# Cursor oracle release v1

Authoring complete; execution and implementation verification remain pending.
No prototype implementation was read and no Python syntax/import/payload check
was run. Only the authorized new T artifacts were written. W, production tests,
generated outputs and all previously issued artifacts remain untouched.

The separately issued pre-implementation case specification is
cursor-oracle-spec-v1.md SHA256
29c0238aa24e0c6d4a9f3834d6f94b46c4bd6ed29f263f0c57511e1ee1b0bfd1.
Its 16 schedules/28 runs are bound by cursor-oracle-cases-v1.json SHA256
ecddd020ffb2a0d85e624aeb7fb544f631b302839f9a5f3542c998b36c37ac61.
The executable is cursor-oracle-v1.py SHA256
15a4741e2532a755fd45f01d4d999dd5d293846b8ae4e9d4e7abedf84c0a8d1e.

Root and the implementation author received the frozen specification/case hashes
before implementation was opened. This executable release followed specification
issuance; it does not assert that executable bytes predated implementation work.
No mutable filesystem timestamp is used as authorization or execution evidence.

The independent design challenge is qualified support for the bounded prototype:
publication ownership, newest-effective pending metadata, exact legacy order,
complete tombstone compaction and operation-level failure staging are necessary.
An internal successful seal followed by a later failing allocation remains a
failed public transaction and must not change retry/continuation costs.

The entrypoint is verify_cursor(api, case_path=CASE_PATH). It has no autorun and
does not invoke or replace the old oracle. It prints per-run cursor_oracle_case
records, failure records with partial costs, and a strict final summary containing
all_completed, failures, planned_cases=16, planned_runs=28, completed_runs,
case_pack_sha256, runtime, hash_seed and maximum_meter_limit=262144. A failed
mechanism stops the remaining cursor schedules in that child and the entrypoint
raises after the summary. The coordinator control must still validate both old
and new summaries and preserve its process/timeout evidence.

The original storage-oracle-v2.py is unchanged at
6a58ef82832d53510f7d44d58cf5a8fa3764f8be5f2c28dcb7e555a83c72cfba,
and storage-oracle-cases-v2.json is unchanged at
3bd5678da334fb551c2f179906e8b4d2cf7a0b0e7a3779e0fad2fb4b4a9c548f.
They retain 28 schedules/34 runs. Combined children therefore plan 44 schedules
and 62 runs, or 372 runs across the six requested runtime/seed slots. The new
343 expanded ordinary schedule operations exclude initial entry setters,
repeated read calls, retention/fault helpers and final historical audits; they
are not a claim about the total public primitive call count.

The cursor oracle calculates expectations from ordinary builtin dictionaries
and the actual legacy builtin set-union algorithm inside each child. It checks
public object types, return contracts, exact token identities and stable old
views/tuples. It alternates omitted default versus explicit False for logically
raw no_work=False sets, exercising both equivalent API spellings without changing
case data or adding scheduled semantic operations. Pure merge callbacks allow
optional unchanged-certified invocations; no cross-name invocation order is
invented. Missing delete and invalid join behavior are explicitly distinguished
from analysis-budget exhaustion.

Each of the four atomicity cases performs only the target primitive inside the
calibrated delta. First/middle/last failures restore only the permitted meter
limit, retry the SAME cursor and require exact pristine units/category deltas.
The subsequent fork/write/publication/read sequence and outputs must also match.
Old witnesses are retained and rechecked. Successful cached returns are allowed;
the oracle does not demand dummy copies or artificial charges.

Compaction category names were supplied as an API/accounting declaration by the
implementation author, without reading implementation: compaction_entry_visits,
compaction_layer_visits and compaction_publication_charge. Only the successful
nonfault retention case uses positive compaction_entry_visits as a structural
precondition. A missing precondition is labeled UnmetStructuralPrecondition,
not a history leak. A throwing compaction charge is never treated as proof of
completion. The fixed fault preparation does not guarantee it lands inside
compaction; reports must inspect actual operation counts before claiming that
coverage.

No production fit, authority-transfer correctness, universal history reclamation,
arbitrary callback effects, general write rollback or collision-subclass behavior
is established by this unexecuted pack. There is no budget or runtime ratio
acceptance threshold. Original charged categories and every public operation
phase remain visible; internal honest-cost coverage still needs source review.

Root owns exact prototype/oracle/control approval and any six serial fresh
D-local children: actual3.11.15 seeds0/1/17, then actual3.14.6 seeds0/1/17.
Authors must not dispatch them. All issued bytes are now immutable.
