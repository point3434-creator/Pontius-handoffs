# v26 storage namespace correction: handoff v1

Candidate ready for coordinator inspection. No payload/import/run configuration,
W mutation, test change, cap change, semantic-v25 merge or algorithm tuning by
this author. Rejected v24 and every earlier artifact remain intact.

All paths are D:/Pontius-handoffs/v0a-i01-c-authority.

- engineer-generator-v26-storage.py,1,150,303 bytes:
  1f908957ee43d5841f8da09e306bd52dc5efeca9609a5d522e76df22b4dcd951
- engineer-generator-v26-storage-from-v24.diff:
  838433dd56ce774bf52111978880a13a2a9f658ec34a13e6241e4dd2d54df2b5
- engineer-generator-v26-storage-from-v22.diff:
  b0e89337d8f58f26419c40f6691ac0392f593fbf95b7b85dfb3b4ead5ddd426d
- engineer-generator-v26-storage-from-r010.diff:
  9e91dca503ba9029c3d8887d376670e44fb6d1e0a4defce07de74e561255b8e4
- engineer-generator-v26-storage-binding-map-v1.json:
  e024329a9dcae92c22b3185f62543bbcd1ec535cbfdf5aba01e930fd67f22d10
- engineer-generator-v26-storage-static-v1.json:
  d30ab3307f7dc11ce978ac045beaca676868000b3d795ab88b31d3a8cf1e2e71
- engineer-generator-v26-storage-root-cause-v2.md:
  5a9bc09b1c9f1efef728e084924e5346afa0b55a3478cff25e936f9dd4ec0e60

Root-cause v1 remains; v2 corrects only its editorial map-count49 to the actual48,
with that correction disclosed. Category membership was always the same17 members.

The defect was in the port and its verification: tokenize.NAME replacement
renamed Attribute member names sharing global helper spellings. The old verifier
repeated that transformation and therefore accepted the same error. The new code
restores only17 AST Attribute spans:5 _history and12 _order occurrences. Global
helper names remain namespaced. No slot string, reflective string, other token,
counter, argument, algorithm or adapter byte changes.

The separately implemented AST comparator checks fields by semantic role:
module definitions and symbol-table-confirmed global Name references may rename;
Attribute.attr, Constant.value, method/parameter/keyword names and all remaining
AST fields must match the original prototype literally. No mapped identifier is
locally/freely bound in an inner prototype scope. This comparator rejects v24
with17 attribute mismatches and accepts v26's41 definitions plus6 constants.
It does not use the Attribute-span source rewriter.

An additional independent slot inventory reads explicit slots or slotted-dataclass
fields, checks every self member read/write against data/method declarations,
and checks explicit constructor writes cover the slots. It rejects v24's
_NameVersion and_NameCursor; all10 primitive classes pass for v26 and their
complete member inventories equal the prototype. Every helper's complete member
and constant sequences also equal the prototype. The three mapped slot strings
remain exact, and there are no reflective calls in this primitive.

Literal inverse restoration recovers exact rejected v24. Every byte outside
the primitive, including all v24 bulk producers, transfers, cell writes, charges,
class/exception semantics and caps, remains exact. All1761 tracked W paths were
hashed before/after and stayed unchanged; W remains v20.
Only static parse/compile-without-exec, symbol analysis, hashes and comparisons
were run by this author.

The coordinator's first floor design53 receipt supplied RED; there is no new
payload test population or claimed runtime GREEN. Root may now inspect the
17-member delta and dispatch the same retained design53. The supported-workload
budget and semantic questions remain for actual execution, not this static proof.
