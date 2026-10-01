import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="student_reward_system"
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