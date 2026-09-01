# Freeze-tools design r001 review consolidation

Status: **COORDINATOR INPUT / NON-VERDICT** — this consolidates the two fixed
formal cold reviews and the advisory state-machine audit. It is not a third cold
verdict.

## Verified identities

- Candidate commit:
  `ad8fbcc1ae5a9e3c3b61ae93d5ae5c0b3e4d289e`
- Candidate parent:
  `d1ed3cbda6107d61ea8e77133871720af04970cd`
- Candidate tree:
  `e8de257880c1a034091034fd17a6c4e2c6a5bfdb`
- Candidate manifest SHA-256:
  `862d245f838f4b7459b6ce2aae19eede3b77a4861575722817db12d63af7b689`
- Immutable handoff packet commit:
  `852c10645924aa9602f0d31c5d37806e0a9ec6df`
- Immutable handoff packet tree:
  `d52b523540b7370a4729217fd98a2b4063f89c7c`
- Adopted workflow SHA-256:
  `ab5202b170a5fd9c2cf1540aa198d4a82c742cb336134b0f9a8db944fd64f91a`
- Runtime closure SHA-256:
  `3390ab3d041d432f06754ca94aed348774c421de1c14553a25395c2cab112a3a`
- Formal review A SHA-256:
  `79d9d814c24f56060b9fb672ff4da8e71702f82c644fb3ae94d186e95f0b1671`
- Formal review B SHA-256:
  `d9f871de0b25c837520aeb4b254b09ef6c2e317012fbe935381a6187a82542a2`
- Advisory audit SHA-256:
  `ee00d34b17f463ad9b35ced5c6eb6ca84a808ddf84b34ca221cb89f01855fee3`

The five frozen candidate blob identities are:

| Bytes | SHA-256 | Frozen path |
| ---: | --- | --- |
| 31,013 | `126cadb5f8be5ae6f8fe6346d560deb323684df7cf240c8f5970a2b01d723ee0` | `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-runtime-boundary.md` |
| 18,040 | `434f0cb6138e808dccdb597f780151a645689802bd402ac915e8669257cb4dee` | `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-git-boundary.md` |
| 16,141 | `8c96bf04d983ec5fa77a24b6dfbfc9a5d495eac86512d1100a1e32385af678ca` | `docs/superpowers/specs/2026-09-01-raw-object-workflow-amendment-v4.md` |
| 10,420 | `e6f0aa542dc7f60d3516c8bbf34e19d1db906fcedb7a9892277998e88e20ed06` | `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-design.md` |
| 4,597 | `ef47e87541ed2abb572ee59da4a77850ccc8792f6af1bdb26e100fc518072104` | `docs/briefs/v0a-i01-freeze-tools-r001-brief.md` |

Both formal reviews bind the candidate and manifest above and return defect
verdict `NOT CLEAN`.

## Consolidated finding clusters

| Violated invariant | Findings | Relationship |
| --- | --- | --- |
| Least authority and frozen role capability | A1, B1; advisory 4 | A1 and B1 substantially overlap. A1 requires network and main mechanisms to be absent from builder-loaded code; B1 additionally identifies the deferred role grammar. Advisory 4 is distinct: no role owns fresh-repository adoption end to end. |
| Complete pre-execution source and runtime closure | A2, A3, B2 | These are distinct issues under one invariant. A2 is the unbound and runtime-forbidden common source. B2 is an executable namespace and loader race before inspection. A3 is unconfined non-module or native runtime-data access after apparently clean module and image inspection. None should be deduplicated. |
| Deterministic raw Git objects | A4 | Unique formal finding: author, committer, and clock inputs are absent from the closed environment. |
| Monotonic durable authority | A5, B4, advisory 5; advisory 3 and 6 | A5, B4, and advisory 5 are the same GCM mutation defect. Advisory 3 is a distinct post-retirement ABA replay. Advisory 6 is a distinct incomplete local tuple and intent atomicity defect. |
| Complete main graph and observation algebra | Advisory 1 and 2 | Coupled but distinct: the current graph drops concurrent packet history, while the generic five-state alphabet cannot represent valid predecessor or result descendants and lost-ack descendants. |
| Canonical, byte-bound review provenance | A6, B5 | Partial overlap. A6 finds missing canonical semantic derivation and incomplete manifest population; B5 finds contradictory report, receipt, and reviewer cardinality plus a missing role and digest relation. Both corrections are required. |
| Falsifiable real-boundary acceptance | B3 | Unique formal finding: local transport plus read-only HTTPS observation does not test the production HTTPS mutation boundary. |

