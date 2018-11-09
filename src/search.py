def search(graph, start, goal, search_strategy):
    """
    Generic graph searching algorithm from the book
    Artificial Inteligence: Foundations of computational agents
    Figure 3.4 p86

    Keyword arguments:
    graph -- A dict that represents the graph
    start -- the start node
    goal -- the end node
    search_strategy -- a function that determines which path to select from the frontier

    returns a path from start to goal

    example usage:
    graph = {"A": [("B", 1), ("C", 1)],
             "B": [("C", 1), ("D", 1)],
             "C": [("D", 1)],
             "D": [("E", 1)],
             "E": [("G", 1)],
             "G": [("F", 1)]}

    start = "A"
    goal = "F"
    depth_first = lambda frontier: frontier.pop()

    search(graph, "A", "F", depth_first)

    """

    class Path():
        def __init__(self, path):
            self.path = path.copy()
            self.cost = 0

        def append(self, element):
            self.path.append(element[0])
            self.cost += element[1]

        def get_last(self):
            return self.path[-1]

        def get_cost(self):
            return self.cost

        def get_path(self):
            return self.path

        def __str__(self):
            return self.path.__str__()

    frontier = []
    frontier.append(Path([start]))

    while len(frontier) != 0:
        #select a path from frontier based on search strategy
        path = search_strategy(frontier)
        if(path.get_last() == goal):
            return path
        else:
            for neighbour in graph[path.get_last()]:
                new_path = Path(path.get_path())
                new_path.append(neighbour)
                frontier.append(new_path)
   
if __name__ == '__main__':
    graph = {"A": [("B", 1), ("C", 1)],
             "B": [("C", 1), ("D", 1)],
             "C": [("D", 1)],
             "D": [("E", 1)],
             "E": [("G", 1)],
             "G": [("F", 1)]}
    
    depth_first = lambda frontier: frontier.pop()
    breadth_first = lambda frontier: frontier.pop(0)
    lowest_cost_first = lambda frontier: frontier.pop(
                                            frontier.index(
                                                min(frontier, key = lambda path: path.get_cost())
                                            ) 
                                        )

    print(search(graph, "A", "F", depth_first))
    print(search(graph, "A", "F", breadth_first))
    print(search(graph, "A", "F", lowest_cost_first))


    