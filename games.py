import db


def post_result(home_id, away_id, winner_id):
    sql = """INSERT INTO games (home_id, away_id, winner_id)
                VALUES (?, ?, ?)"""
    db.execute(sql, [home_id, away_id, winner_id])


def get_games():
    sql = """SELECT home_id,
                    away_id,
                    winner_id
                FROM games"""
    return db.query(sql)
