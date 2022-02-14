from sqlalchemy import null
from app import app
from flask import redirect, render_template, request, session, url_for
from user import User
from recipe import Recipe
from ingredient import Ingredient
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

@app.route("/")
def index():
    result = db.session.execute("SELECT name FROM recipes LIMIT 2")
    recipes = result.fetchall()
    #print("session token", session["username"])
    #return f'heippa {user.name}, your BMR is {calculate_bmr(user.weight, user.height, user.age, True)}'
    return render_template("index.html", recipes=recipes)

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
        sql = "INSERT INTO users (first_name, last_name, username, password, height, weight, age, gender, bmr) VALUES (:first_name, :last_name, :username, :password, :height, :weight, :age, :gender, :bmr)"
        db.session.execute(sql, {"first_name":first_name, "last_name":last_name, "username":username, "password":hash_value, "height":height, "weight":weight, "age":age, "gender":gender, "bmr":bmr })
        db.session.commit()
        return redirect("login")
    except:
        error_message="Username exists already. Please try again with another username."
        return render_template("new_user.html", error_message=error_message)

@app.route("/users")
def users():
    result = db.session.execute("SELECT * FROM users")
    users = result.fetchall()
    return render_template("users.html", count=len(users), users=users)

@app.route("/users/<username>")
def user(username):
    sql = "SELECT * FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    print(user)
    sql_meals = "SELECT r.name, r.total_kcal FROM recipes r, users_recipes ur WHERE user_id=:user_id AND r.id = ur.recipe_id"
    result_meals = db.session.execute(sql_meals, {"user_id":user[0]})
    meals = result_meals.fetchall()
    print(meals)
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

@app.route("/ingredients", methods=['GET', 'POST'])
def ingredients():
    if request.method == 'POST':
        # Fetch ingredient id from the form
        if (request.form.get('ingredient_approved')):
            id = int(request.form.get('ingredient_approved'))
            # Update approval status in db
            sql_approve_ingredient = "UPDATE ingredients SET approved=true WHERE id=:id"
            db.session.execute(sql_approve_ingredient, {"id":id})
            db.session.commit()
            return redirect("/ingredients")
        elif (request.form.get('ingredient_removed')):
            
            id = int(request.form.get('ingredient_removed'))
            print(id, 'removed')
            sql_cancel_adding_ingredient = "DELETE FROM ingredients WHERE id=:id"
            db.session.execute(sql_cancel_adding_ingredient, {"id":id})
            db.session.commit()
            return redirect("/ingredients")

        elif (request.form.get('ingredient_canceled')):
            
            id = int(request.form.get('ingredient_canceled'))
            print(id, 'canceled')
            # Delete row from table, i.e. cancel adding ingredient
            sql_cancel_adding_ingredient = "DELETE FROM ingredients WHERE id=:id"
            db.session.execute(sql_cancel_adding_ingredient, {"id":id})
            db.session.commit()
            return redirect("/ingredients")

    elif request.method == 'GET':
        # Fetch user
        username=session["username"]
        sql_user = "SELECT * FROM users WHERE username=:username"
        user_result = db.session.execute(sql_user, {"username":username})
        user = user_result.fetchone()

        # Fetch approved ingredients
        result = db.session.execute("SELECT name, kcal, carbs, protein, fat, salt FROM ingredients WHERE approved=true")
        ingredients = result.fetchall()

        # Fetch non_approved ingredients
        result_not_approved = db.session.execute("SELECT id, name, kcal, carbs, protein, fat, salt FROM ingredients WHERE approved=false")
        ingredients_not_approved = result_not_approved.fetchall()

        # Fetch non_approved ingredients that logged in user has added
        user_id = user[0]
        sql_ingredient_added_by_user = "SELECT id, name, kcal, carbs, protein, fat, salt FROM ingredients WHERE approved=false AND added_by_user_id=:user_id"
        result_not_approved_user = db.session.execute(sql_ingredient_added_by_user, {"user_id":user_id})
        ingredients_not_approved_user = result_not_approved_user.fetchall()

        print(user)
        return render_template("ingredients.html", count=len(ingredients), ingredients=ingredients, ingredients_not_approved=ingredients_not_approved, ingredients_not_approved_user=ingredients_not_approved_user,user=user)

    else:
        print("mentiin elseen")
        return redirect("/ingredients")

@app.route("/add_ingredient")
def add_ingredient():
    return render_template("add_ingredient.html")

