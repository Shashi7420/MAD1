from flask import Blueprint, render_template, request, redirect, session
from database import get_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (u,p))
        user = cur.fetchone()

        if user:
            session['user_id'] = user[0]
            session['role'] = user[3]
            if user[3] == 'admin':
                return redirect('/admin')
            elif user[3] == 'company':
                return redirect('/company')
            else:
                return redirect('/student')

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        role = request.form['role']

        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username,password,role) VALUES (?,?,?)", (u,p,role))
        user_id = cur.lastrowid

        if role == 'company':
            cur.execute("INSERT INTO companies (user_id,name) VALUES (?,?)", (user_id,u))

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('register.html')