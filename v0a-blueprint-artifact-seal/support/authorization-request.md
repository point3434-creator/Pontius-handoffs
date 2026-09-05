# Exact integration authorization request

Prepared for controller approval; not itself authorization. Execute only after
the r002 metadata review is CLEAN and its post-review checks pass. If the base,
candidate, payload or authority scope changes, stop and request new approval.

## Bound integration

- Task: v0a-blueprint-artifact-seal/r002
- Candidate: 12df7106b2fca3b25ed4f57115ba9a31e70b6815
- Tree: f3acfba65b32e0890bb86f0af9c087f55e75e50d
- Manifest: c09f4bcc313e987764597f49ef703e8794e76e7be725dc52a642850803a5bb1c
- Primary base: c4af7f61270b583eb3a3c6d8b3b7e4c49637dc98 on master
- Decision title: Source-seal the portable blueprint artifact

## Actions requested together

1. Publish the retained codec implementation, Windows fixture and integration
   coordination packets (r001 and r002, including rejected reports and later
   dispositions) to the existing private Pontius-handoffs repository. Preserve
   their corresponding immutable review/archive source refs in the private
   Pontius repository before any ref retirement. Do not move retained experiment
   results, journals or lifecycle artifacts; the packets contain coordination
   records and scoped correctness receipts. Preserve existing published bytes;
   publication conflicts stop rather than overwrite history.
2. Integrate exactly the frozen 14-path candidate into primary from the named
   unchanged base as one ceremonial commit with the title above, and push master
   to its existing private origin https://github.com/point3434-creator/Pontius.git.
   Verify exact raw-tree equality and the metadata checks at the integration
   boundary. No force push, unrelated staged/untracked path, source change or
   additional decision is permitted. Preserve all local review evidence.

The coordination origin is
https://github.com/point3434-creator/Pontius-handoffs.git.
The 14 paths are exactly the 12 accepted source/registration/CI paths plus
ADR-0491 and generated STATUS. The primary source seal activates only at the
authorized commit, never from this request or the temporary review ref.

No workflow-rule adjustment, next source task, rehearsal, operating invocation,
experiment, policy search or parked-lane reopening is included. The selected
sequence is integrate this accepted asset first; consider rules separately.
