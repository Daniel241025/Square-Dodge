import pygame

class Player:
    def __init__(self, x, y, screen_width, screen_height):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = 5
        self.color = (0, 128, 255)
        self.screen_width = screen_width
        self.screen_height = screen_height

    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Movimento para esquerda
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        # Movimento para direita
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        # Movimento para cima
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        # Movimento para baixo
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        
        # Manter jogador dentro da tela
        self.rect.x = max(0, min(self.rect.x, self.screen_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.screen_height - self.rect.height))

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)