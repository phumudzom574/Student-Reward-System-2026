from database import get_connection


def add_participant(name, email, startdate):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO participants
    (Name, Email, StartDate, Active)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(sql, (name, email, startdate, True))

    conn.commit()
    cursor.close()
    conn.close()


def get_participants():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM participants")

    participants = cursor.fetchall()

    cursor.close()
    conn.close()

    return participants


def delete_participant(participant_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM participants WHERE ParticipantID = %s",
        (participant_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()


def get_participant_by_id(participant_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM participants WHERE ParticipantID = %s",
        (participant_id,)
    )

    participant = cursor.fetchone()

    cursor.close()
    conn.close()

    return participant



def update_participant(participant_id, name, email, startdate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE participants
        SET Name = %s,
            Email = %s,
            StartDate = %s
        WHERE ParticipantID = %s
        """,
        (name, email, startdate, participant_id)
    )

    conn.commit()
    cursor.close()
    conn.close()
