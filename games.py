import db


def post_result(home_id, away_id, winner_id):
    sql = """INSERT INTO games (home_id, away_id, winner_id)
                VALUES (?, ?, ?)"""
    db.execute(sql, [home_id, away_id, winner_id])


def get_latest_games():
    sql = """SELECT home_id,
                    away_id,
                    winner_id
                FROM games
                ORDER BY home_id DESC limit 20"""
    return db.query(sql)


def games_count():
    sql = """COUNT(*) FROM games"""
    return db.query(sql)
