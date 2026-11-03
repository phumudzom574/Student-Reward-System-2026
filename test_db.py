import unittest
from unittest.mock import patch

import database


class DefaultDatabaseConfigurationTests(unittest.TestCase):
    def test_connection_uses_documented_local_defaults(self):
        with patch.dict("os.environ", {}, clear=True), patch(
            "database.mysql.connector.connect", return_value=object()
        ) as connect:
            database.get_connection()

        connect.assert_called_once_with(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database="student_reward_system",
        )


if __name__ == "__main__":
    unittest.main()
