from db import db

def get_user(username: str):
    sql_user = "SELECT id FROM users WHERE username=:username"
    user_result = db.session.execute(sql_user, {"username":username})
    return user_result.fetchone()[0]

def get_ingredient_names():
    result = db.session.execute("SELECT name FROM ingredients")
    return result.fetchall()

def add_ingredient(name, kcal, carbs, protein, fat, salt, user_id):
    sql = "INSERT INTO ingredients (name, kcal, carbs, protein, fat, salt, approved, added_by_user_id) VALUES (:name, :kcal, :carbs, :protein, :fat, :salt, false, :user_id)"
    db.session.execute(sql, {"name":name, "kcal":kcal, "carbs":carbs, "protein":protein, "fat":fat, "salt":salt, "user_id":user_id})
    db.session.commit()

def set_ingredient_as_approved(id: int):
    sql_approve_ingredient = "UPDATE ingredients SET approved=true WHERE id=:id"
    db.session.execute(sql_approve_ingredient, {"id":id})
    db.session.commit()

def remove_ingredient(id: int):
    sql_cancel_adding_ingredient = "DELETE FROM ingredients WHERE id=:id"
    db.session.execute(sql_cancel_adding_ingredient, {"id":id})
    db.session.commit()

def cancel_approval(id: int):
    sql_cancel_adding_ingredient = "DELETE FROM ingredients WHERE id=:id"
    db.session.execute(sql_cancel_adding_ingredient, {"id":id})
    db.session.commit()

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