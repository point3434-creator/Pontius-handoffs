# Storage prototype oracle evidence report v1

Engineering auditor: codex/cold_review_a. This is an independent read-only audit of root-executed trials against my independently authored stdlib oracle; it is not a cold review. I did not inspect the prototype implementation and did not launch a new payload. The only new artifacts from this audit are this report and storage-oracle-proof-v1.json.

The bounded storage API checks PASS: all six children exited0, each completed34/34 planned runs with no failure record or stderr, for204/204 total. I found no discrepancy between the saved logs, receipts, frozen inputs and retained payload copies. Engineering evidence supports the sampled immutable-name storage behavior and records its costs. It does not establish production authority correctness, ordinary-corpus headroom or release readiness. Root's separate authorization of a bounded production port is not a verdict issued by this report.

Frozen executed inputs, all independently rehashed:

- Prototype: engineer-storage-prototype-v2.py, SHA25622cc3966435fd4e6e0cecbcbb242275e72d34b36c835b4e960c7c712613822ff.
- Oracle: tests-checks/storage-oracle-v2.py, SHA2566a58ef82832d53510f7d44d58cf5a8fa3764f8be5f2c28dcb7e555a83c72cfba.
- Cases: tests-checks/storage-oracle-cases-v2.json, SHA2563bd5678da334fb551c2f179906e8b4d2cf7a0b0e7a3779e0fad2fb4b4a9c548f.
- Control: engineer-storage-control-v2.py, SHA2568a1d17448ad7a7298a5fda5a78261c04ad4567996b3f474b8853b915a06b400e.
- Config: engineer-storage-run-config-v1.json, SHA25607351a2ba5b508c43a5eee009a9be5365b18e1a6d01cb156ce9f55402786d316.

The operative scope was coordinator-storage-disposition-v1.md SHA256a5eaf456fa762b23ec3ccd23b46ee49cd52cb140410e42c98c3fdd514091d793 and the pre-run approved case/oracle/control/config pins. The plan note tests-checks/storage-oracle-plan-v2.md SHA2560b3d2b56616fe8cee21528330825678c13b57f79856537dc5e584c0226ecc4b8 was not control-bound. Its final issuance/acknowledgment followed root's completed runs, so it is post-execution-issued documentation, not a preregistration hash. This does not assert when it was physically authored. File metadata suggests creation before the first setup, but mutable timestamps are not authorization evidence. Its execution-held/no-run-at-issuance wording is stale at final acknowledgment. This report adopts coordinator-storage-trial-history-v1.md SHA256cc2ba7d41d71bfef89d0eb21bd8d1e0a471f3fdae43465856264d07b8cfb631c; the oracle and case bytes were frozen before dispatch and were not changed after results. Prototype v3's exact-string narrowing was not adopted: selected v2 retains the ordinary-comparison API precondition, while every actual oracle key was an exact builtin string.

The actual runtime identities were3.11.15 and3.14.6, each with seeds0,1,17. The control validates actual3.11.15 with -I -S -B -P. Children use -S -B -P, deliberately retaining environment handling so PYTHONHASHSEED applies. Each child logged its full patch version/executable, safe_path, no_site, disabled bytecode, optimize0, requested seed, snapshot cwd and only the expected scrubbed environment before either payload import. PYTHONPATH pointed to that snapshot's src; TEMP/TMP were D-local; Git was the validated absolute C:/Program Files/Git/cmd/git.exe. All three floor children preceded all three developer children, serially, as dispatched by root and supported by nonoverlapping setup/receipt metadata.

Each of six distinct disposable snapshots had1761 tracked r010 files at commit29c02f6fbd5eb0b7ddc9e816ef28f570b9839358 plus six payload files and one separate manifest. The storage child did not import production code. The external W source was only watched for stable v19 SHA2563d013f20795ff4820656ef45a2aba44a2ee0ad30f830b5e18b2d6975299667c1 before/after; the snapshot generator remained original r010 SHA25629c49c61a632665544e067eb3612039b0828979d21bbc5fd04f6ea5dc2630692. This was not a v19 public-analyzer execution.

