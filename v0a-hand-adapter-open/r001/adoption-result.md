# Adopted source-opening decision

Controller authorization: "Open and push", replying to the exact candidate request.
Decision: abe559511a72086791ca53cd3dfec24e49ec280b.
Title: Open the one-hand file adapter source round.
Parent: 7a387e995e3b37232d2379332927247a4d49c64e.
Tree: 67d0e61c2cce8cba2c6e2ff759c24f432d50ac04.
Reviewed candidate: 36c31477d87028aeec31339d28ccc089ffcaa31d.
Manifest: 83814f33a6f7f64b99da7bedfaaa81e61712c083d8f0ecf55a79f0f9a22f142c.

The exact five-file reviewed tree was committed and explicitly pushed to
https://github.com/point3434-creator/Pontius.git, refs/heads/master. The remote
ref was read back and matched the decision. No candidate byte changed.

Fresh authorized and post-commit metadata checks ran in isolated snapshots,
CPython 3.11.15 first then 3.14.6. STATUS was current and all 12 status tests
passed for each invocation. The post-commit snapshots use the actual decision
commit and their five paths match the frozen raw blobs. Commands, interpreter
and import identities, output and exits are retained in checks/.

Primary tracked worktree/index are clean. The before/after normal untracked
status SHA-256 is unchanged:
3ad015f8e8f7e2623bca0a4e23411f5c287134aa89bb60531a935226189172c5.
Existing untracked work and repository hook files remain untouched. A local,
command-scoped empty hooks path prevented only automatic premature/duplicate
push; the final push was explicit and independently checked.

ADR-0493 now activates exactly the reviewed bounded adapter source opening.
No adapter implementation, source acceptance/seal, operating or research run
is claimed. Existing engine, codec and driver source bytes remain unchanged.

Separate archive and handoff uploads were blocked before execution by the
safety approval because their additional payload/destination need explicit
transfer approval. No archive ref or handoff packet was uploaded by that attempt.
The unaffected, specifically authorized primary commit/push was completed alone.
See ../../publication-blocker.md. All local packets, reports and refs remain
retained; handoff publication is incomplete and is not claimed as completed.
