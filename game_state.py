from enum import Enum

class GameState(Enum):
    RUNNING = 1
    GAME_OVER = 2
    PAUSED = 3

class GameStats:
    def __init__(self):
        self.score = 0
        self.highscore = 0
        self.level = 1
        self.enemies_dodged = 0
        self.time_played = 0