from flask import Flask, render_template, request, redirect, session, send_file

from participants import (
    add_participant,
    get_participants,
    delete_participant,
    get_participant_by_id,
    update_participant
)

from point_rules import (
    add_point_rule,
    get_point_rules
)

from point_transactions import (
    add_transaction,
    get_transactions,
    get_history
)

from goals import (
    add_goal,
    get_goals
)

from goal_progress import (
    add_goal_progress,
    get_goal_progress
)

from leaderboard import get_leaderboard

from users import validate_user

from database import get_connection

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from datetime import datetime


app = Flask(__name__)

app.secret_key = "rewardsystem123"


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = validate_user(username, password)

        if user:

            session["user"] = username

            return redirect("/")

        return render_template(
            "login.html",
            error="Invalid Username or Password"
        )

    return render_template("login.html")


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html")


# =========================================================
# ADD PARTICIPANT
# =========================================================

@app.route("/add_participant", methods=["GET", "POST"])
def participant():

    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":

        name = request.form["name"]

        email = request.form["email"]

        startdate = request.form["startdate"]

        add_participant(
            name,
            email,
            startdate
        )

        return redirect("/participants")

    return render_template("add_participant.html")


# =========================================================
# VIEW PARTICIPANTS
# =========================================================

@app.route("/participants")
def participants():

    if "user" not in session:
        return redirect("/login")

    records = get_participants()

    return render_template(
        "view_participants.html",
        participants=records
    )


# =========================================================
# DELETE PARTICIPANT
# =========================================================

@app.route("/delete_participant/<int:id>")
def delete_participant_page(id):

    if "user" not in session:
        return redirect("/login")

    delete_participant(id)

    return redirect("/participants")


# =========================================================
# EDIT PARTICIPANT
# =========================================================

@app.route("/edit_participant/<int:id>", methods=["GET", "POST"])
def edit_participant_page(id):

    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":

        name = request.form["name"]

        email = request.form["email"]

        startdate = request.form["startdate"]

        update_participant(
            id,
            name,
            email,
            startdate
        )

        return redirect("/participants")

    participant = get_participant_by_id(id)

    return render_template(
        "edit_participant.html",
        participant=participant
    )


# =========================================================
# ADD POINT RULE
# =========================================================

@app.route("/add_point_rule", methods=["GET", "POST"])
def add_rule():

    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":

        activity_name = request.form["activity_name"]

        description = request.form["description"]

        points = request.form["points"]

        max_per_day = request.form["max_per_day"]

        active = request.form["active"]

        if active == "Yes":

            active = True

        else:

            active = False

        add_point_rule(
            activity_name,
            description,
            points,
            max_per_day,
            active
        )

        return redirect("/point_rules")

    return render_template("add_point_rule.html")


# =========================================================
# VIEW POINT RULES
# =========================================================

@app.route("/point_rules")
def point_rules_page():

    if "user" not in session:
        return redirect("/login")

    rules = get_point_rules()

    return render_template(
        "point_rules.html",
        rules=rules
    )


# =========================================================
# ADD TRANSACTION
# =========================================================

@app.route("/add_transaction", methods=["GET", "POST"])
def transaction():

    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":

        participant_id = int(
            request.form["participant_id"]
        )

        rule_id = int(
            request.form["rule_id"]
        )

        activity_date = request.form["activity_date"]

        points = int(
            request.form["points"]
        )

        notes = request.form["notes"]

        add_transaction(
            participant_id,
            rule_id,
            activity_date,
            points,
            notes
        )

        return redirect("/transactions")

    return render_template("add_transaction.html")


# =========================================================
# VIEW TRANSACTIONS
# =========================================================

@app.route("/transactions")
def transactions():

    if "user" not in session:
        return redirect("/login")

    records = get_transactions()

    return render_template(
        "transaction.html",
        transactions=records
    )


# =========================================================
# HISTORY
# =========================================================

@app.route("/history")
def history_page():

    if "user" not in session:
        return redirect("/login")

    records = get_history()

    return render_template(
        "history.html",
        records=records
    )


# =========================================================
# ADD GOAL
# =========================================================

@app.route("/add_goal", methods=["GET", "POST"])
def add_goal_page():

    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":

        participant_id = request.form["participant_id"]

        start_date = request.form["start_date"]

        end_date = request.form["end_date"]

        target_points = request.form["target_points"]

        add_goal(
            participant_id,
            start_date,
            end_date,
            target_points
        )

        return redirect("/goals")

    return render_template("add_goal.html")


# =========================================================
# VIEW GOALS
# =========================================================

@app.route("/goals")
def goals_page():

    if "user" not in session:
        return redirect("/login")

    goals = get_goals()

    return render_template(
        "goal.html",
        goals=goals
    )


# =========================================================
# ADD GOAL PROGRESS
# =========================================================

