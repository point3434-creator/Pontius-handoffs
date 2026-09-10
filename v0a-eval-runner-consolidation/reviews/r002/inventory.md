# Independent inventory sealed before author evidence

Review: r002 cold01, 2026-09-10. No candidate-specific history or prior verdict supplied before handoff. General Pontius memory summary present in system context; no memory files/indexes opened or used. The handoff and guide disclose F1 and the historical NOT CLEAN / NOT SOUND verdict, so this is fresh-context, not finding-blind review. No disposition, prior report, or check contents opened before this inventory.

Identity: manifest SHA256 f8a63b7e64bbc017d539d94c916cea5a606e10fe48f5b55ef3ca6c3aa222cf93. All 19 entries verified by byte hash without reading their contents. All seven override hashes and sizes match identity.json. Base commit 1c7067448106cfa2aca3d57be879842d72293c61 resolves to tree 3d2fe79d2af20125e322dd4a668335e789810863. No AGENTS.md found in that base tree by ls-tree. No mutable checkout source read.

Scope: focused repair in tools/retained_eval_run.py, tests/test_retained_eval_run.py, docs/eval-runner.md. Read launcher and its test suite in full; guide and README in full; suite manifest and adjacent completion admission/test search. Seven override authority remains packet bytes, all other source authority base Git blobs. No source/candidate/packet edits or retained campaigns authorized.

Requirement -> observation -> planned evidence
1. Stop deferral before signal snapshot and inside catch boundary -> stop_deferring() first in finalization try, then interrupted.copy(); handler appends signal and raises KeyboardInterrupt after transition -> execute exact eight-case regression and boundary probes.
2. Deferred signals force incomplete, failure exit survives -> interrupted adds error; exit_status preserves child nonzero -> focused launcher suite and deferred-signal evidence-stage probe for both signals and child statuses.
3. Restore previous handlers and consume claims -> context finally restores both; no release/remove/retry code; preflight rejects used records -> exact regression and boundary probes.
4. Real output publication interruption -> write_new exclusive open/write/flush/fsync; interrupt caught, no rewrite, nonzero result -> run RED and GREEN exact regression, inspect fsync outcome bytes independently.
5. Compatibility -> unchanged launch, attribution, inventory, input binding and child-completion logic in focused delta -> compare retained RED source with candidate after seal; existing focused runner tests. Real campaign/full manifest may be unnecessary for signal-only delta; must not claim fresh coverage if not executed.

Initial assessment (not a verdict): direct repair appears to close stale signal snapshot window. No confirmed material finding from source. Questions to resolve: exact regression failure on RED; behavior for previously deferred signals; injection on stop-deferring transition; outcome bytes at fsync; restoring both handlers. Native console delivery and abrupt termination remain outside deterministic injection proof.

Test quality: exact regression uses signal.raise_signal with actual installed handler and real fixture child/file writes; wraps write_new only to inject before open or fsync. Oracles assert 99 vs 7, diagnostic, restoration, claim retained, repeated invocation 97, and one launch. Eight combinations SIGINT/SIGBREAK x child 0/7 x before-open/during-fsync. It does not itself assert fsync outcome bytes or inject precisely inside stop_deferring.

Allowed execution: Python 3.14 only, all fixture/temp/cache/report writes below this unique scratch, no dependencies installed, no retained launches, no commits/pushes. Existing fixtures internally create private Git commits; these are isolated test mechanics rather than candidate or retained repository commits.