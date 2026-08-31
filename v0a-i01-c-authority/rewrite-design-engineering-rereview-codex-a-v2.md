# Partial C rewrite: bounded design rereview

Reviewer: codex / cold_review_a, engineering participant.
Scope: closure of the six concerns in the original draft review only.
Disposition: all six are substantively addressed, with the narrow comprehension
wording clarification below. This is design support, not an implementation
approval, cold pass, runtime result, or integration verdict.

## Frozen custody

- H repository: D:/Pontius-handoffs
- H commit: 135470ade797dbe2001208a7b6ff3fd4dbb6c5fd
- Manifest: rewrite-design-manifest-v1.sha256
- Manifest SHA-256: 51cf85d387ac0b64c59603cd04fc758dcfa936cac839d016673b02fe9f7a6267
- Detailed design SHA-256: 701552c177840e4c5c0dd9c5985776256af5b31e7e997067dd662638a67c3ca8
- Short brief SHA-256: 8c84baa92400716efee2d4dd23eeafefa88a794125bafd4cc97432572ca7e077
- Retained original draft SHA-256: 18ff3c1d6b228474a321d93f8be4498c717f5af2244be62855cfb5e50ec24acb
- Prior engineering review SHA-256: 40eeb140b1cd7bc312883368df3a97127bf1f727b0b197f4751a98bb3fdf3979

Read-only Git verification resolved the exact commit, read committed blobs, and
independently hashed both blob bytes and retained filesystem bytes. All 14
manifest entries matched their stated SHA-256 and byte lengths; the committed
manifest also matched its separately pinned hash. This includes both design
files, the original input, and the prior report. Semantic rereview was confined
to the two design files and the six prior concerns.

The initial sandbox Git read refused differing ownership. An authorized
owner-context read used the validated absolute non-reparse Git executable with
configuration disabled for that process. No safe.directory or other Git
configuration was changed. No manifest script, candidate, test, or Model ran.

## Six-concern closure

Line references are to rewrite-design-v1.md.

| Prior concern | Resolution in the frozen pair |
| --- | --- |
| Executable entry bridges (P1) | Lines 47-61 explicitly include signature transport, helper-entry/prepass, _ReviewFlow/_snapshot_call, _call_environment, source-ordered helper/review flow, unittest preflight, and recursive _review_body. Reporting projections cannot reconstruct execution. Short brief lines 11-15 retains this boundary. Addressed. |
| Complete historical call observation (P1) | Lines 86-101 bind selected callee/receiver, ordered arguments/default references, call-entry state and tagged result/effects. Mutable referents stay live at the applicable invocation/consumption point; defaults freeze references, and final rendering cannot hydrate from final state. Addressed. |
| Successor payloads and R1 (P1) | Lines 111-115 pair outcomes/issues with originating state and retain missing/unbound alternatives; lines 157-159 put the minimal fork/join, return pairing and exceptional completion required by Gate A in R1. Addressed. |
| Class/comprehension scope (P1) | Lines 103-110 add class fallback/deletion, bound/unbound joins, proved lexical destinations, first-iterable context, deferred scope roles and current member-state ownership. Addressed in substance; apply the P2 wording clarification below. |
| Retention versus execution (P2) | Lines 115-119 distinguish alternative/element/capture/member/deferred edges, preserve issues on ignored returns and retain dependencies on unknown shape. Iterating a container does not necessarily execute a deferred element. Lines 127-135 preserve behavioral tests while allowing prototype-specific APIs to retire. Addressed. |
| Meaningful early checkpoint (P2) | Gate A fixes six existing temporal cases/classifications; Gate B fixes twelve existing cases including exact depth and ambient-size controls. Lines 171-184 include prepass/direct-entry/construction work, separate required order enumeration, and adopt 196608 prospectively as engineering reserve rather than a runtime cap or speedup claim. Lines 202-206 retain size reassessment. Addressed. |

## Narrow clarification before implementation

P2, detailed design lines 107-108: the phrase that the implicit body, targets,
filters and later iterables "use the enclosing nonclass scope" is shorthand for
free-name lookup, not ownership of comprehension-local bindings. They execute
in the comprehension's own implicit frame; its targets bind that frame, and
free-name lookup skips the class namespace to the enclosing nonclass scope.
The first outer iterable remains in its actual surrounding context.

Carry this explicit interpretation into the required category/API implementation
plan. It preserves the existing scope contract and requires no additional cases.
It is not permission to write comprehension targets into an enclosing frame or
to bypass already-bound comprehension locals.

## Limits

The short brief is consistent with the detailed design on these six concerns.
The design now states the necessary boundary and finite checkpoints; their
feasibility, accounting completeness and semantic correctness remain unproved
until implementation and fresh public evidence. The 196608 continuation ceiling
has been selected before results, but its sufficiency remains explicitly unproved.

No production/source/test change was made or independently reverified in this
bounded rereview. No broader architecture audit, new population, payload dispatch,
cold verdict, or acceptance claim is implied. The next required category/API plan
must operationalize these obligations before implementation.