I independently hashed all18 log/setup/receipt artifacts, selected frozen sources, all42 retained payload/manifest files and the generator/test file in each snapshot; compared all1767 before/after entries, setup entries and decoded manifest entries; and verified the only recorded untracked paths were the seven payload/manifest files. The approved control hashed every tracked path before/after and the child wrapper checked the complete manifest before payload imports. This read-only audit did not independently rehash every one of the1761 tracked files again. Every log contains one pre-import identity,34 distinct expected case/phase records and two agreeing summary records. Every case's phase sums and event sums equal Meter.used; summed event category deltas equal its final public counts; required callback names are present and actual callbacks remain within the legacy key union.

The28 baseline cases comprise20 compatibility schedules plus the8-point grid. The pack has336 explicit operations; the two failure schedules add three fresh replays each, giving34 runs per child. Ordinary dict operations and the literal legacy set-union join in each child supply expected values/order. Shared harmless immutable tokens make value identity and input-state order observable. The checks cover retained forks and returned tuples, overwrite position, delete/reinsert, missing get/delete, unrelated roots, metadata-only changes, pending identical raw assignment, terminal ordered reads after linear/balanced merges, and repeated reads. Actual N8 grid key order differs across seeds0/1/17 and matches between runtimes for a given seed, so the order comparison is not a frozen hash-dependent literal. Per-name callback argument identities/order are checked; callback invocation order across distinct names is intentionally unspecified for the pure storage callback.

All eight grid rows below, and all34 per-case phase totals, are identical across the six children. Units are public prototype Meter charges, not elapsed time, measured physical memory, or the prior independent copied-name counters. Construction includes initial root installation, forks and updates; audits occur after the terminal read so they do not prewarm it. Repeated is the total of two repeated reads. Validation contains external len checks, isolated from ordered_items transactions. Initialization and lookup-audit contribute0 for these grid rows.

| N | Joins | Changed per round | Construction | Joins | Terminal ordered read | Two repeated reads | Retained audit | Validation | Total |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 8 | 2 | 0 | 746 | 72 | 547 | 36 | 342 | 13 | 1756 |
| 8 | 2 | 2 | 996 | 489 | 547 | 36 | 918 | 21 | 3007 |
| 8 | 4 | 0 | 748 | 144 | 843 | 36 | 666 | 21 | 2458 |
| 8 | 4 | 2 | 1248 | 1007 | 843 | 36 | 1818 | 37 | 4989 |
| 64 | 2 | 0 | 10909 | 72 | 3459 | 260 | 2470 | 13 | 17183 |
| 64 | 2 | 2 | 11435 | 936 | 3459 | 260 | 6630 | 21 | 22741 |
| 64 | 4 | 0 | 10911 | 144 | 5211 | 260 | 4810 | 21 | 21357 |
| 64 | 4 | 2 | 11963 | 1934 | 5211 | 260 | 13130 | 37 | 32535 |

With D=0, join charge is36 per join at both N8 and N64, with zero callbacks; the grid therefore supports sharing unchanged certified names during these joins. At D=2, exactly the two required names invoke the callback per join; N64 total join cost is936 for J2 and1934 for J4. No numeric threshold was retrofitted to make these costs pass.

Deferred order is not free. Even at D=0, N64 terminal realization grows3459 to5211 when J2 becomes J4; the corresponding public order_union_input_visits grow256 to512 and order_dictionary_reference_copies640 to1152. Each repeated read still costs2N+2 in this grid (18 or130). Including construction, joins, terminal and two repeated reads, D=0 N64 costs14700 at J2 and16526 at J4 before retained audits/validation. Retained audits add2470 and4810; D=2 N64 J4 retained audit alone is13130 because it reads more retained versions. Initial construction also remains material:10909 units for N64/J2/D0. Thus the favorable unchanged-join result is a local storage result; total history/order work still grows.

The largest complete case meter is32535, including audits/validation. Across all34 independently reset case meters, each child's sum is264703; that sum is not one budget failure or one production analysis. The fixed maximum remained262144; only two scheduled failure histories temporarily lowered a case meter's public limit, restoring it without reset/refund.

