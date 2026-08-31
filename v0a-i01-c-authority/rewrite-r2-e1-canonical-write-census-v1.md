# R2-E1 canonical write/fallback census

Read-only engineering guidance; no fix selection, new cases, candidate import or runtime. Bound to frozen H `beff8193e9d5ce7316f5006fccc77ffcb5ca5695`, manifest `ef3561cb462fcbd31dda7d3774ea34d00c575b7549dc1cc804ad9f92e11c582b`, source `rewrite-r2-checkpoint2-source-v1.py` SHA256 `7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d`. Anchors below refer to that source.

Method: whole-file name search, AST caller census, then canonical route/statement/construction source inspection. Source/manifest pins and all seven manifest members rehashed; W remains exact7ce. This is not a cold review or behavioral reproduction.

## Complete namespace-write caller set

There are exactly two calls to `_c_namespace_write` (9799):

| Call site | Owner/route and source context |
| --- | --- |
| `_c_store_name` 10063 | Name binding/removal. Module route is accepted only with current module frame; nonmodule module/global writes refuse at10061–10062. Class route writes its own class namespace. Function/nonlocal cell routes use `_c_cell_write`, not this API. |
| `_c_store` 10111 | Attribute target whose current owner is a class namespace. It writes/removes that class member, then returns protected-class-write refusal. Other attribute owners, including symbolic imported modules, refuse without a namespace write. |

The writer copies the member map and replaces the current namespace record; internal value `None` removes the key (9806–9810). Source literal None is a `_CAtom`, so assignment of it binds a value rather than deleting. Module creation starts with an empty member map (11387); there is no implicit builtin-context record.

## Syntax that can reach module `__builtins__`

| Syntax/category | Actual canonical admission |
| --- | --- |
| Ordinary/chained assignment | `Assign` evaluates RHS then each target (10658–10683); Name targets go through10074/10063. No spelling guard. Any otherwise admitted RHS can bind the module slot, including literal None and empty/exact-string dictionaries; helper-valued dictionaries refuse at10240–10243. |
| Destructuring | Exact native list/tuple RHS with matching arity recursively routes each target through `_c_store` (10075–10099). Nonstarred Name leaves can bind the slot. Starred/unsupported target shapes refuse. |
| Deletion | Name deletion checks current presence, then routes internal None through the same store path (10123–10142). Multiple top-level deletion targets execute in order (10641–10654). Missing names refuse. |
| Import aliases | Absolute nonstar Import/ImportFrom binds the computed name through10063 (10576–10587), including explicit `as __builtins__` or an unaliased binding with that name. Relative/star imports refuse. Imported values are symbols, not verified builtin contexts. |
| Definition installation | Function/async-function construction installs `node.name` through10770 after admitted headers/defaults; deferred body status does not prevent construction. Class installation uses10810 only after normal body completion. A module definition named `__builtins__` therefore binds the slot. |
| Annotation/named expression/augmentation | AnnAssign and AugAssign are not statement cases and refuse at10685. NamedExpr is not an expression case and refuses at10415. Their static lexical classification is not runtime admission. |
| Attribute/element/reflection | No admitted module attribute or subscript write/removal reaches the writer. Class attributes follow the refused route above. Mapping mutation methods and globals/vars/exec/setattr-based mutation are not admitted canonical operations. |
| Aliased value mutation | Admitted list `append` replaces its current object record (10896–10907), including a list already stored under the module slot and reached through an alias; this does not rebind the namespace. String-map environment records have no admitted mutator. Class-member mutation remains explicitly refused. |

Admitted If/Try/helper execution can reach these operations but creates no additional storage entry point. Scope matters: ordinary class-local spelling writes the class map; ordinary function parameters/locals and forwarded nonlocals write cells. None is a module builtin-context replacement. A declared global in a function or class routes toward the module but its write/delete refuses; a module's own global declaration does not prohibit its module write. Class-free reads skip the class frame through the existing capture rules.

## Fallback producers and capture history

The sole explicit canonical builtin fallback is `_c_read_name` 9961–9967: absent module name creates `_CExceptionType` for ValueError/TypeError/KeyError/IndexError, or legacy symbol values for staticmethod/__import__. The former is the only exception-class-proof constructor in the file. Aliases forward values; imported/qualified symbols do not create exception proof. Range/sum producers are absent. No fallback checks `__builtins__`.

The frozen R2-E1 preparation identifies CPython's function-creation builtin capture. Corresponding source inspection confirms `_CFunction` (9148) stores scope/defaults/captures/descriptor/body kind, and `_CFrame` (9138) stores module/class references, with no builtin-context identity/history. Thus later deletion/rebinding can erase the visible module override without representing what an already-created function captured. This is a source-level proof obligation, not a selected remedy or runtime claim.
