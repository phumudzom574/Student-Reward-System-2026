from database import get_connection

try:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM Participants
        WHERE ParticipantID IN (1, 2)
    """)

    conn.commit()

    print("TEST RECORDS REMOVED SUCCESSFULLY!")

    conn.close()

except Exception as error:
    print("ERROR:")
    print(error)