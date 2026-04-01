from flask import Flask
from database import init_db
from controllers.auth_controller import auth_bp
from controllers.admin_controller import admin_bp
from controllers.company_controller import company_bp
from controllers.student_controller import student_bp

app = Flask(__name__)
app.secret_key = "secret123"

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(company_bp)
app.register_blueprint(student_bp)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)