<<<<<<< HEAD
from db import get_connection

try:
    conn = get_connection()
    print("MySQL Connected Successfully!")
    conn.close()
except Exception as e:
=======
from db import get_connection

try:
    conn = get_connection()
    print("MySQL Connected Successfully!")
    conn.close()
except Exception as e:
>>>>>>> origin/main
    print("Error:", e)