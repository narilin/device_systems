import sqlite3

conn = sqlite3.connect('device_systems.db')
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cur.fetchall())