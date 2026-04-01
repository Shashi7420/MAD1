import sqlite3

DB_NAME = "placement.db"

def get_db():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_db()
    cur = conn.cursor()

    # Users
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )
    """)

    # Companies
    cur.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        approved INTEGER DEFAULT 0
    )
    """)

    # Drives
    cur.execute("""
    CREATE TABLE IF NOT EXISTS drives (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER,
        title TEXT,
        description TEXT,
        approved INTEGER DEFAULT 0
    )
    """)

    # Applications
    cur.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        drive_id INTEGER,
        status TEXT DEFAULT 'Applied'
    )
    """)

    # Create admin
    cur.execute("SELECT * FROM users WHERE role='admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin', 'admin')")

    conn.commit()
    conn.close()


