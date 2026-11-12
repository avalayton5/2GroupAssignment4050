#------------------------
#2B: Exact solver validations + counterexamples
#------------------------

import random
from itertools import combinations

from coinChange import(
    IMPOSSIBLE,
    greedy,
    naiveRecursion,
    topDown,
    bottomUp,
)

NAIVE_MAX_AMOUNT = 18

#------------------------
#Independent verification helpers
#------------------------
def verifyResult(denoms, amount, result, solverName = ""):
    if result == IMPOSSIBLE:
        return
    count, coins = result
    assert sum(coins) == amount, f"{solverName}: {coins} does not sum to {amount}"
    assert len(coins) == count, f"{solverName}: reported count {count} but returned {len(coins)} coins"

def countOf(result):
    if result == IMPOSSIBLE:
        return None
    else:
        return result[0]

#------------------------
#Hand check test cases (description, denoms, amount, expectedOptimalCount)
#------------------------
HAND_TESTS = [
    ("target zero", [1, 5, 10, 25], 0, 0),
    ("single coin 1", [1], 7, 7),
    ("exact single coin", [5, 10], 5, 1),
    ("US coins, 25+5", [1, 5, 10, 25], 30, 2),
    ("5+5+1", [1, 2, 5], 11, 3),
    ("impossible: all even, odd target", [2, 4], 7, None),
    ("impossible: target < min coin", [7], 3, None),
    ("impossible: no combo", [2, 5], 3, None),
    ("greedy trap: 3+3", [1, 3, 4], 6, 2),
    ("multiple optimals: 2+4 or 3+3", [1, 2, 3, 4], 6, 2),
]

def runHandTests():
    exactSolvers = [
        ("naive", naiveRecursion),
        ("top down", topDown),
        ("bottom up", bottomUp)
    ]
    for desc, denoms, amount, expected in HAND_TESTS:
        for name, function in exactSolvers:
            result = function(denoms, amount)
            verifyResult(denoms, amount, result, name)
            got = countOf(result)
            assert got == expected, (                
                f"[{desc}] {name}: D={denoms}, A={amount}: "
                f"expected {expected}, got {got}"
            )

        #greedy is allowed to be suboptimal
        verifyResult(denoms, amount, greedy(denoms, amount), "greedy")
    print(f"[PASS] {len(HAND_TESTS)} hand-checkable tests "
        f"(naive, topDown, bottomUp all match expected counts)")

#------------------------
#Random small instances, solvers must agree on optimal count
#------------------------
def runRandomTests(numTrials = 300, seed = 4050):
    rng = random.Random(seed)
    naiveUsed = 0
    impossibleSeen = 0
    for _ in range(numTrials):
        k = rng.randint(1, 5)
        denoms = rng.sample(range(1, 13), k)
        if rng.random() < 0.7 and 1 not in denoms:
            denoms[0] = 1
        amount = rng.randint(0, 30)

        td = topDown(denoms, amount)
        bu = bottomUp(denoms, amount)
        verifyResult(denoms, amount, td, "top down")
        verifyResult(denoms, amount, bu, "bottom up")
        assert countOf(td) == countOf(bu), (
            f"topDown/bottomUp disagree: D={denoms}, A={amount}: {td} vs {bu}"
        )

        if amount <= NAIVE_MAX_AMOUNT:
            nv = naiveRecursion(denoms, amount)
            verifyResult(denoms, amount, nv, "naive")
            assert countOf(nv) == countOf(bu), (
                f"naive disagrees: D={denoms}, A={amount}: {nv} vs {bu}"
            )
            naiveUsed += 1

        gr = greedy(denoms, amount)
        verifyResult(denoms, amount, gr, "greedy")
        if gr != IMPOSSIBLE and bu != IMPOSSIBLE:
            assert gr[0] >= bu[0], "greedy beat exact optimum (impossible)"
        if bu == IMPOSSIBLE:
            impossibleSeen += 1

    print(f"[PASS] {numTrials} randomized instances: topDown == bottomUp on all; "
          f"naive also agreed on {naiveUsed} (A <= {NAIVE_MAX_AMOUNT}); "
          f"{impossibleSeen} impossible instances; every coin list sums to A")

#------------------------
#Search for greedy counterexamples
#------------------------
def greedyCounterexamples(maxDenom = 12, maxSize = 4, maxAmount = 40):
    #find smallest amount where greedy is feasible but suboptimal
    found = []
    for size in range(2, maxSize + 1):
        for denoms in combinations(range(1, maxDenom + 1), size):
            denoms = list(denoms)
            for amount in range(1, maxAmount + 1):
                gr = greedy(denoms, amount)
                if gr == IMPOSSIBLE:
                    continue
                optimal = bottomUp(denoms, amount)
                verifyResult(denoms, amount, gr, "greedy")
                verifyResult(denoms, amount, optimal, "bottom up")
                if optimal != IMPOSSIBLE and gr[0] > optimal[0]:
                    found.append({"denoms": denoms, "amount": amount, "greedy": gr, "optimal": optimal,})
                    break
    found.sort(key=lambda c: (c["amount"], len(c["denoms"]), c["denoms"]))
    return found

def runCounterexample():
    cex = greedyCounterexamples()
    assert len(cex) >= 3, "need at least three distinct counterexamples"
 
    # Required sanity check: the search must detect D={1,3,4}, A=6
    target = [c for c in cex if c["denoms"] == [1, 3, 4] and c["amount"] == 6]
    assert target, "search failed to detect D={1,3,4}, A=6"
    t = target[0]
    assert t["greedy"][0] == 3 and t["optimal"][0] == 2
    print(f"[PASS] counterexample search found {len(cex)} distinct denomination "
          f"systems where greedy is feasible but suboptimal")
    print("[PASS] sanity check: detected D={1,3,4}, A=6 -> "
          f"greedy {t['greedy']} vs optimal {t['optimal']}")
 
    print("\nFirst 8 counterexamples (smallest failing amount per system):")
    for c in cex[:8]:
        gCount, gCoins = c["greedy"]
        oCount, oCoins = c["optimal"]
        print(f"  D={c['denoms']!s:<14} A={c['amount']:<3} "
              f"greedy={gCount} coins {sorted(gCoins, reverse=True)}  "
              f"optimal={oCount} coins {sorted(oCoins, reverse=True)}")
    print("\nCounterexamples used in the report:")
    for c in cex:
        if c["denoms"] in ([1, 3, 4], [1, 5, 6, 9], [1, 5, 10, 12]):
            print(f"  D={c['denoms']}, A={c['amount']}: greedy {c['greedy']} vs optimal {c['optimal']}")
    return cex

if __name__ == "__main__":
    runHandTests()
    runRandomTests()
    runCounterexample()
    print("All Part 2B checks passed.")