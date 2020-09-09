# PySnake - Python Game for fun and machine learning purposes for later
# Copyright (C) 2020  Gabor Tanacs
#
# The first version of a Snake game to try out pygame
# The upcoming versions will upgrade this to be able to run with a neural network.
#
# Gabor Tanacs
# gabor.tanacs@yahoo.com
"""
Main file that contains the work-flow and game logic
"""
import pygame

from config import Colors, Config
from view import renderer as gfx
from model.Game import Game
from model.Direction import Direction
from model.Player import Player


def init():
    pygame.init()
    screen = pygame.display.set_mode(Config.screen_size)
    icon = pygame.image.load('./images/logo.jpg')
    pygame.display.set_caption("PySnake")
    pygame.display.set_icon(icon)

    game = Game(Player('User'), Config.table_size)
    return screen, game


def re_render(screen, game, time):
    """Refresh/update the screen of the game"""
    screen.fill(Colors.black)
    gfx.render_sidebar(screen, time, game)
    gfx.render_board(screen, game)
    pygame.display.update()


def start(screen, game):
    """Main flow of one iteration of the game (until GameOver)"""
    running = True
    time = -1
    # iteration to control the screen-update and elapsed-time with quick keypress processing
    i = -1

    board, player = game.board, game.player
    new_direction = Direction.UP
    while running is not False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return False
        if player.direction.is_not_opposite(keys):
            if keys[pygame.K_UP]:
                new_direction = Direction.UP
            elif keys[pygame.K_DOWN]:
                new_direction = Direction.DOWN
            elif keys[pygame.K_LEFT]:
                new_direction = Direction.LEFT
            elif keys[pygame.K_RIGHT]:
                new_direction = Direction.RIGHT

        i += 1
        pygame.time.delay(10)

        # Refresh the screen with new score and time in every second
        if i % 100 == 0:
            time += 1
            game.score_inc(game.speed)
            re_render(screen, game, time)

        # Refresh the screen with new position depends on the speed
        if i % (1000 // (game.speed * 3)) == 0:
            player.direction = new_direction
            running = player.move(game)
            re_render(screen, game, time)
    return True


def main():
    """Main loop for re/starting the game automatically"""
    in_game = True
    window, game = init()
    game.init_game(Config.table_size)
    while True:
        # Start a new Game
        in_game = start(window, game)

        # Exit if press ESC
        if not in_game:
            full_screen_print(window, "I hope you enjoyed the Game.", 1500, (100, 300))
            full_screen_print(window, "Good bye!", 1500)
            return

        # Display "Game Over" before restart the game automatically
        pygame.time.delay(1000)
        full_screen_print(window, "GAME OVER", 2000)
        game.restart(game.score, Config.table_size)


def full_screen_print(window, title, time, position=(300, 300)):
    finish_font = pygame.font.SysFont('cooperblack', 42)
    pygame.draw.rect(window, Colors.dark_grey, (0, 0, 800, 650))
    window.blit(finish_font.render(title, False, Colors.red), position)
    pygame.display.update()
    pygame.time.delay(time)


if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()
