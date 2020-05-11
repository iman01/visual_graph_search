import pygame
import sys
import time

# Colors
COLOR_BG = (0, 0, 0)
COLOR_FG = (128, 128, 128)
COLOR_GRID = (255, 255, 255)
COLOR_WALL = (255, 64, 64)
COLOR_TEXT = (0, 0, 0)


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
                
                color = COLOR_WALL if (i, j) in self.walls else \
                        COLOR_GRID if (i, j) in [self.start, self.goal] else \
                        COLOR_FG

                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, COLOR_GRID, rect, 3)
                
                if self.start == (i, j):
                    screen.blit(self.start_icon, rect)
                elif self.goal == (i, j):
                    screen.blit(self.goal_icon, rect)
            
                row.append(rect)
            self.cells.append(row)

        
class GameUI:

    width = 800
    height = 600
    padding = 20

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Fonts
        OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
        self.smallFont = pygame.font.Font(OPEN_SANS, 20)
        self.mediumFont = pygame.font.Font(OPEN_SANS, 28)
        self.largeFont = pygame.font.Font(OPEN_SANS, 40)

        # Compute board size 
        board_width = ((2 / 3) * self.width) - (self.padding * 2)
        board_height = self.height - (self.padding * 2)

        self.board = Board(board_width, board_height)

    def draw(self):
        self.screen.fill(COLOR_BG)
        self.board.draw(self.screen, (self.padding, self.padding))

        # Start button
        self.startButton = pygame.Rect(
            (2 / 3) * self.width + self.padding, (1 / 3) * self.height - 50,
            (self.width / 3) - self.padding * 2, 50
        )
        buttonText = self.mediumFont.render("Start", True, COLOR_TEXT)
        buttonRect = buttonText.get_rect()
        buttonRect.center = self.startButton.center
        pygame.draw.rect(self.screen, COLOR_GRID, self.startButton)
        self.screen.blit(buttonText, buttonRect)

        # Reset button
        self.resetButton = pygame.Rect(
            (2 / 3) * self.width + self.padding, (1 / 3) * self.height + 20,
            (self.width / 3) - self.padding * 2, 50
        )
        buttonText = self.mediumFont.render("Reset", True, COLOR_TEXT)
        buttonRect = buttonText.get_rect()
        buttonRect.center = self.resetButton.center
        pygame.draw.rect(self.screen, COLOR_GRID, self.resetButton)
        self.screen.blit(buttonText, buttonRect)

    def run(self):
        while True:
            # Check if game quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.draw()

            # Mouse action
            left, _, right = pygame.mouse.get_pressed()

            if left == 1:
                mouse = pygame.mouse.get_pos()

                # Start button clicked
                if self.startButton.collidepoint(mouse):
                    time.sleep(0.2)

                # Reset button clicked
                elif self.resetButton.collidepoint(mouse):
                    self.board.reset()
                    continue

                # Cell left-clicked
                else:
                    for i in range(self.board.rows):
                        for j in range(self.board.cols):
                            if (self.board.cells[i][j].collidepoint(mouse)):
                                self.board.walls.add((i, j))
            elif right == 1:
                mouse = pygame.mouse.get_pos()

                # Cell right-clicked
                for i in range(self.board.rows):
                    for j in range(self.board.cols):
                        if (self.board.cells[i][j].collidepoint(mouse)):
                            if self.board.start is None:
                                self.board.start = (i, j)
                            elif self.board.goal is None and self.board.start != (i, j):
                                self.board.goal = (i, j)

            pygame.display.flip()


if __name__ == '__main__':
    game = GameUI()
    game.run()