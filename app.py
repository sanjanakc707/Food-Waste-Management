from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import random

# ------------------------------
# Flask App Setup
# ------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# ------------------------------
# Database Models
# ------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    expiry_date = db.Column(db.String(20), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

# ------------------------------
# Dummy ML Function
# ------------------------------
def predict_use_for_expired(food_name):
    # Simple rule-based + random prediction
    fertilizer_foods = ["vegetables", "fruits", "bread", "rice"]
    animal_foods = ["milk", "grains", "leftovers", "meat"]

    if any(word in food_name.lower() for word in fertilizer_foods):
        return "fertilizer"
    elif any(word in food_name.lower() for word in animal_foods):
        return "animal feed"
    else:
        return random.choice(["fertilizer", "animal feed"])

# ------------------------------
# Routes
# ------------------------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------- Authentication ----------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        if User.query.filter_by(email=email).first():
            flash("Email already exists!", "danger")
            return redirect(url_for("signup"))

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Signup successful! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials", "danger")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))

# ---------- Dashboard ----------
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form["name"]
        expiry_date = request.form["expiry_date"]
        new_item = FoodItem(name=name, expiry_date=expiry_date)
        db.session.add(new_item)
        db.session.commit()
        flash("Food item added!", "success")
        return redirect(url_for("dashboard"))

    items = FoodItem.query.order_by(FoodItem.added_at.desc()).all()
    return render_template("dashboard.html", items=items)

# ---------- Check Food Status ----------
@app.route("/food_status/<int:item_id>")
def food_status(item_id):
    item = FoodItem.query.get_or_404(item_id)
    today = datetime.utcnow().date()
    expiry = datetime.strptime(item.expiry_date, "%Y-%m-%d").date()

    if expiry < today:
        suggestion = predict_use_for_expired(item.name)
        return render_template("expired.html", item=item, suggestion=suggestion)
    elif (expiry - today).days <= 3:
        return render_template("near_expiry.html", item=item, days_left=(expiry - today).days)
    else:
        return render_template("fresh.html", item=item)

# ------------------------------
# Run App
# ------------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
