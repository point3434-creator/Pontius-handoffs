# Controller authorization - exact driver seal and packet publication

The controller replied "I authorize both actions" to the request to:

1. Publish the associated v0a-driver/r001 and v0a-driver-seal/r001 review packets
   to Pontius-handoffs with exact-byte preservation.
2. Commit the exact five-file candidate d45de2bb4522851723667f65f4450c7155833d9a as
   "Source-seal the non-evidentiary v0a driver", fast-forward master and push origin/master.

Authorized manifest: b04f8e29d8e4522aefb5ecc8878e6f40f074b91b0bd58208dcc286f48e820e1d.
Authorized tree: 3f1440fcec994239ed7598f391a9a325350dd4ab.
Required parent: af90155ebd970d0be6fe26969b121bd213a7f1f2.
No rehearsal or operational invocation is authorized.

Fresh pre-commit checks ran the exact frozen candidate in separate no-hardlink
detached D-local snapshots, CPython 3.11.15 first and 3.14.6 second, normal-user
Windows permissions, -B -P, scrubbed environment, snapshot cwd/src, absolute Git,
and D-local temporary directories. Both completed six suites and 206 tests, all
passed, no skips, all command exits zero. Snapshot tracked bytes remained unchanged.
Receipts are retained in checks/authorized-311/ and checks/authorized-314/.

Publication stages only these two packet directories and the exact-byte attributes
for them. Each staged packet blob must match its issued working bytes. Existing
unrelated handoff modifications/untracked files are excluded. The source index must
contain exactly five authorized paths and match the approved tree before commit.
Commit-local empty hooks avoid the automatic feature-branch push; normal persistent
hook configuration is not modified. Approved branch pushes are explicit and verified.
Neither review refs nor host-owned worktrees are retired or deleted in these actions.
