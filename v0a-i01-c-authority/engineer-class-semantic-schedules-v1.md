# Finite class/capture semantic preregistration v1

T = D:/Pontius-handoffs/v0a-i01-c-authority. Engineering schedule selection only: no candidate source, cases, oracle, analyzer or payload was authored/imported/executed; no implementation or existing artifact changed. Independent author/root must freeze concrete fixture and harmless-model bytes before semantic implementation. These are twelve exact schedules, not a Cartesian expansion. Preserve all eight existing class cases and the two shared-list cases unchanged.

Read inputs: findings/repair proposal SHA256 `6bc11ee035a6388d73b954d1c5e9b6cd24e8815452fc56bb58197d4ae1b6c143`; challenge SHA256 `14c406145d6eac98529a58c818987afc75f0bbfbc2c4521cc5708281ef6a09d4`. Support was checked statically against Stage0 and the frozen tests-candidate-v4.py matrix/design tests and lexical6 probe. No new result is claimed.

## Shared scaffold and fixed oracle convention

Use the existing ReviewTests.test_static / safe subprocess-argument scaffold from the original composition pack. Each schedule begins with the specified literal `armed = I` and `module = "outer"`. Every Local class starts with `module = "inner"`; classes are ordinary and have no bases, decorators or metaclass keywords. Unless a row replaces the tail, finish with `read()` then `return self._launch(module=module)`.

Define only helpers used by a row. The two common helpers are:

```python
def change(value):
    nonlocal armed
    armed = value

def read():
    if armed:
        ReviewTests._launch = None
```

The independent harmless Model replaces the subprocess body with an event `sink` and a return of its module argument. It uses its own class, not ReviewTests, and records the named events at the statement positions below. `read` records `read` on entry and `write` immediately after replacing Model._launch with None; `change` records `change` before its assignment. Function-definition events are inserted immediately after successful definition in the model only; they do not execute the defined body. Models catch the final TypeError outside test_static and report its type name. They use no Pontius data, private IDs, analyzer output, or candidate result to choose expectations. Sensitive source does not contain event instrumentation.

- **clean** means no blocker and exactly one subprocess argv `[["-m", "outer"]]` from the existing scaffold, with no `inner`/`inner-final` row.
- **refuse** means at least one explicit public unresolved blocker. A clean capability result is forbidden; no exact diagnostic wording or private IDs are required.
- **permitted-refusal** means an explicit blocker is allowed; absent blockers, the exact clean argv above is mandatory. This is fixed now, not a relaxation after execution.

## Twelve schedules

The source-sketch column uses the exact helper/body fragments defined immediately below the table. I and V are fixed Python bool literals shown in each row. No unspecified branch input, loop, runtime choice or optional variant is present.

