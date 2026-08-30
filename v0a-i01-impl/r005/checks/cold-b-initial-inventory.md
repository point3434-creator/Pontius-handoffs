# Cold reviewer B: independent initial inventory

Recorded before reading handoff.md or any implementation coverage claim, other reviewer report, or coordinator probe. Inputs read: candidate.json, manifest.sha256, frozen snapshot ADR-0485 and brief, frozen workflow, model/clock/runtime/replay source. This is a reviewer working inventory, not a newly imposed packet gate.

Target: v0a-i01-impl/r005, candidate a8582e6d6b53b55415dab79c4a54e252d00b74ad, manifest e9b0baf12e258d66a92169d38137cbf2f42317158b6515ac377f745bbc52093a, base b357d333fc2393b7fc7dcf31f30c86616208c817. Identity recomputation from Git blobs is pending.

Scope: R2-03 host failure containment and typed cause occurrence order. Policy-authority/value admission and deferred R2-04/05/06/09/10 are excluded. Current primary-checkout workflow refinements are not retroactive requirements.

| Lifecycle/risk | Required observable invariant | Independent evidence planned |
| --- | --- | --- |
| Initialization and event ingress | Runtime refusal stops the hand; valid first cause survives cleanup and is not duplicated by dead-clock echoes | Real host plus malformed order and live-source clock fault at abort |
| Before delivery | Rejected/ambiguous mailbox status is preserved; no retry; no invented accepted action | Real runtime/mailbox boundary with rejection and acceptance-then-raise schedules |
| After acknowledged delivery | Action and complete decision identity survive clock/host failure; interrupted timing does not invent an endpoint | Real ActionMailbox acceptance followed by failing source; compare receipt/count/action bindings |
| Settlement entry/body/exit | Host settlement and oracle exceptions yield a typed unsuccessful receipt; earlier body exception precedes a later closure failure | Real six-player hand; injected oracle exception combined with a source failing only at context exit |
| Settlement semantic comparison | Independent payout/pot/conservation mismatch becomes settlement_mismatch before later cleanup/publication causes | Public oracle seam with a deliberately wrong independent result; simple independent chip totals |
| Trace construction and publication | Host serialization/writer exceptions are contained without erasing previous cause or accepted records; trace failure survives as separate typed cause | Reachable builder/writer seam faults after real hand execution |
| Publication interval entry/exit and finalize | Completed terminal row cannot prove host success when outer accounting/publication closure fails | Source invalid/reversed at phase-specific public ledger operation; compare terminal and external receipt |
| Compound occurrence order | Journal is chronological, duplicates retained only for independent events, no clock-code substitution | Fault A before fault B using observable phase log, not call-position assumptions copied from implementation |
| Recovery and closure | Failed witness source is never called again; no further input; no successful hand from incomplete closure | Source call log, mailbox count, terminal/receipt flags, and a later dispatch refusal |
| Classification | Ordinary host exceptions map to frozen typed causes; real clock reversal remains clock_reversed, not generic clock_invalid | Exception type variants at different host seams; direct closure journal inspection as supporting evidence |

Initial engineering hypotheses, not findings: the settlement catch outside its measurement context might journal an escaping body error after context-exit failure; the special clock-exception catch assumes the raising seam already journalled; trace construction and some host event-generation operations appear outside a containing try. Need establish these through reachable real hand paths and compare with the actual R2-03 claim before judging relevance.

Checks will run only in the assigned exclusive D:-local snapshot, CPython 3.11.15 first then 3.14.6, exact executable/implementation/version asserted before payload imports, -B -P, PYTHONPATH set to snapshot/src, scrubbed child environment, absolute PONTIUS_GIT. No source/test/config edits, broad suite, optional/GPU imports, experiments, installs, commits, or other reviewer evidence.
