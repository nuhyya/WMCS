from db import create_connection

def check_user(email, password):
    """Verify if a user exists and the password matches."""
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    # Compare the plain text password (for simplicity)
    if user and user["password"] == password:
        return user
    return None
