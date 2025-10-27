import sqlite3
from werkzeug.security import check_password_hash

def init_db():
    """Initialize the database with demo users"""
    import init_db
    return True

def vulnerable_auth_raw(username, password):
    """Vulnerable login - DO NOT USE IN PRODUCTION"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Vulnerable to SQL injection
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result is not None

def verify_user_safe(username, password):
    """Safe login with password hashing and parameterized queries"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username=?', (username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return check_password_hash(result[0], password)
    return False