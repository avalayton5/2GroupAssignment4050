"""
an inversion in A[0...n-1] is a pair of indices i<j with A[i]>A[j]
Inversion count measures how far the array is from sorted order

Part IA: Implement two inversion counters
1. Brute-Force pair counting
2. Divide-and-Conquer Sort-and-Count 
"""

def brute_force_inversions(a):
#check every pair (i,j) with i<j 

	n = len(a)
	count = 0
	for i in range(n-1):
		A_i = a[i]
		for j in range(i + 1, n):
#increment count when A[i]>A[j]
			if A_i > a[j]:
				count +=1
	return count
#!!!!!!!!!!!!!!!!analyze the actual runtime of your implementation!!!!!!!!!!!!!


#Modify mergesort so that each recursive call returns a sorted subarray together with its inversion count. 
# During the merge, count cross inversions in O(n) time.
def merge_and_count(left, right):
	sorted_sub = []
	i = j = 0
	cross = 0
	nL, nR = len(left), len(right)
	while i < nL and j < nR:
		if left[i] <= right[j]: #2<=1
			sorted_sub.append(left[i])
			i += 1
		else:
			sorted_sub.append(right[j])
			j += 1
			cross += nL - i
	sorted_sub.extend(left[i:])
	sorted_sub.extend(right[j:])
	return sorted_sub, cross


def sort_and_count(a):

	n = len(a)
	if n <= 1:
	#return (inversion_count, sorted_list)
		return 0, list(a)
	mid = n // 2
	print(f"mid: {mid} for {list(a)}")
	#recursively divide the array
	left_count, left_sorted = sort_and_count(a[:mid])
	right_count, right_sorted = sort_and_count(a[mid:])
	merged, cross_count = merge_and_count(left_sorted, right_sorted)
	return left_count + right_count + cross_count, merged

#tool to return just the count of inversions
def simply_inversions(a):
	return sort_and_count(a)[0]

