import pygame
import sys
import time

import colors
from solver import Solver
from board import Board


def main():
    width = 800
    height = 600
    
    padding = 20

    pygame.init()
    screen = pygame.display.set_mode((width, height))

    colors.init()

    # Fonts
    OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
    smallFont = pygame.font.Font(OPEN_SANS, 20)
    mediumFont = pygame.font.Font(OPEN_SANS, 28)
    largeFont = pygame.font.Font(OPEN_SANS, 40)

    # Compute board size 
    board_width = ((2 / 3) * width) - (padding * 2)
    board_height = height - (padding * 2)

    board = Board(board_width, board_height, 16, 16)

    while True:
        # Check if game quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(colors.dict['BG'])
        board.draw(screen, (padding, padding))

        # Start button
        startButton = pygame.Rect(
            (2 / 3) * width + padding, (1 / 3) * height - 50,
            (width / 3) - padding * 2, 50
        )
        buttonText = mediumFont.render("Start", True, colors.dict['TEXT'])
        buttonRect = buttonText.get_rect()
        buttonRect.center = startButton.center
        pygame.draw.rect(screen, colors.dict['GRID'], startButton)
        screen.blit(buttonText, buttonRect)

        # Clean button
        cleanButton = pygame.Rect(
            (2 / 3) * width + padding, (1 / 3) * height + 20,
            (width / 3) - padding * 2, 50
        )
        buttonText = mediumFont.render("Clean", True, colors.dict['TEXT'])
        buttonRect = buttonText.get_rect()
        buttonRect.center = cleanButton.center
        pygame.draw.rect(screen, colors.dict['GRID'], cleanButton)
        screen.blit(buttonText, buttonRect)

        # Reset button
        resetButton = pygame.Rect(
            (2 / 3) * width + padding, (1 / 3) * height + 90,
            (width / 3) - padding * 2, 50
        )
        buttonText = mediumFont.render("Reset", True, colors.dict['TEXT'])
        buttonRect = buttonText.get_rect()
        buttonRect.center = resetButton.center
        pygame.draw.rect(screen, colors.dict['GRID'], resetButton)
        screen.blit(buttonText, buttonRect)

        # Mouse action
        left, _, right = pygame.mouse.get_pressed()

        if left == 1:
            mouse = pygame.mouse.get_pos()

            # Start button clicked
            if startButton.collidepoint(mouse):

                if board.start is not None and board.goal is not None:
                    solver = Solver(board)
                    solver.shortest_path(solver.A_STAR)

                time.sleep(0.2)

            # Clean button clicked
            elif cleanButton.collidepoint(mouse):
                board.clean()
                continue

            # Reset button clicked
            elif resetButton.collidepoint(mouse):
                board.reset()
                continue

            # Cell left-clicked
            else:
                for i in range(board.rows):
                    for j in range(board.cols):
                        if (board.cells[i][j].collidepoint(mouse)):
                            board.walls.add((i, j))
        elif right == 1:
            mouse = pygame.mouse.get_pos()

            # Cell right-clicked
            for i in range(board.rows):
                for j in range(board.cols):
                    if (board.cells[i][j].collidepoint(mouse)):
                        if board.start is None:
                            board.start = (i, j)
                        elif board.goal is None and board.start != (i, j):
                            board.goal = (i, j)

        pygame.display.flip()


if __name__ == '__main__':
    main()