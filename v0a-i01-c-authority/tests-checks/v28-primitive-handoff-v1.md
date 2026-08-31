# v28 primitive harness source handoff v1

Author: codex/r010_cold_a. Engineering authoring only; no payload run, cold verdict or execution authorization.

The retained production primitive is ready for root source review. The plan is v28-primitive-plan-v1.md (b9948d186f89e313f5eae829ab9fa4081f03b3260d4bb8f97237d70b4fbdd2ba). All files below are in tests-checks unless stated otherwise.

| Artifact | SHA-256 |
| --- | --- |
| v28-primitive-control-v1.py | 64fcb3ef0aaaf57f63643b3e306fe0f0b65f47c4d5ba8c5fc107dbe68186fcac |
| embedded wrapper (UTF-8 literal value) | a9dfcd8790ab63c9d4a5e3276074633d6e7b765650587e2bbe2b69c357f6a5c5 |
| v28-primitive-extractor-v2.py | 96f3e980751e0d4851b95340e894c9519b96241fc726d1fac30d324fd99d6d9f |
| v28-primitive-extracted-v1.py | bad767aab3b330666fbc4543224e28347a8cf93f8f69d5940c618737dbea2778 |
| v28-primitive-accounting-v1.json | 4592e93634857015cd2befa227e7483db1b00895117881d919e6b0508cfa95ca |
| v28-primitive-extraction-proof-v1.json | 8b6269d44aecaca6a4df93947439e0f54090b4dedb673a6574c5781e580d6c45 |
| v28-primitive-harness-static-v1.json | d988339dc7f1504bb56e86c7b334eb3cdf2efbfccc8587370b1ff6092174ad5a |
| v28-primitive-control-v1-from-indexed-v4.diff | 033718be75dae809213fbffa4804f8dc62fe57d632967116d798bad73a6988e2 |
| v28-primitive-extractor-v2-from-v1.diff | 9e1aa403638b9ff19ad91ca5cb0e8239ddf696b051d99810c2bf442534309aef |

## Provenance and static result

The subject is T/engineer-generator-v28-storage.py, 4db6502350e59fe363998351384a62d9e669598241a644810e9a7ffd6b4b4d0e. The verifier independently lists all 41 primitive definitions and six constants, compares that list to the pinned production binding inventory, copies the exact production source segments and asserts full AST equality for every node. All 47 source segments and ASTs match; attributes, slots, locals and production global spellings are untouched. The namespace map is identity. Public aliases restore the old oracle API without changing the classes or function bodies.

Only future/import nodes, MAXIMUM_WORK=262144, BudgetExceeded and Meter are copied from the exact original prototype 0c4e9ae2bef9b5489cc00f11adb5dd3400be6f6d5ea90537fb5951bba8ba1a71. _NameMeter is a test-support alias. Its production adapter is not imported or copied. Global symbol-table closure has zero unresolved references. The extraction contains no _ExecutionState, resolver, _AnalysisBudget, test or sensitive fixture body.

The 213 literal charge categories are exactly the original 197 plus the declared sixteen A categories. Prior metric/operation classifications are unchanged. The accounting file points to the exact extracted-file SHA for compatibility with the unchanged oracle API, and separately binds the production subject, production accounting and support reference. Original per-site source line metadata is not used as a metric classification; full charge-site/units AST inventory is in the extraction proof. Unknown or unclassified categories fail before execution.

AST schemas differ between Python versions. The child reruns full production/extracted AST equality using its own parser; it does not normalize either side. Extracted module and accounting bytes must regenerate exactly. Runtime-stable claims and source-segment inventories must match the retained floor proof. Full AST-dump hashes and symbol-table references may differ across interpreters and are not incorrectly treated as cross-runtime byte identities. The child emits the current runtime proof hash and retained floor proof hash separately.

## Exact prior obligations retained

