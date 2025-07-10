# --- Final app.py with Landing Page, Session, Logout, Email Validation, Password Strength Check, Timestamp Fix ---

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
import pickle
import numpy as np
from datetime import datetime
import json
import os
import re

app = Flask(__name__)
app.secret_key = "cherry_secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Load ML Model
model = pickle.load(open("model/covid_model.pkl", "rb"))

# -------- MODELS -------- #
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    fever = db.Column(db.Integer)
    tired = db.Column(db.Integer)
    cough = db.Column(db.Integer)
    breath = db.Column(db.Integer)
    throat = db.Column(db.Integer)
    age = db.Column(db.Integer)
    result = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.now)

# -------- LOGIN MANAGER -------- #
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------- ROUTES -------- #
@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/home")
def home():
    return redirect(url_for('login'))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Email format check
        email_pattern = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
        if not re.match(email_pattern, email):
            flash("Invalid email format!", "danger")
            return redirect(url_for("register"))

        # Password strength check (at least 6 characters, one letter, one number)
        password_pattern = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$'
        if not re.match(password_pattern, password):
            flash("Password must be at least 6 characters long and contain letters and numbers.", "danger")
            return redirect(url_for("register"))

        if User.query.filter(User.email.ilike(email)).first():
            flash("Email already exists", "danger")
            return redirect(url_for("register"))

        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registered successfully! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            login_user(user)
            session['user_id'] = user.id
            flash("Logged in successfully!", "success")
            return redirect(url_for("predict"))
        else:
            flash("Invalid credentials", "danger")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/predict", methods=["GET", "POST"])
@login_required
def predict():
    if request.method == "POST":
        f = int(request.form.get("fever"))
        t = int(request.form.get("tired"))
        c = int(request.form.get("cough"))
        b = int(request.form.get("breath"))
        s = int(request.form.get("throat"))
        a = int(request.form.get("age"))

        symptoms = {"Fever": f, "Tiredness": t, "Dry Cough": c, "Breathing": b, "Sore Throat": s}
        final_features = np.array([[f, t, c, b, s, a]])
        prediction = model.predict(final_features)[0]
        result = "⚠️ High Risk of COVID-19" if prediction == 1 else "✅ Low Risk"

        now = datetime.now()
        record = Prediction(user_id=current_user.id, fever=f, tired=t, cough=c, breath=b, throat=s, age=a, result=result, timestamp=now)
        db.session.add(record)
        db.session.commit()

        return render_template("index.html", result=result, symptoms=symptoms)

    return render_template("index.html")

@app.route("/dashboard")
@login_required
def dashboard():
    history = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.timestamp.desc()).all()
    return render_template("dashboard.html", history=history)

# -------- MAIN -------- #
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
