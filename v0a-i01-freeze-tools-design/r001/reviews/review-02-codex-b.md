# Cold design review - v0a-i01-freeze-tools-design/r001

Reviewer ID: `codex-b`
Candidate commit: `ad8fbcc1ae5a9e3c3b61ae93d5ae5c0b3e4d289e`
Manifest SHA-256: `862d245f838f4b7459b6ce2aae19eede3b77a4861575722817db12d63af7b689`
Defect verdict: `NOT CLEAN`
Design verdict: `STRAINED`

Five Important corrections remain. I found no Critical defect. The four-process
decomposition can be retained, but authority is split between a role-neutral
library and contracts deferred to later documents, runtime acceptance is partly
post-execution, and the production mutation route is represented by a local
transport in the proposed evidence. Those choices invite exactly the boundary
errors this checkpoint is intended to remove. A frozen role-capability contract,
a pre-execution runtime namespace/loader gate, and an exact HTTPS mutation
rehearsal would correct the shape without replacing the whole bundle.

## Governing invariants recorded before findings

1. **Immutable identity.** Review authority is the frozen candidate commit plus
   its manifest digest. Changed bytes or scope require a new round.
2. **Acyclic bootstrap.** Only the adopted temporary-index Stage 2, direct Git,
   and handoff packet rule 6 may establish authority for these tools. The tools
   cannot freeze, review, publish, accept, or preserve themselves.
3. **Least authority by role.** The launcher may establish runtime/process
   facts only; the builder is offline and local; the publisher may create only
   the candidate/packet pair; the integrator may add only the exact receipt and
   lease-advance the pinned integration ref. Shared code cannot confer a role.
4. **Pre-execution runtime closure.** Every executable byte, module, native
   image, data path, environment value, argument, inherited handle, and process
   fact outside the stated TCB must be exact before it can execute or influence
   an authority transition, and must remain held through reconciliation.
5. **Raw-object exactness.** Source bytes map directly to blob/tree/commit and
   manifest bytes. Checkout, index, filters, attributes, normalization, and
   implementation-derived test oracles cannot affect identity.
6. **Monotonic durable state.** Only complete ABSENT state may attempt creation;
   complete EXACT state may close a lost acknowledgement. PARTIAL, DIFFERENT,
   UNKNOWN, malformed, unavailable, ambiguous, timeout, and crash states
   preserve durable authority and refuse. There is no rollback or deletion.
7. **Closed Git/GCM route.** Executable, helper, shell, environment, config,
   repository, URL, refspec, transport, output, wall, and descendant lifetime
   are closed inputs, with fresh observation after every uncertain result.
8. **Byte-bound cold provenance.** Generated handoff semantics and utility
   reviews are bound without content recursion, mutable narration, self-review,
   cross-review leakage, or non-issuer ledger authorship.
9. **Falsifiable acceptance.** Each material claim has an independent oracle and
   a rehearsal through the real public boundary, within the declared size and
   TCB limits.

## Systematic seam inventory

| Seam | Authority crossing | Required closure |
| --- | --- | --- |
| Adopted workflow -> utility candidate | Existing Stage 2 freezes new authority tools | Exact workflow capture, base, five-path scope, ref, commit, manifest |
| Controller -> PowerShell launcher | Controller authorizes source and one use | Held source bytes, canonical authorization, exact role and limits |
| Launcher -> CPython | Unreviewed runtime could execute before the utility gate | Complete file and namespace closure, argv, environment, CWD, loader route |
| CPython -> entry point/common library | Shared code can cross role boundaries | Digest-held sources and non-forgeable role-scoped capabilities |
| Python -> Win32 process/Job APIs | Child image and lifetime become authority inputs | Non-null image path, exact quoting/handles/job, timeout and active-zero |
| Python -> local Git object store | Raw bytes become objects and refs | Independent parsers/oracles, exact modes/paths, transactional create-only refs |
| Git -> HTTPS helper -> shell -> GCM | Network and credential authority become reachable | Exact images, config/env/URL, credential side effects, process lifetime |
| Local graph -> remote candidate/packet pair | Two remote refs become review authority | One atomic create-only push plus fresh strict pair classification |
| Remote pair/main -> integrated packet | Main receives one receipt child | Exact graph, protected subtree, fresh main, exact lease, lost-ack recovery |
| Cold-input spec -> generated handoff | Structured authority becomes reviewer prose | Closed schema/template and packet inventory binding |
| Utility reports -> review projection | Reviews authorize later use of the tools | Exact reviewer/role cardinality, immutable reports/receipts/ledger bytes |
| Reviewer outputs -> finalizer/main | Blind outputs become durable coordination state | Create-only refs, issuer authorship, exact copy, protected-task merge rule |

