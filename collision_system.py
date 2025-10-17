import pygame

class CollisionSystem:
    @staticmethod
    def check_collision(rect1, rect2, buffer=0):
        """Verifica colisão com buffer opcional"""
        return rect1.colliderect(pygame.Rect(rect2.x - buffer, rect2.y - buffer, 
                                           rect2.width + buffer * 2, rect2.height + buffer * 2))
    
    @staticmethod
    def check_collisions(player, enemies, buffer=0):
        """Verifica colisões entre jogador e lista de inimigos"""
        for enemy in enemies:
            if CollisionSystem.check_collision(player.rect, enemy.rect, buffer):
                return enemy
        return None