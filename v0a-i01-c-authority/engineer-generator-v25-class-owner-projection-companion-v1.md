# V25 class-owner projection preservation

Engineering-only companion to v3 and origin clarification v2
(458e182d3bfc8e715e1f9f2be0762fe1237088570a98c81f1958b1f766b22e70).
Root accepted the bounded source scope; no payload or candidate import here.

Independent source review identified an existing shape-loss seam:
_flow_store_path (v23:13454-13463) replaces a nonsensitive implicit_class with a
new mapping, and _assign (22260) installs that legacy projection. A scalar store
could therefore erase structural unresolved-class origin before a later store
adds a deferred obligation. It can also detach a reserved enabled class ref.

At that existing _assign caller, retain the legacy _flow_store_path result and
its scalar/member semantics. If the prior root has a resolved class owner,
explicit unresolved-class alternative or existing missing-owner obligation,
attach an explicit result-alternative carrier to that prior root. Arbitrary
mappings acquire no class inference. Scalar storage itself adds no refusal.

The owner walk follows this explicit alternative even on a legacy mapping
wrapper, but never treats ordinary mapping elements as attribute receivers.
For a live reserved class, the carrier retains the ref and current record
lookup dominates the embedded old projection. It does not restore old members.
For unresolved origin, it retains that unresolved class alternative through
the shape change; a later obligation store takes the approved typed fallback.
Direct/contained/captured old aliases remain untouched and valid in their own
successors. No new alias identity, strong heap update or positive class-member
precision is introduced.

The new visit, carrier allocation and copied references use the current
operation budget. This is origin/obligation preservation, not body execution.
