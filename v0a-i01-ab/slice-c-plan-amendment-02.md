# Combined-corpus helper binding dependency

The first combined generator --write failed before publication with ValueError:
zip() argument2 longer than argument1. Read-only derivation reproduced the stack
in _bind_helper_arguments: _helper_is_bound treats any self.method call as bound,
including staticmethod; dropping the first parameter makes defaults longer than
remaining parameters. The new all-default static host_case helper exposes it.
A genuine ordinary/class method can also legally default its receiver, exposing
the same defaults-after-removal problem independently of staticmethod dispatch.

Category: static signature binding must account for descriptor binding and align
defaults with the full declared signature before removing an implicit receiver.
Search members: _helper_is_bound, _bind_helper_arguments and their registry callers;
instance/class/staticmethod, self/cls/class call spellings, positional-only receiver,
all-default and partial-default signatures, explicit/omitted/duplicate/unknown args.

Proposed bounded repair: recognize unambiguous builtin staticmethod before instance
syntax, retain existing class/constructor binding; derive positional default mapping
from the full original positional list and then consume only surviving parameters.
Do not truncate strict zips to hide mismatches. Correct keyword exclusion for a bound
positional-only receiver without accidentally excluding the first ordinary parameter.
Do not infer dynamic decorators or execute source during capability analysis.

RED first via real derive_design_review source fixtures and independently executed
pure descriptor calls for binding expectations, sensitive subprocess calls inspected
only (never launched). Omitted/explicit arguments must name the expected capability;
invalid and dynamically unresolved invocations remain blocked. Then focused existing
binding tests + new category cases, actual3.11 then3.14. Final combined generation,
census and inventory suite must run; no capability grant or baseline change.

This is a newly discovered necessary C integration dependency. Only the already
C-owned generator and inventory test file may change. Keep source/tests/inventory
provenance and independent cold review in C's final frozen candidate. Stage0 review
precedes production edit. No redesign of the analyzer or broad-suite invocation.
