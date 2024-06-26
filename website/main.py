# Dependencies Used
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "abc"
db = SQLAlchemy()
 
login_manager = LoginManager()
login_manager.init_app(app)
 
# Class for user data
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    streak = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))
    lastlogin = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC))

 
db.init_app(app)


with app.app_context():
    db.create_all()
 
# Find a user when they log in
@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)
 
# Adds user to the database when they register
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = Users(username=request.form.get("username"),
                     password=request.form.get("password"),
                     streak=0)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("sign_up.html")
 
# Retrieves user's data and logs them in
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(
            username=request.form.get("username")).first()
        if user.password == request.form.get("password"):
            login_user(user)
            user.lastlogin = datetime.datetime.now(datetime.UTC)
            if user.lastlogin > datetime.datetime.now(datetime.UTC):
                user.streak += 1
            db.session.commit()
            return redirect(url_for("home"))
    return render_template("login.html")
 
# Logs out user
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))
 
 
@app.route("/")
def home():
    return render_template("home.html")
 
# Runs the main script
if __name__ == "__main__":
    app.run()