## Identity and input verification

The immutable handoff packet object
`852c10645924aa9602f0d31c5d37806e0a9ec6df` is a commit with tree
`d52b523540b7370a4729217fd98a2b4063f89c7c` and exactly the five named packet
blobs: `handoff.md`, `candidate.json`, `manifest.sha256`,
`inputs/workflow.md`, and `inputs/runtime-closure.json`.

Both the local review ref and the cached origin-tracking ref resolve to the
declared candidate object. That object has exactly one parent,
`d1ed3cbda6107d61ea8e77133871720af04970cd`, and tree
`e8de257880c1a034091034fd17a6c4e2c6a5bfdb`. Its parent-relative raw diff is
exactly five additions, all mode `100644`; each named base blob is absent.

The frozen candidate blob checks are:

| Bytes | SHA-256 | Frozen path |
| ---: | --- | --- |
| 31,013 | `126cadb5f8be5ae6f8fe6346d560deb323684df7cf240c8f5970a2b01d723ee0` | `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-runtime-boundary.md` |
| 18,040 | `434f0cb6138e808dccdb597f780151a645689802bd402ac915e8669257cb4dee` | `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-git-boundary.md` |
| 16,141 | `8c96bf04d983ec5fa77a24b6dfbfc9a5d495eac86512d1100a1e32385af678ca` | `docs/superpowers/specs/2026-09-01-raw-object-workflow-amendment-v4.md` |
| 10,420 | `e6f0aa542dc7f60d3516c8bbf34e19d1db906fcedb7a9892277998e88e20ed06` | `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-design.md` |
| 4,597 | `ef47e87541ed2abb572ee59da4a77850ccc8792f6af1bdb26e100fc518072104` | `docs/briefs/v0a-i01-freeze-tools-r001-brief.md` |

Those rows are complete and whole-row byte sorted. The 658-byte manifest file
hashes to the declared digest. The adopted workflow capture is 30,942 bytes and
hashes to
`ab5202b170a5fd9c2cf1540aa198d4a82c742cb336134b0f9a8db944fd64f91a`.
The runtime closure is 413,522 bytes and hashes to
`3390ab3d041d432f06754ca94aed348774c421de1c14553a25395c2cab112a3a`.

Read-only parsing of the closure reproduced 2,614 rows and 63,499,244 summed
bytes. Paths are ordinal sorted with no exact duplicate, case-fold duplicate,
file/directory prefix collision, scope violation, or malformed row. This checks
the frozen JSON's internal consistency; it does not attest the live installed
runtime population.

## Important findings

### I-1 - The executable role contract is deferred and the shared boundary has no mandatory role capability

**Severity:** Important. **Confidence:** High.

**Binding:** `ad8fbcc1ae5a9e3c3b61ae93d5ae5c0b3e4d289e` +
`862d245f838f4b7459b6ce2aae19eede3b77a4861575722817db12d63af7b689`.

**Frozen locations:**

- `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-design.md:46-63`
  rejects a single role gate, but lines 88-102 put Git process control in a
  role-neutral shared library.
- The same file at lines 104-129 asserts that the builder has no network route
  and the publisher/integrator cannot cross roles, without defining the
  enforcement boundary.
- `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-runtime-boundary.md:
  197-210` defers the closed `predecessor_state`, exact argument cardinality,
  value domains, and state-to-argument equality to future v8 schemas.
- `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-git-boundary.md:7-10`
  leaves the state machine and object equations separately controlled.

**Concrete state -> wrong outcome:** Freeze the utility bytes in the declared
order, before the later v8 plan/schemas exist. Give the builder a valid builder
authorization, then exercise an erroneous call from its entry point into the
shared Git process API with the literal HTTPS pair-push suffix. The design
specifies neither a non-forgeable builder capability nor a role check at that
shared API. The executable, endpoint, refs, and GCM route are fixed constants,
so the process already has enough ambient Windows authority to attempt the
network operation. Alternatively, if the implementation invents a closed
argument/predecessor grammar now, a later conforming v8 schema can choose a
different grammar and make every valid dispatch refuse. Both outcomes follow
from the same missing contract: role policy is postponed while the
role-neutral mechanism is already frozen.

**Violated invariant:** Least authority by role and acyclic, reviewable
bootstrap. Later artifacts may supply values; they cannot define which
operations an already reviewed tool is capable of performing.

