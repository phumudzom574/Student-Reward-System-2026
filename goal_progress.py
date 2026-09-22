<<<<<<< HEAD
from database import get_connection


def add_goal_progress(goal_id, participant_id, current_points, completed):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO GoalProgress
        (GoalID, ParticipantID, CurrentPoints, Completed)
        VALUES (%s, %s, %s, %s)
        """,
        (goal_id, participant_id, current_points, completed)
    )

    conn.commit()

    cursor.close()
    conn.close()


def get_goal_progress():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM GoalProgress")

    records = cursor.fetchall()

    cursor.close()
    conn.close()

=======
from database import get_connection


def add_goal_progress(goal_id, participant_id, current_points, completed):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO GoalProgress
        (GoalID, ParticipantID, CurrentPoints, Completed)
        VALUES (%s, %s, %s, %s)
        """,
        (goal_id, participant_id, current_points, completed)
    )

    conn.commit()

    cursor.close()
    conn.close()


def get_goal_progress():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM GoalProgress")

    records = cursor.fetchall()

    cursor.close()
    conn.close()

>>>>>>> origin/main
    return records