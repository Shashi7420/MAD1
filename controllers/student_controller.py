from flask import Blueprint, render_template, request, session
from database import get_db

student_bp = Blueprint('student', __name__)

@student_bp.route('/student', methods=['GET','POST'])
def student_dashboard():
    conn = get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        drive_id = request.form['drive_id']

        cur.execute("INSERT INTO applications (student_id, drive_id) VALUES (?,?)", (session['user_id'], drive_id))
        conn.commit()

    cur.execute("SELECT * FROM drives WHERE approved=1")
    drives = cur.fetchall()

    return render_template('student.html', drives=drives)