The only material exact duplicate is the GCM finding across all three reports.
A1 and B1, and A6 and B5, share roots but contribute distinct required
constraints. A3 and B2 are adjacent attack surfaces, not duplicate findings.

All formal material findings are `Important`; neither reviewer found a
`Critical`. Advisory findings 1 through 5 are `Important`; advisory 6 is
`Medium`. There is no severity disagreement on the same defect. Confidence
differs slightly for provenance: A6 is medium-high and B5 is high. A3 assigns
medium confidence only to the particular first-triggering standard-library
path, not to the missing enforcement mechanism.

## Design-verdict disagreement

Formal review A returns `WRONG SHAPE`; formal review B returns `STRAINED`. The
remedies converge more than the labels suggest. Both allow the launcher,
builder, publisher, and integrator topology to remain, but A requires the
authority-bearing common layer and runtime model to change structurally. The
binding synthesis therefore applies A's stricter source and capability split
while retaining B's closed role-capability contract. The shared population may
contain pure mechanisms only; authority vocabularies and routes must remain in
role-specific source populations.

## Binding r002 correction matrix

| Gate | Exact candidate targets | Binding r002 correction | Verification criterion |
| --- | --- | --- | --- |
| R2-01 Role capability closure | Design sections **Alternatives considered**, **Shared library**, **Offline builder**, **Remote-pair publisher**, and **Main integrator** (`46-129`); runtime section **Fourth reviewed utility** (`168-210`); Git sections **Exact common Git argv prefix** and **Exact network suffixes** (`201-342`) | Freeze every role's complete input grammar, predecessor schema, operation vocabulary, and result equations in r002. Keep only pure codecs, identity comparison, and closed process ownership in builder-loaded common code. Put network suffixes, credential configuration, pair publication, and main transition mechanisms in role-specific sources that the builder cannot load or import. No generic or open-ended Git argv API or authority selector may cross the shared boundary. | A static source and dependency inventory shows no builder-loaded network or main operation table. Through the real launcher, all builder dispatches, malformed inputs, recovery branches, and injected selector faults start no HTTPS helper, shell, GCM, `ls-remote`, `fetch`, or `push`. Every cross-role call refuses before repository, credential, or network access. |
| R2-02 Reviewed source identity closure | Design sections **Runtime launcher** and **Shared library** (`67-102`); runtime sections **Fourth reviewed utility** (`134-195`), **Child runtime lock** (`385-424`), and **Receipt and object bindings** (`485-539`); amendment section **Nonrecursive authority-tool bootstrap** (`82-104`) | Replace scalar utility identity with an exhaustive per-role reviewed source population. Bind every entry point, pure shared kernel, and role-specific module by path, byte count, digest, and held file identity in the plan, authorization, review receipts, projection, runtime handshake, packet inventory, and final revalidation. Permit those exact external origins alongside `__main__`. | The real role loads its shared sources and reaches `RUNTIME_LOCKED`. Changed bytes, correct bytes at a wrong path or FileIdInfo, an unlisted external module, omitted projection or review binding, or mismatched source-set identity refuses before repository or network access. Producer and consumer reproduce every source row independently. |
| R2-03 Pre-execution executable and data closure | Runtime sections **Purpose and proportional boundary** and **Fixed runtime authority** (`8-71`), **Exact child launch** (`222-340`), **Launcher verification and ownership** and **Child runtime lock** (`341-469`), and **Required disposable rehearsal** (`553+`); design section **Runtime launcher** (`67-84`) | Replace post-load discovery as the security boundary with a pre-execution, OS-enforced namespace, loader, and read allowlist plus a closed per-role source, import, native-image, and runtime-data projection. Exclude Tk, Tcl, and other facilities with unenumerated reads unless every required data file is admitted and held. Post-load module and image enumeration remains secondary evidence only. | At a deterministic post-parent-check barrier, injected source, cache, and DLL entries execute no sentinel instruction and cause refusal before repository, Git, or network access. Marker bytes in excluded `tcl`, working-directory profile, and other data paths are denied before influence and before `RUNTIME_LOCKED`. Repeat for first import, late import or load, timeout reconciliation, and final success. |
| R2-04 Deterministic commit bytes | Amendment sections **Two complete Stage 2 routes** (`41-57`), **Candidate authority and coordination packet**, **Routine handoff-main publication**, and **Frozen blind-review outputs**; Git sections **Exact child environment** and **Exact common Git argv prefix** (`146-251`); design section **Offline builder** | Define the full canonical commit byte grammar for every candidate, packet, publication receipt, integration, and reviewer-output commit: author and committer names, emails, timestamps, offsets, parent order, tree, encoding if any, message, separator, and final LF. Bind these bytes to controller inputs and forbid clock or config fallback. Raw commit serialization is the clearest deterministic route. | Two clean repositories at different times with poisoned global and repository identities produce byte-identical commit objects and OIDs. Missing, extra, reordered, or malformed metadata refuses before ref mutation. An independent parser compares every header, parent, tree, separator, and message byte. |
| R2-05 Credential monotonicity | Brief sections **Acceptance criteria** and **Forbidden claims** (`39-51`, `76-84`); design sections **Process and Git boundary** and **State and failure model** (`156-189`); Git sections **Exact positive route**, **Exact child environment**, and **Required disposable rehearsal additions** (`102-187`, `443-481`) | Replace persistent `wincredman` behavior with a separately reviewed, controller-authorized per-launch credential route that cannot store or erase Windows Credential Manager state. Its observation, success, rejection, timeout, cancellation, and lost-ack paths must be side-effect-free with respect to durable credentials. | Against an isolated credential-store fixture, success, rejection, transport failure, timeout, cancellation, and lost acknowledgement leave credential identity and population unchanged. No production-store `store` or `erase` occurs, including during read-only queries, and a fresh retry retains the same authority. |
| R2-06 Canonical review provenance and cardinality | Brief section **Acceptance criteria** (`52-54`); design section **Authority and data flow** (`131-150`); runtime sections **Fourth reviewed utility** and **Receipt and object bindings** (`134-195`, `485-539`); amendment sections **Nonrecursive authority-tool bootstrap** and **Frozen blind-review outputs** (`82-104`, `231-259`) | Define exactly two bundle reviewers, two bundle reports, two issuer-authored ledger lines, and four role receipts per reviewer: eight role receipt objects total. Reviewer distinctness applies to the two reviewer identities and excludes every utility author; it does not require eight identities. Every receipt carries reviewer, role, exact utility source-set identity, plan and schema pins, verdicts, and candidate-read attestation. Each reviewer's self-excluding manifest binds its report, four receipts, and exact ledger line. The structured receipts are the sole machine semantic source; required report labels and justification have one exact equality rule. | A canonical fixture has exactly two reviewers, two reports, two ledger lines, eight receipts, and eight reviewer-role slots. Duplicate reviewer, author overlap, missing or wrong role or digest, cross-role replay, contradictory report and receipt values, duplicate labels, ambiguous justification, altered ledger bytes, or non-issuer synthesis refuses before projection or main advancement. |
| R2-07 Exact HTTPS mutation rehearsal | Brief section **Test plan** (`86-93`); design section **Testing strategy** (`191-215`); Git section **Required disposable rehearsal additions** (`443-481`) | Require a separately authorized disposable HTTPS mutation repository or enforced namespace using the exact production Git, helper, credential, and process route and the same server capability class, while being structurally unable to select production task or integration refs. If unavailable, production mutation remains blocked and evidence claims are narrowed. | Perform real atomic pair creation, exact leases, rejection, timeout, unsupported-atomic behavior, and transport-level lost acknowledgement. Fresh observation must classify `AA`, exact, partial, different, and unknown correctly. Malformed dispatch cannot address production refs. |
| R2-08 Main graph and main-specific states | Design sections **Main integrator** and **State and failure model** (`123-129`, `172-189`); runtime section **Fourth reviewed utility** (`197-203`); Git section **Exact network suffixes** (`284-337`); amendment sections **Candidate authority and coordination packet**, **Routine handoff-main publication**, and **Frozen blind-review outputs** (`131-142`, `211-229`, `261-267`) | Make every integration commit preserve fresh main as first parent and the exact packet as a designated additional parent; require the result to be a fast-forward of the exact leased main predecessor. Replace the generic five-state alphabet for main with exact predecessor, allowed predecessor descendant, exact result, allowed result descendant, protected-subtree conflict, different, and unknown. A changed predecessor requires fresh controller authorization; an exact result descendant with unchanged protected subtree may close lost acknowledgement. Update first-parent and packet-parent verification accordingly. | Interleave two tasks' integration, review publication, lost acknowledgements, and finalization in both orders. Both packet histories remain ancestors and both tasks can finish. Unrelated result descendants reconcile; protected-subtree changes refuse; changed predecessors do not mutate under stale authorization; every push leases the exact fresh OID. |
| R2-09 Retirement replay closure | Design section **State and failure model**; Git pair-query suffix (`272-282`); amendment sections **Atomic remote-pair publication** and **Independent retirement** (`182-209`, `273-295`) | Use the already declared candidate and packet archive refs as permanent spent evidence. Retirement must atomically establish both exact archive refs and delete the live pair under exact leases; main reachability alone no longer permits deletion. Publisher observation covers the live and archive pairs. Live absent plus exact archives is terminal `RETIRED`; partial, different, or unknown archive state refuses. | Publish, dispose, retire, then replay the identical authorization: no push occurs and the result is `RETIRED`. Inject crash and lost acknowledgement across atomic retirement and prove no state appears as initial `AA`. Every partial or different archive combination refuses without mutation. |
| R2-10 Fresh-repository adoption ownership | Design sections **Offline builder** and **Remote-pair publisher** (`104-121`); runtime section **Fourth reviewed utility** and fresh-repository recovery (`168-210`, `547-551`); Git adoption fetch (`293-304`); amendment section **Atomic remote-pair publication** (`205-209`) | Define a closed two-step transition using existing roles: the network publisher may fetch only the exact expected remote objects into nonauthority residue and issue a bound adoption receipt; a subsequent offline builder-adopt authorization validates the complete graph, inventory, intent, and receipt, then creates the full local authority tuple transactionally. The publisher creates no authority refs; the builder has no network route. | From a fresh repository with an exact remote pair, all crash points between fetch, validation, and ref transaction recover from fresh state. The publisher cannot create local authority or synthesize objects; the builder starts no network process. Wrong, missing, partial, or unbound fetched graphs never create refs. |
| R2-11 Complete local atomic tuple | Brief section **Acceptance criteria** (`36-38`); design section **Offline builder** (`104-113`); amendment sections **Two complete Stage 2 routes**, **Candidate authority and coordination packet**, **Schema-generated cold handoff**, and adoption (`59-62`, `144-147`, `175-180`, `205-209`); runtime authorization and receipt sections (`197-203`, `526-530`) | Enumerate every governed local intent ref by exact name and target and include all intent refs, candidate ref, and packet anchor in one create-only `update-ref` transaction. Classification and authorization cover the complete tuple; pair-only exactness is insufficient. | Exercise every proper subset, wrong target, malformed ref, lock failure, transaction failure, and lost acknowledgement. Only all-absent permits one transaction; only the entire exact tuple is success or idempotent recovery; no crash yields a false exact state. |

## Hygiene prerequisites outside the material rejection matrix

1. Git-boundary lines 492 and 495 exceed the adopted 100-column limit and must
   be wrapped in r002.
2. The fixed `60000 ms` wall in Git-boundary section **Exact `CreateProcessW`
   boundary** lacks the required frozen calibration provenance. Supply and pin
   that measurement before live use. The reports' requested executable coverage
   map should accompany the r002 rehearsal specification, while executable proof
   remains an implementation-stage gate.

This consolidation was produced from the three fixed reports and frozen
candidate blobs using read-only inspection. It did not execute a candidate
artifact or runtime, access credentials, query a live remote, or mutate a
repository, ref, or external system.
