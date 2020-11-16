#Largest Multiple of Three
#Kieran Hobden
#31-Jul-'20

#From a list of ints, find the largest multiple of three that can be made

#From prior calculations, at most only two digits will need to be removed from the list
#The output will then consist of the list in descending order

def solution(l):

    #Find occurrences of [2,5,8] (one less than multiples of 3) and [1,4,7] (one more than multiples of 3)
    one_less = [x for x in l if x in [2,5,8]]
    one_more = [x for x in l if x in [1,4,7]]

    #The difference (mod 3) in the number of occurences of [2,5,8] and [1,4,7] will help us determine which number to drop, if any
    diff = (len(one_less)-len(one_more))%3

    #If there exists as many occurrences of [2,5,8] as [1,4,7] (i.e. diff==0) our number is already divisible by 3

    #If the difference is 1, we must drop a number from the one_less list
    #To obtain the largest final number, drop the smallest digit
    #If one_less is empty, we must drop 2 numbers from one_more
    #If one_more doesn't contain 2 numbers, we return 0 as no multiple of 3 can be found
    if diff==1:
        if one_less:
            l.remove(min(one_less))
        elif len(one_more)>1:
            l.remove(min(one_more))
            one_more.remove(min(one_more))
            l.remove(min(one_more))
        else:
            return 0


    #If the difference is 2, we must drop a number from the one_more list
    #Again, drop only the smallest digit
    if diff==2:
        if one_more:
            l.remove(min(one_more))
        elif len(one_less)>1:
            l.remove(min(one_less))
            one_less.remove(min(one_less))
            l.remove(min(one_less))
        else:
            return 0


    #Sort the list in descending order and use it to form an integer
    l.sort(reverse=True)
    x = sum([d * 10**i for i, d in enumerate(l[::-1])])

    return x


#Driver
l = [3,1,4,1,5,9,2,6,5,3,5,9]

print(solution(l))