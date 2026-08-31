# Empty-class late-member alias witnesses L01-L08

Author: codex/cold_review_a, independent engineering witness author; not a cold review.
Root approved these eight cases before any family payload: four required-refuse and four required-clean, one harmless Model projection per case. The original44 expectations remain byte-identical.

Case pack: class-owner-late-store-cases-v1.json
SHA256 08fce0e37eaeb24192c4f227677d7625097748ccb2cbc79470df4699718a9b47
Source basis: engineer-generator-v23-semantic.py
SHA256 53a17d52196bd83a540ebf4892d3687f3efbe9633d1539fa834ea0a27f0db499
Reviewed scopev3: engineer-generator-v25-semantic-plan-v3.md
SHA256 1d661231a472fc689af06ea993234f27ab88a65da950d83f1811c1f941d94723

| ID | Owner and old alias | Store / consumption | Requirement |
| --- | --- | --- | --- |
| L01 | Empty local class; direct alias | Marked generator / reached | refuse |
| L02 | Same | Marked generator / literal dormant branch | clean |
| L03 | Empty local class; singleton tuple element | Marked generator / reached | refuse |
| L04 | Same | Marked generator / literal dormant branch | clean |
| L05 | Empty local class; closure captures old alias | Marked generator / reached | refuse |
| L06 | Same | Marked generator / literal dormant branch | clean |
| L07 | Empty module class; direct alias | Marked generator / reached | refuse |
| L08 | Same module origin | Scalar0 / literal dormant branch | clean |

For L01-L06, Bare is created normally inside the selected test before any alias. Every alias exists before the later Installer class body assigns Bare.pending. The direct alias is alias=Bare; the contained alias is owners=(Bare,); the captured alias is a plain local function returning alias, defined before the store and called only at consumption. No visible-name replacement can substitute for all of these live aliases. Neither Bare nor Installer has bases, decorators, methods, custom descriptors or metaclass keywords.

Installer has armed=False, while the enclosing test has armed=True. The generator is created directly as the RHS of Bare.pending=(read(armed) for unused in (0,)) inside Installer. Its real implicit body reads the enclosing function cell, not Installer's shadow. The store itself obtains the first iterator but does not call read. The generator is never exported as an Installer member, so Q05's original Installer-member transport is not a prerequisite. After Installer completes, tuple consumes the selected old alias's pending member. read(True) writes the sink class attribute to None; tuple completes, and the final self._launch() attempt raises TypeError. No unsafe Model reaches sink.

L02/L04/L06 change only the literal consumption guard to False. Construction, aliases and the same marked generator store still happen, but member extraction, captured-alias invocation, generator body and protected sink mutation are unreachable. These clean requirements preserve the admitted dormant-enabled-storage behavior. They do not demand exact ordinary class-member values after consumption.

L07/L08 put the empty Bare class at module scope, before ReviewTests/Model. L07 reaches the same marked store and direct-alias consumption. Public analysis may preserve the obligation or explicitly refuse unresolved-origin storage; it may not silently authorize the fixed sink. This case does not assert an internal disabled/enabled mode: v23 explicitly supplies module classes as qname values with helper_provenance.kind='class' (24788-24803;25009-25010), which is a distinct known-class origin from a locally constructed implicit_class. L08 stores scalar0 and does not consume it. This is the matched nonobligation-store clean control. It deliberately does NOT require a dormant marked store on an unresolved/module origin to be accepted; root separately authorized a new conservative refusal for that boundary.

Expected traces are fixed in JSON. Common unsafe trace:
owner-created (owner-ready for module), alias-created, installer-enter, member-stored, installer-finished, consume, read, write, consume-end -> TypeError.
L05 inserts alias-read immediately after consume.
Local dormant traces stop after installer-finished and then sink -> fixed.
L08 uses owner-ready and scalar-stored, then sink -> fixed.
Unreachable events are explicit per case. Required-clean means no public blockers and exactly argv [[-m,fixed]]. Required-refuse means at least one explicit public blocker; dropping an expanded row alone does not pass.

Existing-source inspection establishes a guard gap, not an executed wrong-clean claim for these new cases:
- _transfer_authority14152-14153 bypasses disabled stores. Its enabled registration predicate14184-14188 does not register an otherwise empty implicit_class. Normal class completion23881-23899 has no initial method obligations for Bare.
- _helper_namespace_store19033-19057 checks reflective writes, known protected/registered members, and selected active-helper unknown owners. The ordinary name pending is neither reflective nor a defined helper/member in these programs.
- The general store guard22011-22017 walks _flow_contains_helper_identity12563-12585, which does not inspect a plain generator state's class_scope_unresolved marker. _flow_is_sensitive12537-12560 does not interpret that marker either.
- The implicit attribute-store check22211-22216/16525-16559 needs a relevant sensitive protocol; these empty ordinary classes have none. Ordinary pending is not an _IMPLICIT_CLASS_METHOD_NAMES update.
- The legacy _flow_store_path13445-13463 may replace a nonsensitive implicit_class projection with a fresh mapping. That is name-local projection, not evidence that old contained/captured aliases share the updated Python object.
These statements do not rule out another conservative public refusal or prescribe how many v23 cases will be RED. Only root-owned fresh execution can establish actual outcomes.

Design assessment: reserving an existing-store owner identity before successful enabled class binding is the smallest coherent way to let later negative member roots reach all old aliases. The class_member_owner tag is ownership evidence only, never a callable/deferred execution obligation or positive class-heap/MRO proof. Same-ID joins retain it, current successor records govern member roots, and historical copies remain immutable. A known unproved class origin must survive ordinary scalar/opaque projections without inventing identity; qname class provenance counts, arbitrary mappings/unknown qnames do not. Store-owner traversal follows immediate owner alternatives only, not contained elements, callable captures or instance-to-class edges. The supplied-value negative-root walker must use current authoritative collection content and role-tagged deferred/callable carriers; stale embedded native contents cannot resurrect roots. Missing owner alternatives cannot be dropped because another alternative has a proved record. Root's new unresolved-origin refusal is explicitly a new policy application, not an old behavior claimed after the fact.

The executable Models are separately authored pure class/function programs. They have no imports, filesystem/process/network capabilities, or sensitive fixture bodies. Static proof compares complete test bodies after removing only Model event-append statements and renaming Model to ReviewTests, and compares the module Bare definition when present. It separately checks the harmless sink and restricted call/name surface. Each future run creates a fresh Model namespace/class and events list, calls test_static once, and catches only its final expected TypeError outside the method. An unexpected Model error is infrastructure/oracle failure, not product RED.

No payload is authorized by this specification. Root will review the distinct class-owner-late-store probe/control before serial actual311 then matching intact same-candidate314 runs. The inherited exact source pin, manifest, fresh D-local r010 snapshot, seed0, scrubbed environment, original caps, 60s owned direct-child watchdog and raw output custody remain required. No private analyzer observer, W/source/test edit, broad/guarded/GPU/owner run, ledger or commit.
