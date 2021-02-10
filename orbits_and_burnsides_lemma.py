#Orbits and Burnside's Lemma
#Kieran Hobden
#13-Oct-'20

#Given the shape of a wxh grid, determine the maximum number of ways it can be filled with s ints
#Two grids are considered identical if after a number of row or column switches, they are the same
#i.e. consider a 1x2 grid with s=2
#We have 4 possibilities: [0,0], [1,1], [0,1] and [1,0]
#The last two are considered identical hence we would here return 3
#Return the output as a string to allow for large numbers

from math import gcd
from math import factorial

def partition(n):
	"""
	(int) -> set of tuples of ints

	Generate partitions of n through recursion
	If n<1 return {(n,)}
	"""

	partition_set = set()
	partition_set.add((n, ))

	#Consider each integer less than n (and greater than 1) as a base number
	#Add the base + partitions of n-base and repeat for each base
	for base in range(1, n):
		remainder = n-base
		for remainder_partitions in partition(remainder):
			partition_set.add(tuple(sorted((base, ) + remainder_partitions)))
	
	return partition_set

def conjugacy_class_size(partition):
	"""
	(int, tuple of ints) -> int

	We use the conjugacy class size formula for the symmetric group
	Found: https://groupprops.subwiki.org/wiki/Conjugacy_class_size_formula_in_symmetric_group
	"""

	#First compute the denominator by finding unique numbers in our partition
	#Find the how many times each number occurs in the partition and plug into the formula
	denom = 1
	unique_nums = set(num for num in partition)
	for num in unique_nums:
		counts = partition.count(num)
		denom *= (num**counts)*factorial(counts)

	size = factorial(sum(partition))//denom

	return size

def solution(w, h, s):
	"""
	(int, int, int) -> int
	
	From Burnside's lemma we see we can find the number of orbits from the number of fixed points
	Row switching (and column switching) is equivalent to the group action of the symmetric group S_w (S_h)
	Cycle type determines conjugacy class and each cycle type corresponds to an integer partition
	Size of conjugacy class determined by given function
	Greatest common divisor determines the number of orbits within a combination of conjugacy classes
	"""

	#Generate partitions
	w_partitions = partition(w)
	h_partitions = partition(h)

	#Initialise sum
	numerator = 0

	for w_conjugacy in w_partitions:
		for h_conjugacy in h_partitions:
			weight = conjugacy_class_size(w_conjugacy)*conjugacy_class_size(h_conjugacy)
			greatest_common_divisor = 0
			for w_element in w_conjugacy:
				for h_element in h_conjugacy:
					greatest_common_divisor += gcd(w_element, h_element)

			numerator += weight*(s**greatest_common_divisor)

	denom = factorial(w)*factorial(h)

	return str(numerator//denom)



if __name__ == "__main__":
	print(solution(12, 12, 20))