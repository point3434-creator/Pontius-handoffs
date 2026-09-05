# r002 FIX coverage planning (deferred reviewer input)

This is the pre-correction claim, not a verdict or a complete-input proof.
Rejected candidate: 6fb7f840d31d946e6b5dcb45faf82939dafd46ec.
Discovery inputs: the adopted API/schema/source-opening acceptance criteria,
both independent r001 reports, the exact record definitions, source origin and
graph predicates, and the complete registered tests. Update this claim explicitly
if implementation discovery adds or excludes members; freeze final evidence in
r002/coverage.md. Do not include its contents in initial cold reviewer inputs.

## Failure category and related paths

1. Exact-population source registration: module-name classification and path
   classification disagree for a flat file at the package import name. Inventory:
   the two permitted package files, flat blueprint_artifact.py, undeclared package
   descendants, codec forbidden imports, legacy-to-codec imports, plus the exact
   existing driver origin and three approved edges and its related negatives.
   The decisive check is actual check_repository against a disposable filesystem,
   not just a predicate or graph helper. Reproduce flat acceptance on r001 before
   the production edit and retain integrated refusal on the corrected candidate.

2. Typed malformed-graph refusal: exact-class checking does not guarantee required
   slots are present. Inventory: source, entry, key and action required fields;
   incomplete records reached after an earlier valid entry; malformed populated
   values and foreign subclasses. Check public encode raises BlueprintArtifactError
   for absent fields without invoking foreign hooks or producing partial bytes.
   Reproduce missing-slot AttributeError on r001 before the production edit. Keep
   resource errors outside the translation promise.

3. Missing independent durable acceptance evidence: inventory the complete 17-key
   history fixture graph and its action, all four artifact entry action labels,
   missing/unknown action members, and numeric scalar/vector/history/action
   integer families at 10**640-1 and 10**640 through decode and exact-source encode.
   Derive expected values from handwritten fixtures and existing value contracts,
   not a codec round trip. These are coverage corrections; passing new controls
   on r001 is legitimate and must not be represented as a behavioral RED.

## Limits and falsifiers

No general serializer, arbitrary-object traversal, runtime mutation, new boundary
family, analyzer inference repair, capability grant or dependency is in scope.
All original positive controls, real runtime/replay outcomes and source/test/
fixture/manual-registration budgets remain binding. Existing tests may be
consolidated only without removing required independent behavioral assertions.

The claim is falsified by an undeclared family path passing the public gate, an
admitted exact record missing a required field escaping the typed refusal, a
foreign hook invocation, or a required schema/numeric family still lacking a
durable independent public-operation assertion. This finite inventory does not
claim exhaustive malformed-Python-state, filesystem race or resource coverage.

Final coverage must cite actual RED, GREEN and positive acceptance receipts,
all limits, discovered changes and measured budgets; no pass is asserted here.
