import sqlite3

conn = sqlite3.connect("mediqa.db")
c = conn.cursor()

print("Users Table:")
for row in c.execute("SELECT * FROM users"):
    print(row)

print("\nChats Table:")
for row in c.execute("SELECT * FROM chats"):
    print(row)

print("\nMessages Table:")
for row in c.execute("SELECT * FROM messages"):
    print(row)

conn.close()
