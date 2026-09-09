# FIX coverage: numerical reference acceptance

Planning record created before candidate edits on 2026-09-09; finalized at freeze.
Scope: the Slice A brief/design; no runtime implementation or execution.
Rejected anchor: e39d3b93695bfc601d051e8e71f334eef4d10d19, manifest
4f16c97f50734f06cc6bcd5286a87d355aaf4f8589f8796de1e33a8c5b47c405.
Prior disposition: ../r001/disposition.md. I-01 is a numerical-validation gap;
no legal board/hand false rejection was reproduced. No residual fix yet exists.

## Invariant, discovery and affected paths

Every numerical acceptance must validate both exact production totals against
independent sealed action values before classifying a tie or choosing an action.
Value allowances must not permit wrong non-ties, and the reference's float argmax
must not veto an independently established exact tie merely through rounding.

Discovery follows plan -> reference construction -> fixed policy -> settlement ->
normalization -> value accumulation -> integer validation -> action comparison ->
teacher/export -> preflight result/stop. Searches for best_response, expected_utilities,
tie, reference, disagreement and stop in both candidate documents and their base
dependencies locate all declared consumers. The base dependency inventory remains
34 blobs; this is a direct semantic inventory, not a transitive-closure claim.

| Stage | Governing surface | Required observation / falsifier |
|---|---|---|
| Plan/domain | brief criteria 2-3; design 1,3 | Reject changed denominator or action domain |
| Sealed construction | legal_river_continuation.py; river.py | Exactly 990 distinct unit weights |
| Fixed policy | evaluation.policy_distribution | Missing CALL policy cannot act as passive oracle |
| Settlement | kernel; continuation returns | Integer chips, magnitude <=4; no private payoff rule |
| Accumulation | evaluation.expected_utilities | Both forced actions checked |
| Integer validation | design 3 | Unique reference lattice values equal both production totals |
| Tie/action | design 3 | Wrong exact action fails; bounded reference tie choice can pass |
| Export | brief 4; design 4 | Canonical production CHECK remains CHECK in exported row |
| Result/stop | brief 2,3,8; design 3,6 | Invalid evidence cannot become a passing preflight |
| Worker root | design 6; Session.prepare; execution.begin_run | cwd must match inherited run root |
| Witness coverage | design 4; deal_for_hand | Sizing cannot substitute observed coverage |

## Planned discriminating cases

- Existing all-zero royal-board control: both totals zero, canonical CHECK.
- Nonzero cancellation: positive, negative and zero float residuals with exact
  equal integer totals. The numeric acceptance boundary must accept correct CHECK
  for either legal reference label when both reference values validate the tie.
- Wrong production total, including a false tie, fails independent lattice checks.
- Smallest nonzero integer-total gap and its reverse: wrong production or reference
  action fails. No epsilon broadens the exact tie class.
- NaN, infinity, out-of-domain utility/weight/count, nonunique/no lattice value,
  malformed reference map, or value beyond the bound fails or marks incomplete.
- The two forced-action calls, best_response, and comparison overhead are separately
  attributable in cost observations. Interruption does not pass preflight.
- A legal non-degenerate tie is recorded if found during the declared finite
  production domain census. No witness means a domain-limited absence statement
  only after a complete census; an incomplete search makes no absence claim.
- Worker cwd and witness-bank sufficiency are future integration checks; no test
  receipt is claimed by this specification. Fixed CALL was already correct.

## Current evidence and limits

The r001 arithmetic receipt demonstrates the floating cancellation mechanism only.
Static inspection of the unchanged source supplies the call graph and exact input
constraints. The candidate specifies independent rational interval/lattice checks
with a conservative explicit bound; it does not alter the sealed evaluator.
Author checks at freeze cover candidate identity, cumulative scope, dependency
pins, text hygiene and arithmetic case reasoning. They are not cold verdicts.
checks/author-arithmetic.json records exact integer checks of the bound and
lattice separation, plus both signs of cancellation validating zero and rejecting
the adjacent wrong totals. It does not exercise the future caller implementation.
No Python, poker enumeration, evaluator, host, test suite or measurement ran.
Both supported interpreter executions and the actual legal tie census remain
requirements of the authorized code/measurement stages, not delivered evidence.

I-01 would remain open if a valid exact tie could be rejected only because of
the floating selected label, or if any wrong integer value/action could pass
through the new allowance. A-01 is addressed by explicit worker cwd; A-02 by
declared sizing assumptions and actual coverage; A-03 by this path inventory.
The fix contains no new source surface, changed game or additional budget.
