from enum import Enum
from database import GameDatabase

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
        self.database = GameDatabase()
        
        # Carregar highscore do banco de dados
        self.load_highscore()
    
    def load_highscore(self):
        """Carrega o highscore do banco de dados"""
        high_scores = self.database.get_high_scores(1)
        if high_scores:
            self.highscore = high_scores[0][1]  # Score do primeiro lugar
    
    def save_to_database(self):
        """Salva a sessão atual no banco de dados"""
        self.database.save_game_session(
            score=self.score,
            level=self.level,
            time_played=self.time_played,
            enemies_dodged=self.enemies_dodged
        )