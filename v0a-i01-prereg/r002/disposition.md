# r2 returned-review disposition and pre-edit counterexamples

Issuer: /root, implementer assessment. Date: 2026-08-30.
Candidate: 119411fda2376d61d9ff310bada71f25aa64de70.
Manifest: da3c4ad5290a49f9d6e600b61e3190047ca6221394a4fc4ad06e40af727d799c.
Claude report SHA-256: e92dde4cc3747417093dd3bb968120ebee4e78814498a5a728c556f6ebcdd539.

The full candidate/ref/base and two-row blob manifest were independently verified,
as were Claude's exact binding and single attributed ledger entry. Claude's CLEAN
verdict and the other reviewers' issued reports remain unmodified. This assessment
does not attribute any newly found defect to those reviewers.

## N1: make the emission-reserve boundary explicit

Accepted as a contract clarification. Deterministic specification counterexample:
the after-blueprint check occurs at 13.8 seconds, adapter action/context preparation
continues to 14.2 seconds, and acknowledged delivery finishes at 14.3 seconds.
The r2 prose brackets blueprint work only; its flags can miss the later decision
work even though the brief requires decision completion by 14 seconds. With
candidate=None, the sealed V2 path does not enforce a candidate work cutoff.

Define a ready-to-emit check after all adapter decision work and payload preparation,
then a reserve covering unchanged V2 emission validation/application and mailbox
delivery only. No fresh policy choice occurs in that reserve. Require separate
controls for late decision work, lawful reserve use, and late delivery.

## N2: private-card schema mapping

Accepted as implementation guidance: JSON private_cards maps to the sealed
OneSeatCardState.private_hand. No new runtime attribute is implied.

## N3: run identity validation

Carry as implementation/source-seal guidance. The declared mode-specific namespace,
ASCII identity rules, create-new path handling, and measured size ceilings remain
binding. Run IDs do not replace the source/configuration/semantic bindings.

## N4: Important contract gap in terminal accounting

The suggested raw witness timing after finalization is not an allowed reading of
r2: lines 378-380 require both terminal compute totals to be final public-ledger
totals. A shared clock source alone does not turn caller subtraction into a ledger
output. The sealed action_clock.py start_preparation_work rejects finalized ledgers.

Before any correction, consider a successful terminal action followed by positive
settlement/trace-writing work. If the outer ledger is already finalized, that work
cannot supply the promised ledger totals. If it stays live, r2 never defines the
partition into its two totals or the accounting endpoint. The terminal row also
cannot contain the elapsed duration of its own future serialization and write.

This is a specification counterexample, not executable runtime RED: no v0a runtime
exists or was invoked. A prospective correction must keep the outer ledger live,
define disjoint bookkeeping totals and a pre-publication cut, and retain terminal
publication cost separately in the returned host outcome. Neither a second clock
nor a fabricated zero can close the gap. Full host success must require that final
publication accounting succeeded; trace-only replay cannot assert it.

## Later controller rulings

The controller retired CodeRabbit and authorized resolving the bootstrap cycle by
the coherent source/seal/rehearsal/measured-bounds ordering. These rulings remove
the old approval questions; they do not constitute a specific ceremonial-commit
authorization. The sealed docs/workflow.md and historical receipts remain intact.
The proposed handoff-directory convention has not been adopted or implemented.

Any corrected bytes form r3 with a new immutable ref and manifest; r2 stays retained.