@app.route("/send_ingredient", methods=["POST"])
def send_ingredient():
    username=session["username"]
    sql_user = "SELECT * FROM users WHERE username=:username"
    user_result = db.session.execute(sql_user, {"username":username})
    user_id = user_result.fetchone()[0]

    name = request.form["name"]
    kcal = request.form["kcal"]
    carbs = request.form["carbs"]
    protein = request.form["protein"]
    fat = request.form["fat"]
    salt = request.form["salt"]
    sql = "INSERT INTO ingredients (name, kcal, carbs, protein, fat, salt, approved, added_by_user_id) VALUES (:name, :kcal, :carbs, :protein, :fat, :salt, false, :user_id)"
    db.session.execute(sql, {"name":name, "kcal":kcal, "carbs":carbs, "protein":protein, "fat":fat, "salt":salt, "user_id":user_id})
    db.session.commit()
    return redirect("/recipes")

@app.route("/recipes")
def recipes():
    result = db.session.execute("SELECT name FROM recipes")
    recipes = result.fetchall()
    return render_template("recipes.html", count=len(recipes), recipes=recipes)

@app.route("/add_recipe")
def add_recipe():
    result = db.session.execute("SELECT name FROM ingredients")
    ingredients = result.fetchall()
    return render_template("add_recipe.html", ingredients=ingredients)

@app.route("/send_recipe", methods=["POST"])
def send_recipe():
    name = request.form["name"]
    ingredients = request.form.getlist("ingredient")
    print(ingredients)
    sql_ingredient_id = "SELECT id, name FROM ingredients WHERE name=:ingredient1"
    sql_ingredient_id_result = db.session.execute(sql_ingredient_id, {"ingredient1":ingredients[0]})
    ingredient_result = sql_ingredient_id_result.fetchone()[0]
    print(ingredient_result)
    amounts = request.form.getlist("ingredient_amount")
    sql_recipe = "INSERT INTO recipes (name) VALUES (:name) RETURNING id"
    result = db.session.execute(sql_recipe, {"name":name})
    db.session.commit()
    recipe_id = result.fetchone()[0]
    print(amounts[0], recipe_id, ingredient_result)
    # add recipe with ingredient(s)
    sql_recipe_ingredients = "INSERT INTO recipes_ingredients (amount, recipe_id, ingredient_id) VALUES (:amount1, :recipe_id, :ingredient_id)"
    db.session.execute(sql_recipe_ingredients, {"amount1":amounts[0], "recipe_id":recipe_id, "ingredient_id":ingredient_result})
    # add total values from ingredient to recipe
    kcal_sql = "SELECT kcal FROM ingredients WHERE id=:ingredient_id"
    kcal_result = db.session.execute(kcal_sql, {"ingredient_id":ingredient_result})
    kcal = int(kcal_result.fetchone()[0]) * int(amounts[0]) / 100.0
    sql_update_recipe = "UPDATE RECIPES SET total_kcal=:kcal WHERE id=:recipe_id"
    db.session.execute(sql_update_recipe, {"kcal":kcal, "recipe_id":recipe_id})
    db.session.commit()
    return redirect("/recipes")

