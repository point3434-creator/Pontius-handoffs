# R2 static aid v2: lexical reparse inspection correction

Author: codex/cold_review_a, tool author and engineering participant; not a cold implementation reviewer. Root and mapping_compatibility identified the v1 path category error: stat() followed reparse points, and exists() could omit a dangling output symlink before resolve(False). V1 and its original note remain immutable; the earlier no-reparse inspection claim was not established by that implementation.

Only pinned_path and checked_file change. Both now inspect metadata with lstat(). pinned_path inspects the lexical leaf and every ancestor without an exists() selector. FileNotFoundError is tolerated only when must_exist is false and the missing item is exactly the prospective output leaf; an absent required leaf or any ancestor re-raises. Existing reparse leaf/ancestor metadata is rejected before resolution. Absolute/no-parent-traversal, T-containment, suffix and regular-file checks remain unchanged. No broader path or analysis logic was added.

Retained pins:
- coordinator-rewrite-r2-static-v1.py: 38981 bytes; SHA-256 4502dea614951d464f3762dbb0a62e823e98b9f5d680918b3cab104d0c1d9214.
- coordinator-rewrite-r2-static-v2.py: 39099 bytes; SHA-256 d129db5a66bd0b5755613873c4de3d965543c4637c857e48d1a7928513977018.
- coordinator-rewrite-r2-static-v2-from-v1.diff: 1447 bytes; SHA-256 579ef56c82a952beef40c9dff75f95db85dfbb15127faff5087514435252281e.

Complete stat/lstat/resolve/is_file call inventory in v2:
- line 71, pinned_path: item.lstat().
- line 77, pinned_path: path.resolve(strict=must_exist).
- line 78, pinned_path: T.resolve(strict=True).
- line 358, checked_file: item.lstat().
- line 359, checked_file: path.is_file().
- line 457, main: checked_file(Path(sys.executable)).resolve(strict=True).
- line 458, main: checked_file(FLOOR_EXE).resolve(strict=True).
No stat() call remains. The four resolve() calls and one is_file() call retain their prior purpose and ordering after the applicable metadata checks. The retained-root resolve compares against T; executable resolution follows checked_file.

The only remaining exists()/is_dir() checks occur after pinned_path returns, for output freshness and parent validity:
- line 461, main: output.parent.is_dir().
- line 461, main: output.exists().
They no longer select whether the lexical output leaf is inspected. Concurrent filesystem replacement remains outside this static metadata-check claim; this correction does not claim an atomic filesystem transaction.

Schema remains pontius-rewrite-r2-static-v1 intentionally. CLI, source/baseline/watch/tool pins, R2/cumulative line accounting, exact R1 binder check, r010 normalization, original-budget/protected16/dependency inventories, named-node review flags, output custody and result predicates are unchanged. Root must pass the v2 file's own SHA when it separately authorizes a run.

Verification was AST/hash/data-only under actual CPython 3.11.15 -I -S -B -P. Both changed function bodies were inspected; every other top-level node is raw-source and location-independent AST exact. Reversing the two explicit source transformations reconstructs v1 bytes. The seven metadata/resolution/regular-file sites and two remaining output predicates were mechanically enumerated. No lstat-based filesystem reproduction was performed. The initial two-line draft attempt stopped at an overly strict AST end-column assertion before creating any artifact; it was superseded by this category-complete correction.

The source, diff and note are exclusive-created, LF UTF-8, fsynced and read back; v1 is rehashed unchanged. Neither aid nor any candidate, Model, test or harness was imported or executed. No current writer source was inspected or modified.

Disposition: ready for independent correction review; unexecuted, no runtime or implementation acceptance granted.
