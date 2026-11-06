import unittest
from unittest.mock import patch

import goals
import point_rules
import point_transactions
from app import app as flask_app


class FakeCursor:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.executed = []

    def execute(self, query, params=None):
        self.executed.append((query, params))

    def fetchone(self):
        return next(self.responses)

    def close(self):
        pass


class FakeConnection:
    def __init__(self, responses):
        self.fake_cursor = FakeCursor(responses)
        self.cursor_options = {}
        self.committed = False
        self.rolled_back = False
        self.closed = False

    def start_transaction(self):
        pass

    def cursor(self, **kwargs):
        self.cursor_options = kwargs
        return self.fake_cursor

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True

    def close(self):
        self.closed = True


class RewardValidationTests(unittest.TestCase):
    def test_duplicate_award_is_rejected(self):
        connection = FakeConnection([
            (1,),
            {"RuleID": 3, "Points": 10, "MaxPerDay": 2, "Active": 1},
            {"DuplicateCount": 1},
        ])
        with patch(
            "point_transactions.get_connection", return_value=connection
        ):
            with self.assertRaisesRegex(ValueError, "already been recorded"):
                point_transactions.add_transaction(
                    "1", "3", "2026-11-03", "Workshop"
                )

        self.assertTrue(connection.rolled_back)
        self.assertFalse(connection.committed)
        self.assertFalse(any(
            query.lstrip().startswith("INSERT")
            for query, _ in connection.fake_cursor.executed
        ))

    def test_daily_limit_rejects_another_distinct_award(self):
        connection = FakeConnection([
            (1,),
            {"RuleID": 3, "Points": 10, "MaxPerDay": 2, "Active": 1},
            {"DuplicateCount": 0},
            {"AwardCount": 2},
        ])
        with patch(
            "point_transactions.get_connection", return_value=connection
        ):
            with self.assertRaisesRegex(ValueError, "daily limit"):
                point_transactions.add_transaction(
                    "1", "3", "2026-11-03", "Second workshop"
                )

        self.assertTrue(connection.rolled_back)
        self.assertFalse(connection.committed)

    def test_missing_or_nonpositive_daily_limit_is_rejected_clearly(self):
        for max_per_day in (None, 0, -1):
            with self.subTest(max_per_day=max_per_day):
                connection = FakeConnection([
                    (1,),
                    {
                        "RuleID": 3,
                        "Points": 10,
                        "MaxPerDay": max_per_day,
                        "Active": 1,
                    },
                ])
                with patch(
                    "point_transactions.get_connection",
                    return_value=connection
                ):
                    with self.assertRaisesRegex(
                        ValueError,
                        "no valid daily limit configured"
                    ):
                        point_transactions.add_transaction(
                            "1", "3", "2026-11-03", "Workshop"
                        )

                self.assertTrue(connection.rolled_back)
                self.assertFalse(connection.committed)

    def test_unique_award_is_allowed_within_daily_limit(self):
        connection = FakeConnection([
            (1,),
            {"RuleID": 3, "Points": 10, "MaxPerDay": 2, "Active": 1},
            {"DuplicateCount": 0},
            {"AwardCount": 1},
        ])
        with patch(
            "point_transactions.get_connection", return_value=connection
        ):
            point_transactions.add_transaction(
                "1", "3", "2026-11-03", "Second workshop"
            )

        self.assertTrue(connection.committed)
        self.assertTrue(any(
            query.lstrip().startswith("INSERT")
            for query, _ in connection.fake_cursor.executed
        ))

    def test_invalid_award_input_fails_before_database_access(self):
        with patch("point_transactions.get_connection") as get_connection:
            with self.assertRaisesRegex(ValueError, "positive whole number"):
                point_transactions.add_transaction(
                    "invalid", "3", "2026-11-03", ""
                )

        get_connection.assert_not_called()

    def test_p9_duplicate_goal_is_rejected(self):
        connection = FakeConnection([(1,), (1,)])
        with patch("goals.get_connection", return_value=connection):
            with self.assertRaisesRegex(ValueError, "already been created"):
                goals.add_goal(
                    "1", "2026-11-01", "2026-11-30", "100"
                )

        self.assertTrue(connection.rolled_back)
        self.assertFalse(connection.committed)

    def test_goal_with_end_before_start_is_rejected_before_database_access(self):
        with patch("goals.get_connection") as get_connection:
            with self.assertRaisesRegex(ValueError, "on or after"):
                goals.add_goal(
                    "1", "2026-11-30", "2026-11-01", "100"
                )

        get_connection.assert_not_called()

    def test_invalid_goal_ids_dates_and_targets_fail_before_database_access(self):
        invalid_goals = (
            ("0", "2026-11-01", "2026-11-30", "100"),
            ("1", "invalid-date", "2026-11-30", "100"),
            ("1", "2026-11-01", "2026-11-30", "0"),
        )
        for participant_id, start_date, end_date, target_points in invalid_goals:
            with self.subTest(
                participant_id=participant_id,
                start_date=start_date,
                target_points=target_points,
            ), patch("goals.get_connection") as get_connection:
                with self.assertRaises(ValueError):
                    goals.add_goal(
                        participant_id, start_date, end_date, target_points
                    )

                get_connection.assert_not_called()

    def test_rule_daily_limit_must_be_a_positive_integer(self):
        with patch("point_rules.get_connection") as get_connection:
            with self.assertRaisesRegex(ValueError, "Daily limit"):
                point_rules.add_point_rule(
                    "Workshop", "Attendance", "10", "0", True
                )

        get_connection.assert_not_called()

    def test_rule_name_description_and_points_are_validated(self):
        invalid_rules = (
            ("", "Attendance", "10", "1"),
            ("Workshop", " ", "10", "1"),
            ("Workshop", "Attendance", "0", "1"),
        )
        for name, description, points, max_per_day in invalid_rules:
            with self.subTest(name=name, points=points), patch(
                "point_rules.get_connection"
            ) as get_connection:
                with self.assertRaises(ValueError):
                    point_rules.add_point_rule(
                        name, description, points, max_per_day, True
                    )

                get_connection.assert_not_called()

    def test_duplicate_rule_name_is_rejected_case_and_whitespace_insensitively(
        self
    ):
        connection = FakeConnection([(1,)])
        with patch("point_rules.get_connection", return_value=connection):
            with self.assertRaisesRegex(ValueError, "already exists"):
                point_rules.add_point_rule(
                    "  WORKSHOP  ", "Different description", "10", "1", True
                )

        query, params = connection.fake_cursor.executed[0]
        self.assertIn("LOWER(TRIM(ActivityName))", query)
        self.assertNotIn("Description", query)
        self.assertEqual(params, ("WORKSHOP",))
        self.assertTrue(connection.rolled_back)
        self.assertFalse(connection.committed)
        self.assertFalse(any(
            statement.lstrip().startswith("INSERT")
            for statement, _ in connection.fake_cursor.executed
        ))

    def test_new_rule_is_inserted_when_no_duplicate_exists(self):
        connection = FakeConnection([(0,)])
        with patch("point_rules.get_connection", return_value=connection):
            point_rules.add_point_rule(
                " Workshop ", " Attendance ", "10", "1", True
            )

        self.assertTrue(connection.committed)
        insert_query, insert_params = connection.fake_cursor.executed[1]
        self.assertTrue(insert_query.lstrip().startswith("INSERT"))
        self.assertEqual(
            insert_params, ("Workshop", "Attendance", 10, 1, True)
        )

    def test_award_validation_error_is_shown_on_form(self):
        client = flask_app.test_client()
        with client.session_transaction() as state:
            state["user"] = "tester"

        with patch(
            "app.add_transaction",
            side_effect=ValueError("The daily limit has been reached.")
        ), patch("app.get_active_point_rules", return_value=[]):
            response = client.post(
                "/add_transaction",
                data={
                    "participant_id": "1",
                    "rule_id": "3",
                    "activity_date": "2026-11-03",
                    "notes": "",
                },
            )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"The daily limit has been reached.", response.data)


if __name__ == "__main__":
    unittest.main()
