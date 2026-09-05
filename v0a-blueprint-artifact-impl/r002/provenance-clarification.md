# Controller clarification of the boundary snapshot description

This corrects the controller's description in provenance-note.md and reviewer
messages; it does not alter a candidate, receipt, issuer report or verdict.

The two boundary GREEN snapshots match eleven of the twelve frozen r002 files.
The differing, unexecuted file is tests/test_blueprint_artifact.py. A direct diff,
independently identified by reviewer B and reproduced by the controller, shows
import formatting, consolidated RAISE/HISTORY assignments, the DELETE sentinel
changed to Ellipsis, and StepClock's initial value moved to a class default.
That particular comparison does NOT add the explicit digest assertion. The
controller's earlier description of its chronology was inaccurate.

The material identity conclusions are unchanged: boundary tests/checker and all
production files match; all twelve files in each correction-final-codec snapshot
match frozen r002; later correction-final2-codec tests remain excluded from r002
evidence. Broad acceptance will use the complete frozen overlay. No candidate
change or extra correction round is needed for this report clarification.