@app.route("/<name>", methods=['GET', 'POST'])
def recipe(name):
    if request.method == 'POST':
        if "submit_comment" in request.form:
            comment = request.form["comment"]
            print("uusi comment!")
            print(comment)
            #Fetch recipe id
            sql_recipe_id = "SELECT id FROM recipes WHERE name=:name"
            recipe_id_result = db.session.execute(sql_recipe_id, {"name":name})
            recipe_id = recipe_id_result.fetchone()[0]
            print(recipe_id)
            #Fetch user id
            username=session["username"]
            sql_user_id = "SELECT id FROM users WHERE username=:username"
            user_id_result = db.session.execute(sql_user_id, {"username":username})
            user_id = user_id_result.fetchone()[0]
            #Fetch all comments
            sql_comment = "INSERT INTO comments (user_id, recipe_id, content, sent_at) VALUES (:user_id, :recipe_id, :comment, NOW())"
            db.session.execute(sql_comment, {"user_id":user_id, "recipe_id":recipe_id, "comment":comment})
            db.session.commit()
            #sql_ingredient_id_result = db.session.execute(sql_ingredient_id, {"ingredient1":ingredient1})
            #ingredient_result = sql_ingredient_id_result.fetchone()[0]
            #print(ingredient_result)
            #amount1 = request.form["ingredient1_amount"]
            #sql_recipe = "INSERT INTO recipes (name) VALUES (:name) RETURNING id"
            #result = db.session.execute(sql_recipe, {"name":name})
            #recipe_id = result.fetchone()[0]
            #print(amount1, recipe_id, ingredient_result)
            #sql_recipe_ingredients = "INSERT INTO recipes_ingredients (amount, recipe_id, ingredient_id) VALUES (:amount1, :recipe_id, :ingredient_id)"
            #db.session.execute(sql_recipe_ingredients, {"amount1":amount1, "recipe_id":recipe_id, "ingredient_id":ingredient_result})
            #db.session.commit()
            return redirect("/recipes")
        elif "add_recipe_to_plan" in request.form:
            sql_recipe_id = "SELECT id FROM recipes WHERE name=:name"
            recipe_id_result = db.session.execute(sql_recipe_id, {"name":name})
            recipe_id = recipe_id_result.fetchone()[0]
            print(recipe_id)
            print("Meal added!")
            #Fetch user id
            username=session["username"]
            sql_user_id = "SELECT id FROM users WHERE username=:username"
            user_id_result = db.session.execute(sql_user_id, {"username":username})
            user_id = user_id_result.fetchone()[0]
            #Add to recipes
            sql_add_to_plan = "INSERT INTO users_recipes (user_id, recipe_id) VALUES (:user_id, :recipe_id)"
            db.session.execute(sql_add_to_plan, {"user_id":user_id, "recipe_id":recipe_id})
            db.session.commit()
            return redirect("/recipes")
        else:
            print("pieleen menee")

    else: 
        sql = "SELECT r.name as recipe_name, i.name as ingredient_name, i.kcal, i.carbs, i.protein, i.fat, i.salt, ri.amount, r.id, r.total_kcal FROM recipes r, ingredients i, recipes_ingredients ri WHERE r.name=:name AND r.id = ri.recipe_id AND i.id = ri.ingredient_id"
        result = db.session.execute(sql, {"name":name})
        recipes = result.fetchone()
        print(recipes)
        recipe_name = recipes[0]
        ingredient_name = recipes[1]
        kcal = recipes[2]
        carbs = recipes[3]
        protein = recipes[4]
        fat = recipes[5]
        salt = recipes[6]
        amount = recipes[7]
        recipe_id = recipes[8]
        total_kcal = recipes[9]
        total = f'Total calories {total_kcal}, carbohydrates {carbs/100*amount}, protein {protein/100*amount}, fat {fat/100*amount}.'
        print(ingredient_name)
        #comments
        #sql_comments = "SELECT * FROM comments WHERE recipe_id=:recipe_id"
        sql_comments = "SELECT c.content, c.sent_at, u.first_name, u.last_name FROM comments c LEFT JOIN users u ON u.id=user_id WHERE recipe_id=:recipe_id ORDER BY c.sent_at"
        result_comments = db.session.execute(sql_comments, {"recipe_id":recipe_id})
        print("kommentointia", result_comments)
        return render_template("recipe.html", recipe_name=recipe_name, ingredient_name=ingredient_name, amount=amount, total=total, comments=result_comments)    

@app.route("/send_comment", methods=["POST"])
def send_comment():
    comment = request.form["comment"]
    print(comment)
    sql_comment = "INSERT INTO comments (user_id, recipe_id, content, sent_at) VALUES (1, 22, :comment, NOW())"
    db.session.execute(sql_comment, {"comment":comment})
    db.session.commit()
    #sql_ingredient_id_result = db.session.execute(sql_ingredient_id, {"ingredient1":ingredient1})
    #ingredient_result = sql_ingredient_id_result.fetchone()[0]
    #print(ingredient_result)
    #amount1 = request.form["ingredient1_amount"]
    #sql_recipe = "INSERT INTO recipes (name) VALUES (:name) RETURNING id"
    #result = db.session.execute(sql_recipe, {"name":name})
    #recipe_id = result.fetchone()[0]
    #print(amount1, recipe_id, ingredient_result)
    #sql_recipe_ingredients = "INSERT INTO recipes_ingredients (amount, recipe_id, ingredient_id) VALUES (:amount1, :recipe_id, :ingredient_id)"
    #db.session.execute(sql_recipe_ingredients, {"amount1":amount1, "recipe_id":recipe_id, "ingredient_id":ingredient_result})
    #db.session.commit()
    return redirect("/recipes")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")