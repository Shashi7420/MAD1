from flask import Blueprint, render_template, request, redirect, session, flash
from models import create_user, get_user, create_company

auth_bp = Blueprint('auth', __name__)

# -------------------------
# LOGIN
# -------------------------
@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        user = get_user(u, p)

        if user:
            session['user_id'] = user[0]
            session['role'] = user[3]

            if user[3] == 'admin':
                return redirect('/admin')
            elif user[3] == 'company':
                return redirect('/company')
            else:
                return redirect('/student')
        else:
            flash("Invalid username or password")

    return render_template('login.html')


# -------------------------
# REGISTER
# -------------------------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        role = request.form['role']

        # create user
        create_user(u, p, role)

        # if company, create company record
        if role == 'company':
            user = get_user(u, p)
            create_company(user[0], u)

        return redirect('/')

    return render_template('register.html')


# -------------------------
# LOGOUT
# -------------------------
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')