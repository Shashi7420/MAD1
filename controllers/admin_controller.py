from flask import Blueprint, render_template, redirect
from models import get_all_companies, get_all_drives, approve_company, approve_drive

admin_bp = Blueprint('admin', __name__)

# -------------------------
# ADMIN DASHBOARD
# -------------------------
@admin_bp.route('/admin')
def admin_dashboard():
    companies = get_all_companies()
    drives = get_all_drives()

    return render_template('admin.html', companies=companies, drives=drives)


# -------------------------
# APPROVE COMPANY
# -------------------------
@admin_bp.route('/approve_company/<int:id>')
def approve_company_route(id):
    approve_company(id)
    return redirect('/admin')


# -------------------------
# APPROVE DRIVE
# -------------------------
@admin_bp.route('/approve_drive/<int:id>')
def approve_drive_route(id):
    approve_drive(id)
    return redirect('/admin')