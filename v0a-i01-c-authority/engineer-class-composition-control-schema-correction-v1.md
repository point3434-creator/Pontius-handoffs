# Class composition control: static schema correction v1

Root found this defect during pre-execution inspection. Neither control version
has been executed by this author; v1 remains retained and unchanged.

class-composition-mechanism-control-v1.py:
67cf68877e9c3daffe980360cdb0ff3c41d06237374dd4aab1f7f6892562702c

Immutable successor class-composition-mechanism-control-v2.py:
5dd1e6692f82d096a976ca248b45e313a93a97922331186e2cf3e462c2c37717

The only byte-content change is line 355: the emitted receipt schema now uses
pontius-class-composition-mechanism-receipt-v1, matching floor_receipt's existing
requirement at line 137. Previously it emitted the old storage-composition
schema, so a completed floor run could not gate the 3.14 invocation.

No scope, source/pack/probe pin, expectation, runtime, timeout, metering,
instrumentation or other control behavior changed. Root must use the v2 path
and its SHA for --control-sha256 and inspect the exact one-line delta before
dispatch. No configuration, payload, production source or existing artifact
was modified.

Static validation: exact v1 SHA verified; exactly one obsolete schema literal
replaced; the new schema occurs twice; v2 parsed with ast.parse under actual
3.11.15; unified diff contains the single intended replacement. No payload or
harmless oracle was executed. This is engineering evidence, not a cold review.
