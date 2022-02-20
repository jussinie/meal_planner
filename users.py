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
    sql = "INSERT INTO users (first_name, last_name, username, password, height, weight, age, gender, bmr) VALUES (:first_name, :last_name, :username, :password, :height, :weight, :age, :gender, :bmr)"
    db.session.execute(sql, {"first_name":first_name, "last_name":last_name, "username":username, "password":hash_value, "height":height, "weight":weight, "age":age, "gender":gender, "bmr":bmr })
    db.session.commit()