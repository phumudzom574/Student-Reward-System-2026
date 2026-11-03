import unittest
from unittest.mock import patch

import database


class DatabaseConnectionTests(unittest.TestCase):
    def test_connection_uses_current_environment_configuration(self):
        config = {
            "DB_HOST": "db.example.test",
            "DB_PORT": "3307",
            "DB_USER": "reward_test",
            "DB_PASSWORD": "unit-test-password",
            "DB_NAME": "student_reward_test",
        }
        with patch.dict("os.environ", config, clear=True), patch(
            "database.mysql.connector.connect", return_value=object()
        ) as connect:
            result = database.get_connection()

        self.assertIsNotNone(result)
        connect.assert_called_once_with(
            host="db.example.test",
            port=3307,
            user="reward_test",
            password="unit-test-password",
            database="student_reward_test",
        )


if __name__ == "__main__":
    unittest.main()
