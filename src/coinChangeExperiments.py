#-------------------------
#2C: Memoization and pseudo-polynomial behavior
#-------------------------

import sys
import time
import csv
import os

from coinChange import bottomUp

sys.setrecursionlimit(20000)

DENOMS = [1, 5, 10, 25]
CUTOFF = 5_000_000

class Cutoff(Exception):
    pass

def saveCSV(filename, header, rows):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(path, "w", newline = "") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(rows)
    print(f"Saved {path}")

def naiveCounts(amount):
    #Naive recursion, returns (calls, distinct states), cache hits are 0
    calls = 0
    seen = set()

    def solve(a):
        nonlocal calls
        calls += 1
        if calls > CUTOFF:
            raise Cutoff
        seen.add(a)
        if a == 0:
            return 0
        return 1 + min(solve(a - d) for d in DENOMS if d <= a)

    solve(amount)
    return calls, len(seen)

def memoCounts(amount):
    #Memoization recursion, returns (calls, distinct states, cache hits)
    memo = {}
    calls = 0
    hits = 0

    def solve(a):
        nonlocal calls, hits
        calls += 1
        if a in memo:
            hits += 1
            return memo[a]
        memo[a] = 0 if a == 0 else 1 + min(solve(a - d) for d in DENOMS if d <= a)
        return memo[a]

    solve(amount)
    return calls, len(memo), hits

def experiment1():
    rows = []
    print(f"EXPERIMENT 1: D = {DENOMS}, naive cutoff = {CUTOFF:,} calls")
    print(f"{'A':>4} | {'naive calls':>12} {'naive states':>13} | "
          f"{'memo calls':>11} {'memo states':>12} {'memo hits':>10}")
    for amount in range(5, 500, 5):
        m_calls, m_states, m_hits = memoCounts(amount)
        try:
            n_calls, n_states = naiveCounts(amount)
        except Cutoff:
            print(f"{amount:>4} | {'> cutoff':>12} {'-':>13} | "
                  f"{m_calls:>11,} {m_states:>12,} {m_hits:>10,}")
            print(f"Naive recursion became impractical at A = {amount}.")
            rows.append([amount, "cutoff", "", m_calls, m_states, m_hits])
            break
        print(f"{amount:>4} | {n_calls:>12,} {n_states:>13,} | "
              f"{m_calls:>11,} {m_states:>12,} {m_hits:>10,}")
        rows.append([amount, n_calls, n_states, m_calls, m_states, m_hits])
    saveCSV("exp1_results.csv",
             ["A", "naive_calls", "naive_states", "memo_calls", "memo_states", "memo_hits"],
             rows)
 
 
def experiment2():
    rows = []
    print(f"\nEXPERIMENT 2: bottom-up DP, D = {DENOMS} (k = {len(DENOMS)})")
    print(f"{'A':>10} {'bits':>5} {'DP states':>11} {'runtime (s)':>12}")
    for exp in range(8, 21):
        amount = 2 ** exp
        start = time.perf_counter()
        bottomUp(DENOMS, amount)
        seconds = time.perf_counter() - start
        print(f"{amount:>10,} {amount.bit_length():>5} {amount + 1:>11,} {seconds:>12.4f}")
        rows.append([amount, amount.bit_length(), amount + 1, seconds])
    saveCSV("exp2_results.csv",
             ["A", "bits", "dp_states", "runtime_seconds"],
             rows)
 
 
if __name__ == "__main__":
    experiment1()
    experiment2()