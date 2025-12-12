# import sqlite3

# # Connect to SQLite database (it will create the file if it doesn’t exist)
# conn = sqlite3.connect("mediqa.db")
# c = conn.cursor()

# # Create users table
# c.execute('''
# CREATE TABLE IF NOT EXISTS users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     first_name TEXT,
#     last_name TEXT,
#     email TEXT UNIQUE,
#     password TEXT
# )
# ''')

# # Create chats table
# c.execute('''
# CREATE TABLE IF NOT EXISTS chats (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     user_id INTEGER,
#     title TEXT,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY(user_id) REFERENCES users(id)
# )
# ''')

# # Create messages table
# c.execute('''
# CREATE TABLE IF NOT EXISTS messages (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     chat_id INTEGER,
#     user_id INTEGER,
#     sender TEXT,
#     message TEXT,
#     timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY(chat_id) REFERENCES chats(id),
#     FOREIGN KEY(user_id) REFERENCES users(id)
# )
# ''')

# conn.commit()
# conn.close()

# print("✅ Database and tables created successfully!")







import sqlite3

conn = sqlite3.connect("mediqa.db")
c = conn.cursor()

# Users table (as before)
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    email TEXT UNIQUE,
    password TEXT
)
''')

# Updated Chats table (with user_email)
c.execute('''
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT,
    title TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Updated Messages table (with user_email)
c.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER,
    user_email TEXT,
    question TEXT,
    answer TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()

print("✅ Updated database schema applied successfully!")
