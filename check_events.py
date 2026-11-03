
from database import get_connection, initialize_database

initialize_database()

conn = get_connection()

rows = conn.execute(
    "SELECT * FROM patient_status_events ORDER BY id DESC"
).fetchall()

if rows:
    for row in rows:
        print(dict(row))
else:
    print("No patient status events found.")

conn.close()
