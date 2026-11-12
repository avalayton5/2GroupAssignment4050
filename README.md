# Group Assignment 2
# CMP_SC 4050 — Group Algorithm Engineering Assignment 2

Divide and Conquer (inversion counting) + Dynamic Programming (coin change).

## Environment

* Language: **Python 3.13.18** (CPython). Any Python ≥ 3.9 should work.
* Only the standard library is needed for the algorithms, validation and experiments.

## Layout

```
src/inversions.py          brute-force and sort-and-count inversion counters
src/coinChange.py         greedy, naive recursion, memoized DP, bottom-up DP, 
validator, instrumentation
src/coinChangeExperiments.py
src/coinChangeValidation.py
src/exp1_results.csv
src/exp2_results.csv
experiments/validate_inversions.py   13 hand tests + 500 random cross-checks vs brute force
results/                   machine-readable outputs (CSV / JSON)
```
## Running the Program
python3 experiments/validate_inversions.py
or
python3 coinChange.py
or 
python3 coinChangeExperiments.py
or 
python3 coinChangeValidation.py

## Determinism

All random inputs use `random.Random(4050)` (seed recorded in each script and in
the JSON outputs). Timings will differ between machines; counts, validation results,
counterexamples and DP state counts are fully deterministic.

