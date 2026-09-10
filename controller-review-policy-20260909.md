# Controller ruling: one reciprocal review

Effective immediately, 2026-09-09, for future Pontius work.

Controller instruction: "claude will review work you draft and vice versa" because
the volume of reviews and associated token cost is unaffordable.

- Codex drafts -> Claude reviews. Claude drafts -> Codex reviews.
- Use one opposing reviewer per candidate by default. Preserve a fresh context for
  a cold review and supply the packet under its allowed-input order.
- The drafting side does not launch additional independent reviews of its own work.
- No automatic prosecutor, completeness-critic, parallel second-pass or verifier
  fan-out. Extra reviewers or review agents require an explicit controller request.
- Reconcile findings locally against the source and requirements. Run appropriate
  implementation and acceptance tests; those are distinct from paid review fan-out.
- A correction returns to the opposing reviewer as needed under the ordinary scope
  and residual rules. Do not multiply reviewers or model calls to resolve a tie.

This is the controller's replacement for default multi-pass/Tier C review counts
in future handoffs. It does not alter the historical instructions or issued reviews
of frozen rounds. It leaves source identity, evidence integrity, scope, testing and
exact adoption/retained-run authorization requirements in force.

The r003 review work already completed is retained; no further review is requested
for its approved byte-identical adoption. Apply this ruling to the next drafted work.
