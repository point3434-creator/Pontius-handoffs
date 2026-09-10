# Controller authorization

Received via chat 2026-09-10; recorded at 2026-09-10T05:50:00Z before any launch.

Controller, verbatim: "lets go with what we have thanks for saying that"

Context, so the scope of these words is unambiguous on the record. The message immediately
preceding it reported that the cold review of solve-run-20260910-r003 returned NOT CLEAN
over three Minors, that solve-run-20260910-r004 closes all three and is published, and that
the controller's judgement call was either to send r004 for one more cold pass or to
authorize as-is with the Minors disclosed, noting that the findings had converged out of
the launch path. "What we have" is therefore the current packet, r004, authorized as-is.

Applied to:

- Packet: v0a-eval-panel-completion/solve-run-20260910-r004, manifest
  c7b13da59a3e80d4097f1e70e8a28ddfd0b5df8837ceb866cc2f376fca432c4e
- Source commit: 1c7067448106cfa2aca3d57be879842d72293c61
- Plan: plans/solve.json, SHA-256
  c1a6af606cc80841d61b5824913c8a1b6c896988ae4c578127c1dfc08b4f8982
- Wrapper: invoke.sh, SHA-256
  160cfcecfb96ee8e565594c998704648b9ad0d1516f3fd53dbcedae1bb95287b
- Envelope: 600 s / 2048 MiB, exactly as the recorded resource decision states

Scope: exactly one retained solve invocation, as requested in authorization-request.md.
Nothing else. The export and agreement phases, any second solve, and integration into
master are not authorized here.

Disclosed at the time of authorization and not closed by it: the r003 cold review's three
Minors are corrected in this packet but its correction has not itself been cold-reviewed;
the r002 review's M-01 assumption stands (the helper trusts that the adopted tool is the
sole journal producer in a checkout only this wrapper drives); and the operator duties in
the r003 review's residual-risk row remain with the operator.
