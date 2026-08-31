# R2 checkpoint 1 category and new-work ledger v1

Engineering implementation input, not cold-review or runtime evidence. Author: mapping_compatibility, 2026-08-31. Bound source: `rewrite-r2-checkpoint1-source-v1.py` SHA256 `41b4de563da886a7c674d49b25acd4332ba208906b403ec244d1a4aea856ee05`; base c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f. Authorization: `rewrite-r2-source-checkpoint1-disposition-v1.md` SHA256 `58059acc64c13acdf7adfbf3330dbb3491f8de3b9dd1c0127557159c190e7977`. Approved plan/addendum remain controlling.

## Invariant and discovery

Identity comparison after successful operand evaluation always returns a builtin boolean, even when the analyzer cannot prove its value. That proof must be separate from generic unknown truth and from runtime object identity. An uncertain proved boolean may enter both source branches, each with its own state wrapper; unsupported generic truth still refuses.

Discovery used whole-file AST/name searches for _CValue alternatives, direct proof constructors, key/choice handling, both _c_truth callers, identity dispatch and outcome/branch transport. The exact source contains two proof-value constructor sites and two truth consumers. Seven edits change seven existing top-level nodes and add two. Reverse application reproduces every base byte.

| Changed node / candidate line | Category responsibility |
| --- | --- |
| New _CBooleanUnknown9091 | Frozen, slotted, fieldless, eq=False proof value. Its Python object/key identity never proves the runtime bool value or identity. |
| _CChoice9096 and _CValue alias | Permit retained proof values in the existing value domain. |
| _c_value_key9455 / _c_choice9474 | Give each proof object an opaque identity key for alternative deduplication; independent proofs do not collapse by structural equality. The choice algorithm is otherwise unchanged; only its element annotation widens. |
| New _c_identity_compare10106 | Receives already evaluated values and the admitted Is/IsNot operator. Produces an exact literal bool only from the facts below; otherwise constructs the new proof at10135. |
| _c_truth10141 | Returns the proof object as a distinct result from exact bool and unsupported None; existing scalar/native-sequence behavior stays intact. |
| _c_eval10229 | Existing single identity-comparison route calls the helper; operand evaluation order and failure propagation remain. Unary Not is the second proof producer at10350. |
| _c_statement10381 | If recognizes the proof, visits body then orelse, and forks the original prior.state separately for each at10442. Exact truth uses one branch; unsupported truth retains the old refusal. |

## Entire value-domain identity disposition

| Operands already evaluated normally | Result |
| --- | --- |
| Two canonical _CRef values | Exact comparison of their stable object IDs, inverted for IsNot. |
| Two literal atoms, at least one None/True/False singleton | Exact identity answer; another admitted literal of a different type cannot be that singleton. Equal non-singleton literal values alone do not prove identity. |
| Canonical reference and literal singleton, either order | Exact nonidentity, inverted for IsNot. |
| Two non-singleton literal atoms | Proved boolean uncertainty; no interning/value-equality assumption. |
| Symbolic, generic unknown or unbound atoms | Proved boolean uncertainty at this internal value boundary. Public unbound/failed operand evaluation still refuses before entering the comparison helper. |
| _CBooleanUnknown, including the same proof object twice | Proved boolean uncertainty; neither object identity nor the choice key is runtime identity proof. |
| _CChoice, including choices with singleton alternatives | Proved boolean uncertainty; no flattening, negative singleton shortcut, or all-alternative precision claim. |

IsNot preserves uncertainty and inverts only an exact bool. Unsupported operator kinds raise explicit InventoryError at the internal helper boundary; the public caller admits only one Is/IsNot comparison.

Both truth consumers are explicit: Not at10347 and If at10427. They check the proof type before Python truth/negation. Generic unknowns and unsupported protocols remain refused. Choices themselves still lack an admitted truth rule, even if their alternatives happen to be booleans. _c_choice has no production caller in this R1/R2 increment; its widened domain is static compatibility, not claimed exercised precision.

