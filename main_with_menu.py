import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Usar o mesmo tamanho do jogo
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Square Dodger - Enhanced")

# Cores
BACKGROUND = (20, 20, 20)
TITLE_COLOR = (0, 128, 255)
BUTTON_COLOR = (50, 100, 200)
BUTTON_HOVER_COLOR = (70, 130, 230)
BUTTON_TEXT_COLOR = (255, 255, 255)

# Fontes
title_font = pygame.font.SysFont("arial", 48, bold=True)
button_font = pygame.font.SysFont("arial", 28)
info_font = pygame.font.SysFont("arial", 16)

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = BUTTON_COLOR
        self.hover_color = BUTTON_HOVER_COLOR
        self.text_color = BUTTON_TEXT_COLOR
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (100, 150, 255), self.rect, 3, border_radius=8)
        
        text_surf = button_font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def is_clicked(self, pos, click):
        return self.rect.collidepoint(pos) and click

class Menu:
    def __init__(self):
        # Botões centralizados na tela 500x500
        self.buttons = [
            Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 30, 200, 50, "Jogar"),
            Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 40, 200, 50, "Sair")
        ]
        
    def draw(self, surface):
        surface.fill(BACKGROUND)
        
        # Título
        title_text = title_font.render("SQUARE DODGER", True, TITLE_COLOR)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        surface.blit(title_text, title_rect)
        
        # Subtítulo
        subtitle_text = info_font.render("Enhanced Edition", True, (200, 200, 255))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4 + 40))
        surface.blit(subtitle_text, subtitle_rect)
        
        # Desenhar botões
        for button in self.buttons:
            button.draw(surface)
        
        # Instruções
       # No método draw() da classe Menu, mude a linha das instruções para:
        info_text = info_font.render("ESC: Menu/Voltar | P: Pausar | SPACE: Reiniciar", True, (180, 180, 180))
        info_rect = info_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 30))
        surface.blit(info_text, info_rect)

def show_menu():
    menu = Menu()
    clock = pygame.time.Clock()
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click = True
        
        # Verificar botões do menu
        for button in menu.buttons:
            button.check_hover(mouse_pos)
            if button.is_clicked(mouse_pos, mouse_click):
                if button.text == "Jogar":
                    return True  # Iniciar jogo
                elif button.text == "Sair":
                    return False  # Sair do jogo
        
        menu.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def main():
    running = True
    
    while running:
        # Mostrar menu
        start_game = show_menu()
        
        if not start_game:
            break
            
        # Se escolheu "Jogar", importar e executar o jogo original
        try:
            # Importar o jogo original
            from game import Game
            
            # Criar e executar o jogo
            game = Game()
            result = game.run()
            
            # Se o jogo retornou "MENU", continuamos no loop para mostrar o menu novamente
            if result == "MENU":
                continue
            else:
                break  # Sair do jogo completamente
                
        except ImportError as e:
            print(f"Erro: Não foi possível carregar o jogo - {e}")
            break
        except Exception as e:
            print(f"Erro durante o jogo: {e}")
            # Volta para o menu se houver erro
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()