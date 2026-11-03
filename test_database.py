import re
import unittest
from pathlib import Path


class CurrentSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sql_path = Path(__file__).with_name("student_reward_system.sql")
        cls.schema = sql_path.read_text(encoding="utf-8-sig")
        cls.tables = {}
        for match in re.finditer(
            r"CREATE TABLE `([^`]+)`\s*\((.*?)\)\s*ENGINE=",
            cls.schema,
            re.DOTALL,
        ):
            table, body = match.groups()
            cls.tables[table] = set(
                re.findall(r"^\s*`([^`]+)`", body, re.MULTILINE)
            )

    def test_award_table_uses_current_column_names(self):
        self.assertTrue(
            {
                "TransactionID",
                "ParticipantID",
                "RuleID",
                "ActivityDate",
                "Points",
                "Notes",
                "CreatedAt",
            }.issubset(self.tables["pointtransactions"])
        )

    def test_rules_and_goals_have_limit_and_target_fields(self):
        self.assertIn("MaxPerDay", self.tables["pointrules"])
        self.assertIn("TargetPoints", self.tables["goals"])

    def test_goal_progress_links_goal_and_participant(self):
        self.assertTrue(
            {
                "GoalID",
                "ParticipantID",
                "CurrentPoints",
                "Completed",
            }.issubset(self.tables["goalprogress"])
        )


if __name__ == "__main__":
    unittest.main()
