from db import db

def get_one_ingredient_with_id(ingredient_id: int):
    kcal_sql = "SELECT kcal FROM ingredients WHERE id=:ingredient_id"
    return db.session.execute(kcal_sql, {"ingredient_id":ingredient_id})

def get_one_ingredient_with_name(ingredient: str):
    sql_ingredient_id = "SELECT id, name FROM ingredients WHERE name=:ingredient"
    sql_ingredient_id_result = db.session.execute(sql_ingredient_id, {"ingredient":ingredient})
    return sql_ingredient_id_result.fetchone()[0]

def get_ingredient_names():
    result = db.session.execute("SELECT name FROM ingredients")
    return result.fetchall()

def get_all_ingredients_for_recipe(name: str):
    sql = "SELECT r.name as recipe_name, i.name as ingredient_name, i.kcal, i.carbs, i.protein, i.fat, i.salt, ri.amount, r.id, r.total_kcal FROM recipes r, ingredients i, recipes_ingredients ri WHERE r.name=:name AND r.id = ri.recipe_id AND i.id = ri.ingredient_id"
    result = db.session.execute(sql, {"name":name})
    return result.fetchall()

def add_ingredient(name, kcal, carbs, protein, fat, salt, user_id):
    sql = "INSERT INTO ingredients (name, kcal, carbs, protein, fat, salt, approved, added_by_user_id) VALUES (:name, :kcal, :carbs, :protein, :fat, :salt, false, :user_id)"
    db.session.execute(sql, {"name":name, "kcal":kcal, "carbs":carbs, "protein":protein, "fat":fat, "salt":salt, "user_id":user_id})
    db.session.commit()

def set_ingredient_as_approved(ingredient_id: int):
    sql_approve_ingredient = "UPDATE ingredients SET approved=true WHERE id=:id"
    db.session.execute(sql_approve_ingredient, {"id":ingredient_id})
    db.session.commit()

def remove_ingredient(ingredient_id: int):
    sql_cancel_adding_ingredient = "DELETE FROM ingredients WHERE id=:id"
    db.session.execute(sql_cancel_adding_ingredient, {"id":ingredient_id})
    db.session.commit()

def cancel_approval(ingredient_id: int):
    sql_cancel_adding_ingredient = "DELETE FROM ingredients WHERE id=:id"
    db.session.execute(sql_cancel_adding_ingredient, {"id":ingredient_id})
    db.session.commit()

def approved_ingredient_count():
    result = db.session.execute("SELECT COUNT(name) from ingredients WHERE approved=true")
    return result.fetchone()[0]

def get_approved_ingredients():
    result = db.session.execute("SELECT name, kcal, carbs, protein, fat, salt FROM ingredients WHERE approved=true")
    return result.fetchall()

def get_non_approved_ingredients():
    result_not_approved = db.session.execute("SELECT id, name, kcal, carbs, protein, fat, salt FROM ingredients WHERE approved=false")
    return result_not_approved.fetchall()

def get_non_approved_ingredients_from_user(user_id: int):
    sql_ingredient_added_by_user = "SELECT id, name, kcal, carbs, protein, fat, salt FROM ingredients WHERE approved=false AND added_by_user_id=:user_id"
    result_not_approved_user = db.session.execute(sql_ingredient_added_by_user, {"user_id":user_id})
    return result_not_approved_user.fetchall()