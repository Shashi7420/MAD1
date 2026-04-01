from database import get_db

# -------------------------
# USER FUNCTIONS
# -------------------------

def create_user(username, password, role):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username,password,role) VALUES (?,?,?)", (username,password,role))
    conn.commit()
    conn.close()


def get_user(username, password):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username,password))
    user = cur.fetchone()
    conn.close()
    return user

# -------------------------
# COMPANY FUNCTIONS
# -------------------------

def create_company(user_id, name):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO companies (user_id,name) VALUES (?,?)", (user_id,name))
    conn.commit()
    conn.close()


def get_all_companies():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM companies")
    data = cur.fetchall()
    conn.close()
    return data


def approve_company(company_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE companies SET approved=1 WHERE id=?", (company_id,))
    conn.commit()
    conn.close()

# -------------------------
# DRIVE FUNCTIONS
# -------------------------

def create_drive(company_id, title, desc):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO drives (company_id,title,description) VALUES (?,?,?)", (company_id,title,desc))
    conn.commit()
    conn.close()


def get_all_drives():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM drives")
    data = cur.fetchall()
    conn.close()
    return data


def approve_drive(drive_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE drives SET approved=1 WHERE id=?", (drive_id,))
    conn.commit()
    conn.close()

# -------------------------
# APPLICATION FUNCTIONS
# -------------------------

def apply_drive(student_id, drive_id):
    conn = get_db()
    cur = conn.cursor()

    # prevent duplicate
    cur.execute("SELECT * FROM applications WHERE student_id=? AND drive_id=?", (student_id,drive_id))
    if cur.fetchone():
        conn.close()
        return "Already Applied"

    cur.execute("INSERT INTO applications (student_id,drive_id) VALUES (?,?)", (student_id,drive_id))
    conn.commit()
    conn.close()
    return "Applied"


def get_applications_by_drive(drive_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM applications WHERE drive_id=?", (drive_id,))
    data = cur.fetchall()
    conn.close()
    return data

def update_application_status(app_id, status):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE applications SET status=? WHERE id=?", (status,app_id))
    conn.commit()
    conn.close()
