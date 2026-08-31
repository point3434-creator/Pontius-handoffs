# Proposed helper1050 budget-assertion correction

This is a new reviewable test candidate, not a relabeling of any prior failed run.
Original r010 and tests-candidate-v4 bytes remain immutable. No W/main change,
payload, analyzer cap or production error wording change is made here.

Source: tests-candidate-v4.py SHA256 06e169d4f35920e0db3c783dfbebf4716cfe45f989847426aa0d7937275e1afd.
Candidate: tests-candidate-v5.py SHA256 48c4620bf5585a76d500b3c9bf4cad4559a04d4f544bc3808832d37b58b03add.

The helper1050 test explicitly accepts an analysis depth OR budget refusal, but
its regex does not match the canonical work-budget error. The original separate
budget-boundary test explicitly requires that exact canonical message. The
contradiction and both source anchors are retained in
coordinator-helper1050-contract-clarification-v1.json.

Only this assertion's regex changes, from:
`analysis.*(?:depth|budget)`
to:
`^analysis (?:helper depth exceeds 64|work units exceed 262144)$`

This recognizes the two precise admissible outcomes for this helper-chain
fixture. It does not accept arbitrary errors mentioning a budget, change the
1050-definition source, skip its execution, or raise the existing 64-depth and
262144-work limits. The independent helper65 and generator70 exact-depth
assertions remain byte-for-byte unchanged, as do all other test AST nodes and
the existing fixed matrix. The regex-only static check is not a payload verdict.

Category: bounded-analysis refusal classification. Enumeration: the one old
depth-or-budget regex, both production canonical error paths, the separate
exact work-budget assertion, and both exact-depth fixtures. This closes an
inconsistent assertion; it makes no claim that storage or analyzer semantics
are repaired. Review this delta before adapting any frozen focused controller.
All earlier design runs retain their recorded failures and original manifests.
