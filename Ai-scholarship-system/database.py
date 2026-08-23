import sqlite3

# Connect to Database
conn = sqlite3.connect("database/scholarship.db")

# Cursor
cursor = conn.cursor()

# Create Student Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT,
    email TEXT UNIQUE,
    password TEXT,
    department TEXT,
    year TEXT,
    cgpa REAL,
    income INTEGER,
    community TEXT
)
""")

# Save Changes
conn.commit()

# Close Database
conn.close()

print("Database Created Successfully!")