# v26 full-join sharing diagnostic v4

Author: codex/cold_review_a, engineering authoring only; not a cold review or a product verdict. Root owns dispatch. No candidate, fixture, probe, controller or wrapper payload was executed by the author.

Frozen inputs:
- v26 source engineer-generator-v26-storage.py: 1f908957ee43d5841f8da09e306bd52dc5efeca9609a5d522e76df22b4dcd951.
- Reviewed predecessor probe v3: 7aa9f188b2917fec149485501eafcc4d516d3104a10b026e5ec33262b24962ae.
- Reviewed predecessor control v3: 91533776e028ad57513611940423cd1cb2c6d8c0d85f8cafd49f089ebfd9e2d7.
- Original tests c46760b0d08a140e8da7c62a2f554b6a2f57410940e939c6914e9d4ffa873aaf. Existing three fixtures, expectations, caps and absent-hash-seed behavior remain unchanged.

Issued:
- engineer-depth-budget-probe-v4.py: 559b099f96a4fcfb9b88eb05338a45ad2184ca5e153a360ee0123e0ee7969379.
- tests-depth-budget-control-v4.py: d62807554ffd50b7552879c5a7eb8b4b940e729063ab041d36ee9e79b823c8a5.
- engineer-depth-budget-probe-v4-from-v3.diff: 674296516e644c210ce873337e169ec414db0dc26a68ecaa878e712a7e419c24.
- tests-depth-budget-control-v4-from-v3.diff: 7a5d62a8353797cf7bb869ab9a653191b3ad3c792c98c30741be72cf741798f3.
- engineer-depth-budget-v4-static-v1.json: 214f1558b94134a8480e327bd438f81eaeb0db527404a1edb3f082198844b721.
- tests-checks/depth-budget-v4-authoring-v1.py: b54a75a38db76fdedb751afd205b1e264fb14c0699cbafaa5fda9077ab1f28ab.
- tests-checks/depth-budget-v4-authoring-receipt-v1.json retains the static-only authoring result.

The sole new observation is attached to the existing full-join bulk-input charge event. Exact v26 takes every input snapshot at22306-22310, then invokes from_unique_entries at22343; its initial bulk_input_iterator_requests charge at14628 already calls record_bulk_shape. V4 does not add, move or wrap any production event. The observed published roots are the resulting NameVersion._root fields, not cursor bases sampled before publication.

Each original budget summary now includes full_join_sharing_facts. Records expose input/source counts; exact NameVersion inputs and ExecutionState sources; root identity equality; all source authority.enabled values exactly False; source/current-version meter identity and budget identity; and each root's raw size, pending count, known flag and all-pending flag. The conjunction restricted_C_guard_facts reports these structural prerequisites together. It does not assert complete shortcut soundness or authorize C implementation.

Pending counts come only from None root=0, exact leaf.pending tuple length, or exact branch.pending_count nonnegative int, compared to exact version._size. Unknown types/counts remain explicitly unknown (-1, false) and cannot satisfy the conjunction. No pending entries or values are enumerated. The pending-count invariant is assumed as the source representation invariant; the observer does not independently prove it.

All emitted signatures contain only bool/int scalars and tuples thereof. Object references exist only as ephemeral function locals while inspecting the existing event; roots, versions, states, authorities, budgets and frames never enter retained records. Raw exact builtin dict/tuple/list accesses and object.__getattribute__ only; no Mapping/cursor/name helper or metered production lookup, iteration, fork, snapshot, transfer or cache mutation.

Static proof: changed existing probe functions are only observed_init (counter), record_bulk_shape (record facts), and summary (serialize facts), plus one raw scalar helper. All other top-level AST, original-consume observer, hook installer and three fixture builders are identical. Controller changes only the exact probe SHA and basename; embedded wrapper and every custody/execution gate remain byte-identical. Probe, controller and extracted wrapper compile without being executed. Source and predecessors rehashed after authoring; all issued files UTF-8 LF, create-only.

Interpretation: observations count charge attempts, not necessarily completed bulk builds. They are excluded from production charged work and are diagnostic overhead, not optimization savings. Equal name counts alone prove nothing. If the conjunction is absent/false on generator70, these data provide no evidence of utility for the restricted C shortcut. If true, exact legacy union-order reconstruction, pending debt, authority/binding joins and scratch/cache behavior still require the separate source proof and an implementation review. No runtime speed ratio, general fitness, cap change or product pass follows.

Only one fresh generator70 floor diagnostic is currently proposed for root review. The inherited CLI still names the unchanged three-case population, but this handoff does not authorize the other cases or any dev/matrix/corpus/GPU/owner run. Use the existing explicit retained source/source SHA, probe SHA, control SHA and separate W-watch arguments, actual311, fresh r0101761 snapshot, and60s owned direct-child watchdog. All raw failure/incomplete evidence remains retained by the unchanged controller.
