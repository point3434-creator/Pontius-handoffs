# Indexed-storage P boundary clarification v1

Pre-result clarification of indexed-storage-extension-spec-v1.md
SHA11d11003b3ce84d485df549e73a494e358db69cc6f5db6faea5dae8f50c330f9.
No payload has been executed. This clarifies the wrapper/content boundary;
it changes no case, N value, growth factor, operation, semantic expectation or cap.

P counts variable-cardinality indexed/name content events: backing entry
visits/copies, stored map/name references, child tuple/list references, and
pending/history/order name entries. Each physical event is classified once.

Fixed-arity instance-field installation is wrapper metadata, non-P, even when
one field refers to content. Therefore these existing accounting categories
remain non-P:
- entry_reference_copies: Entry(value, no_work), two fixed fields;
- radix_leaf_field_reference_copies: leaf(proxy, pending_names), two fields;
- radix_branch_field_reference_copies: branch(bitmap, child_tuple, pending_count),
  three fields;
- history_reference_copies: history(parent, changes, depth), three fields.

Installing a wrapper's pointer to a child tuple differs from visiting/copying
each child reference in that tuple. The former stays non-P, the latter is P.
Likewise dictionary-operation attempts are separate from their explicitly
charged content-reference copies; do not double count the same event.

ALL fixed-field charges remain in full C and its independently required8x/6x
growth comparisons. P is not claimed to count every machine pointer assignment,
all memory allocation, or opaque C dictionary probes.

This classification was resolved with the coordinator before any result.
Only the four requested source charge sites were inspected, at prototype
lines67,163,322/365,778; no algorithm review or result informed the expected
case outcomes. Prototype SHA0c4e9ae2bef9b5489cc00f11adb5dd3400be6f6d5ea90537fb5951bba8ba1a71;
accounting SHA79f64e5e7bbb429bedd108654b69c8ab5893973ee742517b543129f762f68f2b.
The root-reviewed accounting map remains the exhaustive source-bound category
classification supplied to the oracle. Unknown categories cannot silently
contribute zero P.
