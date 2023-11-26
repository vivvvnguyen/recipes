from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/reg/process', methods=["POST"])
def registration_process():
    if not User.validate_reg(request.form):
        return redirect('/')
    password_hash = bcrypt.generate_password_hash(request.form["password"])
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": password_hash
    }
    user_id = User.save(data)
    session["user_id"] = user_id
    return redirect('/success')

@app.route('/success')
def registered():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session["user_id"]
    }
    all_recipes = Recipe.get_all()
    return render_template("dashboard.html", user = User.get_by_id(data), all_recipes = all_recipes)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/login', methods=["POST"])
def login():
    data = {"email": request.form["email"]}
    db_user = User.get_by_email(data)
    # Checks to see if email that was entered is in the database 
    if not db_user:
        flash("Invalid Email/Password","login")
        return redirect('/')
    if not bcrypt.check_password_hash(db_user.password, request.form['password']):
        flash("Invalid Email/Password","login")
        return redirect('/')
    session["user_id"] = db_user.id
    return redirect('/success')