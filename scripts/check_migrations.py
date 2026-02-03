import sqlite3

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
cur.execute("SELECT app, name, applied FROM django_migrations WHERE app='vie_estudiantine_una'")
rows = cur.fetchall()
for r in rows:
    print(r)
conn.close()
