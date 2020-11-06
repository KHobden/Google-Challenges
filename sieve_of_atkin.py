#Sieve of Atkin
#Kieran Hobden
#20-Jul-'20

import math
import cProfile

def SieveOfAtkin(limit, sequence = []):
    """
    (int) -> list of int

    We implement the Sieve of Atkin using the modulo 60 rules
    From Wiki:
    All remainders are modulo-sixty remainders (divide the number by 60 and return the remainder).
    All numbers, including x and y, are positive integers.
    Flipping an entry in the sieve list means to change the marking (prime or nonprime) to the opposite marking.
    This results in numbers with an odd number of solutions to the corresponding equation being potentially prime (prime if they are also square free), and numbers with an even number of solutions being composite.
    
    >>> SieveOfAtkin(11)
    [2, 3, 5, 7, 11]
    >>> SieveOfAtkin(19)
    [2, 3, 5, 7, 11, 13, 17, 19]

    """

	#Create a results list containing 2, 3 and 5
    results = [2, 3, 5]

    #Create a sieve list with an entry for each positive integer
    #Extra False element for 0 index to allow easier indexing
    #All entries are False to show they're non prime (composite)
    sieve=[False]*(limit+1)

    #To find solutions to the required equations, iterate through x and y
    #Limit the range of x and y to sqrt(limit) to avoid needless calculations with n>limit
    for x in range(1,math.ceil(math.sqrt(limit))):
        for y in range(1,math.ceil(math.sqrt(limit))):

        	#Case 1:
        	#If n modulo 60 is an element of {1,13,17,29,37,41,49,53} flip the entry for solutions to 4x^2+y^2=n
            n = 4*x**2 + y**2
            if n<=limit and (n%60 in (1,13,17,29,37,41,49,53)):
            	sieve[n] = not sieve[n]
            
            #Case 2:
            #If n modulo 60 is an element of {7,19,31,43} flip the entry for solutions to 3x^2+y^2=n
            n = 3*x**2 + y**2
            if n<= limit and (n%60 in (7,19,31,43)):
            	sieve[n] = not sieve[n]

            #Case 3:
            #If n modulo 60 is an element of {11,23,47,59} flip the entry for solutions to 3x^2-y^2=n
            n = 3*x**2 - y**2
            if x>y and n<=limit and (n%60 in (11,23,47,59)):
            	sieve[n] = not sieve[n]

    #Take the numbers marked prime  and mark the multiples of its square as non prime
    for x in range(6,int(math.sqrt(limit))):
        if sieve[x]:
            for y in range(x**2,limit+1,x**2):
                sieve[y] = False

    #Exract all primes from the sieve list
    for p in range(6,limit+1):
        if sieve[p]:
        	results.append(p)

    return results

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    primes = SieveOfAtkin(1000)
    print("List of primes up to 1000: ", primes)

    # cProfile.run('SieveOfAtkin(10000)')