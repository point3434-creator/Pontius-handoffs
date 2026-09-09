# r1 contract counterexamples

Issuer: /root (implementer verification, not an independent verdict).
Candidate: 073f0c5b8e6ad4f8d6e10dd9118b722186968ddf.
Manifest: 4b01560395285a30fb65530fb776598d076c4a7bc687eed89d32e650c18dbdc0.

Recorded before modifying the rejected candidate's proposed contracts.
These are deterministic specification counterexamples, not runtime test RED:
the proposed runtime does not exist and no experiment owner was invoked.

1. A controlled turn starts with valid time; the mailbox acknowledges its action;
   the next witness call reverses or returns an invalid value. The preserved
   action_clock.py finish_action invokes _observe before creating its snapshot
   (line 546); _read_clock/_observe raises (181-190). ADR-0485 r1 requires a
   decision row with valid emission/elapsed values and final ledger outputs
   (275-280). No truthful conforming decision row exists. An action-bearing
   failure row cannot replace its full decision record. Before-delivery failure
   also has no timing field to retain an interrupted response.

2. Take identical accepted event payloads, selected decisions, and settlement
   under distinct correctness run IDs A and B. Every decision row has run_id
   (242-250); the r1 projection removes only timing (295-304), so A and B produce
   different canonical projected bytes. The stated exact replay comparison is
   ambiguous unless run identity is excluded and independently validated.

Remediation target: freeze representable interrupted timing and honest incomplete
accounting; freeze an exhaustive run-independent semantic projection. Require
real-path implementation controls later. No sealed API or brief edit is needed.
