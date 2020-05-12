import pygame

import colors
from solver import Environment

class Board(Environment):

    def __init__(self, board_width, board_height, rows = 8, cols = 8):

        self.rows = rows
        self.cols = cols

        self.cell_size = int(min(board_width / cols, board_height / rows))
        self.reset()

        OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
        self.font = pygame.font.Font(OPEN_SANS, int(self.cell_size * 0.7))

    def reset(self):
        self.walls = set()
        self.explored = set()
        self.path = []
        self.source = None
        self.target = None

    def clean(self):
        self.explored = set()
        self.path = []

    def get_actions(self, cell):
        actions = set()

        if cell[0] > 0:
            actions.add('up')
        if cell[0] < self.rows - 1:
            actions.add('down')
        if cell[1] > 0:
            actions.add('left')
        if cell[1] < self.cols - 1:
            actions.add('right')

        return actions

    def transition_model(self, cell, action):

        if action == 'up':
            i, j = cell[0]-1, cell[1]
        if action == 'down':
            i, j = cell[0]+1, cell[1]
        if action == 'left':
            i, j = cell[0], cell[1]-1
        if action == 'right':
            i, j = cell[0], cell[1]+1

        if (i, j) not in self.walls:
            return i, j
        else:
            return cell

    def cost_to_target(self, cell):
        return (abs(cell[0] - self.target[0]) + abs(cell[1] - self.target[1]))

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

                path = [item[0] for item in self.path] if self.path is not None else []

                color = colors.dict['WALL'] if (i, j) in self.walls else \
                        colors.dict['START'] if (i, j) == self.source else \
                        colors.dict['GOAL'] if (i, j) == self.target else \
                        colors.dict['PATH'] if (i, j) in path else \
                        colors.dict['EXPLORED'] if (i, j) in self.explored else \
                        colors.dict['FG']

                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, colors.dict['GRID'], rect, 1)

                text = "A" if (i, j) == self.source else \
                       "B" if (i, j) == self.target else \
                       None

                if text is not None:
                    text = self.font.render(str(text), True, colors.dict['TEXT'])
                    font_rect = text.get_rect()
                    font_rect.center = rect.center
                    screen.blit(text, font_rect)
            
                row.append(rect)
            self.cells.append(row)