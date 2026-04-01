from flask import Blueprint, render_template
from database import get_db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin_dashboard():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM companies")
    companies = cur.fetchall()

    cur.execute("SELECT * FROM drives")
    drives = cur.fetchall()

    return render_template('admin.html', companies=companies, drives=drives)
