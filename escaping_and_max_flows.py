#Escaping and Max Flows
#Kieran Hobden
#03-Oct-'20

#You are given a list of lists of ints which describes the layout of a building
#The first sublist contains describes the paths from the first room to each other room
#The numbers in this sublist represent the number of bunnies that can fit through the corridor to the adjacent room
#i.e. a sublist [0,1,3,0] indicates we cannot reach the first of fourth room from our current room
#But we can reach the second and third rooms with capacity 1 and 3
#Given a list of entrances and a list of exits, determine the maximum number of bunnies that can reach the exits

from collections import defaultdict
from queue import Queue
from queue import LifoQueue

def unweighted_graph(path):
    """
    (list of lists of ints) -> dict of sets

    Generate an unweighted graph from the path array
    Useful in computing the level graph
    If path is non-zero add index of end_room as val of dict with idx start_room
    """

    unweighted_graph = defaultdict(set)
    for start_room in range(len(path)):
        for end_room in range(len(path[start_room])):
            capacity = path[start_room][end_room]
            if capacity != 0:
                unweighted_graph[start_room].add(end_room)

    return unweighted_graph
    
def generate_level_graph(entrances, exits, path):
    """
    (list of ints, list of ints, list of lists of ints) -> list of ints

    From the path, generate the levels of each node
    BFS determines the corresponding level
    """

    #Generate an unweighted graph
    unweighted = unweighted_graph(path)

    #Track the nodes already visited with a set and the nodes under consideration with a FIFO queue
    #Initialise the level graph such that unvisited nodes have a value of 0
    visited = set()
    q = Queue()
    level_graph = defaultdict(int)

    #Add the entrance nodes to our queue, set and dict
    #Entrance nodes have level 1
    for entrance in entrances:
        visited.add(entrance)
        q.put(entrance)
        level_graph[entrance] += 1

    #Typical BFS construction
    while not q.empty():
        node = q.get()

        node_level = level_graph[node]

        #Check neighbours of the current node
        #Update the level of the neighbours if 0 or if the level of the previous node is less than the current node - 1
        for neighbour in unweighted[node]:
            if neighbour not in visited:
                visited.add(neighbour)
                q.put(neighbour)
                neighbour_level = level_graph[neighbour]
                if neighbour_level == 0 or node_level <  (neighbour_level - 1):
                    level_graph[neighbour] = node_level + 1

    #If none of the exits are reached then we return 0 otherwise return the level graph
    exit_levels = [level_graph[exit] for exit in exits]
    if any(exit_levels):
        return level_graph
    else:
        return 0

def depth_first_search(entrance, exits, path, level):
    """
    (int, list of ints, list of lists of ints) -> (list of lists of ints, int)

    Using our level graph, we look for the blocking flow
    A typical depth-first search is used
    The flow is augmented after the sink is reached
    Return the augmented path (graph) and the bottleneck value
    """

    #Pre-processing: If level==False then we could not generate a level graph, abort the function
    if not level:
        return False

    #To aide our computation, generate an unweighted graph
    unweighted = unweighted_graph(path)

    #Initialise queue (to track considered nodes) and set (to track visited nodes)
    q = LifoQueue()
    visited = set()

    #Add entrance
    visited.add(entrance)
    q.put(entrance)

    while not q.empty():
        #Obtain current node by taking it from the queue and putting it straight back
        node = q.get()
        q.put(node)

        neighbours = unweighted[node]

        #If we reach a dead-end, remove last node and try again at previous step
        if len(neighbours) == 0:
            q.get()
            continue

        #Select element from neighbours
        neighbour = unweighted[node].pop()

        #Consider only neighbours with a greater level as per Dinic's algorithm
        if level[node] < level[neighbour]:
            if neighbour in exits:
                #If we found the exit, find the edges that form the chain to the exit and determine the bottleneck (maximum total capacity)
                q.put(neighbour)
                chain = [q.get() for x in range(q.qsize())]
                chain_edges = list(zip(chain, chain[1:]))
                chain_capacities = [path[edge[1]][edge[0]] for edge in chain_edges]
                bottleneck = min(chain_capacities)

                #Augment path along the chain
                for edge in chain_edges:
                    path[edge[1]][edge[0]] -= bottleneck
                    path[edge[0]][edge[1]] -= bottleneck

                return (path, bottleneck)

            else:
                #If we haven't found a neighbour, add to the queue and set and try again
                q.put(neighbour)
                visited.add(neighbour)
                continue

    #Exit has not been found
    return False

def solution(entrances, exits, path):
    """
    (list of ints, list of ints, list of list of ints) -> int

    Consider a directed graph with nodes 0->n
    Each node represents a room and each edge represents a corridor between two rooms
    We want to find the max flow rate from the entrance nodes to the exit nodes
    Entrances and exits are disjoint and we assume a path to an exit can always be found
    There are at most 50 rooms and 200,000 bunnies so we use Dinic's algorithm
    A level graph is computed, then use multiple dfs to find the blocking flows, augmenting each path
    Find a new level graph when no more blocking flows can be found
    Return the bottleneck sum once a level graph that reaches an exit can no longer be found
    """

    level = True
    bottleneck_sum = 0

    #Level will become False when we can no longer find a level graph
    while level:
        level = generate_level_graph(entrances, exits, path)
        for entrance in entrances:
            output = True
            #Output will become False when we can no longer find a blocking flow
            while output:
                output = depth_first_search(entrance, exits, path, level)
                if output:
                    (path, bottleneck) = output
                    bottleneck_sum += bottleneck

    return bottleneck_sum



if __name__ == "__main__":
    # entrances = [0]
    # exits = [3]
    # path = [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 0], [9, 0, 0, 0]]

    entrances = [0, 1]
    exits = [4, 5]
    path = [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]

    # entrances = [0]
    # exits = [10]
    # path = [[0,5,10,15,0,0,0,0,0,0,0],[0,0,0,0,10,0,0,0,0,0,0],[0,15,0,0,0,20,0,0,0,0,0],[0,0,0,0,0,0,25,0,0,0,0],[0,0,0,0,0,25,0,10,0,0,0],[0,0,0,5,0,0,0,0,30,0,0],[0,0,0,0,0,0,0,0,20,10,0],[0,0,0,0,0,0,0,0,0,0,5],[0,0,0,0,15,0,0,0,0,15,15],[0,0,0,0,0,0,0,0,0,0,10],[0,0,0,0,0,0,0,0,0,0,0],]

    # entrances = [0]
    # exits = [5]
    # path = [[0,1,1,0,0,0],[0,0,0,1,1,0],[0,0,0,0,0,1],[0,0,0,0,0,0],[0,0,0,0,0,1],[0,0,0,0,0,0]]

    print(solution(entrances, exits, path))