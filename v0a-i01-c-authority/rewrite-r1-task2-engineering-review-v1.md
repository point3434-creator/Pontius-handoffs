# R1 Task 2 lexical engineering review v1

Reviewer: codex/r010_cold_a. Read-only source engineering review, not a cold review, runtime result or implementation CLEAN verdict.

Disposition: a source-proved lexical completeness gap must be corrected before these facts are treated as authoritative. It comprises omitted pattern captures and comprehension assignment-expression bindings. It does not require adding Match/comprehension execution to R1.

Pins: H aa7b6f38ad8972727410b708291090297376681c; Task2 manifest1c2da3e7ecea72e4af41842727a1fee93704c4c2c7ad972f0a503b8580d84ad4; source83418c6b172ca0699ca01caed5f78d401e4ec21317806bbf83dba6b466b6be01; exact Task1-v2 delta5e1d83cb3d20390dac21cc36c3ba09594313c6d3fc07b5647477cb444733e74b. Baseline Task1 source844b2d01a5854f1c8494dfc56877d17557a67cf53fef554445e4c20491351862. Controlling design701552c177840e4c5c0dd9c5985776256af5b31e7e997067dd662638a67c3ca8 and scope clarification2e699aaf3b520539eca38233b1a758cbdefcdf67fea86aaa54a7699f926ea8c1.

Independent Git/SHA verification matched eight relevant frozen files (manifest, six entries, prior source). The raw diff regenerates exactly; removing the nine inserted helpers reproduces the prior module AST. No in-progress source was read.

## Required correction: dormant syntax can still declare locals

High confidence, material to routing. _c_scope.visit (9533–9675) recognizes ast.Name Store/Del, but ast.MatchAs.name, ast.MatchStar.name and ast.MatchMapping.rest are string fields. Generic ast.iter_child_nodes never visits those fields as Name nodes. Its comprehension branch returns after only the first iterable, dropping NamedExpr targets in filters/elements/dict keys or values and nested comprehensions.

These omissions change local_names and therefore free forwarding, activation-bank allocation and _c_capture/_c_name_route ownership. A name that should designate a still-unbound local may instead select an enclosing capture or module route after an unreachable unsupported form. Refusing the form only when execution reaches it cannot repair a compile-time declaration already missed.

Python determines function locals from bindings throughout the block, including pattern captures and del targets. [Python3.11 execution model](https://docs.python.org/3.11/reference/executionmodel.html#binding-of-names). A comprehension assignment-expression target belongs to the containing scope, including across nested comprehensions; a lambda introduces its own scope, and applicable global/nonlocal declarations still govern. [PEP572 target scope](https://peps.python.org/pep-0572/#scope-of-the-target).

The original _ExceptionBindingVisitor explicitly handles Match via _python_bound_names (r0109735) and traverses comprehension iterables/filters/results without visiting iteration targets (9744–9766). Its purpose is binding discovery, not body execution. The new visitor also collects loads/sites, so blindly visiting the whole comprehension with the current visitor would introduce a different error: treating implicit-frame targets/loads/calls as outer/eager facts.

Minimal obligation: add charged, scope-aware binding discovery for these two categories, including dormant syntax. Preserve lambda/nested-def/class ownership barriers, nested-comprehension containing-scope behavior, declaration subtraction, and the separation between ordinary comprehension targets and containing-scope NamedExpr targets. Do not evaluate the skipped body or collect it as eager runtime work. Unsupported reached execution can remain refused.

Existing frozen test bytes already contain relevant categories: comprehension-walrus around7385, nonmatching as-pattern8991, empty/false-filter generator assignment10041/10045, zero-iteration assignment19610, and starred/mapping-rest patterns20335/20349. These are source/requirement anchors, not newly run demonstrations of Task2 failure. No new fixture was authored.

## Complete bounded binding inventory

| Category | Task2 static disposition |
| --- | --- |
| Positional-only, positional, keyword-only, vararg, kwarg parameters | All names enter function locals before traversal. |
| Name Store/Del; assignment/unpack/starred targets; for/with targets; NamedExpr outside skipped comprehension | Covered by Name context. Member/subscript target receivers and indices remain Load nodes, not invented local destinations. |
| Function/async-function/class declarations | Definition name belongs to containing scope; child body receives a separate _CScope. Defaults/decorators and class bases/keywords are visited in their evaluating scope. |
| Ordinary imports/from-imports | Alias/local names covered. Import-star differs: original visitor conservatively shadows builtin-exception names, new code records '*'. This does not grant star-import precision; reached unsupported imports must refuse. It is not a valid local-scope dormant-binding counterexample because star import is module-only. |
| Except/except* aliases | Explicit ExceptHandler.name handling covers the string binding; generic traversal covers type/body. Cleanup/exception execution remains future evaluator work. |
| Global/nonlocal | Collected throughout the block and removed from locals. Nonlocal names also request free routing; direct declaration routing has priority. |
| Match captures | Missing as described above, including nested patterns/OR alternatives through the named fields. |
| Comprehensions | Correctly avoid declaring ordinary iteration targets in the containing scope; incorrectly omit containing-scope NamedExpr bindings. First iterable's current outer visit is not sufficient binding discovery. |
| Lambda, function annotations, type parameters | No added execution precision is established. Lambda defaults are visited outside its body. Unsupported reached lambda/comprehension and unsupported construction metadata must receive the promised future refusal; static omission must not be interpreted as safe execution. |

## Supported routing mechanisms and remaining entry obligations

Given complete local/free facts and correctly constructed frames, the inspected routes preserve the intended distinction:

- Function free needs are forwarded bottom-up; parent locals stop forwarding because the parent owns the cell, and a parent function's global declaration stops lexical forwarding. Class slots do not suppress child method free requirements.
- _c_capture skips class frames through enclosing_nonclass, then selects a real function activation/local cell or an already captured route. It stores destinations, not copied values. _c_new_activation preallocates declared locals with an unbound atom; _c_cell_read returning that atom is not treated as a missing bank, so creating a closure does not prematurely read an unbound cell.
- _c_name_route checks explicit globals/nonlocals first. Class writes route to class slots; present class reads select that slot. A syntactically class-local but absent slot falls back to module rather than the enclosing function cell. Free class reads may use captured lexical destinations.
- Future frame construction must install the callable's complete capture map, never unrelated caller bindings. The final module fallback in _c_capture is not a proof that an omitted required capture was global. Future delete must request writing=True and check class-local absence before _c_namespace_write's deletion helper; the latter itself does not construct a NameError successor.

Gate A's four storage cases and two hidden-cell cases use the supported parameter/def/nonlocal/local/class separation mechanisms. Their Models distinguish owner-cell changes from class-local module shadowing, shared aliases and returned reader/setter captures. They do not cover the two missing binding categories and do not establish general lexical completeness.

Root separately identified _CProgram AST-key/int annotations and _c_fact_tuple Sequence-versus-dictionary typing mismatches; these remain acknowledged pending corrections, not a claimed new runtime failure. This review does not assess an unwritten evaluator, broad accounting completeness, new syntax precision or final acceptance.

No candidate/probe/Model/fixture was imported or executed. Only isolated stdlib AST/hash/Git reads and primary language-reference reads were used; no source/test changes or runtime checks occurred. This create-only note is the sole output.
