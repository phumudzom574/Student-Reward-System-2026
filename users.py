from database import get_connection


def validate_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM Users WHERE Username=%s AND Password=%s",
        (username, password)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user