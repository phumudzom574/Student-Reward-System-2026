from database import get_connection


def add_point_rule(activity_name, description, points, max_per_day, active):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO PointRules
        (ActivityName, Description, Points, MaxPerDay, Active)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (activity_name, description, points, max_per_day, active)
    )

    conn.commit()
    cursor.close()
    conn.close()


def get_point_rules():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM PointRules")

    rules = cursor.fetchall()

    cursor.close()
    conn.close()

    return rules