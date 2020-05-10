import pygame
import sys
import time

# Colors
COLOR_BG = (0, 0, 0)
COLOR_FG = (128, 128, 128)
COLOR_GRID = (255, 255, 255)
COLOR_WALL = (64, 128, 128)

COLOR_TEXT = (0, 0, 0)

pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)

# Fonts
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
smallFont = pygame.font.Font(OPEN_SANS, 20)
mediumFont = pygame.font.Font(OPEN_SANS, 28)
largeFont = pygame.font.Font(OPEN_SANS, 40)

# Compute board size
HEIGHT = 8
WIDTH = 8
BOARD_PADDING = 20
board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

# Add images
start_icon = pygame.image.load("assets/images/start.png")
start_icon = pygame.transform.scale(start_icon, (cell_size, cell_size))
goal_icon = pygame.image.load("assets/images/goal.png")
goal_icon = pygame.transform.scale(goal_icon, (cell_size, cell_size))

walls = set()
start = None
goal = None

while True:

    # Check if game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(COLOR_BG)

    # Draw board
    cells = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):

            # Draw rectangle for cell
            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size, cell_size
            )

            pygame.draw.rect(screen, COLOR_WALL if (i, j) in walls else COLOR_FG, rect)
            pygame.draw.rect(screen, COLOR_GRID, rect, 3)

            if start == (i, j):
                screen.blit(start_icon, rect)
            elif goal == (i, j):
                screen.blit(goal_icon, rect)
        
            row.append(rect)
        cells.append(row)

    # Start button
    startButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height - 50,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = mediumFont.render("Start", True, COLOR_TEXT)
    buttonRect = buttonText.get_rect()
    buttonRect.center = startButton.center
    pygame.draw.rect(screen, COLOR_GRID, startButton)
    screen.blit(buttonText, buttonRect)

    # Reset button
    resetButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height + 20,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = mediumFont.render("Reset", True, COLOR_TEXT)
    buttonRect = buttonText.get_rect()
    buttonRect.center = resetButton.center
    pygame.draw.rect(screen, COLOR_GRID, resetButton)
    screen.blit(buttonText, buttonRect)

    # Mouse action
    left, _, right = pygame.mouse.get_pressed()

    if left == 1:
        mouse = pygame.mouse.get_pos()

        # Start button clicked
        if startButton.collidepoint(mouse):
            time.sleep(0.2)

        # Reset button clicked
        elif resetButton.collidepoint(mouse):
            walls = set()
            start = None
            goal = None
            continue

        # Cell clicked
        else:
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if (cells[i][j].collidepoint(mouse)):
                        walls.add((i, j))
    elif right == 1:
        mouse = pygame.mouse.get_pos()

        # Cell right-clicked
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if (cells[i][j].collidepoint(mouse)):
                    if start is None:
                        start = (i, j)
                    elif goal is None and start != (i, j):
                        goal = (i, j)

    pygame.display.flip()
