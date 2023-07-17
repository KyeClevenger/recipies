from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def login_reg():
    # if "user_id" in session:
    #     return redirect("/recipes")
    return render_template("index.html")

@app.route('/users/register', methods=["POST"])
def register():
    if not User.is_valid(request.form):
        return redirect('/')
    hash_pass= bcrypt.generate_password_hash(request.form["password"])
    data={
        **request.form,
        "password": hash_pass,
        "cpass": hash_pass
    }
    logged_user_id = User.create(data)
    session["user_id"] =logged_user_id
    session["first_name"]=request.form["first_name"]
    return redirect('/recipes')


@app.route('/users/login', methods=['POST'])
def login():
    data={
        "email": request.form['email']
    }
    potential_user=User.get_by_email(data)
    if not potential_user:
        flash("invalid credentials", "log")
        return redirect('/')
    if not bcrypt.check_password_hash(potential_user.password,request.form["password"]):
        flash("invalid credentials", "log")
        return redirect('/')
    session["user_id"]=potential_user.id
    session["first_name"]=potential_user.first_name
    return redirect('/recipes')
    

@app.route('/recipes')
def dashboard():
    return render_template("recipes.html")