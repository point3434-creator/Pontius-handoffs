# Partial C rewrite: draft engineering design review

Reviewer: codex / cold_review_a, acting as an engineering participant.
Status: bounded read-only design review, not a cold pass, implementation approval,
runtime result, or acceptance verdict.

## Bound input and scope

This report records the review issued in conversation for the coordinator draft
originally read at D:/Pontius/codex-c-core-rewrite-brief-draft.md.

- Reviewed draft SHA-256: 18ff3c1d6b228474a321d93f8be4498c717f5af2244be62855cfb5e50ec24acb
- Frozen v30 source: engineer-generator-v30-storage.py
- Frozen v30 source SHA-256: 1a28fce14cfdd2ee30d9892b7d2719aba8ec152d99d1e3c915660648cf9756fd
- Stage0: stage0-design.md
- Stage0 SHA-256: 78bebca5279bf81e30181787f962d40c73826259d0bb3ffb1c7804804c1211e8
- r010 acceptance: D:/Pontius-handoffs/v0a-i01-ab/r010/acceptance.md
- r010 acceptance SHA-256: 889f0bb7508e22ac668b99165cdccf4b75ee0ada67ce50c1e12e20a1f2153da4
- r010 candidate commit: 29c02f6fbd5eb0b7ddc9e816ef28f570b9839358
- r010 manifest SHA-256: 8741fa20b1ebc7e9e9d226f463680c603c348f1332bf19c8ae12b29579f76deb

The coordinator amended the mutable draft during the review. These findings
apply only to the original hash above. This reviewer did not preserve its raw
bytes and does not claim the present mutable path still contains that input.
The coordinator is separately retaining a hash-verified reconstruction. A later
brief needs its own bounded rereview; neither the input hash nor these findings
is silently rebound to later bytes.

Inspection covered the original behavioral contract and the v30 value/state,
call observation, helper entry, deferred frame and successor seams. There was no
candidate import, inspected-source execution, test run, new scenario population,
source change, or inspection of unfinished v31. Source anchors below refer to
the pinned v30 file. Findings are design closure requirements, not demonstrated
runtime failures of an unimplemented replacement.

## Engineering disposition

The partial replacement boundary is appropriate. The draft correctly supersedes
Stage0's choice to retain legacy abstract values as an independent semantic
representation without superseding behavioral acceptance. Replacing only the
authority payload or storage backend would leave the synchronization problem.

Before implementation, close the following design gaps. P1 means a material
boundary/invariant clarification needed before authoring; P2 means a checkpoint
or representation constraint that must be fixed before the affected work or run.
These are engineering priorities, not cold-review defect labels.

### P1: Close every executable entry bridge

Replacing _SourceOrderedResolver alone is insufficient. Include the executable
semantics of _snapshot_call/_ReviewFlow (17214 and 12340), _call_environment
(15519), _source_ordered_helper_return (24437), _source_ordered_review_flow
(24480), direct unittest preflight/receiver analysis (27401 onward), and recursive
_review_body entry (26042).

At 26525-26589 and 26673-26728, _review_body reconstructs helper arguments through
FlowValue, literal AST, and a new analysis environment. Keeping that bridge for
live objects would preserve a second semantic truth. The current _call_environment
also hydrates projected names from cells; its semantic role must become explicit
frame/reference lookup, not a compatibility projection.

This does not require replacing every line in those functions. Static discovery,
signature matching, row aggregation and other pure algorithms can remain. Their
executable input/output boundary must use the canonical references and state,
without a live FlowValue/literal/alias round trip. The binder's exact positional,
default, keyword and bound-receiver rules remain required.

### P1: Specify a complete historical call observation

The observation must carry the selected callable/bound receiver, evaluated
argument/default references, and the corresponding call-entry state version.
Argument effects update current objects/cells without replacing an already
selected callable merely because its old name was rebound.

Recursive review must use that observation, not a later caller state or a
reconstructed name projection. The v30 snapshot currently stores and separately
merges callable values, state, defaults and arguments (17221-17240); those fields
must not become independent authorities in the replacement.

