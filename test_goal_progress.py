import unittest
from unittest.mock import patch

from app import app as flask_app
import goal_progress
from tests_support import FakeConnection


class GoalProgressTests(unittest.TestCase):
    def test_manual_progress_is_saved_with_the_entered_values(self):
        connection = FakeConnection()
        with patch(
            "goal_progress.get_connection", return_value=connection
        ):
            goal_progress.add_goal_progress("7", "4", "72", True)

        query, params = connection.fake_cursor.executed[0]
        self.assertIn(
            "(GoalID, ParticipantID, CurrentPoints, Completed)", query
        )
        self.assertEqual(params, ("7", "4", "72", True))
        self.assertTrue(connection.committed)

    def test_manual_progress_form_submits_values_and_completion(self):
        client = flask_app.test_client()
        with client.session_transaction() as state:
            state["user"] = "tester"

        with patch("app.add_goal_progress") as add_progress:
            response = client.post(
                "/add_goal_progress",
                data={
                    "goal_id": "7",
                    "participant_id": "4",
                    "current_points": "72",
                    "completed": "Yes",
                },
            )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/goal_progress")
        add_progress.assert_called_once_with("7", "4", "72", True)

    def test_progress_page_displays_named_database_fields(self):
        client = flask_app.test_client()
        with client.session_transaction() as state:
            state["user"] = "tester"

        progress = [{
            "ProgressID": 9,
            "GoalID": 7,
            "ParticipantID": 4,
            "CurrentPoints": 72,
            "Completed": 1,
        }]
        with patch("app.get_goal_progress", return_value=progress):
            response = client.get("/goal_progress")

        self.assertEqual(response.status_code, 200)
        for value in (b">9<", b">7<", b">4<", b">72<", b"Completed"):
            self.assertIn(value, response.data)


if __name__ == "__main__":
    unittest.main()
