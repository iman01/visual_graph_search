import pygame

import colors

class Board:

    def __init__(self, board_width, board_height, rows = 8, cols = 8):

        self.rows = rows
        self.cols = cols

        self.cell_size = int(min(board_width / cols, board_height / rows))
        self.reset()

        # Fonts
        OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
        self.font = pygame.font.Font(OPEN_SANS, int(self.cell_size * 0.7))

    def cost_text_callback(self, cell):
        return None

    def reset(self):
        self.walls = set()
        self.explored = set()
        self.path = []
        self.start = None
        self.goal = None

    def clean(self):
        self.explored = set()
        self.path = []

    def get_neighbors(self, cell):
        if self.cells is None:
            return None

        neighbors = set([
            (cell[0]-1, cell[1]),
            (cell[0]+1, cell[1]),
            (cell[0], cell[1]-1),
            (cell[0], cell[1]+1)
        ])

        for i, j in set(neighbors):

            # Ignore the walls and respect board limits
            if (i, j) in self.walls or \
                    not 0 <= i < self.rows or \
                    not 0 <= j < self.cols:
                neighbors.remove((i, j))

        return neighbors

    def distance(self, first, second):
        return (abs(first[0] - second[0]) + abs(first[1] - second[1]))

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
                        colors.dict['START'] if (i, j) == self.start else \
                        colors.dict['GOAL'] if (i, j) == self.goal else \
                        colors.dict['PATH'] if (i, j) in self.path else \
                        colors.dict['EXPLORED'] if (i, j) in self.explored else \
                        colors.dict['FG']

                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, colors.dict['GRID'], rect, 1)

                text = "A" if (i, j) == self.start else \
                       "B" if (i, j) == self.goal else \
                       self.cost_text_callback((i, j)) if (i, j) in self.path or (i, j) in self.explored else \
                       None

                if text is not None:
                    text = self.font.render(str(text), True, colors.dict['TEXT'])
                    font_rect = text.get_rect()
                    font_rect.center = rect.center
                    screen.blit(text, font_rect)
            
                row.append(rect)
            self.cells.append(row)