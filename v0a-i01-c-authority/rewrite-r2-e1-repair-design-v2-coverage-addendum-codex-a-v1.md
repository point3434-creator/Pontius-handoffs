# R2-E1 repair design v2 coverage addendum, codex A v1

Engineering coverage recommendation only. No input, Model, harness, source or expectation is authored here; no payload is authorized or run. Author: codex/cold_review_a, E1 input/harness author and engineering participant, not a cold reviewer.

Bound design: rewrite-r2-e1-repair-design-codex-a-v2.md SHA256 98b8c09445425ed03d98c6293684c87c4ec94ddb126b3e996e590de17cae3fd1. Bound source/census: source7ce0778ab6e8d3aec78d4b91a02407a3bc6c0068ea8abaf7774e534f1662fb3d and census5640242a28caa83b61c08f1c2ac699823fcae53d38ce74b63dd4c579033e6efb. Existing E1 pack remains exact59b8457a2323634d883fb2c9b0ff82a1e60cd980c5f2a4b50e627c8ca32cdb9b.

## Existing coverage limit

E01 establishes absent module key under the original proved module/class frames. E02 establishes a function created while the module key is present, but both its class frame and creation-time module condition are already unproved. E03 establishes that an already-created unproved function stays unsafe after deletion. E04 establishes that a function-local spelling does not alter module/captured authority.

They do not distinguish:

- creating a nested function or implicit class-body function after the module key has been deleted while the executing frame itself is unproved;
- changing the module key to present after a proved outer function was created, then creating a nested function inside that proved frame;
- deleting an override before a later definition in the still-proved module frame, which must remain clean and therefore rejects a monotonic ever-unproved namespace rule.

## Minimum prospective addition: three cases

Together with existing E02, these three complete the two-input creation rule:

new_proof = false when module key is present; otherwise current_frame_proof.

### N1: absent key plus unproved executing frame remains unproved

Required refusal. Necessary because no existing case prevents an absent-key implementation from laundering authority during nested creation.

Admitted sensitive-source shape:

1. Imports and the existing inert launch envelope occur first.
2. Module __builtins__ is assigned an empty exact map.
3. A module factory function is defined while that key is present, so the factory record is unproved.
4. The module key is deleted.
5. The later clean entry calls factory.
6. While executing factory with unproved captured builtins and an absent module key, it defines a local class with a zero-argument raw class member; that member contains ValueError() followed by the unchanged launch, and factory calls Local.run().

This stays inside current admissions: module assignment/delete, ordinary function, local class without bases/decorators/keywords, ordinary zero-parameter member reached through the class namespace, Return/call and the existing sink. It also exercises the implicit class-body frame plus the method function record. Python may fail even earlier at missing __build_class__; the public requirement is an explicit blocker before acceptance, not an exact exception site or no-row claim.

Independent harmless Model shape: create factory with types.FunctionType and an empty builtin dictionary, delete its globals key, call it, and let its real nested class statement run. Record the external NameError name (expected __build_class__ on CPython) and absence of the launch marker. No process/file operation and no sensitive source execution.

### N2: present key overrides a proved executing frame

Required refusal. Necessary because neither E02 nor E03 distinguishes a correct present-key override from an implementation that merely copies the current frame proof.

Admitted sensitive-source shape:

1. Define a module factory while the ordinary key is absent and module frame is proved.
2. Factory defines and immediately calls an inner function containing ValueError() followed by the unchanged launch.
3. After factory creation, assign module __builtins__ an empty exact map.
4. Define the unittest entry; its body reaches the already-proved factory through its explicit module binding.

When factory executes, its own frame proof is true, but inner creation sees the present module key and must record false. The entry/class may itself be unproved; it needs no absent builtin fallback before calling the explicit factory binding.

Independent harmless Model shape: create factory with types.FunctionType under the standard builtin dictionary, then replace its globals __builtins__ value with an empty dictionary before calling it. Its real nested function is created under the present key and raises NameError naming ValueError before the launch marker.

### N3: proved module frame plus absent key after deletion remains proved

Required clean exact launch. Necessary as the only discriminator against a monotonic module ever-unproved history. E01 is clean with no prior override and therefore cannot serve this purpose.

Admitted sensitive-source shape:

1. In module source order, assign __builtins__ an empty exact map and delete it.
2. Still in the original proved module execution frame, define a helper containing ValueError() followed by the unchanged launch.
3. Define the ordinary unittest entry and call that explicit helper.

The helper is created after deletion with an absent key and inherits the proved module frame. It must not be refused merely because the namespace had an earlier override.

Independent harmless Model shape: create a driver function with types.FunctionType under the standard builtin dictionary. Inside the real driver, assign and delete its global __builtins__ key, define the inner helper, and call it. The inner helper must reach the constructor and launch markers without exception. Using a proved driver is essential; directly constructing a function with an absent globals key from the oracle's restricted host frame would not prove the intended module-frame rule.

## Necessity and bounds

All three are necessary and sufficient for this design choice:

| Creation input | Covered by |
| --- | --- |
| present key, unproved current frame | Existing E02 |
| present key, proved current frame | N2 |
| absent key, unproved current frame | N1 |
| absent key, proved current frame after prior override/delete | N3 |

No fourth case is needed for this truth table. N1 uses class creation and member-function creation; N2 uses nested function creation; N3 guards positive post-deletion precision. Existing E03 remains the separate historical-retention witness after creation.

If root later authorizes inputs, preserve the existing four cases and owner bytes unchanged; use a separately named three-case family with two required-refusal and one required-clean classifications. Sensitive sources remain AST-only; only the independently authored harmless Models may run. A pre-fix floor should be expected to show N1/N2 wrong-clean if the current fallback persists and N3 clean, but actual outcomes must be reported rather than assumed. No development slot follows a RED.
