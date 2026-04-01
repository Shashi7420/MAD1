from flask import Blueprint, render_template, request, session, redirect
from models import create_drive, get_drives_by_company, delete_drive

company_bp = Blueprint('company', __name__)

# -------------------------
# COMPANY DASHBOARD
# -------------------------
@company_bp.route('/company', methods=['GET', 'POST'])
def company_dashboard():

    # session check
    if 'user_id' not in session:
        return redirect('/')

    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

        # create drive using model
        create_drive(session['user_id'], title, desc)

    # get only this company's drives
    drives = get_drives_by_company(session['user_id'])

    return render_template('company.html', drives=drives)


# -------------------------
# DELETE DRIVE
# -------------------------
@company_bp.route('/delete_drive/<int:id>')
def delete_drive_route(id):
    delete_drive(id)
    return redirect('/company')