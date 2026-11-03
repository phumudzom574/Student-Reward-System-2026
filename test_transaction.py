import unittest
from unittest.mock import patch

import point_transactions
from tests_support import FakeConnection


def valid_award_responses(
    *,
    max_per_day=2,
    duplicate_count=0,
    awards_today=0,
    points=50,
):
    return [
        {"ParticipantID": 4},
        {
            "RuleID": 3,
            "Points": points,
            "MaxPerDay": max_per_day,
            "Active": 1,
        },
        {"DuplicateCount": duplicate_count},
        {"AwardCount": awards_today},
    ]


class AwardServiceTests(unittest.TestCase):
    def add_award(self, connection, notes="Attended workshop"):
        with patch(
            "point_transactions.get_connection", return_value=connection
        ):
            point_transactions.add_transaction(
                "4", "3", "2026-11-03", notes
            )

    def test_p2_duplicate_award_is_rejected(self):
        connection = FakeConnection(
            valid_award_responses(duplicate_count=1)
        )
        with patch(
            "point_transactions.get_connection", return_value=connection
        ):
            with self.assertRaisesRegex(ValueError, "already been recorded"):
                point_transactions.add_transaction(
                    "4", "3", "2026-11-03", "Attended workshop"
                )

        self.assertTrue(connection.rolled_back)
        self.assertFalse(connection.committed)
        self.assertFalse(any(
            query.lstrip().startswith("INSERT")
            for query, _ in connection.fake_cursor.executed
        ))

    def test_award_uses_points_configured_on_rule(self):
        connection = FakeConnection(
            valid_award_responses(points=50)
        )
        self.add_award(connection)

        insert_query, insert_params = connection.fake_cursor.executed[-1]
        self.assertIn(
            "(ParticipantID, RuleID, ActivityDate, Points, Notes)",
            insert_query,
        )
        self.assertEqual(
            insert_params,
            (4, 3, "2026-11-03", 50, "Attended workshop"),
        )
        self.assertTrue(connection.committed)

    def test_daily_limit_is_enforced_for_distinct_awards(self):
        connection = FakeConnection(
            valid_award_responses(awards_today=2, max_per_day=2)
        )
        with patch(
            "point_transactions.get_connection", return_value=connection
        ):
            with self.assertRaisesRegex(ValueError, "daily limit"):
                point_transactions.add_transaction(
                    "4", "3", "2026-11-03", "Another workshop"
                )

        self.assertTrue(connection.rolled_back)
        self.assertFalse(connection.committed)

    def test_blank_or_nonpositive_daily_limit_is_rejected(self):
        for max_per_day in (None, 0, -1):
            with self.subTest(max_per_day=max_per_day):
                connection = FakeConnection(
                    valid_award_responses(max_per_day=max_per_day)
                )
                with patch(
                    "point_transactions.get_connection",
                    return_value=connection,
                ):
                    with self.assertRaisesRegex(
                        ValueError, "no valid daily limit configured"
                    ):
                        point_transactions.add_transaction(
                            "4", "3", "2026-11-03", "Attended workshop"
                        )

                self.assertTrue(connection.rolled_back)
                self.assertFalse(connection.committed)

    def test_invalid_ids_and_dates_fail_before_database_access(self):
        invalid_awards = (
            ("invalid", "3", "2026-11-03"),
            ("4", "0", "2026-11-03"),
            ("4", "3", "03-11-2026"),
        )
        for participant_id, rule_id, activity_date in invalid_awards:
            with self.subTest(
                participant_id=participant_id,
                rule_id=rule_id,
                activity_date=activity_date,
            ), patch("point_transactions.get_connection") as get_connection:
                with self.assertRaises(ValueError):
                    point_transactions.add_transaction(
                        participant_id, rule_id, activity_date, ""
                    )

                get_connection.assert_not_called()


if __name__ == "__main__":
    unittest.main()
