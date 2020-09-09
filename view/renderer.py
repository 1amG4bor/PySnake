"""
Control the rendering process/logic to the screen
"""
from typing import List

import pygame
import pygame.gfxdraw as draw

from config import Colors, Config
from model.Direction import Direction
from model.Player import Body
from view import gfx

pygame.init()
pygame.font.init()
title_font = pygame.font.Font('./font/SquadaOne-Regular.ttf', 52)
mainFont = pygame.font.SysFont('comic', 42)
paragraphFont = pygame.font.Font('./font/BreeSerif-Regular.ttf', 24)

size = Config.cell_size
apple = pygame.transform.scale(pygame.image.load('./images/apple.png'), (size - 2, size - 2))
logo = pygame.transform.scale(pygame.image.load('./images/logo.jpg'), (36, 36))


def render_sidebar(screen, time, game):
    """Render the UI elements to the screen"""
    gfx.set_screen(screen)
    grid = Config.grid
    # Game Logo & Title
    # Logo
    position = (grid['col'][0], grid['row'][0]+10)
    gfx.draw_panel(position, (40, 40), Colors.red, Colors.white)
    screen.blit(logo, (shifted_position(position, 2)))

    left = grid['col'][2]
    position = (left+2, grid['row'][0])
    # Title
    gfx.draw_text('PySnake', position, Colors.red, 52, 'SquadaOne-Regular.ttf')
    gfx.draw_line((left, grid['row'][1]), 165)

    left = grid['col'][1]
    padding = 10
    # Username
    position = (left, grid['row'][2])
    gfx.draw_panel(position, (180, 50), Colors.neon_green, Colors.green2)
    gfx.draw_text("Dummy the Player", shifted_position(position, padding))

    padding = 6
    # Elapsed time
    position = (left, grid['row'][3])
    gfx.draw_panel(position, (180, 40), Colors.dark_grey, Colors.grey)
    gfx.draw_text(_format_time(time), shifted_position(position, 12, padding))

    # Actual score
    position = (left, grid['row'][4])
    gfx.draw_panel(position, (180, 40), Colors.dark_grey, Colors.grey)
    gfx.draw_text(f'Score: {game.score:,}', shifted_position(position, 12, padding))

    # Progress-bar (Level)
    position = (left, grid['row'][5])
    values = game.score - game.prev_limit, game.level_limit - game.prev_limit
    width = grid['col'][3] - grid['col'][1]
    gfx.draw_progress_bar(position, (width, 50), game.level, values)

    # Highest score
    position = (left, grid['row'][6])
    gfx.draw_line((position[0], position[1]-20), 180, Colors.white, 1)
    gfx.draw_panel(position, (180, 40), Colors.dark_grey, Colors.orange)
    gfx.draw_text(f'Top score: {game.top_score:,}', shifted_position(position, 8, padding), Colors.black)


def render_board(screen, game):
    dim = Config.board_position + Config.board_size
    pygame.draw.rect(screen, Colors.dark_grey, dim)
    pygame.draw.rect(screen, Colors.grey, dim, 3)  # Border
    _draw_grid(screen, game)


def _draw_grid(screen, game):
    start_off = [i + 2 for i in Config.board_position]
    rect = Config.cell_size

    food_location = (game.board.get_food_location())
    for y in range(Config.table_size):
        dy = start_off[1] + y * rect
        for x in range(Config.table_size):
            dx = start_off[0] + x * rect

            if food_location == (x, y):
                screen.blit(apple, (dx + 1, dy + 1))
            else:
                pygame.draw.rect(screen, Colors.deep_grey, (dx, dy, rect - 1, rect - 1))
            # draw snake
            head = game.player.head
            body: List[Body] = game.player.body
            if x == head.x and y == head.y:
                pygame.draw.rect(screen, Colors.green, (dx + 1, dy + 1, rect - 2, rect - 2))
                # Half and quarter size (1/4) of the cell
                half, q1 = Config.cell_size // 2, Config.cell_size // 4

                if game.player.direction == Direction.UP or game.player.direction == Direction.DOWN:
                    draw.filled_circle(screen, dx + q1, dy + half, 1, Colors.red)
                    draw.filled_circle(screen, dx + half + q1, dy + half, 1, Colors.red)
                else:
                    draw.filled_circle(screen, dx + half, dy + q1, 1, Colors.red)
                    draw.filled_circle(screen, dx + half, dy + half + q1, 1, Colors.red)

            for i, part in enumerate(body):
                if x == part.location.x and y == part.location.y:
                    # Striped color pattern for the snake
                    color = Colors.deep_dark_green if (i % 4 == 0 and i != 0) else Colors.dark_green
                    draw.box(screen, (dx + 1, dy + 1, rect - 2, rect - 2), color)


# Private functions
def _format_time(time):
    minutes = time // 60
    seconds = time % 60
    return f"Time: {minutes:>02}:{seconds:>02}"


def shifted_position(position, x_padding, y_padding=None):
    if not y_padding:
        y_padding = x_padding
    return position[0] + x_padding, position[1] + y_padding
