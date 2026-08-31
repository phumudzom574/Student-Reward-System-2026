from database import get_connection


def add_transaction(participant_id, rule_id, activity_date, points, notes):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO PointTransactions
        (ParticipantID, RuleID, ActivityDate, Points, Notes)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (participant_id, rule_id, activity_date, points, notes)
    )

    conn.commit()

    cursor.close()
    conn.close()


def get_transactions():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM PointTransactions")

    records = cursor.fetchall()

    cursor.close()
    conn.close()

    return records


def get_history():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM PointTransactions
        ORDER BY ActivityDate DESC
    """)

    records = cursor.fetchall()

    cursor.close()
    conn.close()

    return records