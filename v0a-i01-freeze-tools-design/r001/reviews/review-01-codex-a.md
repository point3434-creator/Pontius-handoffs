# Cold design review: v0a-i01-freeze-tools-design/r001

Reviewer ID: codex-a
Candidate commit: ad8fbcc1ae5a9e3c3b61ae93d5ae5c0b3e4d289e
Manifest SHA-256: 862d245f838f4b7459b6ce2aae19eede3b77a4861575722817db12d63af7b689
Defect verdict: NOT CLEAN
Design verdict: WRONG SHAPE

All locations below are line numbers in blobs at the candidate identity above, except
`inputs/*`, which are blobs at immutable handoff commit
`852c10645924aa9602f0d31c5d37806e0a9ec6df`. This report is based only on the
complete cold-input set named by that handoff.

## Frozen identity and input verification

- The local candidate ref and its stored `origin` tracking ref both resolve to the stated
  object. The commit has exactly one parent,
  `d1ed3cbda6107d61ea8e77133871720af04970cd`, and tree
  `e8de257880c1a034091034fd17a6c4e2c6a5bfdb`.
- The parent-to-candidate diff is exactly the five declared additions. Every candidate
  entry is an ordinary `100644` blob; every corresponding base path is absent.
- `manifest.sha256` is 658 bytes and hashes to the stated identity. Its five rows are
  whole-row byte sorted, and each row digest independently reproduces from the frozen
  candidate blob.
- `inputs/workflow.md` is 30,942 bytes and hashes to
  `ab5202b170a5fd9c2cf1540aa198d4a82c742cb336134b0f9a8db944fd64f91a`.
  `inputs/runtime-closure.json` is 413,522 bytes and hashes to
  `3390ab3d041d432f06754ca94aed348774c421de1c14553a25395c2cab112a3a`.
- Read-only structural parsing of the runtime closure found 2,614 rows totaling
  63,499,244 bytes, ordinal path order, no exact or case-fold duplicate path, valid
  lowercase digests, and the declared `python.exe` row. The JSON is UTF-8, LF-only,
  no-BOM, and final-LF.
- The five candidate blobs are UTF-8, LF-only, no-BOM, final-LF, and have no trailing
  whitespace. Two URL lines exceed the adopted 100-column rule; this is recorded below.

No live remote query was made. It would not be a frozen input and, with the proposed GCM
route, can itself invoke credential `store` or `erase`. The branch and stored tracking-ref
identity checks plus direct object-store checks establish the review target available in
the cold repository.

## Governing invariants recorded before assessment

1. Bootstrap authority is acyclic: an unreviewed utility cannot freeze, publish, review,
   attest to, or preserve itself. Every later authority value is derived from an earlier
   immutable value or supplied by the trusted controller.
2. Each process receives only its role's capability. In particular, the builder has no
   network or credential route; the publisher cannot update main; the integrator cannot
   create or publish the candidate pair.
3. Every executable, Python source, native image, runtime data byte, route, argument, and
   environment value that can affect authority is either byte-bound and held for the
   complete interval or explicitly inside the stated trusted computing base.
4. Git object bytes are deterministic functions of declared inputs. Checkout, index,
   filters, attributes, normalization, ambient identity, clock, and configuration cannot
   affect an object or manifest.
5. Durable tuples are classified from one fresh complete observation. Unknown information
   dominates; only absence permits create and only exact state permits idempotent recovery.
6. Failure is monotonic. It may leave unreachable objects or immutable authority, but it
   cannot delete or roll back an object, ref, report, credential authority, or provenance.
   Recovery starts from fresh state rather than a remembered process result.
7. Generated handoff semantics and utility-review provenance are canonically derived and
   byte-bound without a digest depending on its own eventual content.
8. Every child and descendant is owned through quiescence, output is bounded, and no
   successful result escapes before final identity and state reconciliation.
