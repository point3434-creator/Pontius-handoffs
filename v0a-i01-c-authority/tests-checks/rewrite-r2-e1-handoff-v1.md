# R2-E1 four-case harness handoff v1

Author: codex/cold_review_a, engineering input/harness author, not a cold reviewer. This handoff authorizes no payload, candidate, Model or sensitive-source execution. Root owns freeze, configuration, dispatch, evidence adjudication and any source repair.

## Frozen scope and source

- Authoring: H 4bb64a2c06900a57a40785df09a6bf7d0c66ddd9; preparation manifest e27d2466d3326473a457f49984c5058886047410ab0343a27dd1057f796003da; controlling finding/preparation effe5454d347cf2a42dbc90e913a2f2be0e5adb31acf91c2495c58b9877dc50c.
- Held candidate: H beff8193e9d5ce7316f5006fccc77ffcb5ca5695; source manifest ef3561cb462fcbd31dda7d3774ea34d00c575b7549dc1cc804ad9f92e11c582b; retained source SHA 7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d.
- Frozen inputs: H ed837198d2c83757bfb74d962af244c33f0aeae6; input manifest a45941376da823672808050182e151f22520167d6cb24a8a9947e7b2a6c4f45e; independent input review 60d25798393411a5ce9edb4818a5d74b1c873f2a0ad5a839352a1cbfa86cfe05.
- New four-case family is independent of the unchanged fixed twelve. E01/E04 require clean exact argv; E02/E03 require an explicit blocker. Override cases may retain rows. Identity input supplied only the exact sink statement and public invocation envelope; it had not itself passed public analysis.

## Issued immutable inputs

- rewrite-r2-e1-cases-v1.json 59b8457a2323634d883fb2c9b0ff82a1e60cd980c5f2a4b50e627c8ca32cdb9b
- rewrite-r2-e1-spec-v1.md 4fcb92ed30a86be1664d9b1981e5e8dc8c47d5d76eaab7b08dc09db74abc9f11
- rewrite-r2-e1-source-differences-v1.diff a879d595fe18fd76abf7640464d37da983579061a471ea6b23df1a2fb694c76c
- rewrite-r2-e1-source-model-map-v1.json 171f76c7532ae5ef24e279892110b9afdcbb56660951d8c85d9bfd31270f68fb

The sensitive source is parsed and passed only to derive_design_review; it is never executed. The only future executable oracle input is each separately authored process/file-free Model. The probe requires types.FunctionType, exact globals/captured-builtins identity, no closure/free variables, and externally records NameError.name == ValueError.

## Issued immutable harness

Current pair:

- rewrite-r2-e1-probe-v1.py 7ac823d560034a140275d2447bf68bbe1f98adc8c250e61d46aedada018656a3
- rewrite-r2-e1-control-v2.py c76a6e170062094986e7cdea90ad8e2e7737da2d38657c6f604da8eb86417ec0

Supporting review:

- rewrite-r2-e1-probe-from-late-store-v1.diff fbedd43d3fa92568ff5b58575dc54ed3693b12fdbfa017f4caebecd7d53e0de5
- rewrite-r2-e1-control-v2-from-late-store-v1.diff 0c2dde5548b63533b83ba1fbc44c1202031e46892984703b459a99a0ed3c6883
- rewrite-r2-e1-control-v2-from-v1.diff 3e68cbb51ee1ec55b18e7050838b211a498a34fd956690829b2e173a0c76560d
- rewrite-r2-e1-harness-static-v2.json cfaba853c18c420536ba066a03569045fd73a56eaa77cbbd4720746a8875caec

Immutable unexecuted predecessor rewrite-r2-e1-control-v1.py is 09f9fccdca6790d9299c49692eb78f2440206393261994d4df1fe35621e00336; its v1 static map is 73246b42a82a8cbf113c7507ad47be1f51365a43f8e7794c2cc57560b5c53308. V2 changes only validate_result and its two call sites: live and floor replay require exactly six nonempty stdout lines, every line a JSON object, and empty stderr. Failure-path partial-record collection remains best-effort; raw stdout/stderr/log remain retained.

Static-only self-review parsed every script/source/Model AST, checked all four context-operation shapes and public envelope serialization, and proved raw equality of the inherited probe custody helpers and ten controller custody helpers. V1-to-v2 AST changes are limited to validate_result and main; both validator call sites supply stdout and stderr. No probe, controller, candidate or Model was imported or executed.

## Custody and gate

Controller use, only after root freeze/review:

actual311 -I -S -B -P rewrite-r2-e1-control-v2.py LABEL 311 RETAINED_SOURCE_ABSOLUTE SOURCE_SHA --control-sha256 c76a6e170062094986e7cdea90ad8e2e7737da2d38657c6f604da8eb86417ec0

It creates a fresh exact-r010 1761-file D-local snapshot, overlays only the retained source, checks the explicit W copy against the same caller-supplied source digest, watches protected16, and runs the child with -B -P, scrubbed environment, snapshot src PYTHONPATH, seed0 and a 60-second infrastructure watchdog. Full public result/receipt bytes are retained and rehashed; rows, blockers and argv are re-derived from them.

A complete semantic RED on actual3.11.15 is evidence but does not unlock actual3.14.6. A separately authorized repaired candidate must first produce a complete, integrity-clean, semantic GREEN floor receipt with exit0; development must use identical source/probe/control/pack/spec/watch pins and independently revalidates the floor snapshot and raw records. Timeout, oracle/analyzer error, malformed output, custody failure or pre-launch output-stream failure is infrastructure/incomplete, never a product result. Pre-try stream acquisition can leave partial files without a receipt; it cannot yield success.

These files are issued immutable workspace bytes and were not committed by this author.
