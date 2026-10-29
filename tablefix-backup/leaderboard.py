from database import get_connection


def get_leaderboard():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            participants.ParticipantID,
            participants.Name,
            SUM(pointtransactions.Points) AS TotalPoints
        FROM participants
        INNER JOIN pointtransactions
            ON participants.ParticipantID = pointtransactions.ParticipantID
        GROUP BY
            participants.ParticipantID,
            participants.Name
        ORDER BY
            SUM(pointtransactions.Points) DESC
    """)

    records = cursor.fetchall()

    cursor.close()
    conn.close()

    return records