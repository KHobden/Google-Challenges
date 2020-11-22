#XOR Queue
#Kieran Hobden
#14-Aug-'20

#Consider a grid of size lxl containing integers starting at some int s
#The grid is filled from left to right, top to bottom
#Find the value when the upper left triangle (including the diagonal) is continuously XOR'd
#e.g. s=0, l=3
# 0 1 2 /
# 3 4 / 5
# 6 / 7 8
# returns 0^1^2^3^4^6 == 2

def XOR(n):
    """
    (int) -> int

    Function performs a cumulative XOR from 0 to n
    Patterns in mod 4 increase computational efficiency
    """

    mod_4 = n%4
    if mod_4 == 0:
        return n
    elif mod_4 == 1:
        return 1
    elif mod_4 == 2:
        return n+1
    elif mod_4 == 3:
        return 0


def solution(s,l):
    """
    (int, int) -> int
    
    Function takes two ints as inputs: s and l
    s is the start number for the top left of the grid
    l is the length of the square grid

    >>> solution(0,3)
    2
    >>> solution(17,4)
    14
    >>> solution(20,1)
    20
    """

    #XOR is self-inverse, associative and commutative (with identity 0) so checksum includes multiple XORs up to specific values
    #Include the sums to the last worker counted i.e last one before the breaks
    checksum = 0
    for i in range(1,l+1):
        last_counted = s+i*(l-1)
        checksum ^= XOR(last_counted)

    #Include the sums to the number of the last worker of each queue to eliminate values after breaks
    for i in range(1,l):
        last_in_line = s+i*l-1
        checksum ^= XOR(last_in_line)

    #Eliminate numbers below s by including the sum to s-1
    checksum ^= XOR(s-1)

    return checksum



#Driver
if __name__ == "__main__":
    import doctest
    doctest.testmod()

    # import cProfile
    # cProfile.run('solution(1000,10000)')

    print(solution(5,2))