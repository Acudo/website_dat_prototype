# Dependencies Used
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SECRET_KEY"] = "abc"
db = SQLAlchemy()

app.static_folder = 'static'

login_manager = LoginManager()
login_manager.init_app(app)
 
# Class for user data
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    streak = db.Column(db.Integer, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)
    last_streak_update = db.Column(db.DateTime, nullable=False)
    friends = db.Column(db.JSON(db.Integer), default = [])
    pending_friends = db.Column(db.JSON(db.Integer), default = [])


db.init_app(app)


with app.app_context():
    db.create_all()


def get_current_time():
    return datetime.datetime.now(datetime.UTC)
 

# Find a user when they log in
@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)
 

@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))


@app.route("/home")
def home():
    return render_template("home.html")


# Adds user to the database when they register
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = Users(username = request.form.get("username"),
                     password = request.form.get("password"),
                     streak = 0,
                     last_login = get_current_time(),
                     last_streak_update = get_current_time())
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("sign_up.html")

# Retrieves user's data and logs them in
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(
            username = request.form.get("username")).first()
        if user.password == request.form.get("password"):
            # Logs in the user
            login_user(user)
            print((datetime.datetime.now() - user.last_login).days)
            # Updates the streak
            day_difference = (datetime.datetime.now() - user.last_streak_update).days
            if day_difference == 1:
                user.streak += 1
                user.last_streak_update = get_current_time()
            elif day_difference >= 2:
                user.streak = 0
                user.last_streak_update = get_current_time()
            user.lastlogin = get_current_time()
            db.session.commit()
            return redirect(url_for("home"))
    return render_template("login.html")


# Logs out user
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))
 

# Friend List
@app.route('/social', methods=["GET", "POST"])
def social():
    print(request)
    if request.method == "POST" and "username" in request.form:
        receiver = Users.query.filter_by(
                username = request.form.get("username")).first()
        receiver.pending_friends = receiver.pending_friends + [current_user.username]
        db.session.add(receiver)
        db.session.commit()
    elif request.method == "POST" and "":
        pass

    return render_template("social.html", pending_friends=current_user.pending_friends)
 

# Runs the main script
if __name__ == "__main__":
    app.run(host='0.0.0.0')