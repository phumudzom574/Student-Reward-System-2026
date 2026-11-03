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
