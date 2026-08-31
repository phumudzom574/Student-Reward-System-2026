from database import get_connection

conn = get_connection()
cursor = conn.cursor()

for column in cursor.columns(table='PointRules'):
    print(column.column_name)

conn.close()