# Addendum 01 to the coordinator note — finalizer ruling, controller rulings, and a
# judgment miss in the coordinator's review harness

Appended 2026-09-09. New record; the coordinator note and all issued reviews are
unchanged.

## Controller rulings (relayed via chat, recorded verbatim where quoted)

- The controller accepts reviews 01 and 02 as cold passes: "I accept both reviews as
  cold passes."
- The controller authorized a third round on this checkpoint: "he asked for a round 3 I
  authorized". The frozen completion brief limits the checkpoint to two rounds before
  returning to the controller; r001 and r002 consumed them; this is the explicit return
  and reauthorization the brief requires for r003.

## Finalizer ruling on r002 (Codex): NOT CLEAN / STRAINED

The finalizer executed a diagnostic on the frozen candidate `430ad75d` (Python 3.14.6,
`source_verified: true`) using an existing real CHECK-hand capture that passes both the
unchanged host parser and the r002 classifier, then mutated only its retained wire bytes:

| Mutation | Unchanged host parser | r002 classifier |
|---|---|---|
| LF changed to CRLF | `protocol_invalid` | hit, chip-eligible |
| First LF changed to U+001E | `protocol_invalid` | hit, chip-eligible |
| First LF changed to U+2028 | `protocol_invalid` | hit, chip-eligible |
| Ready frame padded beyond the host's size limit | `protocol_invalid` | hit, chip-eligible |

All four also produced `completed=1, hits=1, complete=true` in the outcome summary. The
finalizer promoted the framing finding to **Important**: the governing design excludes
malformed frames before chip or hit credit, and a capture the host rejects is malformed
by definition; the action and chip amount being unchanged does not make the evidence
valid. The finalizer's own statement of the miss: parsed-object validation was corrected
in r002, but text normalization and framing checks ahead of that boundary were not.

The coordinator concurs. The disposition, diagnostic and the bounded r003 repair plan
(physical LF framing, frame size, decoding and parser limits, refusal before any credit;
host, solver, export, timing and ownership code out of scope) are the finalizer's local
records at the time of this addendum.

## What the coordinator's harness got wrong, precisely

Reviews 01 and 02, the prosecutor and the critic all *identified* the behaviour — that
`frames_for` splits on universal newlines and imposes no frame size limit while the host
frames on LF only with a 16,384-byte limit — and all four *misjudged* its consequence,
calling it a fidelity gap with no credit path because every content, identity, pairing and
settlement check still applied to the resulting frames. That reasoning answered the wrong
question. The question the requirement asks is not "can a malformed stream produce a hit
that a well-formed stream could not?" but "can the classifier credit a capture the host
would refuse?" — and the answer to that was yes, from the same lines the reviewers cited.

So this round's miss is a judgment miss, not a detection miss: the harness found the
member and graded it Minor. The prosecutor's lens definition was at fault: it was asked
to find mutations that reach `hit` "that a proper capture could not obtain". The correct
standard for a retained-capture classifier is **host-equivalence of admission**: any byte
sequence the unchanged host would refuse must be excluded by the classifier, and any such
sequence that is credited is a defect regardless of what the credited values are. The
next dispatch states that standard explicitly to the reviewers, the prosecutor and the
critic, and the prosecutor's attack table gains a column: "would the unchanged host accept
these bytes?"

## Effect on the record

Reviews 01 and 02 stand as issued and accepted; their Minor gradings of the framing
member are contradicted by the finalizer's executed check, and this addendum sits beside
them. The parent-round Important (parsed-object admission) is closed by r002 as both
reviews found; r003 addresses the framing boundary ahead of it. Codex drafts r003; per
the controller's decision the coordinator dispatches cold reviews from a fresh session
with the corrected standard.
