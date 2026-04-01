from flask import Blueprint, render_template, request, session
from database import get_db

company_bp = Blueprint('company', __name__)

@company_bp.route('/company', methods=['GET','POST'])
def company_dashboard():
    conn = get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

        cur.execute("SELECT id FROM companies WHERE user_id=?", (session['user_id'],))
        company_id = cur.fetchone()[0]

        cur.execute("INSERT INTO drives (company_id,title,description) VALUES (?,?,?)", (company_id,title,desc))
        conn.commit()

    cur.execute("SELECT * FROM drives")
    drives = cur.fetchall()

    return render_template('company.html', drives=drives)