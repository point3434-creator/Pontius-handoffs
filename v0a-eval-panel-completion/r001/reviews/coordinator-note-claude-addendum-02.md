# Addendum 02 to the coordinator note — the four passes disagree, and Codex is right

Appended 2026-09-09 after Codex's cold reviews 03 and 04 were staged (they remain
Codex's coordinator's to publish; this record cites them by their staged verdict lines
only). New record; nothing earlier is rewritten.

## The split

- Reviews 01 and 02 (Opus 5 agents via this coordinator): CLEAN / SOUND.
- Reviews 03 and 04 (Codex): NOT CLEAN / STRAINED, each with one Important finding on
  the same boundary — retained-protocol admission in `src/pontius/eval_agreement.py`
  (`frames_for`, lines 91-170) can credit a malformed retained capture as a `hit` /
  chip-eligible because missing or mistyped nested members are filled by dataclass
  defaults or coerced by equality rather than refused.

## Coordinator verification from the frozen blobs at `449a2a3c`

I re-derived the finding from the bytes, independently of both reports:

- `clean()` (39-44) checks only `failure_reason` and `secondary_failures`; it enforces
  no field set and no types. The frame-level set check (107-113) covers each frame's
  top-level keys only; the nested `decision` object and its `preparation_use` member
  are never set-checked.
- v1 branch (145-151): `prep = dict(record['preparation_use'])`, then
  `PreparationUseRecord(**prep)`. `PreparationUseRecord` (`v0a/model.py:360-374`)
  declares defaults `producer_status="producer_absent"`, `artifact_sha256s=()`,
  `credited_seconds=0`; a `preparation_use` lacking `producer_status` or
  `credited_seconds` is therefore constructed and validates. Line 147's
  `tuple(prep['artifact_sha256s'])` turns the wrong type `''` into the accepted `()`.
  The unchanged host requires the exact three-member object with a list and an exact
  int (`tools/v0a_table_host.py:801-805`).
- `ready['evidentiary']`: present in `WIRE_FIELDS['ready']` (18-19) so its existence
  is required, but its value is never read; only the terminal and closure values are
  checked (161). The host requires `ready.evidentiary is False` (734).
- `terminal['interrupted_response_count'] == 0` (163) admits `False` and `0.0`; the
  host requires `integer()` (43-44, 890). The same coercion applies to
  `requested_hands`/`completed_hands`/`ordinal` (242-245).
- v2 branch (152-155) checks three delivery fields and nothing else; the public
  `validate_decision` (`decision_provider/codec.py:44-`) is never called; the baseline
  early return (264-266) then grants chip eligibility before any later check.

Reachability: every one of these is a post-capture byte mutation of an otherwise valid
completed stream, which is exactly the class the existing test
`test_missing_required_frame_and_decision_fields_are_excluded` (250-262) already
exercises for whole-object removal. Governing requirement: brief mechanism 7 and the
Tier C statement ("must not manufacture successful agreement from missingness,
defaults or failures"). **Confirmed. Important. The candidate is NOT CLEAN.**

## Why reviews 01, 02 and the critic missed it

All three verified the *preconditions of a hit* — replay equality, exactly one river
record, key equality, teacher presence, zero causes — and took `frames_for`'s
validation as established: the critic's report says outright "any
failure/malformation returns at 256-258". Nobody asked the mutation question: for each
nested member the classifier consumes, what happens if it is absent or mistyped? The
coverage claim "strict retained frames" (coverage.md item 11) was read as a fact rather
than as a claim to falsify. This is the same shape as the coordinator's own r003/r004
misses on the ownership contract: paths were traced, the property was not attacked.

Structural weakness in the coordinator's review harness, recorded so it is fixed: the
adversarial verification stage only runs on findings the reviewers raise; when both
reviewers return CLEAN there is nothing to verify, and CLEAN itself is never attacked.
The next dispatch adds a prosecutor stage — an agent required to produce candidate
defects by mutating every consumed field of every retained envelope, whose candidates
then go through the same three-lens verification — regardless of the reviewers'
verdicts.

## Effect on the record

Reviews 01 and 02 stand as issued (immutable) with this addendum attached; their CLEAN
verdicts are contradicted on this point by the frozen source. The completeness
critique's Tier C conclusion ("no path by which missingness, a default or a failure
becomes a hit") is falsified. The finalizer for this checkpoint is Codex; the r001
disposition and the r002 candidate are his. The coordinator recommends accepting R03-01
/ R04 F1 as one Important finding on one contract, with the correction Codex's reviews
name: validate the exact parsed v1/v2 records and every nested object's required
members and types before any conversion or default can fill them, reusing the public
v2 validator, with RED cases that mutate a real captured stream.