9. Each material claim has an independent falsifying test at the real process, file,
   object, ref, credential, or reviewer-output seam. Hard walls carry measurement
   provenance and the complete matrix fits the declared size budget.

## Systematic seam inventory

- **Adopted Stage 2 to utility review.** Existing trusted route alone must create the
  frozen utility pair and immutable reviews. The acyclic shape is present; provenance
  extraction remains open (Finding 6).
- **Controller to launcher.** Authorization, launcher, role, common source, arguments,
  environment, and argv must be held. The shared source has no coherent identity or
  origin category (Finding 2).
- **Launcher to CPython.** The complete runtime population must be held, with the exact
  root child, pipes, Job, handshake, and final rehash. The file population is coherent;
  non-module data access is not confined (Finding 3).
- **Role to shared Python mechanism.** Only role-authorized calls and facts may be
  reachable. The common module contains cross-role Git capability (Finding 1).
- **Python to Git root.** The application path, quoting, handles, environment, config,
  wall, and output must be fixed. Root launch is specified; commit identity inputs are
  absent (Finding 4).
- **Git to HTTPS, shell, and GCM.** URLs and executables must be pinned without mutable
  credential side effects. The executable route is detailed; persistent credential
  mutation is allowed (Finding 5).
- **Raw bytes to objects and manifest.** Blob, tree, and commit bytes need independent
  reparse without an index or checkout. Blob and tree construction is coherent; commit
  construction is not deterministic (Finding 4).
- **Local intent, candidate, and packet refs.** Only an absence-to-exact transition may
  mutate refs. The static state shape is coherent; executable crash evidence is deferred.
- **Remote candidate and packet pair.** One strict observation, atomic create-only push,
  and mandatory reobservation are required. The `AA`, `EE`, partial, different, and
  unknown precedence is coherent statically.
- **Packet to main.** Receipt-only ancestry, an exact lease, protected subtree, and
  descendant walk are required. The shape is stated; final schema and executable
  rehearsal remain prerequisites.
- **Cold spec to generated handoff.** Exact schema, template, and derived identity must
  replace free-form authority. Acyclic generation is stated; downstream schema proof is
  deferred.
- **Reviewer output to projection and main.** Immutable issuer bytes, exact semantic
  equality, and a single-writer ledger are required. Byte transport is stated; semantic
  derivation is not closed (Finding 6).
- **Timeout or crash to recovery.** Kill, active-zero proof, fresh classification, and
  monotonic residue are required. Ref reconciliation is stated; credential residue
  violates monotonicity (Finding 5).

## Required findings

### Important 1 — the builder still loads a network-capable authority layer

**Confidence:** High.

**Binding:** `ad8fbcc1ae5a9e3c3b61ae93d5ae5c0b3e4d289e` /
`862d245f838f4b7459b6ce2aae19eede3b77a4861575722817db12d63af7b689`.

**Frozen locations:**
`docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-design.md:46-63`,
`:86-108`; `docs/briefs/v0a-i01-freeze-tools-r001-brief.md:36-38`.

**Evidence and concrete wrong outcome:** The design rejects one multi-mode program because
one routing defect could cross from the offline role into network or main authority. It
then places Git process control, the exact Git environment and arguments, ref validation,
timeout handling, and reconciliation in the one shared module loaded by all roles. The
builder claim is nevertheless “no network verb or credential route.” With a builder
authorization and an exact local candidate/packet graph, one ordering or operation-table
defect in a common repository-validation path can issue the literal pair `ls-remote`
before validating the publisher role. That contacts the live endpoint and invokes the
credential route from a process that was promised no such capability. A wrong common
operation selection can go further and attempt the already-known pair refspecs. Separate
entry-point filenames do not prevent this because the authority-bearing mechanism and
route constants are already in the builder process.

**Violated invariant and conflict:** Least authority per role. The stronger invariant is
that the builder cannot express or reach a network operation. The weaker text at design
lines 46-63 and 86-108 centralizes exactly that route behind another role check, recreating
the rejected failure shape.