Cells, aliases, captures/defaults, native sequence elements, helper returns, call observations and ordered outcomes retain the existing _CValue references. Their algorithms and all outcome/context/call reconstruction code remain byte-exact. Existing strict type gates for indexing, member/call selection, environment/string arguments and sink policy do not turn the proof into a concrete scalar; unsupported consumption stays conservative.

## Branch and outcome transport

The predicate is evaluated once. A proved uncertain result creates an ordered pair of AST body references. For each reached alternative, _c_fork receives the same pre-branch prior.state; execution mutates only the returned child wrapper under the existing COW rules. The first child cannot change the parent's cells/objects used by the second fork. The arena remains shared for collision-free allocation IDs.

The unchanged _c_statements dispatches only normal outcomes and carries abrupt ones unchanged. Each returned body outcome is linked with prior debt/trace using unchanged _c_follow; _c_join keeps distinct ordered outcome objects and states without heap flattening. In the fixed three-decision ladder, the true branch ends that ladder and only the false branch reaches its next If. This is the source mechanism for four leaves, not an executed four-leaf claim or a general predicate-correlation solver.

No fixture-name dispatch, supplied Model region, extra decision, mutable-wrapper reuse, exception handler, generator support, telemetry callback or public schema change is introduced.

## New-work accounting

All operations use the existing current ctx.budget. The original budget class/caps and storage algorithms are unchanged. Fixed scalar type/kind dispatch is part of the reached semantic operation; this ledger does not claim a Python-bytecode instruction census.

| Site | Actual charged work |
| --- | --- |
| _c_identity_compare | 1 reached identity operation. Read two canonical IDs or two literal payloads: +2; reference/singleton candidate payload: +1; opaque/choice/proof fallback needs neither payload branch. Exact result uses existing _c_atom cost4; uncertain result allocates one fieldless proof: +1. Invalid operator pays only the reached operation before refusal. |
| Unknown identity examples | Opaque/choice/proof result:2 total; two nonsingleton literal payloads:4; reference plus nonsingleton literal:3. No nonexistent atom fields or alternative traversal is charged. |
| Exact identity examples | Reference/reference or admitted literal pair:7 total; reference/singleton:6. |
| Unary Not on proof | Existing truth/outcome/trace pipeline charges remain; new fieldless proof costs1. Exact bool and refused generic truth keep their original producers. |
| Proof choice key | 4 = identity integer + tuple allocation + two retained tuple fields. Existing choice visits/probes/retained references/container guard remain charged. |
| Exact If branch routing | New singleton branch tuple costs2, plus1 branch visit. No fork. Existing entered/body/follow/join charges remain. |
| Uncertain If routing | Branch tuple costs3, two branch visits cost2, and two existing forks cost8 each:21 before entered/body/follow/join work. Forks occur only when that alternative is reached, not prepaid across an earlier abort. |

The uncertain proof has fewer fields than the old reason-bearing unknown atom; the changed allocation cost is disclosed, not a refund or threshold adjustment. Every additional branch's real body, continuation, trace and subsequent COW copies remains charged. D0 fork itself does not scan ambient cells; subsequent operations may still copy whole object tables/banks, with their unchanged 1+3N costs. No headroom prediction is made.

## Coverage and falsifiers

Baseline evidence is root's full twelve-case r2-base01 floor observation: twelve public attempts,24 exact Model projections; D0 identity cases fail unsupported truth, D2 cases stop at unsupported Try, and generator70 stops at GeneratorExp. The original six controls and helper65 behavior were retained. Checkpoint1 has no runtime evidence; D2/generator remain deliberately unsupported until later approved checkpoints.

Future integrated evidence must show the three identity sites and four distinct leaf states through the real public path, unchanged required-clean controls, strict generic-unknown refusal, and honest costs. An uncertain choice treated as definitely non-singleton, a boolean proof used as runtime identity, parent-state contamination between branches, skipped alternatives, lost prefix effects, new old-engine fallback or missing work charge would falsify this claim. No new fixture or expectation was authored or changed.
