from flask import redirect, render_template, request, session, abort
from app import app
import ingredient_funcs
import users

@app.route("/ingredients", methods=['GET', 'POST'])
def ingredients():
    if request.method == 'POST':
        # Fetch ingredient id from the form
        if request.form.get('ingredient_approved'):
            ingredient_id = int(request.form.get('ingredient_approved'))
            # Update approval status in db
            ingredient_funcs.set_ingredient_as_approved(ingredient_id)
            return redirect("/ingredients")

        elif request.form.get('ingredient_removed'):
            ingredient_id = int(request.form.get('ingredient_removed'))
            ingredient_funcs.remove_ingredient(ingredient_id)
            return redirect("/ingredients")

        elif request.form.get('ingredient_canceled'):
            ingredient_id = int(request.form.get('ingredient_canceled'))
            print(id, 'canceled')
            # Delete row from table, i.e. cancel adding ingredient
            ingredient_funcs.cancel_approval(ingredient_id)
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
        return render_template(
            "ingredients.html",
            count=ingredient_funcs.approved_ingredient_count(),
            approved_ingredients=approved_ingredients,
            ingredients_not_approved=ingredients_not_approved,
            ingredients_not_approved_user=ingredients_not_approved_user,
            user=user)

    else:
        return redirect("/ingredients")

@app.route("/add_ingredient")
def add_ingredient():
    return render_template("add_ingredient.html")

@app.route("/send_ingredient", methods=["POST"])
def send_ingredient():

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    name = request.form["name"]
    kcal = request.form["kcal"]
    carbs = request.form["carbs"]
    protein = request.form["protein"]
    fat = request.form["fat"]
    salt = request.form["salt"]

    try:
        kcal = int(kcal)
        carbs = float(carbs)
        protein = float(protein)
        fat = float(fat)
        salt = float(salt)
    except:
        return render_template("add_ingredient.html", error="Please check the format of inserted values.")

    ingredient_funcs.add_ingredient(name, kcal, carbs, protein, fat, salt, session["user_id"])
    return redirect("/ingredients")