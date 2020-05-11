

class Solver:
    DFS, BFS, GREEDY_BFS, A_STAR = range(4)

    def __init__(self, board):
        self.board = board

    def shortest_path(self, algorithm = DFS):

        start = Node(state=self.board.start, parent=None, action=None)

        frontier = QueueFrontier() if algorithm == self.DFS else \
                   StackFrontier() if algorithm == self.BFS else \
                   GreedyFrontier(self.cost_GREEDY_DFS) if algorithm == self.GREEDY_BFS else \
                   GreedyFrontier(self.cost_A_STAR)

        frontier.add(start)

        self.board.explored = set()

        while True:

            if frontier.empty():
                print('No solution')
                return None

            node = frontier.remove()

            for neighbor in self.board.get_neighbors(node.state):
                if not frontier.contains_state(neighbor) and neighbor not in self.board.explored:
                    child = Node(state=neighbor, parent=node, action=None)

                    if child.state == self.board.goal:
                        path = []

                        while child.parent is not None:
                            path.append(child.state)
                            child = child.parent

                        path.reverse()
                        self.board.path = path
                        return
                    else:
                        frontier.add(child)

            self.board.explored.add(node.state)

    def cost_GREEDY_DFS(self, cell):
        return self.board.distance(cell, self.board.goal)

    def cost_A_STAR(self, cell):
        return self.board.distance(cell, self.board.goal) + self.board.distance(cell, self.board.start)


class Node:

    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier:

    def __init__(self):
        self.list = []

    def add(self, node):
        self.list.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.list)

    def empty(self):
        return len(self.list) == 0

    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            node = self.list[-1]
            self.list = self.list[:-1]
            return node      


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            node = self.list[0]
            self.list = self.list[1:]
            return node


class GreedyFrontier(StackFrontier):

    def __init__(self, cost_function):
        self.list = []
        self.cost_function = cost_function

    def add(self, new):
        i = 0

        for i, node in enumerate(self.list):
            if self.cost_function(new.state) > self.cost_function(node.state):            
                break

        self.list.insert(i, new)
