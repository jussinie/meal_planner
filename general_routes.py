from app import app
from flask import redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash
from db import db
import recipes

@app.route("/")
def index():
    all_recipes = recipes.get_all_recipe_names_limit3()
    return render_template("index.html", all_recipes=all_recipes)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/send_login", methods=["POST"])
def send_login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        print("invalid username!")
        error_message = "Username doesn't exist! Please try again."
        return render_template("login.html", error_message=error_message)
    hash_value = user.password
    if check_password_hash(hash_value, password):
        print("valid password!")
        session["username"] = username
        return redirect("/")
        #return redirect(url_for('user', username=username))
    print("invalid password!")
    return redirect("/login")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
