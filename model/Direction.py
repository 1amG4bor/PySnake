from enum import Flag
import pygame


class Direction(Flag):
    """
    Enum for mark the direction and also helps to calculate new position
    """
    UP = (0, - 1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def is_not_opposite(self, keys):
        if keys[pygame.K_UP]:
            return self is not Direction.DOWN
        elif keys[pygame.K_DOWN]:
            return self is not Direction.UP
        elif keys[pygame.K_LEFT]:
            return self is not Direction.RIGHT
        elif keys[pygame.K_RIGHT]:
            return self is not Direction.LEFT
        else:
            return False
