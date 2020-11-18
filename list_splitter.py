#List splitter
#Kieran Hobden
#01-Aug-'20

#Given a list of integers, split the list where any numbers greater than another given int are found
#If the given int is found in the list, we can stop the procedure
#e.g. list = [1,2,4,2,1,3,5,1] and max = 3
#returns [[1,2],[2,1],[3]]

def splitting(l,t):
	#CASE 1:
	#If there exists multiple elements ==t then we need only consider the list up to the first
	#If we truncate, we must add the t value back at the last step
	for idx, val in enumerate(l):
		if val == t:
			count = idx
			truncated = True
			break
		else:
			count = None
			truncated = False
	trunc_list = l[:count]

	#CASE 2:
	#If we find an element >=t, we want to remove it and form 2 sublists, one containing the prior elements and one containing the latter elements
	#Indices of elements of l greater than t
	greater_than_t_idx = [idx for idx, val in enumerate(trunc_list) if val>t]

	#The zip function returns a tuples containing the index+1 and the index of the next element for >=t
	#[0] is needed for the first case and [None] for the last
	#Empty lists occur for consecutive values >t, these are removed
	one_more = [i+1 for i in greater_than_t_idx]
	split_list = [trunc_list[i:j] for i,j in zip([0]+one_more, greater_than_t_idx+[None]) if trunc_list[i:j]]

	#If we truncated the list, we must re-insert the value t at the end of the list
	if truncated:
		split_list.append([t])

	return split_list



#Driver
l = [2,4,63,3,7,9,2,12,1,5,7]
t = 12

print("Input list: ", l)
print("t: ", t)
print(splitting(l,t))