**Required outcome:** Move network suffix construction, credential environment, and
publisher/main transition capability outside every source and object loaded by the
builder. A shared layer may retain pure codecs, identity comparison, and a process owner,
but it must not accept an open-ended Git argv or an authority-operation selector.

**Verification criteria:** Through the real launcher and Git process boundary, exercise
all builder dispatch variants, malformed values, recovery branches, and injected
operation-selection faults while independently observing process creation and network
access. No HTTPS helper, shell, GCM, `ls-remote`, `fetch`, or `push` may start. A static
dependency/capability inventory must independently show that no builder-loaded source
contains or imports a network/main operation table. Helper doubles alone do not satisfy
this criterion.

**Advisory technique:** Split the current common module into a pure validation/process
kernel and role-specific capability modules, and let the launcher admit only the selected
role module and its closed command vocabulary.

### Important 2 — the required shared Python source is simultaneously unbound and forbidden

**Confidence:** High.

**Binding:** `ad8fbcc1ae5a9e3c3b61ae93d5ae5c0b3e4d289e` /
`862d245f838f4b7459b6ce2aae19eede3b77a4861575722817db12d63af7b689`.

**Frozen locations:**
`docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-design.md:86-102`;
`docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-runtime-boundary.md:187-195`,
`:410-424`, `:485-500`.

**Evidence and concrete wrong outcome:** Every entry point must load
`tools/handoff_freeze_common.py` from an external absolute path. The runtime check permits
`__main__` at the external role path but requires every other file-backed module origin to
be a runtime-inventory row. The runtime inventory is rooted under the CPython installation,
so a normal import of the common module refuses before `RUNTIME_LOCKED`. Avoiding the
refusal by manually executing bytes outside `sys.modules` makes the origin inventory
incomplete. Independently, the closed authorization row descriptions cover plan/schema/
workflow inputs and the launcher plus three entry points, while the exact four-key
`utility_sha256` object omits the common library. Thus a permissive implementation can run
the shared authority code without a field-exhaustive review/authorization identity.

**Violated invariant and conflict:** Every executed non-TCB source must be held, reviewed,
authorized, and represented in runtime-origin evidence. The stronger source-closure
invariant conflicts with the weaker “every other module origin” rule and four-key utility
map; both must be amended rather than bypassed.

**Required outcome:** Give every shared authority source an explicit closed identity class
in the plan, launch authorization, review receipts/projection, packet inventory, runtime
handshake, and used-source revalidation. Permit exactly those authorized external origins
alongside `__main__`; do not hide them from module accounting.

**Verification criteria:** The real entry point must load the exact common source and reach
the handshake successfully. Changed bytes, same bytes at a wrong path/FileIdInfo, an
unlisted second external module, an omitted review binding, or a receipt with a different
common identity must refuse before repository or network access. The receipt round trip
must enumerate the common source field exhaustively.

**Advisory technique:** Define each Python utility identity as a reviewed tuple of its
entry point plus the exact shared-source population, rather than treating one file digest
as the utility.

### Important 3 — module/image auditing does not enforce the claimed runtime-data boundary

**Confidence:** High for the missing enforcement mechanism; medium for which standard
library path would first trigger it in the eventual role imports.

**Binding:** `ad8fbcc1ae5a9e3c3b61ae93d5ae5c0b3e4d289e` /
`862d245f838f4b7459b6ce2aae19eede3b77a4861575722817db12d63af7b689`.

**Frozen locations:**
`docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-runtime-boundary.md:16-20`,
`:60-71`, `:404-428`; `inputs/runtime-closure.json:1`, JSON pointers
`/inventory/included_populations`, `/inventory/root_directories`, and the rows for
`DLLs/_tkinter.pyd`, `DLLs/tcl86t.dll`, `DLLs/tk86t.dll`, and
`Lib/tkinter/__init__.py`.

