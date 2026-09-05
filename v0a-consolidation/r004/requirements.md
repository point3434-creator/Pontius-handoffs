# v0a consolidation r004: controller-approved narrow replacement

Round kind FIX, Tier C. This records the controller's in-chat approval, not a
new architecture, source seal, adoption, or experiment authorization.

Base: bb959371eec17e76ab46ee6e42f1bac49c26d54a. Retain the ten exact r007 core
blobs from ddea6efbeb55cb8b71da1ebd5a359a0c2c901cf1: six src/pontius/v0a modules
and four tests/test_v0a suites. Retain reduced registration, origin/import and
complete-deal boundaries, and the four direct CPU CI additions. Preserve every
inherited kernel, hard gate, and the dependency-baseline blob
5fe6ee47f3380b65887b528efef05b72c8e6ac0a.

## Replacement contract

The controller explicitly replaced the earlier exact descriptor-inference
exception with a narrow crash-to-explicit-blocker contract:

1. Start from the baseline analyzer, not the expanded descriptor-provenance
   machinery. No descriptor scanner, receiver-provenance inference, or parked
   r008-r010 analyzer work is admitted by this round.
2. A helper binding attempted by the baseline analyzer whose receiver adjustment
   leaves fewer positional parameters than positional defaults must return a
   reason-bearing refusal instead of crashing or inventing argument values.
3. Propagate that refusal into the review's explicit blocker list before helper
   sensitivity filtering, at both binding-result consumers. Do not derive an
   exact capability row from the refused helper invocation.
4. Ordinary registration must still run the review and preserve zero capability
   grants. Capability approval must reject a review containing blockers. Do not
   bypass derivation, suppress failures, or weaken the approval gate.
5. The former positive requirement to infer a defaulted static method exactly is
   withdrawn. Its replacement is crash-free registration, an explicit unsupported
   binding result, and no capability derived from that invocation. Existing
   supported baseline helper-binding controls remain binding.

This is not a general repair of Python binding semantics, alias provenance, or
reachability. ADR-0486 deliberately registers over the known-unsound baseline
with no capability grants. The added refusal concerns the stated alignment
failure where binding is attempted; it does not promise discovery of every
unsupported construct in arbitrary Python. A new false exact result introduced
by this correction, a swallowed alignment refusal, or a registration failure
within the approved slice is in scope.

## Acceptance and stop boundary

Ground truth: the approved refusal policy, independently constructed public
review fixtures, real r007 source, baseline behavior outside the corrected
alignment, and the existing exact-import identities. No Python descriptor
soundness claim is made.

Required checks: deterministic RED and GREEN at the public review boundary;
sensitive and non-sensitive helpers plus nested-helper propagation; existing
supported binding controls; ordinary --write and --check; no v0a capability
rows and both capability digests zero; four v0a suites, inventory/profile suite,
boundary suite and public boundary command on CPython 3.11.15 first, then
3.14.6, in disposable D:-local snapshots under the documented environment.

Manual additions remain capped at 600, excluding the ten exact imports and the
two generated artifacts. Mechanically affected census expectations may change.
No sealed file, sdd/ ledger, ADR, STATUS, dependency file, or prior candidate is
editable. Other lanes stay parked until a separately authorized disposition.

Budget: one bounded replacement candidate under the renewed controller ruling.
Any result requiring broader analyzer inference or a different contract returns
to the controller; it is not permission for another descriptor patch series.
Two independent cold Tier-C reviews remain required before any acceptance or
source-seal decision. No decision commit, merge, push, source seal, rehearsal,
experimental owner, or broad profile is authorized by this implementation round.
