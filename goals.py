from database import get_connection
from validation import iso_date, positive_integer


def add_goal(participant_id, start_date, end_date, target_points):
    participant_id = positive_integer(participant_id, "Participant ID")
    start_date = iso_date(start_date, "Start date")
    end_date = iso_date(end_date, "End date")
    target_points = positive_integer(target_points, "Target points")
    if end_date < start_date:
        raise ValueError("End date must be on or after the start date.")

    conn = get_connection()
    cursor = None
    try:
        conn.start_transaction()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT ParticipantID
            FROM participants
            WHERE ParticipantID = %s
            FOR UPDATE
            """,
            (participant_id,)
        )
        if cursor.fetchone() is None:
            raise ValueError("The selected participant does not exist.")
        cursor.execute(
            """
            SELECT COUNT(*) AS GoalCount
            FROM goals
            WHERE ParticipantID = %s
              AND StartDate = %s
              AND EndDate = %s
              AND TargetPoints = %s
            """,
            (participant_id, start_date, end_date, target_points)
        )
        if int(cursor.fetchone()[0]) > 0:
            raise ValueError(
                "This goal has already been created for this participant."
            )

        cursor.execute(
            """
            INSERT INTO goals
            (ParticipantID, StartDate, EndDate, TargetPoints)
            VALUES (%s, %s, %s, %s)
            """,
            (participant_id, start_date, end_date, target_points)
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


def get_goals():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM goals")

    goals = cursor.fetchall()

    cursor.close()
    conn.close()

    return goals