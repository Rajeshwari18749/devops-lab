from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------------
# Database Model
# -------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Create database
with app.app_context():
    db.create_all()

# -------------------------
# Home Page
# -------------------------
@app.route('/')
def home():
    return render_template("home.html")

# -------------------------
# User Registration
# -------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(
            name=name,
            email=email,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        return render_template("success.html")

    return render_template("register.html")

# -------------------------
# Admin Dashboard
# -------------------------
@app.route('/admin')
def admin():

    search = request.args.get("search")

    if search:
        users = User.query.filter(
            (User.name.contains(search)) |
            (User.email.contains(search))
        ).all()
    else:
        users = User.query.all()

    total_users = User.query.count()

    return render_template(
        "admin.html",
        users=users,
        total_users=total_users
    )

# -------------------------
# Run Application
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)