**Evidence and concrete wrong outcome:** The closure admits every file in `Lib` and `DLLs`,
including Tkinter and its native Tcl/Tk images, but expressly excludes all files below the
root `tcl` directory. The text claims that any runtime-data access to an excluded directory
refuses. The enforcement described later inventories `sys.modules` origins and currently
loaded images and uses a Python audit hook for later origins; it specifies no OS-enforced
file-read boundary and no complete native data-access census. An inventory-admitted import
can therefore instantiate Tcl/Tk. Native Tcl can read scripts below the excluded `tcl`
tree, and Tk can read profile files from the process working directory. Those bytes can
affect the process while every module origin and loaded-image identity remains exact. The
child can then emit the runtime lock and perform an authority transition using state
influenced by unheld bytes. Python documents that `sys.addaudithook` is not a sandbox, so
it cannot establish the missing denial boundary by itself.

**Violated invariant and conflict:** Complete runtime/input byte closure. The stronger
invariant requires every influencing file byte to be held or trusted. The weaker text
claims a full closure without transitive prediction while allowing the full standard
library and observing only module/image state.

**Required outcome:** Either establish an OS-enforced read boundary that admits only held
runtime/source/input/System32/temp identities, or define and bind a closed per-role import,
native-image, and runtime-data population that excludes facilities whose reads cannot be
accounted for. Include every admitted Tcl or other native data file if such facilities
remain reachable.

**Verification criteria:** In a disposable runtime and repository, place distinct marker
bytes in an excluded runtime-data path and in a profile/data file under the working
directory. Exercise an otherwise inventory-admitted Python/native path through the real
launcher. Independent OS-level observation must prove the read is denied before the byte
can affect execution and before `RUNTIME_LOCKED`; a marker read followed by a clean module/
image inventory must fail the test. Repeat for late load, timeout reconciliation, and the
final success boundary.

**Advisory technique:** A small sealed per-role runtime/data projection is easier to prove
than treating all of `Lib` and `DLLs` as executable capability and attempting to discover
data reads afterward.

### Important 4 — deterministic commit creation has no legal identity or clock inputs

**Confidence:** High.

**Binding:** `ad8fbcc1ae5a9e3c3b61ae93d5ae5c0b3e4d289e` /
`862d245f838f4b7459b6ce2aae19eede3b77a4861575722817db12d63af7b689`.

**Frozen locations:**
`docs/superpowers/specs/2026-09-01-raw-object-workflow-amendment-v4.md:41-57`;
`docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-git-boundary.md:146-199`,
`:201-251`, `:253-269`.

**Evidence and concrete wrong outcome:** The raw route requires deterministic
`git commit-tree` metadata. Git commit objects include author name, email and date plus
committer name, email and time. The design's complete Git environment contains no
`GIT_AUTHOR_*` or `GIT_COMMITTER_*` variables, its exact repository config contains no
identity, and extra environment/config entries are forbidden. In the declared clean
repository the builder therefore fails with missing identity. If an implementation widens
the boundary to use ambient identity or current time, two runs over identical tree and
parent bytes produce different commit OIDs, so the declared candidate/packet graph is not
a deterministic function of its authorization.

**Violated invariant and conflict:** Exact raw-object determinism and no ambient Git input.
The stronger invariant is exact commit bytes from controller-bound values. The weaker
`commit-tree metadata` sentence and closed Git environment must be made coherent.

**Required outcome:** Canonically specify every commit header and message byte, including
author/committer names, emails, timestamps and offsets. Either serialize the complete
commit bytes and write them with `hash-object -t commit`, or admit exact role-scoped
metadata variables into the constructed Git environment. No clock or config fallback is
permitted. Apply the same rule to packet, publication-receipt, integration, and reviewer-
output commits.

**Verification criteria:** Two clean repositories, different wall-clock times, and poisoned
parent/global identity settings must produce byte-identical commit objects and OIDs for
the same dispatch. Missing, extra, malformed, reordered, or changed metadata must refuse
before any ref transaction. Independent raw-object parsing must compare every header,
parent, tree, separator, message byte, and final newline with the authorized encoding.

