import re
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user


app = Flask(__name__)

# Secret Key For Password Security
app.config["SECRET_KEY"] = "1122"

# Database setup using SQlite3
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

# Making a pointer to the database and hashing passwords and login manager
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Making the default app route if the user is not logged in to point to that
login_manager.login_view = "login"


# User Model For the database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), unique = True, nullable = False)
    password = db.Column(db.String(200), nullable = False)


# Load user function for load manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Password Validation Function
def is_valid_password(password):

    # Making checks for numbers, alphabets, length, specials
    if len(password) < 8:
        return "Password must be at least 8 characters long"
    
    if not re.search(r"[A-Z]", password):
        return "Password must contain 1 Uppercase character"
    
    if not re.search(r"[a-z]", password):
        return "Password must contain 1 Lowercase character"
    
    if not re.search(r"[\d]", password):
        return "Password must contain 1 Number character"
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Password must contain at least one special character."
    
    # If password valid
    return None


# My main index route
@app.route("/")
@login_required
def home():
    return f"Hello, {current_user.username}"


# Register Route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Checking if user name already taken
        existing_user = User.query.filter_by(username = username).first()
        if existing_user:
            flash("Username already taken. Choose another.", "error")
            return  redirect(url_for("register"))
        
        # Validate Password
        validation_error = is_valid_password(password)
        if validation_error:
            flash(validation_error, "error")
            return redirect(url_for("register"))

        # Hash the password before saving
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Create the new user and add to the database
        new_user = User(username = username, password = hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Redirecting user now to login
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("login"))
    
    # If Get method
    return render_template("register.html")


# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():

    # Checking if user submitted a form
    if request.method == "POST":

        # Getting the username and password
        username = request.form.get("username")
        password = request.form.get("password")

        # Finding the user from the database
        user = User.query.filter_by(username=username).first()

        # Checking if name and hash matches
        if user and bcrypt.check_password_hash(user.password, password):

            # Log the user in
            login_user(user)

            # Redirect the user to home
            return redirect(url_for("home"))
        else:
            return "Invalid Credentials"
        
    # If user clicked on site using get
    return render_template("login.html")


# Logout route
@app.route("/logout")
@login_required
def logout():

    # Logout user and redirect to login page
    logout_user()
    return redirect(url_for("login"))




# Default app stuff
if __name__ == '__main__':
    with app.app_context():  # Ensure Flask app context is active
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
