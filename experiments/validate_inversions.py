"""
Part 1B: Validation and Runtime scaling
- Use the brute-force counter as the small-instance 
	oracle for the divide-and-conquer implementation
"""
import json
import os
import random
import sys 

#tells python to also look in src/ for imports
#__file__ = current scripts path
#dirname = this folder
# ".." = means go up one folder from this path
# "src" = the folder to go into once in the shared parent folder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src")) 
from inversions import brute_force_inversions, sort_and_count # noqa: E402

SEED = 4050 #makes arrays consistent so results are reproducable
N_RANDOM = 500 #how many random arrays
OUT = os.path.join(os.path.dirname(__file__), "..", "results", "inversion_validation.json") #establishes folder for saving the results

HAND_TESTS = [
	("empty", [], 0), #(name, array, expected count(calculated by hand))
	("single", [7], 0),
	("two sorted", [1, 2], 0),
	("two reversed", [2, 1], 1),
	("sorted n=6", [1, 2, 3, 4, 5, 6], 0),
	("reverse n=6", [6, 5, 4, 3, 2, 1], 15),
	("nearly sorted: one adjacent swap", [1, 2, 4, 3, 5, 6], 1),
	("nearly sorted: last in front", [6, 1, 2, 3, 4, 5], 5),
	("nearly sorted: first in last", [2, 3, 4, 5, 1], 4),
	("lecture example", [1, 5, 4, 8, 10, 2, 6, 9, 12, 11, 3, 7], 22),
	("random small", [3, 1, 4, 2], 3),
	("interleaved halves", [2, 4, 6, 1, 3, 5], 6),
	("negatives", [0, -1, 5, -3], 4),
]

def check(arr):
	bf = brute_force_inversions(arr) #oracle
	dc, srt = sort_and_count(arr)
	return bf, dc, srt == sorted(arr)

def main():
	rng = random.Random(SEED)
	report = {"seed": SEED, "hand_tests": [], "random_tests": 0, "failures": []}

	for name, arr, expected in HAND_TESTS:
		bf, dc, sorted_ok = check(arr)
		ok = (bf == dc == expected) and sorted_ok
		report["hand_tests"].append(dict(name=name, array=arr, expected=expected, brute_force=bf, divide_conquer=dc, sorted_ok=sorted_ok, pass_=ok))
		
		if not ok: 
			report["failures"].append(name)
	
	for t in range(N_RANDOM):
		n = rng.randint(0, 60)
		arr = rng.sample(range(-1000, 1000), n)
		bf, dc, sorted_ok = check(arr)
		report["random_tests"] += 1
		if bf != dc or not sorted_ok:
			report["failures"].append({"trial": t, "array": arr, "bf": bf, "dc": dc})
	
	report["all_passed"] = not report["failures"]
	with open(OUT, "w") as f:
		json.dump(report, f, indent=2)
	
	print(f"hand tests: {sum(h['pass_'] for h in report ['hand_tests'])}/{len(HAND_TESTS)} passed")
	print(f"random cross-checks: {report ['random_tests']} run, "
			f"{len([x for x in report ['failures'] if isinstance(x, dict)])} disagreements")
	print("ALL PASSED" if report["all_passed"] else "FAILURES: " + str(report["failures"]))
	sys.exit(0 if report["all_passed"] else 1)

if __name__ == "__main__":
	main()