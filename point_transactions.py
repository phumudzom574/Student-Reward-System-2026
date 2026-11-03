from database import get_connection
from validation import iso_date, positive_integer


def add_transaction(participant_id, rule_id, activity_date, notes):
    participant_id = positive_integer(participant_id, "Participant ID")
    rule_id = positive_integer(rule_id, "Point rule")
    activity_date = iso_date(activity_date, "Activity date")
    if notes is None:
        notes = ""
    elif not isinstance(notes, str):
        raise ValueError("Notes must be text.")
    notes = notes.strip()

    conn = get_connection()
    cursor = None
    try:
        conn.start_transaction()
        cursor = conn.cursor(dictionary=True)
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
            SELECT RuleID, Points, MaxPerDay, Active
            FROM pointrules
            WHERE RuleID = %s
            FOR UPDATE
            """,
            (rule_id,)
        )
        rule = cursor.fetchone()
        if not rule:
            raise ValueError("The selected point rule does not exist.")
        if int(rule["Active"]) != 1:
            raise ValueError("This point rule is inactive.")
        if rule["Points"] is None:
            raise ValueError("The selected point rule is not configured correctly.")

        if rule["MaxPerDay"] is None:
            raise ValueError(
                "This rule has no valid daily limit configured."
            )

        max_per_day = int(rule["MaxPerDay"])
        configured_points = int(rule["Points"])
        if max_per_day < 1:
            raise ValueError(
                "This rule has no valid daily limit configured."
            )

        cursor.execute(
            """
            SELECT COUNT(*) AS DuplicateCount
            FROM pointtransactions
            WHERE ParticipantID = %s
              AND RuleID = %s
              AND ActivityDate = %s
              AND COALESCE(Notes, '') = %s
            """,
            (participant_id, rule_id, activity_date, notes)
        )
        if int(cursor.fetchone()["DuplicateCount"]) > 0:
            raise ValueError(
                "This award has already been recorded for this participant."
            )

        cursor.execute(
            """
            SELECT COUNT(*) AS AwardCount
            FROM pointtransactions
            WHERE ParticipantID = %s
              AND RuleID = %s
              AND ActivityDate = %s
            """,
            (participant_id, rule_id, activity_date)
        )
        awards_today = int(cursor.fetchone()["AwardCount"])
        if awards_today >= max_per_day:
            raise ValueError(
                "The daily limit for this point rule has been reached."
            )

        cursor.execute(
            """
            INSERT INTO pointtransactions
            (ParticipantID, RuleID, ActivityDate, Points, Notes)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (participant_id, rule_id, activity_date, configured_points, notes)
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


def get_transactions():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pointtransactions")

    records = cursor.fetchall()

    cursor.close()
    conn.close()

    return records


def get_history():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM pointtransactions
        ORDER BY ActivityDate DESC
    """)

    records = cursor.fetchall()

    cursor.close()
    conn.close()

    return records


def get_leaderboard():
    conn = get_connection()
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                p.ParticipantID,
                p.Name,
                COALESCE(SUM(t.Points), 0) AS TotalPoints
            FROM participants p
            LEFT JOIN pointtransactions t
                ON p.ParticipantID = t.ParticipantID
            GROUP BY p.ParticipantID, p.Name
            ORDER BY TotalPoints DESC
            """
        )
        return cursor.fetchall()
    finally:
        try:
            if cursor is not None:
                cursor.close()
        finally:
            conn.close()