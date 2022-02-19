from db import db

def get_all_recipe_names():
    result = db.session.execute("SELECT name FROM recipes")
    return result.fetchall()