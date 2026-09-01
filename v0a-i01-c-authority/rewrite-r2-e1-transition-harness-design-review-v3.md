# R2-E1 transition harness design review v3

Status: metadata-only successor to `rewrite-r2-e1-transition-harness-design-review-v2.md` SHA-256 `093b377758e918cbf021f5d7c3ad43538fb63d5a9fbbac1298f44953b27ea125`. V1 and V2 remain immutable. V3 changes controlling input pins and corrects lineage metadata only. It makes no harness, adapter, oracle, custody, internal-receipt, or RED/GREEN semantic change from V2.

Lineage finding: V2 correctly bound the v4 pins and correctly used the narrowed CPython 3.14.6 import citation `L2942-L2951` in its interpreter-source section, but its v4 summary incompletely described v4 as adding only T01/T02 route requirements. V4 introduced two metadata changes: those route requirements and the citation narrowing from `L2941-L2951` to `L2942-L2951`. Controlling v5 fixes that lineage description and preserves the narrowed citation. This is a documentation-lineage correction, not an executable-design finding.

Verdict: retain the V2 harness design exactly and bind its future implementation to controlling v5. Use a new owner pair built as a narrow successor to E1 v2; do not rewrite the custody shell. No Model, sensitive source, analyzer, candidate, harness, adapter, oracle, or controller was executed during this review. No governed artifact was edited. Only this create-only coordinator memo was added; H and source remain untouched.

Current controlling v5 pins:

- Pack `946457a644ab777e3c0a66e84c5f942740cec027d03500582ff31b300c16d427`
- Spec `0851471493a93845668cb39d9e6a5d4584688d505a86a87cd7a63df69162243a`
- Static map `0b0dddca5b661ef2622ec79554c7005bffeb60a24561cb44324796081ab7b241`
- Source differences `c393c7b5ecf1e6cad0e753e89e00be1058e4b8c03dea95e8770c60b8b651270a`
- V5 handoff `9a8aadb05251a0ceb84e9fa1d833be4ab7b1350d86183022a20654fc2545cfd9`
- Governing design `eaeb65d775857c229c509b430bf3eeb187bc058e79e27cda2a1b4a17cab74845`
- Held source `7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d` at H `beff8193e9d5ce7316f5006fccc77ffcb5ca5695`, manifest `ef3561cb462fcbd31dda7d3774ea34d00c575b7549dc1cc804ad9f92e11c582b`

V5 changes no governed source, harmless Model, public classification, module-key phase, trace, required argv, exception expectation, public-envelope byte, route requirement, or category-closure contract from v4. It carries the correct v4 lineage and exact 3.14.6 import citation.

Recommended new files remain:

- `rewrite-r2-e1-transition-probe-v1.py`
- `rewrite-r2-e1-transition-control-v1.py`
- Schema `pontius-r2-e1-transition-harness-v1`
- Payload `.rewrite-r2-e1-transition`

## Exact seven-record contract

The child stdout contract remains exactly seven nonempty LF-only JSON-object lines, with empty stderr:

1. One pre-import identity record.
2. T01.
3. T02.
4. T03.
5. C01.
6. I01.
7. One final summary.

Reject malformed JSON, scalars, blank lines, extra records, reordered records, CR bytes, or any stderr. Require exact outer record-key sets.

Each case record must retain the frozen case metadata, full oracle observation, analyzer error, full public result, full receipt, projected rows/blockers/argv, transport hashes, semantic result, and its category-route diagnostic. The controller must independently rederive all projections.

## Oracle and identity contract

The oracle observation must contain only serializable identity facts, never `id()` values:

- Exact trace, result, and exception.
- Exception always records `type`, `name`, and `message`.
- Pre-call and post-call module-key observations:
  - `present`
  - `is_outer_expected` or `null` when absent
  - `is_inner_expected` or `null` when absent
- Outer function facts before and after:
  - exact `types.FunctionType`
  - `__globals__ is _context`
  - `__builtins__ is _outer_builtin_context`
  - no closure/free variables
  - same function/context/builtins relationships after the call
- Inner capture facts after the call:
  - exact count
  - exact FunctionType
  - globals identity
  - expected builtins identity
  - no closure/free variables

The key-object assertions remain derivable from the pinned Models and belong in the reviewed harness:

- T01: absent before/after; outer and inner both capture the same empty dictionary.
- T02: present before/after; key value is the inner empty dictionary and differs from the outer standard dictionary.
- T03: present before; key value is both outer and inner expected because they alias the standard dictionary; absent after.
- C01/I01: absent before/after; outer captures the empty dictionary.

T01-T03 must each retain exactly one captured inner function. C01/I01 must retain zero.

Catch ordinary `Exception` outside `_function`. An expected exception is oracle evidence; setup, identity, or Model-structure failures are oracle errors. Do not catch `BaseException`.

For exception adjudication:

- T01/T02 require exact `NameError` and `.name == "ValueError"`. Record the message, but do not gate it because v5 preserves the v4 expectation without that field.
- C01 requires exact `NameError`, `.name is None`, and message `__build_class__ not found`.
- I01 requires exact `ImportError`, `.name is None`, and message `__import__ not found`.
- T03 requires no exception.

Only the pinned harmless Model may be compiled and executed. Sensitive source remains AST-only and is passed as bytes to `derive_design_review`. The Model allowlist must admit I01's one method-local `import os as launch_os`, while continuing to prohibit process, file, network, `exec`, `eval`, `compile`, and `open` capabilities. C01's sole nested class and all T01-T03 function shapes must be structurally checked before Model execution.

## Four refusal-route diagnostics and composite closure

Keep runtime safety and analyzer-route claims separate. Every refusal case may satisfy its public safety requirement with any explicit blocker, but an earlier conservative blocker does not prove the intended route was reached.

