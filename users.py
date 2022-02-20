from db import db

def get_user_id_with_username(username: str):
    sql_user_id = "SELECT id FROM users WHERE username=:username"
    user_id_result = db.session.execute(sql_user_id, {"username":username})
    return user_id_result.fetchone()[0]

def add_user(
            first_name: str,
            last_name: str,
            username: str,
            hash_value: str,
            height: int,
            weight: float,
            age: int,
            gender: str,
            bmr: float
            ):
    sql = """INSERT INTO users (first_name, last_name, username,
        password, height, weight, age, gender, bmr) 
        VALUES (:first_name, :last_name, :username, :password,
        :height, :weight, :age, :gender, :bmr)"""
    db.session.execute(sql, {"first_name":first_name, "last_name":last_name, "username":username, "password":hash_value, "height":height, "weight":weight, "age":age, "gender":gender, "bmr":bmr })
    db.session.commit()

def get_one_user(username: str):
    sql = """SELECT id, first_name, last_name,
        username, height, weight, age, gender, admin, bmr 
        FROM users WHERE username=:username"""
    result = db.session.execute(sql, {"username":username})
    return result.fetchone()

def get_total_kcal_for_user(user_id: int):
    sql = """select sum(total_kcal)
        FROM users_recipes ur LEFT JOIN recipes r 
        ON ur.recipe_id = r.id WHERE user_id=:user_id AND ur.visible=true"""
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()[0]

def get_all_usernames():
    result = db.session.execute("SELECT username FROM users")
    return result.fetchall()

def remove_meal_from_plan(user_id: int, recipe_id: int):
    sql = """UPDATE users_recipes SET visible=false
        WHERE user_id=:user_id AND recipe_id=:recipe_id"""
    db.session.execute(sql, {"user_id":user_id, "recipe_id":recipe_id})
    db.session.commit()