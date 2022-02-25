from app import app
from flask import redirect, render_template, request, session, url_for
from db import db
import ingredient_funcs
import recipes
import comments
import users

@app.route("/recipes")
def show_recipes():
    recipe_names = recipes.get_all_recipe_names()
    print(recipe_names)
    return render_template("recipes.html", count=recipes.get_recipe_count(), recipe_names=recipe_names)

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
        if amount != "":
            recipes.add_recipe_with_ingredients(amount, recipe_id, ingredient_id)
    db.session.commit()

    # add total values from ingredient to recipe
    total_kcal = 0
    for ingredient_id, amount in zip(ingredient_ids, amounts):
        if amount != "":
            kcal_result = ingredient_funcs.get_one_ingredient_with_id(ingredient_id)
            total_kcal += int(kcal_result.fetchone()[0]) * int(amount) / 100.0
    recipes.update_recipe_total_kcal(total_kcal, recipe_id)

    return redirect(f"/recipes/{name}")

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
            return redirect(f"/users/{username}")
        else:
            print("pieleen menee")

    else:
        all_ingredients = ingredient_funcs.get_all_ingredients_for_recipe(name)
        recipe_data = recipes.get_recipe_data_with_name(name)
        recipe_id = recipe_data[0]
        recipe_name = recipe_data[1]
        recipe_kcal = recipe_data[2]
        return render_template("recipe.html", all_ingredients=all_ingredients, recipe_kcal=recipe_kcal, recipe_name=recipe_name, comments=comments.get_all_comments(recipe_id))

@app.route("/remove_recipe/<name>", methods=['POST'])
def remove_recipe(name):
    username = session["username"]
    user_id = users.get_user_id_with_username(username)
    recipe_id = recipes.get_recipe_id_with_name(name)
    users.remove_meal_from_plan(user_id, recipe_id)
    return redirect(f"/users/{username}")