

class Solver:

    def __init__(self, board):
        self.board = board

    def shortest_path(self):

        start = Node(state=self.board.start, parent=None, action=None)

        frontier = QueueFrontier()
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


class Node:

    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier:

    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node