Add a category diagnostic for each refusal case containing its frozen route description, statically derived source sites, blockers observed at the terminal site, Model evidence, `public_safe_refusal`, `public_route_claimed: false`, and `external_source_proof_required: true`.

- T01 route: outer invocation, nested inner creation, nested inner invocation, then reached explicit `ValueError` fallback. The Model's exact outer/inner identities, `outer` then `constructor` trace, and `NameError.name == "ValueError"` establish the corresponding real-Python route. Public refusal remains safety evidence only.
- T02 route: outer invocation under retained true proof, inner creation while the module `__builtins__` key is present and points to the empty inner dictionary, inner invocation, then reached explicit `ValueError` fallback. The Model's phase and identity facts, exact trace, and exception establish the real-Python route. Public refusal remains safety evidence only.
- C01 route: reached nested `LOAD_BUILD_CLASS` for `Local`. The exact message-only `NameError` establishes the real-Python consumer route. Public refusal remains safety evidence only.
- I01 route: reached method-local `IMPORT_NAME` for `os as launch_os`. The exact message-only `ImportError` establishes the real-Python consumer route. Public refusal remains safety evidence only.

T03 has no refusal-route diagnostic and requires no external route proof. Its exact clean argv and absence of blockers prove that the public analyzer traversed the live method path through direct `ValueError()` and the launch. The Model independently proves the present-before/absent-after key transition, retained standard builtin environment, constructor event, and launch event. A separate route requirement would duplicate the clean public contract without closing another masking risk.

Final category closure remains composite evidence, not a property manufactured by the runtime receipt. It requires:

1. Runtime GREEN for all five fixed public and Model expectations.
2. Reviewed exact-source hook proof, bound to the repaired candidate SHA, for the full T01, T02, C01, and I01 routes.
3. Complete static hook coverage for the explicit fallback table and the admitted ClassDef, Import, and ImportFrom consumers.
4. Original E02/E03 retained evidence as the anti-blanket baseline: the held analyzer constructed/invoked those entries and reached their sink while the Models reached `ValueError` after the constructor marker. The repaired-source proof must show that the new refusal is introduced at the reached authority consumer, not by blanket refusal of function creation or invocation. Repaired E01/E04 clean controls provide the corresponding live nonblanket check.

The controller's `success` field continues to mean runtime semantic GREEN only. It must not set or imply category closure from blockers. The round-level reviewer combines the receipt with the separately frozen source proof.

## Correct interpreter-source metadata

The exact exception provenance remains:

- CPython 3.11.15 `LOAD_BUILD_CLASS`: `https://github.com/python/cpython/blob/v3.11.15/Python/ceval.c#L2547-L2566`
- CPython 3.11.15 import: `https://github.com/python/cpython/blob/v3.11.15/Python/ceval.c#L6969-L6980`
- CPython 3.14.6 `LOAD_BUILD_CLASS`: `https://github.com/python/cpython/blob/v3.14.6/Python/generated_cases.c.h#L8802-L8815`
- CPython 3.14.6 import: `https://github.com/python/cpython/blob/v3.14.6/Python/ceval.c#L2942-L2951`

The 3.14.6 import source begins at line 2942. V5 preserves v4's corrected citation.

## V2 custody shell and exact internal validation

The controller must retain the V2 custody design:

- Exact CPython 3.11.15 controller and child identities.
- Fresh exact-r010 1761-file D-local snapshot.
- One retained-source overlay.
- Exact W watch and protected16 hashes.
- Scrubbed child environment, absolute Git, `-B -P`, seed 0.
- Sixty-second owned-child watchdog.
- Before/after rehash of all tracked and payload inputs.
- Exact HEAD/status reconciliation.
- Six payload members and 1767 verified files on floor; eleven payload members and 1772 verified files on development.
- Create-exclusive output labels and full raw output retention.

The validator must additionally validate public-result internals that the original E1 v2 controller did not:

- Public and receipt schema versions.
- `design_review_receipt_sha256` using production canonical JSON without the harness newline.
- Duplicated `spec_capabilities_sha256`.
- Derivation source path, byte length, and source SHA.
- Baseline and inventory envelope pins.
- Full rows/blockers projection.

Keep the harness transport checksum separate; it uses the harness canonical form with trailing LF.

## Floor-first RED/GREEN adjudication

A complete floor RED remains:

- Child exit 1.
- Five Models valid.
- Five analyzer calls completed.
- Integrity clean.
- Semantic failures retained.
- Controller exit 1 and `success: false`.

Oracle, analyzer, custody, timeout, malformed-output, or incomplete-scope failure is infrastructure and controller exit 2. Actual 3.14 must remain impossible after RED. Development requires a new repaired-source floor receipt with completion, integrity, semantic success, and exit 0 on identical pins.

Reuse the E1 v2 path, environment, snapshot, manifest, watchdog, replay, and final-integrity helpers byte-for-byte where possible. Rewrite only transition pack validation, the oracle, case/result production, and result validation. Preserve the disclosed pre-try stream-acquisition hygiene limitation; fixing it now adds review surface without closing a false-GREEN path.

Residual limits remain:

- T03's harmless Model proves function creation after deletion, not full class-body execution. Exact clean sensitive public behavior plus static source proof covers that distinction.
- A GREEN runtime receipt alone does not close the T01/T02/C01/I01 analyzer-route categories.
- T01/T02 messages remain recorded but intentionally ungated under v5.
- Original E02/E03 evidence is an anti-blanket baseline, not proof of the repaired source. Exact repaired-source hook proof remains mandatory.

No additional material finding was identified. The only V2 issue addressed here is its incomplete account of v4's two metadata changes; all executable-design requirements remain unchanged.
