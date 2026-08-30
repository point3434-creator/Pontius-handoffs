# R2-03 host failure closure — handover to a new implementer

Author: Claude (outgoing implementer), 2026-08-30.
Trigger: fourth residual at r006. The condition recorded in the r006 handoff
and carried forward by the r006 disposition — "no fifth attempt is assigned to
the current author" — has fired. This document is the package the disposition
asks the next owner to receive.

## Standing

| Item | Value |
| --- | --- |
| Last frozen candidate | `c74b80628a89938ca585ef3240b5c267a7174d0f` (r006) |
| Manifest | `2078d59a4a112bf29a2bd9faca9a2ca070bbd1028a940f2eeb617c9e1c31555f` |
| Base | `b357d333fc2393b7fc7dcf31f30c86616208c817` |
| Tests passing | 123 per interpreter, actual CPython 3.11.15 and 3.14.6 |
| Contract state | OPEN — two Important mechanisms (R6-01, R6-02) |
| Design verdict | STRAINED in both cold reports; the *contract* is SOUND |

Scope of replacement is bounded: the error adapter. The hand loop, sealed
ledgers and spine, timing ownership, delivery and record preservation, the
append-only journal, and placement inside the measurement boundary are all
endorsed and should be kept. The evidence does not justify discarding the hand
implementation.

## What is already correct — do not regress these

Each was a finding in its own round and is now closed with tests that go RED
against the prior frozen candidate:

- initiating cause journalled before its own cleanup (`dispatch`, R4-02);
- first observed typed cause is primary regardless of category — no reporting
  exemption (R4-01);
- the abort-cleanup seam retains its cause (R4-02);
- a body error precedes its cleanup fault (R5-01);
- a genuinely fresh body-origin witness failure reaches the receipt (R5-02);
- delivery counting follows acknowledgement, including late deliveries (R2-08);
- full settlement comparison including final stacks and pot eligibility (R2-07);
- no host-side exception escapes for ordinary message controls (G1, partial —
  see R6-02).

The opposing controls matter as much as the fixes: several are the reason a
naive correction of R6-01 would regress R5-02.

## The two open mechanisms

**R6-01 — a failed-witness refusal is journalled as a second cause.**
`runtime.py:414-416` (owner body handler) interacting with `:337-344`. Fail the
shared witness at settlement-interval entry, then sample it from the public
oracle: the source fails once and is never retried, but the dead witness's
later refusal is recorded as a new `clock_invalid`. Expected one cause; actual
two. The fix must distinguish a genuine occurrence from a synthetic refusal —
**not** by deduplicating the enum, and without dropping fresh body-origin
faults, which are the r005 controls.

**R6-02 — failure normalization can escape.** `runtime.py:416`, duplicated at
`:429`. The owner evaluates `str(error)` while constructing `OperationFailed`;
a body error whose string conversion itself raises escapes `run()` after real
actions were delivered, leaving no completion receipt. The coordinator further
showed that `isinstance` classification can be subverted by an
exception-defined `__class__` — raising before retention, or mislabelling an
ordinary exception as `clock_reversed`. Treat the whole
inspect-convert-propagate route as one boundary; removing the `str` call alone
is not closure of the class.

## Why I failed, stated plainly for whoever takes this

Four attempts, and the same error in each: **I apply a correct principle at the
site the finding named, and not at the other sites where the principle holds.**

- r003: fixed escapes and false success; discarded the typed cause.
- r004: retained causes at the five named seams; missed the abort seam.
- r005: fixed ordering in `dispatch`; missed the host's own body/cleanup pairs.
- r006: built an owner so the site could not differ — then omitted the echo
  rule *inside that owner*, which is R6-01.

r006 is the sharpest illustration: I built a mechanism specifically to stop
relying on my recall, and then relied on my recall for one of its two rules.

Two things follow for the next owner. First, the remaining work is an
error-adapter boundary where every rule must hold on every path — genuine
versus synthetic origin, safe classification, safe transfer — so it rewards a
single implementation with no per-path judgement. Second, my coverage claims
were attacked and failed three times because the category I drew was too
narrow; take the category from the r006 disposition ("fresh fault versus
failed-witness refusal, normal versus fallible message/metadata, before versus
after cleanup, and exact multiplicity") rather than from my framing.

## Verification that must survive

- The conservation observer (`R2_03ConservationTests`): wraps the sealed ledger
  and asserts the receipt's ordered clock causes **equal** the genuine raises.
  It is stated in contract terms and should survive your reimplementation. Note
  the coordinator's caveat: presence-only assertions miss extra causes, which
  is exactly R6-01 — compare complete sequences and multiplicity.
- The AST guard against reaching an unowned interval: useful supporting
  coverage, not proof of origin or retention.
- Full-observation sweeps on both fixtures, both fault kinds.
- The opposing controls that a fix for R6-01 could regress.

## Materials

- Frozen candidates and manifests: r001–r006 packets in this directory.
- Root-cause history: `R2-03-root-cause.md`, including the r005 supplement.
- Failing diagnostics and passing controls: each round's `checks/`.
- Dispositions: `r00N/disposition.md`, with r006's addendum withdrawing the
  fabricated-marker finding to advisory.

R3-01 policy authority remains separately open with its own root-cause note at
`R2-01-root-cause.md`; it is not part of this handover.
