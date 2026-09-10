# Solve-plan review coordination

Packet: v0a-eval-panel-completion/solve-run-20260910.
Published input: d8d6badc0ca4194ab8fc60b1e4e1035f5b99c9b2 in the handoffs repository.
Source: 1c7067448106cfa2aca3d57be879842d72293c61.
Date: 2026-09-10. Coordinator: Codex.

Recommendation: **NOT CLEAN; return the invocation packet to the drafter before authorization.**
The concrete solve plan passes both reviewers' admission and identity checks. Both independently
identify four Important failures in the wrapper. No retained phase was invoked by this review.

## Dispatch and independence

The controller explicitly requested two cold reviews for this packet. That request overrides
the ordinary one-review count for this round only. Exactly two reviewer sessions ran; there
was no prosecutor, critic, verifier fan-out or third cold review.

Both were new ephemeral Codex CLI sessions with memories disabled. Each received the packet
path, review contract and an exclusive scratch destination, without the conversation or the
drafter's summary. Reviewer 01 used a bottom-up emphasis; reviewer 02 used a top-down emphasis.
Both assessed the complete handoff, not just their starting emphasis. The launch configuration
left the user's model settings unchanged.

Both reported CONTEXT_PROBE_NONE before opening the packet. Each wrote and hashed a separate
invariant inventory after handoff steps 1-3, before rehearsal records. Their final inventory
hashes match the seals announced at that stage. No report or finding was relayed between them.
The exact reports and inventories are retained without rewriting or line reflow.

Cold-input limitation: both later encountered prior source verdicts and an old diagnostic
finding label inside required authorization, adoption and prerequisite documents. Their reports
identify those exposures. They did not open prior reviews or dispositions. These are fresh,
independent reviews of this plan, but not verdict-blind throughout all required inputs. No
replacement passes were dispatched. The packet should provide identity-only predecessor
receipts if future reviews require blindness to every historical verdict.

The coordinator read the user history and workflow memory and is not a cold reviewer. Its work
was dispatch, identity/preservation checking, reconciliation and retention. The coordinator
independently matched all 15 original packet files to the published Git blobs, reproduced the
manifest discrepancy and checked the wrapper and cited frozen journal control flow.

## Reconciled findings

| Issue | Reviewer 01 | Reviewer 02 | Coordinator assessment |
| --- | --- | --- | --- |
| Separate empty-log check and launch reservation | I-01 | I-01 | Important |
| Rehearsal bypass and unconstrained root overrides | I-02 | I-03 | Important |
| Unchecked required record/evidence writes | I-03 | I-02 | Important |
| Old journal row attached after no new row exists | I-04 | I-04 | Important |
| Manifest canonicalization mismatch | I-05 Important | M-01 Minor | Minor; correct at re-freeze |
| Unsupported agreement memory assertion | M-01 | M-02 | Minor |

The four execution findings are distinct. An atomic reservation prevents duplicate launches;
checked writes prevent a single launch from proceeding without its durable record; explicit
rehearsal/root predicates keep execution inside its authorization; journal reconciliation
prevents an absent current outcome from being replaced by an old row. A successful rehearsal
of the ordinary path does not establish any of those failure-path properties.

Locations in invoke.sh: lines 30-57 (reservation), 10-33 (mode/roots), 50-76 (record failures),
and 60-63 (journal attribution). The frozen entry calls begin_run before its try/finally at
tools/v0a_eval_panel.py:630-633; finish_run writes the result before appending the journal in
src/pontius/execution.py:141-161. The stale-row finding does not claim a nonzero child exit
becomes zero: it concerns the identity of the attached evidence.

The manifest discrepancy is factual in both reports. All twelve member hashes are correct,
and the published digest binds the existing manifest bytes. Therefore the coordinator grades
the ordering-description mismatch Minor, while preserving reviewer 01's Important grade.
The required whole-row byte ordering yields:

`d82f86718bbe04627f3d48f212ffd97546a3cbc73cbb477a45017e8fc8a417cb`

The stored filename-ordered manifest yields the published digest:

`a283396997e87cde60ffe00ae5c1e5413fe27a77eca559a360a20570ffe5abfe`

The memory note must distinguish worker Job peak from parent memory and acknowledge growth
with host outcomes as H grows. The single four-hand measurement does not establish that
98,304 draws must exceed 2048 MiB. Neither reviewer claims that configuration will fit.
This remains a later agreement-envelope question, not a reason to change the solve envelope.

## What passed and what remains

Both reviews independently establish admission of the concrete declared-full plan, the
1,081-hand ordered population, the exact 600 s / 2048 MiB envelope, Python 3.14.6 metadata,
adopted source and checkout identities, and the three prerequisite bindings. Reconstructing
the rehearsal teacher from captured rows reproduces its digest and census. The later phases
are sequenced correctly and still need separate bound plans and one-shot authorization.

Verification consisted of frozen-source inspection and independent read-only utility
calculations. No project tests, fault injection, invocation script, rehearsal or retained
solve/export/agreement ran. The reports disclose unavailable deleted rehearsal originals and
the limits of receipt-only chain measurements. The failure findings are static traces.

Return the packet to Claude for wrapper correction, explicit failure/re-entry checks, a
renewed rehearsal and a consistent freeze under the handoff contract. These reviews authorize
no repair, run, commit or push. Reports, inventories, coordination receipts and ledger lines
are saved locally for the next handoff. Original packet bytes and the user's INDEX.md edit
are preserved. No publication is performed by this coordination step.

Artifact hashes and initial probes are in checks/codex-dispatch-receipt.json. Original packet
hashes are in checks/codex-coordinator-identity.json. Review logs remain in the exclusive
scratch directories identified by the dispatch receipt; their hashes are bound there.
