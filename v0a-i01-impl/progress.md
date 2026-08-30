# v0a-i01-impl task verdict ledger

One line per verdict, written by the verdict's issuer at the moment of the
verdict. Rounds freeze as `review/v0a-i01-impl/r<NNN>`; identity binds to
the candidate commit and manifest SHA-256, never to paths.

2026-08-30 | r001 | claude/implementer | FROZEN (slice A, awaiting cold review) | candidate 2d059f90fb6cec27e4090ad0432c68759a760960 | manifest fc090d962a914b41dec932f21a6c8421499191ccac9dca40363a078cbba95b0c | r001/handoff.md
2026-08-30 | Codex /root/slice_a_cold_a | v0a-i01-impl/r001 | commit 2d059f90fb6cec27e4090ad0432c68759a760960 | manifest fc090d962a914b41dec932f21a6c8421499191ccac9dca40363a078cbba95b0c | NOT CLEAN: six Important findings A-01 through A-06 | r001/reviews/review-01-codex-a.md
- 2026-08-30 | r001 | Codex cold reviewer B | FAIL / NOT CLEAN | candidate=2d059f90fb6cec27e4090ad0432c68759a760960 | manifest=fc090d962a914b41dec932f21a6c8421499191ccac9dca40363a078cbba95b0c | report=r001/reviews/review-02-codex-b.md | Seven material findings; focused suites 36/36 on CPython 3.11.15 and 3.14.6.
2026-08-30 | r002 | claude/implementer | FROZEN (F1-F7 fix round + slice B, awaiting cold review) | candidate 18c965d1f3445c253a6333c4d10899c1dcac0cc6 | manifest 4cfd14ac7bfdb22e052bb9f625610657c01aafa07182acf58d19367a8816cb18 | r002/handoff.md
2026-08-30 | r002 | Codex coordinator /root (additional pass, not cold) | NOT CLEAN: C-01 through C-03 | candidate 18c965d1f3445c253a6333c4d10899c1dcac0cc6 | manifest 4cfd14ac7bfdb22e052bb9f625610657c01aafa07182acf58d19367a8816cb18 | r002/reviews/review-03-codex-coordinator.md
2026-08-30 | v0a-i01-impl/r002 | Codex A | NOT CLEAN | commit 18c965d1f3445c253a6333c4d10899c1dcac0cc6 | manifest 4cfd14ac7bfdb22e052bb9f625610657c01aafa07182acf58d19367a8816cb18 | Five Important findings A1-A5; reviews/review-01-codex-a.md; dual-interpreter bounded probes retained.
- 2026-08-30 | r002 | Codex B | NOT CLEAN | commit 18c965d1f3445c253a6333c4d10899c1dcac0cc6 | manifest 4cfd14ac7bfdb22e052bb9f625610657c01aafa07182acf58d19367a8816cb18 | nine Important findings B1-B9; real-snapshot probes reproduce on CPython 3.11.15 and 3.14.6 | r002/reviews/review-02-codex-b.md
2026-08-30 | r003 | claude/implementer | FROZEN (FIX round, slice 1 of 3: R2-01,02,03,07,08) | candidate 47d08d8c1556d776358e15811e3e98b859fd6a8b | manifest cc255e28680f71fe15de78f26bb8f99a337c1c79e12bf3bdf382a8aa74e7844a | r003/handoff.md
- 2026-08-30 | r003 | Codex cold-a | NOT CLEAN | candidate 47d08d8c1556d776358e15811e3e98b859fd6a8b | manifest cc255e28680f71fe15de78f26bb8f99a337c1c79e12bf3bdf382a8aa74e7844a | 2 Important residual findings: R2-01, R2-03 | report r003/reviews/review-01-codex-a.md
2026-08-30 | r003 | Codex B | NOT CLEAN (2 Important: B1/R2-01, B2/R2-03) | commit 47d08d8c1556d776358e15811e3e98b859fd6a8b | manifest cc255e28680f71fe15de78f26bb8f99a337c1c79e12bf3bdf382a8aa74e7844a | r003/reviews/review-02-codex-b.md
2026-08-30 | r003 | Codex coordinator /root (additional pass, not cold) | NOT CLEAN: C-01 confirms R2-03 | candidate 47d08d8c1556d776358e15811e3e98b859fd6a8b | manifest cc255e28680f71fe15de78f26bb8f99a337c1c79e12bf3bdf382a8aa74e7844a | r003/reviews/review-03-codex-coordinator.md
2026-08-30 | r004 | claude/implementer | FROZEN (FIX round, R3-02 typed closure causes) | candidate 0207430a37e1e5b31c8da8da7aa57da1bc5c88ee | manifest ab28f8dfbe412849c2db2a015b7c40f0549d733a61f6e19295de02dccede06ef | r004/handoff.md
