from app import app
from flask import redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
import ingredient_funcs
import recipes
import comments
import users

@app.route("/")
def index():
    all_recipes = recipes.get_all_recipe_names_limit3()
    return render_template("index.html", all_recipes=all_recipes)

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
        users.add_user(first_name, last_name, username, hash_value, height, weight, age, gender, bmr)
        return redirect("login")
    except:
        error_message="Username exists already. Please try again with another username."
        return render_template("new_user.html", error_message=error_message)

@app.route("/users")
def all_users():
    all_usernames = users.get_all_usernames()
    return render_template("users.html", count=len(all_usernames), all_usernames=all_usernames)

@app.route("/users/<username>")
def user_page(username):
    user = users.get_one_user(username)
    meals = recipes.get_users_recipes(user[0])
    return render_template("user.html", user=user, meals=meals)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/send_login", methods=["POST"])
def send_login():
    username = request.form["username"]
    password = request.form["password"]
    #session["username"] = username
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        print("invalid username!")
        error_message = "Username doesn't exist! Please try again."
        return render_template("login.html", error_message=error_message)
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            print("valid password!")
            session["username"] = username
            return redirect(url_for('user', username=username))
        else:
            print("invalid password!")
            return redirect("/login")

# ROUTES REGARDING INGREDIENTS

@app.route("/ingredients", methods=['GET', 'POST'])
def ingredients():
    if request.method == 'POST':
        # Fetch ingredient id from the form
        if request.form.get('ingredient_approved'):
            id = int(request.form.get('ingredient_approved'))
            # Update approval status in db
            ingredient_funcs.set_ingredient_as_approved(id)
            return redirect("/ingredients")

        elif request.form.get('ingredient_removed'):            
            id = int(request.form.get('ingredient_removed'))
            ingredient_funcs.remove_ingredient(id)
            return redirect("/ingredients")

        elif request.form.get('ingredient_canceled'):
            id = int(request.form.get('ingredient_canceled'))
            print(id, 'canceled')
            # Delete row from table, i.e. cancel adding ingredient
            ingredient_funcs.cancel_approval(id)
            return redirect("/ingredients")

    elif request.method == 'GET':
        # Fetch user
        username = session["username"]
        user = users.get_one_user(username)

        # Fetch approved ingredients
        approved_ingredients = ingredient_funcs.get_approved_ingredients()

        # Fetch non_approved ingredients
        ingredients_not_approved = ingredient_funcs.get_non_approved_ingredients()

        # Fetch non_approved ingredients that logged in user has added
        ingredients_not_approved_user = ingredient_funcs.get_non_approved_ingredients_from_user(user[0])
        return render_template("ingredients.html", count=len(approved_ingredients), approved_ingredients=approved_ingredients, ingredients_not_approved=ingredients_not_approved, ingredients_not_approved_user=ingredients_not_approved_user,user=user)

    else:
        print("mentiin elseen")
        return redirect("/ingredients")

@app.route("/add_ingredient")
def add_ingredient():
    return render_template("add_ingredient.html")

@app.route("/send_ingredient", methods=["POST"])
def send_ingredient():
    username=session["username"]
    user_id = users.get_one_user(username)[0]

    name = request.form["name"]
    kcal = request.form["kcal"] 
    carbs = request.form["carbs"]
    protein = request.form["protein"]
    fat = request.form["fat"]
    salt = request.form["salt"]

    ingredient_funcs.add_ingredient(name, kcal, carbs, protein, fat, salt, user_id)
    return redirect("/ingredients")

# ROUTES REGARDING RECIPES

@app.route("/recipes")
def show_recipes():
    recipe_names = recipes.get_all_recipe_names()
    print(recipe_names)
    return render_template("recipes.html", count=len(recipe_names), recipe_names=recipe_names)

@app.route("/add_recipe")
def add_recipe():
    all_ingredients = ingredient_funcs.get_ingredient_names()
    print(all_ingredients)
    return render_template("add_recipe.html", all_ingredients=all_ingredients)

@app.route("/send_recipe", methods=["POST"])
def send_recipe():
    name = request.form["name"]
    ingredients = request.form.getlist("ingredient")
    print(ingredients)
    # Fetching multiple ingredients from page
    ingredient_ids = []
    for ingredient in ingredients:
        if ingredient != "":
            ingredient_ids.append(ingredient_funcs.get_one_ingredient_with_name(ingredient))
    print(ingredient_ids)

    # Fetching multiple ingredient amounts from page
    amounts = request.form.getlist("ingredient_amount")

    #for amount in amounts:
    #    if (len(amount) > 4):
    #        return redirect("/add_recipe.html")

    recipe_id = recipes.add_recipe_and_return_id(name)
    print(recipe_id, "recipe_id")

    # add recipe with ingredient(s)
    for ingredient_id, amount in zip(ingredient_ids, amounts):
        recipes.add_recipe_with_ingredients(amount, recipe_id, ingredient_id)
    db.session.commit()

    # add total values from ingredient to recipe
    total_kcal = 0
    for ingredient_id in ingredient_ids:
        kcal_result = ingredient_funcs.get_one_ingredient_with_id(ingredient_id)
        total_kcal += int(kcal_result.fetchone()[0]) * int(amount) / 100.0
    recipes.update_recipe_total_kcal(total_kcal, recipe_id)

    return redirect("/recipes")

@app.route("/recipes/<name>", methods=['GET', 'POST'])
def recipe(name):
    username=session["username"]
    user_id = users.get_user_id_with_username(username)

    if request.method == 'POST':
        if "submit_comment" in request.form:
            comment = request.form["comment"]
            recipe_id = recipes.get_recipe_id_with_name(name)
            #Post comment
            comments.add_comment(user_id, recipe_id, comment)
            return redirect("/recipes")
        elif "add_recipe_to_plan" in request.form:
            recipe_id = recipes.get_recipe_id_with_name(name)
            #Add to recipes
            recipes.add_recipe_to_meal_plan(user_id, recipe_id)
            return redirect("/recipes")
        else:
            print("pieleen menee")

    else:
        all_ingredients = ingredient_funcs.get_all_ingredients_for_recipe(name)
        recipe_data = recipes.get_recipe_data_with_name(name)
        recipe_id = recipe_data[0]
        recipe_name = recipe_data[1]
        recipe_kcal = recipe_data[2]
        return render_template("recipe.html", all_ingredients=all_ingredients, recipe_kcal=recipe_kcal, recipe_name=recipe_name, comments=comments.get_all_comments(recipe_id))

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")