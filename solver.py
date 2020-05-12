import abc


class Environment(abc.ABC):

    def reset(self):
        self.source = None
        self.target = None

        self.explored = set()

    def goal_test(self, state):
        return state == self.target

    @abc.abstractmethod
    def get_actions(self, state):
        ...

    @abc.abstractmethod
    def transition_model(self, state, action):
        ...

    def cost_to_target(self, state):
        raise NotImplementedError


class Solver:
    DFS, BFS, GREEDY_BFS, A_STAR = range(4)

    def __init__(self, environment):
        self.environment = environment

    def search_path(self, algorithm = A_STAR):

        start = Node(state=self.environment.source, parent=None, action=None)

        frontier = QueueFrontier() if algorithm == self.DFS else \
                   StackFrontier() if algorithm == self.BFS else \
                   GreedyFrontier(lambda node: self.environment.cost_to_target(node.state)) if algorithm == self.GREEDY_BFS else \
                   GreedyFrontier(lambda node: self.environment.cost_to_target(node.state) + node.cost_to_reach)

        frontier.add(start)

        self.environment.explored = set()

        while True:

            if frontier.empty():
                return None

            node = frontier.remove()

            for action in self.environment.get_actions(node.state):
                state = self.environment.transition_model(node.state, action)

                if not frontier.contains_state(state) and state not in self.environment.explored:
                    child = Node(state=state, parent=node, action=action)

                    if self.environment.goal_test(child.state):
                        path = []

                        while child.parent is not None:
                            path.append((child.state, child.action))
                            child = child.parent

                        path.reverse()
                        return path
                    else:
                        frontier.add(child)

            self.environment.explored.add(node.state)


class Node:

    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost_to_reach = 0

        node = self
        while node.parent is not None:
            node = node.parent
            self.cost_to_reach += 1

    def __str__(self):
        return f"state: {self.state}, action: {self.action}, cost: {self.cost_to_reach}"

    def __repr__(self):
        return self.__str__()


class StackFrontier:

    def __init__(self):
        self.list = []

    def __str__(self):
        return str(self.list)

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
        super().__init__()
        self.cost_function = cost_function

    def add(self, new):
        position = 0

        for node in self.list:
            if self.cost_function(new) <= self.cost_function(node):
                position += 1
                continue
            else:
                break

        self.list.insert(position, new)
