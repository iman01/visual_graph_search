import pygame

import colors

class Board:

    def __init__(self, board_width, board_height, rows = 8, cols = 8):

        self.rows = rows
        self.cols = cols

        self.cell_size = int(min(board_width / cols, board_height / rows))

        # Add images
        self.start_icon = pygame.image.load("assets/images/start.png")
        self.start_icon = pygame.transform.scale(self.start_icon, (self.cell_size, self.cell_size))
        self.goal_icon = pygame.image.load("assets/images/goal.png")
        self.goal_icon = pygame.transform.scale(self.goal_icon, (self.cell_size, self.cell_size))

        self.reset()

    def reset(self):
        self.walls = set()
        self.explored = set()
        self.path = set()
        self.start = None
        self.goal = None

    def get_neighbors(self, cell):
        if self.cells is None:
            return None

        neighbors = set()

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself and walls
                if (i, j) == cell or (i, j) in self.walls:
                    continue

                if 0 <= i < self.rows and 0 <= j < self.cols:
                    neighbors.add((i, j))

        return neighbors

    def draw(self, screen, origin):
        self.board_origin = origin

        self.cells = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):

                # Draw rectangle for cell
                rect = pygame.Rect(
                    origin[0] + j * self.cell_size,
                    origin[1] + i * self.cell_size,
                    self.cell_size, self.cell_size
                )
                
                color = colors.dict['WALL'] if (i, j) in self.walls else \
                        colors.dict['GRID'] if (i, j) in [self.start, self.goal] else \
                        colors.dict['FG']

                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, colors.dict['GRID'], rect, 3)

                if (i, j) in self.path:
                    pygame.draw.circle(screen, colors.dict['PATH'], rect.center, self.cell_size // 5)
                elif (i, j) in self.explored:
                    pygame.draw.circle(screen, colors.dict['EXPLORED'], rect.center, self.cell_size // 5) 
                
                if self.start == (i, j):
                    screen.blit(self.start_icon, rect)
                elif self.goal == (i, j):
                    screen.blit(self.goal_icon, rect)
            
                row.append(rect)
            self.cells.append(row)