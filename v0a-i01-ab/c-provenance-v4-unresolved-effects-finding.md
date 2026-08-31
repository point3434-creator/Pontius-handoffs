# Intermediate engineering finding: unresolved callback effects disappear

Standing: required engineering correction before release; not a cold-review verdict
or a new residual round. It was reproduced on the captured green05 source in the
exploratory disposable clone, not asserted from mutable working files.
Generator SHAa077d8d9adf4dec9e9b87e3a3f47b89fe9ad2401983187a9b63212496954f579;
test SHAde89cf83caccce2c007c72530b0bd2308f03670f54c29f015bf2b2748b5ed3e4.
The source metadata, ordinary-generation receipt and all17 before/after hashes
are bound in the adjacent per-slot receipts.

A callback nested inside ReviewTests.test_static uses the implicit class cell:
def mutate(_): __class__._launch = None
list(map(mutate, [None]))
return self._launch()

The harmless projection raises TypeError on actual3.11.15 and3.14.6 because the
helper was replaced. The design derivation emits the old fixed subprocess row
with zero blockers. Direct invocation of the same mutator instead produces an
unresolved namespace-owner refusal. A readonly __class__.__name__ callback stays
lawful. No sensitive fixture body executed.

This supports the same mechanism as the existing contract finding: an escaping
callable's absent/unproved free binding can disappear from reachable authority,
and an empty discovered-owner set is treated as proof of no relevant effect.
The required outcome is to retain an unresolved namespace-effect obligation when
absence of effects is unproved, while preserving proved readonly/irrelevant
callbacks. Merely adding one spelling to owner seeding would not close that rule.
The source owner will reproduce against r009 and the current repair, then reuse
the bounded effect classifier or document a larger design need. No general
reflection/heap/callback runtime or new capability grant is requested.

Payload: abc-provenance-v4-implicit-class-probe.py

311 receipt: abc-provenance-v4-implicit-class-exploratory01-311-receipt.json SHA256 e405410c6a231bb50e4180bb71b8f36c0984313007acde43989ff1fc8cf25d6b

314 receipt: abc-provenance-v4-implicit-class-exploratory01-314-receipt.json SHA256 89794af2475f2feed061d5be2d8826451da09cc6aa926d0e587a66e180e2cdf5
