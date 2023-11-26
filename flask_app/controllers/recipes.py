from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/create')
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')
    return render_template("create.html")

@app.route("/process/create", methods=["POST"])
def create_recipe_process():
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect('/create')
    data = {
        "user_id": session['user_id'],
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_cooked": request.form["date_cooked"],
        "under_30": request.form["under_30"]
    }
    print(data)
    Recipe.save(data)
    return redirect('/success')

@app.route("/recipe/delete/<int:recipe_id>")
def recipe_destroy(recipe_id):
    data = {"id": recipe_id}
    Recipe.delete(data)
    return redirect('/success')

@app.route("/recipe/show/<int:recipe_id>")
def recipe_show(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_by_id({"id": session["user_id"]})
    recipe = Recipe.get_by_id({"id":recipe_id})
    return render_template("show.html", user = user, one_recipe = recipe)

@app.route("/recipe/edit/<int:recipe_id>")
def recipe_edit(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_by_id({"id": session["user_id"]})
    recipe = Recipe.get_by_id({"id": recipe_id})
    return render_template("edit.html",user=user, one_recipe = recipe)

@app.route("/recipe/edit/process/<int:recipe_id>", methods=["POST"])
def recipe_edit_process(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipe/edit/{recipe_id}')
    data = {
        "user_id": session['user_id'],
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_cooked": request.form["date_cooked"],
        "under_30": request.form["under_30"],
        "id": recipe_id
    }
    # print(data)
    Recipe.update(data)
    return redirect('/success')