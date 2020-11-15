#Finding Triples
#Kieran Hobden
#29-Aug-'20

#Given a list of integers, find the number of triples found in that list
#A triple is defined as an integer that has a divisor to it's left in the list where the divisor has a divisor of its own to its left
#e.g. [2,4,8]
#8 is divisible by 4 and 4 is divisible by 2 hence we have 1 triple

def divisors(l):
	"""
	(list) -> dict

	O(n^2)
	Find divisors in elements with lower index and attach to dictionary
	Dictionary keys = index of elements in l
	Dictionary vals = index of divisors of element l[key]
	"""

	#Use indices in the keys and values to allow for duplicate values
	divisor_dict = {}
	for i in reversed(range(len(l))):
		current_divisors = []
		for j in reversed(range(i)):
			if l[i]%l[j]==0:
				current_divisors.append(j)
			divisor_dict[i] = current_divisors

	#First term has no prior elements so attach an empty list for the element
	divisor_dict[0] = []

	return divisor_dict

def solution(l):
	"""
	(list) -> int

	O(n^2)
	Creates a dictionary (using divisors(l)) indicating the divisors of each element
	Look for "triples" in dictionary i.e. an element has a divisor and that divisor has another divisor
	Return the number of triples found
	"""

	#Ignore any list with less than 3 elements
	if len(l)<3:
		return 0

	#Generate dictionary of divisors
	div_dict = divisors(l)

	#Select element in list, find it's divisors, count the number of divisors of these divisors
	num_triples = 0
	for i in reversed(range(len(l))):
		for j in div_dict[i]:
			num_triples += len(div_dict[j])

	return num_triples



if __name__ == "__main__":
	# l = [1,3,2,4,6,8,9]
	# l = [i+1 for i in range(100)]
	# l = [1,2,3,4,5,6,7,8,9,8,7,6,5,4,3,2,1]
	l = [1,2,4,8]

	print(solution(l))