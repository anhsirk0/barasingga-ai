import pygame
import sys
import time
from barasingga import Barasingga
from ai import BarasinggaAI

BLACK = (39, 39, 39)
GREY = (100, 100, 100)
WHITE = (235, 219, 178)
GREEN = (184, 187, 38)
BLUE = (131, 165, 152)
RED = (251, 73, 52)

blue_dot = pygame.image.load('assets/blue50.png')
red_dot = pygame.image.load('assets/red50.png')

padding = 60
board_size = 600
scale = int(board_size / 4)
line_width = 1

pygame.init()
#create screen
size = (board_size + 2 * padding, board_size + 2 * padding)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Barasingga')

game = Barasingga()
bai = BarasinggaAI(depth=3)
# empty list to store points
points = []

# pygame window
run = True
while run:

    # Check if game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            sys.exit()
        # collect mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            points.append(event.pos)

    screen.fill(BLACK)
    for i in range(5):
        # horizontal lines
        startx = (padding, i * scale + padding)
        endx = (board_size + padding, i * scale + padding)
        # vertical lines
        starty = (i * scale + padding, padding)
        endy = (i * scale + padding, board_size + padding)

        # drawing the diamond
        diamond = [
                    (padding, board_size / 2 + padding),
                    (board_size / 2 + padding, padding),
                    (board_size + padding, board_size / 2 + padding),
                    (board_size / 2 + padding, board_size + padding)
        ]
        pygame.draw.line(screen, (GREEN), startx, endx, line_width)
        pygame.draw.line(screen, (GREEN), starty, endy, line_width)
        pygame.draw.polygon(screen, (GREEN), diamond, line_width)

    if game.player == 2:
        m = bai.best_move(game.board)
        time.sleep(0.1)
        game.move(m)

    if len(points) == 2:
        initial_mouse = points[0]
        final_mouse = points[1]
        initial = None
        final = None
        for i in range(5):
            for j in range(5):
                if pieces[j][i].collidepoint(initial_mouse):
                    initial = (i, j)
                if pieces[j][i].collidepoint(final_mouse):
                    final = (i, j)
        action = (initial, final)
        if action in game.available_actions(game.board, game.player):
            game.move(action)
        points = []

    # drawing the pieces
    pieces = []
    for i in range(5):
        row = []
        for j in range(5):
            center = (padding + i * scale , padding + j * scale)
            rect = pygame.Rect(
                padding + i * scale - 25,
                padding + j * scale - 25,
                50, 50
            )
            row.append(rect)
            if game.board[j][i] == 1:
                screen.blit(blue_dot, rect)
            elif game.board[j][i] == 2:
                screen.blit(red_dot, rect)
        pieces.append(row)

    if game.over:
        print("game over")
    pygame.display.update()

