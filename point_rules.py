from database import get_connection
from validation import positive_integer


def add_point_rule(activity_name, description, points, max_per_day, active):
    if not isinstance(activity_name, str):
        raise ValueError("Activity name is required.")
    if not isinstance(description, str):
        raise ValueError("Description is required.")

    activity_name = activity_name.strip()
    description = description.strip()
    if not activity_name:
        raise ValueError("Activity name is required.")
    if len(activity_name) > 100:
        raise ValueError("Activity name must be 100 characters or fewer.")
    if not description:
        raise ValueError("Description is required.")
    points = positive_integer(points, "Points")
    max_per_day = positive_integer(max_per_day, "Daily limit")
    if not isinstance(active, bool):
        raise ValueError("Choose whether the point rule is active.")

    conn = get_connection()
    cursor = None
    try:
        conn.start_transaction()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM pointrules
            WHERE LOWER(TRIM(ActivityName)) = LOWER(TRIM(%s))
            """,
            (activity_name,)
        )
        if int(cursor.fetchone()[0]) > 0:
            raise ValueError("A rule with this name already exists.")

        cursor.execute(
            """
            INSERT INTO pointrules
            (ActivityName, Description, Points, MaxPerDay, Active)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (activity_name, description, points, max_per_day, active)
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        try:
            if cursor is not None:
                cursor.close()
        finally:
            conn.close()


def get_point_rules():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT RuleID, ActivityName, Description,
                       Points, MaxPerDay, Active
                FROM pointrules
                ORDER BY RuleID
                """
            )
            return cursor.fetchall()
        finally:
            cursor.close()
    finally:
        conn.close()


def get_active_point_rules():
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT RuleID, ActivityName, Description,
                       Points, MaxPerDay, Active
                FROM pointrules
                WHERE Active = 1
                ORDER BY RuleID
                """
            )
            return cursor.fetchall()
        finally:
            cursor.close()
    finally:
        conn.close()