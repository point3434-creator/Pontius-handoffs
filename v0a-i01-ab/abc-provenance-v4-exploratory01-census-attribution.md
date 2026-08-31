# Intermediate v4 corpus attribution

Engineering-only comparison by an independent read-only source/JSON inspector;
not a cold review, final-source check, or acceptance. Root independently checked
the row equality, blocked-item sets and reason deltas in the adjacent JSON.

Old census SHA42013dfbe68bf17a04dc48080f40191b3b89bde617bda59177c31a15edcef9a4.
New census SHAa4737f8f3d7f5d4c7393fdb8a26dcbf874a14e66b9e29a878f5c3f85aeb5e311.
All141 expanded capability row objects, including bounds, are identical. Spec and
analyzed-site hashes are unchanged. The27 cross-file metric counts setUpClass
fixture edges, not a complete graph. Direct45/helper5 subprocess and30CuPy sites
are unchanged. Inventory2860 old entries exact+6new; profile bytes identical.

Blockers895->1159, blocked items344->399:55 newly blocked, zero newly unblocked.
Nine newly blocked items already have capability rows. Raw blocker multiset diff
is296 additions/32 removals.31 removals correspond exactly to+202-line movement
in the sole changed corpus source, tests/test_inventory_and_profiles.py.
The remaining descriptor refusal at transfer_confirmation.py:145 is replaced
by a namespace-identity refusal there, following escape:123 and deferred:135.
The test file's542 decoys preserve content/parent classifications;12 move by202
lines, explaining the digest change without a changed decoy count.

Concrete conservative costs: native_simplex_audit_reanalysis.py:347 creates
cases=[];354/361/370/377 append callbacks retaining local helper functions.
New escape refusals at inert retention sites cascade into28 callable-identity
refusals. Inspected callbacks mutate synthetic campaign dictionaries, not helper
identities. durable_evidence_journal.py:231 passes a self-capturing fsync callback
to patch.object; the escape refusal cascades into namespace refusals on later
assertions. Unchanged v0a_hand_replay.py gains escape refusals at298/313 and1230.

No unsafe output expansion was observed in this corpus, but that does not prove
the implementation correct or every new refusal necessary. The root has asked
the source owner to reproduce the known-list retention case through the public
boundary and distinguish inert storage from invocation before release. External
opaque retention may still refuse explicitly. No corpus counts were copied into
source expectations from this intermediate diagnosis, and no source was replayed.