A default captures the selected value/reference, not a frozen copy of a mutable
object's contents. A closure retains its cell even when unbound or currently
irrelevant. Immutable historical observations must not freeze live closure
contents before later argument effects. Source-point observations and live
execution lookup are distinct operations over the same state model.

### P1: Make successor payloads part of R1

Return values and exceptional outcomes must remain paired with their originating
states. Missing or unbound alternatives must not disappear when present values
are joined. The v30 exceptional and successor structures are at 15222-15240,
throw snapshots at 17405-17437, statement propagation at 22852-22870, and return
handling at 22908 onward.

Minimal fork/join and exceptional completion cannot wait until R2 if R1's fixed
selected controls already exercise them. Preserve throw-point effects, handler
tags/partitions, finally behavior, and failed lookup's absence of helper-body
execution. Joining normal and exceptional effects is not permission to execute
a helper on a proved failed-lookup successor.

This is an increment-boundary correction, not a demand to implement every
supported statement before the first small public checkpoint.

### P1: State the complete fixed class/comprehension boundary

The draft's method free-variable sentence is necessary but insufficient for the
existing fixed contract. Class first iterables, defaults and headers use the
actual class context. Implicit comprehension bodies and method closures use the
enclosing nonclass scope. Include class shadow deletion/fallback and proved
lexical write destinations.

Current cells must come from the applicable successor; class locals must not
become accidental closure locals, nor may a later caller supply a missing
capture. These are existing acceptance traps, not requests for descriptors,
metaclasses or general Python precision beyond the declared contract.

### P2: Distinguish retention from execution in the value algebra

Alternative, element, member, capture and deferred-frame edges cannot all mean
immediate consumption. Iterating a container may forward a deferred element
without executing it. Unknown shape must retain unresolved dependencies while
supported dormant storage remains lawful.

V30 demonstrates the duplication to remove: _FlowValue helper fields at
9019-9037 coexist with _AuthorityRecord.value/cells/retained at 13853-13858;
deferred frames embed bindings/frame/delegate projections at 9261-9271; deferred
state changes repair nested values and name aliases at 17577 onward.

Immutable descriptor syntax may remain reusable. Current member/override
decisions must not become an independent authoritative descriptor projection.
A reporting view is safe only when it cannot feed evaluation back into the core.

### P2: Freeze a meaningful early checkpoint

R1's 2500-line bound is a reassessment boundary, not evidence that the required
vertical slice will fit. Cost fitness must include prepass, construction/protocol
and direct-entry work, not only enabled helper execution. Those entry paths
already execute resolver semantics in v30.

Distinguish prohibited repeated ambient value reconstruction from legitimately
required ordered-name enumeration. The latter still incurs actual charges; a
new backend may not hide it or claim an unexercised order path was verified.

The proposed 196608-unit threshold is prospective engineering headroom/stop
policy, not an existing runtime cap or a demonstrated sufficient margin. Freeze
its disposition before results. Preserve all original budget epochs and caps.
Correct rows/blockers and the required depth outcomes remain prerequisites;
an early unsupported refusal is not a successful replacement checkpoint for a
required-clean or exact-depth case.

## What can remain outside

Parsing/discovery, immutable syntax and lexical metadata, signature-matching
algorithms, exception-partition algorithms, final row rendering, capability
policy, and native publication can remain, provided none reconstruct executable
live state. The same applies to pure evaluators only when their inputs/outputs
cannot contain an alternative copy of mutable helper state.

The fixed requirements do not mandate NameVersion, NameCursor, radix/history,
no_work certificates, MutableMapping compatibility, or the live FlowValue
representation. Their retired implementation evidence stays retained; observable
alias behavior, temporal order, snapshot stability, failure safety and actual-work
accounting remain requirements.

## Limit and next gate

The coordinator accepted these findings as design corrections in conversation.
That acknowledgment does not establish that any later draft implements them.
A hash-bound final brief and category/deletion plan should resolve the concrete
interfaces before authoring. No implementation fitness, performance, complete
coverage, cold CLEAN verdict or integration readiness is claimed here.
