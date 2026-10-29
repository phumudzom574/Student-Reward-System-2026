from database import get_connection


def add_point_rule(activity_name, description, points, max_per_day, active):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        try:
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