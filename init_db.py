import sqlite3
from werkzeug.security import generate_password_hash

# connect or create database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
''')

# insert demo users
users = [
    ('admin', generate_password_hash('admin123')),
    ('student', generate_password_hash('password')),
    ('tester', generate_password_hash('test123'))
]

for u, p in users:
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (u, p))
    except sqlite3.IntegrityError:
        pass

conn.commit()
conn.close()
print("✅ Database initialized with demo users.")
