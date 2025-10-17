import pygame, random
import math

class Enemy:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0, 0, 30, 30)
        self.speed = random.randint(3, 6)
        self.color = (255, 50, 50)
        self.spawn_side = None
        self.set_initial_position()
        
    def set_initial_position(self):
        # Escolhe um lado aleatório para spawnar
        self.spawn_side = random.choice(['top', 'bottom', 'left', 'right'])
        
        if self.spawn_side == 'top':
            self.rect.x = random.randint(0, self.width - self.rect.width)
            self.rect.y = -self.rect.height
        elif self.spawn_side == 'bottom':
            self.rect.x = random.randint(0, self.width - self.rect.width)
            self.rect.y = self.height
        elif self.spawn_side == 'left':
            self.rect.x = -self.rect.width
            self.rect.y = random.randint(0, self.height - self.rect.height)
        elif self.spawn_side == 'right':
            self.rect.x = self.width
            self.rect.y = random.randint(0, self.height - self.rect.height)
    
    def get_movement_direction(self):
        # Define a direção do movimento baseado no lado de spawn
        if self.spawn_side == 'top':
            return 0, 1  # Move para baixo
        elif self.spawn_side == 'bottom':
            return 0, -1  # Move para cima
        elif self.spawn_side == 'left':
            return 1, 0  # Move para direita
        elif self.spawn_side == 'right':
            return -1, 0  # Move para esquerda
    
    def is_off_screen(self):
        # Verifica se saiu completamente da tela pela borda oposta
        if self.spawn_side == 'top' and self.rect.y > self.height:
            return True
        elif self.spawn_side == 'bottom' and self.rect.y < -self.rect.height:
            return True
        elif self.spawn_side == 'left' and self.rect.x > self.width:
            return True
        elif self.spawn_side == 'right' and self.rect.x < -self.rect.width:
            return True
        return False
    
    def update(self):
        dx, dy = self.get_movement_direction()
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        
        # Verifica se saiu da tela para resetar
        if self.is_off_screen():
            self.reset()
    
    def reset(self):
        self.set_initial_position()
        self.speed = random.randint(3, 6)
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


class ZigZagEnemy(Enemy):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.color = (255, 150, 50)  # Laranja
        self.oscillation_speed = random.uniform(0.05, 0.1)
        self.angle = 0
        self.original_spawn_side = self.spawn_side
    
    def update(self):
        dx, dy = self.get_movement_direction()
        
        # Movimento principal
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        
        # Movimento de zigue-zague perpendicular à direção principal
        self.angle += self.oscillation_speed
        
        if self.original_spawn_side in ['top', 'bottom']:
            # Se veio de cima ou baixo, oscila horizontalmente
            self.rect.x += math.sin(self.angle) * 3
        else:
            # Se veio dos lados, oscila verticalmente
            self.rect.y += math.sin(self.angle) * 3
        
        # Verifica se saiu da tela para resetar
        if self.is_off_screen():
            self.reset()
    
    def reset(self):
        super().reset()
        self.original_spawn_side = self.spawn_side
        self.oscillation_speed = random.uniform(0.05, 0.1)
        self.angle = 0


class HomingEnemy(Enemy):
    def __init__(self, width, height, player_rect=None):
        super().__init__(width, height)
        self.color = (255, 50, 150)  # Rosa
        self.player_rect = player_rect
        self.homing_strength = 0.05
        self.original_spawn_side = self.spawn_side
    
    def set_player_rect(self, player_rect):
        self.player_rect = player_rect
    
    def update(self):
        dx, dy = self.get_movement_direction()
        
        # Movimento base na direção original
        base_dx = dx * self.speed
        base_dy = dy * self.speed
        
        # Movimento de perseguição ao jogador
        if self.player_rect:
            # Calcula a direção para o jogador
            target_dx = self.player_rect.x - self.rect.x
            target_dy = self.player_rect.y - self.rect.y
            
            # Normaliza o vetor de direção
            distance = max(1, math.sqrt(target_dx**2 + target_dy**2))
            target_dx /= distance
            target_dy /= distance
            
            # Combina movimento base com perseguição
            final_dx = base_dx + target_dx * self.speed * self.homing_strength
            final_dy = base_dy + target_dy * self.speed * self.homing_strength
        else:
            final_dx, final_dy = base_dx, base_dy
        
        self.rect.x += final_dx
        self.rect.y += final_dy
        
        # Verifica se saiu da tela para resetar
        if self.is_off_screen():
            self.reset()
    
    def reset(self):
        super().reset()
        self.original_spawn_side = self.spawn_side
        self.homing_strength = random.uniform(0.03, 0.07)


class DiagonalEnemy(Enemy):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.color = (50, 255, 100)  # Verde
        self.diagonal_direction = random.choice([-1, 1])
    
    def update(self):
        dx, dy = self.get_movement_direction()
        
        # Movimento diagonal baseado na direção original + componente diagonal
        if self.spawn_side in ['top', 'bottom']:
            # Se veio de cima/baixo, adiciona movimento horizontal
            self.rect.x += dx * self.speed + self.diagonal_direction * 2
            self.rect.y += dy * self.speed
        else:
            # Se veio dos lados, adiciona movimento vertical
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed + self.diagonal_direction * 2
        
        # Verifica se saiu da tela para resetar
        if self.is_off_screen():
            self.reset()
    
    def reset(self):
        super().reset()
        self.diagonal_direction = random.choice([-1, 1])