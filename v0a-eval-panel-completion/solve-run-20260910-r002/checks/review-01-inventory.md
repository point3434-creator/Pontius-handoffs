# r002 FIX review invariant inventory

Reviewer: Codex, current session. This is a follow-up review, not a cold review: the user
summary and r001 findings are already in context. No other reviewer is being dispatched.
Read so far: r002 handoff.md, identity.json, invoke.sh and journal_attribution.py. No r002
checks, rehearsal receipts or r001 disposition have been opened. Seal this inventory before
those deferred inputs. Existing r001 reports were read in the earlier review turn.

1. Frozen identity: all manifest members match raw published blobs at 6cae4f8; sorted LF
   aggregate reproduces the declared hash; helper pin matches; plan equals r001 and checkout.
2. Atomic claim: exactly one mkdir succeeds for callers sharing OUT; all launches follow
   that claim and checked start record; interruption never removes claim; loser does not
   truncate captures. Distinguish a scoped claim from an operator bypass via another path.
3. Mode/root admission: retained roots are fixed; rehearsal requires non-retained detached
   checkout; path spelling/aliases and Git command failure cannot silently admit retained
   execution. Mode must be representable correctly in retained JSON records.
4. Checked evidence: required pre-launch writes refuse launch on failure; redirections are
   exclusive; child and wrapper outcomes stay distinguishable; every required capture/hash
   failure prevents success. Interruption may omit final records but must preserve claim.
5. Attribution: journal baseline is measured before launch, new row count distinguished,
   old/missing/extra/malformed rows not substituted; result/runtimes digests checked; output
   belongs to the intended root and attempt under the actual producer and operator model.
6. Failure-path receipts: inspect what each executable case actually does and observes,
   especially whether race callers both reach the claim and whether checks prove child
   absence or only absence of a wrapper output file. Check script exit/status aggregation.
7. Rehearsal: log/claim/attribution and row counts agree; source/plan/result hashes reconcile;
   reconstruct census and teacher bytes; success is planning evidence only.
8. Campaign: unchanged dependency sequence and resource envelope; memory statement confines
   conclusions to measured owners/population and does not promise an unmeasured capacity.
9. Residuals: name dependence on operator exclusive ownership, no external journal writers,
   no manual claim deletion, environment availability and source stability. Do not expand
   this wrapper review into redesigning the adopted solver or adversarial filesystem security.
10. Outcome: report material reachable failures with minimal predicates and static evidence;
    separate closure, nonblocking limitations, missing tests and uncertain claims. No source
    edits, solve/export/agreement, commit or push. Review and ledger artifacts only.
