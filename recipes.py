from db import db

def get_all_recipe_names():
    result = db.session.execute("SELECT name FROM recipes")
    return result.fetchall()


def get_all_recipe_info():
    result = db.session.execute("SELECT r.name, r.added_by, u.username, r.total_kcal, r.comment_amount FROM recipes r LEFT JOIN users u ON r.added_by=u.id ORDER BY comment_amount")
    return result.fetchall()

def get_all_recipe_names_limit3():
    result = db.session.execute("SELECT name FROM recipes LIMIT 3")
    return result.fetchall()

def get_recipe_id_with_name(name: str):
    sql_recipe_id = "SELECT id FROM recipes WHERE name=:name"
    recipe_id_result = db.session.execute(sql_recipe_id, {"name":name})
    return recipe_id_result.fetchone()[0]

def get_recipe_data_with_name(name: str):
    sql_recipe_id = "SELECT id, name, total_kcal FROM recipes WHERE name=:name"
    recipe_id_result = db.session.execute(sql_recipe_id, {"name":name})
    return recipe_id_result.fetchone()

def get_recipe_count():
    result = db.session.execute("SELECT COUNT(name) from recipes")
    return result.fetchone()[0]

def add_recipe_and_return_id(name: str, user_id: int):
    sql_recipe = "INSERT INTO recipes (name, added_by) VALUES (:name, :added_by) RETURNING id"
    result = db.session.execute(sql_recipe, {"name":name, "added_by":user_id})
    db.session.commit()
    return result.fetchone()[0]

def get_users_recipes(user_id: int):
    sql_meals = """SELECT r.name, r.total_kcal FROM recipes r, users_recipes ur 
        WHERE user_id=:user_id AND r.id = ur.recipe_id AND ur.visible=true"""
    result_meals = db.session.execute(sql_meals, {"user_id":user_id})
    return result_meals.fetchall()

def add_recipe_to_meal_plan(user_id: int, recipe_id: int):
    sql_add_to_plan = "INSERT INTO users_recipes (user_id, recipe_id) VALUES (:user_id, :recipe_id)"
    db.session.execute(sql_add_to_plan, {"user_id":user_id, "recipe_id":recipe_id})
    db.session.commit()
    sql_set_visibility = "UPDATE users_recipes SET visible=true WHERE user_id=:user_id AND recipe_id=:recipe_id"
    db.session.execute(sql_set_visibility, {"user_id":user_id, "recipe_id":recipe_id})
    db.session.commit()

def add_recipe_with_ingredients(amount: int, recipe_id: int, ingredient_id: int):
    sql_recipe_ingredients = "INSERT INTO recipes_ingredients (amount, recipe_id, ingredient_id) VALUES (:amount, :recipe_id, :ingredient_id)"
    db.session.execute(sql_recipe_ingredients, {"amount":amount, "recipe_id":recipe_id, "ingredient_id":ingredient_id})

def update_recipe_total_kcal(total_kcal: float, recipe_id: int):
    sql_update_recipe = "UPDATE RECIPES SET total_kcal=:total_kcal WHERE id=:recipe_id"
    db.session.execute(sql_update_recipe, {"total_kcal":total_kcal, "recipe_id":recipe_id})
    db.session.commit()