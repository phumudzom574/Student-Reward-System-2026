from database import get_connection


def add_goal_progress(goal_id, participant_id, current_points, completed):
    conn = get_connection()
    cursor = None

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO goalprogress
                (GoalID, ParticipantID, CurrentPoints, Completed)
            VALUES (%s, %s, %s, %s)
            """,
            (goal_id, participant_id, current_points, completed)
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


def get_goal_progress():
    """Return named fields so the template does not depend on column positions."""
    conn = get_connection()
    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                ProgressID,
                GoalID,
                ParticipantID,
                COALESCE(CurrentPoints, 0) AS CurrentPoints,
                COALESCE(Completed, 0) AS Completed
            FROM goalprogress
            ORDER BY ProgressID DESC
            """
        )
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()
