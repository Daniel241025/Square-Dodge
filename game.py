import pygame
import random
from config import GameConfig
from game_state import GameState, GameStats
from entities.player import Player
from entities.enemy import HomingEnemy
from enemy_factory import EnemyFactory
from collision_system import CollisionSystem
from particle_system import ParticleSystem

class Game:
    def __init__(self):
        pygame.init()
        self.config = GameConfig()
        self.stats = GameStats()
        self.state = GameState.RUNNING
        
        self.setup_window()
        self.setup_entities()
        self.setup_systems()
        
    def setup_window(self):
        self.window = pygame.display.set_mode(
            (self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Square Dodger - Enhanced")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 24)
        self.big_font = pygame.font.SysFont("arial", 36, bold=True)
    
    def setup_entities(self):
        self.player = Player(
            self.config.SCREEN_WIDTH // 2,
            self.config.SCREEN_HEIGHT // 2,
            self.config.SCREEN_WIDTH,
            self.config.SCREEN_HEIGHT
        )
        self.enemies = self.create_initial_enemies()
    
    def setup_systems(self):
        self.collision_system = CollisionSystem()
        self.particle_system = ParticleSystem()
        self.start_time = pygame.time.get_ticks()
    
    def create_initial_enemies(self):
        enemies = []
        initial_enemies = [
            ("basic", 2), ("zigzag", 1), ("homing", 1), ("diagonal", 1)
        ]
        
        for enemy_type, count in initial_enemies:
            for _ in range(count):
                enemy = EnemyFactory.create_enemy(
                    enemy_type,
                    self.config.SCREEN_WIDTH,
                    self.config.SCREEN_HEIGHT,
                    self.player.rect if enemy_type == "homing" else None
                )
                enemies.append(enemy)
        return enemies
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                # Se estiver no game over, ESC volta para o menu
                    if self.state == GameState.GAME_OVER:
                        return "MENU"  # Sinal para voltar ao menu
                    else:
                        return False  # Sair do jogo normalmente
                if event.key == pygame.K_SPACE and self.state == GameState.GAME_OVER:
                    self.reset_game()
                if event.key == pygame.K_p and self.state == GameState.RUNNING:
                    self.state = GameState.PAUSED
                elif event.key == pygame.K_p and self.state == GameState.PAUSED:
                    self.state = GameState.RUNNING
    
        return True
    
    def update(self):
        if self.state != GameState.RUNNING:
            return
        
        # Atualizar entidades
        self.player.handle_input()
        
        for enemy in self.enemies:
            if isinstance(enemy, HomingEnemy):
                enemy.set_player_rect(self.player.rect)
            enemy.update()
        
        # Verificar colisões
        collided_enemy = self.collision_system.check_collisions(self.player, self.enemies, self.config.COLLISION_BUFFER)
        if collided_enemy:
            self.handle_game_over()
        
        # Atualizar sistemas
        self.particle_system.update()
        
        # Atualizar estatísticas
        self.stats.score += 1
        self.stats.time_played = (pygame.time.get_ticks() - self.start_time) // 1000
        self.increase_difficulty()
    
    def increase_difficulty(self):
        new_level = self.stats.score // self.config.LEVEL_UP_SCORE + 1
        
        if new_level > self.stats.level:
            self.stats.level = new_level
            self.add_new_enemy()
            self.increase_enemy_speed()
    
    def add_new_enemy(self):
        if len(self.enemies) < self.config.MAX_ENEMIES:
            enemy_type = EnemyFactory.get_random_enemy_type(self.stats.level)
            new_enemy = EnemyFactory.create_enemy(
                enemy_type,
                self.config.SCREEN_WIDTH,
                self.config.SCREEN_HEIGHT,
                self.player.rect if enemy_type == "homing" else None
            )
            self.enemies.append(new_enemy)
    
    def increase_enemy_speed(self):
        for enemy in self.enemies:
            enemy.speed += 0.2
            if hasattr(enemy, 'oscillation_speed'):
                enemy.oscillation_speed += 0.005
            if hasattr(enemy, 'homing_strength'):
                enemy.homing_strength = min(0.1, enemy.homing_strength + 0.002)
    
    def handle_game_over(self):
        self.state = GameState.GAME_OVER
        if self.stats.score > self.stats.highscore:
            self.stats.highscore = self.stats.score
    
    # SALVAR NO BANCO DE DADOS - NOVA LINHA ADICIONADA
        self.stats.save_to_database()
    
    # Adicionar efeito de partículas
        self.particle_system.add_explosion(
            self.player.rect.centerx,
            self.player.rect.centery,
            (255, 50, 50),
            20
        )
    
    def reset_game(self):
        self.stats = GameStats()
        self.state = GameState.RUNNING
        self.start_time = pygame.time.get_ticks()
        
        self.player.rect.center = (
            self.config.SCREEN_WIDTH // 2,
            self.config.SCREEN_HEIGHT // 2
        )
        
        for enemy in self.enemies:
            enemy.reset()
        
        # Manter apenas os inimigos iniciais
        self.enemies = self.enemies[:6] if len(self.enemies) > 6 else self.enemies
    
    def render(self):
        self.window.fill((20, 20, 20))
        
        # Renderizar entidades
        self.player.draw(self.window)
        for enemy in self.enemies:
            enemy.draw(self.window)
        
        # Renderizar sistemas
        self.particle_system.draw(self.window)
        
        # Renderizar UI
        self.render_ui()
        
        # Renderizar tela de game over
        if self.state == GameState.GAME_OVER:
            self.render_game_over()
        
        # Renderizar tela de pausa
        if self.state == GameState.PAUSED:
            self.render_pause_screen()
        
        pygame.display.flip()
    
    def render_ui(self):
        # Score e Highscore
        score_text = self.font.render(f"Score: {self.stats.score}", True, (255, 255, 255))
        highscore_text = self.font.render(f"Highscore: {self.stats.highscore}", True, (200, 200, 200))
        level_text = self.font.render(f"Level: {self.stats.level}", True, (200, 255, 200))
        time_text = self.font.render(f"Time: {self.stats.time_played}s", True, (200, 200, 255))
        
        self.window.blit(score_text, (10, 10))
        self.window.blit(highscore_text, (10, 40))
        self.window.blit(level_text, (10, 70))
        self.window.blit(time_text, (10, 100))
        
        # Inimigos restantes
        enemies_text = self.font.render(f"Enemies: {len(self.enemies)}", True, (255, 200, 200))
        self.window.blit(enemies_text, (10, 130))
    
    def render_game_over(self):
        overlay = pygame.Surface((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.window.blit(overlay, (0, 0))
    
        game_over_text = self.big_font.render("GAME OVER", True, (255, 50, 50))
        score_text = self.font.render(f"Final Score: {self.stats.score}", True, (255, 255, 255))
        restart_text = self.font.render("Press SPACE to restart or ESC to return to menu", True, (200, 200, 200))
    
        self.window.blit(game_over_text, game_over_text.get_rect(center=(self.config.SCREEN_WIDTH//2, self.config.SCREEN_HEIGHT//2 - 50)))
        self.window.blit(score_text, score_text.get_rect(center=(self.config.SCREEN_WIDTH//2, self.config.SCREEN_HEIGHT//2)))
        self.window.blit(restart_text, restart_text.get_rect(center=(self.config.SCREEN_WIDTH//2, self.config.SCREEN_HEIGHT//2 + 50)))
    
    def render_pause_screen(self):
        overlay = pygame.Surface((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.window.blit(overlay, (0, 0))
        
        pause_text = self.big_font.render("PAUSED", True, (255, 255, 255))
        continue_text = self.font.render("Press P to continue", True, (200, 200, 200))
        
        self.window.blit(pause_text, pause_text.get_rect(center=(self.config.SCREEN_WIDTH//2, self.config.SCREEN_HEIGHT//2 - 20)))
        self.window.blit(continue_text, continue_text.get_rect(center=(self.config.SCREEN_WIDTH//2, self.config.SCREEN_HEIGHT//2 + 20)))
    
    def run(self):
        running = True
        while running:
            result = self.handle_events()
        
            if result == "MENU":
                return "MENU"  # Sinal para voltar ao menu
            elif result is False:
                break
            
            self.update()
            self.render()
            self.clock.tick(self.config.FPS)
    
        pygame.quit()
        return "EXIT"