# Indexed storage oracle release v1

Engineering oracle authoring only; not a cold review or a prototype result.
Author: codex/cold_review_a. All paths below are relative to
D:/Pontius-handoffs/v0a-i01-c-authority/tests-checks unless prefixed T/.

The released payloads are cursor-oracle-v2.py and
indexed-storage-extension-oracle-v2.py. No oracle or prototype payload was
imported or executed by the author. Root retains execution ownership.

| Artifact | SHA-256 |
| --- | --- |
| cursor-oracle-v2.py | 145fe1d59c48e23cdb426bcbe35edbecc3f941a81dc9780e8eeed849be5bc143 |
| indexed-storage-extension-oracle-v2.py | 95ee5d3dd2e31ffd7ea6ecdd2f5e2b05dddb15e5a5ef1aa70ba8820bd82d2381 |
| cursor-oracle-v2-from-v1.diff | f8cc79715d3c1a1edfe60891bb2432aedbfac33e64c9705a76649a0583d8635e |
| indexed-storage-extension-oracle-v2-from-v1.diff | b5f5da2133fc1a8b6e1fb31ea5d5806e1a58fa3efa5db870399e99e76c081f02 |
| indexed-storage-extension-oracle-v2-from-empty.diff | 5a7dbc1bd5562f2b1211e1ecccd5face122da1334f5c4569e165fc44138ad856 |
| indexed-storage-oracles-static-proof-v2.json | 8fddb6ca3fcaf432175aace69d1f7a3b7d8e4e1c7949ec3994ba53662ebed939 |
| indexed-storage-oracles-static-control-v2.py | add60d8526fe670b9718f6e804a9c796acf8be6fc7d0ca2c6e97560533ad44c0 |
| indexed-storage-oracles-static-v2-receipt.json | 3271ba45328f0f538a2fde553dc19bfefeb03774b5e5a540af3efe7a175f9bd5 |
| indexed-storage-extension-cases-v1.json | 795e893c4fbeee3963a3ea3cbbffdfacbea193f53063eb4848c8e9ac6d12984a |
| indexed-storage-extension-spec-v1.md | 11d11003b3ce84d485df549e73a494e358db69cc6f5db6faea5dae8f50c330f9 |
| indexed-storage-p-boundary-clarification-v1.md | cdc1f9aa5f66114d744e2bc66728f4a64f85032a7b25399a9c0a4c728cb28cb8 |

The existing storage oracle/case pack and cursor case pack remain byte-exact.
The proof records their full hashes. Cursor v2 retains all 24 overwrite and
publication operations and all old weak-reference assertions. Its sole behavioral
change replaces the layer-specific compaction trigger with completed changed
publications and direct ownership evidence. The new I11 adds the stronger
single-publication overwrite/delete retention witness. Old results and old
oracle bytes remain intact.

Indexed v2 retains v1 schedules, case data, value/order oracles, atomicity
calibration and all fourteen P/C growth comparisons. Its five exact substitutions
only add the I07 terminal-collision activation requirement and descriptive
metadata/version text. I07 must observe actual declared hash-width terminal
work as well as hash/equality/dictionary-attempt evidence; otherwise it reports
an unmet structural precondition. I06 requires actual closed-domain dictionary
collision work without requiring a terminal node. Atomic I12-I16 report terminal
activation without imposing an extra target-node requirement: their frozen
contract is changed mixed-key data/order, exact retry and continuation equivalence.

Entrypoints:

- verify_cursor(api, case_path=...): unchanged signature; 16 cases / 28 runs.
- verify_indexed(api, case_path=..., accounting_path=..., accounting_sha256=...):
  16 cases / 31 runs, including five pristine-plus-three-fault schedules.
- The existing independent storage phase remains 28 cases / 34 runs.
  Combined planned population is 93 runs per child.

The indexed module requires its sibling filename
indexed-storage-extension-spec-v1.md. The case path is explicit. Accounting
bytes must hash to the supplied approved hash and name the loaded prototype
source hash. The agreed accounting is T/engineer-name-radix-accounting-v1.json
SHA79f64e5e7bbb429bedd108654b69c8ab5893973ee742517b543129f762f68f2b,
bound to T/engineer-name-radix-prototype-v1.py
SHA0c4e9ae2bef9b5489cc00f11adb5dd3400be6f6d5ea90537fb5951bba8ba1a71.

Both summaries retain all_completed, failures, planned_cases, planned_runs,
completed_runs, case_pack_sha256, runtime, hash_seed and maximum_meter_limit.
Indexed additionally emits accounting_sha256, prototype_sha256,
accounting_complete, fitness_passed, semantic_runs_completed (boolean),
growth_comparisons and fitness_failures. Incomplete or failed growth cannot
produce successful fitness. A budget refusal, semantic/oracle failure,
accounting failure and unmet structural precondition remain distinct outcomes.
Partial events survive failure. Every phase and full original Meter charge is
reported; key protocol observations are separate, uncharged evidence.

The P classification was resolved and accepted before any results: fixed-arity
wrapper fields remain non-P; variable-cardinality stored references/entries are P.
Full C independently includes every charge and has its own unchanged growth gates.
Only the four specifically requested accounting source-site definitions were
inspected by this author; expected outputs were not derived from the prototype
algorithm. Runtime oracle code uses public storage APIs only.

Static validation used actual 3.11.15 with -I -S -B -P, optimization off,
scrubbed environment and D-local cwd/temp. It parsed ASTs/data and checked hashes,
not payload behavior. It completed exit0 with empty stderr. It proves exact
cursor definition preservation outside retention/summary metadata, preservation
of original retention call ASTs and assertions, unchanged case populations,
the indexed v2 five-substitution delta, unchanged atomic/growth definitions,
UTF-8 LF bytes and absence of dynamic execution/process imports in the indexed
module. It does not establish runtime correctness, fitness or release approval.

Infrastructure history is retained honestly. The v1 static core emitted valid
proof/diffs, but its outer PowerShell pair-array log writer failed afterward.
The resulting five-byte null receipt SHA38e0b9de817f645c4bec37c0d4a3e58baecccb040f5718dc069a72c7385a0bed
is invalid and must not be counted as a successful run receipt. The v2 static
proof binds that predecessor failure and fresh valid receipt. No source payload
ran during either static check. A later oversized authoring command was rejected
before process creation; the same narrow substitutions were then applied by
a small create-only script. No issued artifact was overwritten.

All released oracle, case, diff and proof bytes are now immutable. This handoff
does not authorize W integration, production tests, corpus generation or payload
execution. Root reviews and dispatches the separately pinned isolated controller.
