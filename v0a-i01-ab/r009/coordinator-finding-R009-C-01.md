# Coordinator engineering finding R009-C-01

Candidate commit: 8d240db477b8c141e6142e055dbfbedc75c6a2f8
Manifest SHA-256: 4f91aa7ce728c3eff6a7ad30a7c131985d5b86b615875df978d30ac39386aa51
Standing: Important required correction; engineering finding, not a cold pass.
Coordinator disposition: r009 cannot enter acceptance with this finding open.

Eight pure-return projections on actual3.11.15 then3.14.6 reproduce an unblocked
stale helper row: consumed map and sorted key callbacks, each mutating an owner
through a local cell, global name, receiver cell or default argument. Real Python
raises TypeError at the subsequent self._launch() lookup/call after replacement
with None. Design derivation emits one literal subprocess capability row and no
unresolved blocker. Two readonly callbacks retain the lawful fixed result and row.
The subprocess body was replaced with return module only in the runtime projection;
no sensitive synthetic command or GPU code executed. Both payload exits are1;
the outer evidence-capture commands completed successfully, not the tested contract.

This violates the required current-callable/unsupported-escape refusal contract.
It is not a change to A/B, and passing existing tests/unchanged real capability
rows does not close it. No source changes follow this finding in r009. The first
cold review remains independent; this coordinator finding must not enter its
initial or deferred inputs. A new frozen correction must receive fresh reviews.

The current diagnosis separates two mechanisms: helper provenance roots are
selected from incidental syntactic uses rather than every relevant binding load;
callable traversal retains defaults/receivers but does not inspect free cells.
For the default case, replacing final self._launch with ReviewTests._launch is a
pending falsifying check of the root-selection mechanism. Static source diagnosis
is not substituted for executable confirmation. Map has no special interpreter
here; generic callback escape must still refuse unknown authority. Sorted's key
callback is another execution/escape boundary, not evidence of a map-specific bug.

Evidence:
- checks/coordinator-closure-escape-probe.py SHA256 8d1aec927fcc0875724788c1340c14c0fdc83ccd3489f356d38d4b447475808e
- checks/coordinator-closure-escape-311.txt SHA256 da165ab2eeaf4731d165f9c52c6446c3ddc7ea5f33ff3b73d31bcc62e98a6e8d
- checks/coordinator-closure-escape-311-receipt.json SHA256 3f34b2edcc361e82d16f61996f98b642f3851336dbe53c35ffc0522ed5b1e34e
- checks/coordinator-closure-escape-314.txt SHA256 2f7f53ba2c3a420882d3d9aa9cf1a82cd2cc4e397019625a0960a1d0b5dd9c8f
- checks/coordinator-closure-escape-314-receipt.json SHA256 2d69f2138c9a74b04d2c9cf71f2e62d18228d45c3449e6d755392add454f4d72
