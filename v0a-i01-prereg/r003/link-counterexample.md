# r3 generated-link failure

Issuer: /root. Candidate: 953b8703ef93fe261a6857b57bca196b2b8ded9b.
Manifest: f5e5d7a3071518e139e8bdffdbe0f813a510ae80c477fdd9a88fb537be4d6fff.

The existing maintained-local-links test failed on both CPython 3.11.15 and
3.14.6 in fresh snapshots. Each ran 16 tests: 15 passed, 1 failed. STATUS
generation itself and its full 12-test suite passed.

The ADR Decision section includes a relative Markdown link valid under
docs/decisions. The unchanged status generator copies that section verbatim
to repository-root STATUS.md, where ../workflow-amendment-2026-08-30.md
does not resolve. Both r3-py*-2.txt logs retain the deterministic RED.

Correct only the new ADR's portable source reference (and regenerate STATUS),
not the sealed generator or test. Preserve frozen r3. The next candidate is
r004 under the newly adopted permanent handoff convention.
