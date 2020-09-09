import random

from config import Config
from model.Location import Location


class Board:
    """Represent the game board"""
    def __init__(self, size):
        self.table_size = size
        self.food_location = Location(0, 0)

        self.generate_food()

    def get_food_location(self):
        return self.food_location.get_location()

    def generate_food(self):
        self.food_location = Location(*random_position())


def random_position():
    """Generate a random position on the board"""
    return (random.randint(0, Config.table_size - 1),
            random.randint(0, Config.table_size - 1))
