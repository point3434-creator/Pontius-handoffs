# Class12 controller/probe v2: independent bounded static review

Reviewer: Codex authority_cost_audit. Engineering review only; no payload run,
source edit, test edit or cold-review acceptance claim.

Reviewed exact control SHA
d76b3d07b1b5f855a58050c876ddce57b60929302745fd8116eca109a77b2149,
probe SHA40240ceb30d676a71182c68d03a09970296b604d6d3d136b4b2b9952aec25084,
and pack SHA925ae5b9354377a5957f0c32c8bf5b58fea01612498b835abd6392f9cc87d268,
against frozen v1 sources and retained v2 diffs. No material defect found in
the reviewed adaptation. This is static clearance, not an executed pass.

Independently recomputed hashes and AST-compared both revisions. The probe's
oracle, public_review, load_pack, route_result and all other helpers outside
install_route_observer/main are identical. The entire per-case analysis,
expectation and result loop is identical. Control helpers outside main and
validate_result are identical. The only substantive changes are the explicit
retained candidate pin and removal of dict-only private projection diagnostics.

Candidate path must be an absolute, regular, non-reparse retained T
engineer-generator-*.py file; supplied SHA is validated and checked before
snapshot setup. Both snapshot generator and retained-source overlay match it.
The child prints and the controller validates actual interpreter/executable,
slot, scrubbed environment, D-local cwd, manifest and exact source/probe pins
before the generator or Pontius import. The child additionally resolves
Pontius to snapshot/src, checks all1767/1772 files and frozen case/schedule pins.

The dev leg requires a hash-pinned, complete, integrity-true311 receipt matching
candidate path/SHA, control/probe/pack/schedule/base/watch. Saved floor outputs
are rehashed, stdout is revalidated against the exact pack, actual311 identity
is checked, and the retained floor snapshot/manifest is rehashed. A fresh UUID
snapshot is built per invocation. A complete semantic RED floor is expressly
permitted by the inherited diagnostic protocol; it is not represented as GREEN.

C11 still requires actual invoke entry at closure_depth>0 and a matching
returned public subprocess row [-m,outer], not just a named helper or final
top-level row. The observer delegates original _review_body exactly once per
call, preserves exceptions/results, records scalar descriptors/argv only,
and performs no projected-state lookup or budget consume. Removing the old
dict-only snapshot cannot remove the frozen entry-plus-row requirement.

Outputs are create-exclusive. Payload, validation and cleanup failures retain
raw stdout/stderr, partial records, actual return code and explicit incomplete
receipts. Child and Git commands have60-second infrastructure timeouts; child
cleanup gets10seconds after kill. Success requires all12 semantic and coverage
results plus clean custody. Final checks cover retained inputs/W, every tracked
and overlay byte, manifest, HEAD and the exact permitted git-status path set.

Limits: no payload was executed by this reviewer; startup/site and OS integrity
remain those of the inspected environment, not a hardened adversarial runtime.
Atomic output-stream creation itself precedes the try/finally receipt body, so
a filesystem error during that initial reservation may leave partial empty
outputs; it cannot launch payload. No general process-tree watchdog claim is
made for a static-analysis child. The probe's opening docstring still says v19;
runtime context is correctly bound to the explicit candidate, so this is only
an inherited editorial label, not evidence of interpreter/source substitution.