**Primary semantic basis:** Git's `commit-tree` documentation states the author/committer
identity and time fields and the environment-controlled date formats:
<https://git-scm.com/docs/git-commit-tree>.

### Important 5 — the accepted GCM route can delete persistent credential authority

**Confidence:** High.

**Binding:** `ad8fbcc1ae5a9e3c3b61ae93d5ae5c0b3e4d289e` /
`862d245f838f4b7459b6ce2aae19eede3b77a4861575722817db12d63af7b689`.

**Frozen locations:** `docs/briefs/v0a-i01-freeze-tools-r001-brief.md:47-51`;
`docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-design.md:179-189`;
`docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-git-boundary.md:133-160`,
`:472-481`.

**Evidence and concrete wrong outcome:** The stronger brief says no failure path deletes an
object, ref, packet, report, or other authority, and the common state model allows no
rollback. The Git insert selects persistent `wincredman` storage while expressly allowing
GCM `get`, `store`, and `erase`, deferring the decision whether that mutation is allowed.
For a stored credential followed by a server-side authentication rejection, Git reports a
credential reject and the helper may erase the matching Windows Credential Manager entry.
The ref observation then yields refusal or unknown, but durable credential authority has
already been deleted. A fresh retry no longer observes the same predecessor state and may
be unavailable. A successful request may likewise store changed credential state.

**Violated invariant and conflict:** Monotonic failure residue and no deletion of authority.
The stronger invariant is brief lines 50-51. The conditional permission at Git-boundary
lines 141-144 and 479-481 is the weaker text that must be amended; the review cannot
silently treat credentials as outside “other authority.”

**Required outcome:** Use a controller-authorized credential route whose live `get`,
success, rejection, timeout, and cancellation paths cannot store or erase persistent
controller credentials, or obtain an explicit controller ruling that changes the stronger
invariant and then re-review the enlarged side-effect boundary. This review does not grant
that enlargement.

**Verification criteria:** Against an isolated credential target, record entry identity and
metadata without exposing secret bytes, then drive successful authentication, rejected
authentication, nonzero exit, timeout, and lost acknowledgement through the real Git/GCM
route. The before/after credential population must be identical and no `store` or `erase`
effect may occur; a fresh read-only retry must still obtain the same credential authority.

**Primary semantic basis:** Git documents that credential rejection may erase a matching
stored credential and that helper `erase` removes matching credentials:
<https://git-scm.com/docs/git-credential> and
<https://git-scm.com/docs/gitcredentials>.

### Important 6 — review provenance fields are immutable but not canonically derivable

**Confidence:** Medium-high.

**Binding:** `ad8fbcc1ae5a9e3c3b61ae93d5ae5c0b3e4d289e` /
`862d245f838f4b7459b6ce2aae19eede3b77a4861575722817db12d63af7b689`.

**Frozen locations:**
`docs/superpowers/specs/2026-09-01-raw-object-workflow-amendment-v4.md:82-110`,
`:231-259`; `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-runtime-boundary.md:485-500`.

**Evidence and concrete wrong outcome:** The projection must claim verdicts, a
`design-justification` digest, implemented-role population, and whether candidate artifacts
were read, and must prove that these reproduce an immutable Markdown report. Review output
also contains a “structured receipt,” but the complete cold set defines neither that
receipt's closed schema nor the exact report byte ranges/normalization from which those
semantic values are derived. The self-excluding output manifest explicitly names report
and receipt, while the separately authored ledger-line bytes are not named as a manifest
member. Consider an immutable report saying `NOT CLEAN` or disclosing a candidate read and
an immutable receipt saying `CLEAN` and `false`. One finalizer can trust the receipt while
another parses prose differently; both can bind the same report hash. The first can issue
a controller-authorized projection that downstream tools accept even though its semantic
claim does not reproduce the report.

