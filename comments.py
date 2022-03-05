from db import db

def add_comment(user_id: int, recipe_id: int, comment: str):
    sql_comment = """INSERT INTO comments (user_id, recipe_id, content, sent_at)
        VALUES (:user_id, :recipe_id, :comment, NOW())"""
    db.session.execute(sql_comment, {"user_id":user_id, "recipe_id":recipe_id, "comment":comment})
    db.session.commit()
    sql_comment_amount = "SELECT COUNT(recipe_id) FROM comments WHERE recipe_id=:recipe_id"
    comment_amount = db.session.execute(sql_comment_amount, {"recipe_id":recipe_id})
    nr_of_comments = comment_amount.fetchone()[0]
    sql_update_amnt = "UPDATE recipes SET comment_amount=:nr_of_comments WHERE id=:recipe_id"
    db.session.execute(sql_update_amnt, {"nr_of_comments":nr_of_comments, "recipe_id":recipe_id})
    db.session.commit()

def get_all_comments(recipe_id: int):
    sql_comments = """SELECT c.content, c.sent_at, u.first_name, u.last_name
        FROM comments c LEFT JOIN users u ON u.id=user_id 
        WHERE recipe_id=:recipe_id ORDER BY c.sent_at"""
    return db.session.execute(sql_comments, {"recipe_id":recipe_id})
