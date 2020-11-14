#Find Sum
#Kieran Hobden
#31-Jul-'20

#Given a list of ints find two integers that sum to some given total
#Return the positions of the two integers that constitute this sum
#If this can be achieved in multiple ways, return the two with the lowest values (i.e. leftmost integers)

def solution(l,t):
    #Function sums each element in the list with all previous elements
    #Then repeats starting at the next index e.g. [1,2,3,4]: [1,3,6,10]-->[2,5,9]-->[3,7]-->[4]
    for i in range(len(l)):
        for j in range(i,len(l)):
            consec_sum = sum(l[i:j+1])
            #If our sum ==t, the solution is found
            if consec_sum==t:
       	        return [i,j]
            #If our sum >t, adding more won't help so move start again at the next element in l
            elif consec_sum>t:
                break
    #If the return was never triggered then no solution has been found so return [-1,-1]
    return [-1,-1]




#Driver
l = [2,4,63,3,7,9,2,1,5,7]
t = 13

print("Input list: ", l)
print("t: ", t)
print(solution(l,t))