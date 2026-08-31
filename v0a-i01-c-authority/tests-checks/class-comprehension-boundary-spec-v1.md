# Class/comprehension boundary witnesses v1

Engineering preregistration: six schedules and six harmless projections, with
2 required-clean, 3 required-refusal and 1 permitted-refusal cases. Root accepted
this table before any candidate or Model execution. The author has not inspected
the in-progress v23 candidate. This note authorizes no payload.

Frozen JSON: tests-checks/class-comprehension-boundary-cases-v1.json,
SHA256 9df895eb5bd645a5e4ef05be0f7c0a3db76df458ca023bbfbd36407ee3496b71.

Scope derives from engineer-class-name-boundary-addendum-v2.md
SHA256 de7b5417b2cc899710af0a32332360f31546b6264d1cb58896104a362568e93f,
class-frame plan3d57a76a1224db8312fcb614b218c58084753172f1f75aeb10df722033d56536
and ownership APIbf5cf20ac2174707e70eb73d73126a489d68b4c316467517aaf8b071a81b383b.
The retained source basis is v22
61a0ce3bc3ea59bc09a7b14d45da843fb3c3a8614feb4c913132b67028916da3;
no new candidate output determines these expectations.

| ID | Fixed boundary and polarity | Exact Model trace -> result | Classification |
| --- | --- | --- | --- |
| Q01 | Outer/class armed=False; class change(True); eager body reads armed | shadow, change, eager-start, read, write, eager-end -> TypeError | refuse |
| Q02 | Outer/class armed=True; class change(False); same eager body | shadow, change, eager-start, read, eager-end, sink -> fixed | clean |
| Q03 | Outer gates=(False,), class gates=(True,); outer armed=True, class armed=False | shadow, eager-start, read, write, eager-end -> TypeError | refuse |
| Q04 | Outer gates=(True,), class gates=(False,); same armed values | shadow, eager-start, eager-end, sink -> fixed | clean |
| Q05 | Outer/class/consumer armed=False; class creates generator, outer change(True), then consume | shadow, header, generator-created, change, consume, read, write, consume-end -> TypeError | refuse |
| Q06 | Outer/class/consumer armed=True; creation then change(False), then consume | shadow, header, generator-created, change, consume, read, consume-end, sink -> fixed | permitted-refusal |

Q01/Q02 use exactly [read(armed) for unused in (0,)]. The singleton list
comprehension is eager, its result is not consumed, and its body must skip the
class namespace while reading the current enclosing function cell. The class
shadow remains at the opposite value after change. Q02 is an ordinary bounded
eager/helper control, not a request for new collection-result precision.

Q03/Q04 use exactly [read(armed) for gate in gates if gate]. The outermost
iterable is evaluated in the class namespace. Its class-local gate determines
whether the implicit body is reached; that body reads the enclosing armed cell,
not the class shadow. Q04 requires no read or write event, so blanket refusal of
this dormant finite body is not accepted. Together with Q01/Q02 the pair separates
first-iterable context from implicit-body context rather than conflating them.

Q05/Q06 use exactly (read(armed) for unused in header(source)). Outer source=(),
but class source=(0,), so the header called at generator creation obtains the
class-local singleton. The enclosing armed cell is rebound after class completion
and before consume(Local.pending). The consuming helper also binds a same-spelled
armed local with the opposite value. Neither the class shadow, creation-time
cell contents nor consuming-helper projection is the generator's live free cell.
The harmless header event must precede generator-created/change/consume; read
occurs only after consume. tuple(work) fully consumes one finite item. The safe
case permits an explicit unsupported deferred/class-result refusal; no wider
clean precision promise is introduced.

All source cases share the existing fixed-argument ReviewTests._launch scaffold.
Sensitive source is AST-only input to a future real derive_design_review call.
Each separately authored Model has its own fresh namespace, event list and class.
Its sink only appends sink and returns fixed. Invoke Model().test_static()
and catch the final TypeError outside the method. Never execute sensitive source,
derive a runnable projection by sink substitution, or reuse the mutated Model
class between cases. Every unsafe read writes Model._launch=None and the method
later attempts the sink, so TypeError is an expected harmless oracle outcome,
not an infrastructure failure.

Required-clean means no public unresolved blocker and exactly argv [[-m, fixed]].
Required-refusal means at least one explicit public unresolved blocker; row loss
alone is insufficient. Permitted-refusal accepts an explicit blocker, otherwise
requires the same exact argv. Unsafe models have sink unreachable; Q02/Q06 have
write unreachable; Q04 has both read and write unreachable. Event append statements
are observation only and are removed solely for AST correspondence checking;
the sensitive source is never transformed into executable code.

The static correspondence record must establish: all six test_static ASTs match
after renaming Model to ReviewTests and removing event-appends; independent sink
bodies are checked separately; pair deltas are only the specified booleans;
class/outer declarations, helper effects, comprehension first iterable/body/filter,
generator creation/change/consume order, and event label/order assertions match
this table. Parsing is not execution and does not certify Python runtime behavior.
Root-owned actual3.11.15 then3.14.6 runs remain future evidence.

No descriptor/metaclass, TryStar, async, annotation/type-parameter, arbitrary
iterator, compiler-representation, optimization or new budget assertion is added.
No existing case, assertion, source, generated output or cap is changed. These
six witnesses complement the existing class-name and class12 packs; they do not
replace them or establish a general Python interpreter contract.
