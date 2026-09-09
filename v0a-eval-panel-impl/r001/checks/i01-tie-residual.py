"""Standalone check of I-01: exact production tie vs float best_response reference.

No project imports. Models evaluation.best_response's accumulation:
    action_values[a] = sum(reach * value for state, reach in entry.states)
with reach = 1/990 (normalized float weight) and values ±2/0 (CHECK) or ±4/0 (BET),
over the same state order for both actions.
"""
import random
import sys

N = 990
P = 1.0 / N  # what river._normalized_joint_weights produces: weight / total


def naive_sum(terms):
    total = 0.0
    for t in terms:
        total += t
    return total


def run(seed, w, l):
    t = N - w - l
    values = [2] * w + [-2] * l + [0] * t
    rng = random.Random(seed)
    rng.shuffle(values)
    check_terms = [P * v for v in values]        # reach * returns for CHECK
    bet_terms = [P * (2 * v) for v in values]    # reach * (1.0 * ±4) for BET
    s_check_naive, s_bet_naive = naive_sum(check_terms), naive_sum(bet_terms)
    s_check_builtin, s_bet_builtin = sum(check_terms), sum(bet_terms)
    return (s_check_naive, s_bet_naive, s_check_builtin, s_bet_builtin)


def main():
    print(sys.version.split()[0])
    trials = 2000
    for (w, l) in [(495, 495), (300, 300), (100, 100), (450, 450)]:
        pos = neg = zero = 0          # naive residual sign
        doubled_exact = 0             # S_bet == 2*S_check exactly (naive)
        bpos = bneg = bzero = 0       # builtin sum residual sign
        bdoubled_exact = 0
        for seed in range(trials):
            sc, sb, bc, bb = run(seed, w, l)
            if sc > 0: pos += 1
            elif sc < 0: neg += 1
            else: zero += 1
            doubled_exact += (sb == 2 * sc)
            if bc > 0: bpos += 1
            elif bc < 0: bneg += 1
            else: bzero += 1
            bdoubled_exact += (bb == 2 * bc)
        print(f"w=l={w}, t={N-2*w}, {trials} orderings")
        print(f"  naive loop  : residual >0: {pos:4d}  <0: {neg:4d}  ==0: {zero:4d}   "
              f"S_bet==2*S_check exactly: {doubled_exact}/{trials}")
        print(f"  builtin sum : residual >0: {bpos:4d}  <0: {bneg:4d}  ==0: {bzero:4d}   "
              f"S_bet==2*S_check exactly: {bdoubled_exact}/{trials}")
    # reference picks BET iff S_check > 0 (since S_bet = 2*S_check and max takes first on tie)
    print("reference selects BET on an exact production tie iff residual > 0")


if __name__ == "__main__":
    main()