No oracle, case, spec, Model, threshold, fault offset or expected result changed. The byte-pinned phases are storage28cases/34runs, cursor16cases/28runs and indexed16cases/31runs, totaling93 runs in one selected child. All seven prior oracle/case/spec pins were rehashed against the original approved config. Existing primitive retention, real fork snapshots, exact builtin legacy set-union order, collisions, operation atomicity, retry cost equality, continuation equality and finite P/C inequalities remain binding.

The old 558 checks are not evidence for v28. New freeze category presence is not coverage proof; actual new-category counts must establish which changed paths ran. Unexercised branches must be reported without adding cases or relaxing assertions.

## Root-owned config and dispatch interface

No config or snapshot was created by this author. Root must review the controller, verifier, extraction, accounting and proof, then create and pin a new config. It uses the predecessor config fields plus the eight entries in controller EXTRA_INPUTS. Set schema to v28-production-primitive-control-v1 and control_sha256 to the exact controller hash. Replace prototype/accounting with FROZEN_DERIVED entries; cursor/indexed oracle entries are additionally fixed in that mapping. Leave original old-oracle/cases, successor/extension case/spec pins and 16/28,16/31 expected counts unchanged. The historical radix disposition is retained as provenance; it does not itself authorize this new run.

The CLI retains LABEL SLOT SEED CONFIG_RELATIVE CONFIG_SHA256, adding FLOOR_RECEIPT_RELATIVE FLOOR_RECEIPT_SHA256 only for314. One invocation creates one disposable snapshot and runs one explicitly selected slot/seed. No automatic six-child expansion. The controller itself requires actual3.11.15 and -I -S -B -P. A314 child additionally requires a successful matching actual311.15 receipt for this same control/config/source/extraction/accounting/cases/seed, with raw-stream/setup/snapshot replay. No diagnostic RED or incomplete predecessor qualifies.

Output family: tests-checks/v28-primitive-LABEL-SLOT-seedSEED-{setup.json,receipt.json}, plus .stdout.txt/.stderr.txt/.txt. Fresh snapshot root prefix is D:/pontius-snapshots/v28-primitive-; payload directory is .storage-v28-primitive. Exactly1761 tracked r010 files remain untouched. The complete manifest covers1782 files forfloor (1761+21) or1787 fordev (+5 copied floor-evidence files), excluding the separately hashed manifest itself.

Before any payload import the bootstrap validates actual executable/patch, flags, exact scrubbed environment, seed, snapshot/PYTHONPATH/Pontius origin, and complete manifest. It emits identity, loads only the static verifier, checks regenerated extraction/accounting and proof, emits static_extraction_verified, and only then imports the extracted primitive and unchanged oracles. Full candidate and support reference are AST-only inputs; neither full module is imported. The public primitive itself runs only after root dispatch.

The predecessor absolute validated Git, D-local temp, no-Pontius-import guard, seed0/1/17 domain, 60-second owned direct-child watchdog, failure/raw-output retention, complete before/after snapshot/input hashes and W watch remain. W watch is explicitly v20 e61b3a067c67fe35e120ecfbb70f40606e737e4a03a607df94db3afb0c2dd679, independently of the v28 subject. The control preserves eleven parent function ASTs exactly; the main/bootstrap delta and new extraction-record validation are in the raw diff.

## Authoring history and limits

Only actual311.15 static authoring scripts ran with -I -S -B -P. They parsed code and created/compiled source without executing extracted or sensitive code. Extractor v1 stopped before output creation because it compared old source_sites metadata against a selected metric/operation dictionary; v2 compares the intended exact fields. Controller-author v1 stopped before output creation because its mechanical replacement guard expected five record-key occurrences while the source contains seven; author v2 changes that guard and then completed. These are retained authoring infrastructure errors, not product REDs. Both predecessors remain immutable.

No dev execution, primitive import, oracle invocation, analyzer invocation, test, broad wall, owner/GPU action, source edit, ledger mutation or commit occurred. This harness assesses primitive A. Production meter integration, constructor B, helper/cell authority and whole-corpus affordability remain outside its result.
