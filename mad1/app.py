from flask import Flask,render_template,request,redirect,session
import sqlite3
from database import create_db

app = Flask(__name__)
app.secret_key = "secret"

create_db()

def get_db():
    return sqlite3.connect("placement.db")


@app.route("/")
def home():
    return render_template("login.html")


# LOGIN
@app.route("/login",methods=["POST"])
def login():

    email=request.form["email"]
    password=request.form["password"]
    role=request.form["role"]

    conn=get_db()
    cursor=conn.cursor()

    if role=="admin":

        cursor.execute("SELECT * FROM admin WHERE username=? AND password=?",(email,password))
        admin=cursor.fetchone()

        if admin:
            session["admin"]=admin[0]
            return redirect("/admin_dashboard")

    elif role=="student":

        cursor.execute("SELECT * FROM student WHERE email=? AND password=?",(email,password))
        student=cursor.fetchone()

        if student:
            session["student"]=student[0]
            return redirect("/student_dashboard")

    elif role=="company":

        cursor.execute("SELECT * FROM company WHERE email=? AND password=? AND status='Approved'",(email,password))
        company=cursor.fetchone()

        if company:
            session["company"]=company[0]
            return redirect("/company_dashboard")

    return "Invalid Login"


# STUDENT REGISTER
@app.route("/student_register")
def student_register():
    return render_template("student_register.html")


@app.route("/register_student",methods=["POST"])
def register_student():

    name=request.form["name"]
    email=request.form["email"]
    password=request.form["password"]

    conn=get_db()
    cursor=conn.cursor()

    cursor.execute("INSERT INTO student(name,email,password) VALUES(?,?,?)",(name,email,password))
    conn.commit()

    return redirect("/")


# COMPANY REGISTER
@app.route("/company_register")
def company_register():
    return render_template("company_register.html")


@app.route("/register_company",methods=["POST"])
def register_company():

    name=request.form["name"]
    email=request.form["email"]
    password=request.form["password"]
    contact=request.form["contact"]

    conn=get_db()
    cursor=conn.cursor()

    cursor.execute("INSERT INTO company(company_name,email,password,hr_contact,status) VALUES(?,?,?,?,?)",
                   (name,email,password,contact,"Pending"))

    conn.commit()

    return "Company Registered. Wait for admin approval."


# ADMIN DASHBOARD
@app.route("/admin_dashboard")
def admin_dashboard():

    conn=get_db()
    cursor=conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM student")
    students=cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM company")
    companies=cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM drive")
    drives=cursor.fetchone()[0]

    return render_template("admin_dashboard.html",students=students,companies=companies,drives=drives)


# APPROVE COMPANY
@app.route("/approve_company/<id>")
def approve_company(id):

    conn=get_db()
    cursor=conn.cursor()

    cursor.execute("UPDATE company SET status='Approved' WHERE id=?",(id,))
    conn.commit()

    return redirect("/admin_dashboard")


# COMPANY DASHBOARD
@app.route("/company_dashboard")
def company_dashboard():

    company_id=session["company"]

    conn=get_db()
    cursor=conn.cursor()

    cursor.execute("SELECT * FROM drive WHERE company_id=?",(company_id,))
    drives=cursor.fetchall()

    return render_template("company_dashboard.html",drives=drives)


# CREATE DRIVE
@app.route("/create_drive")
def create_drive():
    return render_template("create_drive.html")


@app.route("/add_drive",methods=["POST"])
def add_drive():

    title=request.form["title"]
    desc=request.form["desc"]
    eligibility=request.form["eligibility"]
    deadline=request.form["deadline"]

    company_id=session["company"]

    conn=get_db()
    cursor=conn.cursor()

    cursor.execute("INSERT INTO drive(company_id,job_title,description,eligibility,deadline,status) VALUES(?,?,?,?,?,?)",
                   (company_id,title,desc,eligibility,deadline,"Pending"))

    conn.commit()

    return redirect("/company_dashboard")


# STUDENT DASHBOARD
@app.route("/student_dashboard")
def student_dashboard():

    conn=get_db()
    cursor=conn.cursor()

    cursor.execute("SELECT * FROM drive WHERE status='Approved'")
    drives=cursor.fetchall()

    return render_template("student_dashboard.html",drives=drives)


# APPLY
@app.route("/apply/<id>")
def apply(id):

    student_id=session["student"]

    conn=get_db()
    cursor=conn.cursor()

    cursor.execute("SELECT * FROM application WHERE student_id=? AND drive_id=?",(student_id,id))
    exist=cursor.fetchone()

    if exist:
        return "Already Applied"

    cursor.execute("INSERT INTO application(student_id,drive_id,status) VALUES(?,?,?)",
                   (student_id,id,"Applied"))

    conn.commit()

    return redirect("/student_dashboard")


if __name__ == "__main__":
    app.run(debug=True)