| ID | Source sketch / fixed parameters | Independent harmless trace -> result | Public expectation | Supported-contract rationale / uncertainty |
|---|---|---|---|---|
| C01 call-raise-unsafe | A; I=False, V=True | `["change-raise", "raise", "caught", "read", "write"]` -> `TypeError`; unreachable `change`, `sink` | **refuse** | One direct helper always changes a represented nonlocal then raises known builtin ValueError. Preserve its surfaced exceptional successor and prior effects; do not recover mixed normal/raise correlation. |
| C02 call-raise-safe | A; I=True, V=False | `["change-raise", "raise", "caught", "read", "sink"]` -> `"outer"`; unreachable `change`, `write` | **clean** | Same singleton always-raise path, opposite scalar. Known builtin handler and direct local helper are admitted (lexical6 / design tests 21634-21654); no ambiguous exception partition. |
| C03 forwarded-grandparent-unsafe | B; I=False, V=True | `["factory", "set", "read", "write"]` -> `TypeError`; unreachable `sink` | **refuse** | factory is invoked INSIDE Local after bindings reset; its returned write-only setter owns the test activation's grandparent cell. Stage0 requires retained dependency through return, including currently harmless cells. |
| C04 forwarded-grandparent-safe | B; I=True, V=False | `["factory", "set", "read", "sink"]` -> `"outer"`; unreachable `write` | **permitted-refusal** | **Support uncertainty explicitly retained:** matrix 31947-31949 permits refusal for some returned-callable readonly/raise-before routes; no frozen clean obligation for this factory-created write-only composition was found. Root may establish a narrower clean contract before freezing, but this preregistration does not invent it. Unsafe C03 remains mandatory. |
| C05 define-after-change-unsafe | C; I=False, V=True | `["change", "define", "read", "write"]` -> `TypeError`; unreachable `later-body`, `sink` | **refuse** | Later dormant method construction must retain lexical cell ownership without copying the old outer cell contents over the changed successor value. Correct ownership plus stale contents is still wrong. |
| C06 define-after-change-safe | C; I=True, V=False | `["change", "define", "read", "sink"]` -> `"outer"`; unreachable `later-body`, `write` | **clean** | Ordinary dormant method construction is admitted and cannot execute its body. Opposite polarity prevents blanket-refusal acceptance. No descriptor/metaclass invocation. |
| C07 if-frame-safe | D; I=True | `["if", "change", "define", "inspect", "sink"]` -> `"outer"`; unreachable `write` | **clean** | Literal True branch, source-point class function binding, then direct name call inside the class. Method free cells must skip class namespace even under If. No instance or descriptor call is involved. |
| C08 try-frame-safe | E; I=True | `["raise", "caught", "change", "define", "inspect", "finally", "sink"]` -> `"outer"`; unreachable `write` | **clean** | Direct builtin raise is caught IN the class; handler creates and directly calls the local function, then finally runs. The class frame persists through handler/finally and only the outward exit restores outer module. No mixed helper-return/raise correlation or TryStar claim. |
| C09 nonlocal-delete-safe | F; I=True | `["delete", "read", "missing", "sink"]` -> `"outer"`; unreachable `write` | **clean** | Delete an already-bound represented nonlocal, then read its free cell under an explicit NameError handler. Captured-name deletion/lookup timing is already admitted by lexical6. This neither assumes absent-global precision nor broadens arbitrary deletion/protocol handling. |
| C10 nonlocal-readwrite-safe | G; I=True | `["readwrite", "read", "sink"]` -> `"outer"`; unreachable `write` | **clean** | Explicit scalar Load plus own nonlocal Store is a control for existing capture behavior. Literal True selects one branch and writes False; no AugAssign or arithmetic precision is requested. |
| C11 recursive-row-safe | H; I=True, V=False | `["change", "invoke", "sink"]` -> `"outer"`; unreachable `write` | **clean**, plus route evidence below | The only subprocess-producing call lies inside local invoke. Correct captured input must reach actual recursive public-body review, not just live effect interpretation. Local helper recursive row extraction already exists at v19:25305-25329. |
| C12 recursive-row-unsafe | H; I=False, V=True | `["change", "invoke", "write"]` -> `TypeError`; unreachable `sink` | **refuse** | Same nested public-row route after opposite cell write. A blocker may prevent recursion, so require recursive-entry evidence only for the clean counterpart; never require private entry count/IDs in the semantic oracle. |

## Exact source fragments for the sketches

These are documentation fragments for the independent author, not executable fixture artifacts. All fragments sit inside test_static after its literals and needed helper definitions. Common `change` and `read` are as above; the model event positions are named in comments here for clarity and must be removed from sensitive source.

**A, used by C01/C02.** Additional helper followed by class and common tail:

```python
def change_raise(value):
    nonlocal armed
    # model: change-raise
    armed = value
    # model: raise
    raise ValueError()
try:
    class Local:
        module = "inner"
        change_raise(V)
        change(I)  # unreachable restoration would erase the reached effect
except ValueError:
    # model: caught
    pass
```

