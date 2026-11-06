# Student-reward-system
Student reward system description

## Tests

Run the unit and schema checks from the project root:

```powershell
python -m unittest discover -v
```

These tests use mocked database connections or inspect the SQL schema file;
they do not create or modify records in the configured database. Live-system
test cases must be run separately and recorded with their actual results.

## Goal progress

Goal progress is recorded manually through the **Add Goal Progress** form.
The user enters the goal ID, participant ID, current points, and completion
status; the system stores and displays those values. It does not automatically
calculate progress from point transactions or determine completion from the
goal target. The manual-entry workflow is the approved approach for this
Phase 5 submission. Focused tests verify manual submission, persistence, and
display. The original automatic-progress expectations in TC-07 and TC-08 are
not marked as passed.
