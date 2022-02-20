from app import app
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash
import users
import recipes

@app.route("/new_user")
def new():
    return render_template("new_user.html")

@app.route("/send_new_user", methods=["POST"])
def send():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    username = request.form["username"]
    password = request.form["password"]
    height = int(request.form["height"])
    weight = float(request.form["weight"])
    age = int(request.form["age"])
    gender = request.form["gender"]

    def calculate_bmr(weight: float, height: int, age: int, gender: str):
        if gender == "Male" or gender == "male":
            bmr = 10.0 * weight + 6.25 * height - 5 * age + 5
            return bmr
        else:
            bmr = 10.0 * weight + 6.25 * height - 5 * age - 161
            return bmr

    bmr = calculate_bmr(weight, height, age, gender)

    hash_value = generate_password_hash(password)

    try:
        users.add_user(
            first_name,
            last_name,
            username,
            hash_value,
            height,
            weight,
            age,
            gender,
            bmr
            )
        return redirect("login")
    except RuntimeError:
        return render_template(
            "new_user.html",
            error_message="Username exists already. Please try again with another username."
            )

@app.route("/users")
def all_users():
    all_usernames = users.get_all_usernames()
    return render_template("users.html", count=len(all_usernames), all_usernames=all_usernames)

@app.route("/users/<username>")
def user_page(username):
    user = users.get_one_user(username)
    print(user)
    meals = recipes.get_users_recipes(user[0])
    try:
        total_kcal = users.get_total_kcal_for_user(user[0])
        budget_left = user[9] - total_kcal
        return render_template(
            "user.html",
            user=user,
            meals=meals,
            total_kcal=total_kcal,
            budget_left=budget_left)
    except:
        return render_template(
            "user.html",
            user=user,
            meals=meals)
        