**B, used by C03/C04.** factory must NOT be invoked before the class. The factory has no own nonlocal declaration or read of armed; only its nested setter has a write-only declaration. Follow with common tail:

```python
def factory():
    # model: factory
    def setter(value):
        nonlocal armed
        # model: set
        armed = value
    return setter
class Local:
    module = "inner"
    write = factory()
    write(V)
```

**C, used by C05/C06.** Common read is defined before class creation, so it already retains the outer armed cell. Follow with common tail:

```python
class Local:
    module = "inner"
    change(V)
    def later():
        # model: later-body (must remain absent)
        return armed
    # model: define
```

**D, used by C07.** Replace the common tail with only `return self._launch(module=module)`; do not call a separate outer reader:

```python
class Local:
    module = "inner"
    if True:
        # model: if
        change(False)
        def inspect():
            # model: inspect
            if armed:
                ReviewTests._launch = None
                # model: write
        # model: define
        inspect()
```

**E, used by C08.** The mutation and method construction occur in the known handler, not in a mixed-success helper. Replace the common tail with only `return self._launch(module=module)`:

```python
class Local:
    module = "inner"
    try:
        # model: raise
        raise ValueError()
    except ValueError:
        # model: caught
        change(False)
        def inspect():
            # model: inspect
            if armed:
                ReviewTests._launch = None
                # model: write
        # model: define
        inspect()
    finally:
        # model: finally
        module = "inner-final"
```

**F, used by C09.** Replace common read with this reader, define both functions before class construction, then use the common tail:

```python
def erase():
    nonlocal armed
    # model: delete
    del armed
def read():
    # model: read
    try:
        if armed:
            ReviewTests._launch = None
            # model: write
    except NameError:
        # model: missing
        pass
class Local:
    module = "inner"
    erase()
```

**G, used by C10.** Additional helper; follow with common tail:

```python
def readwrite():
    nonlocal armed
    # model: readwrite
    if armed:
        armed = False
    else:
        armed = True
class Local:
    module = "inner"
    readwrite()
```

**H, used by C11/C12.** Define invoke before Local; replace the entire common tail with `return invoke()`. There is no direct outer `_launch` call:

```python
def invoke():
    # model: invoke
    if armed:
        ReviewTests._launch = None
        # model: write
    return self._launch(module=module)
class Local:
    module = "inner"
    change(V)
```

For C11, retain read-only diagnostic evidence that `_review_body` is entered for invoke and that its recursive review contributes the public `[-m, outer]` row. A successful public row alone cannot establish which path was exercised. This route witness is coverage evidence, not a private numeric-ID equality oracle; original delegation, budget and capture behavior must remain untouched. C12's required refusal does not require that recursion be reached.

## Fixed limits for freezing

Selection totals: twelve cases = seven clean, four refuse, one permitted-refusal. There are no new defining-module global cases or clean promises; the Stage0 absent-global exclusion and conservative unresolved global behavior remain. Presence in callable records/bindings does not prove a destination: cell() can create unresolved-global placeholders. Known unshadowed builtin ValueError/NameError in these fragments uses the existing exception contract, not a new global store model.

Class frame ownership and current cell contents have separate lifetimes. C05/C06 catch old-store reseeding; C07/C08 catch losing the enclosing nonclass frame inside compounds. Newly allocated captures and missing retained-store provenance must not be conflated. The twelve cases do not claim exhaustive coverage of comprehensions, nested class frames, direct class global/nonlocal declarations, arbitrary metaclasses/descriptors, TryStar, unsupported AugAssign, or mixed normal/raise helper correlation. Keep those static obligations or existing conservative outcomes; do not widen clean support to satisfy this preregistration.

Before implementation, independent author/root should freeze these exact schedules, source/model hashes, classifications and unreachable events. Any support-disposition change must be an explicit successor made before candidate execution, not a result-dependent relaxation. All previous scopes and expectations remain intact.
