import sqlite3
from database import GameDatabase

class StatsViewer:
    def __init__(self):
        self.db = GameDatabase()
    
    def show_high_scores(self):
        """Exibe os melhores scores no terminal"""
        print("=== MELHORES SCORES ===")
        high_scores = self.db.get_high_scores(10)
        
        if not high_scores:
            print("Nenhum score registrado ainda!")
            return
        
        for i, (player, score, level, time, date) in enumerate(high_scores, 1):
            print(f"{i}. {player}: {score} pontos (Nível {level}) - {date}")
    
    def show_player_stats(self, player_name="Player"):
        """Exibe estatísticas de um jogador"""
        print(f"\n=== ESTATÍSTICAS DE {player_name.upper()} ===")
        stats = self.db.get_player_stats(player_name)
        
        if stats and stats[0] > 0:
            games, best, avg, highest, total_time = stats
            print(f"Jogos realizados: {games}")
            print(f"Melhor score: {best}")
            print(f"Score médio: {avg:.1f}")
            print(f"Maior nível alcançado: {highest}")
            print(f"Tempo total de jogo: {total_time} segundos")
        else:
            print("Nenhum jogo encontrado para este jogador!")
    
    def show_recent_games(self, days=7):
        """Exibe jogos recentes"""
        print(f"\n=== JOGOS DOS ÚLTIMOS {days} DIAS ===")
        recent_games = self.db.get_game_history(days)
        
        if not recent_games:
            print("Nenhum jogo encontrado neste período!")
            return
        
        for date, player, score, level in recent_games:
            print(f"{date}: {player} - {score} pontos (Nível {level})")

def main():
    viewer = StatsViewer()
    
    while True:
        print("\n" + "="*50)
        print("VISUALIZADOR DE ESTATÍSTICAS - SQUARE DODGER")
        print("="*50)
        print("1. Ver Melhores Scores")
        print("2. Ver Minhas Estatísticas")
        print("3. Ver Jogos Recentes")
        print("4. Sair")
        
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == "1":
            viewer.show_high_scores()
        elif choice == "2":
            name = input("Nome do jogador (Enter para 'Player'): ").strip() or "Player"
            viewer.show_player_stats(name)
        elif choice == "3":
            try:
                days = int(input("Número de dias (padrão 7): ") or "7")
                viewer.show_recent_games(days)
            except ValueError:
                print("Número inválido!")
        elif choice == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()