# Exact required-outcome excerpts

Source: v0a-i01-impl/r002/disposition.md, SHA256 c4a419547767afd4b2bffbe1533244daf571d48fa1b01ce57a37e9b391fb2291.
Only the three already-authorized outcome sections follow; no later narrative.

### R2-04: Non-response serialization and semantic work is not accounted

Origin: both cold reviewers and coordinator C-01.
Frozen locations: `replay.py:395-428`, `:496-507`.

The coordinator adds two seconds at each real decision serializer: eight
seconds disappear while complete preparation and post-terminal totals are
unchanged. Cold A independently adds one second to each real canonical JSON
operation: thirty pre-publication seconds disappear, with only the final
terminal serialization's extra second reflected in its separate receipt.
Cold B independently reproduces the omission with four decision seconds.

Accept as Important. Measure event/decision/failure serialization, required
row writes, semantic computation and other pre-cut host work through public
bookkeeping intervals. Charge each exactly once by terminal state at entry,
and form complete ordered totals through the declared cut. Keep this work
outside subsequent response walls. Preserve separate terminal publication
measurement and fail closed if any necessary interval cannot be closed.

### R2-09: Required row writes are deferred until the whole hand finishes

Origin: coordinator C-02.
Frozen locations: `replay.py:395-428`, `:510-539`; `trace.py:325-342`.

With a real destination supplied, that file is absent after all four decision
serializations in fixture A. It appears only during final terminal publication.
No storage failure can therefore stop input at the first required post-delivery
write boundary. All later events and actions have already executed by then.

Accept as Important, separate from the missing measurement in R2-04. Implement
incremental publication of the required rows before dispatching the next event,
with create-new destination ownership and fail-closed write handling. Preserve
accepted actions and incomplete files without accepting them as successful
traces. The final terminal row and its publication interval remain separate.
A failure at the first post-delivery write must prevent a second action.

### R2-10: The writer's run-root check is not bound to file creation

Origin: coordinator C-03; related cold-A junction observation.
Frozen location: `trace.py:386-410`, specifically path validation at 391-402
and path-based creation at 403.

After real path validation but before os.open, a diagnostic renames the checked
parent and creates a Windows junction in its old name to a directory outside
the run root. The real writer opens and writes through that junction, then
returns a success digest. Both interpreters reproduce. All paths in the
reproduction are inside a unique disposable fixture area; no user data or
pre-existing file is overwritten.

Accept as Important. The stable directory authority checked must be the one
used to create the file. Refuse unsafe replacement/reparse paths before data
is written using a suitable directory-bound primitive or equivalent verified
protocol. O_EXCL alone binds only the leaf's nonexistence. Keep the fix limited
to this trace writer; no general governance transaction engine is requested.
