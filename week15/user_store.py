import sqlite3


class UserStore:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                age  INTEGER NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def load(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, email, age FROM users')
        rows = cursor.fetchall()
        conn.close()
        users = []
        for row in rows:
            users.append({
                'id':    row[0],
                'name':  row[1],
                'email': row[2],
                'age':   row[3]
            })
        return users

    def save(self, user):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (name, email, age) VALUES (?, ?, ?)',
            (user['name'], user['email'], user['age'])
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id

    def find_by_id(self, user_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, name, email, age FROM users WHERE id = ?',
            (user_id,)
        )
        row = cursor.fetchone()
        conn.close()
        if row is None:
            return None
        return {'id': row[0], 'name': row[1], 'email': row[2], 'age': row[3]}

    def search_users(self, search_term):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, name, email, age FROM users WHERE name LIKE ?',
            (f'%{search_term}%',)
        )
        rows = cursor.fetchall()
        conn.close()
        return [
            {'id': row[0], 'name': row[1], 'email': row[2], 'age': row[3]}
            for row in rows
        ]

    def update_user(self, user_id, updated_data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE users SET name = ?, email = ?, age = ? WHERE id = ?',
            (updated_data['name'], updated_data['email'], updated_data['age'], user_id)
        )
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        return rows_affected > 0

    def delete_user(self, user_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        return rows_affected > 0