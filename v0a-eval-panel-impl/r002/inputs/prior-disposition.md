# Finalizer disposition: v0a-eval-panel-impl/r001

Issued: 2026-09-09. Finalizer: Codex, the candidate's drafter.
Authority: the controller explicitly asked the finalizer to decide and publish.

**Final defect verdict: NOT CLEAN (UNCLEAN). Design verdict: SOUND.**
One Important numerical-reference specification gap remains. This is the
finalizer's adjudication, not a third cold review and not a majority vote.

Candidate: e39d3b93695bfc601d051e8e71f334eef4d10d19.
Manifest SHA-256:
4f16c97f50734f06cc6bcd5286a87d355aaf4f8589f8796de1e33a8c5b47c405
Base: 46f45298a405b967976413a4b8e45e7837602316.
The frozen candidate, ref and both issued reviews remain unchanged.

## Review disposition

- Claude 01: NOT CLEAN / SOUND; I-01 accepted with the evidence qualification
  below. The report remains attributed exactly as issued.
- Codex 02: CLEAN / SOUND; retained without amendment. Its discussion accepts
  integer production totals plus a reference value allowance, but does not
  resolve the non-degenerate exact-tie scenario identified by Claude.

I do not adopt the second review's clean conclusion for the round. A permitted
value error and exact action-label equality are different predicates. Allowing
the first does not make the second a valid oracle at an exact tie.

## I-01: accepted as an Important numerical-reference gap

Candidate design.md section 3 specifies integer production totals with CHECK
on exact equality, then exact equality with the action selected by
evaluation.best_response. Only reference values receive an accumulation allowance.
Brief criteria 2-3 treat reference disagreement as a phase-stopping failure.

Frozen source establishes the relevant distinction:

- BASE src/pontius/river.py:203-229 normalizes equal deal weights to floating
  1/990 and returns sorted deals.
- BASE src/pontius/evaluation.py:257-273 sums weighted continuation values
  and applies max to the computed action values. First-action tie-breaking
  applies only when those computed values compare equal.
- BASE src/pontius/legal_river_continuation.py:288-307 obtains kernel net
  returns and converts them to float. At this root, CHECK returns are -2/0/+2
  and bet/CALL returns are -4/0/+4 under the specified opponent.

For an exact non-degenerate tie, wins equal losses with some nonzero terms.
Production totals are equal and select CHECK. With sequential binary64
accumulation, a residual e in the CHECK sum yields 2e in the BET sum under
power-of-two scaling. If e is positive, the reference argmax selects BET.
These residuals are coupled, not independent errors. The all-zero royal-board
fixture does not exercise cancellation because every summand is zero.

The finalizer independently checked this arithmetic with 990 ordered terms:
495 negative then 495 positive terms of magnitude 2/990 yielded
3.122502256758253E-17; the corresponding 4/990 sum yielded
6.245004513516506E-17. Exact totals are zero, but float argmax selects BET.
Reversing the groups reverses the residual sign and selects CHECK.
The retained arithmetic illustration states its limits explicitly.

**Evidence qualification:** neither cold review nor this adjudication identifies
a concrete legal board/hero hand whose actual 990 sorted villain outcomes
realize the failing order. No game enumeration, Python evaluator or host was
executed. The arithmetic illustration is not such a witness, does not establish
frequency, and is not a test of either supported Python interpreter's sum.
The review's categorical wording that the comparison cannot survive an exact
tie is too broad: the royal-board tie and some cancellation orders do survive.
The program-ledger addendum about interpreter-specific summation is not needed
for this verdict and has not been independently executed here.

I accept the finding as an unclosed numerical-validation contract, not a claim
of an observed production failure. The material unverified case is a nonzero
win/loss cancellation tie whose reference chooses BET while production correctly
chooses CHECK. The candidate neither establishes that this case is unreachable
in its reference domain nor defines how to distinguish it from a wrong action.
Its sole declared tie control cannot falsify this mechanism. For this Tier C
oracle, that gap blocks adoption; it is not closed by a second general clean pass.

## Smallest correction and closure evidence

Keep production's exact integer comparison and canonical CHECK tie-break.
Keep the sealed game, settlement, evaluator and fixed-CALL villain unchanged.
The correction belongs to the caller's reference acceptance rule:

1. Obtain both fixed-action reference values independently, for example through
   expected_utilities on the same sealed singleton game with forced CHECK and
   forced bet/CALL policies. best_response returns an optimum and selected map;
   it does not expose a per-action value table, so do not invent that API.
2. Derive and state an allowance covering the actual normalization, products and
   accumulation. Verify both production action values against those references.
   Do not let a production claim of equality certify itself.
3. At an independently validated exact production tie, require canonical CHECK
   from production/export and allow a reference selected-action difference only
   when the reference action values are indistinguishable within that bound.
   Otherwise retain exact action agreement and value checks. Never use epsilon
   to convert a materially unequal production decision into a tie.
4. Retain the all-zero control and add a discriminating cancellation control.
   Identify a legal non-degenerate tie witness in the declared reference domain
   when one exists; if none exists, establish and record that domain limitation.
   Label an arithmetic-only fixture as such. Show that a wrong non-tie action
   still fails, and that a correct tie is not rejected because of float argmax.

These are requirements for a bounded fix candidate, not implemented corrections
or new execution authority. New bytes require a new round and manifest. If
further evidence instead proves the alleged case unreachable and the predicate
stable over the required domain, retain that evidence as an explicit closure
record rather than silently rewriting either review.

## Advisory disposition

- Worker cwd: carry forward explicitly. Session.prepare uses Path.cwd(); the
  worker must enter the inherited run root before normal session preparation.
- Witness-bank sizing: carry forward a declared sizing/confidence calculation
  plus actual coverage verification. Coupon-collector expectations are not a
  guaranteed cover, and a smaller bank is not automatically incomplete. No
  performance or success guarantee is inferred from the review's rough estimate.
- Coverage: state the plan-to-retained-result category and discovery method
  explicitly in the fix/code coverage record, including numerical acceptance.
- Fixed-CALL villain: confirmed existing requirement, not a further correction.
- Combined line and round budgets: preserve the accepted whole-slice limits.
  Checkpoints do not reset them; further authority is requested before exceeding
  the remaining allowance, not inferred from this disposition.

## Publication and limits

The phase structure remains SOUND: capacity, per-hand preflight, measured
decision, then bridge completion. No redesign or wider interface is warranted.
I do not authorize adoption of r001 while this Important gap remains open.

This disposition and its ledger entries publish the finalizer's decision only.
No source, candidate, issued review, historical result or run journal was edited.
No runtime, solver, host, test suite or experiment was invoked. Verification was
frozen-source inspection and a separately labeled native arithmetic illustration.
