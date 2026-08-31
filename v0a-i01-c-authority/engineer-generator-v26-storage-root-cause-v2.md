# v24 namespace failure: category diagnosis and v26 repair boundary

The v24 source156ee88a99abb26edeaaf178841c72e89f2bdc15696c37ef91f4dcc54b767431
is retained and rejected. Its first actual3.11.15 design53 run completed the
53-method population with137 failures and742 errors across subtests.
The root-run receipt is tests-checks/focused-v24-first01-design-311-receipt.json,
SHA c9e6cb1e958bc6a8e15f0989841e5a1562dc3682286c07e7a6b44b95ee9339e1,
exit1, integrity true. Its retained stderr SHA is
68ae7225a5d0377cc6e8d20a3d4fbfccecf7eb1b06d372ad346b30c24a7209e8.
This author read the first complete failure chain and independently hashed the
receipt; no payload was rerun.

## Mechanism and failed verification

Bootstrap reaches _ExecutionState construction, _NameVersion.empty, then
_NameVersion.__init__. At v24 line14614 the latter assigns self._name_history,
but its unchanged __slots__ string declares _history. It raises AttributeError
before normal analysis. _order has the same defect even when not reached first.

The port's source converter replaced every matching tokenize.NAME token. Python
uses that token kind both for global lexical identifiers and for member names
after a dot. The converter incorrectly renamed member attributes that happened
to share a spelling with global helper functions. Slot strings were correctly
untouched, creating an inconsistent object layout.

The canonical checker then applied the same incorrect token converter to the
reference. It established self-consistency of the transformation, not preservation
of Python binding roles. The passing static claim did not protect slot/member
semantics. This is an authoring and verification defect, not a radix cost finding,
interpreter mismatch or authority semantic issue.

## Category enumeration before repair

The complete primitive AST, all48 name-map spellings, all member attributes,
all string constants and all reflective getattr/setattr/delattr/hasattr/vars calls
were enumerated; the repair is not inferred only from the first stack line.
Mapped prototype member spellings are exactly:
- _history:5 Attribute occurrences, one Store and four Load.
- _order:12 Attribute occurrences, four Store and eight Load.
v24 has their17 corresponding incorrectly renamed _name_history/_name_order
attributes. Three exact member-name strings occur in the two explicit slot tuples:
_history once and_order twice. No reflective calls exist in this primitive.
Other mapped spellings do not appear as members.

The prototype symbol-table audit finds no mapped lexical identifier locally or
freely bound in an inner scope. Thus the mapped bare Name uses here resolve to
module definitions/constants; class/function declaration names and those global
references need namespacing. Attribute.attr, method names, parameter names,
keyword names and string literals do not.

## Authorized successor and independent static falsifiers

v26 is based on exact retained v24 and corrects only the17 Attribute token spans
inside the primitive region. Restoration uses AST Attribute source positions,
not a broad string replacement or another global token converter.
No algorithm, threshold, counter, adapter, class/authority semantics, test, cap,
external primitive byte or W file may change.

Verification uses a separate structural AST comparator that treats each field
according to binding role. It permits the declared renaming only for module-level
definitions and audited global ast.Name references. It demands exact member,
string, method/argument/keyword and other AST fields. The comparator must reject
v24 against the original41 definitions plus6 constants and accept v26.
It does not call the source repair function or reproduce its token edits.

An independent slot-layout check reads explicit __slots__ declarations and
dataclass fields, enumerates self member reads/writes/method calls, and checks
constructor writes against declared storage. It must expose v24's undeclared
writes and show v26's slot/member symmetry, including every unchanged member
sequence from the reference. Cross-helper attribute inventories must also match.
No complete arbitrary-Python object-model proof is claimed beyond these
statically enumerated primitive classes and their reviewed reference.

The new source, exact v24 delta, v22/r010 diffs, member/global mapping inventory,
slot checks, original-failing/new-passing static comparison and inverse byte proof
will be retained separately. Root independently inspects before any payload.
The existing helper1050/generator70/corpus cost questions remain unproven.

Static editorial correction: v1 said49 map spellings; the actual retained map has48.
No source, category membership or implementation instruction changed.