@app.route("/add_goal_progress", methods=["GET", "POST"])
def add_goal_progress_page():

    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":

        goal_id = request.form["goal_id"]

        participant_id = request.form["participant_id"]

        current_points = request.form["current_points"]

        completed = request.form["completed"]

        if completed == "Yes":

            completed = True

        else:

            completed = False

        add_goal_progress(
            goal_id,
            participant_id,
            current_points,
            completed
        )

        return redirect("/goal_progress")

    return render_template(
        "add_goal_progress.html"
    )


# =========================================================
# VIEW GOAL PROGRESS
# =========================================================

@app.route("/goal_progress")
def goal_progress_page():

    if "user" not in session:
        return redirect("/login")

    records = get_goal_progress()

    return render_template(
        "goal_progress.html",
        records=records
    )


# =========================================================
# LEADERBOARD
# =========================================================

@app.route("/leaderboard")
def leaderboard_page():

    if "user" not in session:
        return redirect("/login")

    records = get_leaderboard()

    return render_template(
        "leaderboard.html",
        records=records
    )


# =========================================================
# DOWNLOAD STUDENT PROGRESS REPORT
# =========================================================

@app.route("/download_report/<int:participant_id>")
def download_report(participant_id):

    if "user" not in session:
        return redirect("/login")

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)


    # -----------------------------------------------------
    # PARTICIPANT
    # -----------------------------------------------------

    cursor.execute(
        """
        SELECT *
        FROM Participants
        WHERE ParticipantID = %s
        """,
        (participant_id,)
    )

    participant = cursor.fetchone()


    if not participant:

        conn.close()

        return "Participant not found"


    # -----------------------------------------------------
    # TOTAL POINTS
    # -----------------------------------------------------

    cursor.execute(
        """
        SELECT COALESCE(SUM(Points), 0) AS TotalPoints
        FROM PointTransactions
        WHERE ParticipantID = %s
        """,
        (participant_id,)
    )

    points_result = cursor.fetchone()

    total_points = points_result["TotalPoints"]


    # -----------------------------------------------------
    # GOALS
    # -----------------------------------------------------

    cursor.execute(
        """
        SELECT *
        FROM Goals
        WHERE ParticipantID = %s
        ORDER BY StartDate DESC
        """,
        (participant_id,)
    )

    goals = cursor.fetchall()


    # -----------------------------------------------------
    # GOAL PROGRESS
    # -----------------------------------------------------

    cursor.execute(
        """
        SELECT *
        FROM GoalProgress
        WHERE ParticipantID = %s
        ORDER BY ProgressID DESC
        """,
        (participant_id,)
    )

    progress = cursor.fetchall()


    # -----------------------------------------------------
    # TRANSACTIONS
    # -----------------------------------------------------

    cursor.execute(
        """
        SELECT *
        FROM PointTransactions
        WHERE ParticipantID = %s
        ORDER BY ActivityDate DESC
        """,
        (participant_id,)
    )

    transactions = cursor.fetchall()


    conn.close()


    # =====================================================
    # CREATE PDF
    # =====================================================

    filename = f"student_report_{participant_id}.pdf"

    pdf = canvas.Canvas(
        filename,
        pagesize=A4
    )

    width, height = A4


    # =====================================================
    # BACKGROUND
    # =====================================================

    pdf.setFillColorRGB(
        0.96,
        0.98,
        1.0
    )

    pdf.rect(
        0,
        0,
        width,
        height,
        fill=1,
        stroke=0
    )


    # =====================================================
    # HEADER
    # =====================================================

    pdf.setFillColorRGB(
        0.0,
        0.2,
        0.4
    )

    pdf.rect(
        0,
        height - 100,
        width,
        100,
        fill=1,
        stroke=0
    )


    pdf.setFillColorRGB(
        1,
        1,
        1
    )

    pdf.setFont(
        "Helvetica-Bold",
        20
    )

    pdf.drawCentredString(
        width / 2,
        height - 45,
        "STUDENT REWARD SYSTEM"
    )


    pdf.setFont(
        "Helvetica",
        13
    )

    pdf.drawCentredString(
        width / 2,
        height - 70,
        "Student Progress Report"
    )


    y = height - 130


    # =====================================================
    # STUDENT INFORMATION
    # =====================================================

    pdf.setFillColorRGB(
        1,
        1,
        1
    )

    pdf.roundRect(
        40,
        y - 145,
        width - 80,
        145,
        10,
        fill=1,
        stroke=0
    )


    pdf.setFillColorRGB(
        0.0,
        0.2,
        0.4
    )

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        60,
        y - 25,
        "Student Information"
    )


    pdf.setFillColorRGB(
        0.15,
        0.15,
        0.15
    )

    pdf.setFont(
        "Helvetica",
        11
    )


    pdf.drawString(
        60,
        y - 50,
        f"Participant ID: {participant['ParticipantID']}"
    )


    pdf.drawString(
        60,
        y - 72,
        f"Name: {participant['Name']}"
    )


    pdf.drawString(
        60,
        y - 94,
        f"Email: {participant['Email']}"
    )


    pdf.drawString(
        60,
        y - 116,
        f"Start Date: {participant['StartDate']}"
    )


    status = (
        "Active"
        if participant["Active"] == 1
        else "Inactive"
    )


    pdf.drawString(
        300,
        y - 50,
        f"Status: {status}"
    )


    # =====================================================
    # POINT SUMMARY
    # =====================================================

    y -= 180


    pdf.setFillColorRGB(
        0.0,
        0.2,
        0.4
    )


    pdf.roundRect(
        40,
        y - 80,
        width - 80,
        80,
        10,
        fill=1,
        stroke=0
    )


    pdf.setFillColorRGB(
        1,
        1,
        1
    )


    pdf.setFont(
        "Helvetica-Bold",
        14
    )


    pdf.drawString(
        60,
        y - 30,
        "POINTS SUMMARY"
    )


    pdf.setFont(
        "Helvetica-Bold",
        20
    )


    pdf.drawString(
        60,
        y - 60,
        f"Total Points Earned: {total_points}"
    )


    # =====================================================
    # GOALS
    # =====================================================

    y -= 115


    pdf.setFillColorRGB(
        0.0,
        0.2,
        0.4
    )


    pdf.setFont(
        "Helvetica-Bold",
        14
    )


    pdf.drawString(
        50,
        y,
        "Goals"
    )


    y -= 25


    pdf.setFillColorRGB(
        0.15,
        0.15,
        0.15
    )


    pdf.setFont(
        "Helvetica",
        10
    )


    if goals:

        for goal in goals:

            pdf.drawString(
                55,
                y,
                f"Goal ID: {goal['GoalID']}"
            )

            y -= 18

            pdf.drawString(
                70,
                y,
                f"Start Date: {goal['StartDate']}    "
                f"End Date: {goal['EndDate']}"
            )

            y -= 18

            pdf.drawString(
                70,
                y,
                f"Target Points: {goal['TargetPoints']}"
            )

            y -= 25


    else:

        pdf.drawString(
            55,
            y,
            "No goals recorded."
        )

        y -= 25


    # =====================================================
    # GOAL PROGRESS
    # =====================================================

    y -= 10


    pdf.setFillColorRGB(
        0.0,
        0.2,
        0.4
    )


    pdf.setFont(
        "Helvetica-Bold",
        14
    )


    pdf.drawString(
        50,
        y,
        "Goal Progress"
    )


    y -= 25


    pdf.setFillColorRGB(
        0.15,
        0.15,
        0.15
    )


    pdf.setFont(
        "Helvetica",
        10
    )


    if progress:

        for row in progress:

            progress_status = (
                "Completed"
                if row["Completed"] == 1
                else "In Progress"
            )


            pdf.drawString(
                55,
                y,
                f"Goal ID: {row['GoalID']}    "
                f"Current Points: {row['CurrentPoints']}    "
                f"Status: {progress_status}"
            )

            y -= 20


    else:

        pdf.drawString(
            55,
            y,
            "No goal progress recorded."
        )

        y -= 25


    # =====================================================
    # TRANSACTION HISTORY
    # =====================================================

    y -= 10


    pdf.setFillColorRGB(
        0.0,
        0.2,
        0.4
    )


    pdf.setFont(
        "Helvetica-Bold",
        14
    )


    pdf.drawString(
        50,
        y,
        "Transaction History"
    )


    y -= 25


    pdf.setFillColorRGB(
        0.15,
        0.15,
        0.15
    )


    pdf.setFont(
        "Helvetica",
        9
    )


    if transactions:

        for transaction in transactions:

            pdf.drawString(
                55,
                y,
                f"Transaction ID: "
                f"{transaction['TransactionID']}    "
                f"Date: {transaction['ActivityDate']}    "
                f"Points: {transaction['Points']}"
            )

            y -= 18


            if transaction["Notes"]:

                pdf.drawString(
                    70,
                    y,
                    f"Notes: {transaction['Notes']}"
                )

                y -= 18


    else:

        pdf.drawString(
            55,
            y,
            "No transactions recorded."
        )

        y -= 25


    # =====================================================
    # FOOTER
    # =====================================================

    pdf.setFillColorRGB(
        0.0,
        0.2,
        0.4
    )

    pdf.rect(
        0,
        0,
        width,
        35,
        fill=1,
        stroke=0
    )


    pdf.setFillColorRGB(
        1,
        1,
        1
    )


    pdf.setFont(
        "Helvetica",
        8
    )


    pdf.drawCentredString(
        width / 2,
        15,
        f"Generated on "
        f"{datetime.now().strftime('%d %B %Y %H:%M')}"
    )


    # SAVE PDF

    pdf.save()


    return send_file(
        filename,
        as_attachment=True,
        download_name=filename
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)