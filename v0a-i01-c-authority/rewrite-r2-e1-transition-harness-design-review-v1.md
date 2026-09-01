# R2-E1 transition harness design review v1

Verdict: use a new owner pair built as a narrow successor to E1 v2. Do not rewrite the custody shell, and do not issue v4 inputs. No Model, sensitive source, analyzer, candidate, harness, or controller was executed during this review. No governed artifact was edited. Only this create-only coordinator memo was added; H and source remain untouched.

Current controlling pins:

- Pack `71c5e8efd0922b213a917a1709c271d3d0fa26ba0268d2d8a7f780e942550511`
- Spec `fd0e8e6b6a23aca5eed9b75baacab4dfbf552e1a8db11d6673d897873ec7ef64`
- Static map `9ccb088c53a317ada694ead9287c1d5fe8f2376d3c2549d99ac1e6cbb731ea7a`
- Source differences `c393c7b5ecf1e6cad0e753e89e00be1058e4b8c03dea95e8770c60b8b651270a`

Recommended new files:

- `rewrite-r2-e1-transition-probe-v1.py`
- `rewrite-r2-e1-transition-control-v1.py`
- Schema `pontius-r2-e1-transition-harness-v1`
- Payload `.rewrite-r2-e1-transition`

The child stdout contract should be exactly seven nonempty LF-only JSON-object lines, with empty stderr:

1. One pre-import identity record.
2. T01.
3. T02.
4. T03.
5. C01.
6. I01.
7. One final summary.

Reject malformed JSON, scalars, blank lines, extra records, reordered records, CR bytes, or any stderr. Require exact outer record-key sets.

Each case record should retain the frozen case metadata, full oracle observation, analyzer error, full public result, full receipt, projected rows/blockers/argv, transport hashes, semantic result, and a category-route diagnostic. The controller must independently rederive all projections.

The oracle observation should contain only serializable identity facts, never `id()` values:

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

The key-object assertions are derivable from the pinned Models and belong in the reviewed harness; no v4 pack is needed:

- T01: absent before/after; outer and inner both capture the same empty dictionary.
- T02: present before/after; key value is the inner empty dictionary and differs from the outer standard dictionary.
- T03: present before; key value is both outer and inner expected because they alias the standard dictionary; absent after.
- C01/I01: absent before/after; outer captures the empty dictionary.

T01-T03 must each retain exactly one captured inner function. C01/I01 must retain zero.

Catch ordinary `Exception` outside `_function`. An expected exception is oracle evidence; setup, identity, or Model-structure failures are oracle errors. Do not catch `BaseException`.

For exception adjudication:

- T01/T02 require exact `NameError` and `.name == "ValueError"`. Record the message, but do not gate it because v3 does not freeze that field.
- C01 requires exact `NameError`, `.name is None`, and message `__build_class__ not found`.
- I01 requires exact `ImportError`, `.name is None`, and message `__import__ not found`.
- T03 requires no exception.

Only the pinned harmless Model may be compiled and executed. Sensitive source remains AST-only and is passed as bytes to `derive_design_review`. The Model allowlist must admit I01's one method-local `import os as launch_os`, while continuing to prohibit process, file, network, `exec`, `eval`, `compile`, and `open` capabilities. C01's sole nested class and all T01-T03 function shapes should be structurally checked before Model execution.

For C01/I01, keep runtime and architecture claims separate. The runtime harness should prove:

- The harmless Model reached the intended real CPython consumer through the exact exception.
- The public analyzer returned an explicit safe refusal.

It should not claim that the analyzer reached that same consumer merely because some blocker exists. Add a diagnostic object containing the consumer, statically derived consumer line, blockers observed at that line, `model_consumer_reached`, `public_safe_refusal`, `public_reach_claimed: false`, and `external_source_proof_required: true`.

Final category closure should combine the GREEN receipt with a separately reviewed source proof bound to the exact repaired source SHA. That proof must cover the case-specific path to the class/import gate and the complete ClassDef/Import/ImportFrom hook inventory. This avoids adding a public diagnostic or freezing implementation-specific blocker wording.

The controller should retain the v2 custody design:

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

The new validator should additionally validate public-result internals that v2 did not:

- Public and receipt schema versions.
- `design_review_receipt_sha256` using production canonical JSON without the harness newline.
- Duplicated `spec_capabilities_sha256`.
- Derivation source path, byte length, and source SHA.
- Baseline and inventory envelope pins.
- Full rows/blockers projection.

Keep the harness transport checksum separate; it uses the harness canonical form with trailing LF.

A complete floor RED is:

- Child exit 1.
- Five Models valid.
- Five analyzer calls completed.
- Integrity clean.
- Semantic failures retained.
- Controller exit 1 and `success: false`.

Oracle, analyzer, custody, timeout, malformed-output, or incomplete-scope failure is infrastructure and controller exit 2. Actual 3.14 must remain impossible after RED. Development requires a new repaired-source floor receipt with completion, integrity, semantic success, and exit 0 on identical pins.

Reuse the v2 path, environment, snapshot, manifest, watchdog, replay, and final-integrity helpers byte-for-byte where possible. Rewrite only transition pack validation, the oracle, case/result production, and result validation. Preserve the disclosed pre-try stream-acquisition hygiene limitation; fixing it now adds review surface without closing a false-GREEN path.

Residual limits:

- T03's harmless Model proves function creation after deletion, not full class-body execution. Exact sensitive public behavior plus static source proof must cover that distinction.
- A GREEN runtime receipt alone does not close the C01/I01 analyzer-route category.
- T01/T02 messages remain recorded but intentionally ungated under v3.