**Violated invariant and conflict:** Byte-bound, nonrecursive utility-review provenance.
The stronger invariant requires one deterministic derivation from issuer bytes. The weaker
text says values “reproduce” a report without defining the derivation or complete output
manifest population.

**Required outcome:** Define a closed canonical reviewer-receipt schema authored by the
reviewer, exact equality rules between its fields and the report's required single
occurrences, an unambiguous justification byte span or make the receipt the sole semantic
source, and a self-excluding manifest that binds report, receipt, and exact ledger line.
The projection must reject any disagreement rather than choose an interpretation.

**Verification criteria:** Freeze reports containing duplicate labels, alternate case,
line-ending changes, empty/multiple justification sections, contradictory receipt fields,
changed ledger spacing, reviewer/author overlap, and false read attestations. Independent
producer and finalizer implementations must derive the same bytes and must refuse every
conflict before creating a projection or advancing main. A clean control must round-trip
field-exhaustively from frozen issuer output to projection.

**Advisory technique:** Keep prose non-authoritative and make a canonical reviewer-signed
receipt the only machine semantic record; require the visible report labels to equal it for
human consistency.

## Design assessment (advisory)

The outer bootstrap sequence and the atomic pair-state table are promising. Two central
choices nevertheless defeat the properties they were selected to establish. The single
shared Python module puts cross-role Git capability back behind a routing check, and the
full-runtime-plus-audit model cannot confine non-module file reads while deliberately
avoiding a per-role dependency closure. Findings 1 through 3 are consequences of those
shapes rather than isolated wording mistakes.

Before implementation, replace the shared authority module with a pure common kernel plus
closed role-capability modules, and replace after-the-fact runtime data discovery with a
sealed per-role runtime/data projection or a real OS-enforced read boundary. Then add the
common-source identity and canonical review receipt as first-class schema members. The
cost is one new design round, regenerated authorization/receipt schemas, a split of the
planned shared library, and additional real-boundary tests. No implementation exists yet,
so this is materially cheaper than discovering the same boundary failures after the tools
gain live ref and credential access.

## Nonblocking observations and residual gaps

- `docs/superpowers/specs/2026-09-01-v0a-i01-freeze-tools-git-boundary.md:492`
  is 104 columns and line 495 is 101 columns. `inputs/workflow.md:486-488` requires every
  changed file to stay at or below 100 columns. This is a Minor exactness correction.
- Git-boundary line 406 freezes a 60,000 ms operation wall, while the adopted checklist at
  `inputs/workflow.md:479-480` requires calibration provenance for every hard wall. The
  cold set contains no such measurement. Treat the wall as an unresolved live-use
  prerequisite unless the next frozen round includes the pinned calibration source.
- Static text gives a conservative remote-pair table. No executable evidence is available
  here for local `.lock`/pack residue after forced Job termination, main-descendant races,
  output-cap overflow, or stale-lock recovery. The implementation rehearsal must classify
  those cases without deleting an authority object or ref.
- The proposed tests are category lists rather than an executable coverage map. The next
  round should map each invariant and every finding criterion above to a public-boundary
  test and show that the parameterized matrix fits the 2,500-line test budget.

## Evidence limits and actions deliberately not performed

The review used read-only `rev-parse`, `cat-file`, `diff-tree`, `ls-tree`, and in-memory
SHA-256/JSON checks over frozen Git objects. Primary Git, Microsoft, and CPython
documentation was consulted only for API semantics. In particular, CPython documents that
Python audit hooks are not a sandbox:
<https://docs.python.org/3/library/sys.html#sys.addaudithook>, and Tkinter documents its
native Tcl/Tk bridge and profile-file reads:
<https://docs.python.org/3/library/tkinter.html>.

Per the handoff, I did not start the pinned CPython runtime, execute a candidate artifact,
run implementation tests, use a checkout/index as byte authority, mutate any ref or remote,
read mutable packet state, inspect another reviewer output, or implement a correction.
