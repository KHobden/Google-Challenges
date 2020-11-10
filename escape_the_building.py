#Escape the Building
#Kieran Hobden
#08-Oct-'20

#You are given a list of lists of ints describing the paths between rooms in which prisoners are held
#The first sublist hence contains ints describing the time it will take to reach the other rooms
#Starting at the first room and ending at the last, you must visit as many other rooms as possible within a given time limit
#Negative times are possible as passing through certain corridors increases your time limit
#Return a list containing the most amount of rooms that can be visited

from itertools import permutations as perm

def floyd_warshall(times):
    """
    (list of lists of ints) -> list of lists of ints

    Floyd-Warshall algorithm
    Look for a shorter path to connect two nodes e.g.
    1->2 may be replaced with 1->3->2 if the weight of the new path is lower
    Updating the weights allows us to move to the next node via the most efficient path
    This algorithm also finds any negative cycles whereby we could gain infite time and rescue all the bunnies
    """

    #For each edge, loop through all possible new edges and update the weights
    num_nodes = len(times)
    for start_node in range(num_nodes):
        for middle_node in range(num_nodes):
            for end_node in range(num_nodes):
                if times[start_node][end_node] > times[start_node][middle_node] + times[middle_node][end_node]:
                    times[start_node][end_node] = times[start_node][middle_node] + times[middle_node][end_node]

    #If a negative cycle is found, we can return to the same point in negative time
    #We show a negative cycle has been found by returning False
    for node in range(num_nodes):
        if times[node][node] < 0:
            return False

    return times

def solution(times, time_limit):
    """
    (list of lists of ints, int) -> list of ints

    Find the number of bunnies that can be saved
    Run the Floyd-Warshall algorithm
    If a negative cycle is found, all bunnies can be saved
    Permute through the bunny cells to find possible paths through the prison
    Compute the weight of each path
    If the total time taken to rescue the bunnies is less than the allowed time, return the list of bunnies
    """

    #Run Floyd-Warshall to search for a negative cycle. If found, all bunnies can escape
    num_buns = len(times) - 2
    times = floyd_warshall(times)
    if not times:
        return [bun for bun in range(num_buns)]

    #Consider all possible orders that we can collect the bunnies
    for path_length in reversed(range(1, num_buns+1)):
        for collection_order in perm(range(1, num_buns+1), path_length):

            #Generate a list of the edges that will need to be taken to attain the bunnies
            path = [bun for bun in collection_order]
            path.insert(0, 0)
            path.append(num_buns+1)
            edges = list(zip(path, path[1:]))

            #Sum the weights of these edges
            total_time = 0
            for start, end in edges:
                total_time += times[start][end]

            #If we can complete our rescue in the time limit, return the sorted numbers of the saved bunnies
            if total_time <= time_limit:
                return sorted([bun_room-1 for bun_room in collection_order])

    #If no bunnies could be saved, return an empty list
    return []


if __name__ == "__main__":
    times = [[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]]
    time_limit = 1
    # times = [[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]]
    # time_limit = 3


    print(solution(times, time_limit))