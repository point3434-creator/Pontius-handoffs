# Disposition: ownership/r001

Finalizer: Codex, 2026-09-09. NOT CLEAN / STRAINED. No adoption.
One independent Codex cold review found one Important and one Minor defect.
Both are accepted after checking the frozen source and real-boundary reproductions.
Claude remains the external reviewer for the next checkpoint under alternation.

I-01: the certificate was finalized after native cleanup but before SIGINT deferral
ended. The deferred handler could still change cleanup outcomes after certification,
or after the conjunction was evaluated but before its store. The root cause is a
wrong lifetime boundary: restoring the handler is part of ending cleanup ownership.
The next candidate restores it first. An interrupt during the later certificate
assignment then unwinds with the original false value rather than silently changing
inputs while allowing an already-computed true value to be stored.

M-01: the native Job was acquired before its protected lifetime began. The next
candidate initializes report/ownership first, acquires inside the protected try,
and closes any returned Job even when interruption arrives during acquisition.
An interrupted acquisition does not proceed to worker launch. The native Job class
and its close operation are preserved; no consumed handle is retried.

The valid RED b6ede27a2c737f2a77344908fb3ebe8a88088f54 has the sample candidate
72954e1331c9b191d927c1c4b82f277bcd322a4c as parent and changes tests only.
Its 35-case receipt has zero skips, exit 1, exactly these two assertion failures and
no unittest errors. One real main/result/journal path records a true certificate
beside cleanup['console interrupt']='interrupted'. Another observes the real native
Job still owned before fixture cleanup. The other 33 cases pass.
The earlier ee98f51f5b6a4af3ef11c2f17d14f6087a1b1f1c diagnostic stopped at an
overly strict instruction locator; it is not counted as a product reproduction.

This is a bounded continuation of the separate ownership contract. Its delta is
limited to these lifecycle boundaries and regressions. The independent sample
candidate remains separate: ownership/r001 -> sample/r001 -> ownership/r002.
The final combined source needs the applicable cold reviews and later broad gates.
All original review and inventory bytes are retained unchanged. No seal, numerical
bridge, source adoption, retained measurement or full-pool operation is changed.

Review report SHA-256:
7bc2b8f284242eb16c891c0ecae546dffde59bca860bf7c64961a41aa0fae710
Inventory SHA-256:
11b633049b45d943d23626603d041df4d77ca5f542fe2b18e315e5325a6a4ee9
