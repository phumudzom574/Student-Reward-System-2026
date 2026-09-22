<<<<<<< HEAD
from database import get_connection

try:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO PointTransactions
        (ParticipantsID, RuleID, ActivityDate, Points, Notes)
        VALUES (?, ?, ?, ?, ?)
        """,
        (1, 1, "2026-08-11", 10, "Test Transaction")
    )

    conn.commit()
    print("INSERT SUCCESSFUL")

except Exception as e:
    print("ERROR:")
    print(e)

finally:
    try:
        conn.close()
    except:
=======
from database import get_connection

try:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO PointTransactions
        (ParticipantsID, RuleID, ActivityDate, Points, Notes)
        VALUES (?, ?, ?, ?, ?)
        """,
        (1, 1, "2026-08-11", 10, "Test Transaction")
    )

    conn.commit()
    print("INSERT SUCCESSFUL")

except Exception as e:
    print("ERROR:")
    print(e)

finally:
    try:
        conn.close()
    except:
>>>>>>> origin/main
        pass