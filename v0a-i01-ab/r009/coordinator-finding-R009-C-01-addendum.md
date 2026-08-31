# R009-C-01 addendum: provenance prediction confirmed

This append-only record supplements coordinator-finding-R009-C-01.md without
changing that issued finding. It binds to candidate
8d240db477b8c141e6142e055dbfbedc75c6a2f8 and manifest
4f91aa7ce728c3eff6a7ad30a7c131985d5b86b615875df978d30ac39386aa51.

The previously pending falsifier has run in the same frozen disposable snapshot
on actual CPython 3.11.15. All three pure-return projections raise TypeError:
the callback replaced the class's helper with None. With a final self._launch()
lookup, the derivation produces one stale process row and zero blockers.
Adding only unused = ReviewTests, or changing only the final staticmethod lookup
to ReviewTests._launch(), changes the result to zero rows and two blockers.
Thus adding the inert reference changes unsafe acceptance into rejection.
It does not make the real mutation disappear.

The source-point provenance seed hypothesis is confirmed for this witness.
This is not proof that completing roots alone closes callback/free-cell effects.
Cold A's separately issued forwarding finding agrees with the root-selection
mechanism and adds store-free forwarding as an independently reproduced path.
Neither finding was supplied as the other reviewer's input.

Evidence: checks/coordinator-provenance-metamorphic.py,
checks/coordinator-provenance-metamorphic-311.txt and the adjacent receipt.
The receipt binds the executable/version, source hashes and unchanged frozen
snapshot. This is contract-diagnosis evidence only; no sensitive fixture ran.
