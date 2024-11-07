import bcrypt
from db import create_connection

def check_user(email, password):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user and bcrypt.checkpw(password.encode(), user["password"].encode()):
        return user
    return None
