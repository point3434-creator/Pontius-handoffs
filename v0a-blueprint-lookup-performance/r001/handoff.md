# One opposing review: lookup performance r001

Review the candidate overlay in identity.json on its frozen base commit. No verdict is requested
from a second reviewer. The drafter is Codex; Claude is the intended opposing reviewer.

Start with this handoff and identity.json. Verify the base commit/tree from read-only Git in the
declared checkout, then recompute the whole-row sorted manifest from raw packet bytes. Read source/
and relevant frozen base source to derive and seal your own invariant inventory before opening
coverage.md or checks/. base-src.zip is an exact archive of base src/ blobs, verified by the author.
Unchanged tests/tools may be read with git cat-file at the declared base commit.

Do not open prior reviews, ledgers (progress.md, INDEX.md, execution_journal.jsonl), memory,
conversation history, unrelated scratch, or another reviewer's inventory. The checked test
journal-row copy in checks/ is permitted after inventory. Disclose any context exposure; do not
call a pass cold if it is not. Use a unique scratch directory for your inventory and report.

Check canonical and provider identities, field admission, equality/hash/copy/pickle behavior,
default/illegal action behavior, cold/warm work and memory cost, and the actual call paths.
Confirm the integration test copies the changed lookup into its private execution checkout.
The direct immutable-source API assumes an unmodified frozen graph; decide whether the documented
cache behavior preserves that contract at all consumers. Keep the library/provider paths separate.

Use Python 3.14 only. Read-only source and pure checks in isolated scratch are permitted; do not
invoke a retained phase, alter source/packets/retained records, commit, push, or launch more reviewers.
Return one report and inventory; Critical/Important findings need a reachable path, governing
requirement and falsifier. Distinguish material defects from documentation advisories. A further
round is justified by a material unresolved issue or changed executable behavior, not an advisory.
This packet requests review only and supplies no adoption or run authority.
