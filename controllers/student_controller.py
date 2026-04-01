from flask import Blueprint, render_template, request, session, redirect
from models import apply_drive
from database import get_db

student_bp = Blueprint('student', __name__)

# -------------------------
# STUDENT DASHBOARD
# -------------------------
@student_bp.route('/student')
def student_dashboard():
    conn = get_db()
    cur = conn.cursor()

    # show only approved drives
    cur.execute("SELECT * FROM drives WHERE approved=1")
    drives = cur.fetchall()

    return render_template('student.html', drives=drives)


# -------------------------
# APPLY FOR DRIVE
# -------------------------
@student_bp.route('/apply', methods=['POST'])
def apply():
    if 'user_id' not in session:
        return redirect('/')

    drive_id = request.form['drive_id']
    student_id = session['user_id']

    # use model function (prevents duplicate)
    result = apply_drive(student_id, drive_id)

    return redirect('/student')