Fault calibration and replay isolate the primitive ordered_items call from subsequent len/tuple validation. Each pristine call is calibrated on an independent fresh version/history. First/middle/last offsets are0, floor(C/2), C-1 relative to used-before. All36 fault trials raised BudgetExceeded, retained the spent/throwing charge, restored the permitted limit, and retried the SAME failed version. Retry units and every public category delta exactly match the pristine call, with correct complete legacy values/order and subsequent repeated/retained reads.

| History | Pristine/retry units C | Allowed first/middle/last | Failed-attempt units first/middle/last |
|---|---:|---|---|
| Linear | 1407 | 0 / 703 / 1406 | 1 / 719 / 1407 |
| Balanced | 1550 | 0 / 775 / 1549 | 1 / 780 / 1550 |

The middle failure can spend more than its allowed increment because the throwing charge is retained. These results establish public retry equivalence with a pristine version for the sampled histories and boundaries, with no partial-cache cost advantage. They are not an exhaustive proof over every charge position, every cache state or all other mutators.

Material limits for integration:

- The prototype merge is pure and obeys identity-on-equal-inputs. No production FlowValue transfer, cell write, raw-parameter hydration, admission/refusal decision or source-point effect is executed. The storage freedom to choose inter-name callback order does not authorize production transfer/cell reordering.
- The no_work flag is supplied test metadata. The production certificate proof and raw adoption/transfer timing require their own unchanged-contract checks.
- The finite N8/64, J2/4, D0/2 grid cannot establish a general asymptotic bound, large-history behavior, wall time, peak memory or final corpus headroom. Prototype charge categories do not directly substitute for ordinary-generator budget accounting, and pure callback cost does not measure production transfer bodies.
- All actual keys are exact ordinary strings. No custom hash-collision/equality-subclass coverage is claimed; v2's broader ordinary-comparison precondition is not comprehensively exercised.
- The immutable24-case public analyzer family still needs its separately authorized post-integration rerun. The preserved old inventory/corpus/focused expectations and ordinary generation remain separate acceptance evidence. This report does not change them.

Raw evidence is under D:/Pontius-handoffs/v0a-i01-c-authority/engineer-checks/storage-prototype-v2-oracle-v2-01-{slot}-seed{seed}, with -receipt.json, -setup.json and .txt suffixes. Exact setup hashes, identities, per-child validations, grid/order witnesses and fault accounting are in tests-checks/storage-oracle-proof-v1.json SHA256ee6509c1c036a154d3fe134ba57c90b63dc3da97ab2c5d15d671f18f600704e3 (22434 bytes).

| Slot | Seed | Receipt SHA256 | Log SHA256 |
|---|---|---|---|
| 311 | 0 | 904feb5c199253f0b478e947df23e3d4a50242ecbbbbd0e231ef601ee4c149f1 | 3b01256e7be5e1e7b547244e35f4fd6a9c4309c13ec1c4b5ff3d6dce0f2a91ea |
| 311 | 1 | 4cb46d012c071c447708be605c363dd25d0f399a6187cf5d3554ea0f65e0de84 | cb1d2c8f87b049941c993760ca8eed2120893d4e632cd8e32bc596dcc6711dc8 |
| 311 | 17 | 8d962e9971311a691e71972dd9ca3ebd33db92134866c95c85a3201b51575b98 | 1558ec420d91752ebbbcb6221253f593ffda789fd4e7915f0355249302b4fa37 |
| 314 | 0 | ce7b69ec24a4dd351c2be86ea4a0b08a277fb5cc3ed9e8e2e99a7ae486f09e93 | 1db0e993e19f884463d13d1110805d3945b0d5759474b224fcfea2e35acc11e8 |
| 314 | 1 | d41d2d7f78cb4a7bfdb62bfa4a7a7acebf7ba5001f48bfdfbff643b761852216 | a90648c9a6861173397475de7f55244852c9926df960af4edf43688dfcf0a0e5 |
| 314 | 17 | b2bd3f97361ed58c5a501277ed87db00973983d53cda91e308fe8580e21820a1 | ce953878ab783e207c6a1b9ecd29f8e6c27d72a5a3543edf7ad44f21fa7c4b59 |

No production/source/test/generated edits, payload executions, broad suites, sensitive fixture bodies, owners, GPU actions, installs, commits, pushes or ledger writes were performed by this audit. Issued predecessor oracle/data/plan and all root-run evidence bytes remain unchanged.