**Required outcome:** Freeze, in this candidate family, the complete per-role
input grammar, predecessor-state schema, allowed operation set, output/receipt
equations, and a mandatory role-capability check at every shared authority API.
The future plan may bind concrete values and measured limits, but it must not
add a verb, endpoint class, ref class, file source, or argument interpretation.

**Verification criteria:**

1. A single frozen schema yields one canonical valid dispatch and oracle for
   each role without consulting an unlisted document.
2. With a valid authorization for each role, every cross-role common-library
   call refuses before opening a disallowed executable, repository, credential,
   or network path.
3. Unknown/extra/reordered arguments and mismatched predecessor fields refuse
   at the shared boundary, not only in entry-point control flow.
4. Consumer and generator fixtures independently reproduce every role contract.

**Advisory engineering technique:** Have authorization validation mint a
role-specific capability object whose methods expose only that role's closed
operations. Keep byte/JSON/process primitives below it, but do not export a
generic Git launcher to entry points.

### I-2 - Existing-file holds plus post-import inspection do not establish a pre-execution runtime boundary

**Severity:** Important. **Confidence:** High.

**Binding:** `ad8fbcc1ae5a9e3c3b61ae93d5ae5c0b3e4d289e` +
`862d245f838f4b7459b6ce2aae19eede3b77a4861575722817db12d63af7b689`.

**Frozen locations:**

- `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-runtime-boundary.md:
  361-380` holds existing files/directories, performs the last population check
  immediately before `CreateProcessW`, and claims those holds make late imports
  safe.
- The same file at lines 410-424 imports modules and loads native images first,
  then inventories, opens, hashes, and holds their origins. It names a Python
  audit hook but does not define the events, timing, or pre-execution loader
  that closes a newly appearing path.
- Lines 426-430 check again only at the next authority boundary.
- Lines 568-569 require only that ordinary `__pycache__` files are not selected
  and that a preexisting nonempty dynamic cache refuses; they do not cover a
  namespace addition between launch and import.

