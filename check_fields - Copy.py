from database import get_connection

conn = get_connection()
cursor = conn.cursor()

for column in cursor.columns(table='pointrules'):
    print(column.column_name)

conn.close()