<<<<<<< HEAD
from participants import add_participant, get_participants


add_participant(
    "Test Student",
    "test@example.com",
    "2026-08-17"
)

participants = get_participants()

for participant in participants:
=======
from participants import add_participant, get_participants


add_participant(
    "Test Student",
    "test@example.com",
    "2026-08-17"
)

participants = get_participants()

for participant in participants:
>>>>>>> origin/main
    print(participant)