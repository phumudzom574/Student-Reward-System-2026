from database import get_connection


def add_goal(participant_id, start_date, end_date, target_points):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO Goals
        (ParticipantID, StartDate, EndDate, TargetPoints)
        VALUES (%s, %s, %s, %s)
        """,
        (participant_id, start_date, end_date, target_points)
    )

    conn.commit()

    cursor.close()
    conn.close()


def get_goals():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Goals")

    goals = cursor.fetchall()

    cursor.close()
    conn.close()

    return goals