import unittest
from unittest.mock import patch

import participants
from tests_support import FakeConnection


class ParticipantServiceTests(unittest.TestCase):
    def test_add_participant_uses_current_schema_and_commits(self):
        connection = FakeConnection()
        with patch("participants.get_connection", return_value=connection):
            participants.add_participant(
                "Test Student", "test@example.com", "2026-11-03"
            )

        query, params = connection.fake_cursor.executed[0]
        self.assertIn("(Name, Email, StartDate, Active)", query)
        self.assertEqual(
            params, ("Test Student", "test@example.com", "2026-11-03", True)
        )
        self.assertTrue(connection.committed)
        self.assertTrue(connection.fake_cursor.closed)
        self.assertTrue(connection.closed)

    def test_get_participant_uses_participant_id_column(self):
        participant = (1, "Test Student", "test@example.com", "2026-11-03", 1)
        connection = FakeConnection([participant])
        with patch("participants.get_connection", return_value=connection):
            result = participants.get_participant_by_id(1)

        query, params = connection.fake_cursor.executed[0]
        self.assertIn("WHERE ParticipantID = %s", query)
        self.assertEqual(params, (1,))
        self.assertEqual(result, participant)

    def test_update_and_delete_use_current_participant_key(self):
        connection = FakeConnection()
        with patch("participants.get_connection", return_value=connection):
            participants.update_participant(
                7, "Updated", "updated@example.com", "2026-11-03"
            )
            participants.delete_participant(7)

        update_query, update_params = connection.fake_cursor.executed[0]
        delete_query, delete_params = connection.fake_cursor.executed[1]
        self.assertIn("WHERE ParticipantID = %s", update_query)
        self.assertEqual(update_params[-1], 7)
        self.assertIn("WHERE ParticipantID = %s", delete_query)
        self.assertEqual(delete_params, (7,))
        self.assertTrue(connection.committed)


if __name__ == "__main__":
    unittest.main()
