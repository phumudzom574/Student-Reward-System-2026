from database import get_connection

conn = get_connection()
cursor = conn.cursor()

try:
    cursor.execute(
        """
        INSERT INTO PointTransactions
        (ParticipantsID, RuleID, ActivityDate, Points, Notes)
        VALUES (?, ?, ?, ?, ?)
        """,
        (1, 1, "2026-08-11", 10, "Test")
    )

    conn.commit()
    print("INSERT SUCCESSFUL")

except Exception as e:
    print("ERROR:")
    print(e)

finally:
    conn.close()