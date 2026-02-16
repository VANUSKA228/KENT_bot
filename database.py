import sqlite3

def init_db():
    with sqlite3.connect('kent_base.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT
            )
        ''')
        conn.commit()

def save_user(user_id, username):
    with sqlite3.connect('kent_base.db') as conn:
        cursor = conn.cursor()
        # INSERT OR REPLACE — это крутая штука: если юзер есть, она его обновит
        cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, username) 
            VALUES (?, ?)
        ''', (user_id, username.replace("@", ""))) # Сохраняем без собачки
        conn.commit()

def get_id_by_username(username):
    clean_name = username.replace("@", "")
    with sqlite3.connect('kent_base.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM users WHERE username = ?', (clean_name,))
        result = cursor.fetchone()
        return result[0] if result else None
        
def get_all_users():
    with sqlite3.connect('kent_base.db') as conn:
        cursor = conn.cursor()
        # Выбираем все ники из таблицы
        cursor.execute('SELECT username FROM users')
        results = cursor.fetchall()
        # Превращаем список кортежей [('user1',), ('user2',)] в обычный список ['user1', 'user2']
        return [row[0] for row in results if row[0] is not None]