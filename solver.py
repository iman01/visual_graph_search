

class Solver:
    DFS, BFS, GREEDY_BFS, A_STAR = range(4)

    def __init__(self, board):
        self.board = board

    def shortest_path(self, algorithm = DFS):

        start = Node(state=self.board.start, parent=None, action=None)

        frontier = QueueFrontier() if algorithm == self.DFS else StackFrontier()
        frontier.add(start)

        self.board.explored = set()

        while True:

            if frontier.empty():
                print('No solution')
                return None

            if algorithm == self.DFS or algorithm == self.BFS:
                node = frontier.remove()
            elif algorithm == self.GREEDY_BFS:
                node = frontier.remove_best(self.cost_to_goal)

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

    def cost_to_goal(self, cell):
        return (abs(cell[0] - self.board.goal[0]) + abs(cell[1] - self.board.goal[1]))


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

    def remove_best(self, cost_function):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            best_node = None
            min_cost = float("inf")
            for node in self.list:
                if cost_function(node.state) < min_cost:
                    best_node = node
                    min_cost = cost_function(node.state)

            self.list.remove(best_node)
            return best_node           


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            node = self.list[0]
            self.list = self.list[1:]
            return node