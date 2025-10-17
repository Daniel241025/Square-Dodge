import random
from entities.enemy import Enemy, ZigZagEnemy, HomingEnemy, DiagonalEnemy

class EnemyFactory:
    @staticmethod
    def create_enemy(enemy_type, width, height, player_rect=None):
        if enemy_type == "basic":
            return Enemy(width, height)
        elif enemy_type == "zigzag":
            return ZigZagEnemy(width, height)
        elif enemy_type == "homing":
            return HomingEnemy(width, height, player_rect)
        elif enemy_type == "diagonal":
            return DiagonalEnemy(width, height)
        else:
            return Enemy(width, height)
    
    @staticmethod
    def get_random_enemy_type(level):
        weights = {
            "basic": max(0.5, 1.0 - level * 0.1),
            "zigzag": min(0.3, 0.1 + level * 0.05),
            "homing": min(0.2, 0.05 + level * 0.03),
            "diagonal": min(0.25, 0.08 + level * 0.04)
        }
        return random.choices(list(weights.keys()), weights=list(weights.values()))[0]