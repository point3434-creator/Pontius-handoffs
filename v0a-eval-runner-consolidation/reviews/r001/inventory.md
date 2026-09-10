# Independent invariant inventory

Recorded before opening packet checks or author evidence files, 2026-09-10.
Reviewer: one Codex cold reviewer; no fan-out.
Initial exposure: no candidate-specific history, prior verdict or candidate-specific memory summary. General Pontius workspace guidance was present in initial context; no memory files/indexes were opened. Source docs/eval-runner.md itself contains author acceptance/evidence claims, necessarily encountered under the specified read order; these are not independent results.
Authority: base commit 1c7067448106cfa2aca3d57be879842d72293c61, tree 3d2fe79d2af20125e322dd4a668335e789810863 plus exactly seven identity.json overrides. Raw verification: 18 manifest entries and 7 override lengths/hashes match.

| ID | Requirement/risk | Observable obligation | Best evidence planned |
|---|---|---|---|
| I01 | Immutable identity | Binding raw hash fixes exact keys, mode, checkout, interpreter path, Git path, source commit, plan bytes, baseline, records and launcher bytes | preflight and negative binding checks |
| I02 | Authorization | Retained authorization binds the exact launch digest before any claim; rehearsal is detached and distinct from retained root | mode paths, CLI preflight tests |
| I03 | Owned source | Source scope at bound HEAD is clean; child plan/input bytes checked; inherited environment cannot select paths/mode | Git source verification in recorder and child; environment tests |
| I04 | One-shot claim | Concurrent callers passing preflight can produce at most one launch for the same records binding; failures cannot remove claim or retry | mkdir exclusive claim and barrier test |
| I05 | Start boundary | Claim/start creation, flush and close failures prevent launch; partial evidence stays consumed | write_new, launch ordering, write-fault checks |
| I06 | Capture authority | Child nonzero exit remains authoritative if subsequent capture flush/close or evidence fails; otherwise no complete outcome returns 99 | launch exit assignment ordering and fault cases |
| I07 | Journal attribution | Existing journal prefix unchanged, exactly one appended raw row, correct source, result and runtime hashes, exactly the newly created run directory | attribute negative cases and child journal producer |
| I08 | Recursive inventory | Every regular file is represented with JSON path, size and hash; traversal/open/read/close failures propagate; links/junctions/nonregular files fail | inventory implementation and injected filesystem errors |
| I09 | Complete evidence | Create-only capture, copied journal, inventory and outcome evidence; success requires correct plan/phase and child completion/cleanup/resource flags | finalization branches and mismatch tests |
| I10 | Interruption | Observed prelaunch signal prevents launch; observed recorder interruption withholds completion; hard termination remains incomplete and consumed | signal context and deterministic signal tests |
| I11 | Full admission | Full count/board/prerequisite names, exact bound prerequisite bytes, measured status/cleanup/phase/order/sample checks preserved while identities/resources come from current plan | baseline diff, entry validator and alternate-prerequisite tests |
| I12 | Chained phases | Producer completion/scope/permutation/prerequisites/artifact identity still binds export/agreement; no arithmetic or protocol changes hidden in delta | precise completion diff and existing focused suite |
| I13 | Environment/runtime | Python 3.14 only, actual temp creation, version matches plan, standard-library recorder; child owns bounded work and cleanup | preflight and disposable focused execution |
| I14 | Scope and claims | Two small campaigns justify declared hands/controls/inventory only; no full-pool/strength/parent bound claims; failure evidence fairly scoped | inspect test oracle first, then author receipts |
| I15 | Failure reachability | Any material finding must have a reachable path, explicit obligation and no effective protection elsewhere; give falsifying observation | trace consumers and child/base validation before reporting |

Limitations established in advance: no hostile-writer isolation or global lock across distinct bindings; operator owns source/inputs/records. No retained invocation, full campaign rerun, source fix, commit/push or controller authorization is in scope. Existing focused checks may execute only in a private disposable snapshot under this scratch directory with Python 3.14.
