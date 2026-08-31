# Class/comprehension extension R01–R08 v1

Author: codex/cold_review_a, engineering witness author; not a cold review.
Root approved this fixed eight-case table before any extension payload or
candidate repair. The author inspected frozen v23 to discover the source
mechanisms; these expectations come from the Python schedules and independent
harmless Models, not from extension analyzer results. No extension result has
been opened and this specification authorizes no execution.

Case pack: tests-checks/class-comprehension-extension-cases-v1.json
SHA256 eb5551c054fc89da28fd2e4db433f56f7a3dbbd4cdb70509070a89fe362c74fd
Source basis: engineer-generator-v23-semantic.py
SHA256 53a17d52196bd83a540ebf4892d3687f3efbe9633d1539fa834ea0a27f0db499
Engineering source note:
class-comprehension-v23-engineering-review-codex-a-v1.md
SHA256 84461f44efa2da40cfc8729a0d80eb45c0266e4e88a67d88d9d7703c955d44cc
Accepted class-name addendum v2:
de7b5417b2cc899710af0a32332360f31546b6264d1cb58896104a362568e93f
Original comp6 pack remains byte-identical:
9df895eb5bd645a5e4ef05be0f7c0a3db76df458ca023bbfbd36407ee3496b71

There are exactly 8 schedules and 8 independent Model projections:
4 required-refuse, 3 required-clean, 1 permitted-refusal. All sensitive programs
use the existing fixed ReviewTests._launch scaffold solely as AST analyzer input.
Models are separately authored source, not runnable rewrites of sensitive bytes.

| ID | Fixed mechanism | Classification | Exact trace -> result |
| --- | --- | --- | --- |
| R01 | owner._launch target, singleton None iterable | refuse | eager-start, target-completed, eager-end -> TypeError |
| R02 | same target, empty iterable | clean | eager-start, eager-end, sink -> fixed |
| R03 | owners[index]._launch target, singleton None iterable | refuse | eager-start, target-completed, eager-end -> TypeError |
| R04 | same indexed receiver target, empty iterable | clean | eager-start, eager-end, sink -> fixed |
| R05 | two class generators, nested joins with an ordinary generator, outer armed=True | refuse | ordinary-created, class-a-created, class-b-created, first-join, second-join, consume, read, write, consume-end -> TypeError |
| R06 | same joins, outer armed=False | permitted-refusal | ordinary-created, class-a-created, class-b-created, first-join, second-join, consume, read, consume-end, sink -> fixed |
| R07 | class generator over empty list, append then full consumption | refuse | generator-created, append, consume, read, write, consume-end -> TypeError |
| R08 | same empty list and full consumption, append branch skipped | clean | generator-created, consume, consume-end, sink -> fixed |

R01–R04: owner is the protected test class; owners is a singleton tuple containing
that class and index is zero. The comprehension target is an Attribute whose
receiver contains Load names, not a local Name binding. The emitted helper is
called only after the target assignment succeeds. Its Model event
target-completed therefore proves that Python reached the store before the
element expression; it is not an analyzer observation. The surrounding
except NameError must be unreachable in all four Models. It deliberately catches
an analyzer-invented UnboundLocalError if receiver/index loads are incorrectly
masked as comprehension locals. Empty iteration evaluates neither receiver/index
nor emitted. Unsafe programs overwrite the sink with None and the final attempt
raises TypeError; no subprocess or other external operation occurs in the Model.

R05–R06: benign=(0 for unused in (0,)) is created in the enclosing function before
the class. Both a and b are created inside class; their bodies use the enclosing
armed cell despite the class's armed=False shadow. The first conditional selects
a/b, and the second selects that result/benign. left and right are ordinary test
class attributes set to True in both sensitive source and Model, so the concrete
projection consumes a. They remain ordinary receiver attribute reads for public
analysis; no private joined-state assertion is imposed. Both nested conditional
expressions remain in the fixed source, so any analyzer abstraction that joins
them must retain all alternatives. Consumption is list(chosen) inside class:
Q05's class-completion/member carrier is not a prerequisite. R06 explicitly
permits a refusal for this unsupported deferred class path; no new clean precision
promise for mixed generator results is introduced. This pair does not claim
exhaustive branch-polynomial or all selection-order coverage.

R07–R08: items starts as the same empty list object used to create the generator's
first iterator. The class's grow constant controls a single append after
creation. The class armed=False shadow differs from the enclosing armed=True
cell read by the real implicit body. tuple(pending) is inside class in both cases.
When the list grows, the previously created list iterator reaches the appended
element and the body writes the sink. When it does not grow, full consumption
is empty and read/write remain unreachable. This is an initially empty iterator
identity/epoch schedule, not merely rebinding the iterable name or consuming a
different collection. R08's clean requirement prevents blanket marker refusals.

For all cases, source and Model test bodies must have the same AST after removing
only Model event-append expression statements and renaming Model to ReviewTests.
Class-level left/right values are also matched. No semantic substitution is
performed to obtain executable Models. Each Model uses a fresh namespace/class
and event list; invoke Model().test_static() once and catch only the final
TypeError outside the method. NameError is available to the explicit target
handler; an uncaught NameError or any other unexpected oracle exception is an
oracle/infrastructure error, not a valid product RED. The only Model builtins
needed are __build_class__, staticmethod, tuple, list and NameError. Model sources
contain no imports or file/process/network capabilities.

Required-clean: no public unresolved blocker and exactly argv [[-m, fixed]].
Required-refuse: at least one explicit public unresolved blocker; merely dropping
a row is insufficient. Permitted-refusal: an explicit blocker is accepted,
otherwise exactly the same fixed argv is required. All unsafe Models have sink
unreachable. JSON expected traces and unreachable_events are binding and cannot
be rewritten after results.

Static copy inventory, not extra executable cases:
- Same-identity generator merge at v23:13749–13795 uses replace(first, ...), not an
  explicit OR of class_scope_unresolved. Existing identity=id(expression) may make
  the marker invariant among reachable states of that expression. A repair must
  preserve/prove this invariant or the marker disjunction, but this pack invents
  no private mixed-flag state and counts no RED for it.
- Native collection shape poisoning and subsequent extraction remain a related
  unexecuted marker-carrier risk from the engineering note. It is not smuggled
  into these eight cases and no native-result precision claim is added.

Future execution remains root-owned: retained candidate path plus exact SHA,
fresh D-local exact-r010 snapshot with permitted overlays, actual 3.11.15 first,
then matching completed/intact same-candidate 3.14.6 replication; -B -P,
scrubbed seed0 environment, snapshot cwd/src, D-local temporary path, validated
absolute Git, original caps, 60-second direct-child watchdog, and retained raw
stdout/stderr/log/manifest/receipt. An intact semantic RED may be replicated;
oracle, analyzer, custody or incomplete failures cannot satisfy that gate.
No guarded/GPU/owner/broad payload, candidate edit, W test edit, ledger or commit
is authorized by this specification.