Windows sharing rules bind opens of the same file object; they are not a
specified immutable namespace mechanism here. CPython also warns that a
Python-level audit hook is not a sandbox and that a security-sensitive hook
needs to be installed natively before runtime initialization:
[Python 3.11 `sys.addaudithook`](https://docs.python.org/3.11/library/sys.html#sys.addaudithook).
Windows' unpackaged-process DLL search can include the current directory, which
this candidate fixes to the handoff repository:
[Microsoft DLL search order](https://learn.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-search-order).

**Concrete state -> wrong outcome:** Let the launcher's final population and
empty-pycache checks pass. After `CreateProcessW` but before the child imports a
needed nonfrozen module, a concurrent same-user updater that obeys ordinary
share semantics adds a new shadow source/cache entry under a searched
directory, or an unlisted delay-load DLL under a searched loader directory.
The child executes that byte before the lines 410-424 inventory/hold step.
The injected code can call Win32 or Git directly. A later origin, image,
pycache, or population mismatch converts the run to refusal, but it cannot undo
an authority mutation that the byte already performed.

**Violated invariant:** All non-TCB executable bytes and routing facts must be
validated and held before execution or authority access. Detection after code
runs is not preservation.

**Required outcome:** Specify and enforce a namespace and loader gate that
prevents any unlisted Python source/cache/native image from being selected
before its bytes are validated and retained. The guarantee must cover startup,
first imports, late imports, dynamic cache paths, native dependency search, and
the fixed working directory; post-load enumeration may remain defense in depth.

**Verification criteria:**

1. A deterministic barrier after the final parent check injects a shadow
   source, valid cache file, and native image before first/late import; no
   sentinel instruction from any injected byte executes.
2. The same schedule immediately refuses before repository, Git, credential,
   or network access.
3. The test proves pre-execution exclusion through the public launcher, rather
   than accepting a final mismatch after execution.
4. Native dependency search and every Python loader used by the three roles
   have enumerated, independently asserted pre-execution paths.

**Advisory engineering technique:** A private access-controlled runtime
snapshot or a native pre-initialization loader/audit boundary is easier to
reason about than post-import enumeration. If the existing installation is
retained, use a validating importer and an explicit safe DLL search policy, and
eliminate imports after the authority gate where practical.

### I-3 - The production HTTPS mutation boundary is represented by a local-transport double

**Severity:** Important. **Confidence:** High.

**Binding:** `ad8fbcc1ae5a9e3c3b61ae93d5ae5c0b3e4d289e` +
`862d245f838f4b7459b6ce2aae19eede3b77a4861575722817db12d63af7b689`.

**Frozen locations:**

- `docs/briefs/v0a-i01-freeze-tools-r001-brief.md:88-93` assigns publication
  rehearsal to a local transport and exercises the exact Git/GCM route only
  with a read-only observation.
- `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-design.md:198-215`
  claims coverage for atomic push, unsupported atomic push, lease conflict,
  timeout, retry, and lost acknowledgement, then separates local rehearsal
  from the literal live HTTPS endpoint.
- `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-git-boundary.md:
  470-480` requires query/fetch/push route checks but makes the only
  pre-push live exercise an `ls-remote`.
- Frozen `inputs/workflow.md`, Review checklist v1 item 1, requires the real
  production path under a real failure schedule, not a helper double.

**Concrete state -> wrong outcome:** The disposable bare remote accepts atomic
create-only pushes and the local fault shim supplies the expected timeout.
The exact HTTPS server instead omits or changes atomic capability behavior, the
push route starts an image that `ls-remote` never starts, GCM performs a
push-only approval/rejection action, or the HTTPS client loses its
acknowledgement after the server receives the update. All preregistered tests
remain green because no production-route mutation exercised those facts. The
first authorized live pair push is therefore the first test of the material
boundary; it may leave a detected PARTIAL/UNKNOWN residue or consume the only
live attempt despite a claimed accepted rehearsal.

**Violated invariant:** Falsifiable acceptance and the literal helper-double
rule. Local Git plumbing can test the state machine, but it cannot establish
HTTPS helper, GCM, server capability, lease, and acknowledgement behavior.

**Required outcome:** Add a separately authorized disposable HTTPS/GCM
mutation target that uses the exact production executable/helper/shell route
and server class while being unable to address live task refs. Exercise atomic
pair creation, exact leases, rejection, timeout, fresh observation, and
lost-ack recovery there. If no such target is available, narrow the claimed
evidence and keep live mutation blocked.

**Verification criteria:**

1. The tested process tree, environment, helper, credential mode, URL scheme,
   protocol, and server atomic capability match the live boundary.
2. The test performs real create-only pair mutation and proves no sequential or
   partial publication is treated as authority.
3. A real transport-level lost acknowledgement is reconciled from a fresh
   query, and an AA/PARTIAL/DIFFERENT/UNKNOWN result has the specified outcome.
4. The rehearsal namespace cannot select any production task or integration
   ref, even under malformed dispatch.

**Advisory engineering technique:** Use a dedicated private rehearsal
repository or server-side namespace with independently enforced ref prefixes.
Keep the local bare-remote suite for fast state-machine coverage.

### I-4 - The selected GCM route permits deletion of credential authority on a failure path

**Severity:** Important. **Confidence:** High.

**Binding:** `ad8fbcc1ae5a9e3c3b61ae93d5ae5c0b3e4d289e` +
`862d245f838f4b7459b6ce2aae19eede3b77a4861575722817db12d63af7b689`.

**Frozen locations:**

- `docs/briefs/v0a-i01-freeze-tools-r001-brief.md:50-51` says no failure path
  deletes an object, ref, packet, report, or other authority.
- Its lines 80-84 say the design does not defend Windows Credential Manager.
- `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-git-boundary.md:
  117-144` deliberately permits GCM `get`, `store`, and `erase`, and defers the
  decision whether mutation is forbidden.
- The same file at lines 479-480 postpones that decision to rehearsal.

Git's credential contract sends rejection to helpers that may erase persistent
credentials:
[Git credential](https://git-scm.com/docs/git-credential) and
[Git credentials](https://git-scm.com/docs/gitcredentials.html).

**Concrete state -> wrong outcome:** Windows Credential Manager contains the
only token that can publish the pair. A read-only `ls-remote` receives a 401
because the token is stale or the server transiently rejects it. Git reports
the credential as rejected; the configured GCM helper receives `erase` and
removes the matching stored token. The tool classifies the remote observation
as unavailable/UNKNOWN and preserves Git refs, but a failure path has deleted
the durable credential authority and changed the precondition for every fresh
recovery attempt.

**Violated invariant:** Monotonic durable state and fresh-state recovery without
rollback or deletion.

The stronger text is the positive no-deletion acceptance criterion. The weaker
Credential Manager nonclaim and the conditional wording in the Git insert must
be amended; they cannot silently exempt a credential that is itself remote
mutation authority.

**Required outcome:** Select a credential route before implementation that
cannot store or erase the durable credential during query, fetch, push, timeout,
or authentication rejection, or obtain an explicit controller ruling that
redefines the authority boundary and supplies recovery. Without that resolved
contract, live Git/GCM execution remains blocked.

**Verification criteria:**

1. Snapshot an isolated credential-store fixture, exercise success,
   authentication rejection, transport failure, timeout, and cancellation, and
   prove byte/state equality afterward.
2. No invoked helper operation can mutate the production credential store
   during read-only observation or failed publication.
3. Recovery from every remote result depends only on fresh refs/objects and
   does not require reconstructing a credential deleted by the tool.

**Advisory engineering technique:** Use a preauthorized read-only credential
adapter for observation and a one-use injected credential for mutation, with
`store` and `erase` ignored by construction. Review that route separately
because it changes the TCB and secret-handling boundary.

### I-5 - Utility-review provenance has contradictory cardinality and no exact review-to-role relation

**Severity:** Important. **Confidence:** High.

**Binding:** `ad8fbcc1ae5a9e3c3b61ae93d5ae5c0b3e4d289e` +
`862d245f838f4b7459b6ce2aae19eede3b77a4861575722817db12d63af7b689`.

**Frozen locations:**

- `docs/briefs/v0a-i01-freeze-tools-r001-brief.md:52-54` requires two
  independent reviews binding the whole frozen utility commit and manifest.
- `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-design.md:131-149`
  likewise shows two reviews before one utility-review projection.
- `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-runtime-boundary.md:
  145-151,189-195` requires two utility-only reviews for each of four roles and
  exactly eight receipt objects with unspecified distinct-reviewer rules.
- `docs/superpowers/specs/2026-09-01-raw-object-workflow-amendment-v4.md:
  83-104` says every required reviewer is distinct, but its per-review
  projection fields do not include the reviewed utility role or utility digest.

**Concrete state -> wrong outcome:** Two blind reviewers each review the frozen
bundle as the brief requires and each issues one report/ledger line. The runtime
validator expects eight receipt objects and refuses a valid two-review packet.
If the coordinator instead expands those two reports into four role slots per
reviewer, a literal global interpretation of 'required reviewers are distinct'
rejects the duplicates. If it treats ordinal/path convention as the missing
role relation, a launcher or builder receipt can be assigned to a publisher or
integrator slot without a schema-level mismatch. The first two outcomes make
the bootstrap impossible; the third can grant utility authority with a missing
role-specific review.

**Violated invariant:** Byte-bound, single-writer, nonrecursive review
provenance with deterministic distinctness and complete role coverage.

**Required outcome:** Define one exact relation among reviewer identity,
bundle report, utility role, utility digest, receipt, ledger line, and
projection row. State whether the intended population is two bundle reports,
eight role receipts from two reviewers, eight distinct reviewers, or another
closed set; scope reviewer distinctness explicitly. Every role slot must carry
its role and utility digest as data, not infer them from a path.

**Verification criteria:**

1. A canonical valid fixture has one unambiguous count for reports, receipts,
   ledger lines, reviewers, and role slots.
2. Duplicate reviewer within a role, author/reviewer overlap, missing role,
   wrong utility digest, cross-role replay, duplicate ordinal, and synthesized
   non-issuer ledger bytes each refuse.
3. The two issuer-authored report/ledger populations required by the brief can
   be projected without another actor inventing or normalizing review bytes.
4. Every projection field is reproduced from a closed structured receipt or an
   exact report grammar, including the design-justification digest.

**Advisory engineering technique:** Model the required set as the explicit
cross-product `{reviewer-01, reviewer-02} x {launcher, builder, publisher,
integrator}` while keeping one bundle report and one ledger line per reviewer,
then bind four role attestations inside each issuer-authored structured receipt.

## Architecture assessment

The launcher/builder/publisher/integrator decomposition is salvageable and is
preferable to one mode-switched authority program. The current shape is
strained because the role-neutral common layer owns all process mechanisms
while role grammar lives later, and because detection/evidence is placed after
the runtime or transport boundary it is meant to prove. Freeze the capability
contract with the tools, move runtime exclusion before execution, and exercise
the exact HTTPS mutation boundary. The cost is a bounded schema/capability
appendix, a launcher/import-boundary refinement, and a dedicated remote
rehearsal target; the four top-level components need not be replaced.

## Evidence and limits

All Git inspection was read-only against frozen objects. The initial handoff
repository read hit Git's ownership guard; it was retried under narrowly scoped
read-only elevation without changing `safe.directory` or repository state.
Blob hashes and sizes were streamed in memory. The runtime JSON was parsed in
memory; the pinned interpreter and every candidate artifact remained
unexecuted. No implementation tests, repository mutations, ref updates, live
remote query, credential access, experiment, or unlisted artifact inspection
was performed. The cached origin-tracking ref corroborates the pushed value,
but this review did not refresh network state.
