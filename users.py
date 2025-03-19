import db


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
