# R2 static-aid engineering review v1

Verdict: **FINDING R2-S1 (Important, high confidence); design SOUND.**
The two-baseline shape fits the approved review-aid contract. Its new no-reparse
path check does not enforce that contract and needs a narrow successor before
the aid can claim that admission property. No checkpoint1 semantic defect is
asserted.

Reviewer: codex/mapping_compatibility, engineering participant, not the aid author.
This is an engineering tool review, not a final cold source review or runtime
acceptance. Production source remained held and unchanged.

Bound frozen pair:

- H commit: `d74712654a8da4a3ab83d4fcd5d49196784b0471`.
- `rewrite-r2-static-aid-v1-manifest.sha256`:
  `3d20019971d7f4c66cb21a6b7d7058f0e2d931bd1274b55fa60e752b29dd71c1`.
- Aid `coordinator-rewrite-r2-static-v1.py`:
  `4502dea614951d464f3762dbb0a62e823e98b9f5d680918b3cab104d0c1d9214`.
- Exact predecessor diff `coordinator-rewrite-r2-static-v1-from-r1.diff`:
  `625c53d654e63e03fb0d073123b77a70c508077a0da2e1c44acce729c8fa606a`.
- Author note `coordinator-rewrite-r2-static-authoring-note-v1.md`:
  `bb8a62cae578f87e6a856ad333dceb0903148e1e1e27019db97d25e131f89977`.
- Retained predecessor `coordinator-rewrite-r1-final-static-v1.py`:
  `e0a45ca46d5b1a66e1907655b2c43b704250f9d24521a908d0826f4646a5d32a`.

## R2-S1: path guards follow the object they are supposed to reject

Affected category: acquisition and revalidation of existing artifact leaves,
input leaves, their ancestor directories, interpreter paths and the fresh output
path. Exact sites are `pinned_path` lines 66-76, `checked_file` lines 349-354,
and their callers at 448-455, 474-483 and 519-523.

Both guards inspect `item.stat().st_file_attributes & 1024` (70 and 352).
The default stat follows symbolic links; on Windows it follows resolvable
name-surrogate reparse points including junctions. Thus the inspected attributes
can belong to the ordinary target instead of the forbidden lexical path entry.
The subsequent `resolve()` can erase that evidence before the second check.
This follows the documented Python 3.11 API, not a payload result.
[Path.stat/lstat](https://docs.python.org/3.11/library/pathlib.html#pathlib.Path.stat),
[Windows os.stat](https://docs.python.org/3.11/library/os.html#os.stat).

Concrete unexecuted counterexample: an absolute T-local candidate symlink points
to a separate T-local regular file with the expected digest. Every ordinary
target attribute and containment/hash check can pass while the supplied path
contains a reparse point. A junction ancestor within T has the same problem.
Expected hashes still constrain the bytes read; this finding does not establish
unhashed candidate execution or changed production semantics.

The fresh-output sibling also matters: line 69 uses `path.exists()` to decide
whether to inspect the leaf. That call follows a symlink. A dangling output link
to an absent target inside T can therefore skip leaf inspection, be resolved to
that target and satisfy the later fresh-output check. This violates lexical
fresh/non-reparse admission even though exclusive creation protects the resolved
target from overwriting an existing file.

Smallest correction: inspect each existing lexical component without following
it, using `lstat()` (or explicit `follow_symlinks=False`); reject every reparse
component before resolution. For the proposed output, distinguish a genuinely
absent leaf from an existing dangling link via no-follow inspection rather than
`exists()`. Keep the regular-file, containment, explicit pin, exclusive-create
and after-read checks. This is not a demand for new handle-level race guarantees,
a candidate change or a wider controller redesign. No links or test fixtures were
created and no reproduction was executed.

## Independently checked obligations

| Obligation | Source evidence and bounded result |
| --- | --- |
| Frozen identity | All three manifest rows were rehashed from H Git blobs and matched retained bytes; manifest bytes/digest/order matched. The predecessor blob also matched its pin. Recomputed unified diff matched every issued diff byte. |
| No candidate execution | Imports are standard-library modules only. Candidate bytes enter hashing, UTF-8 decoding, difflib and AST operations. `ast.parse(mode="eval")` creates an expression AST; `ast.literal_eval` handles cap literals. No candidate import, exec, eval, compile, subprocess or extracted-helper execution path is present in the aid. |
| Original r010 preservation | `inspect` still receives the pinned r010 bytes, reconstructs original top-level AST/order with only the accepted public-body rename and normalized binder exception, requires five exact integer caps, and checks the budget class AST and raw source segment. |
| Binder normalization | Ten predecessor helper bodies and ten constants are byte-exact, including `normalize_binder`, `call_inventory`, fourteen approved guards/fifteen consumes, six exact read wrappers, `EXPECTED_READ_HELPER`, protected pins and caps. The normalized binder must equal r010. |
| Separate R1 binder protection | Lines 338-346 and 509-510 add a raw whole-line/decorator span comparison against c8fc; a difference fails. This does not replace normalization against r010. |
| R2 size boundary | `raw_line_changes` counts additions plus deletions, both sides of replacements, with raw keepends lines and `autojunk=False`. Lines 500-513 independently compare candidate to c8fc and enforce 1500. Cumulative r010 changes remain informational with no old 2500 ceiling. |
| Input closure | Main requires 21 distinct expected paths: r010, c8fc, retained candidate, separate W generator watch, aid, and sixteen protected W files. It verifies all before source analysis and rehashes all read paths afterward. Partial reads or any mismatch cannot set structural success; partial failure counts stay explicit. The path-topology claim remains subject to R2-S1. |
| Runtime and output | Actual CPython 3.11.15, isolated/no-site/no-bytecode/safe-path, optimize zero and configured executable comparison precede candidate analysis. Only a fresh T JSON report is written with exclusive creation, flush/fsync and readback. Pre-report argument/runtime/output rejection raises; later errors record failure and nonzero exit. |
| Scope honesty | Named-node raw/AST inventories include nested definitions and module/class bindings, changed/removed/added records and relative order. They explicitly remain a manual index, not semantic identity. `scope_approval_granted`, `acceptance_proved`, transitive-engine proof and terminal -c proof remain false; prefixes do not authorize edits. |

The r010 source pin remains
`29c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692`;
the accepted R1/c8fc pin remains
`c8fc013d2be7599aa41b873552dd2a11191f2be1342d1a8f2bd04a39dc1dbd5f`.
These have distinct roles and neither silently replaces the other.

## Method and limits

Read the complete aid, exact diff and author note, then independently compared
frozen Git blobs, hashes and AST/source spans using standard-library code under
actual CPython 3.11.15 `-I -S -B -P`. The verification process exited zero.
It did not import either aid, call any aid helper, execute a candidate, run a
Model/test/harness, or write production files. Official Python documentation
resolved the no-follow API question; root independently flagged the same path
category during review.

No other material concern was found within this bounded tool delta. Executable
aid behavior/performance, malformed-input schedules and public candidate behavior
remain untested. A structural success cannot prove full dependency exclusion,
checkpoint scope, budget placement, terminal child exclusion or semantic GREEN.
No source approval, runtime permission, freeze, commit or publication is granted.
