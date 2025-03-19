import db
from werkzeug.security import generate_password_hash, check_password_hash


def get_user(user_id):
    sql = """SELECT id, username
                FROM users
                WHERE users.id = ?"""
    result = db.query(sql, [user_id])
    return result[0] if result else None


def get_teams(user_id):
    sql = """SELECT id,
                    team
                FROM teams
                WHERE teams.owner = ?"""
    return db.query(sql, [user_id])


def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])


def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])[0]
    if not result:
        return None
    user_id = result["id"]
    password_hash = result["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    else:
        return None
