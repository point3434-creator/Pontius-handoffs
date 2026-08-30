# Review verification setup correction

The first coordinator runner stopped during import inspection before any suite or
probe executed: it incorrectly categorized NumPy as an optional dependency.
Frozen pyproject.toml declares numpy>=1.26 as a required dependency. This was a
review-harness defect, not a candidate failure. The original helper is retained;
v2 records the imported dependency modules and rejects CuPy/Torch scientific
imports while permitting required NumPy. Every v2 run uses a new disposable
snapshot. No implementation or test file was edited.

A reviewer also identified that v2 recorded the version tuple only after runtime
import, omitting implementation and full sys.version. V3 asserts the actual
executable, CPython implementation, version slot, and full version in a separate
child before importing any Pontius payload; it writes that identity first, then
checks import provenance and executes the suites/probes in a fresh snapshot.
V1 and v2 are retained as setup/diagnostic records; v3 is the final scoped review
verification. No candidate bytes changed across these reviewer-runner revisions.
