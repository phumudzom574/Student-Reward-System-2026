from database import get_connection


def get_leaderboard():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            Participants.ParticipantID,
            Participants.Name,
            SUM(PointTransactions.Points) AS TotalPoints
        FROM Participants
        INNER JOIN PointTransactions
            ON Participants.ParticipantID = PointTransactions.ParticipantID
        GROUP BY
            Participants.ParticipantID,
            Participants.Name
        ORDER BY
            SUM(PointTransactions.Points) DESC
    """)

    records = cursor.fetchall()

    cursor.close()
    conn.close()

    return records