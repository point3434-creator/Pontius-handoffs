# R2-E1: builtin environment proof gap and reproduction preparation

Root source finding: Important, source-confirmed, behavioral reproduction pending.
No candidate execution, RED reproduction or fix is claimed by this document.
Source remains held; checkpoint3 is not authorized.

Frozen source pair: H beff8193e9d5ce7316f5006fccc77ffcb5ca5695,
rewrite-r2-checkpoint2-source-v1-manifest.sha256
ef3561cb462fcbd31dda7d3774ea34d00c575b7549dc1cc804ad9f92e11c582b.
Source rewrite-r2-checkpoint2-source-v1.py SHA256
7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d.
The unchanged source's explanatory ledger/report are separately frozen at
H87e35c7d244265004f46835a9e7a7f14062589f6, manifest
5eea3e691cb9aac5f894eb246256e9fb53e7d3312a2d954c1a67f7fd447f73ec.

## Finding and discovery

The new distinct exception-type value correctly separates builtin classes from
ordinary imported symbols. Its producer nevertheless assumes the ordinary
builtin environment whenever the current module has no matching name. That
assumption is not proved by the state model.

Root and authority_cost_audit independently traced the category through source
admission, namespace writes, function construction, entry preflight and fallback:

- _c_store_name10051-10065 accepts module-scope bindings named __builtins__;
  _c_namespace_write9799-9814 records them without a special restriction.
- _c_eval accepts None, and _c_eval_dict10199 onward admits empty or exact-string
  maps. A helper-valued dictionary is refused and is NOT an admitted witness.
- _CFunction/_CFrame construction has no builtin-environment identity. The
  preflight at11330/11450 checks the selected class namespace, not module dunders.
- _c_read_name9958-9968 proves ValueError/TypeError/KeyError/IndexError from an
  absent module binding without inspecting or retaining the builtin environment.
  Existing staticmethod/__import__ fallbacks share that environmental assumption;
  future range/sum proofs must not inherit it.
- Whole-file source search found no __builtins__ guard. Deleting a previously
  admitted module binding can also remove the current visible sign of an override.

CPython3.11.15 selects builtins when constructing a function and stores that
environment in func_builtins. A later module-key deletion does not reconstruct
the existing function's builtin environment. Primary source:
[function construction](https://github.com/python/cpython/blob/v3.11.15/Objects/funcobject.c),
[builtin selection and frame lookup](https://github.com/python/cpython/blob/v3.11.15/Python/ceval.c).
This is a source-based semantic chain; actual candidate behavior remains to be
observed in the separate frozen reproduction below.

A minimal prospective witness replaces module __builtins__ with an empty map
before defining the test method. The method calls ValueError() and then the
unchanged admitted launch. Python's method has no ValueError builtin, whereas
the analyzer's new producer can create a normal canonical exception instance.
An explicit refusal is required when that builtin proof is unavailable; a clean
launch result would be unsound. No test source containing a subprocess call may
be executed to demonstrate this difference.

## Bounded independent reproduction scope

Authorize authoring only of a separate E1 reproduction family and its reviewed
snapshot controller. This is supplemental engineering evidence; the fixed twelve
Gate B cases, their Models, owner identities, expectations and receipts stay exact.
No consumed owner is rerun or relabeled. No source fix or runtime is authorized
by this preparation note. Root separately freezes, reviews and dispatches.

Freeze four cases before execution:

1. Standard builtin environment: ValueError() before the unchanged launch.
   Require the exact clean public row and harmless Model launch marker.
2. Module __builtins__ = {} before method definition. Require explicit public
   refusal; harmless Model raises NameError naming ValueError before its marker.
3. The same module override followed by deletion after method definition.
   Require the same refusal/NameError; this tests captured context, not just the
   module map present at lookup time.
4. Function-local __builtins__ = {} only. Require clean control: this local
   name does not replace the function's builtin environment.

Keep a frozen proved-clean existing launch envelope, inventory/stable-ID setup
and expected row unchanged except for these independently declared context and
constructor statements. Preserve complete raw public results. Bad cases require
an explicit blocker; do not invent a stronger no-row requirement if refusal
already prevents acceptance.

Harmless Models may construct a dedicated inert function via types.FunctionType
with a controlled globals/builtins dictionary, optionally delete the module key,
and record the exact exception name and marker. They must not run the sensitive
source, subprocesses, file operations or external effects. Model input is never
supplied to the analyzer as a proof of its environment.

Reuse reviewed snapshot/runtime/environment/custody helpers where possible;
identify every changed helper and pin every adopted input. Use fresh names,
attempt/output identities and D-local snapshots. Actual3.11.15 RED comes first;
no3.14 RED retry after a failing floor. After a separately authorized fix, a new
GREEN owner must pass floor then development on identical source. This does not
replace the later complete R2 Gate B run or any wider acceptance requirement.

## Fix boundary after RED

The category is builtin-environment authority across module bindings, function
creation and later lookup, not the four exception spellings alone. Enumerate all
fallback producers and ways supported syntax reaches a module __builtins__
write/removal before selecting a change. A lookup-time-only check is insufficient
if it forgets an earlier captured override. Scope-correct conservative refusal
is allowed; general custom-builtins interpretation is not required. A local
variable with that spelling must not be conflated with a module override.

Any fix must retain actual-work accounting, all original caps and owners, binder
bytes, the protected files, original test expectations and the1500-line R2 limit.
Do not modify candidate bytes before the frozen RED reproduction. This record
does not reopen the already closed branch checkpoint or authorize generator work.
