#Changing Mazes
#Kieran Hobden
#15-Aug-'20

#Consider a maze described as a list of zeros and ones
#A zero represents a corridor and a one represents a barrier
#The top left and bottom right of the map are the entrance and exits respectively and are hence both zeros
#Find the shortest path through the maze where any one barrier can be changed to a corridor

from queue import PriorityQueue

class graph:
    def __init__(self, maze_list):
        """
        (graph, list of lists) -> NoneType
        """

        self.maze_list = maze_list
        self.width = len(maze_list[0])
        self.height = len(maze_list)
        self.start = (0,0)
        self.end = (self.width-1, self.height-1)
        self.nodes = set()
        self.barriers = set()
        self.graph_dict = {}

    def __str__(self):
        """
        (graph) -> str

        Print basic information: graph dimensions and node positions
        """

        return "Dimensions: " + str(self.width) + "x" + str(self.height) + "\nNodes: " + str(self.nodes)

    def generate_nodes(self):
        """
        (graph) -> NoneType

        Run a first pass, collect the positions of the nodes and store them in self.nodes
        """

        self.nodes = set()
        for x in range(self.width):
            for y in range(self.height):
                if self.maze_list[y][x] == 0:
                    self.nodes.add((x, y))

    def add_node(self, pos):
        """
        (graph, tuple) -> NoneType

        Add a node by it's (x,y) position
        """

        self.nodes.add(pos)

    def generate_barriers(self):
        """
        (graph) -> NoneType

        Run a first pass, collect the positions of the barriers and store them in self.barriers
        """

        self.barriers = set()
        for x in range(self.width):
            for y in range(self.height):
                if self.maze_list[y][x] == 1:
                    self.barriers.add((x, y))

    def remove_irrelevant_barriers(self):
        """
        (graph) -> NoneType

        A barrier with no nodes as neighbours will not affect the graph when removed
        Similarly with only one node as a neighbour, the simplify() function will render the removal irrelevant
        Keep only barriers with 2 or more nodes as neighbours
        """
        original_barriers = self.barriers.copy()
        for barrier in original_barriers:
            x, y = barrier
            num_neighbours = 0
            if x+1 in range(self.width) and y in range(self.height) and self.maze_list[y][x+1] == 0:
                num_neighbours += 1
            if x-1 in range(self.width) and y in range(self.height) and self.maze_list[y][x-1] == 0:
                num_neighbours += 1
            if x in range(self.width) and y+1 in range(self.height) and self.maze_list[y+1][x] == 0:
                num_neighbours += 1
            if x in range(self.width) and y-1 in range(self.height) and self.maze_list[y-1][x] == 0:
                num_neighbours += 1

            if num_neighbours < 2:
                self.barriers.remove(barrier)

    def generate_graph_dict(self):
        """
        (graph) -> NoneType

        From the positions of the nodes, create a graph represented as a dict of dicts
        The parent key represents the position of the node in consideration
        The associated dictionary has keys corresponding to the positions of the successors and values corresponding to the respective weights
        For now, all weights are 1 as we can only move to adjacent grid squares

        We must generate_nodes before calling generate_graph_dict
        """

        for node in self.nodes:
            x, y = node
            neighbours = {}
            if (x+1,y) in self.nodes:
                neighbours[(x+1,y)] = 1
            if (x-1,y) in self.nodes:
                neighbours[(x-1,y)] = 1
            if (x,y+1) in self.nodes:
                neighbours[(x,y+1)] = 1
            if (x,y-1) in self.nodes:
                neighbours[(x,y-1)] = 1

            self.graph_dict[(x,y)] = neighbours

    def simplify(self):
        """
        (graph) -> bool

        Simplify the graph structure to reduce the spatial complexity when later finding the shortest path, through three steps:
        Step 1: Remove any unconnected nodes. They will not feature in any path
        Step 2: Remove any nodes with only one edge. They are dead ends and will not feature in any path
        Step 3: For any node with two edges: remove the node and connect its two successors with a large edge

        Cycles:
        Small cycles are removed by this function. Note: not all cycles can be removed!
        Repeated application of the function may be required e.g. one node may go from having 3 -> 2 edges, another application may then remove this node altogether

        Isolated subgraphs:
        Any acyclic isolated subgraph will be removed.
        Most small, cyclic, isolated subgraphs are removed with repeated iterations

        Must generate graph dictionary and nodes before running simplify
        """

        #Keep a copy of the original nodes to see if the algorithm simplified the graph
        nodes_before_simplify = self.nodes.copy()

        #To avoid the start or end being removed, they are not considered here
        node_list = [node for node in self.graph_dict if node != self.start and node != self.end]

        for current_node in node_list:
            successors = [succ for succ in self.graph_dict[current_node]]

            if len(successors) == 0:
                #Ignore nodes with no connections. They won't contribute to the solution
                self.graph_dict.pop(current_node)
                self.nodes.remove(current_node)

            elif len(successors) == 1:
                #Having only one edge means the node would be a dead end so we can remove it
                self.graph_dict[successors[0]].pop(current_node)
                self.graph_dict.pop(current_node)
                self.nodes.remove(current_node)

            elif len(successors) == 2:
                #If we have two successors we can replace two edges with just one for computational efficiency
                succ1 = successors[0]
                succ2 = successors[1]

                #The new edge weight will be the sum of the previous two edge weights
                new_weight = sum(self.graph_dict[current_node].values())

                #Check to see if there already exists an edge between the two successors
                is_edge = succ2 in {key for key in self.graph_dict[succ1].keys()}

                #If the edge exists and has a lower weight, we can ignore the new path
                if is_edge and self.graph_dict[succ1][succ2] < new_weight:

                    #New connection would have a larger weight so it can be ignored
                    self.graph_dict[succ1].pop(current_node)
                    self.graph_dict[succ2].pop(current_node)
                    self.graph_dict.pop(current_node)
                    self.nodes.remove(current_node)

                else:
                    #Consider the first successor's successors, remove the current node and replace it with the other successor of the current node and an increased weight
                    self.graph_dict[succ1].pop(current_node)
                    self.graph_dict[succ1][succ2] = new_weight

                    #Repeat for the second successor of the current node
                    self.graph_dict[succ2].pop(current_node)
                    self.graph_dict[succ2][succ1] = new_weight

                    #Remove the current node as it now has no edges
                    self.graph_dict.pop(current_node)
                    self.nodes.remove(current_node)

        #Return False only if the nodes haven't changed, indicating there's no need for re-running simplify()
        return self.nodes != nodes_before_simplify

    def find_shortest_path(self):
        """
        (graph) -> int

        A* algorithm is used with 1D distance as the heuristic to solve the graph
        Algorithm implemented as standard but with no track kept of the predecessor nodes
        Return the number of steps from the start to end +1

        Must have generated nodes and graph dictionary to solve
        """

        #The open set tracks the nodes with non-inf g_scores that have not yet been considered
        open_queue = PriorityQueue()

        #To later update values, we also need a set to track the non-inf, unconsidered nodes
        open_set = {self.start}

        #Initialise scores
        #G represents the cost of the path to the start node
        g_score = {node: float("inf") for node in self.nodes}
        g_score[self.start] = 0

        #F represents the heuristic function (1D distance) from the node to the end + g
        #This will act as our priority number
        f_score = {node: float("inf") for node in self.nodes}
        f_score[self.start] = distance(self.start, self.end)

        #Include the start in the queue
        open_queue.put((f_score[self.start], self.start))

        current_node = self.start
        while current_node != self.end:
            #If no more nodes can be considered and we have not reached the endpoint, the graph is impossible to solve
            if len(open_set) == 0:
                return float("inf")

            #Consider the node with lowest f_score
            current_node = open_queue.get()[1]
            open_set.remove(current_node)

            #For each of its neighbours, check if a new shorter path can be found
            neighbours = [key for key in self.graph_dict[current_node]]

            for neighbour in neighbours:
                new_g_score = g_score[current_node] + self.graph_dict[current_node][neighbour]

                #If a new shortest path has been found, update g, f and our queue
                if new_g_score < g_score[neighbour]:
                    g_score[neighbour] = new_g_score
                    f_score[neighbour] = new_g_score + distance(neighbour, self.end)

                    #We can't remove the old value from the queue so we just re-add it with a new f_score
                    if neighbour not in open_set:
                        open_queue.put((f_score[neighbour], neighbour))
                        open_set.add(neighbour)

        return g_score[self.end] + 1

