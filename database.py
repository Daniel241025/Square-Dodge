import sqlite3
import datetime

class GameDatabase:
    def __init__(self, db_name="game_stats.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT DEFAULT 'Player',
                score INTEGER NOT NULL,
                level INTEGER NOT NULL,
                time_played INTEGER NOT NULL,
                enemies_dodged INTEGER NOT NULL,
                session_date TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_settings (
                id INTEGER PRIMARY KEY,
                setting_name TEXT UNIQUE NOT NULL,
                setting_value TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            INSERT OR IGNORE INTO game_settings (id, setting_name, setting_value) 
            VALUES (1, 'player_name', 'Player')
        ''')
        
        cursor.execute('''
            INSERT OR IGNORE INTO game_settings (id, setting_name, setting_value) 
            VALUES (2, 'difficulty', 'normal')
        ''')
        
        conn.commit()
        conn.close()
    
    def save_game_session(self, score, level, time_played, enemies_dodged, player_name=None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        if player_name is None:
            player_name = self.get_setting('player_name')
        
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            INSERT INTO game_sessions 
            (player_name, score, level, time_played, enemies_dodged, session_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (player_name, score, level, time_played, enemies_dodged, current_date))
        
        conn.commit()
        conn.close()
    
    def get_high_scores(self, limit=10):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT player_name, score, level, time_played, session_date 
            FROM game_sessions 
            ORDER BY score DESC 
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def get_player_stats(self, player_name):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as games_played,
                MAX(score) as best_score,
                AVG(score) as average_score,
                MAX(level) as highest_level,
                SUM(time_played) as total_time_played
            FROM game_sessions 
            WHERE player_name = ?
        ''', (player_name,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result
    
    def get_setting(self, setting_name):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT setting_value FROM game_settings WHERE setting_name = ?
        ''', (setting_name,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def update_setting(self, setting_name, setting_value):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO game_settings (setting_name, setting_value)
            VALUES (?, ?)
        ''', (setting_name, setting_value))
        
        conn.commit()
        conn.close()
    
    def get_game_history(self, days=30):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        start_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
        
        cursor.execute('''
            SELECT session_date, player_name, score, level 
            FROM game_sessions 
            WHERE session_date >= ?
            ORDER BY session_date DESC
        ''', (start_date,))
        
        results = cursor.fetchall()
        conn.close()
        
        return results