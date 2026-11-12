import sys

IMPOSSIBLE = "IMPOSSIBLE"

sys.setrecursionlimit(max(sys.getrecursionlimit(), 20000))

def validate(denoms, amount):
    if amount < 0:
        raise ValueError("Amount must be 0 or greater.")
    ds = sorted(set(denoms))
    if any(d <= 0 for d in ds):
        raise ValueError("Denominations must be positive integers")
    return ds

#--------------------------------
# 2A, A. Greedy largest denomination first, not always optimal
#--------------------------------
def greedy(denoms, amount):
    ds = validate(denoms, amount)
    desc = sorted(ds, reverse = True)
    remaining = amount
    coins = []
    for d in desc:
        while d <= remaining:
            coins.append(d)
            remaining -= d
    if remaining != 0:
        return IMPOSSIBLE
    return len(coins), coins

#--------------------------------
# 2A, B. Naive exact recursion, no memoization
#--------------------------------
def naiveRecursion(denoms, amount):
    ds = validate(denoms, amount)

    def solve(a):
        if a == 0:
            return 0, []
        best = None
        for d in ds:
            if d > a:
                break
            sub = solve(a - d)
            if sub == IMPOSSIBLE:
                continue
            count = sub[0] + 1
            if best is None or count < best[0]:
                best = (count, sub[1] + [d])
        if best is None:
            return IMPOSSIBLE
        else:
            return best

    return solve(amount)

#--------------------------------
# 2A, C. Top down with memoization
#--------------------------------
def topDown(denoms, amount):
    ds = validate(denoms, amount)
    INF = float("inf")
    memo = {0: 0}
    choice = {}

    def solve(a):
        if a in memo:
            return memo[a]
        best = INF
        bestCoin = None
        for d in ds:
            if d > a:
                break
            sub = solve(a - d)
            if sub + 1 < best:
                best = sub + 1
                bestCoin = d
        memo[a] = best
        if bestCoin is not None:
            choice[a] = bestCoin
        return best

    result = solve(amount)
    if result == INF:
        return IMPOSSIBLE

    coins = []
    a = amount
    while a > 0:
        coins.append(choice[a])
        a -= choice[a]
    return result, coins

#--------------------------------
# 2A, D. Bottom up
#--------------------------------
def bottomUp(denoms, amount):
    ds = validate(denoms, amount)
    INF = float("inf")
    dp = [INF] * (amount + 1)
    last = [None] * (amount + 1)
    dp[0] = 0

    for a in range(1, amount + 1):
        for d in ds:
            if d > a:
                break
            if dp[a - d] + 1 < dp[a]:
                dp[a] = dp[a - d] + 1
                last[a] = d

    if dp[amount] == INF:
        return IMPOSSIBLE

    coins = []
    a = amount
    while a > 0:
        coins.append(last[a])
        a -= last[a]
    return dp[amount], coins

SOLVERS = {
    "greedy": greedy,
    "naive": naiveRecursion,
    "top down": topDown,
    "bottom up": bottomUp,
}

if __name__ == "__main__":
    tests = [
        ([1, 5, 10, 25], 63),   # greedy is optimal
        ([1, 3, 4], 6),         # greedy gives 4+1+1 (3 coins), optimal is 3+3 (2)
        ([2, 5], 3),            # impossible
        ([1, 2, 5], 0),         # zero amount
    ]
    for denoms, amount in tests:
        print(f"D={denoms}, A={amount}")
        for name, fn in SOLVERS.items():
            print(f"  {name:10s} -> {fn(denoms, amount)}")