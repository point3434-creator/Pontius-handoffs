# Controller authorization: one retained export

Recorded at 2026-09-10T08:40:47.451257+00:00, before wrapper invocation or claim acquisition.

Controller message, verbatim: "I approve"

Context: the immediately preceding finalizer response identified CLEAN / SOUND readiness
and explicitly named the next gate as one retained export with a 600 s / 2048 MiB worker
envelope, using authorization-template-02.txt. The approval is applied to that exact scope.
It is not quoted as though the controller typed the longer template verbatim.

Resolved binding:

- Source: 1c7067448106cfa2aca3d57be879842d72293c61
- Reviewed manifest: 9965a225729a5896818127c013122f62fb3ae323889fde8ab16ea35e3e43eb17
- Plan SHA-256: c55f26f635f9512c5e5f4a57ab6d64f3327de0697253422e7230296a46fd1c5a
- Wrapper SHA-256: c70c9deab4cb51263a2df134da1dc11b422392bf1309cc5da8f91cf4e9db105b
- Addendum 02 SHA-256: 9d5f71ef45b8d170ce03aa38a8441a125146c295ad385591e17fc36f55417106
- Template 02 SHA-256: 5b8f500dd6cae70be85db3df8fd9e864565bc48444d51b43e3e433294462a4fa
- Identity: D:/Pontius-handoffs/v0a-eval-panel-completion/export-run-20260910-r001/identity.json
- Checkout: D:/Pontius-worktrees/eval-panel-export-20260910, codex/eval-panel-export
- Envelope: 600 seconds / 2048 MiB worker Job memory; parent outside that Job bound.

The current template text resolving this approval is:

I authorize one retained export invocation on 1c7067448106cfa2aca3d57be879842d72293c61 as bound in D:/Pontius-handoffs/v0a-eval-panel-completion/export-run-20260910-r001/identity.json, reviewed manifest SHA-256 9965a225729a5896818127c013122f62fb3ae323889fde8ab16ea35e3e43eb17, with documentation corrections in D:/Pontius-handoffs/v0a-eval-panel-completion/export-run-20260910-r001/finalizer-addendum-02.md (SHA-256 9d5f71ef45b8d170ce03aa38a8441a125146c295ad385591e17fc36f55417106), and the proposed 600 s / 2048 MiB worker Job envelope.

Pre-claim checks verified the frozen files, producer/prerequisite bindings, source HEAD,
checkout scope, tracked run census, locked Python 3.14.6 and required launch environment.
SystemRoot/SYSTEMROOT resolved to an existing directory; TEMP and TMP were writable.
The launch uses Bash --noprofile --norc with REHEARSAL and both root overrides unset.

Authority: exactly one retained export. No second export, solve, agreement, source change,
master integration, commit or push is authorized by this record. A post-claim failure or
ambiguous interruption preserves the claim and requires controller disposition; no retry.
