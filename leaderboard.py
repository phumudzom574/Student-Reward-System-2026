
from database import get_connection


def get_leaderboard():
    connection = get_connection()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                participants.ParticipantID,
                participants.Name,
                SUM(pointtransactions.Points) AS TotalPoints
            FROM participants
            INNER JOIN pointtransactions
                ON participants.ParticipantID =
                   pointtransactions.ParticipantID
            GROUP BY
                participants.ParticipantID,
                participants.Name
            ORDER BY
                TotalPoints DESC
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()
