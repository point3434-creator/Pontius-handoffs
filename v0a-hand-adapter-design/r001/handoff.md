# Cold design review: v0a-hand-adapter-design/r001

Round kind: NEW-SURFACE. Tier C. Read-only design and source-opening review.
Ref: refs/heads/review/v0a-hand-adapter-design/r001.
Commit: 21474e3d5b105c1709205df1eb5543417abb5a0a.
Manifest SHA-256: ce327c6982338c148d26d4d73cad978ad05b49596520449337d2cc9cb9be0bc9.
Base: 7a387e995e3b37232d2379332927247a4d49c64e.
Tree: be02e38610dee1a819a7686f044aee56899ba785.
Object repository: D:/Pontius/tmp/v0a-hand-adapter-design-r001/authoring.
Finalizer: Codex, with separate exact controller authorization for any adoption.

## Requirements and complete review scope

The controller approved a brief/design round for a one-hand file adapter:
an existing saved blueprint and a scripted-hand data file go through the existing
ReplayHost, followed by independent persisted-trace verification and a concise
summary. No Python edits are needed to select those inputs. Existing runtime,
codec, driver and historical evidence remain unchanged. No implementation or
execution is authorized by this round. All three additions are proposed documents:

- docs/architecture/v0a-hand-adapter-r001/brief.md
- docs/architecture/v0a-hand-adapter-r001/design.md
- docs/architecture/v0a-hand-adapter-r001/source-opening-draft.md

Inspect the frozen blobs, not mutable working copies. Independently recompute
candidate parent/tree, exact three-path scope, each raw blob digest and the
whole-row-sorted LF manifest per docs/workflow.md. Verify the source-opening
proposal's six base Git blob pins against that exact base.

Governing inputs at the base: CLAUDE.md; docs/workflow.md and its
2026-08-30 amendment; PROJECT.md's charter/evidence protocol; ROADMAP.md's
blueprint/integration section; ADR-0485, ADR-0486, ADR-0489 through ADR-0492.
Read other directly referenced base requirements only as needed, not retained
results, opened scientific values or implementer conversations.

Assess feasibility against actual base source: src/pontius/v0a/{model,runtime,
replay,trace}.py, src/pontius/blueprint_artifact/codec.py,
src/pontius/immutable_blueprint.py, src/pontius/holdem_cards.py,
tools/v0a_rehearsal_driver.py, the six proposed registration files and their
directly relevant tests. The three docs are proposals, not authority to execute
the design or change any of these files.

## Review procedure and output

Follow the base workflow checklist and required design verdict. Review all three
documents, including whether the prescribed mechanisms can satisfy the brief
without broad copying, hidden runtime changes, circular authority or unearned
acceptance. Challenge input/source bindings, literal-card adaptation, the
independent acceptance path, failure retention, actual dependency directions,
test-oracle independence, finite coverage limits, proportionality and stop rules.
Do not treat hypothetical unimplemented behavior as an executed failure.

Each substantive required finding needs a concrete scenario or contradiction
and a verifiable correction criterion. Separate required outcomes from advisory
implementation choices. Preferences alone are observations. State Spec/Quality
PASS or FAIL; CLEAN only when no required correction remains; C/I/M counts;
Design SOUND, STRAINED or WRONG SHAPE with reasons; evidence and coverage limits.
The design may be rejected even though its hashes are correct.

Do not inspect sibling reports, controller progress/notes, other task transcripts
or mutable authoring narratives. Do not edit source/index/HEAD/refs, invoke any
project code/test/hand/owner, install packages, call the network or spawn agents.
Read-only Git/stdlib identity calculations are permitted. Use absolute Git
C:/Program Files/Git/cmd/git.exe and command-local safe.directory if necessary;
never modify global configuration. No retrospective adoption is possible here.

Return the complete attributed review as the final answer; the dispatch host
retains it without rewriting. Its first line is an attributed one-line verdict
bound to this task, commit and manifest. Include findings and limits after it.
No reviewer writes another reviewer's verdict or controller disposition.
