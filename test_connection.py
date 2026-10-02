from database import get_connection

try:
    conn = get_connection()
    print("CONNECTED SUCCESSFULLY")

    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")

    for table in cursor.fetchall():
        print(table[0])

    conn.close()

except Exception as e:
    print("ERROR:")
    print(e)