def distance(pos1, pos2):
    """
    (tuple of ints, tuple of ints) -> int

    Returns the 1D distance between two points
    """

    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1-x2)+abs(y1-y2)

def solution(maze):
    """
    (list of lists) -> int

    Produce the shortest path length from the top left to the bottom right where at most one barrier can be removed
    """

    #Instantiate the class and produce of list of barriers that we will remove one at a time
    path = graph(maze)
    path.generate_barriers()
    path.remove_irrelevant_barriers()

    solutions = []

    #If there is a barrier, add one barrier at a time as a node and solve for the shortest path
    if path.barriers:
        for barrier in path.barriers:
            path.generate_nodes()
            path.add_node(barrier)
            path.generate_graph_dict()

            #Run the simplify() algorithm as many times as necessary such that the graph stops changing
            repeat = True
            while repeat:
                repeat = path.simplify()

            #Find the shortest path. If path is the minimum  possible, return it
            solution = path.find_shortest_path()
            if solution == path.height + path.width - 1:
                return solution
            solutions.append(solution)

    #If there are no barriers, make no substitutions and find the shortest path as before
    else:
        path.generate_nodes()
        path.generate_graph_dict()

        repeat = True
        while repeat:
            repeat = path.simplify()
        solutions.append(path.find_shortest_path())

    #Loop through the possible shortest paths for different barriers missing to find the shortest overall path
    minimum = float("inf")
    for x in solutions:
        if x < minimum:
            minimum = x
    return minimum



maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
              [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
              [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]]
# maze = [[0, 0, 1, 1, 1], [1, 1, 1, 1, 1], [1, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
# maze = [[0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0]]
# maze = [[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [1, 1, 1, 0]]
# maze = [[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]]

print(solution(maze))