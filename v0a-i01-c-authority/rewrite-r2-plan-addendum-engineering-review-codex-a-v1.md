# R2 plan addendum: bounded engineering review, codex A

Reviewer: codex / r010_cold_a
Design verdict: SOUND
Standing: static design review only; no implementation or harness approval, runtime result, or final cold-review standing. I participated in earlier source reviews and authored the prospective identity input pack; that pack is expressly outside this review.

Frozen pair: H commit aa75536cad0ae54b76b02f9351cd7bc789d7f443; rewrite-r2-inputs-v1-manifest.sha256 SHA-256 96d1b71a3a08b73d2cf1bb09d3ac06473253b6291addf2fbefc541e3bbe3b41f.
Reviewed addendum: rewrite-r2-plan-addendum-v1.md SHA-256 1a1a6bc7f8ef4c56a72735670ff0bb65e883f3aa559abec7b4fec01af6991998.

I independently read both Git blobs at that commit and compared their raw bytes to the local files: manifest 696 bytes; addendum 12424 bytes; both equal and both expected SHA-256 values verified. This verifies the review input, not every other artifact in the input manifest.

Controlling comparisons, read and rehashed:
- rewrite-r2-implementation-inventory-plan-v1.md: d5491bc204b07ec0e1f861b7cfe03facab9b8c9907a38726f64d96c096fe0d4f.
- Held rewrite-r1-task5-source-v2.py: c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f.
- rewrite-r2-implementation-plan-cost-review-v1.md: 4c3ce3b4e30ea60ee68449cfe0ba2656a4db4609fb1f65d02a9b960a84e0f259.
- Adopted rewrite-r2-premise-disposition-v1.md: bdf3b13684d50318c48ddbe3af1682b6e298136e21af3d1ef76ffe7a3f52e6b4.

No design blocker found in the reviewed addendum. It resolves R2-P1 by narrowing the earlier plan rather than treating diagnostic exception strings as runtime proof.

1. Exception admission is closed (addendum lines 9–27). All six legacy tagged-failure categories remain uncatchable: name read, sequence access, cell deletion, namespace deletion, noncallable selection and binder rejection. Central _c_fail normalization must retain conservative issue/debt while removing handler-matchable metadata; changing control alone while retaining an active exception tag would not implement this boundary. The two admitted producer classes are distinct: proved current builtin constructors plus explicit Raise, and the new canonical running-generator rejection. Source spelling, a missing internal entry, or an unknown global is not constructor/type proof. Four-type handler matching does not imply a general exception hierarchy.

2. The metadata and handler design reaches the existing loss points (lines 31–37). Held _c_out at 9866–9876 resets explicit/exclusion fields; _c_follow at 9890–9895 rebuilds an outcome; _CCallObservation at 9253–9263 and _c_call completion construction currently omit the new exception metadata. The plan/addendum require these actual reconstructions, _c_invoke completion and _c_join to preserve active metadata, current state, unrelated debt and prefix traces. An already-matched handler starts from the post-raise state and consumes only that active exception. Historical inner-call completion is evidence, not a second terminal escape. This separates the four D2 alternatives without manufacturing a merged work-pair state.

3. Creation and resume have a bounded proof boundary (lines 41–69). Exact current range(n), exact int excluding bool, and 0 <= n <= 4096 are coherent restrictions. Unsupported first iterables refuse without being resumed. Acquiring the range cursor does not run the element or enter deferred depth. Exact phase/cursor availability precedes body-entry guarding; unknown/missing evidence is not emptiness. The guard still precedes cursor advance, target binding and body evaluation, so generator70 must reach its actual nested-consumption limit rather than an eager g0 scan. Helpers preserve the active generator depth independently of helper depth. Suspended/exhausted updates belong to each current successor.

4. The running-phase rule needs its stated operation ownership preserved in implementation: rejecting a second resume must not itself advance or close the already-running generator. If a known exception subsequently escapes the owning element evaluation, that owning resume closes its own successor record. A handled reentry exception must not become premature exhaustion. This is a consequence of the addendum's separate running-rejection and element-completion rows, not a request for broader generator methods. Python documents both lazy generator-expression evaluation and ValueError for a resume while already executing. [Python 3.11 generator expressions](https://docs.python.org/3.11/reference/expressions.html#generator-expressions), [generator methods](https://docs.python.org/3.11/reference/expressions.html#generator-iterator-methods).

5. BooleanUnknown key equality is explicitly separate from runtime identity (line 74). A structurally deduplicated type-only proof cannot establish is/is not. Exact singleton or proved canonical-object identity remains the only exact-answer basis; other results retain an unknown builtin-bool fact. This fits the adopted identity premise without reviving an implicit scalar or fixture-keyed exception.

The original work caps, per-epoch reserve criterion and separate 1500 additions-plus-deletions stop limit remain controlling. The default full twelve-case baseline/candidate schedule is explicit; intermediate reviews do not authorize extra runtime subsets. Missing new baseline seams are unavailable evidence, not passing zero-work observations. No implementation fitness, headroom or coverage execution is established here.

The checks above are implementation obligations under an otherwise SOUND bounded design, not permission to expand constructors, implicit exception promotion, iterators, handler syntax or general generator precision. I found no need to amend the addendum before the separately controlled authoring process. Prospective input/harness closure remains separate. No candidate, Model, test, harness or sensitive fixture was imported or executed; no source or existing artifact was changed.
