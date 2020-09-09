from typing import List

from config import Config
from model.Direction import Direction
from model.Location import Location


class Player:
    """
    Represent the "Player" in the game
    Contains the movement logic as well as the properties of the player
    """
    name = head = body = direction = None

    def __init__(self, name):
        self.name = name
        self.init()

    def move(self, game):
        """
        The logic of moving the snake that includes collision detection and eating too.
        :return: whether the snake is still alive
        """
        # next location
        x, y = self.head.get_location()
        old_direction = self.direction
        # Calculate the next coordinate based on moving direction
        new = Location(*[sum(i) for i in zip((x, y), self.direction.value)])

        # verify valid move
        collision = self.check_collision(*new.get_location())

        if not collision:
            self.head.set_location(*new.get_location())
            self._add_body_part(Location(x, y), old_direction)

            # check whether he found food
            if self.check_for_food(game.board, new.get_location()):
                game.board.generate_food()
                game.score_inc(500)
            else:
                self.body.pop(-1)

        return not collision

    def check_collision(self, x, y):
        """
        Examine whether the given coordinate is out of the board or the snake itself
        :return: True if the snake collide, or False otherwise
        """
        if x < 0 or x >= Config.table_size or y < 0 or y >= Config.table_size:
            return True
        if any(tail.location.x == x and tail.location.y == y for tail in self.body):
            return True
        return False

    @staticmethod
    def check_for_food(board, location):
        return board.get_food_location() == location

    def _add_body_part(self, location: Location, direction: Direction):
        self.body.insert(0, Body(location, direction))

    def init(self):
        self.head: Location = Location(10, 10)
        self.body: List[Body] = [
            Body(Location(10, 11), Direction.UP),
            Body(Location(10, 12), Direction.UP),
            Body(Location(10, 13), Direction.UP)
        ]
        self.direction = Direction.UP


class Body:
    """Represent the parts of the snake's body/tail"""
    def __init__(self, location: Location, direction: Direction):
        self.location = location
        self.direction = direction
