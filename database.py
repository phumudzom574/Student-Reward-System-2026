
import os
import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", "3306")),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get("DB_NAME", "student_reward_system")
    )


if __name__ == "__main__":
    try:
        conn = get_connection()
        print("DATABASE CONNECTED SUCCESSFULLY!")

        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")

        print("\nTABLES FOUND:")
        for table in cursor.fetchall():
            print(" -", table[0])

        cursor.close()
        conn.close()

    except Exception as error:
        print("DATABASE CONNECTION FAILED")
        print(error)
