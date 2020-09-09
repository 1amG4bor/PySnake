from model.Board import Board


class Game:
    """Represent the game board"""
    player = board = speed = prev_limit = level_limit = level = score = top_score = None

    def __init__(self, player, size):
        self.player = player
        self.init_game(size)
        self.top_score = 0

    def score_inc(self, points):
        self.score += points
        if self.score > self.level_limit:
            self.level += 1
            self.speed += self.level
            self.prev_limit = self.level_limit
            self.level_limit *= 2

    def restart(self, score, size):
        self.init_game(size)
        if score > self.top_score:
            self.top_score = score

    def init_game(self, size):
        self.board = Board(size)
        self.speed = 10
        self.prev_limit = 0
        self.level_limit = 500
        self.level = 1
        self.score = 0
        self.player.init()





